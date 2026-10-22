"""Tek fiyat (muzayede): emir toplama defteri, denge fiyati ve islem dagitimi (03-tek-fiyat.md Bolum B-E).

- Emir toplamada eslestirme yapilmaz; fiyat degisikligi ve kalan artisinda oncelik degisir (madde 19-20). Fiyat ve
  kalan disinda bir alan degisince de degisir (Degistir.gorunmeyen; 04 madde 24, veri).
- Denge fiyati: veri/araclar/tek_fiyat_algoritma.denge (Bolum D; Mart 2025 muzayedelerinin %99,96'si).
  Dengeleyici ve orta nokta emirleri fiyat hesabina girmez; fiyatsiz piyasadan limite piyasa emri sayilir.
- Dagitim: alis ve satis tarafi ayri ayri oncelik sirasina dizilir: piyasa ve piyasadan limite emirler zaman
  sirasiyla, sonra denge fiyatina esit ya da daha iyi limit emirler fiyat ve zaman sirasiyla (madde 48-51). Iki
  liste bastan yurunur; her adimda iki emrin kalanlarinin kucugu kadar islem yazilir (veri: THYAO.E 03.03.2025
  acilisinda 1.872 islemin tamami ayni sirayla).
- Dengeleyici emirler: once denge fiyatinda karsilanmayan karsi taraf emirleriyle, sonra birbirleriyle (52-55).
- Kalanlar: piyasa emri, KIE ve dengeleyici iptal edilir; piyasadan limite emir eslesme fiyatindan limit emre
  doner (05-emirler.md madde 14, 26, 36; 03 madde 55).
"""
import numpy as np
from tek_fiyat_algoritma import denge

from .emir import Emir, Islem, YeniEmir, Degistir, Iptal, LIMIT, PIYASA, PIYASADAN_LIMITE, DENGELEYICI, KIE, \
    yeni_oncelik


def _piyasa(e):
    return e.fiyat_turu in (PIYASA, PIYASADAN_LIMITE) and e.fiyat == 0


class TekFiyat:
    def __init__(self, emirler=()):
        self.emirler = {e.no: e for e in emirler}
        self.sayac = {}

    def _say(self, k):
        self.sayac[k] = self.sayac.get(k, 0) + 1

    def isle(self, o):
        """Emir toplama olayi; eslestirme yapilmaz."""
        if isinstance(o, YeniEmir):
            self.emirler[o.no] = Emir(o.no, o.alis, o.fiyat, o.miktar, o.fiyat_turu, o.gecerlilik, o.tepe,
                                      gorunen=o.miktar, zaman=o.zaman, oncelik=yeni_oncelik())
        elif isinstance(o, Degistir):
            e = self.emirler.get(o.no)
            if e is None:
                self._say("degistir_bulunamadi")
                return
            yeni = e.kalan + o.kalan_farki
            if yeni <= 0:
                del self.emirler[o.no]
                return
            if o.fiyat != e.fiyat or yeni > e.kalan or o.gorunmeyen:
                e.zaman, e.oncelik = o.zaman, yeni_oncelik()
            e.fiyat, e.kalan, e.gorunen = o.fiyat, yeni, yeni
        elif isinstance(o, Iptal):
            if self.emirler.pop(o.no, None) is None:
                self._say("iptal_bulunamadi")
        else:
            raise TypeError(type(o))

    def fiyat(self, tablo, taban=None, tavan=None, referans=None):
        """Denge fiyati hesabi (tek_fiyat_algoritma.denge sonucu)."""
        lim = [e for e in self.emirler.values() if e.fiyat_turu != DENGELEYICI and not _piyasa(e) and e.fiyat > 0]
        a = [e for e in lim if e.alis]
        s = [e for e in lim if not e.alis]
        piy_a = sum(e.kalan for e in self.emirler.values() if e.alis and _piyasa(e))
        piy_s = sum(e.kalan for e in self.emirler.values() if not e.alis and _piyasa(e))
        return denge(np.array([e.fiyat for e in a], dtype=np.int64), np.array([e.kalan for e in a], dtype=np.int64),
                     np.array([e.fiyat for e in s], dtype=np.int64), np.array([e.kalan for e in s], dtype=np.int64),
                     piy_a, piy_s, tablo, taban, tavan, referans)

    def eslestir(self, zaman, tablo, taban=None, tavan=None, referans=None):
        """Denge fiyatini belirler, islemleri dagitir. Donus: (denge sonucu, islemler, sonraki bolume kalan emirler
        oncelik sirasinda)."""
        sonuc = self.fiyat(tablo, taban, tavan, referans)
        p = sonuc.get("fiyat")
        islemler = []
        if p is not None:
            def uygun(alis):
                x = [e for e in self.emirler.values() if e.alis == alis and e.fiyat_turu != DENGELEYICI
                     and (_piyasa(e) or (e.fiyat >= p if alis else e.fiyat <= p))]
                return sorted(x, key=lambda e: (0, 0, e.oncelik) if _piyasa(e)
                              else (1, -e.fiyat if alis else e.fiyat, e.oncelik))
            A, S = uygun(True), uygun(False)
            self._dagit(A, S, p, zaman, islemler)
            dng = lambda alis: sorted((e for e in self.emirler.values() if e.alis == alis and e.fiyat_turu == DENGELEYICI),
                                      key=lambda e: e.oncelik)
            DA, DS = dng(True), dng(False)
            self._dagit([e for e in A if e.kalan], DS, p, zaman, islemler)
            self._dagit(DA, [e for e in S if e.kalan], p, zaman, islemler)
            self._dagit([e for e in DA if e.kalan], [e for e in DS if e.kalan], p, zaman, islemler)
        kalan = []
        for e in sorted(self.emirler.values(), key=lambda e: e.oncelik):
            if e.kalan == 0 or e.fiyat_turu in (PIYASA, DENGELEYICI) or e.gecerlilik == KIE:
                continue
            if e.fiyat_turu == PIYASADAN_LIMITE:
                if e.fiyat == 0:
                    if p is None:
                        continue
                    e.fiyat, e.oncelik = p, yeni_oncelik()
                e.fiyat_turu = LIMIT
            e.gorunen = min(e.tepe, e.kalan) if e.tepe else e.kalan
            kalan.append(e)
        kalan.sort(key=lambda e: e.oncelik)
        self.emirler = {}
        return sonuc, islemler, kalan

    def _dagit(self, A, S, p, zaman, islemler):
        i = j = 0
        while i < len(A) and j < len(S):
            a, s = A[i], S[j]
            q = min(a.kalan, s.kalan)
            if q > 0:
                islemler.append(Islem(len(islemler), zaman, "", "", a.no, s.no, p, q))
                a.kalan -= q
                s.kalan -= q
            if a.kalan == 0:
                i += 1
            if s.kalan == 0:
                j += 1
