"""PP_GUNICIEMIR parquet profili (tek gecis, pyarrow group_by).

Ciktilar (CIKTI_KLASORU):
  emir_kategorik.parquet  : kategorik alanlarin tum birlesimleri ve adetleri (capraz tablolar buradan)
  emir_sira_seans.parquet : (tarih, islem_kodu, seans) bazinda adet, ilk/son degistirilme zamani
  emir_ozet.txt
Kullanim: python -I gunici_emir_profil.py GIRIS.parquet CIKTI_KLASORU [satir_grubu_parcasi]
"""
import sys, os
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

src, out = sys.argv[1], sys.argv[2]
parca = int(sys.argv[3]) if len(sys.argv) > 3 else 20
os.makedirs(out, exist_ok=True)
sozluk = ["islem_kodu", "seans", "gecerlilik_turu", "alis_satis", "afk", "giveup_flag"]
pf = pq.ParquetFile(src, read_dictionary=sozluk)
cols = ["tarih", "emir_giris_zamani", "emir_degistirilme_zamani", "islem_kodu", "alis_satis",
        "emir_fiyat_turu", "emir_turu", "emir_kategorisi", "gecerlilik_turu", "emir_durumu",
        "degisiklik_sebebi", "afk", "seans", "giveup_flag", "guncelleme_zamani", "islem_numarasi",
        "onceki_emir_no", "gorunen_miktar", "emir_miktari", "kalan_miktar", "fiyat"]
K1 = ["tarih", "seans", "degisiklik_sebebi", "emir_fiyat_turu", "emir_turu", "emir_kategorisi",
      "gecerlilik_turu", "emir_durumu", "afk", "alis_satis", "giveup_flag",
      "islem_no_dolu", "onceki_dolu", "gizli", "gun_farki", "utc_fark_saat", "giris_sonra", "fiyat_sifir"]
GUN_US = 86_400_000_000

a_parca, b_parca = [], []
toplam = 0
for bas in range(0, pf.num_row_groups, parca):
    t = pf.read_row_groups(list(range(bas, min(bas + parca, pf.num_row_groups))), columns=cols).unify_dictionaries()
    toplam += t.num_rows
    deg = t["emir_degistirilme_zamani"]
    deg_us = pc.cast(deg, pa.int64()).to_numpy()
    tarih_us = pc.cast(pc.cast(t["tarih"], pa.timestamp("us")), pa.int64()).to_numpy()
    gun_farki = (deg_us // GUN_US - tarih_us // GUN_US).astype(np.int32)
    gz = pc.cast(pc.cast(t["guncelleme_zamani"], pa.timestamp("us")), pa.int64()).to_numpy(zero_copy_only=False)
    utc = np.rint((gz - deg_us) / 3.6e9)
    utc = pa.array(np.where(np.isnan(utc), -99, utc).astype(np.int32))
    ek = {
        "islem_no_dolu": pc.is_valid(t["islem_numarasi"]),
        "onceki_dolu": pc.not_equal(t["onceki_emir_no"], ""),
        "gizli": pc.less(t["gorunen_miktar"], t["emir_miktari"]),
        "gun_farki": pa.array(gun_farki),
        "utc_fark_saat": utc,
        "giris_sonra": pc.greater(t["emir_giris_zamani"], deg),
        "fiyat_sifir": pc.equal(t["fiyat"], 0),
        "tod": pa.array(deg_us % GUN_US),
    }
    for k, v in ek.items():
        t = t.append_column(k, v)
    a_parca.append(t.group_by(K1).aggregate([([], "count_all")]))
    b_parca.append(t.group_by(["tarih", "islem_kodu", "seans"]).aggregate(
        [([], "count_all"), ("tod", "min"), ("tod", "max")]))
    print(f"rg {bas}/{pf.num_row_groups} satir {toplam:,}", flush=True)


def birlestir(parcalar, anahtar, agg):
    t = pa.concat_tables([p.cast(pa.schema([f.with_type(f.type.value_type) if pa.types.is_dictionary(f.type) else f
                                            for f in p.schema])) for p in parcalar])
    return t.group_by(anahtar).aggregate(agg)


A = birlestir(a_parca, K1, [("count_all", "sum")])
B = birlestir(b_parca, ["tarih", "islem_kodu", "seans"], [("count_all", "sum"), ("tod_min", "min"), ("tod_max", "max")])
pq.write_table(A, os.path.join(out, "emir_kategorik.parquet"))
pq.write_table(B, os.path.join(out, "emir_sira_seans.parquet"))
with open(os.path.join(out, "emir_ozet.txt"), "w", encoding="utf-8") as f:
    f.write(f"toplam satir: {toplam}\nkategorik birlesim: {A.num_rows}\nsira-seans: {B.num_rows}\n")
print("bitti", toplam)
