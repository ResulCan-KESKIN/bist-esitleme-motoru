"""ALKLC yaniltici emir yerlesimi: donem (03.03-18.03.2025) ve sonrasi (19.03-30.06.2025).
Kullanim: python -I alklc_cozumle.py alklc_emirler.parquet [piyasa_ozet.parquet]"""
import sys

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

sys.stdout.reconfigure(encoding="utf-8")
A = pd.read_parquet(sys.argv[1])
ad = {k: str(k) for k in range(7)} | {7: "7+"}
print("Gun sayisi:", A.groupby("grup")["tarih"].nunique().to_dict(), " yeni limit emir:", A.groupby("grup").size().to_dict())


def dagilim(x):
    s = x.groupby(["grup", "kova"])["miktar"].sum().unstack(fill_value=0)
    return (s.div(s.sum(axis=1), axis=0) * 100).rename(columns=ad).round(1)


ozet = A.groupby(["grup", "kova", "kisa", "buyuk"]).agg(adet=("miktar", "size"), miktar=("miktar", "sum")).reset_index()
if len(sys.argv) > 2:
    P = pd.read_parquet(sys.argv[2])
    P["grup"] = "piyasa (1 gun)"
    ozet = pd.concat([ozet, P[ozet.columns]], ignore_index=True)

print("\nA) 60 sn icinde islem gormeden iptal edilen BUYUK emirler (pay-gunun en buyuk %1'i): uzaklik dagilimi, miktar %")
print(dagilim(ozet[ozet["kisa"] & ozet["buyuk"]]).to_string())
print("   adet:", ozet[ozet["kisa"] & ozet["buyuk"]].groupby("grup")["adet"].sum().to_dict())
print("\nB) 60 sn icinde islem gormeden iptal edilen BUTUN emirler: uzaklik dagilimi, miktar %")
print(dagilim(ozet[ozet["kisa"]]).to_string())
print("\nC) Butun yeni limit emirler (yerlesim tabani): uzaklik dagilimi, miktar %")
print(dagilim(ozet).to_string())
print("\nD) Her kovada girilen miktarin yuzde kaci 60 sn icinde islem gormeden iptal ediliyor")
s = ozet.groupby(["grup", "kova"]).apply(lambda g: 100 * g.loc[g["kisa"], "miktar"].sum() / g["miktar"].sum())
print(s.unstack().rename(columns=ad).round(1).to_string())
print("\nD2) Ayni, yalniz BUYUK emirler")
b = ozet[ozet["buyuk"]]
s = b.groupby(["grup", "kova"]).apply(lambda g: 100 * g.loc[g["kisa"], "miktar"].sum() / g["miktar"].sum())
print(s.unstack().rename(columns=ad).round(1).to_string())

# Gunluk: gunun yeni limit miktarina gore paylar
def gun(g):
    t = g["miktar"].sum()
    k = g["kisa"]
    return pd.Series({
        "kisa_3plus_hepsi": 100 * g.loc[k & (g["kova"] >= 3), "miktar"].sum() / t,       # mevcut gosterge (uzak_kisa_pay)
        "kisa_0_2_hepsi": 100 * g.loc[k & (g["kova"] <= 2), "miktar"].sum() / t,
        "kisa_buyuk_0_2": 100 * g.loc[k & g["buyuk"] & (g["kova"] <= 2), "miktar"].sum() / t,
        "kisa_buyuk_3plus": 100 * g.loc[k & g["buyuk"] & (g["kova"] >= 3), "miktar"].sum() / t,
        "yeni_emir": len(g),
    })


G = A.groupby(["grup", "tarih"]).apply(gun).reset_index()
print("\nE) Gunluk paylar (gunun yeni limit miktarina gore, %): ortalama / ortanca; Mann-Whitney p (donem > sonra)")
for c in ["kisa_3plus_hepsi", "kisa_0_2_hepsi", "kisa_buyuk_3plus", "kisa_buyuk_0_2"]:
    d, s_ = G.loc[G["grup"] == "ALKLC_donem", c], G.loc[G["grup"] == "ALKLC_sonra", c]
    p = mannwhitneyu(d, s_, alternative="greater").pvalue
    print(f"  {c:18s} donem {d.mean():5.2f} / {d.median():5.2f}   sonra {s_.mean():5.2f} / {s_.median():5.2f}   p = {p:.3f}")
print("\nDonem gunleri:")
print(G[G["grup"] == "ALKLC_donem"].drop(columns="grup").round(2).to_string(index=False))
print("\nSonra, Mart'in kalan gunleri:")
print(G[(G["grup"] == "ALKLC_sonra") & (G["tarih"] < "2025-04-01")].drop(columns="grup").round(2).to_string(index=False))
