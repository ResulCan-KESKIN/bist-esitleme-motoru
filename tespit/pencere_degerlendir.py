"""5 dakikalik pencere tespitinin sentetik enjeksiyonla degerlendirmesi (pencere.py; senaryolar ve olcek
sentetik_degerlendir.py ile ayni).

Pozitif pencere: enjeksiyonlu kosuda ilk ve son sentetik olay arasinda kalan pencereler; kapanis senaryosunda yalniz
kapanis muzayedesi penceresi (emir kapanis emir toplamada girilir, etkisi muzayedede gorulur). Olcutler (enjeksiyonlu
kosularin butun pencereleri):
- ROC-AUC; gun icinde pozitif pencerelerden biri ilk 3 pencerede mi (isabet orani);
- kontrol: ayni pencerelerin enjeksiyonsuz kosuda ilk 3'e girme orani (yanlis alarm tabani).
Kapanis muzayedesi penceresi Z-skor ve kurallarda payin gecmis kapanislarina gore puanlanir (pencere.kapanis_gecmisi).
Isolation Forest ayni gunun pencerelerine gore z'lerle calistigindan bu pencere her gun uc olur; bu yuzden yalniz surekli
islem pencerelerinde egitilir ve puanlar, kapanis penceresinin Isolation Forest puani yoktur (NaN; ilk 3'e girmez).
Kullanim: python -I tespit/pencere_degerlendir.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU [ADET] [TOHUM]
"""
import os, sys, time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sentetik_degerlendir as sd
import pencere as pn
import yontemler as y
import motor_ozellikleri as mo
from motor import veri
from motor.gun import Gun
from ozellikler import gunsonu_ozellikleri

PUANLAR = ["puan_zskor", "puan_kural", "puan_iforest"]
KAPANIS_GECMISI = os.environ.get("KAPANIS_GECMISI", "1") == "1"   # kapanis penceresi gecmis kapanislara gore


if __name__ == "__main__":
    oz, vaka, out = sys.argv[1:4]
    adet = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    os.makedirs(out, exist_ok=True)
    T = pd.read_parquet(oz)
    T = T[T["ozsermaye"].isna() & T["baz"].notna()].reset_index(drop=True)
    e = y.etiketler(vaka)
    etiketli = set(zip(e["islem_kodu"], e["tarih"]))
    aday = T[(T["tarih"] >= "2025-03-10") & (T["islem_sayisi"] >= sd.ISLEM_EN_AZ)]
    aday = aday[[(k, t) not in etiketli for k, t in zip(aday["islem_kodu"], aday["tarih"])]]
    secim = aday.sample(n=min(adet, len(aday)), random_state=int(rng.integers(1 << 31))).reset_index(drop=True)
    parca, t0 = [], time.time()
    for n, r in enumerate(secim.itertuples()):
        gun, kod = str(r.tarih.date()), r.islem_kodu
        senaryo = sd.SENARYO_SIRASI[n % len(sd.SENARYO_SIRASI)]
        try:
            df = veri.pay_gun_emirleri(sd.GUNLUK, gun, kod)
            tepe = veri.tepe_tahmini(df)
            gs = gunsonu_ozellikleri(sd.gunsonu(gun), gun).loc[kod]
            H = int(gs["hacim_tl"] / max(gs["kapanis"], 1e-9))
            g0 = Gun(df, gun, kod, sd.gunsonu(gun), tepe)
            g0.calistir()
            olaylar, _ = sd.senaryo_olaylari(senaryo, g0, df, gun, H, rng)
            g1 = Gun(df, gun, kod, sd.gunsonu(gun), tepe)
            g1.calistir(olaylar)
            if not g1.kabul:
                red = sorted({f"{b}:{s}" for _, b, s in g1.reddedilen})
                print(gun, kod, senaryo, "kabul edilen sentetik olay yok; red:", ", ".join(red) or "-", flush=True)
                continue
            olcu, kirli = sd.temizlik(senaryo, g1, olaylar)
            if kirli:
                print(gun, kod, senaryo, "temiz degil:", olcu, flush=True)
                continue
            W0 = pn.puanla(pn.pencere_ozellikleri(g0, pn.emir_olaylari(df)))
            W1 = pn.puanla(pn.pencere_ozellikleri(g1, pn.emir_olaylari(df, g1)))
            if KAPANIS_GECMISI:
                gecmis = T[(T["islem_kodu"] == kod) & (T["tarih"] < r.tarih)]
                W0 = pn.kapanis_gecmisi(W0, mo.satir(g0, df, gs), gecmis)
                W1 = pn.kapanis_gecmisi(W1, mo.satir(g1, df, gs), gecmis)
        except Exception as ex:
            print(gun, kod, senaryo, "HATA", type(ex).__name__, ex, flush=True)
            continue
        zs = [o.zaman for o, _ in g1.kabul]
        bas, bit = min(zs) // pn.PENCERE_US * pn.PENCERE_US, max(zs) // pn.PENCERE_US * pn.PENCERE_US
        poz = W1["kapanis_muzayedesi"].to_numpy() if senaryo == "kapanis" else (W1.index >= bas) & (W1.index <= bit)
        W1 = W1.assign(poz=poz, kume="enjeksiyonlu")
        W0 = W0.assign(poz=W0.index.isin(W1.index[poz]), kume="kontrol")
        for W in (W0, W1):
            parca.append(W.assign(gun=gun, kod=kod, senaryo=senaryo).reset_index(names="pencere"))
        print(n + 1, gun, kod, senaryo, int(poz.sum()), f"{time.time() - t0:.0f} sn", flush=True)
    A = pd.concat(parca, ignore_index=True)
    # Isolation Forest: surekli islem pencerelerinin z ozellikleri (kapanis muzayedesi penceresi disarida)
    from sklearn.ensemble import IsolationForest
    zc = ["z_" + c for c in pn.OZ]
    m = ~A["kapanis_muzayedesi"]
    X = A.loc[m, zc].fillna(0).clip(-20, 20).to_numpy()
    A["puan_iforest"] = np.nan
    A.loc[m, "puan_iforest"] = -IsolationForest(n_estimators=300, random_state=0).fit(X).score_samples(X)
    A.to_parquet(os.path.join(out, "pencereler.parquet"))
    from sklearn.metrics import roc_auc_score
    R = []
    for kume in ("enjeksiyonlu", "kontrol"):
        x = A[A["kume"] == kume]
        for senaryo in [None] + sd.SENARYO_SIRASI:
            xs = x if senaryo is None else x[x["senaryo"] == senaryo]
            for p in PUANLAR:
                sira = xs.groupby(["gun", "kod"])[p].rank(ascending=False, method="first")
                isabet = xs.assign(ilk3=sira <= 3).groupby(["gun", "kod"]).apply(lambda g: bool((g["ilk3"] & g["poz"]).any()))
                xp = xs[xs[p].notna()]
                R.append(dict(kume=kume, senaryo=senaryo or "hepsi", puan=p, pay_gun=len(isabet),
                              roc_auc=roc_auc_score(xp["poz"], xp[p]) if 0 < xp["poz"].sum() < len(xp) else np.nan,
                              ilk3_isabet=isabet.mean()))
    R = pd.DataFrame(R)
    R.to_csv(os.path.join(out, "pencere_degerlendirme.csv"), index=False, encoding="utf-8")
    print(R.round(3).to_string(index=False))
