"""Hisseye gore ayarli sentetik senaryolar (senaryo-tasarimi.md 5). Parametreler payin profilinden (pay_profili.py) ve
dedektor esiklerinden (3 adim, 60 sn, z >= 3) bagimsiz araliklardan cekilir; aralik sinirlari ve dayanaklari
senaryo-tasarimi.md 5'tedir ([varsayim] olanlar orada isaretli).

- Yaniltici emir: bant (0 / 1-2 / 3-6 / 7-10 adim; cagiranin sirasina gore esit sayida) icinde uzaklik payin buyuk emir
  uzaklik dagilimindan; 1-5 ardisik katman, her biri payin buyuk emirlerinden (>= %90 yuzdelik); omur 5-300 sn
  (log-duzgun); 1-5 dongu, aralar 1-10 dk, her dongude %50 yon degisimi; karsi emir (piyasadan limite KIE) dongu
  omrunun ortasinda, payin emir boyu %50-%90 araligindan.
  Gerceklesme yaklasinca iptal: motor sahte emre tepki vermez; katmanin islem gordugu an enjeksiyonlu kosunun kendisinden
  bilinir. Islem goren parca dolumdan TEPKI_SN once iptal edilir, BEKLEME_SN sonra ayni uzakliktan (o anki en iyi
  fiyata gore) yeniden girilir; en cok PLAN_TUR kez yeniden planlanir. Kalan dolum temizlik olcutuyle (katman toplaminin
  %1'i, sentetik_degerlendir.KATMAN_DOLUM_EN_COK) degerlendirilir.
- Fiyat yukseltme: 5-30 agresif alis (piyasa emri, KIE; kademeleri miktari bitene kadar supurur), aralar ustel
  (ortalama 10-60 sn); boy karsi tarafin ilk 5 kademe miktari ortancasinin k/5'i, yani yaklasik k kademe (k = 1-3;
  enjeksiyondan onceki 30 dk defter ornekleri). Piyasadan limite emir yalniz en iyi kademede islem gordugu icin k > 1
  anlamsiz olurdu (duman testi, 29.10.2026). Etki: senaryo sonunda
  enjeksiyonlu ve taban kosunun son islem fiyati farki (tekrar oynatma tepki vermedigi icin bu fark senaryonun etkisidir).
- Karsilikli islem: 3-30 tekrar, aralar ustel (ortalama 30-300 sn); boy turu (cagiranin sirasina gore yari yariya)
  "karisan" (payin islem boyu %50-%90 araligi) ya da "goze_batan" (%99 yuzdeligin ustundeki islemlerden).
- Kapanis etkileme: boy payin kapanis emir toplama ortancasinin 0,5-3 kati (log-duzgun); giris kapanis eslestirmesinden
  0-300 sn once; fiyat son islemin +-%3 bant ucu (eskisiyle ayni).
Profil yoksa (pay_profili.profil None) boylar eski H tabanli degerlere duser; kayitta profil_yedek = 2.
Senaryo surekli islemin basindan 30 dk sonra baslar ve kapanis emir toplamadan 5 dk once biter (yarim gunlerde de).
Raporlama icin her vakaya piyasa hareketi (XUTUM, pozitif pencerelerde en buyuk |5 dk getiri|) ve piyasa degeri ceyregi
(onceki ay sonu degerleme dosyasi) yazilir.
"""
import datetime, functools, itertools, math, os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from motor import senaryolar as sn, veri
from motor.gun import Gun, kosular
import pay_profili as pp

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
US = 1_000_000
BANT_SIRASI = ["0", "1-2", "3-6", "7-10"]
BANTLAR = {"0": (0, 0), "1-2": (1, 2), "3-6": (3, 6), "7-10": (7, 10)}
KATMAN = (1, 5)
OMUR_SN = (5, 300)            # log-duzgun
DONGU = (1, 5)
ARA_SN = (60, 600)            # donguler arasi
YON_DEGIS = 0.5
TEPKI_SN = 1.0
BEKLEME_SN = (1, 5)
PLAN_TUR = 5
KATMAN_DOLUM_EN_COK = 0.01    # sentetik_degerlendir ile ayni
KENDI_ISLEM_EN_AZ = 0.5       # sentetik_degerlendir ile ayni
YUKSELTME_ADET = (5, 30)
YUKSELTME_ARA_SN = (10, 60)
YUKSELTME_K = (1, 3)
KARSILIKLI_TEKRAR = (3, 30)
KARSILIKLI_ARA_SN = (30, 300)
KARSILIKLI_TURLER = ["karisan", "goze_batan"]
KAPANIS_KAT = (0.5, 3.0)
KAPANIS_SON_SN = 300
BAS_PAY_SN, SON_PAY_SN = 1800, 300
# gercekci agirlik (kor_nokta.py): SPK vakalarinda kisa omurlu buyuk emirlerin uzaklik dagilimi, rapor.md 9.2'deki ALKLC
# donem, ENSRI etiket ve VKFYO etiket satirlarinin ortalamasi; 7+ kovasi 7-10 bandina yazildi (kaba, [varsayim])
GERCEKCI_AGIRLIK = {"0": 0.586, "1-2": 0.088, "3-6": 0.087, "7-10": 0.239}


def log_duzgun(rng, a, b):
    return float(math.exp(rng.uniform(math.log(a), math.log(b))))


def zaman_araligi(df):
    """Senaryonun yerlesebilecegi [ilk, son] (us): surekli islemin basindan BAS_PAY_SN sonra, kapanis emir toplamadan
    SON_PAY_SN once. Surekli islem yoksa (tek fiyatla islem goren pay, or. KLNMA.E 19.03.2025) None."""
    kos = kosular(df)
    bas = next((b for s, b, _ in kos if s == veri.SUREKLI), None)
    if bas is None:
        return None
    kap = next((b for s, b, _ in kos if s.startswith("P_KAPANIS_EMIR")), None)
    son = kap if kap is not None else max(e for s, _, e in kos if s == veri.SUREKLI)
    return bas + BAS_PAY_SN * US, son - SON_PAY_SN * US


def _baslangic(rng, ilk, son, sure_us):
    return int(rng.integers(ilk, son - sure_us)) if son - ilk > sure_us + 1 else None


def _kos(ctx, olaylar):
    g1 = Gun(ctx["df"], ctx["gun"], ctx["kod"], ctx["gunsonu"], ctx["tepe"])
    g1.calistir(olaylar)
    return g1


def yaniltici(g0, ctx, rng, sira):
    prof, tablo = ctx["profil"], g0.tablo
    bant = BANT_SIRASI[sira % len(BANT_SIRASI)]
    lo, hi = BANTLAR[bant]
    u = prof["buyuk_uzaklik"] if prof else np.array([], dtype=int)
    u = u[(u >= lo) & (u <= hi)]
    d = int(rng.choice(u)) if len(u) else int(rng.integers(lo, hi + 1))
    K = int(rng.integers(KATMAN[0], KATMAN[1] + 1))
    omur = log_duzgun(rng, *OMUR_SN)
    D = int(rng.integers(DONGU[0], DONGU[1] + 1))
    aralar = [float(rng.uniform(*ARA_SN)) for _ in range(D - 1)]
    ilk, son = ctx["aralik"]
    while D > 1 and (D * omur + sum(aralar[:D - 1])) * US >= son - ilk:
        D -= 1
    t = _baslangic(rng, ilk, son, int((D * omur + sum(aralar[:D - 1])) * US))
    if t is None:
        return None
    yon = bool(rng.integers(2))
    boylar = [int(rng.choice(prof["buyuk_boy"])) if prof else max(1, int(ctx["H"] * 0.02)) for _ in range(K)]
    karsi = int(rng.uniform(prof["emir_q50"], prof["emir_q90"])) if prof else max(1, int(ctx["H"] * 0.002))
    karsi = max(1, karsi)
    bekleme = int(rng.uniform(*BEKLEME_SN) * US)
    sayac = itertools.count(1)
    kat = {}                      # emir no -> katman sirasi (yeniden giriste uzaklik korunur)

    def yeni_no(k):
        no = sn._no("yaniltici", next(sayac))
        kat[no] = k
        return no

    def ref(z):
        return sn.son_fiyat(ctx["sirali"], z) or g0.baz

    bolumler, karsilar, tc, yon_degisim = [], [], t, 0
    for c in range(D):
        if c and rng.random() < YON_DEGIS:
            yon, yon_degisim = not yon, yon_degisim + 1
        ea, es = sn.en_iyi_fiyatlar(g0.defter_ornekleri, tc)
        en_iyi = (ea if yon else es) or ref(tc)
        bit = tc + int(omur * US)
        for k, p in enumerate(sn.katman_fiyatlari(en_iyi, tablo, yon, d, K)):
            bolumler.append((yeni_no(k), yon, p, boylar[k], tc + k, bit))
        karsilar.append((sn._no("yaniltici", next(sayac)), tc + int(omur * US / 2), not yon, karsi))
        if c < D - 1:
            tc = bit + int(aralar[c] * US)

    def yeni_fiyat(eski, alis, z, p):
        ea, es = sn.en_iyi_fiyatlar(g0.defter_ornekleri, z)
        e = ea if alis else es
        return sn.katman_fiyatlari(e, tablo, alis, d + kat[eski], 1)[0] if e else p

    for tur in range(PLAN_TUR + 1):
        olaylar = sn.plan_olaylari(bolumler, karsilar)
        g1 = _kos(ctx, olaylar)
        kn = {b[0] for b in bolumler}
        dolum = {}
        for _, i in g1.islemler:
            for no in (i.alis_no, i.satis_no):
                if no in kn and no not in dolum:
                    dolum[no] = i.zaman
        if not dolum or tur == PLAN_TUR:
            break
        bolumler = sn.bolum_bol(bolumler, dolum, int(TEPKI_SN * US), bekleme, yeni_fiyat, lambda eski: yeni_no(kat[eski]))
    kn = {b[0] for b in bolumler}
    dolan = sum(i.adet for _, i in g1.islemler if i.alis_no in kn or i.satis_no in kn)
    toplam = sum(b[3] for b in bolumler)
    kayit = dict(bant=bant, uzaklik=d, uzaklik_dagilimdan=int(len(u) > 0), katman=K, boy_ort=float(np.mean(boylar)),
                 boy_orani=float(np.mean(boylar)) / prof["emir_q99"] if prof else np.nan, omur_sn=round(omur, 1),
                 dongu=D, yon_degisim=yon_degisim, karsi_boy=karsi, plan_tur=tur, parca=len(bolumler),
                 yeniden_giris=len(bolumler) - D * K, katman_toplam=toplam, temizlik_olcusu=dolan)
    return dict(g1=g1, olaylar=olaylar, kayit=kayit, temiz=dolan <= KATMAN_DOLUM_EN_COK * toplam)


def _araliklar(rng, n, ort_sn, en_az_sn):
    return [max(en_az_sn, float(x)) for x in rng.exponential(ort_sn, n - 1)]


def yukseltme(g0, ctx, rng, sira):
    n = int(rng.integers(YUKSELTME_ADET[0], YUKSELTME_ADET[1] + 1))
    ort = float(rng.uniform(*YUKSELTME_ARA_SN))
    ara = _araliklar(rng, n, ort, 1.0)
    ilk, son = ctx["aralik"]
    while n > 1 and sum(ara[:n - 1]) * US >= son - ilk:
        n -= 1
    ara = ara[:n - 1]
    t = _baslangic(rng, ilk, son, int(sum(ara) * US))
    if t is None:
        return None
    zamanlar = [t] + [t + int(x * US) for x in np.cumsum(ara)]
    dp = pp.defter_profili(g0.defter_ornekleri, t, g0.tablo)
    k = int(rng.integers(YUKSELTME_K[0], YUKSELTME_K[1] + 1))
    q = max(1, int(dp["derinlik_satis"] * k / 5)) if dp and dp["derinlik_satis"] > 0 else max(1, int(ctx["H"] * 0.005))
    olaylar = sn.fiyat_yukseltme_ayarli(zamanlar, [q] * n)
    g1 = _kos(ctx, olaylar)
    son_t = zamanlar[-1] + 1
    p0 = sn.son_fiyat(ctx["sirali"], son_t)
    p1 = sn.son_fiyat(sorted((i for _, i in g1.islemler), key=lambda i: i.zaman), son_t)
    kayit = dict(adet=n, ara_ort_sn=round(ort, 1), k=k, boy=q, boy_kaynak="defter" if dp else "H",
                 makas=dp["makas"] if dp else np.nan, etki=(p1 / p0 - 1) if p0 and p1 else np.nan,
                 sure_sn=round(sum(ara), 1))
    return dict(g1=g1, olaylar=olaylar, kayit=kayit, temiz=True)


def karsilikli(g0, ctx, rng, sira):
    prof = ctx["profil"]
    tur = KARSILIKLI_TURLER[sira % len(KARSILIKLI_TURLER)]
    n = int(rng.integers(KARSILIKLI_TEKRAR[0], KARSILIKLI_TEKRAR[1] + 1))
    ort = float(rng.uniform(*KARSILIKLI_ARA_SN))
    ara = _araliklar(rng, n, ort, 5.0)
    ilk, son = ctx["aralik"]
    while n > 1 and (sum(ara[:n - 1]) + 60) * US >= son - ilk:
        n -= 1
    ara = ara[:n - 1]
    t = _baslangic(rng, ilk, son, int((sum(ara) + 60) * US))
    if t is None:
        return None
    zamanlar = [t] + [t + int(x * US) for x in np.cumsum(ara)]
    if prof and not np.isnan(prof["islem_q50"]):
        if tur == "karisan":
            boylar = [max(1, int(rng.uniform(prof["islem_q50"], prof["islem_q90"]))) for _ in range(n)]
        else:
            ust = prof["islem_boy"][prof["islem_boy"] >= prof["islem_q99"]]
            boylar = [max(1, int(rng.choice(ust))) for _ in range(n)]
    else:
        boylar = [max(1, int(ctx["H"] * 0.005))] * n
    refler = [sn.son_fiyat(ctx["sirali"], z) or g0.baz for z in zamanlar]
    olaylar = sn.karsilikli_islem_ayarli(zamanlar, boylar, refler, g0.tablo, g0.defter_ornekleri)
    g1 = _kos(ctx, olaylar)
    ki = sn.kendi_islem(g1)
    satis = sum(o.miktar for o in olaylar if not o.alis)
    kayit = dict(boy_turu=tur, tekrar=n, ara_ort_sn=round(ort, 1), boy_ort=float(np.mean(boylar)),
                 boy_orani=float(np.mean(boylar)) / prof["islem_q90"] if prof and prof["islem_q90"] else np.nan,
                 temizlik_olcusu=ki, sure_sn=round(sum(ara), 1))
    return dict(g1=g1, olaylar=olaylar, kayit=kayit, temiz=ki >= KENDI_ISLEM_EN_AZ * satis)


def kapanis(g0, ctx, rng, sira):
    prof = ctx["profil"]
    kos = kosular(ctx["df"])
    k = next(j for j, (s, _, _) in enumerate(kos) if s.startswith("P_KAPANIS_EMIR"))
    bas = kos[k][1]
    esl = next((b for s, b, _ in kos[k:] if s in veri.ESLESTIRME), None)
    ref = sn.son_fiyat(ctx["sirali"], bas) or g0.baz
    kat = log_duzgun(rng, *KAPANIS_KAT)
    if prof and prof["kapanis_toplama"] > 0:
        miktar, kaynak = max(1, int(prof["kapanis_toplama"] * kat)), "profil"
    else:
        miktar, kaynak = max(1, int(ctx["H"] * 0.03)), "H"
    ust = ((esl or bas + 240 * US) - bas) // US - 1
    once = int(min(max(1, round(rng.uniform(0, KAPANIS_SON_SN))), max(1, ust)))
    alis = bool(rng.integers(2))
    olaylar = sn.kapanis_etkileme(bas, g0.tablo, ref, alis=alis, miktar=miktar, saniye_once=once, kapanis_eslestirme=esl)
    g1 = _kos(ctx, olaylar)
    kayit = dict(kat=round(kat, 2), boy=miktar, boy_kaynak=kaynak, saniye_once=once, yon_alis=int(alis))
    return dict(g1=g1, olaylar=olaylar, kayit=kayit, temiz=True)


URETICI = {"yaniltici": yaniltici, "yukseltme": yukseltme, "karsilikli": karsilikli, "kapanis": kapanis}


@functools.lru_cache(maxsize=4)
def _xutum(gun, pencere_us):
    f = os.path.join(KOK, "veri", "gun-ici-endeks", f"PP_GUNICITUMENDEKS.M.{gun[:4]}{gun[5:7]}.parquet")
    if not os.path.exists(f):
        return None
    t = pq.read_table(f, columns=["zaman", "deger"],
                      filters=[("tarih", "=", datetime.date.fromisoformat(gun)), ("endeks_kodu", "=", "XUTUM")])
    if t.num_rows == 0:
        return None
    z = pd.Timestamp(gun).value // 1000 + pc.cast(t["zaman"], pa.int32()).to_numpy().astype(np.int64) * 1000
    s = pd.Series(t["deger"].to_numpy(), index=z).sort_index()
    son = s.groupby(s.index // pencere_us * pencere_us).last()
    return np.log(son / son.shift()).abs()


def piyasa_hareketi(gun, pencereler, pencere_us):
    """Pozitif pencerelerde XUTUM'un en buyuk |5 dk log getirisi|; endeks yoksa NaN."""
    r = _xutum(gun, pencere_us)
    if r is None:
        return np.nan
    x = r.reindex(sorted(pencereler)).dropna()
    return float(x.max()) if len(x) else np.nan


@functools.lru_cache(maxsize=4)
def _pd_yuzdelik(ay):
    f = os.path.join(KOK, "veri", "degerleme-orani", f"degoran_M_{ay}.parquet")
    if not os.path.exists(f):
        return {}
    d = pd.read_parquet(f, columns=["tur", "kod", "piyasa_degeri"])
    d = d[d["tur"] == "pay"]
    return dict(zip(d["kod"], d["piyasa_degeri"].rank(pct=True)))


def pd_ceyrek(gun, kod):
    """Onceki ay sonu degerleme dosyasinda payin piyasa degeri ceyregi (1 en kucuk); yoksa NaN."""
    p = pd.Period(gun[:7], "M") - 1
    y = _pd_yuzdelik(f"{p.year}{p.month:02d}").get(kod.split(".")[0])
    return np.nan if y is None else min(4, int(y * 4) + 1)


def uret(senaryo, gunluk, g0, df, gun, kod, gunsonu, tepe, H, rng, sira, pencere_us):
    """Taban kosusu g0 icin senaryoyu kurar ve enjeksiyonlu kosuyu calistirir. sira: bu senaryonun kacinci secimi
    (bant ve boy turu tabakalamasi). Donus: dict(g1, olaylar, kayit, temiz) ya da None (senaryo yerlesemedi)."""
    aralik = zaman_araligi(df)
    if aralik is None and senaryo != "kapanis":
        return None
    prof = pp.profil(gunluk, gun, kod, df, aralik[0] if aralik else None)
    ctx = dict(df=df, gun=gun, kod=kod, gunsonu=gunsonu, tepe=tepe, H=H, profil=prof, aralik=aralik,
               sirali=sorted((i for _, i in g0.islemler), key=lambda i: i.zaman))
    u = URETICI[senaryo](g0, ctx, rng, sira)
    if u is None:
        return None
    pz = {o.zaman // pencere_us * pencere_us for o, _ in u["g1"].kabul}
    u["kayit"] = dict(profil_yedek=2 if prof is None else prof["yedek"],
                      profil_gun=prof["gun_sayisi"] if prof else 0,
                      emir_q50=prof["emir_q50"] if prof else np.nan, emir_q99=prof["emir_q99"] if prof else np.nan,
                      islem_q50=prof["islem_q50"] if prof else np.nan,
                      pd_ceyrek=pd_ceyrek(gun, kod), piyasa_5dk=piyasa_hareketi(gun, pz, pencere_us),
                      olay=len(u["olaylar"]), kabul=len(u["g1"].kabul), red=len(u["g1"].reddedilen), **u["kayit"])
    return u
