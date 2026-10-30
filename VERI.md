# Elimizdeki BIST verisi

Ne var, ne işe yarıyor, bir pay hakkında ne biliyoruz · Bitirme projesi · 30.10.2026

Bu belge verinin kısa özetidir. Ayrıntılar `veri/README.md`'de (klasör düzeni, dönüşüm ve kayıpsızlık kontrolleri), alan tanımları `veri/datastore-dosya-formatlari.md`'de ve `veri/gunici-veri-dogrulama.md`'de (alanların anlamı, Mart 2025 doğrulamaları) bulunur.

## 1. Dosyalar

| Dosya | İçinde ne var | Dönem | Ne işe yarıyor |
|---|---|---|---|
| **Gün içi emir** | Her emrin her hareketi: giriş, değişiklik, iptal, işlem, süre dolumu | 2024-01 … 2025-06 | Emir defterini yeniden kurmak, motoru gerçek emirlerle tekrar oynatmak, sahte emir göstergeleri |
| **Gün içi işlem** | Gerçekleşen her işlem (alış ve satış tarafı ayrı) | 2024-01 … 2025-06 | Motorun doğruluğunu ölçmek (gerçek işlemlerle birebir karşılaştırma); getiri, alış-satış baskısı |
| **Gün sonu fiyat-hacim** | Her payın günlük özeti | 2024-01 … 2025-06 | Baz fiyat ve fiyat sınırları, pazar kuralları, günlük hacim, tedbir ve sermaye işlemi günleri |
| **Gün içi endeks** | 75–77 endeksin saniyelik değeri | 2024-01 … 2025-06 | Endekse bağlı devre kesici eşiği; o an piyasanın sakin mi hareketli mi olduğu |
| **Değerleme oranları** | Şirketlerin ay sonu finansal göstergeleri | 2024-01 … 2025-06 | Küçük / büyük pay ayrımı, sektör bilgisi |
| **ITCH** | Borsanın canlı veri akışı mesajları | Yalnız 08.10.2018 | Emir defteri kurallarının (öncelik vb.) çapraz kontrolü |

Büyüklük: ayda 0,7–1,1 milyar emir satırı ve 0,17–0,35 milyar işlem satırı. 18 ayın hepsi dönüştürüldü ve doğrulandı; emirler gün gün bölümlendi. Tarih parametreleri (fiyat marjı, devre kesici vb.) 18 ayın hepsinde ölçüldü; motor 2024-01-02 … 2025-06-30 arasında çalışır (`motor/parametreler.py` `VERI_DONEMI`, `rapor.md` 15).

## 2. Bir pay hakkında elimizdeki bilgiler

| Bilgi | Açıklama | Dosya |
|---|---|---|
| **Kimlik ve sınıflandırma** | | |
| Pay kodu ve adı | Örn. THYAO.E | Gün sonu |
| Pazar (Yıldız, Ana, Alt Pazar vb.) ve alt bölüm | Pazar kurallarını belirler | Gün sonu |
| İşlem yöntemi: sürekli işlem ya da tek fiyat | Günlük | Gün sonu |
| BIST 100 / BIST 30 üyeliği, piyasa yapıcı var mı | Günlük | Gün sonu |
| Sektör ve ana sektör | Aylık | Değerleme |
| **Fiyat** | | |
| Önceki kapanış (baz fiyat), açılış, en düşük, en yüksek, kapanış, ağırlıklı ortalama fiyat, referans fiyat | Günlük | Gün sonu |
| Her işlemin fiyatı ve zamanı | Mikrosaniye | İşlem |
| Her emir olayı anında en iyi alış ve en iyi satış fiyatı | Makas, en iyi fiyata uzaklık | Emir |
| **Hacim** | | |
| Günlük toplam hacim (TL), adet ve işlem sayısı | Günlük | Gün sonu |
| Açılış seansı, kapanış seansı ve kapanış fiyatından işlemlerin hacmi | Günlük | Gün sonu |
| Her işlemin adedi, TL hacmi ve işlemi başlatan taraf (alıcı mı satıcı mı) | İşlem başına | İşlem |
| **Emirler ve emir defteri** | | |
| Her emrin fiyatı, miktarı, kalan ve görünen miktarı | Her olayda güncel hâli | Emir |
| Emir tipi (limit, piyasa, piyasadan limite…) ve geçerlilik (gün, kalanı iptal et) | | Emir |
| Emrin başına gelen her şey: yeni, değişiklik, iptal, işlem, süre dolumu | Emrin ömrü ölçülebilir | Emir |
| Açığa satış emri mi; günlük açığa satış özeti | | Emir, Gün sonu |
| AFK (emir aracısı / fon kodu) | Kimlik değil | Emir |
| Emir defterinin herhangi bir andaki hâli | Motorla yeniden kurulur | Emir → motor |
| Gün sonunda defterde kalan alış ve satış miktarı | Günlük | Gün sonu |
| **Seans ve durum** | | |
| Olayın hangi bölümde olduğu: açılış, sürekli işlem, kapanış, devre kesici… | Her satırda | Emir, İşlem |
| İşleme kapalı mı, brüt takas (tedbir), sermaye artırımı / temettü günü | Günlük | Gün sonu |
| **Şirket ve değerleme** | | |
| Piyasa değeri, özsermaye, son 4 çeyrek net kâr, nakit temettü | Aylık, ay sonu | Değerleme |
| F/K, PD/DD, temettü verimi | Aylık, ay sonu | Değerleme |
| **Piyasa bağlamı** | | |
| BIST 100, BIST TÜM ve sektör endekslerinin değeri | Saniyelik | Endeks |
| Aynı gün bütün payların özeti (kesitsel karşılaştırma için) | Günlük | Gün sonu |

## 3. Elimizde olmayanlar

- **Kimin emir verdiği (üye, hesap no).** Aynı kişinin emirleri birbirine bağlanamaz; olağan boyda kendi kendine alıp satma (karşılıklı işlem) görülemez.
- **Yatırımcı türü:** yerli / yabancı, bireysel / kurumsal ayrımı yok.
- **Haberler ve KAP bildirimleri:** yanlış haberle yapılan (bilgi bazlı) manipülasyon bu veriyle görülemez.
- **Hazır emir defteri görüntüsü:** defter, emir olaylarından motorla yeniden kuruluyor.

> SPK etiketleri (hangi payda hangi dönemde manipülasyon olduğu) BIST verisi değildir; SPK haftalık bültenlerinden çıkarıldı (`veri/etiketler/vaka.csv`). 18 ayda değerlendirmeye giren 34 pay: A seviyesi 4 pay (93 pay-gün), B seviyesi 31 pay (582 pay-gün); KRGYO ikisinde de var (`rapor.md` 14).

## 4. Dosyaların yeri

Ham veri git dışıdır (`.gitignore`). Bütün dosyalar parquet'e çevrilmiştir.

| Dosya | Yol |
|---|---|
| Gün içi emir | `veri/gun-ici-emir/gunluk/YYYY-MM-DD/{pay,varant}-{0..7}.parquet` (gün ve sıra kovasına bölünmüş, 371 gün, motorun girdisi); aylık `PP_GUNICIEMIR.M.YYYYAA.parquet` dosyaları harici diskte (F:) |
| Gün içi işlem | `veri/gun-ici-islem/PP_GUNICIISLEM.M.YYYYAA.parquet` |
| Gün sonu fiyat-hacim | `veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.YYYYAA.parquet` |
| Gün içi endeks | `veri/gun-ici-endeks/PP_GUNICITUMENDEKS.M.YYYYAA.parquet` |
| Değerleme oranları | `veri/degerleme-orani/degoran_M_YYYYAA.parquet` |
| ITCH | `veri/itch/2018-10-08/` |
| SPK etiketleri | `veri/etiketler/vaka.csv` |
| Pay-gün özellik tablosu (18 ay, 211.698 pay-gün) | `veri/gunici-dogrulama/2024-01_2025-06/tespit/ozellikler.parquet` |
