"""Tarih parametresi olcum kontrolu ve yaniltici emir senaryosu."""
import os, sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from motor import parametreler, senaryolar
from motor.emir import YeniEmir, Iptal, LIMIT, PIYASADAN_LIMITE, KIE
from tek_fiyat_algoritma import TABLO7

US = 1_000_000


def test_olcum_kontrolu():
    """Mart 2025 olcum satiri bulunur; veri doneminde olcumsuz gun hata verir; donem disinda metin degeri kullanilir."""
    assert parametreler.deger("fiyat_marji", "2025-03-10", "Z") == 0.10
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.deger("fiyat_marji", "2025-04-15", "Z")
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.satir("dk_yon", "2024-06-03", "Z")
    assert parametreler.deger("fiyat_marji", "2026-10-01", "Z") == 0.20
    assert parametreler.satir("kapanis_seansi_fiyat_bandi", "2025-04-15")   # veriden olculmeyen parametre
    # pazara uygulanmayan parametre (YIP'te devre kesici orani) None; uygulanan pazarda olcum eksikse hata yutulmaz
    assert parametreler.varsa("dk_tetikleme_orani", "2025-03-10", "W") is None
    assert parametreler.varsa("dk_tetikleme_orani", "2025-03-10", "Z")["deger"] == "0.05"
    with pytest.raises(parametreler.OlcumEksik):
        parametreler.varsa("dk_yon", "2025-04-15", "Z")


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


if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("test_"):
            f()
            print("TAMAM", ad)
