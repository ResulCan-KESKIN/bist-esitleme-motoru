"""Sentetik emir dogrulama testleri (motor/dogrulama.py): Ek-19 izinleri, fiyat adimi, sinirlar, kapanis kurallari,
emir bilgisi degisikligi (04 madde 24 karari).

Kullanim: python -I motor/testler/test_dogrulama.py   (pytest ile de calisir)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor.dogrulama import Dogrulayici
from motor.emir import Emir, YeniEmir, Degistir, Iptal, LIMIT, PIYASA, KIE
from tek_fiyat_algoritma import TABLO7

D = Dogrulayici(TABLO7, 90000, 110000, aciga_satis_kapsami="yok")   # baz 100 TL, +-%10; adim 0,05 (50-100), 0,10 (100-250)


def test_fiyat_adimi_ve_sinir():
    assert D.kontrol(YeniEmir(0, "a", True, 99950, 10), "P_SUREKLI_ISLEM") is None
    assert D.kontrol(YeniEmir(0, "a", True, 99930, 10), "P_SUREKLI_ISLEM") == "fiyat_adimi"
    assert D.kontrol(YeniEmir(0, "a", True, 100050, 10), "P_SUREKLI_ISLEM") == "fiyat_adimi"   # 100 TL ustu 0,10
    assert D.kontrol(YeniEmir(0, "a", True, 110100, 10), "P_SUREKLI_ISLEM") == "fiyat_siniri"


def test_ek19_izinleri():
    # Yildiz/Ana disi acilis akisinda piyasa emri yok; acilisin son 5 dk'sinda iptal yok; EBDKS durdurmasinda emir yok
    assert D.kontrol(YeniEmir(0, "a", True, 0, 10, PIYASA, KIE), "P_ACS_EMR_TP2_PY") == "emir_tipi_B"
    assert D.kontrol(YeniEmir(0, "a", True, 0, 10, PIYASA, KIE), "P_ACILIS_EMIR_TPL") is None
    assert D.kontrol(Iptal(0, "a"), "P_ACS_EMR_TP_EIY") == "iptal"
    assert D.kontrol(YeniEmir(0, "a", True, 99950, 10), "P_GECICI_DURDUR_EBDK") == "emir_tipi_A"
    assert D.kontrol(YeniEmir(0, "a", True, 99950, 10), "YOK_BOYLE_BOLUM") == "bolum_ek19_disi"


def test_kapanis_kurallari():
    # kapanis emir toplama: son islem 100 TL'nin +-%3'u; kapanis fiyatindan islemler: yalniz kapanis fiyati
    assert D.kontrol(YeniEmir(0, "a", True, 103000, 10), "P_KAPANIS_EMIR_TPL", son_fiyat=100000) is None
    assert D.kontrol(YeniEmir(0, "a", True, 103100, 10), "P_KAPANIS_EMIR_TPL", son_fiyat=100000) == "kapanis_bandi"
    assert D.kontrol(YeniEmir(0, "a", True, 100000, 10), "P_KAPANIS_FIY_ISLEM", kapanis_fiyati=100000) is None
    assert D.kontrol(YeniEmir(0, "a", True, 99950, 10), "P_KAPANIS_FIY_ISLEM", kapanis_fiyati=100000) == \
        "kapanis_fiyati_disi"


def test_degisiklik():
    e = Emir("a", True, 99950, 10)
    assert D.kontrol(Degistir(0, "a", 99950, 0, gorunmeyen=True), "P_SUREKLI_ISLEM", e) == "emir_bilgisi_degisikligi"
    assert D.kontrol(Degistir(0, "a", 99900, 0), "P_SUREKLI_ISLEM", e) is None
    assert D.kontrol(Degistir(0, "a", 99900, 0), "P_ACS_EMR_TP_EIY", e) == "fiyat_kotulestirme"
    assert D.kontrol(Degistir(0, "a", 99950, -5), "P_ACS_EMR_TP_EIY", e) == "miktar_azaltma"
    assert D.kontrol(Degistir(0, "b", 99950, -5), "P_SUREKLI_ISLEM", None) == "emir_yok"


def test_aciga_satis():
    assert D.kontrol(YeniEmir(0, "a", False, 99950, 10, aciga=True), "P_SUREKLI_ISLEM") == "aciga_satis_kapsam"
    D2 = Dogrulayici(TABLO7, 90000, 110000, aciga_satis_kapsami="BIST 50", aciga_satis_izinli=True)
    assert D2.kontrol(YeniEmir(0, "a", False, 99950, 10, aciga=True), "P_SUREKLI_ISLEM") is None
    assert D2.kontrol(YeniEmir(0, "a", False, 99950, 10, aciga=True), "P_ACILIS_EMIR_TPL") == "aciga_satis_bolum"


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            try:
                f()
                print("TAMAM", ad)
            except AssertionError as e:
                print("HATA ", ad, e)
