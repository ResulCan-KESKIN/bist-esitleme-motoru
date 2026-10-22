"""Gunluk bolumlenmis emir verisinde emir yasam dongusu ve bolum kurallari kontrolleri.

Her emrin satirlari (emir_no, guncelleme_no) sirasina dizilip bir onceki satirla karsilastirilir:
  - degisiklik (5): fiyat iyilesme/kotulesme, emir miktari artis/azalis, emir_giris_zamani degisti mi,
    seans bolumu ve kategori bazinda sayilir (Ek-19 I/J/K/L sutunlari ve oncelik kurallari icin).
  - islem (3): kalan miktar = onceki kalan - eslesen miktar; emir miktari ve giris zamani degismez.
  - guncelleme_no ardisikligi, ilk satirin sebebi, KIE (IMMEDIATE) emirlerin aktif kalma suresi,
    gun sonunda aktif emir kalmamasi.
  - yeni emirler: pazar x bolum x fiyat turu (aciliksta piyasa emri hangi pazarlarda).
  - kapanis seansi (P_KAPANIS_EMIR_TPL*) yeni/degisiklik fiyatlari: son surekli islem fiyatinin +-%3'u
    (ice dogru yuvarlanmis) ve gunluk sinir.
  - kapanis fiyatindan islemler (P_KAPANIS_FIY_ISLEM): yeni emir fiyati = kapanis fiyati.
Kullanim: python -I gunici_emir_kural_kontrol.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet CIKTI [GUN ...]
"""
import sys, os, glob, datetime
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import GRUP_TABLO, yukari_adim, asagi_adim

emir_dir, islem_src, gs_src, out = sys.argv[1:5]
secili = set(sys.argv[5:])
os.makedirs(out, exist_ok=True)
cols = ["islem_kodu", "emir_no", "emir_giris_zamani", "emir_degistirilme_zamani", "alis_satis",
        "emir_fiyat_turu", "emir_turu", "emir_kategorisi", "gecerlilik_turu", "emir_durumu",
        "degisiklik_sebebi", "emir_miktari", "kalan_miktar", "fiyat", "seans", "eslesen_miktar",
        "guncelleme_no"]
gs = pd.read_parquet(gs_src, columns=["trade_date", "instrument_series_code", "instrument_group", "market_segment",
                                      "previous_last_price", "closing_price", "closing_session_price"])
gs = gs.rename(columns={"trade_date": "tarih", "instrument_series_code": "islem_kodu"})
ipf = pq.ParquetFile(islem_src)
iidx = ipf.schema_arrow.get_field_index("tarih")
say = {}


def ekle(tablo, df, keys):
    g = df.groupby(keys, dropna=False, observed=True).size()
    acc = say.setdefault(tablo, (keys, {}))[1]
    for k, v in g.items():
        acc[k] = acc.get(k, 0) + int(v)


def son_surekli(d):
    rgs = [i for i in range(ipf.num_row_groups)
           if ipf.metadata.row_group(i).column(iidx).statistics.min <= d <= ipf.metadata.row_group(i).column(iidx).statistics.max]
    t = ipf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "alis_satis", "islem_fiyati", "islem_zamani",
                                         "seans", "ortak_sozlesme_no"])
    t = t.filter(pc.and_(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["alis_satis"], "A")),
                         pc.equal(t["seans"], "P_SUREKLI_ISLEM")))
    df = t.to_pandas().sort_values(["islem_kodu", "islem_zamani", "ortak_sozlesme_no"])
    return df.groupby("islem_kodu")["islem_fiyati"].last()


gunler = sorted(os.path.basename(p) for p in glob.glob(os.path.join(emir_dir, "20*")))
for gun in gunler:
    if secili and gun not in secili:
        continue
    d = datetime.date.fromisoformat(gun)
    gsd = gs[gs.tarih == d].set_index("islem_kodu")
    son = son_surekli(d)
    for f in sorted(glob.glob(os.path.join(emir_dir, gun, "*.parquet"))):
        t = pq.read_table(f, columns=cols)
        t = t.take(pc.sort_indices(t, sort_keys=[("emir_no", "ascending"), ("guncelleme_no", "ascending")]))
        df = t.to_pandas()
        for c in ["islem_kodu", "seans", "gecerlilik_turu", "alis_satis"]:
            df[c] = df[c].astype(str)
        ayni = np.r_[False, df["emir_no"].to_numpy()[1:] == df["emir_no"].to_numpy()[:-1]]
        onc = df.shift(1)
        grup = os.path.basename(f).split("-")[0]
        df["grup"] = grup
        df["sonek"] = df["islem_kodu"].str.rsplit(".", n=1).str[-1]
        df["pazar"] = df["islem_kodu"].map(gsd["market_segment"]).fillna("?")
        # ilk satir ve ardisiklik
        ilk = ~ayni
        ekle("ilk_satir_sebebi", df[ilk], ["grup", "degisiklik_sebebi", "emir_durumu"])
        ard = ayni & (df["guncelleme_no"].to_numpy() != onc["guncelleme_no"].to_numpy() + 1)
        ekle("guncelleme_no_atlama", df[ayni].assign(atlama=ard[ayni]), ["grup", "atlama"])
        # degisiklikler
        m = ayni & (df["degisiklik_sebebi"] == 5).to_numpy()
        x = df[m].copy()
        o = onc[m]
        alis = x["alis_satis"] == "A"
        dp = x["fiyat"] - o["fiyat"]
        x["fiyat_yon"] = np.select([dp == 0, (dp > 0) == alis], ["ayni", "iyi"], "kotu")
        dq = x["emir_miktari"] - o["emir_miktari"]
        x["miktar_yon"] = np.select([dq == 0, dq > 0], ["ayni", "artis"], "azalis")
        x["giris_degisti"] = (x["emir_giris_zamani"] != o["emir_giris_zamani"]).to_numpy()
        x["giris_eq_deg"] = (x["emir_giris_zamani"] == x["emir_degistirilme_zamani"]).to_numpy()
        x["onceki_seans"] = o["seans"].to_numpy()
        ekle("degisiklik", x, ["grup", "emir_kategorisi", "seans", "fiyat_yon", "miktar_yon", "giris_degisti", "giris_eq_deg"])
        # islemler
        m = ayni & (df["degisiklik_sebebi"] == 3).to_numpy()
        x = df[m]
        o = onc[m]
        x = x.assign(kalan_tutarli=(o["kalan_miktar"] - x["eslesen_miktar"] == x["kalan_miktar"]).to_numpy(),
                     miktar_sabit=(o["emir_miktari"] == x["emir_miktari"]).to_numpy(),
                     giris_sabit=(o["emir_giris_zamani"] == x["emir_giris_zamani"]).to_numpy())
        ekle("islem_satiri", x, ["grup", "seans", "kalan_tutarli", "miktar_sabit", "giris_sabit"])
        # diger sebepler ve durum
        ekle("sebep_seans_durum", df, ["grup", "degisiklik_sebebi", "seans", "emir_durumu"])
        # sistem kaynakli sebepler: onceki satira gore ne degisti
        m = ayni & df["degisiklik_sebebi"].isin([4, 8, 9, 13, 34, 116, 117]).to_numpy()
        x = df[m]
        o = onc[m]
        x = x.assign(onceki_durum=o["emir_durumu"].to_numpy(), onceki_fiyat_turu=o["emir_fiyat_turu"].to_numpy(),
                     onceki_seans=o["seans"].to_numpy(), onceki_sebep=o["degisiklik_sebebi"].to_numpy(),
                     fiyat_degisti=(x["fiyat"] != o["fiyat"]).to_numpy(),
                     kalan_degisti=(x["kalan_miktar"] != o["kalan_miktar"]).to_numpy(),
                     giris_degisti=(x["emir_giris_zamani"] != o["emir_giris_zamani"]).to_numpy(),
                     ayni_an=(x["emir_degistirilme_zamani"] == o["emir_degistirilme_zamani"]).to_numpy())
        ekle("sistem_sebep", x, ["grup", "degisiklik_sebebi", "seans", "onceki_seans", "onceki_sebep", "onceki_durum",
                                 "emir_durumu", "onceki_fiyat_turu", "emir_fiyat_turu", "gecerlilik_turu",
                                 "fiyat_degisti", "kalan_degisti", "giris_degisti", "ayni_an"])
        # KIE: aktif satiri olan IMMEDIATE emirler (bolum bazinda)
        k = df[(df["gecerlilik_turu"] == "IMMEDIATE") & (df["emir_durumu"] == 1)]
        ekle("kie_aktif", k, ["grup", "seans", "degisiklik_sebebi"])
        # gun sonu: emrin son satiri aktif mi
        son_satir = np.r_[df["emir_no"].to_numpy()[1:] != df["emir_no"].to_numpy()[:-1], True]
        z = df[son_satir]
        ekle("emir_son_durum", z, ["grup", "emir_durumu", "degisiklik_sebebi", "seans"])
        # yeni emirler: pazar x bolum x fiyat turu
        y = df[ilk & (df["degisiklik_sebebi"] == 6).to_numpy()]
        ekle("yeni_emir_pazar", y, ["grup", "sonek", "pazar", "seans", "emir_fiyat_turu", "gecerlilik_turu", "emir_kategorisi"])
        # kapanis seansi +-%3 ve KFI fiyati
        kap = df[df["seans"].isin(["P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2"]) & df["degisiklik_sebebi"].isin([5, 6])
                 & (df["fiyat"] > 0)].copy()
        if len(kap):
            kap["son"] = kap["islem_kodu"].map(son)
            kap["igrup"] = kap["islem_kodu"].map(gsd["instrument_group"])
            kap["baz"] = kap["islem_kodu"].map(gsd["previous_last_price"])
            sonuc = []
            for (kod, sp, ig, bz), g in kap.groupby(["islem_kodu", "son", "igrup", "baz"], dropna=False):
                tb = GRUP_TABLO.get(ig)
                p = np.rint(g["fiyat"].to_numpy() * 1000).astype(np.int64)
                if tb is None:
                    continue
                if sp == sp:
                    s = int(round(sp * 1000))
                    alt, ust = yukari_adim(s * 0.97, tb), asagi_adim(s * 1.03, tb)
                    durum = np.where((p >= alt) & (p <= ust), "icinde", "disinda")
                    ref = "son_islem"
                else:
                    durum = np.full(len(p), "son_islem_yok")
                    ref = "yok"
                if bz == bz and bz > 0:
                    b = int(round(bz * 1000))
                    gun_ici = (p >= yukari_adim(b * 0.9, tb)) & (p <= asagi_adim(b * 1.1, tb))
                else:
                    gun_ici = np.ones(len(p), bool)
                sonuc.append(pd.DataFrame({"sonek": g["sonek"].to_numpy(), "seans": g["seans"].to_numpy(),
                                           "sebep": g["degisiklik_sebebi"].to_numpy(), "ref": ref,
                                           "durum": durum, "gunluk_sinir_icinde": gun_ici}))
            if sonuc:
                ekle("kapanis_yuzde3", pd.concat(sonuc), ["sonek", "seans", "sebep", "ref", "durum", "gunluk_sinir_icinde"])
        kfi = df[(df["seans"] == "P_KAPANIS_FIY_ISLEM") & df["degisiklik_sebebi"].isin([5, 6]) & (df["fiyat"] > 0)].copy()
        if len(kfi):
            kfi["kapanis"] = kfi["islem_kodu"].map(gsd["closing_price"])
            kfi["esit"] = np.isclose(kfi["fiyat"], kfi["kapanis"])
            ekle("kfi_fiyat", kfi, ["sonek", "degisiklik_sebebi", "esit"])
        print(gun, os.path.basename(f), len(df), flush=True)

for ad, (keys, acc) in say.items():
    s = pd.Series(acc)
    s.index = pd.MultiIndex.from_tuples([k if isinstance(k, tuple) else (k,) for k in s.index], names=keys)
    s.rename("adet").reset_index().to_csv(os.path.join(out, ad + ".csv"), index=False, encoding="utf-8")
print("bitti")
