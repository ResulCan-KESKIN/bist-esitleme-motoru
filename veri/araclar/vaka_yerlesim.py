"""Kademe emri (VI-104.1 md 5/1-b) nitelemeli SPK vakalarinda emir yerlesimi: ENSRI.E, VKFYO.E (B seviyesi).
Gruplar: etiket (B penceresi, 20 islem gunu), belirsiz (tedbirden onceki 2 is gunu; disarida), diger (verideki diger gunler).
Emir tanimi yaniltici_yerlesim.py ile ayni. Dosyalar yalniz ilgili payin satirlariyla okunur (bellek).
Kullanim: python -I vaka_yerlesim.py KOK CIKTI.parquet"""
import glob, os, sys, time

import numpy as np
import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

KOK, CIKTI = sys.argv[1], sys.argv[2]
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "tespit"))
from ozellikler import fiyat_adimi
import yontemler as y

sys.stdout.reconfigure(encoding="utf-8")
GUNLUK = os.path.join(KOK, "veri", "gun-ici-emir", "gunluk")
SUTUN = ["islem_kodu", "emir_no", "emir_degistirilme_zamani", "alis_satis", "emir_fiyat_turu", "emir_kategorisi",
         "degisiklik_sebebi", "emir_miktari", "fiyat", "seans", "en_iyi_alis_fiyati", "en_iyi_satis_fiyati"]
KODLAR = ["ENSRI.E", "VKFYO.E"]
e = y.etiketler(os.path.join(KOK, "veri", "etiketler", "vaka_pencere_dogrulama.csv"))
etiket = {(k, str(t)[:10]): s for k, t, s in zip(e["islem_kodu"], e["tarih"], e["seviye"])}


def emir_tablosu(d, gun):
    z = d["emir_degistirilme_zamani"].astype("int64")
    seb = d["degisiklik_sebebi"]
    gir = d[(seb == 6) & (d["seans"] == "P_SUREKLI_ISLEM") & (d["emir_fiyat_turu"] == 1)
            & (d["en_iyi_alis_fiyati"] > 0) & (d["en_iyi_satis_fiyati"] > 0)]
    if gir.empty:
        return None
    alis = (gir["alis_satis"] == "A").to_numpy()
    en_iyi = np.where(alis, gir["en_iyi_alis_fiyati"], gir["en_iyi_satis_fiyati"])
    mesafe = np.where(alis, en_iyi - gir["fiyat"], gir["fiyat"] - en_iyi) / fiyat_adimi(en_iyi)
    no = d["emir_no"]
    iptal = z[seb == 1].groupby(no[seb == 1]).min()
    dolu = set(no[seb.isin([3, 13])])
    omur = iptal.reindex(gir["emir_no"]).to_numpy() - z[gir.index].to_numpy()
    q = gir["emir_miktari"].astype(float)
    return pd.DataFrame({"tarih": gun, "kova": np.clip(np.rint(mesafe), 0, 7).astype(int), "miktar": q.to_numpy(),
                         "kisa": (omur <= 60_000_000) & ~gir["emir_no"].isin(dolu).to_numpy(),
                         "buyuk": (q >= q.quantile(0.99)).to_numpy()})


parca, t0 = [], time.time()
for gun in sorted(os.listdir(GUNLUK)):
    for f in sorted(glob.glob(os.path.join(GUNLUK, gun, "pay-*.parquet"))):
        kodlar = set(pc.unique(pq.read_table(f, columns=["islem_kodu"])["islem_kodu"]).to_pylist())
        for kod in KODLAR:
            if kod not in kodlar:
                continue
            d = pq.read_table(f, columns=SUTUN, filters=[("islem_kodu", "=", kod)]).to_pandas()
            d = d[d["emir_kategorisi"] == 1]
            for c in ("seans", "alis_satis"):
                d[c] = d[c].astype(str)
            x = emir_tablosu(d, gun)
            if x is not None:
                s = etiket.get((kod, gun))
                parca.append(x.assign(kod=kod, grup="etiket" if s == "B" else ("belirsiz" if s else "diger")))
    if gun.endswith(("-03", "-17")):
        print(gun, f"{time.time() - t0:.0f} sn", flush=True)
A = pd.concat(parca, ignore_index=True)
A.to_parquet(CIKTI)
print(A.groupby(["kod", "grup"])["tarih"].nunique().to_string())
