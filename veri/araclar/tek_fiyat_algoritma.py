"""Tek fiyat (denge fiyati) algoritmasi - 03-tek-fiyat.md Bolum D, varyantlariyla.

Fiyatlar milli-TL (int). Defter: alis/satis icin (fiyat, miktar) dizileri; piyasa (ve fiyatsiz piyasadan
limite) emirleri ayrica toplam miktar olarak verilir. Dengeleyici emirler hesaplamaya girmez (madde 45).
"""
import numpy as np

# milli-TL; bant alt siniri dahil (02-fiyat.md Tablo-7 / Tablo-8)
TABLO7 = (np.array([0, 20000, 50000, 100000, 250000, 500000, 1000000, 2500000]),
          np.array([10, 20, 50, 100, 250, 500, 1000, 2500]))
TABLO8 = (np.array([0, 50000, 100000, 250000, 500000, 1000000, 2500000]),
          np.array([10, 20, 50, 100, 250, 500, 1000]))
TEK = (np.array([0]), np.array([10]))
GRUP_TABLO = {"EQT": TABLO7, "RGT": TABLO7, "ETF": TABLO8, "GMF": TABLO8, "GSF": TABLO8,
              "ECW": TEK, "EPW": TEK, "XCR": TEK, "EMS": TEK, "AOF": TEK}


def adim(p, tablo):
    bas, ad = tablo
    return int(ad[np.searchsorted(bas, p, side="right") - 1])


def yukari_adim(x, tablo):
    """x'ten buyuk ya da esit ilk gecerli fiyat."""
    a = adim(int(np.floor(x)), tablo)
    return int(-(-x // a) * a)


def asagi_adim(x, tablo):
    a = adim(int(np.floor(x)), tablo)
    return int((x // a) * a)


def fiyat_izgarasi(alt, ust, tablo):
    p, out = yukari_adim(alt, tablo), []
    while p <= ust:
        out.append(p)
        p += adim(p, tablo)
    return np.array(out, dtype=np.int64)


def denge(alis_f, alis_q, satis_f, satis_q, piy_alis, piy_satis, tablo, taban=None, tavan=None,
          referans=None):
    """Aday fiyatlar, adim adim eleme ve karar adimi.

    Donus: dict(fiyat (None = olusmaz), miktar, adim, adaylar, ...). Varyant sonuclari 'v_*' anahtarlarinda.
    """
    limit = np.concatenate([alis_f, satis_f])
    if len(limit) == 0:
        return {"fiyat": None, "miktar": 0, "adim": "limit_emir_yok"}
    lo, hi = int(limit.min()), int(limit.max())
    lo = lo - adim(max(lo - 1, 0), tablo)                   # Adim 6: en dusukten bir adim asagi
    hi = hi + adim(hi, tablo)                               # en yuksege bir adim yukari
    if taban is not None:
        lo = max(lo, taban)                                 # Adim 7
    if tavan is not None:
        hi = min(hi, tavan)
    if lo > hi:
        return {"fiyat": None, "miktar": 0, "adim": "aralik_bos"}
    P = fiyat_izgarasi(lo, hi, tablo)
    if len(P) == 0:
        return {"fiyat": None, "miktar": 0, "adim": "aralik_bos"}
    ai = np.argsort(alis_f); af, aq = alis_f[ai], alis_q[ai]
    si = np.argsort(satis_f); sf, sq = satis_f[si], satis_q[si]
    ac = np.concatenate([[0], np.cumsum(aq[::-1])])[::-1]   # ac[k] = sum aq[k:]
    sc = np.concatenate([[0], np.cumsum(sq)])               # sc[k] = sum sq[:k]
    D = piy_alis + ac[np.searchsorted(af, P, side="left")]  # alis >= p
    S = piy_satis + sc[np.searchsorted(sf, P, side="right")]  # satis <= p
    V = np.minimum(D, S)
    vmax = int(V.max())
    sonuc = {"vmax": vmax, "aday_alt": int(P[0]), "aday_ust": int(P[-1])}
    if vmax == 0:
        sonuc.update(fiyat=None, miktar=0, adim="eslesme_yok")
        return sonuc
    k1 = np.flatnonzero(V == vmax)                          # Adim 1
    art = np.abs(D - S)
    amin = art[k1].min()
    k2 = k1[art[k1] == amin]                                # Adim 2
    sonuc["n_adim1"], sonuc["n_adim2"] = len(k1), len(k2)
    sonuc["aday_fiyatlar"] = P[k2].tolist()
    sonuc["aday_fazla"] = (D[k2] - S[k2]).tolist()
    sonuc["toplam_alis"] = int(piy_alis + aq.sum())
    sonuc["toplam_satis"] = int(piy_satis + sq.sum())
    if len(k2) == 1:
        sonuc.update(fiyat=int(P[k2[0]]), miktar=vmax, adim="adim1" if len(k1) == 1 else "adim2")
        return sonuc
    fazla = D[k2] - S[k2]
    # Adim 3 (kullanici karari): aday seviyelerdeki kalan miktarin yonu. Yon karisiksa (alis ve satis
    # fazlasi birlikte; kaynakta tanimsiz) kullanici karari 21.10.2026: referans fiyata en yakin aday,
    # esitlik surerse esit uzak adaylarin orta noktasi (asagida).
    if (fazla > 0).all():
        y = "alis"
    elif (fazla < 0).all():
        y = "satis"
    elif (fazla == 0).all():
        y = "esit"
    else:
        y = "karisik"
    sonuc["yon"] = y
    if y == "alis":
        sonuc.update(fiyat=int(P[k2].max()), miktar=vmax, adim="adim3")
        return sonuc
    if y == "satis":
        sonuc.update(fiyat=int(P[k2].min()), miktar=vmax, adim="adim3")
        return sonuc
    # Adim 4: referans fiyata en yakin
    if referans is not None and referans > 0:
        uz = np.abs(P[k2] - referans)
        k4 = k2[uz == uz.min()]
        sonuc["n_adim4"] = len(k4)
        if len(k4) == 1:
            sonuc.update(fiyat=int(P[k4[0]]), miktar=vmax, adim="adim4_" + y)
            return sonuc
        sonuc["v_esit_uzak_yuksek"], sonuc["v_esit_uzak_dusuk"] = int(P[k4].max()), int(P[k4].min())
        if y == "karisik":
            # karisik yon (kullanici karari 21.10.2026): esitlik surerse esit uzak adaylarin orta noktasi
            ort = (int(P[k4].max()) + int(P[k4].min())) / 2
            a, b = asagi_adim(ort, tablo), yukari_adim(ort, tablo)
            sonuc.update(fiyat=int(b if (b - ort) <= (ort - a) else a), miktar=vmax, adim="adim4_esit_uzaklik_orta_karisik")
            return sonuc
        sonuc.update(fiyat=int(P[k4].max()), miktar=vmax, adim="adim4_esit_uzaklik_" + y)
        return sonuc
    # Adim 5: en yuksek ve en dusuk adayin ortalamasi, en yakin adima
    ort = (int(P[k2].max()) + int(P[k2].min())) / 2
    a, b = asagi_adim(ort, tablo), yukari_adim(ort, tablo)
    f = b if (b - ort) <= (ort - a) else a
    sonuc["v_orta_yukari"], sonuc["v_orta_asagi"] = b, a
    sonuc.update(fiyat=int(f), miktar=vmax, adim="adim5_" + y)
    return sonuc
