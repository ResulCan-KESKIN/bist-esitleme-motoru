"""Sentetik manipulasyon senaryolari (TASARIM.md 5; VI-104.1 Tebligi bentleri). Her uretici, verilen andaki
fiyat duzeyine gore sentetik olay listesi (YeniEmir / Iptal) uretir. Emir numaralari "SENT-<senaryo>-<n>" bicimindedir;
ayni senaryodaki emirler tek sentetik aktore aittir.

Fiyat duzeyi taban cizgisi oynatmasindan alinir (enjeksiyonsuz motor islemleri: son_fiyat). Fiyatlar fiyat adimina
yuvarlanir; sinirlari asan emirler motorun dogrulayicisinda reddedilir.
"""
import bisect

from tek_fiyat_algoritma import adim, yukari_adim, asagi_adim

from .emir import YeniEmir, Iptal, LIMIT, PIYASADAN_LIMITE, KIE

US = 1_000_000


def son_fiyat(islemler, zaman):
    """zaman'dan onceki son islem fiyati; islemler: zamana gore sirali Islem listesi."""
    z = [i.zaman for i in islemler]
    k = bisect.bisect_left(z, zaman)
    return islemler[k - 1].fiyat if k else None


def en_iyi_fiyatlar(defter_ornekleri, zaman):
    """zaman'dan onceki son defter orneginden (en iyi alis, en iyi satis); Gun.defter_ornekleri (surekli islem)."""
    z = [o[0] for o in defter_ornekleri]
    k = bisect.bisect_right(z, zaman)
    return (defter_ornekleri[k - 1][3], defter_ornekleri[k - 1][4]) if k else (None, None)


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
                   karsi_miktar=500, en_iyi=None, karsi_agresif=True):
    """Yaniltici emir (spoofing/layering): yaniltici tarafta, o tarafin en iyi fiyatindan adim_uzak adim geride katman
    sayida buyuk emir, sure_sn sonra iptal; arada karsi tarafta kucuk bir emir. yon_alis: yaniltici emirlerin yonu.

    en_iyi: giris anindaki (en iyi alis, en iyi satis) (taban oynatmasinin defter orneklerinden: en_iyi_fiyatlar);
    yaniltici tarafta en iyi fiyat yoksa son islem fiyati (ref) kullanilir.
    Karsi emir: karsi_agresif ise piyasadan limite ve KIE (karsi taraftaki en iyi seviyeden hemen islem gorur, kalan iptal:
    yaniltici baskinin olusturdugu fiyattan yararlanma); degilse karsi tarafin en iyi fiyatindan pasif limit emir (fiyatin
    yaniltici baskiyla o seviyeye gelmesini bekler; en iyi fiyat yoksa ref'in bir adim berisi)."""
    out, n = [], 0
    en_iyi_alis, en_iyi_satis = en_iyi or (None, None)
    taban = (en_iyi_alis if yon_alis else en_iyi_satis) or ref
    a = adim(taban, tablo)
    for k in range(katman):
        n += 1
        p = taban - (adim_uzak + k) * a if yon_alis else taban + (adim_uzak + k) * a
        out.append(YeniEmir(t + k, _no("yaniltici", n), yon_alis, p, miktar, LIMIT))
    n += 1
    tk = t + sure_sn * US // 2
    if karsi_agresif:
        out.append(YeniEmir(tk, _no("yaniltici", n), not yon_alis, 0, karsi_miktar, PIYASADAN_LIMITE, KIE))
    else:
        pk = (en_iyi_satis if yon_alis else en_iyi_alis) or (ref + a if yon_alis else ref - a)
        out.append(YeniEmir(tk, _no("yaniltici", n), not yon_alis, pk, karsi_miktar, LIMIT))
    out += [Iptal(t + sure_sn * US + k, _no("yaniltici", k + 1)) for k in range(katman)]
    return out


def katman_dolan(g, katman=3):
    """Yaniltici emir katmanlarindan (SENT-yaniltici-1..katman) islem goren toplam miktar; temiz senaryoda 0."""
    nos = {_no("yaniltici", k + 1) for k in range(katman)}
    return sum(i.adet for _, i in g.islemler if i.alis_no in nos or i.satis_no in nos)


def fiyat_yukseltme(t, tablo, ref, adim_sayisi=10, aralik_sn=20, miktar=1000):
    """Adim adim fiyat yukseltme (ramping): aralik_sn arayla agresif alis emirleri. Emirler piyasadan limite ve KIE'dir:
    her biri en iyi satis seviyesinden islem gorur, kalan iptal edilir; ardisik emirler satis seviyelerini tuketerek
    fiyati yukari iter (ref yalniz arayuz uyumu icin; fiyat defterden belirlenir)."""
    return [YeniEmir(t + k * aralik_sn * US, _no("yukseltme", k + 1), True, 0, miktar, PIYASADAN_LIMITE, KIE)
            for k in range(adim_sayisi)]


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
