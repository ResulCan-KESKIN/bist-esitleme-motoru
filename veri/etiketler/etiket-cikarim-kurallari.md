# SPK bültenlerinden manipülasyon etiketi çıkarım kuralları (v1)

Kaynak: `kaynaklar/spk_bultenleri/{2024,2025,2026}/` (197 PDF; üç eksik bülten eklendi, `2024 15.pdf` dosyası `2024-15.pdf` olarak yeniden adlandırıldı (19.10.2026).
Dayanak: 35 bülten gözle okundu (her yıldan 5 sistematik + 20 rastgele, tohum 20261012). Örnekler bülten numarasıyla verilmiştir.
Durum (12.10.2026): kurallar `veri/araclar/spk_bulten_etiket.py` ile 197 bültenin tümünde çalıştırıldı; bölüm sonundaki 13 otomatik test geçti. Çıktılar `veri/etiketler/` altında (`vaka.csv`, `olay.csv`, `bulten_indeks.csv`, `vaka_pencere_dogrulama.csv`). Elle doğrulama bekliyor.
İlgili kod: `veri/araclar/spk_bulten_etiket.py`.

## Kurallar

1. Bölüm sınırı başlık metniyle bulunur: "SUÇ DUYURUSU, İDARİ PARA CEZASI İLE DİĞER YAPTIRIM VE TEDBİRLER" ve "DUYURU VE İLKE KARARLARI". Bölüm harfi ve alt numarası kullanılmaz (uzun bültende C, özel bültende A veya B; alt numaralar değişken: 2024-7, 2024-44, 2025-22, 2026-9). Başlıktaki harften sonra nokta unutulabilir ("A DUYURU VE İLKE KARARLARI", 2026-13); ayrıştırıcı noktayı isteğe bağlı sayar.
2. Bir bültende bu bölümlerden biri veya ikisi bulunmayabilir (2026-22 hiçbirini içermez); bölüm yokluğu hata değildir.
3. Kayıt birimi: "a) b) c)" ile başlayan paragraf ile onu izleyen tablo (sonraki "a)" veya alt başlığa kadar). Alt başlık yoksa (2025-52, 2026-44) harf işaretli paragraf kayıt birimidir.
4. Manipülasyon filtresi hukuki dayanağa bakar; "pay piyasasında gerçekleştirilen işlemler" ifadesine bakmaz. Kayıt ancak şunlardan en az birini içerirse aday olur: SPKn 104, SPKn 107 (107/1, 107/2), VI-104.1 sayılı Piyasa Bozucu Eylemler Tebliği, V-101.1 sayılı Tedbirler Tebliği (5/1, 5/2, 6/1, 6/2, 9/2). Gerekçe: 2024-13 (LDR), 2024-14 (Martı GYO, Mega Polietilen) ve 2025-6 (USAK) "pay piyasasında işlem" geçer ama II-15.1 Özel Durumlar veya V-65 açığa satış ihlalidir.
5. Hariç sınıflar (etiket üretmez): SPKn 109 izinsiz faaliyet, TCK 157/158, 99/99-A site erişim engeli, II-15.1 özel durum, II-17.1 kurumsal yönetim, VII-128.1 pay satış bilgi formu/fon kullanımı, II-5.1 izahname, III-37.1/III-39.1/VII-128.9 aracı kurum, fon ve portföy kuralları, V-65 açığa satış ihlali (SPKn 103).
6. Karar türü:
   - `tedbir_gecici`: "geçici işlem yasağı", Tebliğ 5/1, 6/1, süre 6 ay, "makul şüphe" (2024-3, 2025-22, 2026-23, 2026-44, 2026-50).
   - `tedbir_kesin`: "2 yıl" işlem yapma yasağı, Tebliğ 5/2, 6/2 (9/2 aracı kurum), suç tespiti sonrası (2025-49, 2026-37). Metinde "geçici işlem **yapma** yasağı" biçimi de geçer (2026-37); düz "geçici işlem yasağı" araması bunu kaçırır.
   - `ipc`: "idari para cezası" + VI-104.1 (2024-21, 2024-44, 2024-50, 2025-8, 2025-49).
   - `suc_duyurusu`: "suç duyurusunda bulunulmasına" + SPKn 107 (2024-1, 2026-37).
   - `tedbir_uzatma`: mevcut geçici yasağın 6 ay uzatılması ("uzatılmasına karar verilmiştir", 2025-14 NTHOL); yeni olay değildir, başlangıç tarihi taşımaz, A/B donörü olamaz.
   - `lisans_iptali`: "Lisansları İptal Edilen" tablosu (V-101.1 md 17/1, suç duyurusunun ardından, 2025-66); etiket üretmez.
   - `piyasa_olayi`: bkz. kural 15.
7. SPKn madde fıkrası kayıttan çıkarılır: 107/1 (işlem bazlı), 107/2 (bilgi bazlı; sosyal medya paylaşımı ile birlikte), 104, "104 veya 107/1", "104 ve 107/1". Birleşik ifade olduğu gibi saklanır; ayrıştırılıp tek değere indirgenmez.
8. Pay kodu: kayıt başlığındaki parantezli büyük harfli kod; kod yoksa şirket unvanı ile kod↔unvan sözlüğü (ITCH `R` mesajları/DataStore). Sözlük tarihlidir (unvan/kod değişikliği: PEGYO→PEHOL, 2024-43). Üç-altı harf büyük harf kalıbı tek başına kod sayılmaz (SPK, BIST, AŞ, TAŞ, TL, KAP gürültüdür).
9. Birden fazla kod aynı kayıtta ayrı alanlarda tutulur (PAMEL, BMELK 2025-66; THYAO, DOCO, PGSUS, VAKKO, FROTO, AKSEN, PETKM 2024-50). Kayıt başına birden fazla kod varsa dönem ve karar her koda ayrı satır olarak kopyalanır, `coklu_kod=1` işaretlenir.
10. Pay kodu bulunamayan veya "muhtelif pay piyasaları" / "Borsa İstanbul AŞ pay piyasaları" diyen kayıtlar (2025-49 genel suç duyurusu, 26 paylık X platformu İPC'si) `etiket_uygun=0` işaretlenir; vaka kaydı olarak saklanır, hisse-gün etiketi üretmez. Kodları açıkça sayılmış ama 5'ten fazla kod içeren kayıtlar (2025-15: 25, 2025-38: 22, 2025-49: 26 kod, 2024-50: 7 kod; sosyal medya paylaşımı listeleri) seviye D'dir ve başka vakalara bağlanmaz; 2–5 kodlu kayıtlar (PAMEL+BMELK; EKSUN+AVGYO; IPEKE+TMSN+TUCLK+DZGYO) her koda ayrı satır üretir.
11. Varant ve sertifika kayıtları (kodda `.V`, "varant piyasası", 2025-62 KZBAZ.V) `araç_tipi=varant` işaretlenir ve hisse etiketi tablosuna girmez; dayanak kodu (KOZAL) ayrı alanda tutulur.
12. Dönem yalnızca bağlamı açık tarih aralığından alınır: başlıkta veya tablo hücresinde "gg.aa.yyyy-gg.aa.yyyy döneminde" / "tarihleri arasında" / "ile" (2024-21, 2024-44, 2024-33 hücre, 2025-11). Ay adlı biçimler ("Haziran 2023 ve Eylül 2023 tarihleri arasında", 2024-33) ay başı–ay sonu olarak çevrilir, `donem_kesinligi=ay` işaretlenir. Aralık bağlamı olmayan tek tarih dönem değildir (olay tarihi: 2024-13 "26.04.2022 tarihinde", 2024-14 "12.05.2022 tarihli alım").
13. Yasak başlangıcı "gg.aa.yyyy tarihli işlemlerden başlamak üzere" kalıbından alınır; bitiş = başlangıç + süre (6 ay veya 2 yıl) ve `tedbir_gecici` için fiilî sona erme (kaldırma) ayrı kontrol edilir.
14. Karar tarihi: metinde "Kurul Karar Organı'nın gg.aa.yyyy tarih ve N/M sayılı Kararı" geçiyorsa o; yoksa bülten tarihi. `bulten_tarihi` her zaman ayrıca saklanır (bülten başlığındaki "yyyy/N gg/aa/yyyy").
15. Piyasa olayları ayrı tabloda tutulur: açığa satış yasağı (başlangıç, uzatma, kaldırma, kapsam: tüm pay piyasaları / BIST 50), pay geri alımı kolaylaştırma ilke kararı, öz kaynak oranı esnetme. Olay yalnızca konu, birimin ilk ~1100 karakterinde geçiyorsa sayılır (yeniden değerleme tablosu 2024-60/2025-68, fiili dolaşımdaki pay 2026-57 gibi geçerken anan birimler olay değildir). Karar tarihi önce "Kurul Karar Organı'nın gg.aa.yyyy tarih ve N/M sayılı Kararı Uyarınca Yapılan Duyuru" kalıbından, sonra "i-SPK.xx (gg.aa.yyyy tarih ve N/M s.k.)" kalıbından alınır. Uzatma zinciri "gg.aa.yyyy tarihli ve yyyy/N sayılı bülteni ile duyurulan" atfıyla bağlanır (2026-27 → 2026-30; 2025-18 → 2025-24 → 2025-32 → 2025-36).
16. Aynı vaka birden fazla bültende tekrar eder (ALKLC: tedbir 2025-17, suç duyurusu 2025-57; USAK: özel durum İPC'si 2025-6, 107/2 suç duyurusu 2025-55). C seviyesi (dönemsiz) bir kayıt, aynı payın **kendisinden önce veya aynı gün yayımlanmış** en yakın A/B kaydına bağlanır (üst sınır 1100 gün); karar ve ceza tedbirden sonra yayımlandığı için yön tek taraflıdır (2024-19 TUREX İPC'si Eylül 2024 tedbirine bağlanmamalıdır). Metin önceki bir karara atıf yapıyorsa ("gg.aa.yyyy tarihli … kararı ile … yasak getirilen") bülten tarihi veya yasak başlangıcı atıf tarihiyle (±1 / ±3 gün) eşleşen aday öncelikli seçilir (KRGYO 2025-45 → 2025-11). Atıf var ama eşleşme yoksa (karar bültenler dışında kaldıysa: AVHOL, CEOEM, BJKAS) bağlantı kurulmaz (kural 21). Atıf yoksa ve aynı payda birden fazla farklı tedbir/dönem adayı varsa en yakın önceki aday seçilir ve `baglanti_belirsiz=1` işaretlenir. Kendi karar tarihi atıf sayılmaz. Kayıtlar silinmez; bağlanan kayıt kendi `seviye` değerini korur, devralınan değer `seviye_nihai` alanındadır. Özel Durum İPC'si (kural 5) vakaya bağlanabilir ama etiket üretmez.
17. Kişi adı, TCKN ve MKK sicil no etiket tablosuna ve tez çıktılarına alınmaz; alıntı alanında "Ad SOYAD" kalıpları `[KİŞİ]` ile maskelenir. Kişi sayısı (`kisi_sayisi`, maskeli TCKN sayısı) saklanır. İPC tutarı v1'de çıkarılmaz (tablo satır yapısı güvenilir toplam vermiyor).
18. Eylem türü (`manipulasyon_tipi`) VI-104.1 Tebliği atıflarından ve SPKn 107 fıkrasından türetilir; Tebliğ metni `kaynak-vi-104-1-piyasa-bozucu-eylemler-tebligi.md` dosyasındadır. Bent/fıkra atfı, tablo hücreleri iç içe geçse de yakalanır (madde 4–7, bent harfleri ayrı alanda). Eşleme (yalnızca Tebliğ metnindeki ifadeler; yorum eklenmemiştir):
    - md 5/1 (emir/işlem): (a) alım-satım, hesap hareketi, emir verme/iptal/değiştirme `emir_islem_genel`; (b) farklı fiyat kademelerine emir `kademe_emri`; (c) bir dakikadan kısa sürede yön değiştiren emir `yon_degistiren_emir`; (ç) kendinden kendine veya karşılıklı işlem `karsilikli_veya_kendinden_islem`; (d) açılış/kapanış fiyatını etkileme `acilis_kapanis_fiyati`; (e) gün sonu/vade sonu uzlaşma fiyatı `uzlasma_fiyati`; (f) fiyat yükseltici/düşürücü/sabit tutucu işlem `fiyat_etkileme`; (g) VİOP pozisyon limiti `viop_pozisyon_limiti`; (ğ) VİOP dayanak aynı yönlü `viop_dayanak_ayni_yonlu`.
    - md 6 (iletişim): 6/1 `yanlis_bilgi_haber_yorum`; 6/2 `yanlis_bilgi_yayma`; 6/3 `aciklama_yukumlulugu_ihlali`; 6/4 `tavsiye_sonrasi_ters_islem` (al/tut tavsiyesi verip 5 işgünü içinde satma veya tersi).
    - md 4 (içsel bilgi): 4/2 `icsel_bilgi_aktarma_veya_islem`; 4/3 `finansal_tablo_donemi_islem`; 4/4 `icsel_bilgi_donemi_islem`. md 7: 7/1 `emir_oncesi_islem`; 7/2 `baskasinin_hesabi`; 7/3 `pay_tebligi_md27`; 7/4 `islem_yasagi_ihlali`.
    - SPKn 107 (suç duyurusu/tedbir): 107/1 `islem_bazli_piyasa_dolandiriciligi`; 107/2 `bilgi_bazli_piyasa_dolandiriciligi` (bülten metni: "işlem bazlı" / "bilgi bazlı"); fıkrasız 104 atfı `md104_piyasa_bozucu_eylem_belirsiz_tur`.
    - Bentler eylemin hukuki nitelemesidir; bir emir/işlem deseninin (ör. katmanlama, sahte emir) gerçekleştiğini kanıtlamaz. Tebliğde "spoofing" veya "layering" terimi geçmez; `kademe_emri` (md 5/1-b) ve `yon_degistiren_emir` (md 5/1-c) bu davranışlara en yakın bentlerdir, eşleme kullanıcı kararıdır.
19. V-101.1 Tebliği md 15 (yasaklı kişilerin hesabından kredili satış/tasfiye) aracı kurum ihlalidir; VI-104.1 veya 107 atfı yoksa kayıt üretmez (2024-59, 2026-10).
20. İPC kayıtlarında `madde`: VI-104.1 atfı varsa ("VI-104.1", satır/hücre sonunda bölünmüş "VI-
21. Atıf edilen karar arşiv dışındaysa (örn. 05.06.2023, 18.08.2023, 03.11.2023 kararları; bülten arşivi yalnızca 2024–2026): bağlantı kurulmaz, `baglanti_belirsiz=0`, `baglanti_disarida=1`, kayıt kendi `seviye` değerinde (C) kalır; donörden dönem veya yasak başlangıcı devralınmaz. Gerekçe: bu kayıtları atıf dışı rastgele başka bir tedbire bağlamak yanlış dönem/pencere üretir.
22. Aynı bültende aynı paya ait suç duyurusu, o bültendeki kesin tedbir (`tedbir_kesin`) kaydı bir donöre bağlıysa aynı donöre bağlanır (`baglanti_notu=kural22_ayni_bulten`); kesin tedbirin bağı kural 21 gereği koparsa suç duyurusu da donörsüz kalır (`kural22_kardes_disarida`). Gerekçe: bülten suç duyurusundan "Bakınız 3. Diğer Yaptırım, Tedbir ve İşlem Yasakları" ile aynı bültendeki yasağa çapraz atıf yapar; KRGYO 2025-45'te suç duyurusu ve kesin yasak aynı kişiye (2025-11'deki yasaklı) aittir, 2025-28'deki yasaklı başka kişidir. Kardeşin donörsüz kalması bu kayıtların aynı kişi/olay olduğunu kanıtlamaz; bülten çapraz atfına dayalı bir varsayımdır.
104.1" veya açık yazılmış "Piyasa Bozucu Eylemler Tebliği") `104` bayrağı her zaman birlikte yazılır (`104,VI-104.1`). Gerekçe: VI-104.1, SPKn md 104'e dayanan Tebliğdir (dayanak: Tebliğ başlığı); bayrak, metinde ayrıca "104" yazıp yazılmadığını göstermez.

## Etiket seviyeleri

| Seviye | Koşul | Hisse-gün etiketi |
|---|---|---|
| A | Pay kodu + açık dönem + kural 4 dayanağı | Dönemin işlem günleri "şüpheli" |
| B | Pay kodu + yasak başlangıcı, dönem yok (`tedbir_gecici`, `tedbir_kesin`) | Bitiş = başlangıçtan 3 iş günü önce (önceki 2 iş günü belirsiz, değerlendirme dışı); başlangıç N = 20 işlem günü (duyarlılık analizi N = 10, 40) |
| C | Pay kodu + dönemsiz İPC/suç duyurusu | Etiket yok; vaka kaydı; aynı vakaya bağlanan A veya B kaydı varsa o seviye devralınır |
| D | Kodsuz, "muhtelif", varant | Etiket yok; vaka kaydı |

Etiketsiz gün negatif değildir (bilinmiyor). Etiketler sağdan kesiktir: karar gecikmesi 1–2 yıldır, pencerenin son ayları eksik kalır.

## Çıktı tabloları

`vaka`: `vaka_id | pay_kodu | unvan | arac_tipi | tur | madde | donem_bas | donem_bit | donem_kesinligi | tedbir_bas | tedbir_sure | karar_tarihi | bulten | bulten_tarihi | sayfa | kisi_sayisi | ipc_tutari_toplam | etiket_uygun | seviye | alinti | dogrulandi`
`olay`: `olay_id | tur | bas | bit | kapsam | karar_tarihi | bulten | atif_bulten | alinti | dogrulandi`

## Açık sorular

- [DOĞRULANDI 12.10.2026] VI-104.1 bent/fıkra eşlemesi Tebliğ metniyle yapıldı (kural 18); 188 İPC kaydının 188'inde atıf çıkarıldı. Metin 21.01.2014 yayımıdır. [DOĞRULANDI 19.10.2026, RG 18.02.2017 – 29983 metni] VI-104.1.a md 6/1-2'ye "fiilden önce veya sonra ilgili araçta her türlü emir ve/veya işlem" şartını ekledi, md 8'i tek fıkra olarak değiştirdi; kaynak dosyadaki md 6 ve 8 buna göre güncellendi. Etiket adları (`yanlis_bilgi_haber_yorum`, `yanlis_bilgi_yayma`) ve bent eşlemesi etkilenmez; md 6/1-2 vakalarında eylemin unsuru emir/işlem de olduğundan ITCH'te ilgili kişinin işlemleri aranabilir (bu bir tespit ipucudur, kanıt değildir). 2017 sonrası başka değişiklik kontrol edilmedi.
- [DOĞRULA] `tedbir_kesin` (2 yıl) kayıtlarının dönemi: karar gerekçesinde dönem yazmıyorsa (2026-37) B seviyesi geçerli mi, yoksa ilgili suç duyurusunun dönemi mi alınmalı.
- [DOĞRULANDI 22.10.2026] B seviyesi için başlangıç varsayımı **N = 20 işlem günü** (yaklaşık 1 takvim ayı). Duyarlılık analizi N = 10 ve N = 40 ile yapılır. Uygulama kararı (kullanıcı, 22.10.2026): seçim Claude'a bırakıldı; gerekçe aşağıdadır.
  - [BİLGİ 22.10.2026] `vaka.csv`'de dönemi gün düzeyinde yazılı 12 benzersiz vaka var (11 A, 1 D). Dönem uzunlukları işlem günü olarak 2, 6, 8, 8, 20, 23, 24, 31, 33, 41, 78 ve 131'dir; ortanca 23,5, çeyrekler 8 ve 35. Sayım hafta içi günlerle yapıldı, resmî tatiller düşülmedi.
  - [BİLGİ 22.10.2026] Dönemi ve geçici yasağı birlikte bilinen 4 vaka (EUREN 6, ALKLC 8, TDGYO 23, KRGYO 33 işlem günü) B seviyesinin doğrudan örneğidir. Dördünde de dönem bitişi ile yasak başlangıcı arasında 3 hafta içi gün vardır.
  - [BİLGİ 22.10.2026] Pencere ile gerçek dönem karşılaştırıldı. Kapsama, dönemin pencereye düşen payıdır. Saflık, pencerenin dönem içinde kalan payıdır. İkisinin F1'i hesaplandı; pencere sonu dönem sonuna hizalandı.

    | N | 12 vaka: kapsama | 12 vaka: saflık | 12 vaka: F1 | 4 tedbir vakası: kapsama | 4 tedbir vakası: saflık | 4 tedbir vakası: F1 |
    |---|---|---|---|---|---|---|
    | 10 | 0,54 | 0,87 | 0,66 | 0,68 | 0,85 | 0,76 |
    | 15 | 0,64 | 0,80 | 0,71 | 0,78 | 0,73 | 0,75 |
    | 20 | 0,74 | 0,77 | 0,75 | 0,87 | 0,68 | 0,76 |
    | 25 | 0,81 | 0,72 | 0,76 | 0,94 | 0,62 | 0,75 |
    | 30 | 0,85 | 0,67 | 0,75 | 0,98 | 0,56 | 0,71 |
    | 40 | 0,90 | 0,57 | 0,70 | 1,00 | 0,44 | 0,61 |

  - Gerekçe: N = 20 iki kümede de F1'in en yüksek olduğu bölgededir (0,75 / 0,76). N = 25 aynı F1'i daha düşük saflıkla verir. Etiketsiz gün negatif sayılmadığı için (bkz. Etiket seviyeleri) saflık kapsamadan önemlidir. N = 20 dönem ortancasına (23,5) yakındır ve 1 aya karşılık gelir. n = 12 küçüktür; N = 10 ve 40 duyarlılık analizi olarak kalır.
  - [DOĞRULANDI 22.10.2026 – kullanıcı kararı] Pencere bitişi. Gözlenen 4 vakada (EUREN, ALKLC, TDGYO, KRGYO) dönem, yasaktan 3 iş günü önce biter. Uygulama kararı (kullanıcı, 22.10.2026): B penceresi yasaktan 3 iş günü önce biter; yasaktan önceki 2 iş günü "belirsiz" sayılır ve değerlendirmeden çıkarılır (ne pozitif ne negatif). Gerekçe: eski kural (bitiş = yasaktan önceki iş günü) her pencereye 4/4 vakada dönem dışında kalan 2 gün katıyordu (20 günlük pencerede pozitiflerin ≈ %10'u); boşluk SPK inceleme penceresinin kesilmesinden de kaynaklanabileceği için bu 2 gün negatif de sayılmaz. Kanıt 4 A vakasına dayanır; yeni A vakalarıyla yeniden kontrol edilir.
- [DOĞRULA] Kural 13: geçici yasağın kaldırıldığı veya uzatıldığı bültenlerde (varsa) bitiş tarihinin nasıl yazıldığı henüz görülmedi.
- [DOĞRULANDI 19.10.2026] `2024-4.pdf`: PDF başlığı "2024/04 18/01/2024" (bülten 4, 18.01.2024). `ad_no_uyumsuz=True` yalnızca iç numaranın sıfır dolgulu (`2024/04`) yazılmasından gelen sahte uyumsuzluktu; betik artık sıra numarasını tamsayıya çevirir (`2024/4`) ve `bulten_indeks.csv`'de uyumsuz bülten kalmadı. `2024 15.pdf` dosyası `2024-15.pdf` yapıldı.
- [DOĞRULA] Kural 13: `tedbir_bas` ile dönem bitişi arasındaki ilişki yalnızca 3 vakada (KRGYO, TDGYO, ALKLC) ve EUREN'de (dönem 14–21.04.2025, tedbir 24.04.2025) görüldü; hepsinde dönem bitişi yasak başlangıcından 1–3 gün önce.
- [DOĞRULANDI 19.10.2026] `madde` alanında "104" bayrağı tutarsızdı (VI-104.1 ile birlikte yalnızca bir kısmında çıkıyordu): bayrak, metinde ayrıca "SPKn 104" ifadesi geçip geçmediğine bağlıydı; VI-104.1 ise SPKn md 104'e dayanır. Ek olarak 10 İPC kaydında VI-104.1 `madde` alanına hiç yazılmıyordu ("VI-" ile "104.1" satır/hücre sonunda bölünmüş veya Tebliğ adı açık yazılmış). Kural 20 ile standartlaştırıldı; 188 İPC kaydının 188'inde `madde = 104,VI-104.1`.
- [DOĞRULANDI 12.10.2026] Olay tablosu (19 kayıt) kaynak metinle karşılaştırıldı; 2026-19, 2026-57, 2026-63, 2025-16 sorunları düzeltildi (`dogrulama-kaydi.md`, bulgu 7–9).
- [DOĞRULANDI 19.10.2026] Önceki 5 belirsiz bağlantı kural 21–22 ile çözüldü: AVHOL 2025-55, CEOEM 2026-4, BJKAS 2025-32 kesin tedbirleri ve aynı bülten/paydaki suç duyuruları donörsüz (C) kaldı; KRGYO 2025-45 suç duyurusu 2025-11'e (A) bağlandı. Kalan belirsiz bağlantı: yalnızca ENSRI 2026-6 İPC'si (atıf yok; aynı payda 2024-40 ve 2025-22 iki aday, en yakın önceki seçildi). Kalan [DOĞRULA]: ENSRI.
- [DOĞRULA] Kural 8 sözlüğü: ITCH `R` mesajlarındaki unvan alanının SPK bülteni unvanlarıyla (yazım farkları: "AŞ", "A.Ş.", "TAŞ") eşleşme oranı ölçülmedi. Kodsuz kayıtlar için bkz. aşağıdaki [DOĞRULANDI 19.10.2026] Kural 8 kontrolü.
- [DOĞRULANDI 19.10.2026] Kural 8, pay kodu boş kayıtlar: 337 kod satırından 31'inde `pay_kodu` boştu. Hepsi "genel karar" değildi: (a) 11 İPC kaydında belirli şirket unvanı var, kod yok (Metemtur Yatırım Enerji, Mega Polietilen Köpük, Martı Otel, Sanica Isı, İzmir Fırça, Global Yatırım Holding, Esenboğa Elektrik, Naturel Yenilenebilir Enerji, Margün Enerji, Allbatross Portföy, Hidropar); bunlar artık `sirket_unvani` sütununda, kod sözlükle bulunacak, `etiket_uygun=0` kalır; (b) 3 İPC kaydında kod parantezsiz yazılmıştı ("ASUZU pay piyasasına", 2026-34), betik bu kalıbı da yakalar, kayıtlar kodlu oldu; (c) kalan 17 kayıt "Borsa İstanbul AŞ pay piyasaları" / "muhtelif pay piyasaları" / kimliği [KİŞİ] ile verilmiş şahıs / kişi listesi (2025-49, 2026-29, 2026-6, 2026-14 vb.) olup şirket veya kod içermiyor. Kural 10 ile uyumlu: kural değişmedi, hisse-gün etiketi üretilmez. Kod önerileri kullanıcıdan alındı (`kod_unvan_eslemesi.csv`, ITCH ile doğrulanmadı; yalnızca ESEN ve HKTM bültenlerde kodlu geçiyor); `vaka.csv`'ye işlenmedi. Allbatross Portföy bir pay değil yatırım kuruluşudur, `etiket_uygun=0` kalır (kullanıcı notundaki "Yatırım Menkul Değerler" yerine bülten unvanı "Portföy Yönetimi AŞ" esas alındı). Pencere sonucu değişmedi (47 satır). Seviye dağılımı: D 146→143, C 93→96.
- [BİLGİ] Taban oranı: rastgele 20 bültenin 4'ünde (2024-1, 2024-3, 2024-50, 2026-44) manipülasyon kaydı var; 2'sinde piyasa olayı (2026-27, 2026-30); 14'ünde hiçbiri.

## Çalıştırma sonucu (197 bülten, 12.10.2026)

| Ölçü | Değer |
|---|---|
| Bülten / hata | 197 / 0 |
| Vaka kaydı / kod satırı | 233 / 337 |
| Tür (kod satırı) | İPC 188, `tedbir_gecici` 59, `tedbir_kesin` 37, `suc_duyurusu` 33, `lisans_iptali` 18, `tedbir_uzatma` 2 |
| Seviye (ham → bağlama sonrası) | A 13 → 16, B 56 → 76, C 125 → 102, D 143 → 143 |
| Bağlanan kayıt / belirsiz bağlantı / arşiv dışı atıf (bağ kopuk) | 23 / 1 / 3 kesin tedbir + 3 suç duyurusu |
| Pencere (01.06.2024–31.05.2025) ile kesişen | 43 kod satırı (önce 47), 28 benzersiz kaynak vaka (donör anahtarı: A 6, B 22; değişmedi), 27 pay |
| Olay kaydı | 19 (açığa satış, geri alım, öz kaynak oranı) |
| Elle doğrulama | 47 pencere kaydı + 19 olay kaydı PDF metniyle karşılaştırıldı: `dogrulama-kaydi.md` |
| Bölüm bulunamayan bülten | 5 (hiçbirinde ilgili anahtar kelime yok) |

Pencere ölçütü: A için dönem pencereyle kesişir; B için `tedbir_bas` ∈ [01.06.2024, 31.05.2025 + 60 gün] (N ≤ 40 işlem günü varsayımı).

## Test örnekleri

| Bülten | Beklenen kayıt |
|---|---|
| 2024-3 (17/01/2024) | HATEK, `tedbir_gecici`, 107/1, tedbir_bas 18.01.2024, 6 ay, 3 kişi, seviye B |
| 2024-8 (02/02/2024) | YAYLA, `tedbir_gecici`, 107/2, tedbir_bas 05.02.2024, 6 ay, 2 kişi, seviye B |
| 2024-21 (25/04/2024) | DERIM, `ipc`, VI-104.1 md 6/1, dönem 02.03.2023–29.03.2023, 2 kişi, seviye A |
| 2024-44 (05/09/2024) | PCILT, `ipc`, VI-104.1 md 6/4, dönem 28.07.2023–31.07.2023, 5 kişi, seviye A |
| 2024-50 (03/10/2024) | ASUZU `ipc` (md 6/1, 23 kişi, seviye C); THYAO, DOCO, PGSUS, VAKKO, FROTO, AKSEN, PETKM `ipc` (md 6/4, 7 kod, `muhtelif=1`, seviye D, kural 10); açığa satış ihlali İPC'si hariç (kural 5) |
| 2025-11 (27/02/2025) | KRGYO dönem 10.01.2025–25.02.2025, TDGYO dönem 24.01.2025–25.02.2025, `tedbir_gecici`, 104 veya 107, tedbir_bas 28.02.2025, seviye A |
| 2025-49 (18/09/2025) | Genel suç duyurusu `etiket_uygun=0`; 2 yıl `tedbir_kesin` 14 kişi `etiket_uygun=0`; ALCTL `ipc` md 5/1 (a), (b), (ç) seviye C; 26 kodlu X platformu İPC'si seviye D (`muhtelif=1`, kural 10) |
| 2025-62 (10/12/2025) | KZBAZ.V `arac_tipi=varant`, dayanak KOZAL, hisse etiketi üretmez |
| 2026-37 (12/06/2026) | DERHL `suc_duyurusu` 107/2 + `tedbir_kesin` 2 yıl, tedbir_bas 11.06.2026, karar_tarihi 10.06.2026 (35/1096), Alnus kendi nam ve hesabına, seviye B |
| 2026-27 / 2026-30 | `olay`: açığa satış yasağı uzatma (08.05.2026, 26.05.2026), atıf zinciri 2026/24 → 2026/27 → 2026/30 |
