"""Tek fiyat (muzayede) dagitimi testleri (03-tek-fiyat.md Bolum E; 05-emirler.md madde 14, 26, 36).

Kullanim: python -I motor/testler/test_tek_fiyat.py   (pytest ile de calisir)
"""
import os, sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor.tek_fiyat import TekFiyat
from motor.emir import YeniEmir, Degistir, Iptal, LIMIT, PIYASA, PIYASADAN_LIMITE, DENGELEYICI, KIE

ADIM = (np.array([0]), np.array([10]))   # fiyat adimi 0,01 TL


def tl(x):
    return round(x * 1000)


def defter(emirler):
    t = TekFiyat()
    for z, (no, alis, p, q, tur) in enumerate(emirler, 1):
        t.isle(YeniEmir(z, no, alis, tl(p), q, tur))
    return t


def test_dagitim_sirasi():
    """Piyasa emri once; limitler fiyat sonra zaman onceligiyle; iki liste bastan yurunur (madde 48-51)."""
    t = defter([("B1", True, 0, 50, PIYASA), ("L1", True, 10.10, 40, LIMIT), ("L2", True, 10.00, 30, LIMIT),
                ("L3", True, 10.10, 20, LIMIT), ("S1", False, 10.00, 60, LIMIT), ("S2", False, 9.90, 30, LIMIT),
                ("S3", False, 10.20, 50, LIMIT)])
    sonuc, isl, kalan = t.eslestir(100, ADIM)
    assert sonuc["fiyat"] == tl(10.10) and sonuc["miktar"] == 90
    assert [(i.alis_no, i.satis_no, i.adet) for i in isl] == [("B1", "S2", 30), ("B1", "S1", 20), ("L1", "S1", 40)]
    assert all(i.fiyat == tl(10.10) for i in isl)
    assert [(e.no, e.kalan) for e in kalan] == [("L2", 30), ("L3", 20), ("S3", 50)]


def test_dengeleyici():
    """Dengeleyici emir denge fiyatinda karsilanmayan karsi taraf emriyle eslesir; kalani iptal (madde 52-55)."""
    t = defter([("L1", True, 10.00, 50, LIMIT), ("S1", False, 10.00, 30, LIMIT), ("D1", False, 0, 15, DENGELEYICI),
                ("D2", True, 0, 10, DENGELEYICI)])
    sonuc, isl, kalan = t.eslestir(100, ADIM)
    assert sonuc["fiyat"] == tl(10.00) and sonuc["miktar"] == 30
    assert [(i.alis_no, i.satis_no, i.adet) for i in isl] == [("L1", "S1", 30), ("L1", "D1", 15)]
    assert [(e.no, e.kalan) for e in kalan] == [("L1", 5)]


def test_kalanlar():
    """Piyasa emri ve KIE kalani iptal; piyasadan limite kalani eslesme fiyatindan limit emir (05 madde 14, 26)."""
    t = TekFiyat()
    t.isle(YeniEmir(1, "M", True, 0, 50, PIYASA))
    t.isle(YeniEmir(2, "X", True, 0, 40, PIYASADAN_LIMITE))
    t.isle(YeniEmir(3, "K", True, tl(10.00), 10, LIMIT, KIE))
    t.isle(YeniEmir(4, "S", False, tl(10.00), 60, LIMIT))
    sonuc, isl, kalan = t.eslestir(100, ADIM, tavan=tl(10.00))
    assert sonuc["fiyat"] == tl(10.00)
    assert [(i.alis_no, i.adet) for i in isl] == [("M", 50), ("X", 10)]
    assert [(e.no, e.fiyat, e.kalan, e.fiyat_turu) for e in kalan] == [("X", tl(10.00), 30, LIMIT)]


def test_toplamada_oncelik():
    """Emir toplamada fiyat degisikligi, kalan artisi ve gorunmeyen alan degisikligi onceligi kaybettirir;
    azaltmada korunur (madde 20; 04 madde 24)."""
    t = defter([("A", True, 10.00, 10, LIMIT), ("B", True, 10.00, 10, LIMIT), ("C", True, 10.00, 10, LIMIT),
                ("D", True, 10.00, 10, LIMIT), ("S", False, 10.00, 30, LIMIT)])
    t.isle(Degistir(10, "A", tl(10.00), -5))                     # azaltma: A basta kalir
    t.isle(Degistir(11, "B", tl(10.00), 0, gorunmeyen=True))     # B sona gider
    t.isle(Degistir(12, "C", tl(10.00), 0))                      # gorunur degisiklik yok: C yerinde
    t.isle(Iptal(13, "YOK"))
    sonuc, isl, kalan = t.eslestir(100, ADIM, tavan=tl(10.00))
    assert [(i.alis_no, i.adet) for i in isl] == [("A", 5), ("C", 10), ("D", 10), ("B", 5)]
    assert t.sayac == {"iptal_bulunamadi": 1}


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            try:
                f()
                print("TAMAM", ad)
            except AssertionError as e:
                print("HATA ", ad, e)
