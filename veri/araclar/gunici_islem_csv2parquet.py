"""PP_GUNICIISLEM CSV -> Parquet (akis, kayipsiz tip donusumu).

Kullanim: python -I gunici_islem_csv2parquet.py GIRIS.csv|GIRIS.zip CIKIS.parquet [max_blok]
"""
import sys
import zipfile
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]
max_blocks = int(sys.argv[3]) if len(sys.argv) > 3 else None

# Kaynakta 21 sutun; 18 ve 21 ayni adli oldugu icin yeniden adlandirildi.
names = [
    "tarih", "islem_kodu", "ortak_sozlesme_no", "eslesen_bolum", "alis_satis",
    "islem_adedi", "islem_fiyati", "islem_hacmi", "emir_no", "islem_zamani",
    "normal_islem", "seans", "islem_durumu", "takas_tarihi", "aktif_pasif",
    "takas_tarafi_islem_no", "takas_tarafi_ortak_anlasma_no",
    "islem_degistirilme_zamani", "giveup_flag", "guncelleme_no", "guncelleme_zamani",
]
types = {
    "tarih": pa.date32(),
    "islem_kodu": pa.string(),
    "ortak_sozlesme_no": pa.string(),
    "eslesen_bolum": pa.string(),
    "alis_satis": pa.string(),
    "islem_adedi": pa.int64(),
    "islem_fiyati": pa.float64(),
    "islem_hacmi": pa.float64(),
    "emir_no": pa.string(),
    "islem_zamani": pa.string(),          # HH:MM:SS.ffffff, oldugu gibi
    "normal_islem": pa.int16(),
    "seans": pa.string(),
    "islem_durumu": pa.string(),
    "takas_tarihi": pa.string(),          # kaynakta cogunlukla bos (" ")
    "aktif_pasif": pa.string(),
    "takas_tarafi_islem_no": pa.int64(),
    "takas_tarafi_ortak_anlasma_no": pa.int64(),
    "islem_degistirilme_zamani": pa.timestamp("s"),
    "giveup_flag": pa.string(),
    "guncelleme_no": pa.string(),
    "guncelleme_zamani": pa.timestamp("s"),
}
dict_cols = [
    "islem_kodu", "eslesen_bolum", "alis_satis", "normal_islem", "seans",
    "islem_durumu", "takas_tarihi", "aktif_pasif", "giveup_flag", "guncelleme_no",
]

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
    read_options=pc.ReadOptions(column_names=names, skip_rows=2, block_size=64 << 20),
    parse_options=pc.ParseOptions(delimiter=";"),
    convert_options=pc.ConvertOptions(
        column_types=types,
        strings_can_be_null=False,
        timestamp_parsers=["%Y-%m-%d %H:%M:%S"],
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
