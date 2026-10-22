"""Tespit yontemleri ve SPK etiketleri (TASARIM.md 6.3): Z-skor temel cizgisi, iktisadi kurallar, Isolation Forest.

- Z-skor: her ozellik, payin onceki gunlerine gore (genisleyen pencere, gun haric; en az GECMIS_EN_AZ gun).
  Pay-gun puani: secili ozelliklerin |z| en buyugu.
- Iktisadi kurallar (VI-104.1 md 5/1; esikler tasarim parametresidir, Prosedur kurali degildir):
  a) emir iptali / degisikligi: z(iptal_orani) veya z(emir_islem_orani) >= ESIK;
  b) farkli fiyat kademelerine emir: z(fiyat_kademesi) >= ESIK;
  d) acilis / kapanis fiyatini etkileme: |z(kapanis_aof_sapma)| >= ESIK ve z(kapanis_seansi_payi) >= ESIK_2;
     ya da z(acilis_iptal_orani) >= ESIK ve |z(acilis_sapma)| >= ESIK_2;
  f) fiyat yukseltici / dusurucu: |z(getiri)| >= ESIK ve |z(aktif_dengesizlik)| >= ESIK_2 ayni yonde;
     ya da z(kucuk_islem_payi) >= ESIK ve |z(getiri)| >= ESIK_2.
  Puan: tetiklenen bent sayisi (esitlikte Z-skor puanina gore siralanir).
- Isolation Forest: z ozellikleri uzerinde (sklearn; random_state sabit).
- SPK etiketleri (veri/etiketler/vaka.csv, seviye_nihai A/B, etiket_nihai 1): A donemin islem gunleri; B tedbir
  baslangicindan onceki N = 20 islem gunu, bitis tedbirden onceki is gunu (etiket-cikarim-kurallari.md).
"""
import numpy as np
import pandas as pd

GECMIS_EN_AZ = 5
ESIK, ESIK_2 = 3.0, 2.0
N_B = 20
TATILLER = ["2025-01-01", "2025-03-31", "2025-04-01", "2025-04-23", "2025-05-01", "2025-05-19",
            "2024-06-17", "2024-06-18", "2024-06-19", "2024-07-15", "2024-08-30", "2024-10-29"]   # resmi tatiller (tam gun)
OZELLIKLER = ["getiri", "aralik", "hacim_tl", "kapanis_aof_sapma", "acilis_sapma", "kapanis_seansi_payi", "kfi_payi",
              "iptal_orani", "degisiklik_orani", "piyasa_payi", "kie_payi", "afk_payi", "fiyat_kademesi",
              "acilis_iptal_orani", "kapanis_degisiklik_yogunlugu", "aktif_dengesizlik", "kucuk_islem_payi",
              "kapanis_oncesi_getiri", "emir_islem_orani"]
LOG = {"hacim_tl", "fiyat_kademesi", "emir_islem_orani"}


def z_skorlari(df):
    """Her pay icin onceki gunlere gore z; donus: z_<ozellik> sutunlari eklenmis tablo (gecmisi yetersiz satir NaN)."""
    d = df.sort_values(["islem_kodu", "tarih"]).copy()
    for c in OZELLIKLER:
        x = np.log1p(d[c].clip(lower=0)) if c in LOG else d[c]
        g = x.groupby(d["islem_kodu"])
        ort = g.transform(lambda s: s.shift().expanding(GECMIS_EN_AZ).mean())
        ss = g.transform(lambda s: s.shift().expanding(GECMIS_EN_AZ).std())
        d["z_" + c] = (x - ort) / ss.where(ss > 1e-9)
    zc = ["z_" + c for c in OZELLIKLER]
    d["puan_zskor"] = d[zc].abs().max(axis=1, skipna=True)
    d.loc[d[zc].isna().all(axis=1), "puan_zskor"] = np.nan
    return d


def kurallar(d):
    z = lambda c: d["z_" + c]
    a = (z("iptal_orani") >= ESIK) | (z("emir_islem_orani") >= ESIK)
    b = z("fiyat_kademesi") >= ESIK
    dd = ((z("kapanis_aof_sapma").abs() >= ESIK) & (z("kapanis_seansi_payi") >= ESIK_2)) | \
         ((z("acilis_iptal_orani") >= ESIK) & (z("acilis_sapma").abs() >= ESIK_2))
    f = ((z("getiri").abs() >= ESIK) & (z("aktif_dengesizlik").abs() >= ESIK_2) & (np.sign(z("getiri")) == np.sign(z("aktif_dengesizlik")))) | \
        ((z("kucuk_islem_payi") >= ESIK) & (z("getiri").abs() >= ESIK_2))
    d = d.assign(kural_a=a, kural_b=b, kural_d=dd, kural_f=f)
    d["kural_sayisi"] = d[["kural_a", "kural_b", "kural_d", "kural_f"]].sum(axis=1)
    d["puan_kural"] = d["kural_sayisi"] + d["puan_zskor"].fillna(0) / 1000   # esitlikte Z-skor
    return d


def isolation_forest(d, random_state=0):
    from sklearn.ensemble import IsolationForest
    zc = ["z_" + c for c in OZELLIKLER]
    m = d["puan_zskor"].notna()
    X = d.loc[m, zc].fillna(0).clip(-10, 10).to_numpy()
    model = IsolationForest(n_estimators=300, random_state=random_state).fit(X)
    d = d.copy()
    d["puan_iforest"] = np.nan
    d.loc[m, "puan_iforest"] = -model.score_samples(X)
    return d


COK_GUN = ["getiri_5g", "hacim_artisi_5g"]


def cok_gunlu(d):
    """Payin son 5 gunu (gun dahil): birikimli getiri; hacmin onceki 5 gun ortalamasina orani."""
    d = d.sort_values(["islem_kodu", "tarih"]).copy()
    g = d.groupby("islem_kodu")
    d["getiri_5g"] = g["getiri"].transform(lambda s: np.exp(np.log1p(s).rolling(5, min_periods=3).sum()) - 1)
    d["hacim_artisi_5g"] = d["hacim_tl"] / g["hacim_tl"].transform(lambda s: s.shift().rolling(5, min_periods=3).mean())
    return d


def kesitsel(d, random_state=0):
    """Kesitsel karsilastirma: her ozellik, ayni gun ayni pazardaki paylar icinde yuzdelik sira (k_*).
    Puan: Isolation Forest (k_* uzerinde) ve en uc sira (|2 sira - 1|) ortalamasi. Payin kendi gecmisi uzun suren
    manipulasyonda kirlenebilir; kesitsel karsilastirma buna duyarli degildir."""
    from sklearn.ensemble import IsolationForest
    d = cok_gunlu(d)
    kc = []
    for c in OZELLIKLER + COK_GUN:
        d["k_" + c] = d.groupby(["tarih", "pazar"])[c].rank(pct=True)
        kc.append("k_" + c)
    X = d[kc].fillna(0.5).to_numpy()
    d["puan_kesit_uc"] = np.abs(2 * X - 1).mean(axis=1)
    d["puan_kesit_iforest"] = -IsolationForest(n_estimators=300, random_state=random_state).fit(X).score_samples(X)
    return d


def is_gunleri(bas, bit):
    return pd.DatetimeIndex(np.arange(np.datetime64(bas, "D"), np.datetime64(bit, "D") + 1)).to_series().pipe(
        lambda s: s[np.is_busday(s.values.astype("datetime64[D]"), holidays=TATILLER)]).index


def etiketler(vaka_csv):
    """Pay-gun etiket tablosu: islem_kodu, tarih, seviye (A/B), kaynak bulten."""
    v = pd.read_csv(vaka_csv, encoding="utf-8-sig", dtype=str)
    v = v[v["seviye_nihai"].isin(["A", "B"]) & (v["etiket_nihai"] == "1") & v["pay_kodu"].notna()]
    satir = []
    for r in v.itertuples():
        if r.seviye_nihai == "A" and isinstance(r.nihai_donem_bas, str):
            gunler = is_gunleri(r.nihai_donem_bas, r.nihai_donem_bit)
        elif r.seviye_nihai == "B" and isinstance(r.nihai_tedbir_bas, str):
            t = np.datetime64(r.nihai_tedbir_bas, "D")
            bit = np.busday_offset(t, -1, roll="backward", holidays=TATILLER)
            bas = np.busday_offset(bit, -(N_B - 1), roll="backward", holidays=TATILLER)
            gunler = is_gunleri(str(bas), str(bit))
        else:
            continue
        satir += [(r.pay_kodu + ".E", g, r.seviye_nihai, r.bulten) for g in gunler]
    e = pd.DataFrame(satir, columns=["islem_kodu", "tarih", "seviye", "bulten"])
    # ayni pay-gun birden cok kayitta: A onceliklidir
    return e.sort_values("seviye").drop_duplicates(["islem_kodu", "tarih"], keep="first")


def degerlendir(d, puanlar, etiket_sutunu="pozitif", ust=0.01):
    """Pay-gun siralama olcutleri: ROC-AUC, ortalama kesinlik, en yuksek %ust dilimde duyarlilik ve kesinlik."""
    from sklearn.metrics import roc_auc_score, average_precision_score
    out = []
    for p in puanlar:
        m = d[p].notna()
        y, s = d.loc[m, etiket_sutunu].astype(int).to_numpy(), d.loc[m, p].to_numpy()
        if y.sum() == 0 or y.sum() == len(y):
            continue
        k = max(1, int(round(ust * len(y))))
        ilk = np.argsort(-s, kind="stable")[:k]
        out.append(dict(puan=p, pay_gun=len(y), pozitif=int(y.sum()), roc_auc=roc_auc_score(y, s),
                        ort_kesinlik=average_precision_score(y, s), taban_oran=y.mean(),
                        ust_dilim=k, ust_dilim_duyarlilik=y[ilk].sum() / y.sum(), ust_dilim_kesinlik=y[ilk].mean()))
    return pd.DataFrame(out)
