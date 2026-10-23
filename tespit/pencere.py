"""5 dakikalik pencere tespiti (TASARIM.md 6.1: pay-pencere birimi).

Pencere ozellikleri motor ciktisindan (islemler) ve emir olaylarindan (veri satirlari + kabul edilen sentetik olaylar)
hesaplanir; enjeksiyonlu ve enjeksiyonsuz kosu ayni yolla olculur. Muzayede islemleri gerceklestigi pencereye duser
(kapanis muzayedesi 18:05 penceresi).
- Ozellikler: islem sayisi, hacim (lot), getiri (pencere son fiyati / onceki pencere son fiyati), aktif taraf
  dengesizligi, yeni emir, iptal, iptal orani, kisa omurlu uzak emir miktari payi (ozellikler.py tanimi), yeni limit
  emirlerde farkli fiyat kademesi sayisi, net agresif adim (surekli islemde ardisik islemlerde fiyati yukari iten
  agresif alis sayisi eksi asagi iten agresif satis sayisi; adim adim fiyat yukseltme / dusurme gostergesi), defter
  derinlik dengesizligi ve toplam derinlik (motor defterinden 10 sn'de bir: en iyi 5 seviyedeki gorunen alis ve satis
  miktari; dengesizlik (A - S)/(A + S) ortalamasi).
- Puanlar: ayni pay-gunun diger pencerelerine gore saglam Z (ortanca, 1,4826 x MAD); pencere puani en buyuk |z|.
  Kurallar (VI-104.1 md 5/1): a/b z(iptal_orani) ya da z(uzak_kisa_pay) >= ESIK; f |z(getiri)| >= ESIK ve
  |z(aktif_dengesizlik)| >= ESIK_2 ayni yonde, ya da |z(net_adim)| >= ESIK; d kapanis muzayedesi penceresinde
  |z(getiri)| >= ESIK. Bayraklar kural_ab, kural_f, kural_d sutunlarinda.
- Kapanis penceresi (kapanis_gecmisi): kapanis muzayedesi her gun ayni gunun diger pencerelerine gore uc degerdir;
  bu pencere payin onceki gunlerdeki kapanislarina gore puanlanir (kapanis fiyatinin AOF'den sapmasi, kapanis seansi
  hacim payi, kapanis oncesi getiri, kapanis muzayedesi sapmasi, kapanis emir toplama dengesizligi, son dakika payi;
  z, payin onceki en az 5 gunune gore). Kural d yontemler.kurallar ile aynidir.
"""
import os

import numpy as np
import pandas as pd

from ozellikler import UZAK_ADIM, KISA_SN, fiyat_adimi

PENCERE_US = int(os.environ.get("PENCERE_DK", "5")) * 60 * 1_000_000   # pencere uzunlugu (varsayilan 5 dk)
ESIK, ESIK_2 = 3.0, 2.0
OZ = ["islem_sayisi", "hacim", "getiri", "aktif_dengesizlik", "yeni", "iptal", "iptal_orani", "uzak_kisa_pay",
      "fiyat_kademesi", "net_adim", "derinlik_dengesizlik", "derinlik"]
LOG = {"islem_sayisi", "hacim", "yeni", "iptal", "fiyat_kademesi", "derinlik"}


def emir_olaylari(df, g=None):
    """Emir olay tablosu: zaman, sebep (6/5/1), limit, fiyat, miktar, uzak_kisa (yeni limit emirde). Veri satirlari
    (normal emir) + g verilirse kabul edilen sentetik olaylar."""
    d = df[df["emir_kategorisi"] == 1]
    seb = d["degisiklik_sebebi"]
    yeni = d[(seb == 6)]
    iptal_z = d[seb == 1].groupby("emir_no")["zaman"].min()
    dolu = set(d.loc[seb.isin([3, 13]), "emir_no"])
    sur = (yeni["seans"] == "P_SUREKLI_ISLEM") & (yeni["emir_fiyat_turu"] == 1) & (yeni["en_iyi_alis_fiyati"] > 0) \
        & (yeni["en_iyi_satis_fiyati"] > 0)
    en_iyi = np.where(yeni["alis"], yeni["en_iyi_alis_fiyati"], yeni["en_iyi_satis_fiyati"])
    with np.errstate(invalid="ignore", divide="ignore"):
        mesafe = np.where(yeni["alis"], en_iyi - yeni["fiyat"], yeni["fiyat"] - en_iyi) / fiyat_adimi(np.where(en_iyi > 0, en_iyi, 1))
    omur = iptal_z.reindex(yeni["emir_no"]).to_numpy() - yeni["zaman"].to_numpy()
    kisa = (omur <= KISA_SN * 1_000_000) & ~yeni["emir_no"].isin(dolu).to_numpy()
    E = pd.DataFrame({"zaman": d["zaman"].to_numpy(), "sebep": seb.to_numpy(), "limit": (d["emir_fiyat_turu"] == 1).to_numpy(),
                      "fiyat": d["fiyat_m"].to_numpy(), "miktar": d["emir_miktari"].to_numpy(), "surekli_limit": False,
                      "uzak_kisa": False})
    E = E[E["sebep"].isin([6, 5, 1])].copy()
    ix = E.index[E["sebep"] == 6]
    E.loc[ix, "surekli_limit"] = sur.to_numpy()
    E.loc[ix, "uzak_kisa"] = (sur.to_numpy() & (mesafe >= UZAK_ADIM - 1e-9) & kisa)
    if g is not None and g.kabul:
        from motor.emir import YeniEmir, Degistir, Iptal, LIMIT
        iptal = {}
        for o, b in g.kabul:
            if isinstance(o, Iptal) and o.no not in iptal:
                iptal[o.no] = o.zaman
        sdolu = {n for _, i in g.islemler for n in (i.alis_no, i.satis_no) if n in g.sentetik_nolar}
        ek = []
        for o, b in g.kabul:
            if isinstance(o, YeniEmir):
                sl, uk = False, False
                if b == "P_SUREKLI_ISLEM" and o.fiyat_turu == LIMIT and o.no in g.sentetik_en_iyi:
                    ea, es = g.sentetik_en_iyi[o.no]
                    if ea is not None and es is not None:
                        sl = True
                        ei = (ea if o.alis else es) / 1000
                        m = ((ei - o.fiyat / 1000) if o.alis else (o.fiyat / 1000 - ei)) / fiyat_adimi(ei)
                        uk = m >= UZAK_ADIM - 1e-9 and o.no in iptal and iptal[o.no] - o.zaman <= KISA_SN * 1_000_000 \
                            and o.no not in sdolu
                ek.append((o.zaman, 6, o.fiyat_turu == LIMIT, o.fiyat, o.miktar, sl, uk))
            elif isinstance(o, Degistir):
                ek.append((o.zaman, 5, True, o.fiyat, 0, False, False))
            else:
                ek.append((o.zaman, 1, True, 0, 0, False, False))
        E = pd.concat([E, pd.DataFrame(ek, columns=E.columns)], ignore_index=True)
    return E


def pencere_ozellikleri(g, E):
    """g: calistirilmis Gun; E: emir_olaylari. Donus: pencere basina ozellikler (index: pencere baslangici, us)."""
    I = pd.DataFrame([(i.zaman, i.fiyat, i.adet, b, (1 if i.aktif_no == i.alis_no else -1 if i.aktif_no == i.satis_no else 0))
                      for b, i in g.islemler], columns=["zaman", "fiyat", "adet", "bolum", "aktif"])
    I = I.sort_values("zaman", kind="stable")
    I["p"] = I["zaman"] // PENCERE_US * PENCERE_US
    sur = I["bolum"] == "P_SUREKLI_ISLEM"
    dp = I["fiyat"].where(sur).diff()
    I["adim"] = np.where(sur & (dp > 0) & (I["aktif"] == 1), 1, np.where(sur & (dp < 0) & (I["aktif"] == -1), -1, 0))
    E = E.assign(p=E["zaman"] // PENCERE_US * PENCERE_US)
    gI = I.groupby("p")
    W = pd.DataFrame({"islem_sayisi": gI.size(), "hacim": gI["adet"].sum(), "son": gI["fiyat"].last(),
                      "aktif_alis": I[I["aktif"] == 1].groupby("p")["adet"].sum(),
                      "aktif_satis": I[I["aktif"] == -1].groupby("p")["adet"].sum(),
                      "net_adim": gI["adim"].sum(),
                      "kapanis_muzayedesi": gI["bolum"].agg(lambda b: (b == "P_ESLESTIRME").any())})
    gE = E.groupby("p")
    W = W.join(pd.DataFrame({"yeni": gE["sebep"].agg(lambda s: (s == 6).sum()), "iptal": gE["sebep"].agg(lambda s: (s == 1).sum()),
                             "sl_miktar": E[E["surekli_limit"]].groupby("p")["miktar"].sum(),
                             "uk_miktar": E[E["uzak_kisa"]].groupby("p")["miktar"].sum(),
                             "fiyat_kademesi": E[(E["sebep"] == 6) & E["limit"]].groupby("p")["fiyat"].nunique()}), how="outer")
    O = pd.DataFrame(getattr(g, "defter_ornekleri", []) or [], columns=["zaman", "alis", "satis", "en_iyi_alis", "en_iyi_satis"])
    if len(O):
        O["p"] = O["zaman"] // PENCERE_US * PENCERE_US
        O["deng"] = (O["alis"] - O["satis"]) / (O["alis"] + O["satis"]).where(O["alis"] + O["satis"] > 0)
        O["toplam"] = O["alis"] + O["satis"]
        W = W.join(O.groupby("p").agg(derinlik_dengesizlik=("deng", "mean"), derinlik=("toplam", "mean")), how="outer")
    else:
        W["derinlik_dengesizlik"], W["derinlik"] = np.nan, np.nan
    W = W.sort_index()
    W["son"] = W["son"].ffill()
    W["getiri"] = np.log(W["son"] / W["son"].shift()).fillna(0)
    aa, asat = W["aktif_alis"].fillna(0), W["aktif_satis"].fillna(0)
    W["aktif_dengesizlik"] = (aa - asat) / (aa + asat).clip(lower=1)
    W["iptal_orani"] = W["iptal"].fillna(0) / W["yeni"].fillna(0).clip(lower=1)
    W["uzak_kisa_pay"] = W["uk_miktar"].fillna(0) / W["sl_miktar"].where(W["sl_miktar"] > 0)
    for c in ("islem_sayisi", "hacim", "yeni", "iptal", "fiyat_kademesi", "net_adim"):
        W[c] = W[c].fillna(0)
    W["kapanis_muzayedesi"] = W["kapanis_muzayedesi"].astype("boolean").fillna(False).astype(bool)
    return W[OZ + ["kapanis_muzayedesi"]]


KAPANIS_OZ = ["kapanis_aof_sapma", "kapanis_seansi_payi", "kapanis_oncesi_getiri", "kapanis_muzayede_sapma",
              "kapanis_toplama_dengesizlik", "kapanis_son_dakika_payi"]


def kapanis_gecmisi(W, gun_ozellik, gecmis, en_az=5):
    """Kapanis muzayedesi penceresinin puanini payin gecmis kapanislarina gore yeniden hesaplar.
    gun_ozellik: o gunun pay-gun ozellikleri (dict; motor_ozellikleri.satir); gecmis: payin onceki gunlerine ait
    pay-gun ozellik tablosu (ozellikler.parquet satirlari)."""
    W = W.copy()
    k = W["kapanis_muzayedesi"].to_numpy()
    if not k.any() or len(gecmis) < en_az:
        return W
    z = {}
    for c in KAPANIS_OZ:
        x = gecmis[c].dropna()
        ss = x.std()
        z[c] = (gun_ozellik.get(c, np.nan) - x.mean()) / ss if len(x) >= en_az and ss and ss > 0 else 0.0
        z[c] = 0.0 if not np.isfinite(z[c]) else z[c]
    puan = max(abs(v) for v in z.values())
    d = (abs(z["kapanis_aof_sapma"]) >= ESIK and z["kapanis_seansi_payi"] >= ESIK_2) or \
        (abs(z["kapanis_muzayede_sapma"]) >= ESIK and abs(z["kapanis_toplama_dengesizlik"]) >= ESIK_2 and
         np.sign(z["kapanis_muzayede_sapma"]) == np.sign(z["kapanis_toplama_dengesizlik"]))
    W.loc[k, "puan_zskor"] = puan
    W.loc[k, ["kural_ab", "kural_f"]] = False
    W.loc[k, "kural_d"] = d
    W.loc[k, "kural_sayisi"] = int(d)
    W.loc[k, "puan_kural"] = int(d) + puan / 1000
    for c in KAPANIS_OZ:
        W.loc[k, "z_kapanis_" + c] = z[c]
    return W


def puanla(W):
    """Ayni pay-gunun pencerelerine gore saglam z ve puanlar."""
    W = W.copy()
    for c in OZ:
        x = np.log1p(W[c].clip(lower=0)) if c in LOG else W[c]
        med = x.median()
        mad = (x - med).abs().median() * 1.4826
        if not mad or np.isnan(mad):
            mad = x.std() or np.nan
        W["z_" + c] = (x - med) / mad if mad and mad > 0 else 0.0
    zc = ["z_" + c for c in OZ]
    W["puan_zskor"] = W[zc].abs().max(axis=1).fillna(0)
    a_b = (W["z_iptal_orani"] >= ESIK) | (W["z_uzak_kisa_pay"].fillna(0) >= ESIK)
    f = ((W["z_getiri"].abs() >= ESIK) & (W["z_aktif_dengesizlik"].abs() >= ESIK_2) &
         (np.sign(W["z_getiri"]) == np.sign(W["z_aktif_dengesizlik"]))) | (W["z_net_adim"].abs() >= ESIK)
    d = W["kapanis_muzayedesi"] & (W["z_getiri"].abs() >= ESIK)
    W["kural_ab"], W["kural_f"], W["kural_d"] = a_b, f, d
    W["kural_sayisi"] = a_b.astype(int) + f.astype(int) + d.astype(int)
    W["puan_kural"] = W["kural_sayisi"] + W["puan_zskor"] / 1000
    return W
