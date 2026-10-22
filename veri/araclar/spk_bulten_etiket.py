#!/usr/bin/env python3
"""SPK bültenlerinden manipülasyon vaka/olay tablosu çıkarır.

Kurallar: veri/etiketler/etiket-cikarim-kurallari.md (v1, kural numaraları yorumlarda).
Kullanım: python spk_bulten_etiket.py [--bulten-dir DIR] [--cikti-dir DIR] [--onbellek DIR]
Girdi PDF'leri güvenilmez veri sayılır: yalnızca metin çıkarılır, hiçbir şey çalıştırılmaz.
"""
import argparse
import csv
import datetime as dt
import io
import os
import re
import sys
from pathlib import Path

import pdfplumber

KOK = Path(__file__).resolve().parents[2]
PENCERE = (dt.date(2024, 6, 1), dt.date(2025, 5, 31))
B_ONCESI_GUN = 60  # seviye B için başlangıç belirsizliği üst sınırı (N=40 işlem günü ≈ 60 takvim günü)

AYLAR = {"ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "haziran": 6, "temmuz": 7,
         "ağustos": 8, "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12}
AY_RE = "|".join(AYLAR)
TARIH = r"\d{2}[./]\d{2}[./]\d{4}"

KOD_STOP = {"SPK", "AŞ", "TAŞ", "KAP", "TL", "BIST", "MKK", "TCKN", "İPC", "IPC", "SPKN", "SARL", "AO",
            "ŞİRKET", "SIRKET", "BYF", "NOT", "KGK", "TMS", "TFRS", "VUK", "TCK", "BDS", "TBB"}
ADLI_BUYUK_STOP = {"AŞ", "TAŞ", "AO", "SARL", "A.Ş.", "KAP", "SPK", "TL", "MKK", "BIST", "GYO", "A.Ş"}

# kural 4: hukuki dayanak
DAYANAK = [
    r"VI-104\.1", r"V-101\.1", r"SPKn?[’'`]?nun\s+(?:\(SPKn\)\s*)?10[47]\b", r"\b107\s*(?:nci|inci|ncı)\b",
    r"\b107/\d", r"\b104\s*(?:üncü|uncu|ncü)\b", r"\b104\s+(?:veya|ve)\s+107", r"107/\d\s+(?:veya|ve)\s+104",
    r"Piyasa\s+Dolandırıcılığı\s+suçu", r"Piyasa\s+Bozucu\s+Eylemler",
]
DAYANAK_RE = re.compile("|".join(DAYANAK), re.I)

BASLIK_C = re.compile(r"SUÇ\s+DUYURUSU,\s*İDARİ\s+PARA\s+CEZASI", re.I)
BASLIK_DUYURU = re.compile(r"DUYURU\s+VE\s+İLKE\s+KARARLARI", re.I)
UST_BASLIK = re.compile(r"^\s*([A-ZÇĞİÖŞÜ])\.?\s+[A-ZÇĞİÖŞÜ]{3}")  # "A DUYURU…" (nokta unutulmuş, 2026-13)
HARF_MADDE = re.compile(r"^\s*([a-zçğıöşü])\)\s+\S")
NUM_MADDE = re.compile(r"^\s*(\d{1,2})\.\s+\S")
ALT_BASLIK_ATLA = re.compile(r"^\s*\d\.\s*(İdari Para Cezaları|Suç Duyuruları|Diğer Yaptırım|Lisans ve Yetki)", re.I)


def tr_upper_ok(s):
    return s == s.upper()


def parse_tarih(s):
    g, a, y = re.split(r"[./]", s)
    try:
        return dt.date(int(y), int(a), int(g))
    except ValueError:
        return None


def maskele(s):
    """Kural 17: kişi adlarını alıntıdan çıkar (Ad SOYAD kalıbı)."""
    def sub(m):
        last = m.group(0).split()[-1]
        if last.upper() in ADLI_BUYUK_STOP or last in ADLI_BUYUK_STOP:
            return m.group(0)
        return "[KİŞİ]"
    s = re.sub(r"\b(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+){1,3}[A-ZÇĞİÖŞÜ]{2,}\b", sub, s)
    # maskeli TCKN'nin hemen öncesindeki büyük harfle başlayan 1-4 sözcük kişi adıdır ("FEVZİ SARGIN 36*******00")
    s = re.sub(r"(?:\b[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜa-zçğıöşü’'.\-]*\s+){1,4}(?=\d{2}\*{5,}\d{2})", "[KİŞİ] ", s)
    return re.sub(r"(?:\[KİŞİ\]\s*){2,}", "[KİŞİ] ", s)


def metin_cikar(pdf_yolu):
    sayfalar = []
    with pdfplumber.open(pdf_yolu) as p:
        for pg in p.pages:
            sayfalar.append(pg.extract_text() or "")
    return sayfalar


def bulten_adi(yol):
    m = re.search(r"(\d{4})[- ](\d+)\.pdf$", yol.name, re.I)
    return f"{m.group(1)}-{int(m.group(2))}" if m else yol.stem


def bulten_ust_bilgi(ilk_sayfa):
    m = re.search(r"(\d{4}/\d+)\s+(\d{2}/\d{2}/\d{4})", ilk_sayfa[:900])
    if not m:
        return "", None
    yil, sira = m.group(1).split("/")
    return f"{yil}/{int(sira)}", parse_tarih(m.group(2))  # "2024/04" -> "2024/4" (dosya adıyla aynı biçim)


def satirlar_sayfali(sayfalar):
    out = []
    for i, s in enumerate(sayfalar, 1):
        for l in s.split("\n"):
            if re.match(r"^\s*(_{5,}|MERKEZ |İSTANBUL TEMSİLCİLİĞİ)", l):
                continue
            out.append((i, l.rstrip()))
    return out


def bolumler(satirlar):
    """Kural 1-2: başlık metniyle bölüm sınırı."""
    sonuc = []
    cur = None
    for sayfa, l in satirlar:
        if UST_BASLIK.match(l):
            if cur:
                sonuc.append(cur)
            tur = "C" if BASLIK_C.search(l) else ("DUYURU" if BASLIK_DUYURU.search(l) else None)
            cur = {"tur": tur, "baslik": l.strip(), "satirlar": []} if tur else None
            continue
        if cur is not None:
            cur["satirlar"].append((sayfa, l))
    if cur:
        sonuc.append(cur)
    return sonuc


def birimler(satirlar, harf_modu=True):
    """Kural 3: 'a) b)' paragraf + tablo; harf yoksa alt başlık bloğu tek birim."""
    out, cur = [], None
    for sayfa, l in satirlar:
        if harf_modu and HARF_MADDE.match(l):
            if cur:
                out.append(cur)
            cur = {"sayfa": sayfa, "satirlar": [l]}
        elif not harf_modu and NUM_MADDE.match(l) and not re.match(r"^\s*\d\.\s*\d", l):
            if cur:
                out.append(cur)
            cur = {"sayfa": sayfa, "satirlar": [l]}
        elif ALT_BASLIK_ATLA.match(l) and harf_modu:
            if cur:
                out.append(cur)
            cur = {"sayfa": sayfa, "satirlar": [l], "alt_baslik": True}
        else:
            if cur is None:
                cur = {"sayfa": sayfa, "satirlar": []}
            cur["satirlar"].append(l)
    if cur:
        out.append(cur)
    for u in out:
        u["metin"] = re.sub(r"\s+", " ", " ".join(u["satirlar"])).strip()
    return [u for u in out if u["metin"]]


def kodlar_bul(metin):
    """Kural 8-9: başlıktaki parantezli kodlar; sözlük doğrulaması ayrı adım."""
    kodlar = []
    for m in re.finditer(r"\(([^()]{2,60})\)", metin[:1400]):
        ic = m.group(1)
        for parca in re.split(r"\s*[,;]\s*", ic):
            p = parca.strip()
            if re.fullmatch(r"[A-ZÇĞİÖŞÜ]{3,6}(?:\.[A-Z])?", p) and p not in KOD_STOP:
                if p not in kodlar:
                    kodlar.append(p)
    if not kodlar:  # parantezsiz yazım: "ASUZU pay piyasasına yönelik" (2026-34)
        for m in re.finditer(r"(?<![A-Za-zÇĞİÖŞÜçğıöşü])([A-ZÇĞİÖŞÜ]{4,5})\s+pay\s+piyasas", metin[:700]):
            if m.group(1) not in KOD_STOP and m.group(1) not in kodlar:
                kodlar.append(m.group(1))
    return kodlar


def unvan_bul(metin):
    """Kural 8: kodu olmayan, şirket unvanıyla anılan kayıtlar için unvan (sözlük eşlemesi sonraki adım)."""
    m = re.match(r"\s*(?:[a-zçğıöşü]|\d+)[).]\s*(.{3,110}?)\s+(?:\(Şirket\)\s+)?(?:hakkında|paylarında)\b", metin[:400], re.S)
    if not m:
        return ""
    u = re.sub(r"^(?:\d+\.\s*)?İdari\s+Para\s+Cezaları\s+", "", re.sub(r"\s+", " ", m.group(1)).strip())
    return "" if re.search(r"pay\s+piyasa|şahıs|kişi|Kimlik|Borsa\s+İstanbul", u, re.I) else u


def donem_bul(metin):
    """Kural 12: yalnızca bağlamı açık aralıklar."""
    bulunan = []
    for m in re.finditer(rf"({TARIH})\s*(?:-|–|—)\s*({TARIH})", metin):
        a, b = parse_tarih(m.group(1)), parse_tarih(m.group(2))
        if a and b and a <= b:
            bulunan.append((a, b, "gun"))
    for m in re.finditer(rf"({TARIH})\s+ile\s+({TARIH})\s+tarihleri", metin):
        a, b = parse_tarih(m.group(1)), parse_tarih(m.group(2))
        if a and b and a <= b:
            bulunan.append((a, b, "gun"))
    for m in re.finditer(rf"({TARIH})\s+tarihinden\s+({TARIH})\s+tarihine", metin):
        a, b = parse_tarih(m.group(1)), parse_tarih(m.group(2))
        if a and b and a <= b:
            bulunan.append((a, b, "gun"))
    for m in re.finditer(rf"({AY_RE})\s+(\d{{4}})\s+(?:ve|ile|-)\s+({AY_RE})\s+(\d{{4}})\s+tarihleri", metin, re.I):
        a1, y1, a2, y2 = AYLAR[m.group(1).lower()], int(m.group(2)), AYLAR[m.group(3).lower()], int(m.group(4))
        bas = dt.date(y1, a1, 1)
        nxt = dt.date(y2 + (a2 == 12), (a2 % 12) + 1, 1)
        bulunan.append((bas, nxt - dt.timedelta(days=1), "ay"))
    # tekrarları at
    tekil = []
    for b in bulunan:
        if b not in tekil:
            tekil.append(b)
    return tekil


def tur_belirle(metin):
    m = metin
    # lisans iptali (V-101.1 md 17/1) suç duyurusunun ardından gelir; etiket değeri yoktur
    if re.search(r"Lisansları\s+İptal\s+Edilen|tüm\s+lisansların", m, re.I):
        return "lisans_iptali"
    # mevcut yasağın uzatılması: yeni olay değil, süre uzatma (2025-14 NTHOL)
    if re.search(r"yasağ\w*[^.]{0,200}uzatılmasına|uzatılmasına[^.]{0,60}yasağ", m, re.I):
        return "tedbir_uzatma"
    kesin = re.search(r"\b2\s*Yıl\b", m, re.I) and re.search(r"5/2|6/2|yapma\s+yasağı", m)
    gecici = re.search(r"geçici\s+işlem\s+(?:yapma\s+)?yasağı", m, re.I) or re.search(r"\b6\s*ay\b.{0,40}5/1", m)
    if kesin:
        return "tedbir_kesin"
    if gecici:
        return "tedbir_gecici"
    if re.search(r"suç\s+duyurusunda\s+bulunulmas|Suç\s+Duyurusunda/?|suç\s+ihbar", m, re.I):
        return "suc_duyurusu"
    if re.search(r"idari\s+para\s+ceza", m, re.I):
        return "ipc"
    return "diger"


# kural 18: VI-104.1 Tebliği md 4-7 bent/fıkra → eylem türü (metin: veri/etiketler/kaynak-vi-104-1-...md)
FIKRA = {"birinci": 1, "ikinci": 2, "üçüncü": 3, "dördüncü": 4, "beşinci": 5}
TIP_M5 = {"a": "emir_islem_genel", "b": "kademe_emri", "c": "yon_degistiren_emir", "ç": "karsilikli_veya_kendinden_islem",
          "d": "acilis_kapanis_fiyati", "e": "uzlasma_fiyati", "f": "fiyat_etkileme",
          "g": "viop_pozisyon_limiti", "ğ": "viop_dayanak_ayni_yonlu"}
TIP_M6 = {1: "yanlis_bilgi_haber_yorum", 2: "yanlis_bilgi_yayma", 3: "aciklama_yukumlulugu_ihlali",
          4: "tavsiye_sonrasi_ters_islem"}
TIP_M4 = {2: "icsel_bilgi_aktarma_veya_islem", 3: "finansal_tablo_donemi_islem", 4: "icsel_bilgi_donemi_islem"}
TIP_M7 = {1: "emir_oncesi_islem", 2: "baskasinin_hesabi", 3: "pay_tebligi_md27", 4: "islem_yasagi_ihlali"}
GRUP = {4: "icsel_bilgi", 5: "emir_islem", 6: "iletisim", 7: "diger"}


def tebligi_atif(metin):
    """VI-104.1 atıflarını (madde, fıkra, bentler) olarak döndürür; yalnızca VI-104.1 geçen birimde çalışır."""
    if not re.search(r"VI-104\.1|Piyasa\s+Bozucu\s+Eylemler", metin, re.I):
        return []
    bulunan = []
    pat = re.compile(r"(?<![\d.,/])\b([4-7])\b(?![.,/\d]).{0,150}?\b(?:inci|nci|üncü|uncu|ncı|ncü)\b.{0,160}?maddesinin\b.{0,100}?\b(birinci|ikinci|üçüncü|dördüncü|beşinci|[1-5](?=\s*(?:inci|nci|üncü|uncu|ncı|ncü)\b))\b.{0,100}?fıkrası(?:nın)?(.{0,170})",
                     re.S)
    for m in pat.finditer(metin):
        madde = int(m.group(1))
        fikra = FIKRA[m.group(2)] if m.group(2) in FIKRA else int(m.group(2))
        bentler = []
        kuyruk = m.group(3)
        bit = re.search(r"bent", kuyruk)
        if bit:
            bentler = re.findall(r"\(([a-zçğıöşü])\)", kuyruk[:bit.start()])
        bulunan.append((madde, fikra, tuple(bentler)))
    if not bulunan:  # fıkra belirtmeden yalnızca madde atfı ("Tebliği'nin 7 nci maddesi")
        for m in re.finditer(r"Bozucu\s+Eylemler.{0,140}?(?<![\d.,/])\b([4-7])\b(?![.,/\d]).{0,150}?\b(?:inci|nci|üncü|uncu|ncı|ncü)\b\s+madde", metin, re.S):
            bulunan.append((int(m.group(1)), 0, ()))
    # tekrarları at
    tekil = []
    for b in bulunan:
        if b not in tekil:
            tekil.append(b)
    return tekil


def tip_cikar(tur, madde_alani, atiflar):
    tipler, madde_parca = [], []
    for madde, fikra, bentler in atiflar:
        if madde == 5:
            etiket = (f"5/{fikra}(" + ",".join(bentler) + ")") if bentler else (f"5/{fikra}" if fikra else "5")
            tipler += [TIP_M5.get(b, "bilinmeyen_bent") for b in bentler] or ["emir_islem_genel_bentsiz"]
        elif madde == 6:
            etiket = f"6/{fikra}" if fikra else "6"
            tipler.append(TIP_M6.get(fikra, "iletisim"))
        elif madde == 4:
            etiket = f"4/{fikra}" if fikra else "4"
            tipler.append(TIP_M4.get(fikra, "icsel_bilgi"))
        else:
            etiket = f"7/{fikra}" if fikra else "7"
            tipler.append(TIP_M7.get(fikra, "diger"))
        madde_parca.append(etiket)
    if "107/1" in madde_alani:
        tipler.append("islem_bazli_piyasa_dolandiriciligi")
    if "107/2" in madde_alani:
        tipler.append("bilgi_bazli_piyasa_dolandiriciligi")
    if re.search(r"(?<![\d./-])104(?![\d.])", madde_alani) and "107/1" not in madde_alani and "107/2" not in madde_alani:
        tipler.append("md104_piyasa_bozucu_eylem_belirsiz_tur")  # "104 veya 107" gibi fıkrasız atıf (2025-11 KRGYO, TDGYO)
    gruplar = sorted({GRUP[a[0]] for a in atiflar})
    tek = []
    for t in tipler:
        if t not in tek:
            tek.append(t)
    return ";".join(madde_parca), ";".join(tek), ";".join(gruplar)


def vaka_cikar(bulten, bulten_no, bulten_tarihi, bolum_satirlari):
    vakalar = []
    for u in birimler(bolum_satirlari, harf_modu=True):
        metin = u["metin"]
        # etkin pişmanlık dipnotu (107/1, 107/3) suçun dayanağı değildir; 109 izinsiz faaliyet kayıtlarına bulaşır (2026-6)
        metin = re.sub(r"\d\)\s*6362\s+sayılı\s+SPKn.{0,3}nun\s+107/1\s+maddesi\s+çerçevesinde\s+hakkında.*?gerekmektedir\.",
                       " ", metin, flags=re.S)
        if u.get("alt_baslik") and len(metin) < 80:
            continue
        # V-101.1 md 15 (yasaklı kişi hesabından kredili satış/tasfiye) aracı kurum ihlalidir; manipülasyon değildir (2024-59, 2026-10)
        if re.search(r"Tedbirler\s+Tebliği.{0,60}\b15\s*inci", metin) and not re.search(r"VI-104\.1|\b107\s*(?:nci|inci|ncı)|\b107/\d", metin):
            continue
        if not DAYANAK_RE.search(metin):
            continue  # kural 4-5
        tur = tur_belirle(metin)
        if tur == "diger":
            continue
        kodlar = kodlar_bul(metin)
        donemler = donem_bul(metin)
        tb = re.search(rf"({TARIH})\s+tarihli\s+işlemlerden\s+başlamak", metin)
        tedbir_bas = parse_tarih(tb.group(1)) if tb else None
        sure = ""
        ms = re.search(r"(\d+)\s*(ay|yıl)\s+süreyle", metin, re.I)
        if ms:
            sure = f"{ms.group(1)} {ms.group(2).lower()}"
        elif re.search(r"\b2\s*Yıl\b", metin, re.I) and tur == "tedbir_kesin":
            sure = "2 yıl"
        mad = []
        if re.search(r"VI-\s*104\.1|Piyasa\s+Bozucu\s+Eylemler", metin):  # satır sonunda "VI-" / "104.1" bölünebilir; bazı bültenler Tebliğ adını açık yazar
            mad.append("VI-104.1")
            if "104" not in mad:
                mad.append("104")  # kural 20: VI-104.1, SPKn md 104'e dayanır; İPC kayıtlarında bayrak tutarlı
        for x in re.findall(r"\b107/\d", metin):
            if x != "107/3":  # 107/3 = etkin pişmanlık dipnotu, suçun kendisi değil
                mad.append(x)
        for f in re.findall(r"\b107\s*(?:nci|inci|ncı)\s*maddesinin\s*(birinci|ikinci)", metin):
            mad.append("107/1" if f == "birinci" else "107/2")
        if re.search(r"SPKn[’'`]?nun\s+(?:\(SPKn\)\s*)?104\b|\b104\s+(?:üncü|uncu|veya|ve)\b|\bveya\s+104\b", metin):
            mad.append("104")
        if re.search(r"V-101\.1", metin):
            mad.append("V-101.1")
        karar = re.search(rf"Kurul\s+Karar\s+Organı[’'`]nın\s+({TARIH})\s+tarih(?:li)?\s+ve\s+([\d/]+)\s+sayılı", metin)
        karar_tarihi = parse_tarih(karar.group(1)) if karar else None
        kisi = len(re.findall(r"\b\d{2}\*{5,}\d{2}\b", " ".join(u["satirlar"])))
        varant = bool(re.search(r"\b[A-ZÇĞİÖŞÜ]{3,6}\.V\b|varant", metin, re.I))
        muhtelif = bool(re.search(r"muhtelif\s+pay|Borsa\s+İstanbul\s+A\.?Ş\.?\s+pay\s+piyasaları", metin[:700], re.I))
        if len(kodlar) > 5:  # kural 10: 22-26 paylık sosyal medya listeleri (2025-15, 2025-38, 2025-49, 2024-50) hisse-gün etiketi değildir
            muhtelif = True
        # önceki karara atıf: "gg.aa.yyyy tarihli ... kararı ile ... yasağı getirilen" (kural 16 bağlama önceliği)
        atif_t = []
        for mm in re.finditer(rf"({TARIH})\s+tarihli(?:\s+ve\s+[\d/]+\s+sayılı)?(?:\s+ve\s+{TARIH}\s+tarihli\s+ve\s+[\d/]+\s+sayılı)?(?:\s+iki)?\s+[Kk]arar", metin):
            t_ = parse_tarih(mm.group(1))
            if t_:
                atif_t.append(t_)
        tebligi_madde, mtip, tgrup = tip_cikar(tur, ",".join(sorted(set(mad))), tebligi_atif(metin))
        vakalar.append({
            "bulten": bulten, "bulten_no": bulten_no, "bulten_tarihi": bulten_tarihi, "sayfa": u["sayfa"],
            "tur": tur, "pay_kodlari": kodlar, "donemler": donemler, "tedbir_bas": tedbir_bas, "tedbir_sure": sure,
            "madde": ",".join(sorted(set(mad))),
            "tebligi_madde": tebligi_madde, "manipulasyon_tipi": mtip, "tip_grubu": tgrup,
            "karar_tarihi": karar_tarihi, "kisi_sayisi": kisi, "varant": varant, "muhtelif": muhtelif,
            "atif_tarihleri": atif_t,
            "sirket_unvani": "" if kodlar else unvan_bul(metin),
            "alinti": maskele(metin[:320]),
            "metin_tam": metin,  # yalnızca bellekte (doğrulama yardımcıları için); CSV'ye yazılmaz
        })
    return vakalar


def seviye_etiket(v):
    donem = v["donemler"][0] if v["donemler"] else None
    kod_var = bool(v["pay_kodlari"])
    if v["tur"] == "lisans_iptali":
        return "D", 0
    if v["varant"] or v["muhtelif"] or not kod_var:
        return "D", 0
    if donem:
        return "A", 1
    if v["tur"] in ("tedbir_gecici", "tedbir_kesin") and v["tedbir_bas"]:
        return "B", 1
    return "C", 0


def olay_cikar(bulten, bulten_no, bulten_tarihi, bolum_satirlari):
    olaylar = []
    for u in birimler(bolum_satirlari, harf_modu=False):
        metin = u["metin"]
        if not re.search(r"açığa\s+satış|geri\s+alım|öz\s*kaynak\s+oranı|devre\s+kesici", metin, re.I):
            continue
        ktur = []
        baş = metin[:1100]  # yalnızca geçerken anılan konular olay değildir (ör. yeniden değerleme tablosu, fiili dolaşımdaki pay)
        if re.search(r"açığa\s+satış", baş, re.I) and re.search(r"yasak|kaldırıl|devam", baş, re.I):
            ktur.append("acigasatis")
        if re.search(r"geri\s+alım", baş, re.I) and re.search(r"i-SPK\.?\s*22\.\d|geri\s+alım\s+program|pay\s+geri\s+alım", baş[:450], re.I):
            ktur.append("geri_alim")
        if re.search(r"öz\s*kaynak\s+(?:koruma\s+)?oranı", baş, re.I):
            ktur.append("ozkaynak_esnetme")
        if not ktur:
            continue
        alt = "kaldirma" if re.search(r"yürürlükten\s+kaldırıl|kaldırılmas", metin, re.I) else (
            "uzatma" if re.search(r"devam\s+edilmesine", metin, re.I) else "baslangic")
        karar = (re.search(rf"Kurul\s+Karar\s+Organı[’'`]nın\s+({TARIH})\s+tarih(?:li)?\s+ve\s+([\d/]+)(?:\s+ile\s+[\d/]+)?\s+sayılı\s+Karar(?:ı|ları)?\s+Uyarınca", metin, re.I)
                 or re.search(rf"i-SPK[\s\d.A-Za-z]{{0,12}}\(({TARIH})\s+tarih(?:li)?\s+ve\s+([\d/]+)\s+s\.k\.\)", metin)
                 or re.search(rf"Kurul\s+Karar\s+Organı[’'`]nın\s+({TARIH})\s+tarih(?:li)?\s+ve\s+([\d/]+)\s+sayılı", metin)
                 or re.search(rf"({TARIH})\s+tarih(?:li)?\s+ve\s+([\d/]+)\s+sayılı", metin))
        bit = re.search(rf"({TARIH})\s+tarihi\s+seans\s+sonuna\s+kadar", metin)
        bas = (re.search(rf"({TARIH})\s+tarihinden\s+itibaren", metin)
               or re.search(rf"({TARIH})\s+tarihinden\s+{TARIH}\s+tarihi\s+seans\s+sonuna", metin))
        atif = re.search(rf"({TARIH})\s+tarihli\s+ve\s+(\d{{4}}/\d+)\s+sayılı\s+bülten", metin)
        kapsam = "BIST50" if re.search(r"BIST\s*50", metin) else ("tum_pay" if re.search(r"pay\s+piyasalar", metin, re.I) else "")
        olaylar.append({
            "bulten": bulten, "bulten_no": bulten_no, "bulten_tarihi": bulten_tarihi, "sayfa": u["sayfa"],
            "tur": "+".join(ktur) or "diger", "alt_tur": alt,
            "karar_tarihi": parse_tarih(karar.group(1)) if karar else None,
            "bas": parse_tarih(bas.group(1)) if bas else None,
            "bit": parse_tarih(bit.group(1)) if bit else None,
            "atif_bulten": atif.group(2) if atif else "", "kapsam": kapsam, "alinti": maskele(metin[:320]),
        })
    return olaylar


def pencere_adayi(v):
    w0, w1 = PENCERE
    for a, b, _ in v["donemler"]:
        if a <= w1 and b >= w0:
            return "A_donem_kesisiyor"
    tb = v["tedbir_bas"]
    if tb and w0 <= tb <= w1 + dt.timedelta(days=B_ONCESI_GUN):
        return "B_tedbir_pencerede"
    return ""


def yaz_csv(yol, satirlar, alanlar):
    with io.open(yol, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=alanlar, extrasaction="ignore")
        w.writeheader()
        for s in satirlar:
            w.writerow({k: ("" if s.get(k) is None else s.get(k)) for k in alanlar})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bulten-dir", default=str(KOK / "kaynaklar" / "spk_bultenleri"))
    ap.add_argument("--cikti-dir", default=str(KOK / "veri" / "etiketler"))
    ap.add_argument("--onbellek", default="")
    a = ap.parse_args()
    out = Path(a.cikti_dir)
    out.mkdir(parents=True, exist_ok=True)
    cache = Path(a.onbellek) if a.onbellek else None
    if cache:
        cache.mkdir(parents=True, exist_ok=True)

    pdfler = sorted(Path(a.bulten_dir).glob("20*/*.pdf"))
    indeks, vakalar, olaylar = [], [], []
    for yol in pdfler:
        ad = bulten_adi(yol)
        sayfalar = None
        if cache and (cache / f"{ad}.txt").exists():
            sayfalar = (cache / f"{ad}.txt").read_text(encoding="utf-8").split("\f")
        if sayfalar is None:
            try:
                sayfalar = metin_cikar(yol)
            except Exception as e:  # bozuk PDF
                indeks.append({"bulten": ad, "dosya": yol.name, "hata": str(e)[:100]})
                continue
            if cache:
                (cache / f"{ad}.txt").write_text("\f".join(sayfalar), encoding="utf-8")
        no, tarih = bulten_ust_bilgi(sayfalar[0] if sayfalar else "")
        satirlar = satirlar_sayfali(sayfalar)
        bol = bolumler(satirlar)
        v_say = o_say = 0
        for b in bol:
            if b["tur"] == "C":
                for v in vaka_cikar(ad, no, tarih, b["satirlar"]):
                    v["seviye"], v["etiket_uygun"] = seviye_etiket(v)
                    v["pencere"] = pencere_adayi(v)
                    vakalar.append(v)
                    v_say += 1
            else:
                for o in olay_cikar(ad, no, tarih, b["satirlar"]):
                    olaylar.append(o)
                    o_say += 1
        indeks.append({"bulten": ad, "dosya": yol.name, "bulten_no_ic": no,
                       "bulten_tarihi": tarih, "sayfa_sayisi": len(sayfalar),
                       "karakter": sum(len(s) for s in sayfalar), "c_bolumu": any(b["tur"] == "C" for b in bol),
                       "duyuru_bolumu": any(b["tur"] == "DUYURU" for b in bol),
                       "vaka_sayisi": v_say, "olay_sayisi": o_say,
                       "ad_no_uyumsuz": (no.replace("/", "-") != ad) if no else True})

    # dönem-satırlarını aç: kayıt başına her koda ayrı satır (kural 9)
    satirlar = []
    for i, v in enumerate(vakalar, 1):
        kodlar = v["pay_kodlari"] or [""]
        for kod in kodlar:
            d = v["donemler"][0] if v["donemler"] else (None, None, "")
            satirlar.append({
                "vaka_kaydi": i, "bulten": v["bulten"], "bulten_tarihi": v["bulten_tarihi"], "sayfa": v["sayfa"],
                "pay_kodu": kod, "sirket_unvani": v["sirket_unvani"], "coklu_kod": int(len(v["pay_kodlari"]) > 1), "tur": v["tur"], "madde": v["madde"],
                "tebligi_madde": v["tebligi_madde"], "manipulasyon_tipi": v["manipulasyon_tipi"], "tip_grubu": v["tip_grubu"],
                "donem_bas": d[0], "donem_bit": d[1], "donem_kesinligi": d[2], "donem_sayisi": len(v["donemler"]),
                "tedbir_bas": v["tedbir_bas"], "tedbir_sure": v["tedbir_sure"], "karar_tarihi": v["karar_tarihi"],
                "kisi_sayisi": v["kisi_sayisi"], "arac_tipi": "varant" if v["varant"] else "pay",
                "muhtelif": int(v["muhtelif"]), "seviye": v["seviye"], "etiket_uygun": v["etiket_uygun"],
                "pencere": v["pencere"], "alinti": v["alinti"], "dogrulandi": "",
                "atif_tarihleri": v["atif_tarihleri"],
            })

    # kural 16: dönemsiz C seviyesi kaydı, aynı payın A/B kaydına bağlanır (en yakın bülten tarihi, <= 3 yıl)
    by_kod = {}
    for r in satirlar:
        if r["pay_kodu"] and r["arac_tipi"] == "pay":
            by_kod.setdefault(r["pay_kodu"], []).append(r)
    for r in satirlar:
        r["bagli_kayit"], r["seviye_nihai"], r["etiket_nihai"] = "", r["seviye"], r["etiket_uygun"]
        r["baglanti_belirsiz"] = 0
        r["nihai_donem_bas"], r["nihai_donem_bit"], r["nihai_tedbir_bas"] = r["donem_bas"], r["donem_bit"], r["tedbir_bas"]
        if r["seviye"] != "C" or not r["pay_kodu"]:
            continue
        # karar/ceza, tedbirden sonra yayımlanır: yalnızca kayıttan ÖNCE (veya aynı gün) yayımlanmış A/B kaydı aday
        adaylar = [d for d in by_kod.get(r["pay_kodu"], [])
                   if d["seviye"] in ("A", "B") and d["vaka_kaydi"] != r["vaka_kaydi"]
                   and r["bulten_tarihi"] and d["bulten_tarihi"]
                   and 0 <= (r["bulten_tarihi"] - d["bulten_tarihi"]).days <= 1100]
        if not adaylar:
            continue
        adaylar.sort(key=lambda d: (r["bulten_tarihi"] - d["bulten_tarihi"]).days)  # en yakın önceki
        # kendi karar tarihi atıf sayılmaz
        atif = [a_ for a_ in (r.get("atif_tarihleri") or []) if not (r.get("karar_tarihi") and a_ == r["karar_tarihi"])]

        def eslesir(d):
            for a_ in atif:
                if d["bulten_tarihi"] and abs((d["bulten_tarihi"] - a_).days) <= 1:
                    return True
                if d["tedbir_bas"] and abs((d["tedbir_bas"] - a_).days) <= 3:
                    return True
            return False
        esl = [d for d in adaylar if eslesir(d)]
        farkli = {(x["tedbir_bas"], x["donem_bas"]) for x in adaylar}
        if esl:
            d = esl[0]  # atıf edilen karar bülteniyle eşleşen en yakın aday
            r["baglanti_belirsiz"] = 0
        elif atif:
            # kural 21: atıf edilen karar arşivde (2024-2026) yok; rastgele başka bir tedbire BAĞLANMAZ, kayıt kendi seviyesinde kalır
            r["baglanti_disarida"] = 1
            continue
        else:
            d = adaylar[0]
            r["baglanti_belirsiz"] = int(len(farkli) > 1)
        r["bagli_kayit"] = f'{d["bulten"]}#{d["vaka_kaydi"]}'
        r["seviye_nihai"], r["etiket_nihai"] = d["seviye"], 1
        r["nihai_donem_bas"], r["nihai_donem_bit"], r["nihai_tedbir_bas"] = d["donem_bas"], d["donem_bit"], d["tedbir_bas"]

    # kural 22: aynı bültende aynı paya ait suç duyurusu, o bültendeki bağlanmış kesin tedbir kaydının donörüne bağlanır
    # ("Bakınız 3. Diğer Yaptırım, Tedbir ve İşlem Yasakları" çapraz atfı); atıf edilen karar donörle eşleşmiş olmalı
    for r in satirlar:
        if r["tur"] != "suc_duyurusu" or r["seviye"] != "C" or not r["pay_kodu"]:
            continue
        kardes = [k for k in satirlar if k["bulten"] == r["bulten"] and k["pay_kodu"] == r["pay_kodu"]
                  and k["tur"] == "tedbir_kesin" and k["bagli_kayit"] and not k["baglanti_belirsiz"]]
        kopuk = [k for k in satirlar if k["bulten"] == r["bulten"] and k["pay_kodu"] == r["pay_kodu"]
                 and k["tur"] == "tedbir_kesin" and k.get("baglanti_disarida")]
        if kopuk and not kardes:  # kardeş kesin tedbirin atıf ettiği ilk karar arşiv dışında; aynı bülten/pay suç duyurusu da donörsüz kalır
            r["bagli_kayit"], r["baglanti_belirsiz"] = "", 0
            r["seviye_nihai"], r["etiket_nihai"] = r["seviye"], r["etiket_uygun"]
            r["nihai_donem_bas"], r["nihai_donem_bit"], r["nihai_tedbir_bas"] = r["donem_bas"], r["donem_bit"], r["tedbir_bas"]
            r["baglanti_disarida"], r["baglanti_notu"] = 1, "kural22_kardes_disarida"
            continue
        if kardes:
            k = kardes[0]
            r["bagli_kayit"], r["baglanti_belirsiz"] = k["bagli_kayit"], 0
            r["seviye_nihai"], r["etiket_nihai"] = k["seviye_nihai"], 1
            r["nihai_donem_bas"], r["nihai_donem_bit"], r["nihai_tedbir_bas"] = k["nihai_donem_bas"], k["nihai_donem_bit"], k["nihai_tedbir_bas"]
            r["baglanti_notu"] = "kural22_ayni_bulten"

    def nihai_pencere(r):
        w0, w1 = PENCERE
        a, b, t = r["nihai_donem_bas"], r["nihai_donem_bit"], r["nihai_tedbir_bas"]
        if a and b and a <= w1 and b >= w0:
            return "A_donem_kesisiyor"
        if t and w0 <= t <= w1 + dt.timedelta(days=B_ONCESI_GUN):
            return "B_tedbir_pencerede"
        return ""
    for r in satirlar:
        r["pencere_nihai"] = nihai_pencere(r) if r["etiket_nihai"] else ""
    vk = ["vaka_kaydi", "bulten", "bulten_tarihi", "sayfa", "pay_kodu", "sirket_unvani", "coklu_kod", "tur", "madde", "tebligi_madde", "manipulasyon_tipi", "tip_grubu", "donem_bas",
          "donem_bit", "donem_kesinligi", "donem_sayisi", "tedbir_bas", "tedbir_sure", "karar_tarihi", "kisi_sayisi",
          "arac_tipi", "muhtelif", "seviye", "etiket_uygun", "pencere", "bagli_kayit", "baglanti_belirsiz", "baglanti_disarida", "baglanti_notu", "seviye_nihai",
          "etiket_nihai", "nihai_donem_bas", "nihai_donem_bit", "nihai_tedbir_bas", "pencere_nihai", "alinti", "dogrulandi"]
    yaz_csv(out / "vaka.csv", satirlar, vk)
    yaz_csv(out / "vaka_pencere_dogrulama.csv", [s for s in satirlar if s["pencere_nihai"] or s["pencere"]], vk)
    yaz_csv(out / "olay.csv", olaylar, ["bulten", "bulten_no", "bulten_tarihi", "sayfa", "tur", "alt_tur", "karar_tarihi",
                                       "bas", "bit", "atif_bulten", "kapsam", "alinti"])
    yaz_csv(out / "bulten_indeks.csv", indeks, ["bulten", "dosya", "bulten_no_ic", "bulten_tarihi", "sayfa_sayisi",
                                               "karakter", "c_bolumu", "duyuru_bolumu", "vaka_sayisi", "olay_sayisi",
                                               "ad_no_uyumsuz", "hata"])
    print(f"{len(pdfler)} PDF, {len(vakalar)} vaka kaydı ({len(satirlar)} kod satırı), {len(olaylar)} olay kaydı")


if __name__ == "__main__":
    sys.exit(main())
