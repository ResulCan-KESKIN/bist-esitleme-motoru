"""Pay profili (senaryo-tasarimi.md 4): hisseye gore ayarli senaryo parametreleri icin payin onceki ONCEKI_GUN islem
gunundeki emir ve islem dagilimlari ile enjeksiyon anindan onceki defter. Yalniz gecmis kullanilir.

- Emir boyu: surekli islemde yeni limit emirlerin miktari (lot); yuzdelikler ve buyuk emirler (>= %90 yuzdelik).
- Buyuk emir uzakligi: buyuk emirlerin girildigi anda ayni taraftaki en iyi fiyata uzakligi, fiyat adimi cinsinden
  (veri satirindaki en iyi fiyat; ozellikler.uzak_kisa_omurlu ve veri/araclar/yaniltici_yerlesim.py ile ayni tanim);
  yalniz en iyi fiyat ya da gerisi (uzaklik >= 0).
- Islem boyu: surekli islemde islem miktari (alis tarafi satirlarinin eslesen miktari; islem dosyasiyla birebir:
  THYAO.E 10.03.2025'te 55.666 islem, toplam miktar ayni).
- Kapanis emir toplama: gun basina kapanis emir toplamada girilen yeni emir miktari; gunlerin ortancasi.
- Defter (defter_profili): taban oynatmanin defter orneklerinden, enjeksiyondan onceki DEFTER_DK dakikada makas (adim)
  ve ilk 5 kademe derinligi (ortanca).
Yedek: onceki gunlerde EN_AZ_EMIR'den az yeni limit emir varsa ayni gunun enjeksiyondan onceki satirlari eklenir
(yedek = 1); o da yetmezse profil None doner ve cagiran eski H tabanli boylara duser.
"""
import glob, os

import numpy as np

from motor import veri
from ozellikler import fiyat_adimi
from tek_fiyat_algoritma import adim

ONCEKI_GUN = 5
EN_AZ_EMIR = 50
DEFTER_DK = 30
US = 1_000_000


def onceki_gunler(gunluk, gun, n=ONCEKI_GUN):
    gunler = sorted(os.path.basename(p) for p in glob.glob(os.path.join(gunluk, "20*")))
    return [g for g in gunler if g < gun][-n:]


def satirlar(df, t_son=None):
    """Surekli islemde yeni limit emirlerin boyu ve uzakligi, alis tarafi islem satirlarinin miktari, kapanis emir
    toplamadaki yeni emir miktari. t_son verilirse yalniz bu andan onceki satirlar."""
    sur = df["seans"] == veri.SUREKLI
    if t_son is not None:
        sur &= df["zaman"] < t_son
    yeni = df[sur & df["kapsam"] & (df["degisiklik_sebebi"] == 6) & (df["emir_fiyat_turu"] == 1)]
    ok = ((yeni["en_iyi_alis_fiyati"] > 0) & (yeni["en_iyi_satis_fiyati"] > 0)).to_numpy()
    ei = np.where(yeni["alis"], yeni["en_iyi_alis_fiyati"], yeni["en_iyi_satis_fiyati"]).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        uz = np.where(yeni["alis"], ei - yeni["fiyat"], yeni["fiyat"] - ei) / fiyat_adimi(np.where(ei > 0, ei, 1))
    uz = np.where(ok, np.rint(uz), np.nan)
    isl = df.loc[sur & df["alis"] & (df["islem_numarasi"] != 0), "eslesen_miktar"].to_numpy()
    kap = df.loc[df["seans"].isin(veri.KAPANIS_TOPLAMA) & df["kapsam"] & (df["degisiklik_sebebi"] == 6), "emir_miktari"].sum()
    return yeni["emir_miktari"].to_numpy(), uz, isl, int(kap)


def profil(gunluk, gun, kod, df_gun=None, t=None):
    boy, uz, isl, kap = [], [], [], []
    gunler = onceki_gunler(gunluk, gun)
    for g in gunler:
        try:
            d = veri.pay_gun_emirleri(gunluk, g, kod)
        except ValueError:
            continue
        b, u, i, k = satirlar(d)
        boy.append(b), uz.append(u), isl.append(i), kap.append(k)
    yedek = 0
    if sum(len(b) for b in boy) < EN_AZ_EMIR and df_gun is not None and t is not None:
        b, u, i, _ = satirlar(df_gun, t)
        boy.append(b), uz.append(u), isl.append(i)
        yedek = 1
    B = np.concatenate(boy) if boy else np.array([])
    if len(B) < EN_AZ_EMIR:
        return None
    U, I = np.concatenate(uz), np.concatenate(isl)
    q50, q90, q99 = np.percentile(B, [50, 90, 99])
    buyuk = B >= q90
    Ub = U[buyuk]
    iq = np.percentile(I, [50, 90, 99]) if len(I) else [np.nan] * 3
    return dict(gun_sayisi=len(kap), yedek=yedek, emir_sayisi=len(B), emir_q50=float(q50), emir_q90=float(q90),
                emir_q99=float(q99), emir_max=float(B.max()), buyuk_boy=B[buyuk],
                buyuk_uzaklik=Ub[~np.isnan(Ub) & (Ub >= 0)].astype(int),
                islem_q50=float(iq[0]), islem_q90=float(iq[1]), islem_q99=float(iq[2]),
                islem_max=float(I.max()) if len(I) else np.nan, islem_boy=I,
                kapanis_toplama=float(np.median(kap)) if kap else np.nan)


def defter_profili(ornekler, t, tablo):
    """Enjeksiyondan onceki DEFTER_DK dakikadaki defter ornekleri (Gun.defter_ornekleri): makas (adim) ve ilk 5 kademe
    derinligi ortancasi. Ornek yoksa None."""
    bas = t - DEFTER_DK * 60 * US
    o = [x for x in ornekler if bas <= x[0] < t and x[3] and x[4]]
    if not o:
        return None
    return dict(makas=float(np.median([(x[4] - x[3]) / adim(x[3], tablo) for x in o])),
                derinlik_alis=float(np.median([x[1] for x in o])), derinlik_satis=float(np.median([x[2] for x in o])))
