"""Tespit modulu testleri: etiket penceresi, Z-skorun yalniz gecmisi kullanmasi, kisa omurlu uzak emir tanimi.

Kullanim: python -I tespit/testler/test_tespit.py   (pytest ile de calisir)
"""
import os, sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yontemler as y
from ozellikler import uzak_kisa_omurlu, fiyat_adimi


def test_b_penceresi(tmp_path=None):
    """B: tedbirden 3 is gunu once biter, N = 20 islem gunu (tatil haric); onceki 2 is gunu belirsiz."""
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_vaka_test.csv")
    pd.DataFrame([dict(pay_kodu="ABC", seviye_nihai="B", etiket_nihai="1", nihai_tedbir_bas="2025-04-03",
                       nihai_donem_bas=None, nihai_donem_bit=None, bulten="x")]).to_csv(yol, index=False)
    try:
        e = y.etiketler(yol)
    finally:
        os.remove(yol)
    g = sorted(e.loc[e["seviye"] == "B", "tarih"])
    assert len(g) == y.N_B
    assert g[-1] == pd.Timestamp("2025-03-27")                                            # 03-31, 04-01 bayram
    assert sorted(e.loc[e["seviye"] == "B_belirsiz", "tarih"]) == [pd.Timestamp("2025-03-28"), pd.Timestamp("2025-04-02")]


def test_zskor_yalniz_gecmis():
    """Bir gundeki uc deger yalniz o gunun z'sini buyutur; once gelen gunlerin z'si degismez."""
    gun = pd.bdate_range("2025-03-03", periods=10)
    rows = [dict(islem_kodu="X.E", tarih=t, **{c: 1.0 + 0.01 * i for c in y.OZELLIKLER}) for i, t in enumerate(gun)]
    d0 = y.z_skorlari(pd.DataFrame(rows))
    rows[-1]["getiri"] = 50.0
    d1 = y.z_skorlari(pd.DataFrame(rows))
    assert np.allclose(d0["z_getiri"].iloc[:-1].fillna(0), d1["z_getiri"].iloc[:-1].fillna(0))
    assert d1["z_getiri"].iloc[-1] > 100
    assert d1["z_getiri"].iloc[:y.GECMIS_EN_AZ].isna().all()


def test_kisa_omurlu_uzak():
    """Satis: en iyi satis 10,00, adim 0,01; 10,03 (3 adim) 30 sn sonra iptal -> sayilir; 10,02 (2 adim) sayilmaz;
    10,05 (5 adim) dolar -> sayilmaz."""
    us = lambda s: pd.Timestamp("2025-03-03 11:00:00") + pd.Timedelta(seconds=s)
    r = []
    for no, p, iptal, dolum in [("a", 10.03, 30, None), ("b", 10.02, 30, None), ("c", 10.05, None, 20)]:
        r.append(dict(islem_kodu="X.E", emir_no=no, emir_degistirilme_zamani=us(0), degisiklik_sebebi=6,
                      seans="P_SUREKLI_ISLEM", emir_fiyat_turu=1, alis_satis="S", fiyat=p, emir_miktari=100,
                      en_iyi_alis_fiyati=9.99, en_iyi_satis_fiyati=10.00))
        if iptal:
            r.append({**r[-1], "emir_degistirilme_zamani": us(iptal), "degisiklik_sebebi": 1})
        if dolum:
            r.append({**r[-1], "emir_degistirilme_zamani": us(dolum), "degisiklik_sebebi": 3})
    x = uzak_kisa_omurlu(pd.DataFrame(r)).loc["X.E"]
    assert x["uzak_kisa"] == 100 and x["surekli_yeni_miktar"] == 300
    assert abs(fiyat_adimi(10.00) - 0.01) < 1e-12 and abs(fiyat_adimi(32.14) - 0.02) < 1e-12


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            try:
                f()
                print("TAMAM", ad)
            except AssertionError as e:
                print("HATA ", ad, e)
