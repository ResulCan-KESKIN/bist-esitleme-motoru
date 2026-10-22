"""Surekli islem eslestirmesi testleri: Ek-18 ornekleri (04-surekli-islem.md Test ornekleri) ve oncelik kurallari.

Kullanim: python -I motor/testler/test_surekli_islem.py   (her test icin TAMAM/HATA yazar; pytest ile de calisir)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor.surekli_islem import SurekliIslem
from motor.emir import YeniEmir, Degistir, Iptal, LIMIT, PIYASA, PIYASADAN_LIMITE, KIE


def tl(x):
    return round(x * 1000)


def ek18_defteri():
    """Ek-18 2.2.2 / 3.2.2 baslangic defteri."""
    m = SurekliIslem()
    z = 0
    for alis, p, q in [(True, 10.50, 100), (True, 10.45, 90), (True, 10.40, 80),
                       (False, 11.00, 80), (False, 11.05, 90), (False, 11.10, 100)]:
        z += 1
        m.isle(YeniEmir(z, f"{'A' if alis else 'S'}{p:.2f}", alis, tl(p), q))
    return m


def defter(m, alis):
    return [(p / 1000, q) for p, q, _ in m.defter.derinlik(alis, 10)]


def test_ek18_piyasa_emri():
    m = ek18_defteri()
    isl = m.isle(YeniEmir(10, "P", True, 0, 150, PIYASA, KIE))
    assert [(i.fiyat / 1000, i.adet) for i in isl] == [(11.00, 80), (11.05, 70)]
    assert defter(m, False) == [(11.05, 20), (11.10, 100)]
    assert defter(m, True) == [(10.50, 100), (10.45, 90), (10.40, 80)]


def test_ek18_piyasadan_limite():
    m = ek18_defteri()
    isl = m.isle(YeniEmir(10, "PL", True, 0, 150, PIYASADAN_LIMITE))
    assert [(i.fiyat / 1000, i.adet) for i in isl] == [(11.00, 80)]
    assert defter(m, True) == [(11.00, 70), (10.50, 100), (10.45, 90), (10.40, 80)]
    assert defter(m, False) == [(11.05, 90), (11.10, 100)]


def test_piyasadan_limite_karsi_taraf_bos():
    m = SurekliIslem()
    assert m.isle(YeniEmir(1, "PL", True, 0, 10, PIYASADAN_LIMITE)) == []
    assert "PL" not in m.defter.emirler   # 04 madde 45: karsi tarafta emir yoksa iptal


def test_limit_kie_kalani_iptal():
    m = ek18_defteri()
    isl = m.isle(YeniEmir(10, "K", True, tl(11.05), 200, LIMIT, KIE))
    assert [(i.fiyat / 1000, i.adet) for i in isl] == [(11.00, 80), (11.05, 90)]
    assert "K" not in m.defter.emirler


def test_islem_pasif_fiyatindan():
    m = ek18_defteri()
    isl = m.isle(YeniEmir(10, "L", False, tl(10.40), 120))
    assert [(i.fiyat / 1000, i.adet, i.pasif_no) for i in isl] == [(10.50, 100, "A10.50"), (10.45, 20, "A10.45")]


def test_zaman_onceligi_ve_degisiklik():
    """04 madde 20-22: azaltmada oncelik korunur; artirma ve fiyat degisikliginde kaybolur."""
    m = SurekliIslem()
    for z, no in enumerate(["S1", "S2", "S3"], 1):
        m.isle(YeniEmir(z, no, False, tl(5.00), 10))
    m.isle(Degistir(4, "S1", tl(5.00), -5))    # azaltma: S1 basta kalir
    assert [i.pasif_no for i in m.isle(YeniEmir(5, "A1", True, tl(5.00), 5))] == ["S1"]
    m.isle(YeniEmir(6, "S1b", False, tl(5.00), 10))
    m.isle(Degistir(7, "S2", tl(5.00), +5))    # artirma: S2 sona gider
    assert [i.pasif_no for i in m.isle(YeniEmir(8, "A2", True, tl(5.00), 10))] == ["S3"]
    assert [i.pasif_no for i in m.isle(YeniEmir(9, "A3", True, tl(5.00), 25))] == ["S1b", "S2"]


def test_gorunmeyen_alan_degisikligi():
    """Fiyat ve kalan disinda bir alan degisince (veride AFK dolu emir) oncelik kaybolur (04 madde 24, veri)."""
    m = SurekliIslem()
    m.isle(YeniEmir(1, "S1", False, tl(5.00), 10))
    m.isle(YeniEmir(2, "S2", False, tl(5.00), 10))
    m.isle(Degistir(3, "S1", tl(5.00), 0, gorunmeyen=True))
    assert [i.pasif_no for i in m.isle(YeniEmir(4, "A", True, tl(5.00), 10))] == ["S2"]


def test_fiyat_degisikligi_agresif():
    m = ek18_defteri()
    isl = m.isle(Degistir(10, "A10.50", tl(11.00), 0))   # alis emri satis fiyatina cekilir
    assert [(i.fiyat / 1000, i.adet, i.aktif_no) for i in isl] == [(11.00, 80, "A10.50")]
    assert defter(m, True)[0] == (11.00, 20)


def test_iptal():
    m = ek18_defteri()
    m.isle(Iptal(10, "S11.00"))
    assert defter(m, False)[0] == (11.05, 90)
    m.isle(Iptal(11, "YOK"))
    assert m.sayac["iptal_bulunamadi"] == 1


def test_kismi_gorunme():
    """04 madde 30: gorunen kisim bitince yeni kisim seviyenin sonuna; ayni gelen emirle tekrar eslesme tek islem."""
    m = SurekliIslem()
    m.isle(YeniEmir(1, "G", False, tl(5.00), 300, tepe=100))
    m.isle(YeniEmir(2, "N", False, tl(5.00), 50))
    isl = m.isle(YeniEmir(3, "A", True, tl(5.00), 180))
    # G 100 -> yenilenir, N'nin arkasina gecer; N 50; G'den 30 daha (tek islem: 130)
    assert [(i.pasif_no, i.adet) for i in isl] == [("G", 130), ("N", 50)]
    assert m.defter.emirler["G"].kalan == 170 and m.defter.emirler["G"].gorunen == 70


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_") and callable(f):
            try:
                f()
                print("TAMAM", ad)
            except AssertionError as e:
                print("HATA ", ad, e)
