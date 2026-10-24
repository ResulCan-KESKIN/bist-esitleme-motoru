"""Tarihe bagli kural parametreleri (motor/tarih_parametreleri.csv; TASARIM.md 3.6).

Bir parametre icin tarih ve kapsam (pazar harfi) uyan satirlardan en ozeli secilir: iki ucu tarihli aralik,
sonra tek ucu tarihli, sonra tarihsiz (yururlukteki metin). Ayni ozellikte birden fazla satir varsa en dar aralik.
Kapsam metnindeki tek buyuk harfler pazar kodlaridir (Z Yildiz, N Ana, T Alt, W YIP, S POIP, K BYF, Q GSF, E emtia).

Olcum kontrolu: bir parametre o pazar icin veriden olculuyorsa (kapsami pazari iceren en az bir tarihli satirinin
kaynagi "veri" ile baslar), veri donemindeki (VERI_DONEMI) bir gun icin secilen satir veriden degilse OlcumEksik hatasi
verilir. Boylece yeni bir ayin parametresi olculmeden motor sessizce yururlukteki metin degerine (or. marj %20,
devre kesici iki yonde) dusmez. Pazara hic uygulanmayan parametrede (or. YIP'te devre kesici orani) KeyError verilir.
"""
import csv, datetime, os, re

DOSYA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarih_parametreleri.csv")
VERI_DONEMI = (datetime.date(2024, 6, 1), datetime.date(2025, 5, 31))   # DataStore gun ici verisi (CLAUDE.md)
_satirlar = None


class OlcumEksik(KeyError):
    pass


def _veriden(r):
    return r["kaynak"].startswith("veri")


def _kapsamda(r, pazar):
    if pazar is None:
        return True
    harfler = set(re.findall(r"\b([A-Z])\b", r["kapsam"]))
    return not harfler or pazar in harfler


def olculen(parametre, pazar=None):
    """Parametre bu pazar icin veriden olculuyor mu: kapsami pazari iceren en az bir tarihli satirinin kaynagi veri."""
    return any(r["parametre"] == parametre and (r["baslangic"] or r["bitis"]) and _veriden(r) and _kapsamda(r, pazar)
               for r in _oku())


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
        if r["parametre"] != parametre or not _kapsamda(r, pazar):
            continue
        bas = datetime.date.fromisoformat(r["baslangic"]) if r["baslangic"] else None
        bit = datetime.date.fromisoformat(r["bitis"]) if r["bitis"] else None
        if (bas and t < bas) or (bit and t > bit):
            continue
        ozel = (bas is not None) + (bit is not None)
        genislik = ((bit or datetime.date.max) - (bas or datetime.date.min)).days
        aday.append((-ozel, genislik, r))
    donemde = VERI_DONEMI[0] <= t <= VERI_DONEMI[1] and olculen(parametre, pazar)
    if not aday:
        raise (OlcumEksik if donemde else KeyError)(f"{parametre} {tarih} {pazar}: uygun satir yok")
    r = min(aday, key=lambda x: x[:2])[2]
    if donemde and not _veriden(r):
        raise OlcumEksik(f"{parametre} {tarih} {pazar}: veri doneminde olcum satiri yok (secilen: {r['kaynak']}); "
                         f"tarih_parametreleri.csv'ye bu gunu kapsayan olcum satiri eklenmeli")
    return r


def deger(parametre, tarih, pazar=None, tip=float):
    return tip(satir(parametre, tarih, pazar)["deger"])


def varsa(parametre, tarih, pazar=None):
    """satir() ya da (parametre bu pazara / tarihe uygulanmiyorsa) None. OlcumEksik yutulmaz: olculmesi gereken
    parametre eksikse motor durur."""
    try:
        return satir(parametre, tarih, pazar)
    except OlcumEksik:
        raise
    except KeyError:
        return None
