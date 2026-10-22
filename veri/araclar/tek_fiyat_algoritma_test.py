"""tek_fiyat_algoritma.denge icin Ek-16 orneklerinin testi (ekler/ek16.md s. 197-200).

Kullanim: python -I tek_fiyat_algoritma_test.py   (her ornek icin TAMAM/HATA yazar)
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import denge

A = np.array
T10 = (A([0]), A([100]))   # ornekte fiyat adimi 0,10
T50 = (A([0]), A([500]))   # ornekte fiyat adimi 0,50


def kur(alis, satis):
    af = A([round(p * 1000) for p, q in alis], dtype=np.int64)
    aq = A([q for p, q in alis], dtype=np.int64)
    sf = A([round(p * 1000) for p, q in satis], dtype=np.int64)
    sq = A([q for p, q in satis], dtype=np.int64)
    return af, aq, sf, sq


ornekler = [
    ("Ornek 1", kur([(20.30, 30), (20.20, 15), (20.10, 5), (20.00, 20), (19.90, 25), (19.80, 20), (19.70, 10)],
                    [(20.50, 10), (20.40, 20), (20.30, 40), (20.20, 15), (20.10, 20), (20.00, 5), (19.90, 30)]),
     10, 10, T10, None, 20100, 60),
    ("Ornek 2", kur([(20.30, 30), (20.20, 15), (20.10, 5), (20.00, 20), (19.90, 15), (19.80, 10), (19.70, 5)],
                    [(20.50, 10), (20.40, 10), (20.30, 15), (20.20, 15), (20.10, 5), (20.00, 20), (19.90, 30)]),
     10, 10, T10, None, 20100, 60),
    ("Ornek 3-A", kur([(20.30, 100), (20.00, 700), (19.80, 450)], [(20.10, 830), (19.90, 1000), (19.80, 400)]),
     0, 0, T10, None, 19900, 800),
    ("Ornek 3-B", kur([], [(20.00, 10)]), 30, 10, T10, None, 20100, 20),
    ("Ornek 4", kur([(57.00, 200), (56.50, 300)], [(60.50, 500)]), 100, 100, T50, 55000, 57500, 100),
]
hata = 0
for ad, (af, aq, sf, sq), pa_, ps, tb, ref, bf, bm in ornekler:
    r = denge(af, aq, sf, sq, pa_, ps, tb, referans=ref)
    ok = r["fiyat"] == bf and r["miktar"] == bm
    hata += not ok
    print(ad, "TAMAM" if ok else "HATA", r["fiyat"], r["miktar"], r["adim"])
sys.exit(1 if hata else 0)
