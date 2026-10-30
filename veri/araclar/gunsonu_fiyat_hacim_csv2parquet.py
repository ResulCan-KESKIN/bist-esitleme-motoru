"""PP_GUNSONUFIYATHACIM CSV -> Parquet (kayipsiz; tum satirlar geri okunup dogrulanir).

Her ay ayni sabit semayla yazilir (SEMA), aylar birlestirilebilsin diye. Her sutun
once metin okunur, sonra semadaki ture cevrilir; deger o turde birebir
korunmuyorsa (or. ondalik sutunda metin) dosya yazilmaz, sema genisletilmelidir.
Bos hucre sayisal sutunda ve corporate_action'da null olur, diger metin
sutunlarinda "" kalir.

Kullanim: python -I gunsonu_fiyat_hacim_csv2parquet.py GIRIS.csv CIKIS.parquet
"""
import sys
from datetime import date
from decimal import Decimal
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

# 2024-09…2025-08 aylarinin hepsine uyan en genis tur. corporate_action metindir
# ("01&03" gibi degerler var; kodlar iki haneli: "03", "06").
D, I, S = pa.float64(), pa.int64(), pa.string()
SEMA = pa.schema([
    ("trade_date", pa.date32()),
    ("instrument_series_code", S), ("instrument_name", S), ("market_sub_segment", S), ("market_segment", S),
    ("market", S), ("instrument_group", S), ("instrument_type", S), ("instrument_class", S), ("trading_method", S),
    ("market_maker", I), ("bist_100_index", I), ("bist_30_index", I), ("gross_settlement", I),
    ("corporate_action", S), ("suspended", I),
    ("previous_last_price", D), ("opening_price", D), ("opening_session_price", D), ("lowest_price", D),
    ("highest_price", D), ("closing_price", D), ("closing_session_price", D), ("change_to_previous_closing_yuzde", D),
    ("remaining_bid", D), ("remaining_ask", D), ("vwap", D), ("total_traded_value", D),
    ("total_traded_volume", I), ("total_number_of_contracts", I), ("reference_price", D),
    ("traded_value_at_opening_session", D), ("traded_volume_at_opening_session", I),
    ("number_of_contracts_at_opening_session", I),
    ("traded_value_at_closing_session", D), ("traded_volume_at_closing_session", I),
    ("number_of_contracts_at_closing_session", I),
    ("traded_value_of_trades_at_closing_price", D), ("traded_volume_of_trades_at_closing_price", I),
    ("number_of_contracts_of_trades_at_closing_price", I),
    ("lowest_short_sale_price", D), ("highest_short_sale_price", D), ("short_sale_vwap", D),
    ("traded_value_of_short_sale_trades", D), ("traded_volume_of_short_sale_trades", I),
    ("number_of_contracts_of_short_sale_trades", I),
    ("lowest_trade_report_price", D), ("highest_trade_report_price", D), ("trade_report_vwap", D),
    ("trade_report_traded_value", D), ("trade_report_traded_volume", I), ("number_of_trade_reports", I),
])

src, dst = sys.argv[1], sys.argv[2]

# 52 sutun; kaynak basliklari Turkce ve bazilari bosluklu, ASCII slug kullan.
with open(src, encoding="utf-8") as f:
    en = f.readlines()[1].strip().split(";")
names = [c.lower().replace(" ", "_").replace("(%)", "yuzde").replace(".", "") for c in en]
assert names == SEMA.names, ("sutunlar semayla ayni degil", [n for n in names if n not in SEMA.names])

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


cols = []
for fld in SEMA:
    n, t = fld.name, fld.type
    vals = raw[n].to_pylist()
    try:
        if pa.types.is_date(t):
            arr = as_date(vals)
        elif pa.types.is_integer(t):
            arr = as_int(vals)
        elif pa.types.is_floating(t):
            arr = as_float(vals)
        elif n == "corporate_action":
            arr = pa.array([None if v == "" else v for v in vals], pa.string())
        else:
            arr = raw[n]
    except ValueError:
        arr = None
    if arr is None:
        sys.exit(f"HATA: {n} sutunu {t} turune kayipsiz cevrilemiyor; SEMA genisletilmeli")
    cols.append(arr)

table = pa.Table.from_arrays(cols, schema=SEMA)
pq.write_table(table, dst, compression="zstd", compression_level=9, row_group_size=1_000_000)

# Dogrulama: parquet'i geri oku, her hucreyi kaynak metinle karsilastir.
back = pq.read_table(dst)
assert back.schema.equals(SEMA, check_metadata=False), back.schema
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
            ok = x == y or (n == "corporate_action" and x == "" and y is None)
        if not ok:
            bad += 1
            if bad <= 5:
                print("FARK", n, repr(x), repr(y))
print(f"satir={back.num_rows:,} sutun={back.num_columns} fark={bad} sema=sabit")
print("SONUC:", "GECTI" if bad == 0 else "KALDI")
