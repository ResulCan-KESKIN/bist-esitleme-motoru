"""PP_GUNICIISLEM -> pay-gun ozetleri; PP_GUNSONUFIYATHACIM ile alan alan karsilastirma.

Her islem iki satirdir (A ve S, ayni ortak_sozlesme_no); ozetler yalniz A satirlarindan kurulur.
Bolum (asama) sinifi: seans adi + saat (P_ESLESTIRME 12:00 oncesi acilis, 18:00 sonrasi kapanis,
arasi pay bazinda devre kesici eslestirmesi).
Kullanim: python -I gunici_islem_gunsonu_karsilastir.py ISLEM.parquet GUNSONU.parquet CIKTI_KLASORU
"""
import sys, os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

src, gs_src, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
pf = pq.ParquetFile(src)
cols = ["tarih", "islem_kodu", "ortak_sozlesme_no", "alis_satis", "islem_adedi", "islem_fiyati",
        "islem_hacmi", "islem_zamani", "normal_islem", "seans", "islem_durumu"]

# satir gruplarini tarihe gore ayir (dosya tarihe gore buyuk olcude sirali)
idx = pf.schema_arrow.get_field_index("tarih")
gunler = {}
for i in range(pf.num_row_groups):
    s = pf.metadata.row_group(i).column(idx).statistics
    for d in pd.date_range(s.min, s.max).date:
        gunler.setdefault(d, []).append(i)


def asama(seans, saat):
    a = np.full(len(seans), "diger", dtype=object)
    a[seans == "P_SUREKLI_ISLEM"] = "surekli"
    e = seans == "P_ESLESTIRME"
    a[e & (saat < "12")] = "acilis"
    a[e & (saat >= "18")] = "kapanis"
    a[e & (saat >= "12") & (saat < "18")] = "dk_eslestirme"
    a[e & (saat < "12") & (saat >= "10")] = "dk_eslestirme"
    a[seans == "P_ESLESTIRME_EBDK"] = "ebdk_eslestirme"
    tf = seans == "P_ESLESTIRMETEKFIYAT"
    a[tf & (saat < "10")] = "acilis"
    a[tf & (saat >= "18")] = "kapanis"
    a[tf & (saat >= "10") & (saat < "18")] = "tf_gun_ici"
    a[seans == "P_KAPANIS_FIY_ISLEM"] = "kapanis_fiyatindan"
    return a


ozet = []
for d in sorted(gunler):
    t = pf.read_row_groups(gunler[d], columns=cols)
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["alis_satis"], "A")))
    df = t.to_pandas()
    df["asama"] = asama(df["seans"].to_numpy(), df["islem_zamani"].str[:2].to_numpy())
    df["ozel"] = df["normal_islem"].isin([3, 5])
    df = df.sort_values(["islem_zamani", "ortak_sozlesme_no"], kind="stable")
    nor = df[~df["ozel"]]
    g = nor.groupby("islem_kodu", sort=False)
    o = pd.DataFrame({
        "adet": g.size(), "miktar": g["islem_adedi"].sum(), "hacim": g["islem_hacmi"].sum(),
        "ilk": g["islem_fiyati"].first(), "son": g["islem_fiyati"].last(),
        "en_dusuk": g["islem_fiyati"].min(), "en_yuksek": g["islem_fiyati"].max(),
        "hacim_fxq": (nor["islem_fiyati"] * nor["islem_adedi"]).groupby(nor["islem_kodu"]).sum(),
    })
    for a in ["acilis", "kapanis", "kapanis_fiyatindan", "surekli", "dk_eslestirme", "ebdk_eslestirme", "tf_gun_ici"]:
        x = nor[nor["asama"] == a].groupby("islem_kodu")
        o[a + "_adet"] = x.size()
        o[a + "_miktar"] = x["islem_adedi"].sum()
        o[a + "_hacim"] = x["islem_hacmi"].sum()
        o[a + "_fiyat_n"] = x["islem_fiyati"].nunique()
        o[a + "_fiyat"] = x["islem_fiyati"].last()
    oz = df[df["ozel"]].groupby("islem_kodu")
    o["ozel_adet"] = oz.size()
    o["ozel_miktar"] = oz["islem_adedi"].sum()
    o["ozel_hacim"] = oz["islem_hacmi"].sum()
    # kapanis fiyatindan islemler haric son fiyat (bulten "kapanis fiyati" tanimi icin aday)
    k = nor[nor["asama"] != "kapanis_fiyatindan"].groupby("islem_kodu")["islem_fiyati"].last()
    o["son_kfi_haric"] = k
    o["tarih"] = d
    ozet.append(o.reset_index())
    print(d, len(df), flush=True)

oz = pd.concat(ozet, ignore_index=True)
oz.to_parquet(os.path.join(out, "islem_pay_gun_ozet.parquet"))

gs = pd.read_parquet(gs_src).rename(columns={"trade_date": "tarih", "instrument_series_code": "islem_kodu"})
m = gs.merge(oz, on=["tarih", "islem_kodu"], how="outer", indicator=True)
m.to_parquet(os.path.join(out, "gunsonu_islem_birlesik.parquet"))

sat = []
def kiyas(ad, a, b, tol=0.0):
    a = a.fillna(0).astype(float); b = b.fillna(0).astype(float)
    ok = (a - b).abs() <= tol
    sat.append((ad, int(len(a)), int(ok.sum()), int((~ok).sum())))
    return ~ok

islem_goren = m[(m["total_number_of_contracts"].fillna(0) > 0) | (m["adet"].fillna(0) > 0)]
x = islem_goren
kiyas("toplam sozlesme = normal islem adedi", x["total_number_of_contracts"], x["adet"])
kiyas("toplam miktar = normal islem miktari", x["total_traded_volume"], x["miktar"])
kiyas("toplam hacim = sum(islem_hacmi) (0,01)", x["total_traded_value"], x["hacim"], 0.011)
kiyas("en dusuk fiyat", x["lowest_price"], x["en_dusuk"])
kiyas("en yuksek fiyat", x["highest_price"], x["en_yuksek"])
kiyas("acilis fiyati = ilk islem", x["opening_price"], x["ilk"])
kiyas("kapanis fiyati = son islem (tumu)", x["closing_price"], x["son"])
kiyas("kapanis fiyati = son islem (kapanis fiyatindan haric)", x["closing_price"], x["son_kfi_haric"])
kiyas("AOF = hacim/miktar (3 hane, 0,0005)", x["vwap"], (x["hacim"] / x["miktar"]).round(3), 0.0006)
kiyas("acilis seansi fiyati", x["opening_session_price"], x["acilis_fiyat"])
kiyas("acilis seansi sozlesme", x["number_of_contracts_at_opening_session"], x["acilis_adet"])
kiyas("acilis seansi miktar", x["traded_volume_at_opening_session"], x["acilis_miktar"])
kiyas("acilis seansi hacim (0,01)", x["traded_value_at_opening_session"], x["acilis_hacim"], 0.011)
kiyas("kapanis seansi fiyati", x["closing_session_price"], x["kapanis_fiyat"])
kiyas("kapanis seansi sozlesme", x["number_of_contracts_at_closing_session"], x["kapanis_adet"])
kiyas("kapanis seansi miktar", x["traded_volume_at_closing_session"], x["kapanis_miktar"])
kiyas("kapanis fiyatindan sozlesme", x["number_of_contracts_of_trades_at_closing_price"], x["kapanis_fiyatindan_adet"])
kiyas("kapanis fiyatindan miktar", x["traded_volume_of_trades_at_closing_price"], x["kapanis_fiyatindan_miktar"])
kiyas("ozel islem bildirimi sayisi", x["number_of_trade_reports"], x["ozel_adet"])
kiyas("ozel islem bildirimi miktari", x["trade_report_traded_volume"], x["ozel_miktar"])
r = pd.DataFrame(sat, columns=["kontrol", "pay_gun", "uyan", "uymayan"])
r.to_csv(os.path.join(out, "gunsonu_karsilastirma.csv"), index=False, encoding="utf-8")
print(r.to_string())
print(m["_merge"].value_counts().to_dict())
