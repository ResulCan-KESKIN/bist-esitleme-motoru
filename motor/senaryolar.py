"""Sentetik manipulasyon senaryolari (TASARIM.md 5; VI-104.1 Tebligi bentleri). Her uretici, verilen andaki
fiyat duzeyine gore sentetik olay listesi (YeniEmir / Iptal) uretir. Emir numaralari "SENT-<senaryo>-<n>" bicimindedir;
ayni senaryodaki emirler tek sentetik aktore aittir.

Fiyat duzeyi taban cizgisi oynatmasindan alinir (enjeksiyonsuz motor islemleri: son_fiyat). Fiyatlar fiyat adimina
yuvarlanir; sinirlari asan emirler motorun dogrulayicisinda reddedilir.
"""
import bisect

from tek_fiyat_algoritma import adim, yukari_adim, asagi_adim

from .emir import YeniEmir, Iptal, LIMIT

US = 1_000_000


def son_fiyat(islemler, zaman):
    """zaman'dan onceki son islem fiyati; islemler: zamana gore sirali Islem listesi."""
    z = [i.zaman for i in islemler]
    k = bisect.bisect_left(z, zaman)
    return islemler[k - 1].fiyat if k else None


def _adimla(p, tablo, yukari):
    return yukari_adim(p, tablo) if yukari else asagi_adim(p, tablo)


def _no(senaryo, n):
    return f"SENT-{senaryo}-{n}"


def kapanis_etkileme(kapanis_toplama_bas, tablo, ref, alis=True, miktar=10000, saniye_once=10, bant=0.03,
                     kapanis_eslestirme=None):
    """Kapanis fiyatini etkileme: kapanis emir toplamanin sonuna dogru, bandin ucundan buyuk bir emir.
    kapanis_eslestirme: veride kapanis eslestirme ani (emir bu andan saniye_once saniye once girilir)."""
    t = (kapanis_eslestirme or kapanis_toplama_bas + 240 * US) - saniye_once * US
    p = _adimla(ref * (1 + bant if alis else 1 - bant), tablo, not alis)
    return [YeniEmir(t, _no("kapanis", 1), alis, p, miktar, LIMIT)]


def yaniltici_emir(t, tablo, ref, yon_alis=False, katman=3, adim_uzak=2, miktar=20000, sure_sn=30,
                   karsi_miktar=500):
    """Yaniltici emir (spoofing/layering): bir tarafa en iyi fiyattan adim_uzak adim otede katman sayida buyuk emir,
    sure_sn sonra iptal; arada karsi tarafta kucuk bir agresif emir. yon_alis: yaniltici emirlerin yonu."""
    out, n = [], 0
    a = adim(ref, tablo)
    for k in range(katman):
        n += 1
        p = ref - (adim_uzak + k) * a if yon_alis else ref + (adim_uzak + k) * a
        out.append(YeniEmir(t + k, _no("yaniltici", n), yon_alis, p, miktar, LIMIT))
    n += 1
    # karsi tarafta (yaniltici emirlerin tersine) kucuk agresif emir: referansin bir adim otesinden
    pk = ref + a if yon_alis else ref - a
    out.append(YeniEmir(t + sure_sn * US // 2, _no("yaniltici", n), not yon_alis, pk, karsi_miktar, LIMIT))
    out += [Iptal(t + sure_sn * US + k, _no("yaniltici", k + 1)) for k in range(katman)]
    return out


def fiyat_yukseltme(t, tablo, ref, adim_sayisi=10, aralik_sn=20, miktar=1000):
    """Adim adim fiyat yukseltme (ramping): aralik_sn arayla, her biri bir oncekinden bir adim yuksek fiyatli
    agresif alis emirleri."""
    out, p = [], ref
    for k in range(adim_sayisi):
        p = p + adim(p, tablo)
        out.append(YeniEmir(t + k * aralik_sn * US, _no("yukseltme", k + 1), True, p, miktar, LIMIT))
    return out


def karsilikli_islem(t, tablo, ref, tekrar=5, aralik_sn=60, miktar=2000):
    """Karsilikli islem (wash trade): ayni sentetik aktorun ayni fiyattan satis ve hemen ardindan alis emri.
    Fiyat referansin bir adim ustu (satis once girer, alis onu karsilar; defterde daha iyi satis yoksa)."""
    out = []
    for k in range(tekrar):
        p = ref + adim(ref, tablo)
        tz = t + k * aralik_sn * US
        out.append(YeniEmir(tz, _no("karsilikli", 2 * k + 1), False, p, miktar, LIMIT))
        out.append(YeniEmir(tz + 1, _no("karsilikli", 2 * k + 2), True, p, miktar, LIMIT))
    return out
