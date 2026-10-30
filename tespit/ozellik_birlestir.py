"""Aylik pay-gun ozellik dosyalarini (ozellikler.py) tek dosyada birlestirir; cok ayli degerlendirmelerin girdisi
(degerlendir.py, sentetik_degerlendir.py, pencere_degerlendir.py, spk_pencere.py).

ozsermaye sutunu gun sonu dosyalarindan yeniden okunur: 27.10.2026'dan once uretilen ozellik dosyalarinda sayidir
(3.0), gun sonu sabit semaya gecince metindir ("03"); aylar ancak ayni turle birlestirilebilir.
Kullanim: python -I tespit/ozellik_birlestir.py CIKTI.parquet OZELLIKLER.parquet [OZELLIKLER.parquet ...]
"""
import os, sys

import pandas as pd
import pyarrow.parquet as pq

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    cikti, girdiler = sys.argv[1], sys.argv[2:]
    T = pd.concat([pd.read_parquet(f) for f in girdiler], ignore_index=True)
    assert not T.duplicated(["tarih", "islem_kodu"]).any(), "ayni pay-gun birden cok dosyada"
    G = pd.concat([pq.read_table(os.path.join(KOK, "veri", "gun-sonu-fiyat-hacim", f"PP_GUNSONUFIYATHACIM.M.{ay}.parquet"),
                                 columns=["trade_date", "instrument_series_code", "corporate_action"]).to_pandas()
                   for ay in sorted(T["tarih"].dt.strftime("%Y%m").unique())])
    oz = G.set_index([pd.to_datetime(G["trade_date"]), "instrument_series_code"])["corporate_action"]
    once = int(T["ozsermaye"].notna().sum())
    T["ozsermaye"] = oz.reindex(pd.MultiIndex.from_arrays([T["tarih"], T["islem_kodu"]])).to_numpy()
    assert int(T["ozsermaye"].notna().sum()) == once, (once, int(T["ozsermaye"].notna().sum()))
    T = T.sort_values(["tarih", "islem_kodu"]).reset_index(drop=True)
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    T.to_parquet(cikti)
    print("yazildi", cikti, len(T), "pay-gun,", T["tarih"].nunique(), "gun,", f"{T['tarih'].min():%Y-%m-%d}..{T['tarih'].max():%Y-%m-%d}")
