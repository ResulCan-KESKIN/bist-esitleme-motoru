"""Tek fiyatta aday seviyelerde yonun karisik oldugu muzayedeler (kullanici karari 21.10.2026).

Kural: Adim 2 sonrasi adaylar arasinda referans fiyata (baz) / son islem fiyatina en yakin seviye; esitlik
surerse esit uzak adaylarin orta noktasi (en yakin fiyat adimina). Kurala uymayan vakalar zorlanmaz,
yon_karisik_istisna = 1 ile isaretlenir.
Girdi: gunici_tek_fiyat_kontrol.py ciktisi (aday_fiyatlar, aday_fazla saklidir; karar yalniz bunlara ve
referansa baglidir). Gun sonu: grup -> fiyat adimi tablosu.
Kullanim: python -I gunici_tek_fiyat_karisik.py TEK_FIYAT_SONUC.parquet GUNSONU.parquet CIKTI.csv
"""
import sys, os, ast
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import GRUP_TABLO, yukari_adim, asagi_adim

src, gs_src, out = sys.argv[1:4]
R = pd.read_parquet(src)
a = R[(R.kotasyon == "haric") & R.sinirli & R.adim.fillna("").str.startswith("adim4_") &
      R.yon.eq("karisik")].copy()


def karar(adaylar, ref, tablo):
    P = np.array(adaylar, dtype=np.int64)
    if ref is None or not ref == ref or ref <= 0:
        return None, "referans_yok"
    uz = np.abs(P - ref)
    k = P[uz == uz.min()]
    if len(k) == 1:
        return int(k[0]), "en_yakin"
    ort = (int(k.max()) + int(k.min())) / 2
    lo, hi = asagi_adim(ort, tablo), yukari_adim(ort, tablo)
    return int(hi if (hi - ort) <= (ort - lo) else lo), "esitlik_orta_nokta"


satir = []
for (t, kod, M), g in a.groupby(["tarih", "islem_kodu", "M"]):
    r0 = g.iloc[0]
    tablo = GRUP_TABLO[r0.grup]
    adaylar = ast.literal_eval(r0.aday_fiyatlar)
    fazla = ast.literal_eval(r0.aday_fazla)
    d = dict(tarih=t, islem_kodu=kod, sinif=r0.sinif, M=M, gercek_fiyat=r0.gercek_fiyat, baz=r0.baz,
             son_islem=r0.son_islem, aday_alt=min(adaylar), aday_ust=max(adaylar), n_aday=len(adaylar),
             alis_fazlali_seviye=sum(f > 0 for f in fazla), satis_fazlali_seviye=sum(f < 0 for f in fazla))
    for ad, ref in (("baz", r0.baz), ("son", r0.son_islem if r0.son_islem == r0.son_islem else r0.baz)):
        f, how = karar(adaylar, ref, tablo)
        d[f"fiyat_{ad}"], d[f"karar_{ad}"] = f, how
        d[f"uyar_{ad}"] = f is not None and f == r0.gercek_fiyat
    # yonun alistan satisa dondugu sinir seviyeleri (bilgi)
    i = [j for j in range(len(fazla) - 1) if np.sign(fazla[j]) != np.sign(fazla[j + 1])]
    d["donus_seviyeleri"] = ";".join(f"{adaylar[j]}/{adaylar[j + 1]}" for j in i)
    d["yon_karisik_istisna"] = int(not (d["uyar_baz"] or d["uyar_son"]))
    satir.append(d)
T = pd.DataFrame(satir)
if T.empty:   # o ayda karisik yonlu muzayede yok (or. 2024-08)
    T = pd.DataFrame(columns=["tarih", "islem_kodu", "M", "yon_karisik_istisna"])
T.to_csv(out, index=False, encoding="utf-8")
pd.set_option("display.width", 250)
print(T.to_string())
print("karisik yon vakasi:", len(T), "kurala uyan:", int((T.yon_karisik_istisna == 0).sum()),
      "istisna:", int(T.yon_karisik_istisna.sum()))
