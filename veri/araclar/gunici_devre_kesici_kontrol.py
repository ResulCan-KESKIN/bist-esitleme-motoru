"""Pay bazinda devre kesici: sureler ve tetikleme orani (gun ici emir + islem verisi).

Girdi: gunici_seans_akis_kontrol.py ciktisi devre_kesici_olaylari.parquet, aylik islem ve gun sonu parquet.
Tetikleme ani T = DK bolumune gecisten onceki son surekli islem satiri. Referans fiyat (06-devre-kesici.md
madde 8): T'den onceki son tek fiyat (muzayede) islem fiyati; yoksa baz fiyat (onceki kapanis).
Olcum: T'den onceki son surekli islem fiyatinin referansa orani; ayrica gun boyunca tum surekli islemlerin
o anki referansa gore en buyuk sapmasi (pazar bazinda) - tetikleme sinirinin ust siniri.
Kullanim: python -I gunici_devre_kesici_kontrol.py DK_OLAYLARI.parquet ISLEM.parquet GUNSONU.parquet CIKTI
"""
import sys, os, datetime
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

dk_src, islem_src, gs_src, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
D = pd.read_parquet(dk_src)
gs = pd.read_parquet(gs_src, columns=["trade_date", "instrument_series_code", "market_segment", "previous_last_price",
                                      "corporate_action", "instrument_group"])
gs = gs.rename(columns={"trade_date": "tarih", "instrument_series_code": "islem_kodu"})
gs = gs[gs.instrument_group == "EQT"]
ipf = pq.ParquetFile(islem_src)
iidx = ipf.schema_arrow.get_field_index("tarih")
MUZ = {"P_ESLESTIRME", "P_ESLESTIRMETEKFIYAT", "P_ESLESTIRME_EBDK"}

olay, sapma = [], []
for gun in sorted(D.tarih.unique()):
    d = datetime.date.fromisoformat(gun)
    rgs = [i for i in range(ipf.num_row_groups)
           if ipf.metadata.row_group(i).column(iidx).statistics.min <= d <= ipf.metadata.row_group(i).column(iidx).statistics.max]
    t = ipf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "alis_satis", "islem_fiyati", "islem_zamani", "seans",
                                         "normal_islem", "ortak_sozlesme_no"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["alis_satis"], "A")))
    df = t.to_pandas()
    df = df[df.islem_kodu.str.endswith(".E") & ~df.normal_islem.isin([3, 5])]
    df["zaman"] = pd.to_datetime(gun + " " + df.islem_zamani)
    df = df.sort_values(["islem_kodu", "zaman", "ortak_sozlesme_no"])
    g = gs[gs.tarih == d].set_index("islem_kodu")
    for kod, x in df.groupby("islem_kodu", sort=False):
        if kod not in g.index or g.loc[kod, "previous_last_price"] <= 0 or pd.notna(g.loc[kod, "corporate_action"]):
            continue
        baz = g.loc[kod, "previous_last_price"]
        muz = x.seans.isin(MUZ).to_numpy()
        # her islem icin o anki referans: oncesindeki son muzayede fiyati, yoksa baz
        ref = pd.Series(np.where(muz, x.islem_fiyati, np.nan)).ffill().shift(1).fillna(baz).to_numpy()
        sur = (x.seans == "P_SUREKLI_ISLEM").to_numpy()
        r = x.islem_fiyati.to_numpy()[sur] / ref[sur] - 1
        if len(r):
            sapma.append((gun, kod, g.loc[kod, "market_segment"], float(r.max()), float(r.min())))
        for _, o in D[(D.tarih == gun) & (D.islem_kodu == kod)].iterrows():
            T = pd.Timestamp(o.son_surekli)
            onc = x[x.zaman <= T]
            m = onc[onc.seans.isin(MUZ)]
            rf = m.islem_fiyati.iloc[-1] if len(m) else baz
            s = onc[onc.seans == "P_SUREKLI_ISLEM"]
            son = s.islem_fiyati.iloc[-1] if len(s) else np.nan
            olay.append(dict(tarih=gun, islem_kodu=kod, pazar=g.loc[kod, "market_segment"], T=T, referans=rf,
                             referans_turu="muzayede" if len(m) else "baz", baz=baz, son_surekli_fiyat=son,
                             oran=son / rf - 1 if son == son else np.nan))
    print(gun, len(olay), flush=True)

O = pd.DataFrame(olay)
S = pd.DataFrame(sapma, columns=["tarih", "islem_kodu", "pazar", "en_buyuk_artis", "en_buyuk_dusus"])
O.to_parquet(os.path.join(out, "dk_tetikleme_orani.parquet"))
S.to_parquet(os.path.join(out, "surekli_sapma.parquet"))
O["abs"] = O.oran.abs()
print(O.groupby(["pazar", "referans_turu"]).abs.describe(percentiles=[.05, .25, .5, .75, .95]).round(4).to_string())
print(S.groupby("pazar").agg(n=("en_buyuk_artis", "size"), artis_max=("en_buyuk_artis", "max"),
                             dusus_min=("en_buyuk_dusus", "min")).round(4).to_string())
