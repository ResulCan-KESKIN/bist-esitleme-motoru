"""SPK etiketleriyle denetimli model, pay-gun duzeyi (TASARIM.md 6.3).

Ornek: pay-gun (ozellikler.parquet; ozsermaye gunleri ve baz fiyati olmayanlar disarida). Hedef: SPK etiketi A ya da B
(yontemler.etiketler; tedbirden onceki 2 belirsiz is gunu disarida). Etiketsiz pay-gun negatif sayilir ama temiz oldugu
bilinmez: olcutler alt sinirdir.
Girdiler (paya ozgu duzeyi tasimayan oransal ya da goreli gostergeler):
- yontemler.OZELLIKLER'in ham degerleri (duzey tasiyan hacim_tl ve fiyat_kademesi haric);
- payin kendi gecmisine gore z (z_*), ayni gun ayni pazara gore yuzdelik sira (k_*), 5 gunluk getiri ve hacim artisi;
- endeks gostergeleri (endeks_ozellikleri.py; varsa): fazla_getiri, sektor_fazla_getiri ve onlarin z / k karsiliklari.
Girdi olmayanlar: pazar, BIST 100 uyeligi, piyasa yapici, brut takas (tedbir: etiketle sizinti), fiyat ve hacim duzeyi,
sektor, piyasa degeri, gune ozgu piyasa / sektor getirisi (o gun butun paylarda ayni: pay gruplu dogrulamada etiketli
gunler gun uzerinden taninabilir).
Model: gradyan artirmali karar agaci; dengesiz sinif icin sinif agirligi; asiri ogrenmeye karsi sabit, kucuk agac
ayarlari (ayar aramasi yok: test katlarina bakilarak secilmedi).
Dogrulama: paya gore gruplu, pozitif paylari katlara dengeleyen 5 katli capraz dogrulama (StratifiedGroupKFold); ayni
payin hicbir gunu egitim ve testte bir arada olmaz. Her pay-gunun puani o payi gormemis katin modelinden gelir.
Iki surum: endeks gostergeleriyle ve onlarsiz (katkiyi olcmek icin). Karsilastirma: ayni satirlarda egitimsiz puanlar
(Z-skor, kurallar, Isolation Forest, kesitsel).
Olcutler: ROC-AUC, ortalama kesinlik (taban oranla), en ust %1'de duyarlilik ve kesinlik; A ve B ayri; kat bazinda
ROC-AUC (belirsizlik); etiketli paylarin gunlerinin gun icindeki ortalama yuzdelik sirasi; test katlarinda permutasyon
onemi.
Kullanim: python -I tespit/spk_denetimli.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU
"""
import os, sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yontemler as y

DUZEY = {"hacim_tl", "fiyat_kademesi"}
ENDEKS = ["fazla_getiri", "sektor_fazla_getiri"]
TABAN = ["puan_zskor", "puan_kural", "puan_iforest", "puan_kesit_uc", "puan_kesit_iforest"]
KAT = 5


def ek_z_k(d, sutunlar):
    """yontemler.z_skorlari ve kesitsel ile ayni tanimla ek sutunlarin z ve k karsiliklari."""
    d = d.sort_values(["islem_kodu", "tarih"]).copy()
    for c in sutunlar:
        g = d[c].groupby(d["islem_kodu"])
        ort = g.transform(lambda s: s.shift().expanding(y.GECMIS_EN_AZ).mean())
        ss = g.transform(lambda s: s.shift().expanding(y.GECMIS_EN_AZ).std())
        d["z_" + c] = (d[c] - ort) / ss.where(ss > 1e-9)
        d["k_" + c] = d.groupby(["tarih", "pazar"])[c].rank(pct=True)
    return d


def model():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=100,
                                          l2_regularization=1.0, class_weight="balanced", early_stopping=False,
                                          random_state=0)


def capraz(d, girdiler, ad, out, onem=True):
    X, yy, gr = d[girdiler], d["pozitif"].astype(int).to_numpy(), d["islem_kodu"].to_numpy()
    puan, katlar, imp = np.full(len(d), np.nan), [], []
    for k, (egit, test) in enumerate(StratifiedGroupKFold(n_splits=KAT, shuffle=True, random_state=0).split(X, yy, gr)):
        m = model().fit(X.iloc[egit], yy[egit])
        puan[test] = m.predict_proba(X.iloc[test])[:, 1]
        katlar.append(dict(surum=ad, kat=k, test_pozitif=int(yy[test].sum()), test_pozitif_pay=len(set(gr[test][yy[test] == 1])),
                           roc_auc=roc_auc_score(yy[test], puan[test]) if 0 < yy[test].sum() < len(test) else np.nan))
        if onem and yy[test].sum() > 0:
            r = permutation_importance(m, X.iloc[test], yy[test], scoring="average_precision", n_repeats=3,
                                       random_state=0, n_jobs=1)
            imp.append(pd.Series(r.importances_mean, index=girdiler))
    if imp:
        pd.concat(imp, axis=1).mean(axis=1).sort_values(ascending=False).rename("onem").to_csv(
            os.path.join(out, f"spk_denetimli_onem_{ad}.csv"), encoding="utf-8")
    return puan, pd.DataFrame(katlar)


if __name__ == "__main__":
    src, vaka, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    d = pd.read_parquet(src)
    d = d[d["ozsermaye"].isna() & d["baz"].notna()]
    d = y.kesitsel(y.isolation_forest(y.kurallar(y.z_skorlari(d))))
    endeks = [c for c in ENDEKS if c in d.columns]
    if endeks:
        d = ek_z_k(d, endeks)
    e = y.etiketler(vaka)
    d = d.merge(e, on=["islem_kodu", "tarih"], how="left")
    d = d[d["seviye"] != "B_belirsiz"].reset_index(drop=True)
    d["pozitif"] = d["seviye"].isin(["A", "B"])
    temel = ([c for c in y.OZELLIKLER if c not in DUZEY] + ["z_" + c for c in y.OZELLIKLER]
             + ["k_" + c for c in y.OZELLIKLER + y.COK_GUN] + y.COK_GUN)
    ek = endeks + ["z_" + c for c in endeks] + ["k_" + c for c in endeks]
    print(f"pay-gun {len(d):,}, pozitif {int(d['pozitif'].sum())} (A {int((d['seviye'] == 'A').sum())}, "
          f"B {int((d['seviye'] == 'B').sum())}), pozitif pay {d.loc[d['pozitif'], 'islem_kodu'].nunique()}, "
          f"girdi {len(temel)} + endeks {len(ek)}", flush=True)
    K = []
    d["puan_spk_denetimli"], k1 = capraz(d, temel + ek, "endeksli", out)
    K.append(k1)
    if ek:
        d["puan_spk_denetimli_endekssiz"], k2 = capraz(d, temel, "endekssiz", out, onem=False)
        K.append(k2)
    K = pd.concat(K, ignore_index=True)
    K.to_csv(os.path.join(out, "spk_denetimli_kat.csv"), index=False, encoding="utf-8")
    puanlar = ["puan_spk_denetimli"] + (["puan_spk_denetimli_endekssiz"] if ek else []) + TABAN
    R = []
    for etiket, kosul in [("A+B", d["pozitif"]), ("A", d["seviye"] == "A"), ("B", d["seviye"] == "B")]:
        x = d[kosul | d["seviye"].isna()].assign(pozitif=kosul)
        r = y.degerlendir(x, puanlar)
        r.insert(0, "etiket", etiket)
        R.append(r)
    R = pd.concat(R, ignore_index=True)
    R.to_csv(os.path.join(out, "spk_denetimli_degerlendirme.csv"), index=False, encoding="utf-8")
    for p in puanlar:
        d["sira_" + p] = d.groupby("tarih")[p].rank(pct=True)
    s = d[d["pozitif"]].groupby(["islem_kodu", "seviye"])[["sira_" + p for p in puanlar]].mean()
    s.insert(0, "gun", d[d["pozitif"]].groupby(["islem_kodu", "seviye"]).size())
    s.to_csv(os.path.join(out, "spk_denetimli_siralama.csv"), encoding="utf-8")
    d[["islem_kodu", "tarih", "seviye", "pozitif"] + puanlar].to_parquet(os.path.join(out, "spk_denetimli_puanlar.parquet"))
    pd.set_option("display.width", 200)
    print(R.round(4).to_string(index=False))
    print(K.round(3).to_string(index=False))
    print(s.round(3).to_string())
    f = os.path.join(out, "spk_denetimli_onem_endeksli.csv")
    if os.path.exists(f):
        print(pd.read_csv(f, index_col=0).head(15).round(4).to_string())
