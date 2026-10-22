"""gunici_tek_fiyat_kontrol.py ciktisinin ozeti: varyant karsilastirmasi ve aciklanan/aciklanmayan uyumsuzluklar.

Aciklanan disi birakmalar:
  - ozsermaye: gun sonu corporate_action dolu (baz fiyat duzeltilmemis onceki kapanis)
  - kesilen: muzayede eslestirme bolumune ulasmadan EBDKS durdurmasina girdi (emir toplama kosusunu izleyen
    kosu P_GECICI_DUR* EBDK bolumu; seans kosulari tablosundan)
Kullanim: python -I gunici_tek_fiyat_ozet.py TEK_FIYAT_SONUC.parquet SEANS_KOSULARI.parquet GUNSONU.parquet CIKTI_KLASORU
"""
import sys, os
import numpy as np
import pandas as pd

src, dk_src, gs_src, out = sys.argv[1:5]
R = pd.read_parquet(src)
R["uy"] = R.fiyat.fillna(-1).astype("int64") == R.gercek_fiyat.fillna(-1).astype("int64")
R["miktar_uy"] = R.miktar_dengeleyicili.fillna(0).astype("int64") == R.gercek_miktar.fillna(0).astype("int64")
gs = pd.read_parquet(gs_src, columns=["trade_date", "instrument_series_code", "corporate_action"])
oz = set(zip(gs.loc[gs.corporate_action.notna(), "trade_date"], gs.loc[gs.corporate_action.notna(), "instrument_series_code"]))
K = pd.read_parquet(dk_src).sort_values(["tarih", "islem_kodu", "sira"])
K["sonraki"] = K.groupby(["tarih", "islem_kodu"]).seans.shift(-1)
kk = K[K.sonraki.fillna("").str.startswith("P_GECICI_DUR") & K.sonraki.fillna("").str.contains("EBDK")]
kes = {}
for t, k, son in zip(kk.tarih, kk.islem_kodu, kk.son):
    kes.setdefault((pd.Timestamp(t).date(), k), []).append(pd.Timestamp(son))
R["ozsermaye"] = [(t, k) in oz for t, k in zip(R.tarih, R.islem_kodu)]
# M = son toplama satiri + 1 us (eslestirme satiri yoksa); kosu sonu M'den 1 sn icinde olmali
R["kesilen"] = ~R.eslestirme_satiri & R.gercek_fiyat.isna() & pd.Series(
    [any(abs((pd.Timestamp(m) - s).total_seconds()) < 1 for s in kes.get((t, k), []))
     for t, k, m in zip(R.tarih, R.islem_kodu, R.M)], index=R.index)
R["temiz"] = ~R.ozsermaye & ~R.kesilen
# karisik yonde kurala (referansa en yakin, esitlikte orta nokta) uymayan vaka: istisna bayragi
R["yon_karisik_istisna"] = (R.adim.fillna("").str.startswith("adim4_") & R.yon.eq("karisik") & ~R.uy).astype(int)

var = R.groupby(["kotasyon", "ref_tur", "sinirli", "sinif"]).agg(n=("uy", "size"), fiyat=("uy", "sum")).reset_index()
var.to_csv(os.path.join(out, "varyantlar.csv"), index=False, encoding="utf-8")
a = R[(R.kotasyon == "haric") & (R.ref_tur == "baz") & R.sinirli]
tab = a.groupby("sinif").agg(muzayede=("uy", "size"), fiyat_uyan=("uy", "sum"), ozsermaye=("ozsermaye", "sum"),
                             kesilen=("kesilen", "sum"))
t = a[a.temiz].groupby("sinif").agg(temiz=("uy", "size"), temiz_fiyat=("uy", "sum"), temiz_miktar=("miktar_uy", "sum"))
tab = tab.join(t)
tab.loc["toplam"] = tab.sum()
tab.to_csv(os.path.join(out, "ozet.csv"), encoding="utf-8")
print(tab.to_string())
print(a[a.temiz].groupby(["sinif", "adim"]).agg(n=("uy", "size"), fiyat=("uy", "sum")).to_string())
# Adim 4 referans ayrimi
b = R[(R.kotasyon == "haric") & (R.ref_tur == "son") & R.sinirli].set_index(["tarih", "islem_kodu", "M"])
x = a[a.temiz & a.adim.str.startswith("adim4")].set_index(["tarih", "islem_kodu", "M"])
y = b.loc[x.index]
print(f"Adim 4: {len(x)} muzayede; baz referansla uyan {int(x.uy.sum())}, son islem referansla uyan {int(y.uy.sum())}, "
      f"iki referans farkli {int((x.baz != y.son_islem).sum())}")
kalan = a[a.temiz & ~a.uy]
kalan.to_csv(os.path.join(out, "aciklanmayan_uyumsuz.csv"), index=False, encoding="utf-8")
print("aciklanmayan uyumsuz:", len(kalan))
print(kalan[["tarih", "islem_kodu", "pazar", "sinif", "M", "gercek_fiyat", "gercek_miktar", "fiyat", "miktar", "adim",
             "n_kotasyon", "yon_karisik_istisna"]].to_string())
