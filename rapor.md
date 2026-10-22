# Çalışma raporu

Bu dosya, bitirme projesi vize raporunun yazılacağı kaynak kayıttır. Önce 21.10.2026'ya kadar yapılanlar özetlenir, sonra oturumlar tarih başlığı altında ayrıntılı kaydedilir. Ayrıntılı teknik sonuçlar ilgili dosyalardadır; bu raporda yalnız özetleri ve sayıları vardır.

**Proje:** "Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi" (bilgisayar mühendisliği bitirme projesi, tek kişilik).

**Üç bileşen:**
1. Tarihsel emir ve işlem verisinden emir defterinin yeniden kurulması (veri katmanı).
2. Borsa İstanbul (BIST) kurallarına uygun eşleştirme motoru: sürekli işlem, tek fiyat (müzayede), devre kesiciler. Gerçek emir akışı tekrar oynatılır, araya sentetik manipülatif emirler enjekte edilir.
3. Manipülasyon tespiti: iktisadi kurallar, denetimsiz model ve denetimli model; SPK vakalarıyla değerlendirme.

---

## 1. 21.10.2026'ya kadar yapılanların özeti

### 1.1 Kaynakların derlenmesi ve aktarımı

- **Pay Piyasası Prosedürü ekleri:** Ek-1 … Ek-21 (s. 104–380) tek tek markdown'a aktarıldı (`ekler/ek1.md` … `ek21.md`, `ekler/README.md`).
  - Tablolar, sayfadaki kenarlık çizgilerinden kurularak sütun kayması olmadan çıkarıldı.
  - Her sayfada kelime kaybı 0 olduğu otomatik denetlendi.
  - Ek-16 ve Ek-18 tablolarında aritmetik tutarlılık (kümülatif toplam, işlem = min(alış, satış)) kontrol edildi.
  - Ek-10 akış tablolarında satır ve saat sırası kontrol edildi.
  - Seçili sayfalar görüntüyle karşılaştırıldı. Tüm ekler kullanıcı tarafından doğrulandı.
- **Protokol ve veri belgelerinin Türkçe çevirileri (`veri/`):**
  - BIST ITCH 2112 (piyasa verisi yayını),
  - MoldUDP64, SoupBinTCP (taşıma katmanları),
  - OUCH (emir iletimi),
  - FIX Reference Data ve FIX Order Entry (kapsamı sınırlı),
  - "Emrimle Eşleşmesin" (SMP) teknik çalışma esasları,
  - DataStore dosya formatları (sürüm 1.4; 121 tablo).

### 1.2 Kural dosyaları (`kurallar/`)

Prosedürden motorun kodlanmasında kullanılacak, madde numaralı ve kaynak gösterimli 8 kural dosyası yazıldı:

| Dosya | Kapsam | Madde |
|---|---|---|
| `01-seanslar.md` | Seans saatleri, bölümler/aşamalar, geçici durdurma, seans uzama/iptal | 92 |
| `02-fiyat.md` | Lot, fiyat adımı, baz/referans fiyat, fiyat değişme sınırları, AOF, maddi hata | 47 |
| `03-tek-fiyat.md` | Tek fiyat yöntemi, 9 adımlı denge fiyatı algoritması, kapanış seansı, kapanış fiyatından işlemler | 99 |
| `04-surekli-islem.md` | Sürekli işlem, fiyat-zaman önceliği, değişiklikte öncelik, SMP | 48 |
| `05-emirler.md` | Emir tipleri, değiştirme/iptal, değer sınırları, geçerlilik, Ek-19 bölüm × emir tipi matrisi | 143 |
| `06-devre-kesici.md` | Pay bazında devre kesici, endekse bağlı devre kesici (EBDKS) | 53 |
| `07-itch.md` | ITCH mesaj kuralları, veri tipleri, emir defteri görünümü | 68 |
| `08-pazarlar-tedbirler.md` | Pazarlar, piyasa yapıcılık, brüt takas, gruplama, bülten | 55 |

Kurallar:
- Belirsiz ya da çelişkili noktalar yorumlanmadı; her dosyanın "Açık sorular" bölümüne [DOĞRULA] ile yazıldı.
- Belgeler arası çelişkiler kullanıcı kararıyla kapatıldı. Örnekler:
  - gün "tek seans", parçalar "bölüm/aşama" olarak adlandırılır;
  - açılışta piyasa emri yalnız Yıldız ve Ana Pazar'da girilebilir;
  - askıya alma = iptal + yeni emir;
  - marj dışı kalan tarihli emirler gün başında iptal edilir, gün içi limit kaymasında emir duraklatılır.
- Prosedür örnekleri (Ek-16 açılış fiyatı örnekleri, Ek-18 emir tipi örnekleri) "Test örnekleri" bölümlerine motorun birim testleri olarak aktarıldı.
- Proje kökünde `CLAUDE.md` (dizin ve kararlar) ile `DURUM.md` (durum notu) oluşturuldu. 10.10.2026'da iki commit yapıldı.

### 1.3 ITCH örnek verisi doğrulaması (08.10.2018; `veri/itch-ornek-veri-dogrulama.md`)

- **Dosya biçimi:** DataStore'dan alınan tek günlük ITCH örneğinde ikili `.VRD` dosyalarının biçimi çözüldü. Dosya, MoldUDP64 başlığı olmadan `[2 bayt uzunluk][mesaj]` dizisidir.
- **Çözümleyici:** Metin (TXT) çıktısıyla 5.615.765 mesajda alan alan karşılaştırıldı; fark 0.
- **Defter kurma:**
  - emir defteri yeniden kurma (zaman geri gitmesi, bilinmeyen emir, negatif kalan: 0),
  - fiyat adımı tabloları (2018 verisi eski Tablo-7'ye uyar),
  - seans durum adları ve Ek-10 akışlarıyla karşılaştırma,
  - fiyat-zaman önceliği (fiyat önceliği ihlali 0),
  - değişiklikte öncelik kaybı/korunması,
  - devre kesici süreleri.
- **Ana kısıt:** ITCH'te müzayede (emir toplama) aşamasındaki emirler yayımlanmadığından tek fiyat algoritması bu veriyle sınanamadı. Bu kısıt, 21.10.2026'daki veri kararının gerekçelerinden biridir.

### 1.4 SPK bülten etiketleme (12.10.2026 ve 19.10.2026; `veri/etiketler/`)

- 2024–2026 dönemine ait 197 SPK bülteni (PDF) işlendi.
- Etiket çıkarım kuralları yazıldı (`etiket-cikarim-kurallari.md`, 22 kural, 4 etiket seviyesi).
- Betik (`veri/araclar/spk_bulten_etiket.py`) çıktıları: `vaka.csv` (340 kod satırı), `olay.csv` (19 kayıt), `vaka_pencere_dogrulama.csv`.
- Etiket seviyeleri:
  - **A:** manipülasyon dönemi kesin olarak yazılı;
  - **B:** yalnız işlem yasağı (tedbir) tarihi biliniyor, dönem tedbirden önceki N işlem günü varsayılır.
- 47 pencere kaydı ve 19 olay kaydı PDF metniyle elle karşılaştırıldı; 10 sınıflandırma/bağlama hatası düzeltildi (`dogrulama-kaydi.md`).
- VI-104.1 Piyasa Bozucu Eylemler Tebliği metni eklendi; ihlal bentleri `manipulasyon_tipi` olarak çıkarıldı.
- Açığa satış yasağı tarihçesi bültenlerden çıkarıldı.

---

## 2. 21.10.2026 — Veri kaynağı değişikliği, Mart 2025 doğrulamaları ve sistem tasarımı (sürüm 2)

### 2.1 Veri kaynağı kararı

**Kullanıcı kararı:** ITCH verisi yalnız 2 aylık örnek olarak alınacak. Ana veri Borsa İstanbul DataStore'un gün içi dosyalarıdır:

| DataStore dosyası | İçerik |
|---|---|
| `PP_GUNICIEMIR` (gün içi emir) | Her emir olayından sonra emrin tam durumu: giriş, değişiklik, iptal, işlem, süre dolumu. Müzayede aşamaları dâhil |
| `PP_GUNICIISLEM` (gün içi işlem) | Her işlemin alış ve satış tarafı, iki tarafın emir numarası, aktif/pasif tarafı |
| `PP_GUNSONUFIYATHACIM` (gün sonu fiyat-hacim) | Sıra-gün bülteni: baz fiyat, pazar, işlem yöntemi, fiyat ve hacim özetleri |

Gerekçe: ITCH'te müzayede aşamasındaki emirler yayımlanmaz. DataStore emir dosyasında ise bütün emir olayları vardır. Böylece açılış, kapanış ve devre kesici müzayedeleri dâhil eşleştirme motoru uçtan uca doğrulanabilir.

### 2.2 Veri indirme ve parquet dönüşümleri (20–21.10.2026)

DataStore'dan aylık CSV (zip) dosyaları indirildi. Dosyalar kayıpsız tip dönüşümüyle Apache Parquet biçimine (zstd sıkıştırma) çevrildi. Dönüştürme betikleri:
- `veri/araclar/gunici_emir_csv2parquet.py`
- `veri/araclar/gunici_islem_csv2parquet.py`
- `veri/araclar/gunsonu_fiyat_hacim_csv2parquet.py` (gün sonu dosyasında her hücre kaynak metinle yeniden karşılaştırılır)

| Dosya | Aylar | Satır | Parquet boyutu | Dönüşüm tarihi |
|---|---|---|---|---|
| Gün içi emir | 2025-03 | 1.128.466.831 | 20,7 GB | 20.10.2026 |
| Gün içi emir | 2025-04 | 1.026.868.890 | 17,7 GB (CSV 209 GB) | 21.10.2026 |
| Gün içi emir | 2025-05 | 947.232.947 | 17,3 GB | 21.10.2026 |
| Gün içi işlem | 2025-03 … 2025-09 (7 ay) | 192–269 milyon/ay (toplam 1.640.155.088) | 3,2–4,5 GB/ay | 20–21.10.2026 |
| Gün sonu fiyat-hacim | 2025-03 … 2025-08 (6 ay) | 147–198 bin/ay | ≈ 3 MB/ay | 21.10.2026 |

Ham veri git dışıdır (`.gitignore`).

### 2.3 Veri hazırlama: günlük bölümleme

- Aylık emir dosyasında satır grupları 12 güne kadar yayıldığından gün ve pay bazında okuma pratik değildi.
- `veri/araclar/gunici_emir_gunluk_bol.py` ile Mart 2025 emir dosyası gün × araç grubu (pay / varant) × 8 kova olarak `veri/gun-ici-emir/gunluk/` altına bölümlendi.
  - Dosyalar `islem_kodu`, `emir_degistirilme_zamani`, `guncelleme_no` sırasındadır.
  - Satır toplamı aylık dosyayla aynıdır (1.128.466.831; kayıpsız).
- Bu yapı, motorun ve tüm doğrulamaların ortak girdisidir.
- Bellek (16 GB) ve süre kısıtları nedeniyle betikler pyarrow ile vektörel hâle getirildi. Örneğin bölümlemenin ilk sürümü saatler sürecekken son sürümü yaklaşık 1 saatte tamamlandı.

### 2.4 Mart 2025 verisiyle doğrulamalar (`veri/gunici-veri-dogrulama.md`)

20 işlem günü (03–28.03.2025) üzerinde yapılan kontroller ve ana sonuçlar:

| # | Kontrol | Sonuç |
|---|---|---|
| 1 | Alan anlamları | Zaman dilimleri çözüldü: emir zamanları İstanbul saati, µs; güncelleme zamanı UTC. Emir↔işlem anahtarı: `islem_numarasi = int(ortak_sozlesme_no, 16)`. Değişiklik sebepleri ve geçerlilik türleri belirlendi (yalnız Gün ve KİE; her gün bağımsız) |
| 2 | İşlem defteri ↔ gün sonu bülteni | 74.979 sıra-günde bütün bülten alanları işlemlerden yeniden üretildi: toplam/özel işlem 74.979/74.979, AOF 74.960/74.979 |
| 3 | Fiyat marjı | Tüm pazarlarda ±%10; 495 tavan ve 786 taban isabeti içe yuvarlanmış sınırlara tam eşit |
| 4 | Fiyat adımı | 797.067.974 emir fiyatında Tablo-7/8'e aykırı 0; 117 milyon işlemde yalnız 1 (özel işlem bildirimi) |
| 5 | Seans bölümleri ve saatler | 22 bölüm adı, Ek-10 akışlarıyla uyumlu; müzayede eşleşme anı aşama başına ortak rastlantısal saniye |
| 6 | Ek-19 (bölüm × emir tipi) | 230,8 milyon yeni emirde izin dışı tip 0 |
| 7 | Emir yaşam döngüsü | Açılışın son 5 dakikasında iptal/kötüleştirme/azaltma 0; EBDKS durdurmasında yalnız izinli değişiklikler; kapanış seansında ±%3 dışı %0,04 |
| 8 | Fiyat-zaman önceliği (3 gün, 9,6 milyon pasif gerçekleşme) | Fiyat önceliği %99,998; zaman önceliği %99,76 (öncelik kalan miktar artışında ve kısmi görünme yenilemesinde de kaybolur) |
| 9 | **Tek fiyat (müzayede) defterinin yeniden kurulması** | 29.633 müzayedenin 29.621'inde (%99,96) hesaplanan denge fiyatı gerçek fiyata eşit; Adım 4 referansı = baz fiyat; kapanışta son işlem ±%3 sınırı; dengeleyici emir eşleşmesi doğrulandı |
| 10 | Pay bazında devre kesici (1.195 olay) | Yalnız düşüş yönlü, %5 eşik, 15 dk emir toplama + 2 dk eşleştirme bölümü; eşleştirme ilk 30 sn'de rastlantısal |
| 11 | EBDKS | 19 ve 21 Mart'ta ikişer kez; `.E` sıraları 20 dk, `.V/.C/.F` 30 dk durdurma (01.09.2025 öncesi kural) |
| 12 | Açığa satış | 03–21.03 yalnız 50 payda (BIST 50), 24.03'ten itibaren 0 |

Doğrulamanın projeye katkısı:
- **Tek fiyat algoritması:** 2018 ITCH verisiyle sınanamayan algoritma, gerçek müzayede defterleriyle doğrulandı. Başvuru uygulaması `veri/araclar/tek_fiyat_algoritma.py`, birim testi `tek_fiyat_algoritma_test.py` (Ek-16'nın beş örneği).
- **Tarihe bağlı kurallar:** Veri tarihinde geçerli kuralların yürürlükteki Prosedürden farklı olduğu belirlendi: marj, devre kesici yönü/oranı/süresi, EBDKS eşikleri ve süreleri. Bunlar tarih parametresi olarak ayrıldı (`motor/tarih_parametreleri.csv`).
- **Kapanan açık sorular:** Kural dosyalarındaki bazı açık sorular veriyle kapandı:
  - tek fiyat Adım 4 referansı,
  - Ek-16 Örnek 3-B açıklaması,
  - açılışın son 5 dakikası kuralı,
  - AOF kapsamı,
  - piyasa emrinin yalnız KİE kullanılması,
  - değişiklik sebeplerinin anlamı.

### 2.5 Kullanıcı kararları (21.10.2026)

1. **Pay bazında devre kesici eşleştirmesi:** "Sabit saat" kararı kaldırıldı. Kural şöyle tanımlandı: emir toplama süresi sabit, eşleştirme tarihe bağlı rastlantısal tolerans penceresi içinde başlar (Mart 2025: 30 sn, 2018: 0 sn).
2. **Tablo-4 ile veri farkı:** Veride gözlenen fiili eşikler kullanılır. Fark "Borsa İstanbul Pay Piyasası Prosedürü Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak belgelendi.
3. **Tek fiyatta karışık yön:** Referansa / son işlem fiyatına en yakın aday seçilir, eşitlikte orta nokta alınır. Mart 2025'teki 4 vakanın 2'si kurala uyar, 2'si `yon_karisik_istisna = 1` ile işaretlendi.
4. **Veri ayları:**
   - Emir verisi 2025-04 ve 2025-05 başı.
   - ITCH örneği **2025-01 ve 2025-02**. Bu aylar A seviyesi SPK vakalarını kapsar: KRGYO 10.01–25.02.2025, TDGYO 24.01–25.02.2025, ALKLC 04.02–18.03.2025.
   - 2025-01 ve 2025-02 için DataStore gün içi emir ve gün içi işlem dosyaları da indirilecek. Böylece aynı günlerde ITCH ve DataStore'dan kurulan defterler karşılaştırılabilir.
   - 2025-07 ITCH için alınmaz.
   - Güncelleme (22.10.2026): DataStore emir, işlem ve gün sonu verisi 2024-06…2025-05 arası alınır (12 ay; 12.10.2026 planından; gerekirse genişletilir). "2025-07 alınmaz" kararı yalnız ITCH içindir.
   - Ay-etiket karşılaştırması `veri/etiketler/ay_etiket_ortusmesi.csv` dosyasındadır.

### 2.6 Sistem tasarımı, sürüm 2 (`TASARIM.md`)

- **Veri katmanı:** DataStore gün içi verisi; hazırlama akışı (CSV → parquet → günlük bölümleme); sıra-gün referans tablosu; tarih parametresi tablosu.
- **Eşleştirme motoru:** İki çalışma modu vardır:
  - tekrar oynatma: gerçek emir niyetleri motora verilir, üretilen işlemler gerçekleriyle karşılaştırılır;
  - enjeksiyon: gerçek akışa sentetik aktörün emirleri eklenir.

  Bileşenler kural dosyalarına bağlandı.
- **Sentetik manipülasyon senaryoları:** kapanış/açılış fiyatını etkileme, yanıltıcı emir (spoofing/layering), adım adım fiyat yükseltme, karşılıklı işlem.
- **Tespit:** Veride üye/hesap kimliği olmadığından birim pay-penceredir. Özellik grupları: emir akışı, defter, işlem, referans. Modeller: kurallar, denetimsiz ve denetimli; değerlendirme SPK vakalarıyla.
- **ITCH'in rolü:** ikincil. Kamuya yayımlanan defter ve A seviyesi vaka dönemleri için kullanılır.

### 2.7 Belge güncellemeleri

- **Kural dosyalarına işlenen veri kanıtları:** 01, 02, 03, 04, 05, 06 ve 08'e [BİLGİ] / [DOĞRULANDI] / [KISMEN DOĞRULANDI] notları ve kullanıcı kararları eklendi.
- **Durum belgeleri:** `CLAUDE.md` (kararlar listesi, dizin), `DURUM.md`, `veri/README.md`, `.gitignore` güncellendi.
- **Son kontroller:**
  - bütün belgelerde tablo bütünlüğü kontrol edildi (hata 0);
  - anılan dosyaların varlığı ve betiklerin derlenmesi kontrol edildi;
  - sayıların belgeler arasında tutarlılığı kontrol edildi.

### 2.8 Bu oturumda üretilen dosyalar

| Tür | Dosya |
|---|---|
| Tasarım ve rapor | `TASARIM.md`, `rapor.md`, `veri/gunici-veri-dogrulama.md` |
| Parametre | `motor/tarih_parametreleri.csv` |
| Hazırlama betikleri | `gunici_emir_gunluk_bol.py`, `gunici_emir_profil.py` |
| Doğrulama betikleri | `gunici_islem_gunsonu_karsilastir.py`, `gunici_marj_kontrol.py`, `gunici_fiyat_adimi_sinir_kontrol.py`, `gunici_emir_sinir_disi.py`, `gunici_ek19_kontrol.py`, `gunici_emir_kural_kontrol.py`, `gunici_emir_kural_ozet.py`, `gunici_oncelik_kontrol.py`, `gunici_tek_fiyat_kontrol.py`, `gunici_tek_fiyat_ozet.py`, `gunici_tek_fiyat_karisik.py`, `gunici_eslestirme_zamani.py`, `gunici_seans_akis_kontrol.py`, `gunici_devre_kesici_kontrol.py`, `etiket_ay_ortusmesi.py` |
| Algoritma ve test | `tek_fiyat_algoritma.py`, `tek_fiyat_algoritma_test.py` |
| Çıktılar | `veri/gunici-dogrulama/2025-03/` (özet CSV/TXT), `veri/etiketler/ay_etiket_ortusmesi.csv` |

Betikler `veri/araclar/` altındadır. Bu oturumun çalışması commit edilmedi.

### 2.9 Açık konular ve sonraki adımlar

- **Veri:**
  - 2025-05 emir verisinin doğrulanması (parquet'e dönüştürüldü; günlük bölümleme yapılmadı).
  - 2025-04 verisinin aynı betiklerle doğrulanması.
  - 2025-01/02 için ITCH, gün içi emir, gün içi işlem ve gün sonu dosyalarının indirilmesi ve dönüştürülmesi; ITCH 2112 sürümü alanlarının sınanması; ITCH ↔ DataStore defter karşılaştırması.
- **Motor:** Python başvuru uygulaması:
  - seans durum makinesi, emir doğrulama, sürekli işlem, tek fiyat, devre kesiciler;
  - tekrar oynatma modunda Mart 2025 işlemlerinin yeniden üretilmesi (doğruluk ölçütü).
- **Tespit:** pay-pencere özelliklerinin çıkarılması; B seviyesi etiket penceresi N için karar.
- **Bilinmeyenler:**
  - değişiklik sebebi 116/117'nin anlamı,
  - `guncelleme_no` atlamaları,
  - kotasyonların müzayedeye katılımı,
  - kısmi görünme koşullu emirlerde görünen miktar,
  - özsermaye günlerinde düzeltilmiş baz fiyat,
  - karışık yönlü 2 istisna vaka.

### 2.10 2025-01/02 verisi için dikkat edilecekler

İndirme ve dönüştürme:
- **İndirilecek dosyalar (her biri 2025-01 ve 2025-02):** ITCH, `PP_GUNICIEMIR`, `PP_GUNICIISLEM`, `PP_GUNSONUFIYATHACIM`.
  - Gün sonu dosyası olmadan baz fiyat, pazar ve işlem yöntemi bilinmez; gün sonu karşılaştırması ve tek fiyat doğrulaması yapılamaz.
- **Disk:** D: sürücüsünde 290 GB boş alan var (21.10.2026).
  - Emir dosyası zip olarak yaklaşık 20 GB, açılmış CSV olarak yaklaşık 209 GB, parquet olarak 17–21 GB yer tutar.
  - `gunici_emir_csv2parquet.py` zip'i doğrudan okur; CSV'yi açmaya gerek yoktur. İki ayın CSV'si birlikte açılırsa disk yetmez.
  - Günlük bölümleme ay başına yaklaşık 14 GB ve ilk geçişte ayrıca geçici dosya alanı ister.
- **Biçim kontrolü:** Dönüştürmeden önce başlık satırı ve sütun sırası Mart dosyasıyla karşılaştırılmalıdır. Dönüştürme betikleri sütun adlarını ve tiplerini sabit tanımlar.
- **Kayıpsızlık:** Parquet satır sayısı CSV satır sayısıyla, günlük bölümleme toplamı aylık dosyayla karşılaştırılmalıdır.
- **Kaynak:** 16 GB RAM nedeniyle büyük işler en çok ikişer paralel çalıştırılmalıdır.

Veri alanları (Mart 2025'te öğrenilenler):
- Aylık emir dosyası tarihe göre sıralı değildir. Gün bazlı işler `gun-ici-emir/gunluk/` bölümlemesinden yapılır (`gunici_emir_gunluk_bol.py`).
- `guncelleme_zamani` UTC'dir (yerel saat − 3 sa); `emir_degistirilme_zamani` yerel saattir.
- `islem_numarasi` 18 hanelidir. pandas'a geçmeden önce `fill_null(0)` uygulanmalı, yoksa float'a dönüp hassasiyet kaybolur. Eşleme: `emir.islem_numarasi = int(islem.ortak_sozlesme_no, 16)`.
- `emir_giris_zamani` hiç değişmez; öncelik zamanı değildir (öncelik modeli M5).
- Değişiklik sebeplerinde yeni kod çıkıp çıkmadığına bakılmalıdır (Mart 2025'te 116 ve 117'nin anlamı bilinmiyor).

Tarih parametreleri (`motor/tarih_parametreleri.csv`):
- Veriden ölçülen satırların geçerlilik aralığı 2025-03-03…28'dir. Haziran 2024–Şubat 2025 için (2025-01/02 dahil) aynı değerler varsayılmamalı, veriden yeniden ölçülmelidir: fiyat marjı, devre kesici yönü / oranı / emir toplama süresi / rastlantısal pencere, kapanışa taşma saati, Adım 4 referansı, EBDKS süreleri.
- Varant `P_SALTKOTASYON` başlangıcı 07.03.2025'ten önce 10:00:00'dır; Ocak–Şubat'ta bu değer beklenir.
- Açığa satış: `DURUM.md` notuna göre yasak BIST 50 payları için 02.01.2025'te kalktı. Ocak–Şubat'ta açığa satışın yalnız BIST 50 paylarında görülmesi beklenir; veriyle doğrulanmalı.
- Fiyat adımı tabloları (Tablo-7/8) 06.11.2023'ten beri geçerlidir; değişiklik beklenmez.
- EBDKS bu aylarda hiç oluşmamış olabilir. Bu durumda eşikler ve süreler bu aylarla sınanamaz.

ITCH ↔ DataStore karşılaştırması:
- ITCH sürümü 2112'dir. 2018 örneğinde `R` mesajı 129, `A` mesajı 37 bayttı. 2025 dosyasında mesaj uzunlukları ve dosya biçimi (VRD/TXT, 2 bayt uzunluk öneki, MoldUDP64 başlığı) ITCH 2112 çevirisiyle yeniden sınanmalıdır [DOĞRULA].
- ITCH zamanları UTC'dir (2018 örneği).
- Eşleme gerekir:
  - ITCH `Order Book ID` ↔ DataStore `islem_kodu` (`R` mesajlarından);
  - ITCH emir kimliği ↔ DataStore `emir_no` ilişkisi bilinmiyor [DOĞRULA].
- ITCH'te müzayede emir toplama aşamasında tek tek emir (`A`) yayımlanmaz. Karşılaştırma sürekli işlem defteriyle sınırlıdır; müzayedede yalnız `Z` denge bilgisi karşılaştırılır.
- ITCH'in mesaj sırası, DataStore'da aynı µs içindeki olayların sırasını çözmek için kullanılabilir (`TASARIM.md` 8).

Doğrulama:
- Mart 2025 betikleri aynı sırayla çalıştırılmalıdır: profil → işlem ↔ gün sonu → marj → fiyat adımı → Ek-19 → emir kuralları → öncelik → seans akışı → devre kesici / EBDKS → tek fiyat → karışık yön.
- Çıktılar `veri/gunici-dogrulama/2025-01/` ve `2025-02/` altına yazılmalıdır.
- SPK vakaları: KRGYO 10.01, TDGYO 24.01, ALKLC 04.02'de başlar. ALKLC dönemi 18.03'e kadar sürer, yani Mart verisiyle devam eder.

## 3. 22.10.2026 — Öneri formuyla farklar ve veri kapsamı

### 3.1 Öneri formu ile mevcut sistem

Öneri formu (`Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.docx`) başlığı: "Ajan Tabanlı Yapay Borsa Simülasyonu ile Borsa İstanbul Pay Piyasasında Kural Dışı Fiyat Hareketlerinin (Anomalilerin) Tespiti". Kullanıcı kararıyla (22.10.2026) sistem ajan tabanlı simülasyon olmayacak; `TASARIM.md`'deki sistem uygulanacaktır. Farklar vize raporunda açıklanacaktır. Gerekçe sütunu taslaktır; kullanıcı tamamlayacaktır.

| Öneri formunda | Mevcut sistemde | Gerekçe (taslak) |
|---|---|---|
| Küçük, büyük ve yabancı yatırımcı ajanları | Yok; DataStore'daki gerçek emir akışı tekrar oynatılır | Gün içi emir verisi her emir olayını içerir; piyasa akışı yapay ajanlarla üretilmek yerine gerçek veriden alınır |
| GA/PSO ile ajan kalibrasyonu | Yok | Ajan olmadığı için kalibrasyon gerekmez; motor gerçek işlemlerin yeniden üretilmesiyle doğrulanır |
| Monte Carlo "kurallara uygun piyasa" olasılık bandı | Yok; iktisadi kurallar + denetimsiz model | [kullanıcı] |
| Sentetik manipülasyon senaryoları (pompala-boşalt, danışıklı işlem) | Var; gerçek emir akışına enjekte edilir | Değişmedi; gerçek emirlerle etkileşim hesaplanır |
| Anomalilerin piyasa geneli / paya özgü sınıflandırılması | Denetimli model (SPK etiketleri) | [kullanıcı] |
| Sanal-reel paralel çalışma, gecikmeli canlı veri, gün sonu eşitleme | Yalnız tarihsel tekrar oynatma | [kullanıcı] |
| Z-skor, Isolation Forest ile karşılaştırma | Z-skor temel çizgi olarak korunur; Isolation Forest eklenebilirse eklenir | Korunabilecek basit yöntemler korunur (kullanıcı kararı, 22.10.2026) |
| BIST 30'dan 5–10 pay, günlük ve dakikalık veri | Tüm paylar, olay düzeyinde gün içi emir ve işlem verisi | DataStore verisi pay ve olay düzeyindedir |
| Emir defteri ve fiyat-zaman öncelikli eşleştirme motoru | Var; sürekli işlem, tek fiyat, devre kesiciler | Değişmedi; kurallar Prosedürden ve veriden doğrulandı |
| SPK kararlarından etiketli olay kümesi | Var (`veri/etiketler/`) | Değişmedi |
| Görselleştirme arayüzü | Var, zorunlu (`TASARIM.md` 6.5): emir enjeksiyonu ve manipülasyon uyarıları grafikte | Değişmedi; arayüz emir enjeksiyonunu da içerir |

### 3.2 Veri kapsamı (kullanıcı kararı, 22.10.2026)

- Veri talep dilekçesi (13.10.2026): gün içi emir ve işlem defteri 01.03–31.03.2025; aylık ITCH ve gün sonu fiyat-hacim 01.06.2024–31.05.2025.
- Karar: 01.06.2024–31.05.2025 aralığında DataStore gün içi emir, gün içi işlem ve gün sonu verisi çekilir. ITCH yalnız 2025-01 ve 2025-02 çekilir.
- Diskte aralık dışı dosyalar var: emir 2025-06…08, işlem 2025-06…09, gün sonu 2025-06…08. Bunlar silinecektir; saklama biçimini kullanıcı yönetir (22.10.2026).

### 3.3 Diğer kararlar (22.10.2026)

- Öneri formundan basit ve yararlı olanlar eklenir: Z-skor temel çizgisi, F1, görselleştirme (zorunlu), eklenebilirse Isolation Forest.
- B seviyesi etiket penceresi N = 20 işlem günü (duyarlılık N = 10, 40). Gerekçe `veri/etiketler/etiket-cikarim-kurallari.md` Açık sorular.
- Kural dosyalarının kullanıcı onayı veriyle birlikte yapılacaktır.
- `ekler/ek3.md` ve `ek4.md`'deki girintili düzyazı satırlarının girintisi kaldırıldı (GitHub'da kod bloğu olarak görünüyordu).
