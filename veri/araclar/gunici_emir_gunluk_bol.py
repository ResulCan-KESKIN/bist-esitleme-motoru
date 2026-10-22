"""PP_GUNICIEMIR aylik parquet -> gun ve arac grubu bazinda bolumlenmis, sirali parquet.

Aylik dosyada satir gruplari 12 gune kadar yayilir; gun bazinda okumak icin bu adim gerekir.
Cikti: CIKTI/YYYY-MM-DD/<grup>-<kova>.parquet
  grup: pay (.E, .F, .F1, .F2, .S1, .R, .BE, ...), varant (.V, .C)
  kova: islem_kodu'na gore sabit kova (crc32 % 8); her dosya
        (islem_kodu, emir_degistirilme_zamani, guncelleme_no) sirasinda yazilir.
Kayipsizdir: kolonlar ve degerler degismez; yalniz satir sirasi degisir. Sonda satir sayisi denetlenir.
Kullanim: python -I gunici_emir_gunluk_bol.py AYLIK.parquet CIKTI_KLASORU [GECICI_KLASOR] [--yalniz-ikinci-gecis]
  --yalniz-ikinci-gecis: kesintiden sonra yalniz gecici klasorde kalan ara dosyalari isler; sonda tum
  gunluk dosyalarin satir toplami aylik dosyayla karsilastirilir.
"""
import sys, os, shutil, zlib
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

arg = [a for a in sys.argv[1:] if not a.startswith("--")]
ikinci = "--yalniz-ikinci-gecis" in sys.argv
src, out = arg[0], arg[1]
tmp = arg[2] if len(arg) > 2 else os.path.join(out, "_gecici")
KOVA = 8
VARANT = {"V", "C"}
SOZLUK = ["islem_kodu", "alis_satis", "gecerlilik_turu", "afk", "seans", "giveup_flag"]
os.makedirs(tmp, exist_ok=True)


def grup(kod):
    return "varant" if kod.rsplit(".", 1)[-1] in VARANT else "pay"


def kod_sutunu(t, f):
    """islem_kodu sozlugu uzerinden satir basina f(kod) degeri (int32)."""
    de = t["islem_kodu"].combine_chunks()
    if not pa.types.is_dictionary(de.type):
        de = pc.dictionary_encode(de)
    return pc.take(pa.array([f(k) for k in de.dictionary.to_pylist()], pa.int32()), de.indices)


# 1. gecis: (gun, grup, kova) ara dosyalari
pf = pq.ParquetFile(src, read_dictionary=SOZLUK)
yazici = {}
toplam = 0
for bas in range(0, 0 if ikinci else pf.num_row_groups, 20):
    t = pf.read_row_groups(list(range(bas, min(bas + 20, pf.num_row_groups)))).unify_dictionaries()
    toplam += t.num_rows
    g = kod_sutunu(t, lambda k: (KOVA if grup(k) == "varant" else 0) + zlib.crc32(k.encode()) % KOVA)
    gun = pc.cast(t["tarih"], pa.int32())
    anahtar = pc.add(pc.multiply(gun, 2 * KOVA), g)
    t = t.take(pc.sort_indices(anahtar))
    vc = sorted(pc.value_counts(anahtar).to_pylist(), key=lambda x: x["values"])
    ofs = 0
    for v in vc:
        k, n = v["values"], v["counts"]
        if k not in yazici:
            d = np.datetime64(k // (2 * KOVA), "D")
            gk = k % (2 * KOVA)
            ad = f"{d}_{'varant' if gk >= KOVA else 'pay'}-{gk % KOVA}.parquet"
            yazici[k] = pq.ParquetWriter(os.path.join(tmp, ad), t.schema, compression="lz4",
                                         use_dictionary=SOZLUK, write_statistics=False)
        yazici[k].write_table(t.slice(ofs, n))
        ofs += n
    print(f"1. gecis rg {bas}/{pf.num_row_groups}", flush=True)
for w in yazici.values():
    w.close()

# 2. gecis: her ara dosyayi sirala ve yaz
yazilan = 0
for ad in sorted(os.listdir(tmp)):
    d, gk = ad[:-8].split("_")
    t = pq.read_table(os.path.join(tmp, ad), read_dictionary=SOZLUK).unify_dictionaries()
    kodlar = t["islem_kodu"].combine_chunks().dictionary.to_pylist()
    sira = {k: i for i, k in enumerate(sorted(kodlar))}
    t = t.append_column("_sira", kod_sutunu(t, lambda k: sira[k]))
    t = t.take(pc.sort_indices(t, sort_keys=[("_sira", "ascending"), ("emir_degistirilme_zamani", "ascending"),
                                             ("guncelleme_no", "ascending")])).drop_columns(["_sira"])
    gun_dir = os.path.join(out, d)
    os.makedirs(gun_dir, exist_ok=True)
    pq.write_table(t, os.path.join(gun_dir, f"{gk}.parquet"), compression="zstd", use_dictionary=SOZLUK,
                   row_group_size=1_000_000, write_statistics=["islem_kodu", "emir_degistirilme_zamani"])
    yazilan += t.num_rows
    del t
    os.remove(os.path.join(tmp, ad))
    print(f"2. gecis {ad}", flush=True)
shutil.rmtree(tmp, ignore_errors=True)
if ikinci:
    toplam = pf.metadata.num_rows
    yazilan = sum(pq.ParquetFile(os.path.join(r, f)).metadata.num_rows
                  for r, _, fs in os.walk(out) for f in fs if f.endswith(".parquet"))
print(f"okunan {toplam:,} yazilan {yazilan:,}", "TAMAM" if toplam == yazilan else "FARK VAR")
