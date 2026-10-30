"""Yaniltici emir yerlesimi olcumu: surekli islemde girilen yeni limit emirlerin ayni taraftaki en iyi fiyata uzakligi
(fiyat adimi cinsinden) ve 60 sn icinde islem gormeden iptal edilip edilmedigi (kisa omurlu; ozellikler.uzak_kisa_omurlu
ile ayni tanim).

Gruplar:
- ALKLC_donem: ALKLC.E, 03.03-18.03.2025 (SPK donemi 04.02-18.03.2025, A seviyesi)
- ALKLC_sonra: ALKLC.E, 19.03-30.06.2025
- piyasa: Mart 2025, diger .E paylar (SPK etiketli pay-gunler haric)
Buyuk emir: pay-gunun yeni limit emirlerinin en buyuk %1'i. Ayrica pay-gun basina en buyuk emrin gunluk islem
miktarina (gun sonu total_traded_volume) orani (senaryodaki katman buyuklugu H x %2 ile karsilastirma).
Kullanim: python -I yaniltici_yerlesim.py KOK CIKTI_KLASORU [--deneme]"""
import glob, os, sys, time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

KOK, OUT = sys.argv[1], sys.argv[2]
DENEME = "--deneme" in sys.argv
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "tespit"))
from ozellikler import fiyat_adimi
import yontemler as y

sys.stdout.reconfigure(encoding="utf-8")
GUNLUK = os.path.join(KOK, "veri", "gun-ici-emir", "gunluk")
SUTUN = ["islem_kodu", "emir_no", "emir_degistirilme_zamani", "alis_satis", "emir_fiyat_turu", "emir_kategorisi",
         "degisiklik_sebebi", "emir_miktari", "fiyat", "seans", "en_iyi_alis_fiyati", "en_iyi_satis_fiyati"]
KISA_US = 60 * 1_000_000
BUYUK_YUZDELIK = 0.99   # buyuk emir: pay-gunun yeni limit emirlerinin en buyuk %1'i
KOVA = 7          # 7 = "7+"
ALKLC = "ALKLC.E"
DONEM_BIT = "2025-03-18"
os.makedirs(OUT, exist_ok=True)
_e = y.etiketler(os.path.join(KOK, "veri", "etiketler", "vaka_pencere_dogrulama.csv"))
etiketli = set(zip(_e["islem_kodu"], _e["tarih"].astype(str).str[:10]))


def gunluk_hacim(gun):
    f = os.path.join(KOK, "veri", "gun-sonu-fiyat-hacim", f"PP_GUNSONUFIYATHACIM.M.{gun[:4]}{gun[5:7]}.parquet")
    import datetime
    t = pq.read_table(f, columns=["trade_date", "instrument_series_code", "total_traded_volume"],
                      filters=[("trade_date", "=", datetime.date.fromisoformat(gun))]).to_pandas()
    return t.set_index("instrument_series_code")["total_traded_volume"]


def emir_tablosu(d, gun, H):
    """Yeni limit emir basina: kod, uzaklik kovasi, miktar, kisa omurlu mu, buyuk mu."""
    d = d.sort_values(["islem_kodu", "emir_degistirilme_zamani"], kind="stable")
    z = d["emir_degistirilme_zamani"].astype("int64")
    seb = d["degisiklik_sebebi"]
    gir = d[(seb == 6) & (d["seans"] == "P_SUREKLI_ISLEM") & (d["emir_fiyat_turu"] == 1)
            & (d["en_iyi_alis_fiyati"] > 0) & (d["en_iyi_satis_fiyati"] > 0)]
    if gir.empty:
        return None
    alis = (gir["alis_satis"] == "A").to_numpy()
    en_iyi = np.where(alis, gir["en_iyi_alis_fiyati"], gir["en_iyi_satis_fiyati"])
    mesafe = np.where(alis, en_iyi - gir["fiyat"], gir["fiyat"] - en_iyi) / fiyat_adimi(en_iyi)
    anahtar = d["islem_kodu"] + "|" + d["emir_no"].astype(str)
    ga = anahtar[gir.index]
    iptal = z[seb == 1].groupby(anahtar[seb == 1]).min()
    dolu = set(anahtar[seb.isin([3, 13])])
    omur = iptal.reindex(ga).to_numpy() - z[gir.index].to_numpy()
    q = gir["emir_miktari"].astype(float)
    esik = q.groupby(gir["islem_kodu"]).transform(lambda s: s.quantile(BUYUK_YUZDELIK))
    return pd.DataFrame({
        "tarih": gun, "islem_kodu": gir["islem_kodu"].to_numpy(),
        "kova": np.clip(np.rint(mesafe), 0, KOVA).astype(int),
        "miktar": q.to_numpy(),
        "kisa": (omur <= KISA_US) & ~ga.isin(dolu).to_numpy(),
        "buyuk": (q >= esik).to_numpy(),
        "H": H.reindex(gir["islem_kodu"]).to_numpy().astype(float),
    })


def oku(f, filtre):
    t = pq.read_table(f, columns=SUTUN)
    t = t.filter(pc.and_(pc.equal(t["emir_kategorisi"], 1), filtre(pc.cast(t["islem_kodu"], pa.string()))))
    d = t.to_pandas()
    for c in ("islem_kodu", "seans", "alis_satis"):
        d[c] = d[c].astype(str)
    return d


gunler = sorted(os.listdir(GUNLUK))
mart = [g for g in gunler if g.startswith("2025-03")]
if DENEME:
    mart, gunler = mart[5:6], ["2025-03-10", "2025-03-20"]

# 1) ALKLC: butun gunler, emir duzeyinde
t0, parca = time.time(), []
for gun in gunler:
    H = gunluk_hacim(gun)
    for f in sorted(glob.glob(os.path.join(GUNLUK, gun, "pay-*.parquet"))):
        d = oku(f, lambda k: pc.equal(k, ALKLC))
        if len(d):
            e = emir_tablosu(d, gun, H)
            if e is not None:
                parca.append(e)
A = pd.concat(parca, ignore_index=True)
A["grup"] = np.where(A["tarih"] <= DONEM_BIT, "ALKLC_donem", "ALKLC_sonra")
A.to_parquet(os.path.join(OUT, "alklc_emirler.parquet"))
print(f"ALKLC: {len(A)} yeni limit emir, {A['tarih'].nunique()} gun, {time.time() - t0:.0f} sn", flush=True)

# 2) Piyasa: Mart, diger .E paylar, kovalara toplanmis
ozet, boyut = [], []
for gun in mart:
    H = gunluk_hacim(gun)
    for f in sorted(glob.glob(os.path.join(GUNLUK, gun, "pay-*.parquet"))):
        d = oku(f, lambda k: pc.and_(pc.ends_with(k, ".E"), pc.not_equal(k, ALKLC)))
        if not len(d):
            continue
        e = emir_tablosu(d, gun, H)
        if e is None:
            continue
        e = e[[(k, gun) not in etiketli for k in e["islem_kodu"]]]
        b = e.groupby("islem_kodu").agg(en_buyuk=("miktar", "max"), H=("H", "first"), yeni=("miktar", "size"))
        boyut.append(b.assign(tarih=gun))
        ozet.append(e.groupby(["kova", "kisa", "buyuk"]).agg(adet=("miktar", "size"), miktar=("miktar", "sum")).reset_index())
    print(gun, f"{time.time() - t0:.0f} sn", flush=True)
P = pd.concat(ozet).groupby(["kova", "kisa", "buyuk"], as_index=False).sum()
P["grup"] = "piyasa"
P.to_parquet(os.path.join(OUT, "piyasa_ozet.parquet"))
B = pd.concat(boyut).reset_index()
B.to_parquet(os.path.join(OUT, "pay_gun_boyut.parquet"))

# 3) Tablolar
Aoz = A.groupby(["grup", "kova", "kisa", "buyuk"]).agg(adet=("miktar", "size"), miktar=("miktar", "sum")).reset_index()
T = pd.concat([Aoz, P], ignore_index=True)
T.to_csv(os.path.join(OUT, "kova_ozet.csv"), index=False, encoding="utf-8")
ad = {k: str(k) for k in range(KOVA)} | {KOVA: f"{KOVA}+"}


def dagilim(x, deger="miktar"):
    s = x.groupby(["grup", "kova"])[deger].sum().unstack(fill_value=0)
    return (s.div(s.sum(axis=1), axis=0) * 100).rename(columns=ad).round(1)


print("\nA) Kisa omurlu (60 sn icinde islem gormeden iptal) BUYUK emirlerin uzaklik dagilimi, miktar payi %:")
print(dagilim(T[T["kisa"] & T["buyuk"]]).to_string())
print("\n   adet:", T[T["kisa"] & T["buyuk"]].groupby("grup")["adet"].sum().to_dict())
print("\nB) Kisa omurlu butun emirlerin uzaklik dagilimi, miktar payi %:")
print(dagilim(T[T["kisa"]]).to_string())
print("\nC) Butun yeni limit emirlerin uzaklik dagilimi (yerlesim tabani), miktar payi %:")
print(dagilim(T).to_string())
print("\nD) Her kovada girilen miktarin ne kadari 60 sn icinde islem gormeden iptal ediliyor, %:")
s = T.groupby(["grup", "kova"]).apply(lambda g: 100 * g.loc[g["kisa"], "miktar"].sum() / g["miktar"].sum())
print(s.unstack().rename(columns=ad).round(1).to_string())
print("\nE) Gunluk toplam yeni limit miktarina gore kisa omurlu buyuk emir payi, %:")
G = A.groupby("tarih").apply(lambda g: pd.Series({
    "0-2 kademe": 100 * g.loc[g["kisa"] & g["buyuk"] & (g["kova"] <= 2), "miktar"].sum() / g["miktar"].sum(),
    "3+ kademe": 100 * g.loc[g["kisa"] & g["buyuk"] & (g["kova"] >= 3), "miktar"].sum() / g["miktar"].sum(),
    "yeni_emir": len(g)}))
G["grup"] = np.where(G.index <= DONEM_BIT, "donem", "sonra")
G.to_csv(os.path.join(OUT, "alklc_gunluk.csv"), encoding="utf-8")
print(G.groupby("grup")[["0-2 kademe", "3+ kademe"]].agg(["mean", "median", "max"]).round(2).to_string())
print("\nDonem gunleri:")
print(G[G["grup"] == "donem"].round(2).to_string())
print("\nF) Piyasa (Mart, en az 300 yeni limit emirli pay-gunler): en buyuk tek emrin gunluk islem miktarina orani, %:")
b = B[(B["yeni"] >= 300) & (B["H"] > 0)]
r = 100 * b["en_buyuk"] / b["H"]
print(r.describe(percentiles=[.25, .5, .75, .9]).round(2).to_string())
print(f"en buyuk emri gunluk hacmin %2'sini asan pay-gun orani: %{100 * (r >= 2).mean():.1f} (n = {len(r)})")
