"""Degerleme Oranlari (Aylik) xlsx -> Parquet (kayipsiz; tum hucreler geri okunup dogrulanir).

DataStore `degoran_M_YYYYAA.zip -> oranYYYYAA.xlsx` (`datastore-dosya-formatlari.md` 2.1.23).
Ilk sayfa ("sinif"): ustte endeks/pazar toplamlari, sonra sektor basliklari altinda paylar ve
"TOPLAM / ORTALAMA" satirlari. Basligin hemen altinda TOPLAM gelen sektor ana sektordur; alt
sektorleri, toplamlari ana sektor toplamini tutana kadar onu izler (sinir tabloda yazmaz, toplamdan
bulunur). En sonda Piyasa Oncesi Islem Platformu (POIP) bolumu vardir.

Her satir tek kayit: tur (ozet / ana_sektor_toplam / sektor_toplam / pay), kod, ad, ana_sektor, sektor
ve sayisal alanlar. Sayi olmayan hucreler ("VY" veri yok, "---" anlamsiz F/K) `<alan>_metin`
sutununda aynen tutulur; sayi sutunu o hucrede bostur.

Kullanim: python -I degerleme_oranlari_xlsx2parquet.py GIRIS.zip|GIRIS.xlsx CIKIS.parquet
"""
import io
import math
import re
import sys
import zipfile
from datetime import date

import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]
sys.stdout.reconfigure(encoding="utf-8")

# (sutun no, ad, beklenen baslik); sutun 5 basliksizdir (bazi toplam satirlarinda 0 tasir).
ALANLAR = [(3, "piyasa_degeri", "PİYASA DEĞERİ"), (4, "net_kar_son4", "NET KAR\n(SON 4 ÇEYREK)"),
           (5, "sutun_f", None), (6, "nakit_net_temettu", "NAKİT NET TEMETTÜ"), (7, "ozsermaye", "ÖZSERMAYE"),
           (10, "fk", "F/K"), (12, "tv_yuzde", "TV (%)"), (14, "pd_dd", "PD/DD")]
KULLANILAN = {0, 2} | {j for j, _, _ in ALANLAR}
S, D = pa.string(), pa.float64()
SEMA = pa.schema([("tarih", pa.date32()), ("satir", pa.int32()), ("tur", S), ("kod", S), ("ad", S),
                  ("ana_sektor", S), ("sektor", S)]
                 + [f for _, a, _ in ALANLAR for f in ((a, D), (a + "_metin", S))])

if src.lower().endswith(".zip"):
    z = zipfile.ZipFile(src)
    assert len(z.infolist()) == 1, z.namelist()
    veri = z.read(z.infolist()[0])
else:
    veri = open(src, "rb").read()
wb = openpyxl.load_workbook(io.BytesIO(veri), read_only=True, data_only=True)
satirlar = [tuple(r) for r in wb.worksheets[0].iter_rows(values_only=True)]

# Baslik: tarih satiri ve sutun basliklari sabit yerde olmali.
m = re.fullmatch(r"\((\d\d)\.(\d\d)\.(\d{4}) Tarihi İtibarıyladır\)", str(satirlar[3][2]))
assert satirlar[2][2] == "DEĞERLEME ORANLARI" and m, satirlar[2:4]
tarih = date(int(m[3]), int(m[2]), int(m[1]))
assert satirlar[4][3] == "(Bin TL)", satirlar[4]
for j, a, b in ALANLAR:
    assert satirlar[5][j] == b, (a, satirlar[5][j], b)
for i, r in enumerate(satirlar):
    disarida = [j for j, v in enumerate(r) if v is not None and j not in KULLANILAN]
    assert not disarida, ("beklenmeyen dolu sutun", i, disarida)

kayit = []
ana = None          # [ad, hedef toplam, birikmis toplam]
sektor = None
pay_toplam = 0.0
bolum = 0           # 0: ust ozet, 1: pay piyasasi


def sayi(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def ekle(i, tur, kod, ad, r):
    k = {"tarih": tarih, "satir": i, "tur": tur, "kod": kod, "ad": ad,
         "ana_sektor": ana[0] if ana else (sektor if tur != "ozet" else None),
         "sektor": sektor if tur in ("pay", "sektor_toplam") else None}
    for j, a, _ in ALANLAR:
        v = r[j] if j < len(r) else None
        if v is None:
            k[a], k[a + "_metin"] = None, None
        elif sayi(v):
            assert math.isfinite(v) and float(v) == v, (i, a, v)
            k[a], k[a + "_metin"] = float(v), None
        else:
            k[a], k[a + "_metin"] = None, str(v)
    kayit.append(k)
    return k


for i, r in enumerate(satirlar):
    if i < 6 or all(v is None for v in r):
        continue
    c0, c2 = r[0], r[2]
    sonraki = next((s for s in satirlar[i + 1:] if any(v is not None for v in s)), (None,) * 3)
    if bolum == 0:
        if c2 == "PAY PİYASASI (PP)":
            bolum = 1
            continue
        assert isinstance(c2, str) and c2.endswith("TOPLAM/ORT."), (i, r[:4])
        ekle(i, "ozet", c0, c2, r)
    elif (c0 == c2 or c0 is None) and isinstance(c2, str) and not c2.startswith("TOPLAM") \
            and all(r[j] is None for j, _, _ in ALANLAR):
        # sektor basligi (2024-05'te bazi basliklarda kod sutunu bos)
        if sonraki[0] is None and str(sonraki[2]).startswith("TOPLAM"):
            assert ana is None, ("ana sektor kapanmadan yenisi basladi", i, ana)
            ana = [c2, None, 0.0]
            sektor = None
        else:
            sektor = c2
    elif c0 is None and str(c2).startswith("TOPLAM"):
        if ana is not None and ana[1] is None and sektor is None:
            ana[1] = r[3]
            ekle(i, "ana_sektor_toplam", None, ana[0], r)
            continue
        k = ekle(i, "sektor_toplam", None, sektor, r)
        payler = sum(x["piyasa_degeri"] or 0 for x in kayit if x["tur"] == "pay" and x["sektor"] == sektor
                     and x["ana_sektor"] == k["ana_sektor"])
        assert math.isclose(payler, r[3], rel_tol=1e-9, abs_tol=1e-3), ("sektor toplami tutmuyor", sektor, payler, r[3])
        if ana is not None:
            ana[2] += r[3]
            if math.isclose(ana[2], ana[1], rel_tol=1e-9, abs_tol=1e-3):
                ana = None
            else:
                assert ana[2] < ana[1] * (1 + 1e-9), ("ana sektor toplami asildi", ana)
        sektor = None
    elif c0 is not None and isinstance(c2, str) and c2.endswith("TOPLAM / ORT."):
        # POIP bolumu kendi TOPLAM satiri yerine bu ozet satiriyla biter
        assert ana is None, ana
        ekle(i, "ozet", c0, c2, r)
        if sektor is not None:
            payler = sum(x["piyasa_degeri"] or 0 for x in kayit if x["tur"] == "pay" and x["sektor"] == sektor)
            assert math.isclose(payler, r[3], rel_tol=1e-9, abs_tol=1e-3), ("bolum toplami tutmuyor", sektor, payler, r[3])
            sektor = None
    elif c0 is not None and c2 is not None and c0 != c2:
        assert sektor is not None, ("sektorsuz pay", i, r[:4])
        ekle(i, "pay", c0, c2, r)
    else:
        sys.exit(f"HATA: tanimlanamayan satir {i}: {r[:8]}")
assert ana is None and sektor is None, (ana, sektor)

t = pa.Table.from_pylist(kayit, schema=SEMA)
pq.write_table(t, dst, compression="zstd", compression_level=9)

# Dogrulama: geri oku; her kaydin hucreleri kaynak satirdaki hucrelerle ayni olmali.
geri = pq.read_table(dst)
assert geri.schema.equals(SEMA, check_metadata=False)
fark = 0
for k in geri.to_pylist():
    r = satirlar[k["satir"]]
    if k["kod"] != r[0] and not (k["tur"].endswith("toplam") and r[0] is None):
        fark += 1
    if k["tur"] != "ana_sektor_toplam" and k["tur"] != "sektor_toplam" and k["ad"] != r[2]:
        fark += 1
    for j, a, _ in ALANLAR:
        v = r[j] if j < len(r) else None
        g = k[a] if k[a] is not None else k[a + "_metin"]
        if not ((v is None and g is None) or (sayi(v) and g == float(v)) or (isinstance(v, str) and g == v)):
            fark += 1
            if fark <= 5:
                print("FARK", k["satir"], a, repr(v), repr(g))
pay = [k for k in kayit if k["tur"] == "pay"]
pp = next(k for k in kayit if k["ad"] == "PP GENEL TOPLAM/ORT.")
pp_tutar = math.isclose(sum(k["piyasa_degeri"] or 0 for k in pay), pp["piyasa_degeri"], rel_tol=1e-9)
print(f"tarih={tarih} satir={geri.num_rows} pay={len(pay)} sektor={len({(k['ana_sektor'], k['sektor']) for k in pay})} "
      f"ana_sektor={len({k['ana_sektor'] for k in pay})} pp_genel_toplami={'tutar' if pp_tutar else 'TUTMAZ'} fark={fark}")
print("SONUC:", "GECTI" if fark == 0 and pp_tutar else "KALDI")
