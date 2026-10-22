"""Pay-gun ozellikleri (TASARIM.md 6.1-6.2): DataStore gun ici emir, gun ici islem ve gun sonu dosyalarindan.

Birim: pay-gun (.E siralari, pay pazarlari). Gruplar ve VI-104.1 md 5/1 bentleriyle iliskisi:
- Emir akisi (bent a, b): yeni / degisiklik / iptal sayilari ve oranlari, emir/islem orani; piyasa emri, KIE,
  aciga satis ve AFK paylari; yeni limit emirlerdeki farkli fiyat kademesi sayisi; acilis emir toplamada (09:40-09:50)
  iptal orani; kapanis emir toplamada degisiklik ve iptal yogunlugu.
- Islem (bent d, f): getiri, gun ici aralik, aktif taraf dengesizligi, kucuk islem payi (1.000 TL alti), kapanis
  seansi ve kapanis fiyatindan islemlerin hacim payi, kapanis fiyatinin AOF'den sapmasi, acilis seansi fiyatinin
  baz fiyattan sapmasi, kapanis oncesi (17:45 sonrasi surekli islem) getiri.
- Referans: pazar, BIST 100 uyeligi, piyasa yapici, brut takas, ozsermaye hali (model girdisi degil, ayirt etme ve
  aciklama icin; brut takas bir tedbirdir, etiketle sizinti yaratabilir).
Aktor gerektiren bentler (c yon degistiren emir, c kendinden kendine islem) gercek veride olculemez (uye/hesap yok).

Kullanim: python -I tespit/ozellikler.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet CIKTI.parquet [GUN ...]
          (gun verilmezse klasordeki butun gunler)
"""
import datetime, glob, os, sys, time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

PAY_PAZARLARI = ("Z", "N", "T", "W", "S")
ACILIS_TOPLAMA = ("P_ACILIS_EMIR_TPL", "P_ACS_EMR_TP2_PY")          # 09:40-09:50 (son 5 dk haric)
KAPANIS_TOPLAMA = ("P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2")
KUCUK_ISLEM_TL = 1000
EMIR_SUTUN = ["islem_kodu", "emir_degistirilme_zamani", "emir_fiyat_turu", "emir_turu", "emir_kategorisi",
              "gecerlilik_turu", "degisiklik_sebebi", "seans", "fiyat", "afk"]


def emir_ozellikleri(gunluk, gun):
    parcalar = []
    for f in sorted(glob.glob(os.path.join(gunluk, gun, "pay-*.parquet"))):
        t = pq.read_table(f, columns=EMIR_SUTUN)
        t = t.filter(pc.and_(pc.equal(t["emir_kategorisi"], 1),
                             pc.ends_with(pc.cast(t["islem_kodu"], pa.string()), ".E")))
        d = t.to_pandas()
        for c in ("islem_kodu", "gecerlilik_turu", "seans", "afk"):
            d[c] = d[c].astype(str)
        seb = d["degisiklik_sebebi"]
        yeni = seb == 6
        lim = yeni & (d["emir_fiyat_turu"] == 1)
        acl = d["seans"].isin(ACILIS_TOPLAMA)
        kap = d["seans"].isin(KAPANIS_TOPLAMA)
        x = pd.DataFrame({
            "islem_kodu": d["islem_kodu"],
            "yeni": yeni, "degisiklik": seb == 5, "iptal": seb == 1,
            "piyasa": yeni & d["emir_fiyat_turu"].isin([2, 3]), "kie": yeni & (d["gecerlilik_turu"] == "IMMEDIATE"),
            "aciga": yeni & ((d["emir_turu"] & 2) != 0), "afk": yeni & (d["afk"] == "E"),
            "acilis_yeni": yeni & acl, "acilis_iptal": (seb == 1) & acl,
            "kapanis_yeni": yeni & kap, "kapanis_degisiklik": seb.isin([1, 5]) & kap,
        })
        g = x.groupby("islem_kodu").sum()
        g["fiyat_kademesi"] = d[lim].groupby("islem_kodu")["fiyat"].nunique()
        parcalar.append(g)
    e = pd.concat(parcalar).groupby(level=0).sum()
    y = e["yeni"].clip(lower=1)
    out = pd.DataFrame({
        "emir_yeni": e["yeni"], "emir_degisiklik": e["degisiklik"], "emir_iptal": e["iptal"],
        "iptal_orani": e["iptal"] / y, "degisiklik_orani": e["degisiklik"] / y,
        "piyasa_payi": e["piyasa"] / y, "kie_payi": e["kie"] / y, "aciga_payi": e["aciga"] / y, "afk_payi": e["afk"] / y,
        "fiyat_kademesi": e["fiyat_kademesi"].fillna(0),
        "acilis_iptal_orani": e["acilis_iptal"] / e["acilis_yeni"].clip(lower=1),
        "kapanis_degisiklik_yogunlugu": e["kapanis_degisiklik"] / e["kapanis_yeni"].clip(lower=1),
    })
    out.index.name = "islem_kodu"
    return out


def islem_ozellikleri(islem_parquet, gun):
    d0 = datetime.date.fromisoformat(gun)
    f = pq.ParquetFile(islem_parquet)
    ti = f.schema_arrow.get_field_index("tarih")
    rgs = [i for i in range(f.num_row_groups)
           if f.metadata.row_group(i).column(ti).statistics.min <= d0 <= f.metadata.row_group(i).column(ti).statistics.max]
    t = f.read_row_groups(rgs, columns=["tarih", "islem_kodu", "alis_satis", "islem_adedi", "islem_fiyati", "islem_hacmi",
                                         "islem_zamani", "normal_islem", "seans", "aktif_pasif"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d0)), pc.ends_with(t["islem_kodu"], ".E")))
    d = t.to_pandas()
    d = d[~d["normal_islem"].isin([3, 5])]
    s = d[d["seans"] == "P_SUREKLI_ISLEM"]
    aa = s[(s["alis_satis"] == "A") & (s["aktif_pasif"] == "A")].groupby("islem_kodu")["islem_adedi"].sum()
    asat = s[(s["alis_satis"] == "S") & (s["aktif_pasif"] == "A")].groupby("islem_kodu")["islem_adedi"].sum()
    a = d[d["alis_satis"] == "A"]
    sa = s[s["alis_satis"] == "A"]
    n = a.groupby("islem_kodu").size()
    kucuk = sa[sa["islem_hacmi"] < KUCUK_ISLEM_TL].groupby("islem_kodu").size()
    son = sa.sort_values("islem_zamani").groupby("islem_kodu")["islem_fiyati"].last()
    o1745 = sa[sa["islem_zamani"] < "17:45:00"].sort_values("islem_zamani").groupby("islem_kodu")["islem_fiyati"].last()
    out = pd.DataFrame({"islem_sayisi": n})
    out["aktif_dengesizlik"] = ((aa.reindex(out.index).fillna(0) - asat.reindex(out.index).fillna(0))
                                / (aa.reindex(out.index).fillna(0) + asat.reindex(out.index).fillna(0)).clip(lower=1))
    out["kucuk_islem_payi"] = kucuk.reindex(out.index).fillna(0) / sa.groupby("islem_kodu").size().reindex(out.index).clip(lower=1)
    out["kapanis_oncesi_getiri"] = (son / o1745 - 1).reindex(out.index)
    out.index.name = "islem_kodu"
    return out


def gunsonu_ozellikleri(gunsonu, gun):
    t = pq.read_table(gunsonu, filters=[("trade_date", "=", datetime.date.fromisoformat(gun))]).to_pandas()
    t = t[t["instrument_series_code"].str.endswith(".E") & t["market_segment"].isin(PAY_PAZARLARI)]
    b = t["previous_last_price"].where(t["previous_last_price"] > 0)
    hac = t["total_traded_volume"].where(t["total_traded_volume"] > 0)
    out = pd.DataFrame({
        "islem_kodu": t["instrument_series_code"],
        "pazar": t["market_segment"], "bist100": t["bist_100_index"], "piyasa_yapici": t["market_maker"],
        "brut_takas": t["gross_settlement"], "ozsermaye": t["corporate_action"],
        "baz": b, "kapanis": t["closing_price"],
        "getiri": t["closing_price"] / b - 1,
        "aralik": (t["highest_price"] - t["lowest_price"]) / b,
        "hacim_tl": t["total_traded_value"],
        "kapanis_aof_sapma": t["closing_price"] / t["vwap"].where(t["vwap"] > 0) - 1,
        "acilis_sapma": t["opening_session_price"].where(t["opening_session_price"] > 0) / b - 1,
        "kapanis_seansi_payi": t["traded_volume_at_closing_session"] / hac,
        "kfi_payi": t["traded_volume_of_trades_at_closing_price"] / hac,
    }).set_index("islem_kodu")
    return out


def gun_ozellikleri(gunluk, islem_parquet, gunsonu, gun):
    gs = gunsonu_ozellikleri(gunsonu, gun)
    x = gs.join(emir_ozellikleri(gunluk, gun), how="left").join(islem_ozellikleri(islem_parquet, gun), how="left")
    x["emir_islem_orani"] = x["emir_yeni"] / x["islem_sayisi"].fillna(0).clip(lower=1)
    x.insert(0, "tarih", pd.Timestamp(gun))
    return x.reset_index()


if __name__ == "__main__":
    gunluk, islem_parquet, gunsonu, cikti = sys.argv[1:5]
    gunler = sys.argv[5:] or sorted(os.path.basename(p) for p in glob.glob(os.path.join(gunluk, "20*")))
    parcalar = []
    for gun in gunler:
        t0 = time.time()
        parcalar.append(gun_ozellikleri(gunluk, islem_parquet, gunsonu, gun))
        print(gun, len(parcalar[-1]), f"{time.time() - t0:.0f} sn", flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    pd.concat(parcalar, ignore_index=True).to_parquet(cikti)
    print("yazildi", cikti)
