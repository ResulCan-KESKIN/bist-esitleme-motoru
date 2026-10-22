"""Gun ici emir ve islem fiyatlarinin fiyat adimi (Tablo-7/Tablo-8) ve fiyat sinirlarina uygunlugu.

Girdi: gunluk bolumlenmis emir klasoru (gunici_emir_gunluk_bol.py ciktisi), aylik islem ve gun sonu parquet.
Yalniz uyenin belirledigi fiyatlar sinanir: yeni emir (6) ve degisiklik (5) satirlari, fiyat > 0.
Baz fiyat: gun sonu previous_last_price. Marj adaylari 0,10/0,15/0,20; sinirlar ice dogru yuvarlanir
(alt sinir yukari, ust sinir asagi adima; 02-fiyat.md madde 37).
Kullanim: python -I gunici_fiyat_adimi_sinir_kontrol.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet CIKTI
"""
import sys, os, glob, datetime
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

emir_dir, islem_src, gs_src, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)

# milli-TL; bant alt siniri dahil
TABLO7 = (np.array([0, 20000, 50000, 100000, 250000, 500000, 1000000, 2500000]),
          np.array([10, 20, 50, 100, 250, 500, 1000, 2500]))
TABLO8 = (np.array([0, 50000, 100000, 250000, 500000, 1000000, 2500000]),
          np.array([10, 20, 50, 100, 250, 500, 1000]))
TEK = (np.array([0]), np.array([10]))
GRUP_TABLO = {"EQT": TABLO7, "RGT": TABLO7, "ETF": TABLO8, "GMF": TABLO8, "GSF": TABLO8,
              "ECW": TEK, "EPW": TEK, "XCR": TEK, "EMS": TEK, "AOF": TEK}
SINIRLI = ["EQT", "ETF", "GMF", "GSF", "RGT", "EMS"]
MARJ = [0.10, 0.15, 0.20]

gs = pq.read_table(gs_src, columns=["trade_date", "instrument_series_code", "instrument_group",
                                    "market_segment", "previous_last_price"])
gs = gs.rename_columns(["tarih", "islem_kodu", "grup", "pazar", "baz"])


def adim_kod(p, kod, sozluk):
    """kod: grup sozluk indisleri; sozluk: grup adlari."""
    t = np.zeros(len(p), dtype=np.int64)
    for i, g in enumerate(sozluk):
        if g in GRUP_TABLO:
            m = kod == i
            if m.any():
                bas, ad = GRUP_TABLO[g]
                t[m] = ad[np.searchsorted(bas, p[m], side="right") - 1]
    return t


def yuvarla(x, kod, sozluk, yukari):
    xi = np.ceil(x) if yukari else np.floor(x)
    t = adim_kod(xi.astype(np.int64), kod, sozluk)
    t = np.where(t == 0, 10, t)
    return (np.ceil(x / t) * t if yukari else np.floor(x / t) * t).astype(np.int64)


parcalar, ornek = [], []


def isle(t, kaynak, d):
    """t: islem_kodu, fiyat, kategori, seans kolonlu tablo (tek gun)."""
    g = gs.filter(pc.equal(gs["tarih"], pa.scalar(d))).drop_columns(["tarih"])
    t = t.join(g, "islem_kodu", join_type="left outer")
    de = pc.dictionary_encode(t["grup"].fill_null("?")).combine_chunks()
    sozluk = de.dictionary.to_pylist()
    kod = de.indices.to_numpy()
    p = np.rint(t["fiyat"].to_numpy() * 1000).astype(np.int64)
    a = adim_kod(p, kod, sozluk)
    tick_ok = np.where(a > 0, p % np.where(a > 0, a, 1) == 0, True)
    base = np.rint(t["baz"].fill_null(0).to_numpy() * 1000)
    sinirli_grup = np.array([g_ in SINIRLI for g_ in sozluk])
    sinir_var = (base > 0) & sinirli_grup[kod]
    cols = {"kaynak": pa.array(np.full(len(p), kaynak)), "grup": de,
            "pazar": t["pazar"].fill_null("?"), "kategori": t["kategori"], "seans": pc.cast(t["seans"], pa.string()),
            "tick_ok": pa.array(tick_ok), "tablo_var": pa.array(a > 0)}
    for m in MARJ:
        alt = yuvarla(base * (1 - m), kod, sozluk, True)
        ust = yuvarla(base * (1 + m), kod, sozluk, False)
        cols[f"disari_{int(m * 100)}"] = pa.array(sinir_var & ((p < alt) | (p > ust)))
    oran = np.where(sinir_var, p / np.where(base > 0, base, 1) - 1, np.nan)
    cols["oran_bin"] = pa.array(np.round(oran, 2))
    x = pa.table(cols)
    x = x.set_column(1, "grup", pc.cast(x["grup"], pa.string()))
    parcalar.append(x.group_by(list(cols)).aggregate([([], "count_all")]))
    bad = ~tick_ok
    if bad.any() and sum(len(o) for o in ornek) < 500:
        e = t.filter(pa.array(bad)).slice(0, 25).to_pandas()
        e["kaynak"], e["tarih"] = kaynak, d
        ornek.append(e)


gunler = sorted(os.path.basename(p) for p in glob.glob(os.path.join(emir_dir, "20*")))
for gun in gunler:
    d = datetime.date.fromisoformat(gun)
    for f in sorted(glob.glob(os.path.join(emir_dir, gun, "*.parquet"))):
        t = pq.read_table(f, columns=["islem_kodu", "fiyat", "emir_kategorisi", "seans", "degisiklik_sebebi"])
        t = t.filter(pc.and_(pc.is_in(t["degisiklik_sebebi"], pa.array([5, 6], pa.int16())),
                             pc.greater(t["fiyat"], 0)))
        t = t.select(["islem_kodu", "fiyat", "emir_kategorisi", "seans"]).rename_columns(
            ["islem_kodu", "fiyat", "kategori", "seans"])
        isle(t, "emir", d)
    print("emir", gun, flush=True)

pf = pq.ParquetFile(islem_src)
idx = pf.schema_arrow.get_field_index("tarih")
for gun in gunler:
    d = datetime.date.fromisoformat(gun)
    rgs = [i for i in range(pf.num_row_groups)
           if pf.metadata.row_group(i).column(idx).statistics.min <= d <= pf.metadata.row_group(i).column(idx).statistics.max]
    t = pf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "islem_fiyati", "alis_satis", "seans", "normal_islem"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["alis_satis"], "A")))
    t = pa.table({"islem_kodu": t["islem_kodu"], "fiyat": t["islem_fiyati"],
                  "kategori": pc.cast(t["normal_islem"], pa.int16()), "seans": t["seans"]})
    isle(t, "islem", d)
    print("islem", gun, flush=True)

A = pa.concat_tables(parcalar)
A = A.group_by(A.column_names[:-1]).aggregate([("count_all", "sum")]).rename_columns(A.column_names[:-1] + ["adet"])
pq.write_table(A, os.path.join(out, "fiyat_kontrol_sayac.parquet"))
if ornek:
    pd.concat(ornek).to_csv(os.path.join(out, "fiyat_adimi_ihlal_ornek.csv"), index=False, encoding="utf-8")
r = A.to_pandas()
print(r.groupby(["kaynak", "grup", "tick_ok"]).adet.sum().to_string())
for m in MARJ:
    k = f"disari_{int(m * 100)}"
    print(k, r[r.grup.isin(SINIRLI)].groupby(["kaynak", "grup", "pazar", k]).adet.sum().unstack(fill_value=0).to_string())
