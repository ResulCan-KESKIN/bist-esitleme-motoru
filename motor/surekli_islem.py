"""Surekli islem eslestirmesi (04-surekli-islem.md, 05-emirler.md).

- Islem, defterde bekleyen (pasif) emrin fiyatindan olur (04 Acik sorular, madde 1/14-16 dogrulamasi).
- Limit emir karsi taraftaki uygun fiyatli seviyeleri tarar; kalani GUN ise deftere yazilir, KIE ise iptal edilir.
- Piyasa emri tum seviyeleri tarar, kalani iptal edilir (05 madde 7, 10; 04 madde 44).
- Piyasadan limite yalniz en iyi seviyeyle eslesir; kalani islem fiyatindan limit emir olarak yazilir, karsi taraf
  bossa iptal edilir (05 madde 22-23, 29-31; 04 madde 45).
- Oncelik: fiyat degisikligi ve kalan miktar artisinda kaybolur, azaltmada korunur (04 madde 20-22; veride M5).
  Fiyat ve kalan disinda bir alan degistiginde de kaybolur (Degistir.gorunmeyen; 04 madde 24, veri).
- Kismi gorunme: gorunen kisim bitince yeni kisim seviyenin sonuna gecer (04 madde 30). Gelen (agresif) emir
  tum kalaniyla eslesir; defterde yalnizca gorunen kisim eslesmeye aciktir. Ayni gelen emir ayni pasif emirle
  yenilemeden sonra tekrar eslesirse veride tek islem yazilir (ilk eslesmenin sirasinda, adetler toplanir).
"""
import collections

from .defter import Defter
from .emir import Emir, Islem, YeniEmir, Degistir, Iptal, LIMIT, PIYASA, PIYASADAN_LIMITE, KIE, yeni_oncelik


class SurekliIslem:
    def __init__(self, defter=None, sabit_fiyat=None, alt_sinir=None, ust_sinir=None):
        """sabit_fiyat: kapanis fiyatindan islemler bolumu; butun islemler bu fiyattan (03-tek-fiyat.md madde 86-88).
        alt_sinir / ust_sinir: pay bazinda devre kesici esigi; esigin otesindeki seviyelerle eslesilmez (06). Esigin
        otesinde eslesecek olan gelen emrin kalani (hic islem gormediyse tamami) iptal edilir ve devre kesici
        tetiklenir (dk_tetiklendi; veri Mart 2025: THYAO.E 19.03, KRGYO.E 03.03)."""
        self.defter = defter if defter is not None else Defter()
        self.sabit_fiyat = sabit_fiyat
        self.alt_sinir, self.ust_sinir = alt_sinir, ust_sinir
        self.dk_tetiklendi = False
        self._esik = False
        self.islemler = []
        self.sayac = collections.Counter()

    def isle(self, o):
        """Bir girdi olayini uygular; uretilen islemleri dondurur."""
        n = len(self.islemler)
        if isinstance(o, YeniEmir):
            self.yeni(o)
        elif isinstance(o, Degistir):
            self.degistir(o)
        elif isinstance(o, Iptal):
            self.iptal(o)
        else:
            raise TypeError(type(o))
        return self.islemler[n:]

    def yeni(self, o):
        e = Emir(o.no, o.alis, o.fiyat, o.miktar, o.fiyat_turu, o.gecerlilik, o.tepe, zaman=o.zaman)
        self._yerlestir(e, o.zaman)

    def degistir(self, o):
        d = self.defter
        e = d.emirler.get(o.no)
        if e is None:
            self.sayac["degistir_bulunamadi"] += 1
            return
        yeni_kalan = e.kalan + o.kalan_farki
        if yeni_kalan <= 0:
            d.cikar(e.no)
            self.sayac["degistir_kalan_sifir"] += 1
            return
        if o.fiyat != e.fiyat:
            d.cikar(e.no)
            e.fiyat, e.kalan = o.fiyat, yeni_kalan
            self._yerlestir(e, o.zaman)
        elif yeni_kalan > e.kalan or o.gorunmeyen:
            e.kalan = yeni_kalan
            e.gorunen = min(e.tepe, e.kalan) if e.tepe else e.kalan
            e.zaman, e.oncelik = o.zaman, yeni_oncelik()
            d.sona_al(e)
        else:
            e.kalan = yeni_kalan
            e.gorunen = min(e.gorunen, e.kalan)

    def iptal(self, o):
        if self.defter.cikar(o.no) is None:
            self.sayac["iptal_bulunamadi"] += 1

    def _yerlestir(self, e, zaman):
        self._esik = False
        ilk = self._eslestir(e, zaman)
        if self._esik:
            self.dk_tetiklendi = True
            self.sayac["dk_tetikleyen_iptal"] += 1
            return
        if e.kalan == 0 or e.gecerlilik == KIE or e.fiyat_turu == PIYASA:
            return
        if e.fiyat_turu == PIYASADAN_LIMITE:
            if ilk is None:
                return
            e.fiyat, e.fiyat_turu = ilk, LIMIT
        e.gorunen = min(e.tepe, e.kalan) if e.tepe else e.kalan
        e.zaman, e.oncelik = zaman, yeni_oncelik()
        self.defter.ekle(e)

    def _eslestir(self, e, zaman):
        """Gelen emri karsi tarafla eslestirir; ilk islem fiyatini (yoksa None) dondurur."""
        d = self.defter
        karsi = not e.alis
        ilk = None
        bu_olay = {}   # pasif emir -> islem; ayni pasif emirle tekrar eslesme tek islem yazilir (veri, kismi gorunme)
        while e.kalan > 0:
            p = d.en_iyi(karsi)
            if p is None:
                break
            if e.fiyat_turu == LIMIT and (p > e.fiyat if e.alis else p < e.fiyat):
                break
            if (self.alt_sinir is not None and p < self.alt_sinir) or (self.ust_sinir is not None and p > self.ust_sinir):
                self._esik = True
                break
            if e.fiyat_turu == PIYASADAN_LIMITE and ilk is not None and p != ilk:
                break
            if ilk is None:
                ilk = p
            pasif = d.ilk_emir(karsi, p)
            adet = min(e.kalan, pasif.gorunen)
            fiyat = self.sabit_fiyat if self.sabit_fiyat is not None else p
            onceki = bu_olay.get(pasif.no)
            if onceki is not None and onceki.fiyat == fiyat:
                onceki.adet += adet
            else:
                i = Islem(len(self.islemler), zaman, e.no, pasif.no,
                          e.no if e.alis else pasif.no, pasif.no if e.alis else e.no, fiyat, adet)
                self.islemler.append(i)
                bu_olay[pasif.no] = i
            e.kalan -= adet
            pasif.kalan -= adet
            pasif.gorunen -= adet
            if pasif.kalan == 0:
                d.cikar(pasif.no)
            elif pasif.gorunen == 0:
                pasif.gorunen = min(pasif.tepe, pasif.kalan)
                pasif.zaman, pasif.oncelik = zaman, yeni_oncelik()
                d.sona_al(pasif)
        return ilk
