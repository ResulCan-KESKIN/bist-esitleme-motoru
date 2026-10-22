"""Pay-gun ozellikleri (TASARIM.md 6.1-6.2): DataStore gun ici emir, gun ici islem ve gun sonu dosyalarindan.

Birim: pay-gun (.E siralari, pay pazarlari). Gruplar ve VI-104.1 md 5/1 bentleriyle iliskisi:
- Emir akisi (bent a, b): yeni / degisiklik / iptal sayilari ve oranlari, emir/islem orani; piyasa emri, KIE,
  aciga satis ve AFK paylari; yeni limit emirlerdeki farkli fiyat kademesi sayisi; acilis emir toplamada (09:40-09:50)
  iptal orani; kapanis emir toplamada degisiklik ve iptal yogunlugu; kisa omurlu uzak emir payi (surekli islemde ayni
  taraftaki en iyi fiyattan en az UZAK_ADIM adim uzakta girilip KISA_SN icinde islem gormeden iptal edilen emirlerin
  miktar payi; yaniltici emir gostergesi).
- Defter (veride olay anindaki en iyi alis / satis fiyatindan): surekli islemde goreli makasin ortancasi.
- Islem (bent d, f): getiri, gun ici aralik, aktif taraf dengesizligi, kucuk islem payi (1.000 TL alti), kapanis
  seansi ve kapanis fiyatindan islemlerin hacim payi, kapanis fiyatinin AOF'den sapmasi, acilis seansi fiyatinin
  baz fiyattan sapmasi, kapanis oncesi (17:45 sonrasi surekli islem) getiri.
- Referans: pazar, BIST 100 uyeligi, piyasa yapici, brut takas, ozsermaye hali (model girdisi degil, ayirt etme ve
  aciklama icin; brut takas bir tedbirdir, etiketle sizinti yaratabilir).
Aktor gerektiren bentler (c yon degistiren emir, c kendinden kendine islem) gercek veride olculemez (uye/hesap yok).

Kullanim: python -I tespit/ozellikler.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet CIKTI.parquet [GUN ...]
          (gun verilmezse klasordeki butun gunler; gun basina ara dosyalar CIKTI_gunluk/ altinda, var olan gun atlanir;
          CIKTI o ana kadar hesaplanan butun gunlerin birlesimidir)
"""
import datetime, glob, os, sys, time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veri", "araclar"))

PAY_PAZARLARI = ("Z", "N", "T", "W", "S")
ACILIS_TOPLAMA = ("P_ACILIS_EMIR_TPL", "P_ACS_EMR_TP2_PY")          # 09:40-09:50 (son 5 dk haric)
KAPANIS_TOPLAMA = ("P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2")
KUCUK_ISLEM_TL = 1000
UZAK_ADIM, KISA_SN = 3, 60
EMIR_SUTUN = ["islem_kodu", "emir_no", "emir_degistirilme_zamani", "emir_fiyat_turu", "emir_turu", "emir_kategorisi",
              "gecerlilik_turu", "degisiklik_sebebi", "seans", "fiyat", "afk", "alis_satis", "emir_miktari",
              "en_iyi_alis_fiyati", "en_iyi_satis_fiyati"]


def fiyat_adimi(fiyat_tl):
    """Pay fiyat adimi (TL), Tablo-7 (tek_fiyat_algoritma.TABLO7)."""
    from tek_fiyat_algoritma import TABLO7
    bas, ad = TABLO7
    m = np.rint(np.asarray(fiyat_tl, dtype=float) * 1000).astype(np.int64)
    return ad[np.clip(np.searchsorted(bas, m, side="right") - 1, 0, len(ad) - 1)] / 1000


def uzak_kisa_omurlu(d):
    """Kod basina (pay, payda): kisa omurlu uzak emir miktari ve surekli islemde yeni limit emir miktari."""
    z = d["emir_degistirilme_zamani"].astype("int64")
    seb = d["degisiklik_sebebi"]
    gir = d[(seb == 6) & (d["seans"] == "P_SUREKLI_ISLEM") & (d["emir_fiyat_turu"] == 1)
            & (d["en_iyi_alis_fiyati"] > 0) & (d["en_iyi_satis_fiyati"] > 0)]
    if gir.empty:
        return pd.DataFrame(columns=["uzak_kisa", "surekli_yeni_miktar"])
    alis = gir["alis_satis"] == "A"
    en_iyi = np.where(alis, gir["en_iyi_alis_fiyati"], gir["en_iyi_satis_fiyati"])
    mesafe = np.where(alis, en_iyi - gir["fiyat"], gir["fiyat"] - en_iyi) / fiyat_adimi(en_iyi)
    iptal = z[seb == 1].groupby(d.loc[seb == 1, "emir_no"]).min()
    dolu = set(d.loc[seb.isin([3, 13]), "emir_no"])
    omur = iptal.reindex(gir["emir_no"]).to_numpy() - z[gir.index].to_numpy()
    kisa = (omur <= KISA_SN * 1_000_000) & ~gir["emir_no"].isin(dolu).to_numpy()
    q = gir["emir_miktari"].to_numpy()
    x = pd.DataFrame({"islem_kodu": gir["islem_kodu"].to_numpy(), "uzak_kisa": np.where((mesafe >= UZAK_ADIM - 1e-9) & kisa, q, 0),
                      "surekli_yeni_miktar": q})
    return x.groupby("islem_kodu").sum()


def makas(d):
    s = d[(d["seans"] == "P_SUREKLI_ISLEM") & (d["en_iyi_alis_fiyati"] > 0) & (d["en_iyi_satis_fiyati"] > 0)]
    m = (s["en_iyi_satis_fiyati"] - s["en_iyi_alis_fiyati"]) / ((s["en_iyi_satis_fiyati"] + s["en_iyi_alis_fiyati"]) / 2)
    return m.groupby(s["islem_kodu"]).median()


def emir_ozellikleri(gunluk, gun):
    parcalar = []
    for f in sorted(glob.glob(os.path.join(gunluk, gun, "pay-*.parquet"))):
        t = pq.read_table(f, columns=EMIR_SUTUN)
        t = t.filter(pc.and_(pc.equal(t["emir_kategorisi"], 1),
                             pc.ends_with(pc.cast(t["islem_kodu"], pa.string()), ".E")))
        d = t.to_pandas()
        for c in ("islem_kodu", "gecerlilik_turu", "seans", "afk", "alis_satis"):
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
        g = g.join(uzak_kisa_omurlu(d), how="left")
        g["makas"] = makas(d)
        parcalar.append(g)
    e = pd.concat(parcalar).groupby(level=0).sum(min_count=1)
    y = e["yeni"].clip(lower=1)
    out = pd.DataFrame({
        "emir_yeni": e["yeni"], "emir_degisiklik": e["degisiklik"], "emir_iptal": e["iptal"],
        "iptal_orani": e["iptal"] / y, "degisiklik_orani": e["degisiklik"] / y,
        "piyasa_payi": e["piyasa"] / y, "kie_payi": e["kie"] / y, "aciga_payi": e["aciga"] / y, "afk_payi": e["afk"] / y,
        "fiyat_kademesi": e["fiyat_kademesi"].fillna(0),
        "acilis_iptal_orani": e["acilis_iptal"] / e["acilis_yeni"].clip(lower=1),
        "kapanis_degisiklik_yogunlugu": e["kapanis_degisiklik"] / e["kapanis_yeni"].clip(lower=1),
        "kisa_omurlu_uzak_pay": e["uzak_kisa"] / e["surekli_yeni_miktar"].where(e["surekli_yeni_miktar"] > 0),
        "makas": e["makas"],
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
    # gun basina ara dosya (kaldigi yerden devam): CIKTI'nin yanindaki <ad>_gunluk/ klasoru
    ara = os.path.splitext(os.path.abspath(cikti))[0] + "_gunluk"
    os.makedirs(ara, exist_ok=True)
    for gun in gunler:
        f = os.path.join(ara, gun + ".parquet")
        if os.path.exists(f):
            continue
        t0 = time.time()
        x = gun_ozellikleri(gunluk, islem_parquet, gunsonu, gun)
        x.to_parquet(f)
        print(gun, len(x), f"{time.time() - t0:.0f} sn", flush=True)
    tum = sorted(glob.glob(os.path.join(ara, "20*.parquet")))
    pd.concat([pd.read_parquet(f) for f in tum], ignore_index=True).to_parquet(cikti)
    print("yazildi", cikti, len(tum), "gun")
