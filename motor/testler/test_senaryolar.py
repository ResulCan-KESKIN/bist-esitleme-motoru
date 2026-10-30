"""Tarih parametresi olcum kontrolu ve yaniltici emir senaryosu."""
import os, sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor import parametreler, senaryolar
from motor.emir import YeniEmir, Iptal, LIMIT, PIYASADAN_LIMITE, KIE
from tek_fiyat_algoritma import TABLO7

US = 1_000_000


def test_olcum_kontrolu():
    """Olcum satiri bulunur; veri doneminde olcumsuz gun hata verir; donem disinda metin degeri kullanilir.
    Olcumsuz gun ornegi 2024-01-01: veri doneminin ilk gunu (resmi tatil); olcum satirlari ilk islem gununden (2024-01-02)
    baslar (28.10.2026'ya kadar 2024-07, 30.10.2026'ya kadar 2024-06-01 kullaniliyordu; o aylar olculdu)."""
    assert parametreler.deger("fiyat_marji", "2025-03-10", "Z") == 0.10
    assert parametreler.deger("fiyat_marji", "2025-04-15", "Z") == 0.10
    assert parametreler.deger("fiyat_marji", "2024-07-10", "Z") == 0.10
    assert parametreler.deger("fiyat_marji", "2024-03-15", "Z") == 0.10
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.deger("fiyat_marji", "2024-01-01", "Z")
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.satir("dk_yon", "2024-01-01", "Z")
    assert parametreler.deger("fiyat_marji", "2026-10-01", "Z") == 0.20
    assert parametreler.satir("kapanis_seansi_fiyat_bandi", "2025-04-15")   # veriden olculmeyen parametre
    # pazara uygulanmayan parametre (YIP'te devre kesici orani) None; uygulanan pazarda olcum eksikse hata yutulmaz
    assert parametreler.varsa("dk_tetikleme_orani", "2025-03-10", "W") is None
    assert parametreler.varsa("dk_tetikleme_orani", "2025-03-10", "Z")["deger"] == "0.05"
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.varsa("dk_yon", "2024-01-01", "Z")


def test_yaniltici_katmanlar_en_iyi_fiyata_gore():
    """Satis katmanlari en iyi satis fiyatinin 2, 3, 4 adim gerisinde (son islem fiyatina gore degil)."""
    t = 1000 * US
    ol = senaryolar.yaniltici_emir(t, TABLO7, 100_000, yon_alis=False, adim_uzak=2, en_iyi=(99_900, 100_300))
    katman = [o for o in ol if isinstance(o, YeniEmir) and not o.alis]
    assert [o.fiyat for o in katman] == [100_500, 100_600, 100_700]
    assert sum(isinstance(o, Iptal) for o in ol) == 3


def test_yaniltici_karsi_emir():
    """Karsi emir varsayilan olarak agresif (piyasadan limite, KIE); pasifte karsi tarafin en iyi fiyatindan limit."""
    t = 1000 * US
    k = [o for o in senaryolar.yaniltici_emir(t, TABLO7, 100_000, en_iyi=(99_900, 100_300)) if isinstance(o, YeniEmir) and o.alis]
    assert len(k) == 1 and k[0].fiyat_turu == PIYASADAN_LIMITE and k[0].gecerlilik == KIE
    k = [o for o in senaryolar.yaniltici_emir(t, TABLO7, 100_000, en_iyi=(99_900, 100_300), karsi_agresif=False)
         if isinstance(o, YeniEmir) and o.alis]
    assert k[0].fiyat_turu == LIMIT and k[0].fiyat == 99_900


def test_karsilikli_makasin_icinden():
    """Her tekrar kendi araliginda makasin en az iki adim acik oldugu ilk anda, en iyi alisin bir adim ustunden
    (makasin ici); aralikta makas hep tek adimsa aralik basinda son islem fiyatinin bir adim ustu."""
    t = 1000 * US
    defter = [(t - 5 * US, 0, 0, 99_900, 100_300), (t + 55 * US, 0, 0, 99_900, 99_950), (t + 70 * US, 0, 0, 99_900, 100_300),
              (t + 115 * US, 0, 0, 99_900, 99_950)]
    ol = senaryolar.karsilikli_islem(t, TABLO7, 100_000, tekrar=3, aralik_sn=60, defter=defter)
    assert [(o.zaman, o.alis, o.fiyat) for o in ol] == [
        (t, False, 99_950), (t + 1, True, 99_950),                          # makas acik: hemen
        (t + 70 * US, False, 99_950), (t + 70 * US + 1, True, 99_950),      # 60. sn'de makas tek adim: 70. sn beklenir
        (t + 120 * US, False, 100_100), (t + 120 * US + 1, True, 100_100)]  # aralikta hep tek adim: son islem + 1 adim


def test_katman_fiyatlari():
    """Satis: en iyi satistan 0, 1, 2 adim geride (adim 0,10 TL); alis: en iyi alistan 2, 3 adim geride (adim 0,05 TL)."""
    assert senaryolar.katman_fiyatlari(100_300, TABLO7, False, 0, 3) == [100_300, 100_400, 100_500]
    assert senaryolar.katman_fiyatlari(99_900, TABLO7, True, 2, 2) == [99_800, 99_750]


def test_bolum_bol_dolumdan_once_iptal():
    """Islem goren parca dolumdan tepki kadar once biter, bekleme sonra yeniden girilir; dolum girisle tepki arasindaysa
    parca hic girilmez; yeniden giris bitisten sonraya kalirsa yapilmaz; islem gormeyen parca degismez."""
    B = [("a", False, 100_500, 10, 0, 100), ("b", False, 100_600, 10, 0, 100), ("c", False, 100_700, 10, 0, 100),
         ("d", False, 100_800, 10, 0, 100)]
    yeni = senaryolar.bolum_bol(B, {"a": 50, "b": 3, "c": 95}, 5, 10, lambda no, alis, z, p: p + 1,
                                lambda no: no + "2")
    assert yeni == [("a", False, 100_500, 10, 0, 45), ("a2", False, 100_501, 10, 60, 100),
                    ("b2", False, 100_601, 10, 13, 100), ("c", False, 100_700, 10, 0, 90),
                    ("d", False, 100_800, 10, 0, 100)]


def test_plan_olaylari():
    """Her parca bir yeni emir ve bitiste iptal; karsi emir piyasadan limite KIE; olaylar zamana gore sirali."""
    ol = senaryolar.plan_olaylari([("x1", False, 100_500, 10, 5, 40)], [("x2", 20, True, 3)])
    assert [(type(o).__name__, o.zaman, o.no) for o in ol] == [("YeniEmir", 5, "x1"), ("YeniEmir", 20, "x2"),
                                                                ("Iptal", 40, "x1")]
    assert ol[1].fiyat_turu == PIYASADAN_LIMITE and ol[1].gecerlilik == KIE and ol[1].alis


def test_karsilikli_ayarli_degisken_aralik():
    """Tekrar k kendi araligi [zamanlar[k], zamanlar[k+1]) icinde makasin acik oldugu ilk anda; boy tekrar basina."""
    t = 1000 * US
    defter = [(t - 5 * US, 0, 0, 99_900, 100_300), (t + 10 * US, 0, 0, 99_900, 99_950), (t + 100 * US, 0, 0, 99_900, 100_300)]
    ol = senaryolar.karsilikli_islem_ayarli([t + 20 * US, t + 200 * US], [7, 9], [100_000, 100_000], TABLO7, defter)
    assert [(o.zaman, o.alis, o.fiyat, o.miktar) for o in ol] == [
        (t + 100 * US, False, 99_950, 7), (t + 100 * US + 1, True, 99_950, 7),
        (t + 200 * US, False, 99_950, 9), (t + 200 * US + 1, True, 99_950, 9)]


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_"):
            f()
            print("TAMAM", ad)
