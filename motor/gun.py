"""Bir sira-gunun bolum akisi (tekrar oynatma): emir toplama -> eslestirme -> surekli islem -> ... -> gun sonu.

Bolum gecisleri ve muzayede eslestirme anlari veriden alinir (TASARIM.md 4.3). Her bolumde yalniz girdi olaylari
motora verilir; islemler motor tarafindan uretilir.
- Emir toplama bolumleri (acilis, kapanis, devre kesici, EBDKS tek fiyat, gun ici tek fiyat) ve EBDKS durdurmasi:
  emirler toplanir, eslestirme yapilmaz (TekFiyat).
- Eslestirme: veride eslestirme bolumu satiri varsa o anda; yoksa toplamadan surekli isleme / kapanis fiyatindan
  islemlere geciste. Toplamadan baska bir toplamaya geciste (devre kesicinin kapanisa tasmasi, acilistan EBDKS
  durdurmasina) eslestirme yapilmaz.
- Fiyat sinirlari: gunluk marj; kapanis muzayedesinde ayrica son islem fiyatinin +-%3'u (03 madde 72).
- Surekli islem: pay bazinda devre kesici esigi (son muzayede fiyati, yoksa baz; oran ve yon tarih parametresi;
  ice yuvarlanir). Esigin otesindeki seviyelerle eslesilmez; esigin otesinde eslesecek gelen emrin kalani iptal
  edilir ve devre kesici tetiklenir. Tetiklemeden sonraki olaylar emir toplama olarak islenir; bolum suresi veriden gelir
  (06-devre-kesici.md).
- Kapanis fiyatindan islemler: butun islemler kapanis fiyatindan (03 madde 86-88).
Girdi olaylari: yeni emir (6), degisiklik (5), iptal (1) ve dissal sistem iptalleri (116 surekli islemde, 117 EBDKS
durdurmasinda; veride gorulen alanlardan turetilemez).
Enjeksiyon (TASARIM.md 4.1, 5): sentetik olaylar zamanlarina gore bolume yerlesir (bolum, verideki bir sonraki bolumun
ilk satirina kadar surer); her biri o anki bolum ve defter durumuyla dogrulanir (dogrulama.py), reddedilenler
`reddedilen` listesine yazilir. Gercek akis disssal kabul edilir: gercek katilimcilar enjeksiyona tepki vermez.
"""
import collections

from . import veri, parametreler
from .defter import Defter
from .dogrulama import Dogrulayici
from .emir import Iptal
from .surekli_islem import SurekliIslem
from .tek_fiyat import TekFiyat
from tek_fiyat_algoritma import GRUP_TABLO, yukari_adim, asagi_adim

DURDURMA = ("P_GECICI_DURDUR_EBDK", "P_GECICI_DUR_EBDK_KT", "P_GECICI_DUR_EBDK_SI")
TOPLAMA = veri.ACILIS_TOPLAMA + veri.KAPANIS_TOPLAMA + DURDURMA + (
    "P_DK_TEKFIY_EMIR_TPL", "P_DK_TEKFIY_EMR_TPL2", "P_TF_EMIR_TPL_EBDK", "P_TF_EMIR_TPL2_EBDK",
    "P_TEKFIYAT_EMIR_TPL", "P_TEKFIYAT_EMIR_TPL2")
DISSAL_IPTAL = (116, 117)


def kategori(seans):
    if seans in TOPLAMA:
        return "toplama"
    if seans in veri.ESLESTIRME:
        return "eslestirme"
    if seans == veri.SUREKLI:
        return "surekli"
    if seans == veri.KAPANIS_FIYATI:
        return "kfi"
    if seans == "P_GUNSONU":
        return "gunsonu"
    return "diger"


def kosular(df):
    """Zaman sirasinda ayni bolumdeki ardisik satir kosulari: [(seans, bas, bit)]."""
    s = df.sort_values("zaman", kind="stable")
    out = []
    for sn, z in zip(s["seans"].to_numpy(), s["zaman"].to_numpy()):
        if out and out[-1][0] == sn:
            out[-1][2] = int(z)
        else:
            out.append([sn, int(z), int(z)])
    return out


class Gun:
    def __init__(self, df, gun, kod, gunsonu, tepe):
        self.df, self.gun, self.tepe = df, gun, tepe
        grup, self.pazar, self.baz = veri.sira_bilgisi(gunsonu, gun, kod)
        self.tablo = GRUP_TABLO.get(grup)
        if self.tablo is None or self.baz is None:
            raise ValueError(f"{kod} {gun}: fiyat adimi tablosu ya da baz fiyat yok")
        marj = parametreler.deger("fiyat_marji", gun, self.pazar)
        self.taban = yukari_adim(self.baz * (1 - marj), self.tablo)
        self.tavan = asagi_adim(self.baz * (1 + marj), self.tablo)
        self.referans = self.baz if parametreler.satir("tek_fiyat_adim4_referansi", gun)["deger"] == "baz" else None
        try:
            self.dk_oran = parametreler.deger("dk_tetikleme_orani", gun, self.pazar)
            self.dk_yon = parametreler.satir("dk_yon", gun, self.pazar)["deger"]
        except KeyError:
            self.dk_oran, self.dk_yon = None, None
        try:
            aciga = parametreler.satir("aciga_satis_kapsami", gun)["deger"]
        except KeyError:
            aciga = None
        izinli = bool(((df["emir_turu"] & 2) != 0).any())   # BIST 50 listesi yok: veride aciga satis gorulen sira
        self.dogrulayici = Dogrulayici(self.tablo, self.taban, self.tavan, aciga, izinli)
        self.islemler = []           # (bolum, Islem)
        self.reddedilen = []         # (sentetik olay, bolum, sebep)
        self.sentetik_nolar = set()
        self.muzayedeler = []        # (eslestirme ani, bolum, denge sonucu)
        self.anlik = []              # (eslestirme ani, {emir_no: (alis, fiyat, kalan, fiyat_turu)}) tani icin
        self.sayac = collections.Counter()

    def _olaylar(self, bas, bit, seanslar):
        olaylar, _ = veri.eylemler(self.df, bas, bit + 1, self.tepe, seanslar)
        d = self.df
        s = d[d["seans"].isin(seanslar) & d["kapsam"] & d["degisiklik_sebebi"].isin(DISSAL_IPTAL)
              & (d["zaman"] >= bas) & (d["zaman"] <= bit)]
        olaylar += [Iptal(int(z), n) for z, n in zip(s["zaman"], s["emir_no"])]
        self.sayac["dissal_iptal"] += len(s)
        return sorted(olaylar, key=lambda o: o.zaman)

    def _dk_siniri(self, ref):
        if self.dk_oran is None or ref is None:
            return None, None
        alt = yukari_adim(ref * (1 - self.dk_oran), self.tablo)
        ust = asagi_adim(ref * (1 + self.dk_oran), self.tablo) if self.dk_yon == "iki_yon" else None
        return alt, ust

    def sentetik_mi(self, islem):
        return islem.alis_no in self.sentetik_nolar or islem.satis_no in self.sentetik_nolar

    def calistir(self, sentetik=()):
        sentetik = sorted(sentetik, key=lambda o: o.zaman)
        self.sentetik_nolar = {o.no for o in sentetik}
        kos = kosular(self.df)
        sinir = [b for _, b, _ in kos[1:]] + [None]          # bolum penceresi: [bas, sonraki bolumun basi)
        si = 0

        def sentetikler(k):
            nonlocal si
            out = []
            while si < len(sentetik) and (sinir[k] is None or sentetik[si].zaman < sinir[k]):
                out.append(sentetik[si])
                si += 1
            return out

        def birlestir(gercek, sent):
            return sorted([(o.zaman, 0, o) for o in gercek] + [(o.zaman, 1, o) for o in sent], key=lambda x: x[:2])

        tf, defter, surekli = TekFiyat(), None, None
        toplama_turleri, son_fiyat, ref_muzayede, kapanis_fiyati = set(), None, None, None
        bekleyen = True   # toplanmis ve henuz eslestirilmemis emir defteri var mi

        def eslestir(M, bolum):
            nonlocal tf, defter, bekleyen, son_fiyat, ref_muzayede, kapanis_fiyati
            alt, ust = self.taban, self.tavan
            kapanis = bool(toplama_turleri & set(veri.KAPANIS_TOPLAMA))
            if kapanis and son_fiyat:
                bant = parametreler.deger("kapanis_seansi_fiyat_bandi", self.gun)
                alt = max(alt, yukari_adim(son_fiyat * (1 - bant), self.tablo))
                ust = min(ust, asagi_adim(son_fiyat * (1 + bant), self.tablo))
            self.anlik.append((M, {e.no: (e.alis, e.fiyat, e.kalan, e.fiyat_turu) for e in tf.emirler.values()}))
            sonuc, isl, kalan = tf.eslestir(M, self.tablo, alt, ust, self.referans)
            self.islemler += [(bolum, i) for i in isl]
            self.muzayedeler.append((M, bolum, sonuc))
            for k, v in tf.sayac.items():
                self.sayac["toplama_" + k] += v
            if sonuc.get("fiyat") is not None:
                ref_muzayede = sonuc["fiyat"]
                if isl:
                    son_fiyat = sonuc["fiyat"]
            if kapanis:
                kapanis_fiyati = sonuc.get("fiyat") if isl else son_fiyat
            defter = Defter()
            for e in kalan:
                defter.ekle(e)
            tf, bekleyen = None, False
            toplama_turleri.clear()

        def gecerli(o, sentetik_mi, bolum, mevcut):
            if not sentetik_mi:
                return True
            r = self.dogrulayici.kontrol(o, bolum, mevcut.get(o.no), son_fiyat, kapanis_fiyati)
            if r:
                self.reddedilen.append((o, bolum, r))
            return r is None

        for k, (seans, bas, bit) in enumerate(kos):
            kat = kategori(seans)
            sent = sentetikler(k)
            if kat == "toplama":
                if tf is None:
                    tf = TekFiyat((defter.emirler.values() if defter is not None else ()))
                    defter, surekli = None, None
                bekleyen = True
                toplama_turleri.add(seans)
                for _, s_, o in birlestir(self._olaylar(bas, bit, (seans,)), sent):
                    if gecerli(o, s_, seans, tf.emirler):
                        tf.isle(o)
            elif kat == "eslestirme":
                if bekleyen and tf is not None:
                    eslestir(bas, seans)
                for o in sent:
                    self.reddedilen.append((o, seans, "eslestirme_bolumu"))
            elif kat in ("surekli", "kfi"):
                if tf is not None:
                    eslestir(bas - 1, "eslestirme_satirsiz")
                if kat == "surekli":
                    alt, ust = self._dk_siniri(ref_muzayede if ref_muzayede is not None else self.baz)
                    surekli = SurekliIslem(defter, alt_sinir=alt, ust_sinir=ust)
                else:
                    surekli = SurekliIslem(defter, sabit_fiyat=kapanis_fiyati if kapanis_fiyati is not None else son_fiyat)
                n = len(surekli.islemler)
                for _, s_, o in birlestir(self._olaylar(bas, bit, (seans,)), sent):
                    if tf is not None:
                        if gecerli(o, s_, "P_DK_TEKFIY_EMIR_TPL", tf.emirler):
                            tf.isle(o)  # devre kesici tetiklendi: veride bolum adi henuz degismemis olabilir
                        continue
                    if not gecerli(o, s_, seans, surekli.defter.emirler):
                        continue
                    surekli.isle(o)
                    if surekli.dk_tetiklendi:
                        tf, defter = TekFiyat(surekli.defter.emirler.values()), None
                        bekleyen = True
                        toplama_turleri.add("P_DK_TEKFIY_EMIR_TPL")
                        self.sayac["dk_tetikleme"] += 1
                yeni = surekli.islemler[n:]
                self.islemler += [(seans, i) for i in yeni]
                if yeni:
                    son_fiyat = yeni[-1].fiyat
                for k, v in surekli.sayac.items():
                    self.sayac[kat + "_" + k] += v
            elif kat == "gunsonu":
                self.reddedilen += [(o, seans, "gun_sonu") for o in sent + sentetik[si:]]
                break
            else:
                self.sayac["bilinmeyen_bolum_" + seans] += 1
                self.reddedilen += [(o, seans, "bilinmeyen_bolum") for o in sent]
        return self.islemler
