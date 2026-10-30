"""Kademe emri vakalari (ENSRI, VKFYO): etiket (B penceresi) ve diger gunlerde emir yerlesimi.
Kullanim: python -I vaka_cozumle.py kademe_vakalari_emirler.parquet"""
import sys

import pandas as pd
from scipy.stats import mannwhitneyu

sys.stdout.reconfigure(encoding="utf-8")
A = pd.read_parquet(sys.argv[1])
A = A[A["grup"] != "belirsiz"]
A["g"] = A["kod"].str[:5] + "_" + A["grup"]
ad = {k: str(k) for k in range(7)} | {7: "7+"}


def dagilim(x):
    s = x.groupby(["g", "kova"])["miktar"].sum().unstack(fill_value=0)
    return (s.div(s.sum(axis=1), axis=0) * 100).rename(columns=ad).round(1)


print("Gun:", A.groupby("g")["tarih"].nunique().to_dict())
print("\nA) 60 sn icinde islem gormeden iptal edilen BUYUK emirler (pay-gunun en buyuk %1'i): uzaklik dagilimi, miktar %")
print(dagilim(A[A["kisa"] & A["buyuk"]]).to_string())
print("   adet:", A[A["kisa"] & A["buyuk"]].groupby("g").size().to_dict())
print("\nB) 60 sn icinde islem gormeden iptal edilen BUTUN emirler: uzaklik dagilimi, miktar %")
print(dagilim(A[A["kisa"]]).to_string())
print("\nC) Butun yeni limit emirler: uzaklik dagilimi, miktar %")
print(dagilim(A).to_string())
print("\nD) Her kovada girilen miktarin yuzde kaci 60 sn icinde islem gormeden iptal ediliyor")
s = A.groupby(["g", "kova"]).apply(lambda x: 100 * x.loc[x["kisa"], "miktar"].sum() / x["miktar"].sum())
print(s.unstack().rename(columns=ad).round(1).to_string())


def gun(x):
    t, k = x["miktar"].sum(), x["kisa"]
    return pd.Series({
        "kisa_3plus_hepsi": 100 * x.loc[k & (x["kova"] >= 3), "miktar"].sum() / t,
        "kisa_0_2_hepsi": 100 * x.loc[k & (x["kova"] <= 2), "miktar"].sum() / t,
        "kisa_buyuk_3plus": 100 * x.loc[k & x["buyuk"] & (x["kova"] >= 3), "miktar"].sum() / t,
        "kisa_buyuk_0_2": 100 * x.loc[k & x["buyuk"] & (x["kova"] <= 2), "miktar"].sum() / t,
        "yeni_emir": len(x)})


G = A.groupby(["kod", "grup", "tarih"]).apply(gun).reset_index()
print("\nE) Gunluk paylar (gunun yeni limit miktarina gore, %): etiket ortalama/ortanca, diger ortalama/ortanca; p (etiket > diger)")
for kod, x in G.groupby("kod"):
    print(kod)
    for c in ["kisa_3plus_hepsi", "kisa_0_2_hepsi", "kisa_buyuk_3plus", "kisa_buyuk_0_2"]:
        a, b = x.loc[x["grup"] == "etiket", c], x.loc[x["grup"] == "diger", c]
        p = mannwhitneyu(a, b, alternative="greater").pvalue
        print(f"  {c:18s} etiket {a.mean():6.2f} / {a.median():6.2f}   diger {b.mean():6.2f} / {b.median():6.2f}   p = {p:.3f}")
