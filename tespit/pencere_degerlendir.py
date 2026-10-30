"""5 dakikalik pencere tespitinin sentetik enjeksiyonla degerlendirmesi (pencere.py; senaryolar ve olcek
sentetik_degerlendir.py ile ayni).

Pozitif pencere: enjeksiyonlu kosuda kabul edilen en az bir sentetik olay iceren pencere (29.10.2026'ya kadar ilk ve son
sentetik olay arasindaki butun pencereler; sabit senaryolarda olaylar arasi bosluk 5 dk'dan kisa oldugundan ayni sonuc);
kapanis senaryosunda yalniz kapanis muzayedesi penceresi (emir kapanis emir toplamada girilir, etkisi muzayedede
gorulur). Olcutler (enjeksiyonlu kosularin butun pencereleri):
- ROC-AUC; gun icinde pozitif pencerelerden biri ilk 3 pencerede mi (isabet orani);
- kontrol: ayni pencerelerin enjeksiyonsuz kosuda ilk 3'e girme orani (yanlis alarm tabani).
Kapanis muzayedesi penceresi Z-skor ve kurallarda payin gecmis kapanislarina gore puanlanir (pencere.kapanis_gecmisi).
Isolation Forest ayni gunun pencerelerine gore z'lerle calistigindan bu pencere her gun uc olur; bu yuzden yalniz surekli
islem pencerelerinde egitilir ve puanlar, kapanis penceresinin Isolation Forest puani yoktur (NaN; ilk 3'e girmez).
Senaryo surumu (SENARYO_SURUM ortam degiskeni): "eski" (varsayilan) sabit kaliplar (sentetik_degerlendir.py); "yeni"
hisseye gore ayarli senaryolar (ayarli_senaryo.py, senaryo-tasarimi.md). SENARYOLAR: virgulle senaryo sirasi (tekrar
olabilir; varsayilan kapanis,yaniltici,yukseltme,karsilikli). Her secim senaryo_kayit.csv'ye yazilir (parametreler ve
sonuc: tamam / kabul_yok / temiz_degil / yer_yok / hata); bant raporu kor_nokta.py.
Kullanim: python -I tespit/pencere_degerlendir.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU [ADET] [TOHUM]
"""
import collections, os, sys, time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sentetik_degerlendir as sd
import ayarli_senaryo as ay
import pencere as pn
import yontemler as y
import motor_ozellikleri as mo
from motor import veri
from motor.gun import Gun
from ozellikler import gunsonu_ozellikleri

PUANLAR = ["puan_zskor", "puan_kural", "puan_iforest"]
KAPANIS_GECMISI = os.environ.get("KAPANIS_GECMISI", "1") == "1"   # kapanis penceresi gecmis kapanislara gore
SURUM = os.environ.get("SENARYO_SURUM", "eski")
SENARYOLAR = os.environ.get("SENARYOLAR", ",".join(sd.SENARYO_SIRASI)).split(",")


if __name__ == "__main__":
    oz, vaka, out = sys.argv[1:4]
    adet = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    os.makedirs(out, exist_ok=True)
    T = pd.read_parquet(oz)
    T = T[T["ozsermaye"].isna() & T["baz"].notna()].reset_index(drop=True)
    e = y.etiketler(vaka)
    etiketli = set(zip(e["islem_kodu"], e["tarih"]))
    # Z-skor icin en az 5 gunluk gecmis: verinin 6. gununden itibaren (Mart 2025: 10.03)
    aday = T[(T["tarih"] >= np.sort(T["tarih"].unique())[5]) & (T["islem_sayisi"] >= sd.ISLEM_EN_AZ)]
    aday = aday[[(k, t) not in etiketli for k, t in zip(aday["islem_kodu"], aday["tarih"])]]
    secim = aday.sample(n=min(adet, len(aday)), random_state=int(rng.integers(1 << 31))).reset_index(drop=True)
    parca, kayitlar, sayac, t0 = [], [], collections.Counter(), time.time()
    for n, r in enumerate(secim.itertuples()):
        gun, kod = str(r.tarih.date()), r.islem_kodu
        senaryo = SENARYOLAR[n % len(SENARYOLAR)]
        kayit = dict(gun=gun, kod=kod, senaryo=senaryo, surum=SURUM, sonuc="hata")
        kayitlar.append(kayit)
        try:
            df = veri.pay_gun_emirleri(sd.GUNLUK, gun, kod)
            tepe = veri.tepe_tahmini(df)
            gs = gunsonu_ozellikleri(sd.gunsonu(gun), gun).loc[kod]
            H = int(gs["hacim_tl"] / max(gs["kapanis"], 1e-9))
            g0 = Gun(df, gun, kod, sd.gunsonu(gun), tepe)
            g0.calistir()
            if SURUM == "yeni":
                u = ay.uret(senaryo, sd.GUNLUK, g0, df, gun, kod, sd.gunsonu(gun), tepe, H, rng, sayac[senaryo],
                            pn.PENCERE_US)
                sayac[senaryo] += 1
                if u is None:
                    kayit["sonuc"] = "yer_yok"
                    print(gun, kod, senaryo, "senaryo gunun surekli islemine sigmadi", flush=True)
                    continue
                g1, olaylar, kirli = u["g1"], u["olaylar"], not u["temiz"]
                kayit.update(u["kayit"])
                olcu = kayit.get("temizlik_olcusu", 0)
            else:
                olaylar, _ = sd.senaryo_olaylari(senaryo, g0, df, gun, H, rng)
                g1 = Gun(df, gun, kod, sd.gunsonu(gun), tepe)
                g1.calistir(olaylar)
                olcu, kirli = sd.temizlik(senaryo, g1, olaylar) if g1.kabul else (0, False)
                kayit.update(olay=len(olaylar), kabul=len(g1.kabul), red=len(g1.reddedilen), temizlik_olcusu=olcu)
            if not g1.kabul:
                red = sorted({f"{b}:{s}" for _, b, s in g1.reddedilen})
                kayit["sonuc"] = "kabul_yok"
                print(gun, kod, senaryo, "kabul edilen sentetik olay yok; red:", ", ".join(red) or "-", flush=True)
                continue
            if kirli:
                kayit["sonuc"] = "temiz_degil"
                print(gun, kod, senaryo, "temiz degil:", olcu, flush=True)
                continue
            W0 = pn.puanla(pn.pencere_ozellikleri(g0, pn.emir_olaylari(df)))
            W1 = pn.puanla(pn.pencere_ozellikleri(g1, pn.emir_olaylari(df, g1)))
            if KAPANIS_GECMISI:
                gecmis = T[(T["islem_kodu"] == kod) & (T["tarih"] < r.tarih)]
                W0 = pn.kapanis_gecmisi(W0, mo.satir(g0, df, gs), gecmis)
                W1 = pn.kapanis_gecmisi(W1, mo.satir(g1, df, gs), gecmis)
        except Exception as ex:
            kayit["hata"] = f"{type(ex).__name__}: {ex}"
            print(gun, kod, senaryo, "HATA", type(ex).__name__, ex, flush=True)
            continue
        kayit["sonuc"] = "tamam"
        pz = sorted({o.zaman // pn.PENCERE_US * pn.PENCERE_US for o, _ in g1.kabul})
        poz = W1["kapanis_muzayedesi"].to_numpy() if senaryo == "kapanis" else W1.index.isin(pz)
        kayit["pozitif_pencere"] = int(poz.sum())
        W1 = W1.assign(poz=poz, kume="enjeksiyonlu")
        W0 = W0.assign(poz=W0.index.isin(W1.index[poz]), kume="kontrol")
        for W in (W0, W1):
            parca.append(W.assign(gun=gun, kod=kod, senaryo=senaryo).reset_index(names="pencere"))
        print(n + 1, gun, kod, senaryo, int(poz.sum()), f"{time.time() - t0:.0f} sn", flush=True)
    pd.DataFrame(kayitlar).to_csv(os.path.join(out, "senaryo_kayit.csv"), index=False, encoding="utf-8")
    print(pd.DataFrame(kayitlar).groupby(["senaryo", "sonuc"]).size().to_string(), flush=True)
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
            if xs.empty:
                continue
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
