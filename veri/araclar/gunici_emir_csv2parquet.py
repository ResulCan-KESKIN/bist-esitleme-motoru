"""PP_GUNICIEMIR CSV -> Parquet (akis, kayipsiz tip donusumu).

Kullanim: python -I gunici_emir_csv2parquet.py GIRIS.csv|GIRIS.zip CIKIS.parquet [max_blok]
"""
import sys
import zipfile
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]
max_blocks = int(sys.argv[3]) if len(sys.argv) > 3 else None

names = [
    "tarih", "emir_no", "emir_giris_zamani", "emir_degistirilme_zamani", "islem_kodu",
    "alis_satis", "emir_fiyat_turu", "emir_turu", "emir_kategorisi", "gecerlilik_turu",
    "emir_durumu", "degisiklik_sebebi", "emir_miktari", "kalan_miktar", "gorunen_miktar",
    "fiyat", "afk", "seans", "en_iyi_alis_fiyati", "en_iyi_satis_fiyati",
    "onceki_emir_no", "islem_numarasi", "eslesen_miktar", "giveup_flag",
    "guncelleme_no", "guncelleme_zamani",
]
types = {
    "tarih": pa.date32(),
    "emir_no": pa.string(),
    "emir_giris_zamani": pa.timestamp("us"),
    "emir_degistirilme_zamani": pa.timestamp("us"),
    "islem_kodu": pa.string(),
    "alis_satis": pa.string(),
    "emir_fiyat_turu": pa.int16(),
    "emir_turu": pa.int16(),
    "emir_kategorisi": pa.int16(),
    "gecerlilik_turu": pa.string(),
    "emir_durumu": pa.int16(),
    "degisiklik_sebebi": pa.int16(),
    "emir_miktari": pa.int64(),
    "kalan_miktar": pa.int64(),
    "gorunen_miktar": pa.int64(),
    "fiyat": pa.float64(),
    "afk": pa.string(),
    "seans": pa.string(),
    "en_iyi_alis_fiyati": pa.float64(),
    "en_iyi_satis_fiyati": pa.float64(),
    "onceki_emir_no": pa.string(),        # cogunlukla bos
    "islem_numarasi": pa.int64(),         # bos -> null
    "eslesen_miktar": pa.int64(),         # bos -> null
    "giveup_flag": pa.string(),
    "guncelleme_no": pa.int64(),
    "guncelleme_zamani": pa.timestamp("s"),
}

if src.lower().endswith(".zip"):
    # CSV'yi diske acmadan zip icinden akis olarak oku (tek CSV beklenir)
    zf = zipfile.ZipFile(src)
    members = [i.filename for i in zf.infolist() if i.filename.lower().endswith(".csv")]
    assert len(members) == 1, members
    src_stream = zf.open(members[0])
else:
    src_stream = src

reader = pc.open_csv(
    src_stream,
    read_options=pc.ReadOptions(column_names=names, skip_rows=2, block_size=128 << 20),
    parse_options=pc.ParseOptions(delimiter=";"),
    convert_options=pc.ConvertOptions(
        column_types=types,
        strings_can_be_null=False,
    ),
)

writer = pq.ParquetWriter(
    dst, reader.schema, compression="zstd", compression_level=9,
    use_dictionary=True, write_statistics=True,
)
n = 0
for i, batch in enumerate(reader):
    writer.write_batch(batch, row_group_size=2_000_000)
    n += batch.num_rows
    if i % 20 == 0:
        print(f"blok {i} satir {n:,}", flush=True)
    if max_blocks and i + 1 >= max_blocks:
        break
writer.close()
print(f"bitti: {n:,} satir", flush=True)
