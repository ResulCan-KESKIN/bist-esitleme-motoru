"""Motorun veri tipleri: emir, islem ve girdi olaylari.

Fiyatlar milli-TL (int; tek_fiyat_algoritma.py ile ayni olcek), miktarlar lot (int), zamanlar us (int).
Fiyat turu ve gecerlilik kodlari DataStore PP_GUNICIEMIR alanlarindaki degerlerdir.
"""
import itertools
from dataclasses import dataclass

LIMIT, PIYASA, PIYASADAN_LIMITE, DENGELEYICI = 1, 2, 3, 66   # emir_fiyat_turu
GUN, KIE = "DAY", "IMMEDIATE"                 # gecerlilik_turu; KIE = kalani iptal et

_SIRA = itertools.count(1)


def yeni_oncelik():
    """Artan oncelik numarasi; kucuk olan once gelir. Butun bolumlerde ortak sayac (bolum gecisinde sira korunur)."""
    return next(_SIRA)


@dataclass(slots=True)
class Emir:
    no: str
    alis: bool
    fiyat: int                 # piyasa ve piyasadan limite emirde 0
    kalan: int
    fiyat_turu: int = LIMIT
    gecerlilik: str = GUN
    tepe: int | None = None    # kismi gorunme kosullu emirde gorunen kisim buyuklugu
    gorunen: int = 0           # defterde eslesmeye acik miktar
    zaman: int = 0             # son oncelik zamani (bilgi amacli)
    oncelik: int = 0           # zaman onceligi sirasi (yeni_oncelik); defterde seviye ici sira bununla aynidir


@dataclass(slots=True)
class Islem:
    sira: int
    zaman: int
    aktif_no: str
    pasif_no: str
    alis_no: str
    satis_no: str
    fiyat: int
    adet: int


@dataclass(slots=True)
class YeniEmir:
    zaman: int
    no: str
    alis: bool
    fiyat: int
    miktar: int
    fiyat_turu: int = LIMIT
    gecerlilik: str = GUN
    tepe: int | None = None
    aciga: bool = False        # aciga satis (emir_turu 2)


@dataclass(slots=True)
class Degistir:
    """Fiyat ve/veya kalan miktar degisikligi. Kalan, fark olarak verilir: tekrar oynatmada motorun
    kalani gercekten saparsa degisiklik yine uygulanabilir."""
    zaman: int
    no: str
    fiyat: int
    kalan_farki: int
    gorunmeyen: bool = False   # fiyat ve kalan disinda bir alan degisti (veride AFK dolu emir); oncelik kaybolur


@dataclass(slots=True)
class Iptal:
    zaman: int
    no: str
