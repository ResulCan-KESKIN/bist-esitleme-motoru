"""Muzayede eslestirme anlari: islem defterindeki ESLESTIRME islemlerinin gun ve asama bazinda zaman dagilimi.

Her (gun, islem_kodu, asama) icin ilk islem zamani alinir; asama icinde paylar arasi yayilim ve nominal
saate gore gecikme (sn) raporlanir. Asama: P_ESLESTIRME / P_ESLESTIRMETEKFIYAT / P_ESLESTIRME_EBDK + saat.
Kullanim: python -I gunici_eslestirme_zamani.py ISLEM.parquet CIKTI.csv
"""
import sys
import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

src, out = sys.argv[1:3]
t = pq.read_table(src, columns=["tarih", "islem_kodu", "islem_zamani", "seans", "alis_satis"],
                  filters=[("alis_satis", "=", "A")])
t = t.filter(pc.is_in(t["seans"], value_set=pc.cast(pc.unique(t["seans"]), t["seans"].type).filter(
    pc.match_substring(pc.unique(t["seans"]), "ESLESTIRME"))))
df = t.to_pandas()
df["saniye"] = pd.to_timedelta(df["islem_zamani"]).dt.total_seconds()
ilk = df.groupby(["tarih", "islem_kodu", "seans", df["islem_zamani"].str[:5]])["saniye"].min().reset_index()
ilk = ilk.rename(columns={"islem_zamani": "dakika"})
ilk["nominal"] = pd.to_timedelta(ilk["dakika"] + ":00").dt.total_seconds()
ilk["gecikme"] = ilk["saniye"] - ilk["nominal"]
r = ilk.groupby(["seans", "dakika", "tarih"]).agg(pay=("gecikme", "size"), en_erken=("gecikme", "min"),
                                                  en_gec=("gecikme", "max")).reset_index()
r["yayilim"] = r["en_gec"] - r["en_erken"]
r.to_csv(out, index=False, encoding="utf-8")
ozet = r[r.pay >= 5].groupby(["seans", "dakika"]).agg(gun=("tarih", "size"), pay_ort=("pay", "mean"),
                                                     gecikme_min=("en_erken", "min"), gecikme_max=("en_erken", "max"),
                                                     yayilim_max=("yayilim", "max"))
print(ozet.round(3).to_string())
