"""Kismi gorunme tepe tahmini (veri._tepe_tutarli) testleri; satirlar Mart 2025 verisinden alinmistir.

Kullanim: python -I motor/testler/test_tepe.py   (pytest ile de calisir)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor.veri import _tepe_tutarli


def satirlar(baslangic, dizi, giris=0, muzayede=False):
    """dizi: [(sebep, kalan)] pasif gerceklesmeler; zamanlar giristen farkli."""
    out = [(6, giris, baslangic, 0, baslangic, not muzayede, giris)]
    once = baslangic
    for i, (seb, kal) in enumerate(dizi, 1):
        out.append((seb, giris + i, kal, once - kal, once, True, giris))
        once = kal
    return out


def test_yenileme_sonrasi_ilk_islem_13():
    # THYAO.E 03.03.2025, 6EAFCA8400E091DA: 12000'deki yenilemeden sonraki 1417'lik islem de 13
    s = satirlar(20000, [(13, 16000), (13, 12000), (13, 10583), (13, 8000), (13, 4000), (3, 0)])
    assert _tepe_tutarli(4000, s)


def test_yenileme_sonrasi_ilk_islem_3():
    # ASELS.E 03.03.2025, 6EAFCA81007A01A2: 5000'deki yenilemeden sonraki 3500'luk islem 3
    s = satirlar(25000, [(13, 20000), (13, 14624), (13, 10000), (13, 5000), (3, 1500), (3, 0)])
    assert _tepe_tutarli(5000, s)


def test_tek_islemde_birlesme():
    # THYAO.E 03.03.2025, 6EAFCA840079A7FB: 1010'luk tek islem (1000 gorunen + yenilenen kisimdan 10)
    s = satirlar(5000, [(3, 4040), (13, 4000), (13, 2990), (13, 2000), (3, 0)], muzayede=True)
    assert _tepe_tutarli(1000, s)
    assert not _tepe_tutarli(1010, s)


def test_iki_kez_yenileme():
    # GARAN.E 19.03.2025, 6EC64FC200C99637: 4062'lik islemde iki yenileme, ardindan 13
    s = satirlar(10000, [(13, 7500), (13, 6562), (13, 2500), (13, 1644), (3, 0)])
    assert _tepe_tutarli(2500, s)


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            try:
                f()
                print("TAMAM", ad)
            except AssertionError as e:
                print("HATA ", ad, e)
