"""Motor ciktisindan pay-gun ozellikleri: ozellikler.py ile ayni tanimlar, enjeksiyonlu oynatma icin (TASARIM.md 6.3).

Emir akisi: gercek emir satirlari (veri) + motorun kabul ettigi sentetik olaylar (Gun.kabul). Islem ozellikleri motorun
urettigi islemlerden. Gun sonu bulteni alanlari (kapanis, AOF, kapanis seansi payi vb.) islemlerden yeniden hesaplanir;
bulten toplamlarindaki ozel islem bildirimleri motorda yoktur (fark kucuktur, dogrula() ile olculur).
"""
import os, sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor import veri
from motor.emir import YeniEmir, Degistir, Iptal, PIYASA, PIYASADAN_LIMITE, LIMIT, KIE

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ozellikler import ACILIS_TOPLAMA, KAPANIS_TOPLAMA, KUCUK_ISLEM_TL, UZAK_ADIM, KISA_SN, fiyat_adimi, uzak_kisa_omurlu, makas


def _emir_sayilari(df, kabul):
    d = df[df["emir_kategorisi"] == 1]
    seb = d["degisiklik_sebebi"]
    yeni = seb == 6
    acl, kap = d["seans"].isin(ACILIS_TOPLAMA), d["seans"].isin(KAPANIS_TOPLAMA)
    c = dict(yeni=int(yeni.sum()), degisiklik=int((seb == 5).sum()), iptal=int((seb == 1).sum()),
             piyasa=int((yeni & d["emir_fiyat_turu"].isin([2, 3])).sum()),
             kie=int((yeni & (d["gecerlilik_turu"] == "IMMEDIATE")).sum()),
             aciga=int((yeni & ((d["emir_turu"] & 2) != 0)).sum()), afk=int((yeni & (d["afk"] == "E")).sum()),
             acilis_yeni=int((yeni & acl).sum()), acilis_iptal=int(((seb == 1) & acl).sum()),
             kapanis_yeni=int((yeni & kap).sum()), kapanis_degisiklik=int((seb.isin([1, 5]) & kap).sum()))
    fiyatlar = set(d.loc[yeni & (d["emir_fiyat_turu"] == 1), "fiyat_m"])
    for o, bolum in kabul:
        if isinstance(o, YeniEmir):
            c["yeni"] += 1
            c["piyasa"] += o.fiyat_turu in (PIYASA, PIYASADAN_LIMITE)
            c["kie"] += o.gecerlilik == KIE
            c["aciga"] += bool(o.aciga)
            c["acilis_yeni"] += bolum in ACILIS_TOPLAMA
            c["kapanis_yeni"] += bolum in KAPANIS_TOPLAMA
            if o.fiyat_turu == LIMIT:
                fiyatlar.add(o.fiyat)
        elif isinstance(o, Degistir):
            c["degisiklik"] += 1
            c["kapanis_degisiklik"] += bolum in KAPANIS_TOPLAMA
        elif isinstance(o, Iptal):
            c["iptal"] += 1
            c["acilis_iptal"] += bolum in ACILIS_TOPLAMA
            c["kapanis_degisiklik"] += bolum in KAPANIS_TOPLAMA
    c["fiyat_kademesi"] = len(fiyatlar)
    return c


def _uzak_kisa(g, df):
    """Kisa omurlu uzak emir payi: veri emirleri (ozellikler.uzak_kisa_omurlu) + kabul edilen sentetik emirler (giris
    anindaki en iyi fiyat motor defterinden)."""
    d = df[df["emir_kategorisi"] == 1].assign(islem_kodu="x")
    v = uzak_kisa_omurlu(d)
    pay, payda = (float(v["uzak_kisa"].sum()), float(v["surekli_yeni_miktar"].sum())) if len(v) else (0.0, 0.0)
    iptal = {}
    for o, b in g.kabul:
        if isinstance(o, Iptal) and o.no not in iptal:
            iptal[o.no] = o.zaman
    dolu = {n for _, i in g.islemler for n in (i.alis_no, i.satis_no) if n in g.sentetik_nolar}
    for o, b in g.kabul:
        if not (isinstance(o, YeniEmir) and b == veri.SUREKLI and o.fiyat_turu == LIMIT and o.no in g.sentetik_en_iyi):
            continue
        ea, es = g.sentetik_en_iyi[o.no]
        if ea is None or es is None:
            continue
        en_iyi = (ea if o.alis else es) / 1000
        mesafe = ((en_iyi - o.fiyat / 1000) if o.alis else (o.fiyat / 1000 - en_iyi)) / fiyat_adimi(en_iyi)
        kisa = o.no in iptal and iptal[o.no] - o.zaman <= KISA_SN * 1_000_000 and o.no not in dolu
        payda += o.miktar
        pay += o.miktar if (mesafe >= UZAK_ADIM - 1e-9 and kisa) else 0
    m = makas(d)
    return (pay / payda if payda else np.nan), (float(m.iloc[0]) if len(m) else np.nan)


def satir(g, df, gs_satir):
    """g: calistirilmis Gun; df: veri.pay_gun_emirleri; gs_satir: ozellikler.gunsonu_ozellikleri satiri (Series)."""
    c = _emir_sayilari(df, g.kabul)
    y = max(c["yeni"], 1)
    I = [(b, i) for b, i in g.islemler]
    fiyat = np.array([i.fiyat / 1000 for _, i in I])
    adet = np.array([i.adet for _, i in I])
    bolum = np.array([b for b, _ in I])
    hacim = fiyat * adet
    baz = gs_satir["baz"]
    sur = bolum == veri.SUREKLI
    out = gs_satir[["pazar", "bist100", "piyasa_yapici", "brut_takas", "ozsermaye", "baz"]].to_dict()
    kapanis = fiyat[-1] if len(I) else np.nan
    if len(I):
        sira = np.argsort([i.zaman for _, i in I], kind="stable")
        kapanis = fiyat[sira][-1]
    toplam_adet = adet.sum()
    vwap = hacim.sum() / toplam_adet if toplam_adet else np.nan
    acilis = next((s.get("fiyat") for M, b, s in g.muzayedeler if s.get("fiyat") is not None), None)
    sur_isl = [i for b, i in I if b == veri.SUREKLI]
    aa = sum(i.adet for i in sur_isl if i.aktif_no == i.alis_no)
    asat = sum(i.adet for i in sur_isl if i.aktif_no == i.satis_no)
    zaman_1745 = None
    if sur_isl:
        gun0 = pd.Timestamp(pd.Timestamp(sur_isl[0].zaman, unit="us").date())
        zaman_1745 = int((gun0 + pd.Timedelta(hours=17, minutes=45)).value // 1000)
    son = sur_isl[-1].fiyat / 1000 if sur_isl else np.nan
    once = [i.fiyat / 1000 for i in sur_isl if i.zaman < zaman_1745] if sur_isl else []
    # kapanis muzayedesi: gunun son eslestirme bolumu islemleri (acilis da P_ESLESTIRME; son muzayedeyi ayir)
    son_muz = next(((M, b) for M, b, s in reversed(g.muzayedeler) if b == "P_ESLESTIRME"), None)
    kap_seans = np.array([b == "P_ESLESTIRME" and son_muz is not None and i.zaman == son_muz[0] for b, i in I]) \
        if len(I) else np.array([], dtype=bool)
    out.update(
        kapanis=kapanis, getiri=kapanis / baz - 1 if baz else np.nan,
        aralik=(fiyat.max() - fiyat.min()) / baz if len(I) and baz else np.nan,
        hacim_tl=hacim.sum(), kapanis_aof_sapma=kapanis / vwap - 1 if vwap else np.nan,
        acilis_sapma=(acilis / 1000) / baz - 1 if acilis and baz else np.nan,
        kapanis_seansi_payi=adet[kap_seans].sum() / toplam_adet if toplam_adet else np.nan,
        kfi_payi=adet[bolum == veri.KAPANIS_FIYATI].sum() / toplam_adet if toplam_adet else np.nan,
        emir_yeni=c["yeni"], emir_degisiklik=c["degisiklik"], emir_iptal=c["iptal"],
        iptal_orani=c["iptal"] / y, degisiklik_orani=c["degisiklik"] / y, piyasa_payi=c["piyasa"] / y,
        kie_payi=c["kie"] / y, aciga_payi=c["aciga"] / y, afk_payi=c["afk"] / y, fiyat_kademesi=c["fiyat_kademesi"],
        acilis_iptal_orani=c["acilis_iptal"] / max(c["acilis_yeni"], 1),
        kapanis_degisiklik_yogunlugu=c["kapanis_degisiklik"] / max(c["kapanis_yeni"], 1),
        islem_sayisi=len(I), aktif_dengesizlik=(aa - asat) / max(aa + asat, 1),
        kucuk_islem_payi=(sum(1 for i in sur_isl if i.fiyat / 1000 * i.adet < KUCUK_ISLEM_TL) / len(sur_isl)) if sur_isl else np.nan,
        kapanis_oncesi_getiri=(son / once[-1] - 1) if once else np.nan,
        emir_islem_orani=c["yeni"] / max(len(I), 1),
    )
    out["kisa_omurlu_uzak_pay"], out["makas"] = _uzak_kisa(g, df)
    from kapanis_ozellikleri import motor_kapanis
    out.update(motor_kapanis(g, df))
    return out
