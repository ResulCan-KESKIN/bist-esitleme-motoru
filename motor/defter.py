"""Surekli islem emir defteri: fiyat seviyeleri ve seviye icinde zaman onceligi (04-surekli-islem.md madde 15-16).

Her taraf icin fiyat -> {emir_no: Emir}; sozlugun ekleme sirasi zaman onceligidir. Seviye fiyatlari artan
sirali listede tutulur: alista en iyi fiyat listenin sonu, satista basidir.
"""
import bisect


class Defter:
    def __init__(self):
        self.seviye = {True: {}, False: {}}
        self.fiyatlar = {True: [], False: []}
        self.emirler = {}

    def ekle(self, e):
        """Emri fiyat seviyesinin sonuna ekler."""
        sv = self.seviye[e.alis]
        lv = sv.get(e.fiyat)
        if lv is None:
            lv = sv[e.fiyat] = {}
            bisect.insort(self.fiyatlar[e.alis], e.fiyat)
        lv[e.no] = e
        self.emirler[e.no] = e

    def cikar(self, no):
        e = self.emirler.pop(no, None)
        if e is None:
            return None
        sv = self.seviye[e.alis]
        lv = sv[e.fiyat]
        del lv[no]
        if not lv:
            del sv[e.fiyat]
            f = self.fiyatlar[e.alis]
            del f[bisect.bisect_left(f, e.fiyat)]
        return e

    def sona_al(self, e):
        """Emri kendi seviyesinin sonuna tasir (oncelik kaybi)."""
        lv = self.seviye[e.alis][e.fiyat]
        lv[e.no] = lv.pop(e.no)

    def en_iyi(self, alis):
        f = self.fiyatlar[alis]
        if not f:
            return None
        return f[-1] if alis else f[0]

    def ilk_emir(self, alis, fiyat):
        return next(iter(self.seviye[alis][fiyat].values()))

    def derinlik(self, alis, n=5):
        """En iyi n seviye: [(fiyat, gorunen toplam, emir sayisi)]."""
        f = self.fiyatlar[alis]
        sec = f[::-1][:n] if alis else f[:n]
        return [(p, sum(e.gorunen for e in self.seviye[alis][p].values()), len(self.seviye[alis][p])) for p in sec]
