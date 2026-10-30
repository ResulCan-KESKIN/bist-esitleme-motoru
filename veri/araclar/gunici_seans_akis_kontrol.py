"""Gunluk emir verisinden islem sirasi bazinda seans bolumu dizileri (ardisik ayni bolum satirlari = bir kosu).

Emir satirlarinda seans, olayin oldugu andaki bolumdur; bolum gecis ani dogrudan yazilmaz, yalniz ilk/son
olay zamani gorulur. Cikti: kosular (tarih, islem_kodu, sira, seans, ilk, son, satir, sebep sayilari) ve
devre kesici olaylari (tetikleme oncesi son surekli satir, ilk DK satiri, ilk eslestirme satiri, surekliye donus).
GUN yerine ay (YYYY-MM) da verilebilir: o aydaki gunler islenir.
Kullanim: python -I gunici_seans_akis_kontrol.py GUNLUK_EMIR_KLASORU CIKTI [GUN|AY ...]
"""
import sys, os, glob
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

emir_dir, out = sys.argv[1:3]
secili = set(sys.argv[3:])
os.makedirs(out, exist_ok=True)
cols = ["islem_kodu", "emir_no", "emir_degistirilme_zamani", "seans", "degisiklik_sebebi", "fiyat", "alis_satis",
        "emir_fiyat_turu", "kalan_miktar", "guncelleme_no"]
kosu, dk = [], []
for gun in sorted(os.path.basename(p) for p in glob.glob(os.path.join(emir_dir, "20*"))):
    if secili and not any(gun.startswith(s) for s in secili):
        continue
    for f in sorted(glob.glob(os.path.join(emir_dir, gun, "*.parquet"))):
        df = pq.read_table(f, columns=cols).to_pandas()
        df["islem_kodu"] = df["islem_kodu"].astype(str)
        df["seans"] = df["seans"].astype(str)
        for kod, g in df.groupby("islem_kodu", sort=False):
            s = g["seans"].to_numpy()
            z = g["emir_degistirilme_zamani"].to_numpy()
            yeni = np.r_[True, s[1:] != s[:-1]]
            bas = np.flatnonzero(yeni)
            bit = np.r_[bas[1:], len(s)] - 1
            seb = g["degisiklik_sebebi"].to_numpy()
            for r, (a, b) in enumerate(zip(bas, bit)):
                sb = np.bincount(seb[a:b + 1], minlength=120)
                kosu.append((gun, kod, r, s[a], z[a], z[b], b - a + 1, int(sb[6]), int(sb[5]), int(sb[1]),
                             int(sb[3]), int(sb[9] + sb[34] + sb[116] + sb[117])))
            # pay bazinda devre kesici olaylari
            for r, a in enumerate(bas):
                if s[a] in ("P_DK_TEKFIY_EMIR_TPL", "P_DK_TEKFIY_EMR_TPL2") and a > 0 and s[a - 1] == "P_SUREKLI_ISLEM":
                    b = a
                    while b < len(s) and s[b] in ("P_DK_TEKFIY_EMIR_TPL", "P_DK_TEKFIY_EMR_TPL2"):
                        b += 1
                    esl = z[b] if b < len(s) and s[b].startswith("P_ESLESTIRME") else None
                    c = b
                    while c < len(s) and s[c].startswith("P_ESLESTIRME"):
                        c += 1
                    don = z[c] if c < len(s) else None
                    # tetikleme: DK'dan onceki ayni zaman damgali surekli satirlar
                    k = a - 1
                    tz = z[k]
                    tet = g.iloc[[i for i in range(max(0, a - 50), a) if z[i] == tz]]
                    dk.append(dict(tarih=gun, islem_kodu=kod, son_surekli=tz, ilk_dk=z[a], ilk_eslestirme=esl,
                                   sonraki_bolum=s[c] if c < len(s) else None, sonraki_ilk=don,
                                   tetik_sebepler=",".join(map(str, sorted(set(tet["degisiklik_sebebi"])))),
                                   tetik_fiyatlar=",".join(f"{x:g}" for x in sorted(set(tet["fiyat"])))))
        print(gun, os.path.basename(f), len(kosu), len(dk), flush=True)

pd.DataFrame(kosu, columns=["tarih", "islem_kodu", "sira", "seans", "ilk", "son", "satir", "yeni", "degisiklik",
                            "iptal", "islem", "sistem_iptal"]).to_parquet(os.path.join(out, "seans_kosulari.parquet"))
pd.DataFrame(dk).to_parquet(os.path.join(out, "devre_kesici_olaylari.parquet"))
print("bitti", len(kosu), len(dk))
