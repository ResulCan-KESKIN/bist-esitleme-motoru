"""Emir dogrulama: sentetik (enjeksiyon) emirleri icin. Tekrar oynatmada gercek emirler dogrulanmaz.

- Ek-19 bolum x emir tipi ve degisiklik izinleri (05-emirler.md madde 139; ekler/ek19.md). "1*" (yalniz IKG limit)
  gun / KIE emirleri icin izin sayilmaz. Matriste olmayan bolumde emir reddedilir.
- Fiyat adimi (02-fiyat.md Tablo-7/8) ve gunluk fiyat sinirlari (marj tarih parametresi).
- Kapanis seansi emir toplamada son islem fiyatinin +-%3'u (03-tek-fiyat.md madde 72); kapanis fiyatindan islemlerde
  yalniz kapanis fiyati (madde 88).
- Aciga satis: tarih parametresi `aciga_satis_kapsami` ("yok" ise reddedilir; "BIST 50" ise sira listesi verilmelidir).
- Emir bilgisi (MPF-AFK-Hesap No) degisikligi reddedilir (04 madde 24, kullanici karari 22.10.2026).
- Orta nokta emirleri ve kotasyonlar motorda yoktur; reddedilir.
Donus: None (gecerli) ya da red sebebi.
"""
import os

from tek_fiyat_algoritma import adim, yukari_adim, asagi_adim

from .emir import YeniEmir, Degistir, Iptal, LIMIT, PIYASA, PIYASADAN_LIMITE, DENGELEYICI, KIE

EK19 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ekler", "ek19.md")
_matris = None


def ek19():
    """{bolum: {sutun: '0'|'1'|'1*'}}; sutunlar A..P (05-emirler.md madde 139)."""
    global _matris
    if _matris is None:
        _matris = {}
        for satir in open(EK19, encoding="utf-8"):
            h = [c.strip() for c in satir.strip().strip("|").split("|")]
            if len(h) == 17 and h[0].startswith("P"):
                _matris[h[0]] = dict(zip("ABCDEFGHIJKLMNOP", h[1:]))
    return _matris


class Dogrulayici:
    def __init__(self, tablo, taban, tavan, aciga_satis_kapsami=None, aciga_satis_izinli=False):
        self.tablo, self.taban, self.tavan = tablo, taban, tavan
        self.aciga_kapsam, self.aciga_izinli = aciga_satis_kapsami, aciga_satis_izinli

    def _izin(self, bolum, sutun):
        return ek19().get(bolum, {}).get(sutun) == "1"

    def _fiyat(self, p, bolum, son_fiyat, kapanis_fiyati, bant):
        if p % adim(p, self.tablo) != 0:
            return "fiyat_adimi"
        if not (self.taban <= p <= self.tavan):
            return "fiyat_siniri"
        if bolum.startswith("P_KAPANIS_EMIR") and son_fiyat:
            if not (yukari_adim(son_fiyat * (1 - bant), self.tablo) <= p <= asagi_adim(son_fiyat * (1 + bant), self.tablo)):
                return "kapanis_bandi"
        if bolum == "P_KAPANIS_FIY_ISLEM" and kapanis_fiyati is not None and p != kapanis_fiyati:
            return "kapanis_fiyati_disi"
        return None

    def kontrol(self, o, bolum, mevcut=None, son_fiyat=None, kapanis_fiyati=None, bant=0.03):
        if bolum not in ek19():
            return "bolum_ek19_disi"
        if isinstance(o, YeniEmir):
            if o.miktar <= 0:
                return "miktar"
            tip = {LIMIT: "A", PIYASA: "B", PIYASADAN_LIMITE: "C", DENGELEYICI: "F"}.get(o.fiyat_turu)
            if tip is None or not self._izin(bolum, tip):
                return "emir_tipi_" + str(tip)
            if o.gecerlilik == KIE and not self._izin(bolum, "D"):
                return "kie"
            if o.tepe and not self._izin(bolum, "G"):
                return "kismi_gorunme"
            if getattr(o, "aciga", False):
                if not self._izin(bolum, "O"):
                    return "aciga_satis_bolum"
                if self.aciga_kapsam == "yok" or (self.aciga_kapsam and not self.aciga_izinli):
                    return "aciga_satis_kapsam"
            if o.fiyat_turu == LIMIT:
                return self._fiyat(o.fiyat, bolum, son_fiyat, kapanis_fiyati, bant)
            return None
        if isinstance(o, Iptal):
            return None if self._izin(bolum, "M") else "iptal"
        if isinstance(o, Degistir):
            if o.gorunmeyen:
                return "emir_bilgisi_degisikligi"
            if mevcut is None:
                return "emir_yok"
            if o.fiyat != mevcut.fiyat:
                iyi = o.fiyat > mevcut.fiyat if mevcut.alis else o.fiyat < mevcut.fiyat
                if not self._izin(bolum, "J" if iyi else "I"):
                    return "fiyat_iyilestirme" if iyi else "fiyat_kotulestirme"
                r = self._fiyat(o.fiyat, bolum, son_fiyat, kapanis_fiyati, bant)
                if r:
                    return r
            if o.kalan_farki < 0 and not self._izin(bolum, "K"):
                return "miktar_azaltma"
            if o.kalan_farki > 0 and not self._izin(bolum, "L"):
                return "miktar_artirma"
            return None
        raise TypeError(type(o))
