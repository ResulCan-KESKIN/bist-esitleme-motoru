"""Yeni emirlerin (degisiklik sebebi 6) seans bolumu x emir tipi dagilimi; Ek-19 matrisiyle karsilastirma.

Girdi: gunici_emir_profil.py ciktisi emir_kategorik.parquet ve ekler/ek19.md.
Emir tipi esleme (DataStore referans tablolari): A limit = fiyat turu 1 ve kategori 1 (normal emir); B piyasa = 2; C piyasadan limite = 3;
D KIE = gecerlilik IMMEDIATE; E orta nokta = emir turu 64; F dengeleyici = fiyat turu 66 (64 Imbalance + 2);
H kotasyon = kategori 4; N ozel islem bildirimi = kategori 32; O aciga satis = emir turu 2.
Kullanim: python -I gunici_ek19_kontrol.py emir_kategorik.parquet ek19.md CIKTI.csv
"""
import sys, re
import pandas as pd

src, ek19, out = sys.argv[1:4]
mat = {}
for satir in open(ek19, encoding="utf-8"):
    h = [c.strip() for c in satir.strip().strip("|").split("|")]
    if len(h) == 17 and h[0].startswith("P"):
        mat[h[0]] = dict(zip("ABCDEFGHIJKLMNOP", h[1:]))
A = pd.read_parquet(src)
y = A[A.degisiklik_sebebi == 6].copy()
tip = {
    "A": (y.emir_fiyat_turu == 1) & (y.emir_kategorisi == 1), "B": y.emir_fiyat_turu == 2, "C": y.emir_fiyat_turu == 3,
    "D": y.gecerlilik_turu == "IMMEDIATE", "E": (y.emir_turu & 64) > 0, "F": y.emir_fiyat_turu == 66,
    "H": y.emir_kategorisi == 4, "N": y.emir_kategorisi == 32, "O": (y.emir_turu & 2) > 0,
}
satirlar = []
for s, g in y.groupby("seans"):
    for k, m in tip.items():
        n = int(g.loc[m.loc[g.index], "count_all_sum"].sum())
        izin = mat.get(s, {}).get(k, "?")
        satirlar.append((s, k, n, izin, "IHLAL" if n > 0 and izin == "0" else ""))
r = pd.DataFrame(satirlar, columns=["seans", "tip", "yeni_emir", "ek19", "durum"])
r.to_csv(out, index=False, encoding="utf-8")
print(r[r.yeni_emir > 0].to_string())
print("ek19'da olmayan bolumler:", sorted(set(y.seans) - set(mat)))
