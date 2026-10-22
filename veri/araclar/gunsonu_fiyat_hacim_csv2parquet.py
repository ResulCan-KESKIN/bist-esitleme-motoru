"""PP_GUNSONUFIYATHACIM CSV -> Parquet (kayipsiz; tum satirlar geri okunup dogrulanir).

Her sutun once metin okunur; int64 / float64 / date32'ye yalnizca her deger
sayisal olarak birebir korunuyorsa cevrilir, aksi halde metin kalir. Bos hucre
sayisal sutunda null olur.

Kullanim: python -I gunsonu_fiyat_hacim_csv2parquet.py GIRIS.csv CIKIS.parquet
"""
import sys
from datetime import date
from decimal import Decimal
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]

# 50 sutun; kaynak basliklari Turkce ve bazilari bosluklu, ASCII slug kullan.
with open(src, encoding="utf-8") as f:
    en = f.readlines()[1].strip().split(";")
names = [c.lower().replace(" ", "_").replace("(%)", "yuzde").replace(".", "") for c in en]
assert len(set(names)) == len(names), "yinelenen sutun adi"

raw = pc.read_csv(
    src,
    read_options=pc.ReadOptions(column_names=names, skip_rows=2),
    parse_options=pc.ParseOptions(delimiter=";"),
    convert_options=pc.ConvertOptions(
        column_types={n: pa.string() for n in names}, strings_can_be_null=False),
)


def as_int(vals):
    out = []
    for v in vals:
        if v == "":
            out.append(None)
        else:
            i = int(v)
            if str(i) != v:
                return None
            out.append(i)
    return pa.array(out, pa.int64())


def as_float(vals):
    out = []
    for v in vals:
        if v == "":
            out.append(None)
        else:
            x = float(v)
            if Decimal(repr(x)) != Decimal(v):
                return None
            out.append(x)
    return pa.array(out, pa.float64())


def as_date(vals):
    try:
        return pa.array([date.fromisoformat(v) for v in vals], pa.date32())
    except ValueError:
        return None


cols, kinds = [], {}
for n in names:
    vals = raw[n].to_pylist()
    arr = None
    if n == "trade_date":
        arr = as_date(vals)
    elif any(vals):  # tamami bos sutun metin kalir
        for fn, kind in ((as_int, "int64"), (as_float, "float64")):
            try:
                arr = fn(vals)
            except ValueError:
                arr = None
            if arr is not None:
                break
    if arr is None:
        arr, kind = raw[n], "string"
    else:
        kind = str(arr.type)
    kinds[n] = kind
    cols.append(arr)

table = pa.table(cols, names=names)
pq.write_table(table, dst, compression="zstd", compression_level=9, row_group_size=1_000_000)

# Dogrulama: parquet'i geri oku, her hucreyi kaynak metinle karsilastir.
back = pq.read_table(dst)
assert back.num_rows == raw.num_rows, (back.num_rows, raw.num_rows)
bad = 0
for n in names:
    a, b = raw[n].to_pylist(), back[n].to_pylist()
    t = back.schema.field(n).type
    for x, y in zip(a, b):
        if pa.types.is_integer(t):
            ok = (y is None and x == "") or (y is not None and int(x) == y)
        elif pa.types.is_floating(t):
            ok = (y is None and x == "") or (y is not None and Decimal(x) == Decimal(repr(y)))
        elif pa.types.is_date(t):
            ok = x == y.isoformat()
        else:
            ok = x == y
        if not ok:
            bad += 1
            if bad <= 5:
                print("FARK", n, repr(x), repr(y))
print(f"satir={back.num_rows:,} sutun={back.num_columns} fark={bad}")
print("turler:", {k: sum(1 for v in kinds.values() if v == k) for k in set(kinds.values())})
print("string kalan:", [n for n, k in kinds.items() if k == "string"])
print("SONUC:", "GECTI" if bad == 0 else "KALDI")
