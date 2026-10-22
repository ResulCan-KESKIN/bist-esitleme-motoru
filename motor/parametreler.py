"""Tarihe bagli kural parametreleri (motor/tarih_parametreleri.csv; TASARIM.md 3.6).

Bir parametre icin tarih ve kapsam (pazar harfi) uyan satirlardan en ozeli secilir: iki ucu tarihli aralik,
sonra tek ucu tarihli, sonra tarihsiz (yururlukteki metin). Ayni ozellikte birden fazla satir varsa en dar aralik.
Kapsam metnindeki tek buyuk harfler pazar kodlaridir (Z Yildiz, N Ana, T Alt, W YIP, S POIP, K BYF, Q GSF, E emtia).
"""
import csv, datetime, os, re

DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarih_parametreleri.csv")
_satirlar = None


def _oku():
    global _satirlar
    if _satirlar is None:
        with open(DOSYA, encoding="utf-8") as f:
            _satirlar = list(csv.DictReader(f))
    return _satirlar


def satir(parametre, tarih, pazar=None):
    t = datetime.date.fromisoformat(str(tarih))
    aday = []
    for r in _oku():
        if r["parametre"] != parametre:
            continue
        bas = datetime.date.fromisoformat(r["baslangic"]) if r["baslangic"] else None
        bit = datetime.date.fromisoformat(r["bitis"]) if r["bitis"] else None
        if (bas and t < bas) or (bit and t > bit):
            continue
        if pazar is not None:
            harfler = set(re.findall(r"\b([A-Z])\b", r["kapsam"]))
            if harfler and pazar not in harfler:
                continue
        ozel = (bas is not None) + (bit is not None)
        genislik = ((bit or datetime.date.max) - (bas or datetime.date.min)).days
        aday.append((-ozel, genislik, r))
    if not aday:
        raise KeyError(f"{parametre} {tarih} {pazar}")
    return min(aday, key=lambda x: x[:2])[2]


def deger(parametre, tarih, pazar=None, tip=float):
    return tip(satir(parametre, tarih, pazar)["deger"])
