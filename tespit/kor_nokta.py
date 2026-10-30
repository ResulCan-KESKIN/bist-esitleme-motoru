"""Kor nokta haritasi (senaryo-tasarimi.md 7): pencere_degerlendir.py ciktisinin (SENARYO_SURUM=yeni) senaryo
parametre bantlarina gore ayrilmasi.

Her senaryo, eksen ve bant icin: vaka (pay-gun) sayisi; o pay-gunlerin enjeksiyonlu pencerelerinde ROC-AUC; gun icinde
pozitif pencerelerden biri ilk 3'te mi (ilk3); ayni pencerelerin enjeksiyonsuz kosuda ilk 3'e girme orani (kontrol_ilk3).
Puanlar: Z-skor, kurallar, Isolation Forest (pencereler.parquet) ve varsa denetimli model (denetimli_puanlar.parquet).
Yaniltici emirde ayrica uzaklik bandi x boy bandi tablosu ve bantlarin esit ya da gercekci agirlikli ortalamasi
(ayarli_senaryo.GERCEKCI_AGIRLIK). Secimlerin sonuc dagilimi (tamam / temiz_degil / ...) senaryo ve bant bazinda yazilir:
temizlik olcutuyle disarida kalan vakalar sonucu belirli paylara kaydirabilir (rapor.md 8.3).
Kullanim: python -I tespit/kor_nokta.py PENCERE_KLASORU
"""
import os, sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sentetik_degerlendir  # noqa: F401  (motor ve veri/araclar arama yolu)
import ayarli_senaryo as ay

PUANLAR = ["puan_zskor", "puan_kural", "puan_iforest", "puan_denetimli"]


def _kes(x, sinir, ad):
    return pd.cut(x, sinir, labels=ad, right=False).astype(str)


def bantlar(K):
    """Kayit tablosuna bant sutunlari ekler; donus: (K, {senaryo: [eksen sutunlari]})."""
    K = K.copy()
    if K["piyasa_5dk"].notna().sum() >= 3:
        K["piyasa"] = pd.qcut(K["piyasa_5dk"], 3, labels=["sakin", "orta", "hareketli"], duplicates="drop").astype(str)
    else:
        K["piyasa"] = "nan"
    K["pd_ceyrek"] = K["pd_ceyrek"].map(lambda v: "nan" if pd.isna(v) else f"Q{int(v)}")
    s = K["senaryo"]
    y, yk, kr, kp = s == "yaniltici", s == "yukseltme", s == "karsilikli", s == "kapanis"
    if y.any():
        K.loc[y, "boy_bant"] = _kes(K.loc[y, "boy_orani"], [0, 1, 3, np.inf], ["<1", "1-3", ">=3"])
        K.loc[y, "omur_bant"] = _kes(K.loc[y, "omur_sn"], [0, 30, 60, 150, np.inf], ["5-30", "30-60", "60-150", "150-300"])
        K.loc[y, "yeniden_giris_var"] = np.where(K.loc[y, "yeniden_giris"] > 0, "var", "yok")
        for c in ("katman", "dongu"):
            K.loc[y, c + "_b"] = K.loc[y, c].astype("Int64").astype(str)
    if yk.any():
        K.loc[yk, "etki_bant"] = _kes(K.loc[yk, "etki"], [-np.inf, 0.01, 0.03, 0.05, np.inf], ["<%1", "%1-3", "%3-5", ">%5"])
        K.loc[yk, "adet_bant"] = _kes(K.loc[yk, "adet"], [0, 11, 21, np.inf], ["5-10", "11-20", "21-30"])
        K.loc[yk, "k_b"] = K.loc[yk, "k"].astype("Int64").astype(str)
    if kr.any():
        K.loc[kr, "tekrar_bant"] = _kes(K.loc[kr, "tekrar"], [0, 11, 21, np.inf], ["3-10", "11-20", "21-30"])
    if kp.any():
        K.loc[kp, "kat_bant"] = _kes(K.loc[kp, "kat"], [0, 1, 2, np.inf], ["0,5-1", "1-2", "2-3"])
        K.loc[kp, "once_bant"] = _kes(K.loc[kp, "saniye_once"], [0, 60, 180, np.inf], ["0-60", "60-180", "180-300"])
    ortak = ["pd_ceyrek", "piyasa"]
    eksen = {"yaniltici": ["bant", "katman_b", "boy_bant", "omur_bant", "dongu_b", "yeniden_giris_var"] + ortak,
             "yukseltme": ["etki_bant", "adet_bant", "k_b"] + ortak,
             "karsilikli": ["boy_turu", "tekrar_bant"] + ortak,
             "kapanis": ["kat_bant", "once_bant"] + ortak}
    return K, eksen


def olc(x, p):
    """x: bir vaka kumesinin pencereleri (enjeksiyonlu ve kontrol)."""
    out = {}
    for kume, ad in (("enjeksiyonlu", "ilk3"), ("kontrol", "kontrol_ilk3")):
        xs = x[x["kume"] == kume]
        sira = xs.groupby(["gun", "kod"])[p].rank(ascending=False, method="first")
        h = (sira <= 3) & xs["poz"]
        out[ad] = h.groupby([xs["gun"], xs["kod"]]).any().mean() if len(xs) else np.nan
    e = x[(x["kume"] == "enjeksiyonlu") & x[p].notna()]
    out["roc_auc"] = roc_auc_score(e["poz"], e[p]) if 0 < e["poz"].sum() < len(e) else np.nan
    return out


if __name__ == "__main__":
    kl = sys.argv[1]
    A = pd.read_parquet(os.path.join(kl, "pencereler.parquet"))
    A["gun"] = A["gun"].astype(str)
    f = os.path.join(kl, "denetimli_puanlar.parquet")
    if os.path.exists(f):
        D = pd.read_parquet(f)
        D["gun"] = D["gun"].astype(str)
        A = A.merge(D[["gun", "kod", "pencere", "kume", "puan_denetimli"]], on=["gun", "kod", "pencere", "kume"], how="left")
    else:
        A["puan_denetimli"] = np.nan
    K0 = pd.read_csv(os.path.join(kl, "senaryo_kayit.csv"))
    K0["gun"] = K0["gun"].astype(str)
    K, eksen = bantlar(K0)
    T = K[K["sonuc"] == "tamam"]
    R = []
    for senaryo, eks in eksen.items():
        Ts = T[T["senaryo"] == senaryo]
        if Ts.empty:
            continue
        for ek in ["hepsi"] + eks:
            gruplar = [("hepsi", Ts)] if ek == "hepsi" else list(Ts.groupby(ek))
            for b, g in gruplar:
                x = A[A.set_index(["gun", "kod"]).index.isin(list(zip(g["gun"], g["kod"])))]
                for p in PUANLAR:
                    if x[p].notna().any():
                        R.append(dict(senaryo=senaryo, eksen=ek, bant=b, puan=p, vaka=len(g), **olc(x, p)))
    R = pd.DataFrame(R)
    R.to_csv(os.path.join(kl, "kor_nokta.csv"), index=False, encoding="utf-8")
    S = K0.groupby(["senaryo", K0.get("bant", pd.Series("-", index=K0.index)).fillna("-"), "sonuc"]).size().unstack(fill_value=0)
    S.to_csv(os.path.join(kl, "kor_nokta_sonuc.csv"), encoding="utf-8")
    pd.set_option("display.width", 200)
    print("Secim sonuclari:\n", S.to_string(), "\n")
    for senaryo in eksen:
        r = R[R["senaryo"] == senaryo]
        if r.empty:
            continue
        print(f"== {senaryo}")
        t = r.pivot_table(index=["eksen", "bant", "vaka"], columns="puan", values=["roc_auc", "ilk3", "kontrol_ilk3"])
        print(t.round(2).to_string(), "\n")
    y = T[T["senaryo"] == "yaniltici"]
    if len(y):
        I = []
        for (b, bb), g in y.groupby(["bant", "boy_bant"]):
            x = A[A.set_index(["gun", "kod"]).index.isin(list(zip(g["gun"], g["kod"])))]
            for p in PUANLAR:
                if x[p].notna().any():
                    I.append(dict(bant=b, boy_bant=bb, puan=p, vaka=len(g), **olc(x, p)))
        I = pd.DataFrame(I)
        I.to_csv(os.path.join(kl, "kor_nokta_yaniltici_2b.csv"), index=False, encoding="utf-8")
        print("== yaniltici: uzaklik bandi x boy bandi (ilk3)\n",
              I.pivot_table(index=["bant", "boy_bant", "vaka"], columns="puan", values="ilk3").round(2).to_string(), "\n")
        rb = R[(R["senaryo"] == "yaniltici") & (R["eksen"] == "bant")]
        O = []
        for p, g in rb.groupby("puan"):
            w = g["bant"].map(ay.GERCEKCI_AGIRLIK)
            for olcu in ("roc_auc", "ilk3", "kontrol_ilk3"):
                v = g[olcu]
                O.append(dict(puan=p, olcu=olcu, esit=v.mean(), gercekci=float((v * w).sum() / w[v.notna()].sum())))
        O = pd.DataFrame(O)
        O.to_csv(os.path.join(kl, "kor_nokta_ozet.csv"), index=False, encoding="utf-8")
        print("== yaniltici: bantlarin esit ve gercekci agirlikli ortalamasi\n",
              O.pivot_table(index="olcu", columns="puan", values=["esit", "gercekci"]).round(2).to_string())
