"""Emir fiyatlarinin gunluk sinir (baz +-%10, ice yuvarlanmis) disina ciktigi sira-gunler.

Her sira-gun icin yeni emir/degisiklik (sebep 5/6, fiyat > 0) satirlarinin en dusuk ve en yuksek fiyati
sinirla karsilastirilir; sinir disi sira-gunler ozsermaye hali (gun sonu corporate_action) ile birlikte listelenir.
Kullanim: python -I gunici_emir_sinir_disi.py GUNLUK_EMIR_KLASORU GUNSONU.parquet CIKTI.csv
"""
import sys, os, glob, datetime
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import GRUP_TABLO, yukari_adim, asagi_adim

emir_dir, gs_src, out = sys.argv[1:4]
gs = pd.read_parquet(gs_src, columns=["trade_date", "instrument_series_code", "instrument_group", "market_segment",
                                      "previous_last_price", "corporate_action"])
gs = gs[gs.instrument_group == "EQT"]
sonuc = []
for gun in sorted(os.path.basename(p) for p in glob.glob(os.path.join(emir_dir, "20*"))):
    d = datetime.date.fromisoformat(gun)
    g = gs[gs.trade_date == d].set_index("instrument_series_code")
    for f in glob.glob(os.path.join(emir_dir, gun, "pay-*.parquet")):
        t = pq.read_table(f, columns=["islem_kodu", "fiyat", "degisiklik_sebebi"])
        t = t.filter(pc.and_(pc.is_in(t["degisiklik_sebebi"], pa.array([5, 6], pa.int16())), pc.greater(t["fiyat"], 0)))
        a = t.group_by("islem_kodu").aggregate([("fiyat", "min"), ("fiyat", "max"), ([], "count_all")]).to_pandas()
        for _, r in a.iterrows():
            k = str(r.islem_kodu)
            if k not in g.index or not g.loc[k, "previous_last_price"] > 0:
                continue
            b = round(g.loc[k, "previous_last_price"] * 1000)
            tb = GRUP_TABLO["EQT"]
            alt, ust = yukari_adim(b * 0.9, tb) / 1000, asagi_adim(b * 1.1, tb) / 1000
            if r.fiyat_min < alt - 1e-9 or r.fiyat_max > ust + 1e-9:
                sonuc.append(dict(tarih=gun, islem_kodu=k, pazar=g.loc[k, "market_segment"],
                                  ozsermaye=g.loc[k, "corporate_action"], baz=b / 1000, alt=alt, ust=ust,
                                  en_dusuk=r.fiyat_min, en_yuksek=r.fiyat_max))
    print(gun, len(sonuc), flush=True)
R = pd.DataFrame(sonuc)
R.to_csv(out, index=False, encoding="utf-8")
print(R.to_string())
print("ozsermaye hali olmayan sinir disi sira-gun:", int(R.ozsermaye.isna().sum()), "/", len(R))
