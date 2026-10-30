"""Yaniltici emir senaryosu: katman uzakligi 4 (temel), 1, 0 karsilastirmasi.
Kullanim: python -I yaniltici_karsilastir.py TESPIT_KLASORU"""
import os, re, sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.stdout.reconfigure(encoding="utf-8")
T = sys.argv[1]
KOSU = {"4 (temel)": "pencere", "1": "pencere_yaniltici_adim1", "0": "pencere_yaniltici_adim0"}
PUAN = ["puan_zskor", "puan_kural", "puan_iforest", "puan_denetimli"]

# 1) denetimli_degerlendirme.csv: yaniltici satirlari (ROC-AUC / ilk 3 / kontrol ilk 3)
satir = []
for ad, k in KOSU.items():
    d = pd.read_csv(os.path.join(T, k, "denetimli_degerlendirme.csv"))
    d = d[d["senaryo"] == "yaniltici"].set_index("puan")
    r = {"adim": ad, "pay_gun": int(d["pay_gun"].iloc[0])}
    for p in PUAN:
        r[p] = f"{d.loc[p, 'roc_auc']:.2f} / %{100 * d.loc[p, 'ilk3_isabet']:.0f} / %{100 * d.loc[p, 'kontrol_ilk3']:.0f}"
    satir.append(r)
print("Yaniltici emir (ROC-AUC / ilk 3 / kontrol ilk 3):")
print(pd.DataFrame(satir).to_string(index=False))

# 2) gunlukten disarida kalan yaniltici vakalar
for ad, k in KOSU.items():
    f = os.path.join(T, k, "kosu.log")
    if os.path.exists(f):
        L = [l.strip() for l in open(f, encoding="utf-8", errors="replace") if "yaniltici" in l and
             ("temiz degil" in l or "kabul edilen" in l or "HATA" in l)]
        print(f"\nadim {ad}: disarida kalan yaniltici vaka {len(L)}")
        for l in L:
            print("  ", l)

# 3) mekanizma: pozitif pencerelerde gostergeler ve kural bayragi
print("\nPozitif yaniltici pencerelerde (enjeksiyonlu kume) gostergeler, pay-gun basina en buyuk pozitif pencere:")
ms = []
for ad, k in KOSU.items():
    A = pd.read_parquet(os.path.join(T, k, "pencereler.parquet"))
    x = A[(A["senaryo"] == "yaniltici") & (A["kume"] == "enjeksiyonlu") & A["poz"]]
    g = x.groupby(["gun", "kod"])
    ms.append(dict(adim=ad, pay_gun=g.ngroups,
                   uzak_kisa_pay_ort=g["uzak_kisa_pay"].max().mean(),
                   z_uzak_kisa_pay_ort=g["z_uzak_kisa_pay"].max().mean(),
                   z_iptal_orani_ort=g["z_iptal_orani"].max().mean(),
                   z_derinlik_deng_ort=g["z_derinlik_dengesizlik"].apply(lambda s: s.abs().max()).mean(),
                   kural_ab_pay=g["kural_ab"].any().mean()))
print(pd.DataFrame(ms).round(2).to_string(index=False))

# 4) uc kosuda da temiz olan ortak pay-gunlerde ROC-AUC (Z-skor, kural)
ortak = None
for k in KOSU.values():
    A = pd.read_parquet(os.path.join(T, k, "pencereler.parquet"))
    s = set(map(tuple, A[A["senaryo"] == "yaniltici"][["gun", "kod"]].drop_duplicates().to_numpy()))
    ortak = s if ortak is None else ortak & s
print(f"\nUc kosuda ortak temiz yaniltici pay-gun: {len(ortak)}")
for ad, k in KOSU.items():
    A = pd.read_parquet(os.path.join(T, k, "pencereler.parquet"))
    x = A[(A["senaryo"] == "yaniltici") & (A["kume"] == "enjeksiyonlu")]
    x = x[[(g, c) in ortak for g, c in zip(x["gun"], x["kod"])]]
    r = [f"adim {ad}:"]
    for p in ["puan_zskor", "puan_kural"]:
        sira = x.groupby(["gun", "kod"])[p].rank(ascending=False, method="first")
        ilk3 = x.assign(i=(sira <= 3) & x["poz"]).groupby(["gun", "kod"])["i"].any().mean()
        r.append(f"{p} {roc_auc_score(x['poz'], x[p]):.2f} / %{100 * ilk3:.0f}")
    print("  ".join(r))
