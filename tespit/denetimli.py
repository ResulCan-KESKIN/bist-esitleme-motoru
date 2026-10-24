"""Denetimli model (TASARIM.md 6.3): sentetik enjeksiyon etiketli 5 dakikalik pencereler (pencere_degerlendir.py
ciktisi pencereler.parquet) uzerinde gradyan artirmali karar agaci.

- Girdi: pencere ozellikleri (ham, log donusumlu) ve ayni pay-gune gore saglam z'ler.
- Model yalniz surekli islem pencerelerinde egitilir ve puanlar. Kapanis muzayedesi penceresi her gun uc degerdir ve
  kapanis senaryosunda pozitif pencere hep odur; model bu pencereyi taniyabildigi surece "kapanis penceresi pozitiftir"
  ogrenir. Kapanis penceresi pencere.kapanis_gecmisi ile (payin gecmis kapanislarina gore) puanlanir; kapanis
  senaryosunun pay-gunleri (pozitif penceresi yalniz kapanis penceresidir) modelin disindadir.
- Dogrulama: pay-gune gore gruplu 5 katli capraz dogrulama (ayni pay-gunun pencereleri egitim ve testte bir arada
  olmaz). Katin modeli, test pay-gunlerinin enjeksiyonsuz (kontrol) pencerelerini de puanlar.
- Olcutler: ROC-AUC, ortalama kesinlik; gun icinde pozitif pencerelerden biri ilk 3'te mi; kontrolde ayni pencerelerin
  ilk 3'e girme orani (yanlis alarm tabani). Senaryo basina ayrica.
Kullanim: python -I tespit/denetimli.py PENCERELER.parquet CIKTI_KLASORU
"""
import os, sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import GroupKFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pencere as pn


def girdi(A):
    X = pd.DataFrame(index=A.index)
    for c in pn.OZ:
        X[c] = np.log1p(A[c].clip(lower=0)) if c in pn.LOG else A[c]
        X["z_" + c] = A["z_" + c].clip(-50, 50)
    return X


def ilk3(df, p):
    sira = df.groupby(["gun", "kod"])[p].rank(ascending=False, method="first")
    return df.assign(i3=sira <= 3).groupby(["gun", "kod"]).apply(lambda g: bool((g["i3"] & g["poz"]).any())).mean()


if __name__ == "__main__":
    src, out = sys.argv[1:3]
    os.makedirs(out, exist_ok=True)
    A = pd.read_parquet(src)
    A["grup"] = A["gun"].astype(str) + "|" + A["kod"]
    A = A[~A["kapanis_muzayedesi"] & (A["senaryo"] != "kapanis")]
    E, K = A[A["kume"] == "enjeksiyonlu"].copy(), A[A["kume"] == "kontrol"].copy()
    E["puan_denetimli"], K["puan_denetimli"] = np.nan, np.nan
    XE, XK = girdi(E), girdi(K)
    gruplar = E["grup"].to_numpy()
    for egit, test in GroupKFold(n_splits=5).split(XE, E["poz"], gruplar):
        m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0)
        m.fit(XE.iloc[egit], E["poz"].iloc[egit])
        E.iloc[test, E.columns.get_loc("puan_denetimli")] = m.predict_proba(XE.iloc[test])[:, 1]
        tg = set(gruplar[test])
        kk = K["grup"].isin(tg).to_numpy()
        K.loc[kk, "puan_denetimli"] = m.predict_proba(XK[kk])[:, 1]
    R = []
    for senaryo in [None] + sorted(E["senaryo"].unique()):
        e = E if senaryo is None else E[E["senaryo"] == senaryo]
        k = K if senaryo is None else K[K["senaryo"] == senaryo]
        for p in ["puan_zskor", "puan_kural", "puan_iforest", "puan_denetimli"]:
            R.append(dict(senaryo=senaryo or "hepsi", puan=p, pay_gun=e["grup"].nunique(),
                          roc_auc=roc_auc_score(e["poz"], e[p]), ort_kesinlik=average_precision_score(e["poz"], e[p]),
                          taban_oran=e["poz"].mean(), ilk3_isabet=ilk3(e, p), kontrol_ilk3=ilk3(k, p)))
    R = pd.DataFrame(R)
    R.to_csv(os.path.join(out, "denetimli_degerlendirme.csv"), index=False, encoding="utf-8")
    m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0).fit(XE, E["poz"])
    from sklearn.inspection import permutation_importance
    imp = permutation_importance(m, XE, E["poz"], scoring="average_precision", n_repeats=5, random_state=0)
    pd.Series(imp.importances_mean, index=XE.columns).sort_values(ascending=False).to_csv(
        os.path.join(out, "denetimli_ozellik_onemi.csv"), encoding="utf-8")
    print(R.round(3).to_string(index=False))
    print(pd.Series(imp.importances_mean, index=XE.columns).sort_values(ascending=False).head(10).round(4).to_string())
