"""Gorsellestirme arayuzunun veri hazirligi (TASARIM.md 6.5); Streamlit'ten bagimsiz.

- Taban cizgisi (enjeksiyonsuz) ve enjeksiyonlu oynatma (motor/enjeksiyon.py ile ayni akis).
- Bolum bantlari: muzayede emir toplama, eslestirme, EBDKS durdurmasi (veriden).
- Dakikalik seriler ve Z-skor temel cizgisi (TASARIM.md 6.3): surekli islem dakikalarinda hacim ve |getiri| icin
  gunun ortalama ve standart sapmasina gore z; z >= ESIK uyari. Bu, tespit modulunun ilk temel cizgisidir; kural ve
  model uyarilari tespit modulu yazildikca eklenecektir.
"""
import glob, os, sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
from motor import veri, senaryolar
from motor.gun import Gun, kosular, kategori

GUNLUK = os.path.join(KOK, "veri", "gun-ici-emir", "gunluk")
ESIK = 3.0


def gunsonu_dosyasi(gun):
    return os.path.join(KOK, "veri", "gun-sonu-fiyat-hacim", f"PP_GUNSONUFIYATHACIM.M.{gun[:4]}{gun[5:7]}.parquet")


def gunler():
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(GUNLUK, "20*"))
                  if os.path.exists(gunsonu_dosyasi(os.path.basename(p))))


def siralar(gun):
    return sorted(k for k in veri._kod_dosyasi(GUNLUK, gun) if k.endswith(".E"))


def _islem_tablosu(g):
    rows = [(b, i.zaman, i.fiyat / 1000, i.adet, g.sentetik_mi(i)) for b, i in g.islemler]
    df = pd.DataFrame(rows, columns=["bolum", "zaman", "fiyat", "adet", "sentetik"])
    df["zaman"] = pd.to_datetime(df["zaman"], unit="us")
    return df.sort_values("zaman", kind="stable").reset_index(drop=True)


def bolum_bantlari(df):
    """Surekli islem disindaki bolumler: (ad, bas, bit) birlestirilmis bantlar."""
    out = []
    for seans, bas, bit in kosular(df):
        kat = kategori(seans)
        if kat == "eslestirme" and out:
            out[-1][2] = bit   # eslestirme, onceki emir toplama bandinin sonudur
        elif kat in ("toplama", "eslestirme"):
            ad = ("EBDKS durdurma" if seans.startswith("P_GECICI") else
                  "Devre kesici" if seans.startswith("P_DK_") else
                  "EBDKS tek fiyat" if seans.endswith("_EBDK") else
                  "Kapanış" if seans.startswith("P_KAPANIS") else "Müzayede")
            if out and out[-1][0] == ad:
                out[-1][2] = bit
            else:
                out.append([ad, bas, bit])
    return pd.DataFrame([(a, pd.to_datetime(b, unit="us"), pd.to_datetime(c, unit="us")) for a, b, c in out],
                        columns=["ad", "bas", "bit"])


def dakikalik(islemler):
    s = islemler[islemler["bolum"] == veri.SUREKLI]
    if s.empty:
        return pd.DataFrame(columns=["dakika", "hacim", "son", "getiri", "z_hacim", "z_getiri", "uyari"])
    m = s.set_index("zaman").resample("1min").agg({"adet": "sum", "fiyat": "last"}).dropna(subset=["fiyat"])
    m = m.rename(columns={"adet": "hacim", "fiyat": "son"})
    m["getiri"] = np.log(m["son"]).diff().fillna(0)

    def z(x):
        sd = x.std()
        return (x - x.mean()) / sd if sd and sd > 0 else x * 0
    m["z_hacim"], m["z_getiri"] = z(m["hacim"]), z(m["getiri"].abs())
    m["uyari"] = (m["z_hacim"] >= ESIK) | (m["z_getiri"] >= ESIK)
    return m.reset_index().rename(columns={"zaman": "dakika"})


def oynat(gun, kod, senaryo=None, saat=None, **param):
    """Donus: dict(taban, enjeksiyonlu, bantlar, dakika_taban, dakika_enj, reddedilen, olaylar, ozet)."""
    gunsonu = gunsonu_dosyasi(gun)
    df = veri.pay_gun_emirleri(GUNLUK, gun, kod)
    tepe = veri.tepe_tahmini(df)
    tb = Gun(df, gun, kod, gunsonu, tepe)
    tb.calistir()
    taban = _islem_tablosu(tb)
    out = dict(taban=taban, bantlar=bolum_bantlari(df), dakika_taban=dakikalik(taban), olaylar=[],
               enjeksiyonlu=None, dakika_enj=None, reddedilen=pd.DataFrame(columns=["zaman", "emir", "bolum", "sebep"]))
    if senaryo:
        sirali = sorted((i for _, i in tb.islemler), key=lambda i: i.zaman)
        if senaryo == "kapanis":
            kos = kosular(df)
            k = next(j for j, (s, _, _) in enumerate(kos) if s.startswith("P_KAPANIS_EMIR"))
            esl = next((b for s, b, _ in kos[k:] if s in veri.ESLESTIRME), None)
            ref = senaryolar.son_fiyat(sirali, kos[k][1])
            olaylar = senaryolar.kapanis_etkileme(kos[k][1], tb.tablo, ref, kapanis_eslestirme=esl, **param)
        else:
            t = int(pd.Timestamp(f"{gun} {saat}").value // 1000)
            ref = senaryolar.son_fiyat(sirali, t)
            uret = {"yaniltici": senaryolar.yaniltici_emir, "yukseltme": senaryolar.fiyat_yukseltme,
                    "karsilikli": senaryolar.karsilikli_islem}[senaryo]
            olaylar = uret(t, tb.tablo, ref, **param)
        ej = Gun(df, gun, kod, gunsonu, tepe)
        ej.calistir(olaylar)
        enj = _islem_tablosu(ej)
        out.update(enjeksiyonlu=enj, dakika_enj=dakikalik(enj), olaylar=olaylar,
                   reddedilen=pd.DataFrame([(pd.to_datetime(o.zaman, unit="us"), o.no, b, r) for o, b, r in ej.reddedilen],
                                           columns=["zaman", "emir", "bolum", "sebep"]))
    son = out["enjeksiyonlu"] if out["enjeksiyonlu"] is not None else taban
    kap = lambda d: d.loc[d["bolum"] != veri.KAPANIS_FIYATI, "fiyat"].iloc[-1] if len(d) else None
    out["ozet"] = dict(islem_taban=len(taban), kapanis_taban=kap(taban), islem=len(son), kapanis=kap(son),
                       sentetik_islem=int(son["sentetik"].sum()), sentetik_adet=int(son.loc[son["sentetik"], "adet"].sum()),
                       uyari=int(dakikalik(son)["uyari"].sum()))
    return out
