"""SPK etiketleriyle pay-gun degerlendirmesi (TASARIM.md 6.3): Z-skor, iktisadi kurallar, Isolation Forest.

Pozitif: SPK etiketli pay-gun (A ve/veya B). Etiketsiz gun negatif degildir (bilinmiyor; etiket-cikarim-kurallari.md);
olcutler bu nedenle siralama olcutleridir ve alt sinir olarak okunmalidir. Ozsermaye gunleri disarida birakilir.
Kullanim: python -I tespit/degerlendir.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU
"""
import os, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yontemler as y

PUANLAR = ["puan_zskor", "puan_kural", "puan_iforest", "puan_kesit_uc", "puan_kesit_iforest"]

if __name__ == "__main__":
    oz, vaka, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    d = pd.read_parquet(oz)
    d = d[d["ozsermaye"].isna() & d["baz"].notna()]
    d = y.kesitsel(y.isolation_forest(y.kurallar(y.z_skorlari(d))))
    e = y.etiketler(vaka)
    d = d.merge(e, on=["islem_kodu", "tarih"], how="left")
    sonuc = []
    for ad, kosul in [("A+B", d["seviye"].notna()), ("A", d["seviye"] == "A"), ("B", d["seviye"] == "B")]:
        x = d[kosul | d["seviye"].isna()].assign(pozitif=kosul)
        r = y.degerlendir(x, PUANLAR)
        r.insert(0, "etiket", ad)
        sonuc.append(r)
    R = pd.concat(sonuc, ignore_index=True)
    R.to_csv(os.path.join(out, "degerlendirme.csv"), index=False, encoding="utf-8")
    print(R.round(4).to_string(index=False))
    # bent bazinda: etiketli pay-gunlerde kural tetiklenme orani ve genel oran
    b = d.groupby(d["seviye"].fillna("etiketsiz"))[["kural_a", "kural_b", "kural_d", "kural_f"]].mean()
    b.to_csv(os.path.join(out, "kural_oranlari.csv"), encoding="utf-8")
    print(b.round(4).to_string())
    # etiketli paylarin gun bazinda siralamasi (gunun icindeki yuzdelik; 1 = en supheli)
    for p in PUANLAR:
        d["sira_" + p] = d.groupby("tarih")[p].rank(pct=True)
    s = d[d["seviye"].notna()].groupby(["islem_kodu", "seviye"])[["sira_" + p for p in PUANLAR]].mean()
    s.to_csv(os.path.join(out, "etiketli_siralama.csv"), encoding="utf-8")
    print(s.round(3).to_string())
    d.to_parquet(os.path.join(out, "puanlar.parquet"))
