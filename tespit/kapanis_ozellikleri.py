"""Kapanis etkilemesi gostergeleri (pay-gun; VI-104.1 md 5/1-d): veriden ve motor ciktisindan ayni tanimlarla.

- kapanis_muzayede_sapma: kapanis muzayedesi fiyati / gunun son surekli islem fiyati - 1 (kapanis muzayedesinde islem
  yoksa NaN). Kapanisi itmenin dogrudan sonucudur.
- kapanis_toplama_dengesizlik: kapanis emir toplamada (P_KAPANIS_EMIR_TPL*) girilen yeni emirlerin alis-satis miktar
  dengesizligi, (A - S) / (A + S).
- kapanis_son_dakika_payi: kapanis emir toplamadaki yeni emir, degisiklik ve iptallerin, emir toplamanin son SON_SN
  saniyesine dusen payi (son an: payin kapanis emir toplamadaki son olayi).
Kapanis muzayedesi islemleri: bolum P_ESLESTIRME ve saat 18:00 sonrasi.

Kullanim (var olan ozellik tablosuna sutun ekler; gun basina ara dosyalar da guncellenir):
  python -I tespit/kapanis_ozellikleri.py GUNLUK_EMIR_KLASORU ISLEM.parquet OZELLIKLER.parquet
"""
import datetime, glob, os, sys

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

KAPANIS_TOPLAMA = ("P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2")
SON_SN = 60
SUTUNLAR = ["kapanis_muzayede_sapma", "kapanis_toplama_dengesizlik", "kapanis_son_dakika_payi"]


def _toplama(d):
    """d: kapanis emir toplama satirlari (islem_kodu, zaman us, sebep, alis bool, miktar). Kod basina iki gosterge."""
    yeni = d[d["sebep"] == 6]
    a = yeni[yeni["alis"]].groupby("islem_kodu")["miktar"].sum()
    s = yeni[~yeni["alis"]].groupby("islem_kodu")["miktar"].sum()
    ev = d[d["sebep"].isin([6, 5, 1])]
    son = ev.groupby("islem_kodu")["zaman"].transform("max")
    out = pd.DataFrame({"a": a, "s": s}).fillna(0)
    out["kapanis_toplama_dengesizlik"] = (out["a"] - out["s"]) / (out["a"] + out["s"]).where(out["a"] + out["s"] > 0)
    gec = (ev["zaman"] >= son - SON_SN * 1_000_000).groupby(ev["islem_kodu"]).mean()
    out = out.join(gec.rename("kapanis_son_dakika_payi"), how="outer")
    return out[["kapanis_toplama_dengesizlik", "kapanis_son_dakika_payi"]]


def veri_kapanis(gunluk, islem_parquet, gun):
    parca = []
    for f in sorted(glob.glob(os.path.join(gunluk, gun, "pay-*.parquet"))):
        t = pq.read_table(f, columns=["islem_kodu", "emir_degistirilme_zamani", "seans", "degisiklik_sebebi", "alis_satis",
                                      "emir_miktari", "emir_kategorisi"])
        t = t.filter(pc.and_(pc.is_in(pc.cast(t["seans"], pa.string()), pa.array(list(KAPANIS_TOPLAMA))),
                             pc.equal(t["emir_kategorisi"], 1)))
        x = t.to_pandas()
        parca.append(pd.DataFrame({"islem_kodu": x["islem_kodu"].astype(str), "zaman": x["emir_degistirilme_zamani"].astype("int64"),
                                   "sebep": x["degisiklik_sebebi"], "alis": x["alis_satis"].astype(str) == "A",
                                   "miktar": x["emir_miktari"]}))
    out = _toplama(pd.concat(parca, ignore_index=True))
    # islemler: kapanis muzayedesi fiyati ve son surekli islem fiyati
    d0 = datetime.date.fromisoformat(gun)
    pf = pq.ParquetFile(islem_parquet)
    ti = pf.schema_arrow.get_field_index("tarih")
    rgs = [i for i in range(pf.num_row_groups)
           if pf.metadata.row_group(i).column(ti).statistics.min <= d0 <= pf.metadata.row_group(i).column(ti).statistics.max]
    t = pf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "alis_satis", "islem_fiyati", "islem_zamani", "seans", "normal_islem"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d0)), pc.equal(t["alis_satis"], "A")))
    x = t.to_pandas()
    x = x[~x["normal_islem"].isin([3, 5])].sort_values("islem_zamani", kind="stable")
    sur = x[x["seans"] == "P_SUREKLI_ISLEM"].groupby("islem_kodu")["islem_fiyati"].last()
    kap = x[(x["seans"] == "P_ESLESTIRME") & (x["islem_zamani"] >= "18:00:00")].groupby("islem_kodu")["islem_fiyati"].last()
    out = out.join((kap / sur - 1).rename("kapanis_muzayede_sapma"), how="outer")
    out.index.name = "islem_kodu"
    return out[SUTUNLAR]


def motor_kapanis(g, df):
    """g: calistirilmis Gun (enjeksiyonlu olabilir); df: veri.pay_gun_emirleri. Donus: dict (SUTUNLAR)."""
    from motor.emir import YeniEmir, Degistir, Iptal
    d = df[df["seans"].isin(KAPANIS_TOPLAMA) & (df["emir_kategorisi"] == 1)]
    x = pd.DataFrame({"islem_kodu": "x", "zaman": d["zaman"].to_numpy(), "sebep": d["degisiklik_sebebi"].to_numpy(),
                      "alis": d["alis"].to_numpy(), "miktar": d["emir_miktari"].to_numpy()})
    ek = [("x", o.zaman, 6 if isinstance(o, YeniEmir) else 5 if isinstance(o, Degistir) else 1,
           bool(getattr(o, "alis", False)), getattr(o, "miktar", 0)) for o, b in g.kabul if b in KAPANIS_TOPLAMA]
    if ek:
        x = pd.concat([x, pd.DataFrame(ek, columns=x.columns)], ignore_index=True)
    out = {c: np.nan for c in SUTUNLAR}
    if len(x):
        t = _toplama(x)
        if "x" in t.index:
            out.update(t.loc["x"].to_dict())
    I = sorted(((b, i) for b, i in g.islemler), key=lambda bi: bi[1].zaman)
    sur = [i.fiyat for b, i in I if b == "P_SUREKLI_ISLEM"]
    gun0 = pd.Timestamp(pd.Timestamp(I[0][1].zaman, unit="us").date()) if I else None
    t18 = int((gun0 + pd.Timedelta(hours=18)).value // 1000) if gun0 is not None else None
    kap = [i.fiyat for b, i in I if b == "P_ESLESTIRME" and i.zaman >= t18] if I else []
    if sur and kap:
        out["kapanis_muzayede_sapma"] = kap[-1] / sur[-1] - 1
    return out


if __name__ == "__main__":
    gunluk, islem_parquet, oz = sys.argv[1:4]
    ara = os.path.splitext(os.path.abspath(oz))[0] + "_gunluk"
    for f in sorted(glob.glob(os.path.join(ara, "20*.parquet"))):
        gun = os.path.basename(f)[:10]
        x = pd.read_parquet(f)
        if all(c in x for c in SUTUNLAR):
            continue
        k = veri_kapanis(gunluk, islem_parquet, gun)
        x = x.drop(columns=[c for c in SUTUNLAR if c in x]).merge(k, left_on="islem_kodu", right_index=True, how="left")
        x.to_parquet(f)
        print(gun, int(x["kapanis_muzayede_sapma"].notna().sum()), flush=True)
    pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(ara, "20*.parquet")))], ignore_index=True).to_parquet(oz)
    print("yazildi", oz)
