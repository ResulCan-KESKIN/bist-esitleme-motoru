"""Endeks gostergeleri (pay-gun): payin gunluk getirisi piyasadan (BIST TUM, XUTUM) ve kendi sektor endeksinden ne kadar
ayriliyor. Var olan ozellik tablosuna sutun ekler (kapanis_ozellikleri.py gibi).

- Endeksin gun sonu degeri: gun ici endeks dosyasinda (veri/gun-ici-endeks) o gunun son kaydi; gunluk getiri bir onceki
  islem gununun son kaydina gore. Verinin ilk gununde onceki ay dosyasi yoksa getiri bostur.
- Payin sektoru: degerleme dosyasinda (veri/degerleme-orani) bir onceki ay sonundaki sektoru (yoksa ayni ay); sektor ->
  endeks eslemesi tespit/sektor_endeks.csv (sektor adi endeks adiyla ortusuyor / ana sektor endeksi / karsiligi yoksa
  XUTUM; dayanak sutununda). Degerleme dosyasinda olmayan pay XUTUM'a baglanir.
Eklenen sutunlar:
- piyasa_getiri, sektor_getiri, sektor_endeksi: bilgi. Gune ozgu getiriler o gun butun paylarda (sektorde) aynidir; model
  girdisi yapilmaz: pay gruplu dogrulamada etiketli gunler gun uzerinden taninabilir.
- fazla_getiri = getiri - piyasa_getiri, sektor_fazla_getiri = getiri - sektor_getiri: girdi olabilir.
Kullanim: python -I tespit/endeks_ozellikleri.py OZELLIKLER.parquet   (sutunlari ekleyip ayni dosyaya yazar)
"""
import datetime, glob, os, sys

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKLENEN = ["piyasa_getiri", "sektor_getiri", "sektor_endeksi", "fazla_getiri", "sektor_fazla_getiri"]


def endeks_kapanislari(aylar, kodlar):
    """{(tarih, endeks_kodu): gun sonu degeri} tablosu: satir tarih, sutun endeks kodu."""
    parca = []
    for ay in aylar:
        f = os.path.join(KOK, "veri", "gun-ici-endeks", f"PP_GUNICITUMENDEKS.M.{ay}.parquet")
        if not os.path.exists(f):
            continue
        t = pq.read_table(f, columns=["tarih", "zaman", "endeks_kodu", "deger"],
                          filters=[("endeks_kodu", "in", sorted(kodlar))])
        d = pd.DataFrame({"tarih": t["tarih"].to_pandas(), "zaman": pc.cast(t["zaman"], pa.int32()).to_numpy(),
                          "kod": t["endeks_kodu"].to_pandas(), "deger": t["deger"].to_numpy()})
        parca.append(d.sort_values(["tarih", "zaman"], kind="stable").groupby(["tarih", "kod"])["deger"].last())
    s = pd.concat(parca)
    k = s.unstack("kod").sort_index()
    k.index = pd.to_datetime(k.index)
    return k


def sektorler(aylar):
    """{ay (YYYYMM): {kod: (ana_sektor, sektor)}} degerleme dosyalarindan."""
    out = {}
    for f in sorted(glob.glob(os.path.join(KOK, "veri", "degerleme-orani", "degoran_M_*.parquet"))):
        d = pd.read_parquet(f, columns=["tur", "kod", "ana_sektor", "sektor"])
        d = d[d["tur"] == "pay"]
        out[os.path.basename(f)[10:16]] = dict(zip(d["kod"], zip(d["ana_sektor"], d["sektor"])))
    return out


if __name__ == "__main__":
    yol = sys.argv[1]
    T = pd.read_parquet(yol).drop(columns=EKLENEN, errors="ignore")
    E = pd.read_csv(os.path.join(KOK, "tespit", "sektor_endeks.csv"))
    esle = dict(zip(zip(E["ana_sektor"], E["sektor"]), E["endeks_kodu"]))
    aylar = sorted(T["tarih"].dt.strftime("%Y%m").unique())
    onceki = (pd.Period(aylar[0][:4] + "-" + aylar[0][4:], "M") - 1).strftime("%Y%m")
    K = endeks_kapanislari([onceki] + aylar, set(E["endeks_kodu"]) | {"XUTUM"})
    R = K.pct_change(fill_method=None)
    S = sektorler(aylar)
    sek_aylar = sorted(S)

    def sektor_endeksi(kod, ay):
        p = (pd.Period(ay[:4] + "-" + ay[4:], "M") - 1).strftime("%Y%m")
        aday = [a for a in sek_aylar if a <= p] or [a for a in sek_aylar if a <= ay]
        if not aday:
            return "XUTUM"
        s = S[aday[-1]].get(kod.split(".")[0])
        return esle.get(s, "XUTUM") if s else "XUTUM"

    cift = T[["islem_kodu"]].assign(ay=T["tarih"].dt.strftime("%Y%m")).drop_duplicates()
    harita = {(k, a): sektor_endeksi(k, a) for k, a in zip(cift["islem_kodu"], cift["ay"])}
    T["sektor_endeksi"] = [harita[(k, a)] for k, a in zip(T["islem_kodu"], T["tarih"].dt.strftime("%Y%m"))]
    T["piyasa_getiri"] = R["XUTUM"].reindex(T["tarih"]).to_numpy()
    uzun = R.stack().rename("g")
    T["sektor_getiri"] = uzun.reindex(pd.MultiIndex.from_arrays([T["tarih"], T["sektor_endeksi"]])).to_numpy()
    T["fazla_getiri"] = T["getiri"] - T["piyasa_getiri"]
    T["sektor_fazla_getiri"] = T["getiri"] - T["sektor_getiri"]
    T.to_parquet(yol)
    print("yazildi", yol, len(T), "pay-gun;", "piyasa_getiri bos", int(T["piyasa_getiri"].isna().sum()),
          "sektor_getiri bos", int(T["sektor_getiri"].isna().sum()))
    print(T["sektor_endeksi"].value_counts().head(12).to_string())
