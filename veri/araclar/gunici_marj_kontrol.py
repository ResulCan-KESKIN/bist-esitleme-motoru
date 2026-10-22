"""Fiyat marji: islem olan sira-gunlerde en yuksek/en dusuk fiyatin baz fiyata gore sinirlarla karsilastirilmasi.

Girdi: gunici_islem_gunsonu_karsilastir.py ciktisi gunsonu_islem_birlesik.parquet.
Baz = previous_last_price; marj adaylari 0,10/0,15/0,20; sinirlar ice yuvarlanir (02-fiyat.md madde 37).
Kullanim: python -I gunici_marj_kontrol.py GUNSONU_ISLEM_BIRLESIK.parquet CIKTI.csv
"""
import sys, os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import GRUP_TABLO, yukari_adim, asagi_adim

src, out = sys.argv[1:3]
m = pd.read_parquet(src)
x = m[(m.adet > 0) & (m.previous_last_price > 0) & m.instrument_group.isin(["EQT", "ETF", "GMF", "GSF", "EMS", "RGT"])].copy()
x["ust_oran"] = x.highest_price / x.previous_last_price - 1
x["alt_oran"] = x.lowest_price / x.previous_last_price - 1
print(x.groupby(["instrument_group", "market_segment"]).agg(n=("ust_oran", "size"), ust_max=("ust_oran", "max"),
                                                            alt_min=("alt_oran", "min")).round(4).to_string())
satir = []
for marj in [0.10, 0.15, 0.20]:
    s = x.apply(lambda r: (yukari_adim(round(r.previous_last_price * 1000) * (1 - marj), GRUP_TABLO[r.instrument_group]),
                           asagi_adim(round(r.previous_last_price * 1000) * (1 + marj), GRUP_TABLO[r.instrument_group])),
                axis=1, result_type="expand")
    taban, tavan = s[0] / 1000, s[1] / 1000
    dis = (x.highest_price > tavan + 1e-9) | (x.lowest_price < taban - 1e-9)
    satir.append(dict(marj=marj, sira_gun=len(x), sinir_disi=int(dis.sum()),
                      sinir_disi_ozsermaye=int((dis & x.corporate_action.notna()).sum()),
                      sinir_disi_rucan_bp=int((dis & x.islem_kodu.str.endswith((".R", ".BE"))).sum()),
                      tavana_esit=int(np.isclose(x.highest_price, tavan).sum()),
                      tabana_esit=int(np.isclose(x.lowest_price, taban).sum())))
r = pd.DataFrame(satir)
r.to_csv(out, index=False, encoding="utf-8")
print(r.to_string())
