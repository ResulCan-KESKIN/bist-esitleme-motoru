"""PP_GUNICITUMENDEKS CSV -> Parquet (kayipsiz; her farkli metin degeri geri cevrilip dogrulanir).

Gun ici endeks degerleri, butun fiyat endeksleri, saniyelik (`datastore-dosya-formatlari.md` 2.1.19).
Iki baslik satiri (TR/EN), `;` ayracli; tarih GG/AA/YYYY. Satirlar kaynaktaki sirada ve oldugu gibi
yazilir (19.07.2024 ve 28.08.2024 acilisindaki tekrarli satirlar dahil; `veri/README.md`).

Kullanim: python -I gunici_endeks_csv2parquet.py GIRIS.csv|GIRIS.zip CIKIS.parquet
"""
import sys
import zipfile
from datetime import datetime, time
from decimal import Decimal

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pcsv
import pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]
BASLIK = [b"TARIH;ZAMAN;ENDEKS KODU;ENDEKSLER;FIYAT ENDEKSI DEGERI", b"DATE;TIME;INDEX CODE; INDICES;PRICE INDEX VALUE"]
AD = ["tarih", "zaman", "endeks_kodu", "endeks_adi", "deger"]
SEMA = pa.schema([("tarih", pa.date32()), ("zaman", pa.time32("ms")), ("endeks_kodu", pa.string()),  # parquet time32[s] tutmaz
                  ("endeks_adi", pa.string()), ("deger", pa.float64())])


def ac():
    if src.lower().endswith(".zip"):
        z = zipfile.ZipFile(src)
        assert len(z.infolist()) == 1, z.namelist()
        return z.open(z.infolist()[0])
    return open(src, "rb")


with ac() as f:
    bas = [f.readline().rstrip(b"\r\n") for _ in range(2)]
assert bas == BASLIK, bas
n, son = 0, b""
with ac() as f:
    while True:
        b = f.read(64 << 20)
        if not b:
            break
        n += b.count(b"\n")
        son = b[-1:]
csv_satir = (n if son == b"\n" else n + 1) - 2

with ac() as f:
    ham = pcsv.read_csv(f, read_options=pcsv.ReadOptions(skip_rows=2, column_names=AD, block_size=64 << 20),
                        parse_options=pcsv.ParseOptions(delimiter=";"),
                        convert_options=pcsv.ConvertOptions(column_types={a: pa.string() for a in AD},
                                                            strings_can_be_null=False))
assert ham.num_rows == csv_satir, (ham.num_rows, csv_satir)


def sozlukle(ad, cevir, geri):
    """Sutunu sozluk kodla; her farkli metni cevir, geri metne donusturup ayniligini dogrula."""
    d = pc.dictionary_encode(ham[ad].combine_chunks())
    metin = d.dictionary.to_pylist()
    deger = [cevir(m) for m in metin]
    for m, v in zip(metin, deger):
        if geri(v, m) is False:
            sys.exit(f"HATA: {ad} degeri kayipsiz cevrilemiyor: {m!r} -> {v!r}")
    return d.indices, pa.array(deger, SEMA.field(ad).type)


def tarih_cevir(m):
    return datetime.strptime(m, "%d/%m/%Y").date()


def zaman_cevir(m):
    s, d, sn = (int(x) for x in m.split(":"))
    return time(s, d, sn)


def deger_geri(v, m):
    return Decimal(repr(v)) == Decimal(m)


kolon = {}
for ad, cevir, geri in [("tarih", tarih_cevir, lambda v, m: v.strftime("%d/%m/%Y") == m),
                        ("zaman", zaman_cevir, lambda v, m: v.strftime("%H:%M:%S") == m),
                        ("deger", float, deger_geri)]:
    ind, sozluk = sozlukle(ad, cevir, geri)
    kolon[ad] = sozluk.take(ind)
kolon["endeks_kodu"] = ham["endeks_kodu"].combine_chunks()
kolon["endeks_adi"] = ham["endeks_adi"].combine_chunks()
for a in ("endeks_kodu", "endeks_adi"):
    assert pc.all(pc.not_equal(kolon[a], "")).as_py(), f"bos {a}"

tablo = pa.Table.from_arrays([kolon[a] for a in SEMA.names], schema=SEMA)
pq.write_table(tablo, dst, compression="zstd", compression_level=9, row_group_size=1_000_000)

# Dogrulama: geri oku; her sutun yazilanla birebir ayni olmali.
geri = pq.read_table(dst)
assert geri.schema.equals(SEMA, check_metadata=False), geri.schema
assert geri.num_rows == csv_satir, (geri.num_rows, csv_satir)
fark = 0
for a in SEMA.names:
    esit = pc.equal(geri[a], tablo[a])
    fark += geri.num_rows - pc.sum(pc.cast(esit, pa.int64())).as_py()
gunler = pc.unique(geri["tarih"])
print(f"csv_veri_satiri={csv_satir:,} parquet={geri.num_rows:,} gun={len(gunler)} "
      f"endeks={len(pc.unique(geri['endeks_kodu']))} fark={fark}")
print("SONUC:", "GECTI" if fark == 0 else "KALDI")
