# Çalışma raporu

Bu dosya, bitirme projesi vize raporunun yazılacağı kaynak kayıttır. Önce 21.10.2026'ya kadar yapılanlar özetlenir, sonra oturumlar tarih başlığı altında ayrıntılı kaydedilir (bölüm 2: 21.10.2026, bölüm 3: 22.10.2026, bölüm 4: 23.10.2026). Ayrıntılı teknik sonuçlar ilgili dosyalardadır; bu raporda yalnız özetleri ve sayıları vardır.

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

Betikler `veri/araclar/` altındadır. Bu oturumun çalışması 22.10.2026'da `c9a3f7e` ile commit edildi.

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

## 3. 22.10.2026 — Kapsam kararları ve eşleştirme motorunun ilk sürümü

### 3.1 Durum değerlendirmesi ve veri kapsamı

- Oturum başında proje durumu `DURUM.md` ve diskteki dosyalarla karşılaştırıldı. Onaylı aylar dışında indirilmiş dosyalar görüldü.
- **Veri aralığı:** Önceki oturum kayıtlarında 12.10.2026 planı bulundu: "Haziran 2024 – Mayıs 2025, 1 yıllık veri". Bu aralık ITCH ve gün sonu için seçilmişti; 21.10.2026'da ana veri DataStore'a geçince belgelere aktarılmamıştı.
- **Veri talep dilekçesi (13.10.2026, Borsa İstanbul Pazarlama ve Satış Bölümü'ne):**
  - gün içi emir defteri ve gün içi işlem defteri: 01.03.2025–31.03.2025;
  - aylık ITCH ve gün sonu fiyat-hacim: 01.06.2024–31.05.2025.
- **Kullanıcı kararı:** 01.06.2024–31.05.2025 aralığında DataStore gün içi emir, gün içi işlem ve gün sonu verisi çekilir. ITCH yalnız 2025-01 ve 2025-02 çekilir (A seviyesi SPK vakaları KRGYO, TDGYO, ALKLC bu aylardadır).
- **Diskteki durum (22.10.2026):**
  - aralıkta olan: emir, işlem ve gün sonu 2025-03…05;
  - aralıkta eksik: 2024-06…2025-02 (9 ay);
  - aralık dışı (silinecek): emir 2025-06…08, işlem 2025-06…09, gün sonu 2025-06…08.
- **Disk hesabı:** 12 ayın aylık parquet'i ile günlük bölümlemesi birlikte tutulursa yaklaşık 440 GB gerekir (ay başına emir ≈ 17–21 GB parquet + ≈ 14 GB günlük, işlem ≈ 4 GB). Saklama biçimini kullanıcı yönetir.

### 3.2 Öneri formu ile mevcut sistem

Öneri formu (`Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.docx`) başlığı: "Ajan Tabanlı Yapay Borsa Simülasyonu ile Borsa İstanbul Pay Piyasasında Kural Dışı Fiyat Hareketlerinin (Anomalilerin) Tespiti". Kullanıcı kararıyla (22.10.2026) sistem ajan tabanlı simülasyon olmayacak; `TASARIM.md`'deki sistem uygulanacaktır:
- eşleştirme motoru,
- veriye dayalı (denetimsiz) makine öğrenmesi,
- etiketli verilerle (denetimli) makine öğrenmesi,
- iktisadi kurallara uygunluk.

Farklar vize raporunda açıklanacaktır. Gerekçe sütununda `[kullanıcı]` yazan satırları kullanıcı tamamlayacaktır.

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

Öneri formundaki iş-zaman çizelgesi: emir defteri ve eşleştirme motoru Kasım–Aralık, ajanlar Aralık–Ocak, birinci dönem raporu Ocak. Birinci yarıyıl hedeflerinde literatür taraması da vardır; projede henüz literatür bölümü yoktur.

### 3.3 Diğer kararlar

- **Öneri formundan eklenecekler:** basit ve yararlı olanlar. Z-skor temel çizgisi, F1 ölçütü, görselleştirme (zorunlu; emir enjeksiyonu ve manipülasyon uyarıları grafikte), eklenebilirse Isolation Forest (`TASARIM.md` 6.3, 6.5).
- **B seviyesi etiket penceresi N = 20 işlem günü** (duyarlılık analizi N = 10 ve 40). Kullanıcı seçimi Claude'a bıraktı; gerekçe:
  - SPK bültenlerinde dönemi yazılı 12 vaka: dönem uzunluğu 2–131 işlem günü, ortanca 23,5;
  - dönemi ve geçici yasağı birlikte bilinen 4 vaka (EUREN 6, ALKLC 8, TDGYO 23, KRGYO 33 işlem günü): dördünde de dönem yasaktan 3 iş günü önce biter;
  - pencerenin gerçek dönemi kapsaması ile pencerenin dönem içinde kalan payı (saflık) için F1, N = 20'de en yüksek bölgededir (0,75 / 0,76);
  - ayrıntı ve tablo: `veri/etiketler/etiket-cikarim-kurallari.md` Açık sorular.
- **B penceresinin bitişi (kullanıcı kararı, 22.10.2026):** pencere yasaktan 3 iş günü önce biter; yasaktan önceki 2 iş günü "belirsiz" sayılır, değerlendirmede ne pozitif ne negatiftir. Gerekçe:
  - dönemi ve yasağı birlikte bilinen 4 A vakasının (EUREN, ALKLC, TDGYO, KRGYO) dördünde de dönem yasaktan 3 iş günü önce biter;
  - eski kural (bitiş = yasaktan önceki iş günü) her B penceresine bu vakalarda hiç dönem içinde olmamış 2 gün katıyordu; 20 günlük pencerede pozitiflerin ≈ %10'u yanlış etiketleniyordu (kısa vakalarda daha fazla);
  - boşluk, manipülasyonun bitmesinden de SPK inceleme penceresinin kesilmesinden de kaynaklanabilir; bu yüzden 2 gün negatif sayılmaz, değerlendirme dışı tutulur;
  - kanıt 4 vakaya dayanır; 12 aylık etiketlerde yeni A vakalarıyla yeniden kontrol edilecek.
- **Kural onayları:** kural dosyalarının kullanıcı onayı veriyle birlikte yapılacak.
- **Belge düzeltmesi:** `ekler/ek3.md` ve `ek4.md`'de girintili 265 düzyazı satırının girintisi kaldırıldı (GitHub'da kod bloğu olarak görünüyordu; boşluk dışı fark yok).
- **Git:** öneri formu ve dilekçe kişisel bilgi içerdiğinden `.gitignore`'a eklendi. 21–22.10.2026 çalışması `c9a3f7e` ile commit edildi.

### 3.4 Eşleştirme motoru: sürekli işlem

Motor ITCH olmadan kuruldu. Girdi DataStore emir olaylarıdır; doğrulama `PP_GUNICIISLEM` ile yapılır. ITCH yalnız aynı µs'deki olayların sırası ve defter çapraz doğrulaması için gerekir.

Yöntem (tekrar oynatma, `TASARIM.md` 4.1):
- Her emrin satırlarından yalnız kullanıcı eylemleri alınır: yeni emir (sebep 6), değişiklik (5), iptal (1). Diğer satırlar motorun üretmesi beklenen çıktılardır.
- Değişiklik, kalan miktar farkı olarak verilir. Böylece motorun kalanı saparsa da uygulanabilir.
- Motorun ürettiği işlemler gerçek işlemlerle (alış emri, satış emri, fiyat, adet) birebir karşılaştırılır; ilk sapma noktası yazılır.

Veriden öğrenilenler ve motora etkisi (THYAO.E 03.03.2025 üzerinde, sırayla):

| Adım | Bulgu | Birebir aynı işlem |
|---|---|---|
| İlk sürüm | Fiyat-zaman önceliği, öncelik kaybı (fiyat değişikliği, kalan artışı), kısmi görünme yenilemesi | %99,59 |
| Kısmi görünme yazımı | Gelen emir yenilenen kısımdan aynı eşleşmede tekrar alırsa veride tek işlem yazılır | %99,65 |
| Tepe tahmini | Sebep 13, görünen kısmı bitiren işlemde yazılır; yenilemeden (ve müzayededen geçişten) sonraki ilk işlem 3 ya da 13 olabilir; tek işlemde iki yenileme olabilir | %99,81 |

Açıklanamayan sapmalar:
- Aynı fiyatta miktar azaltmada öncelik çoğunlukla korunur; THYAO.E 03.03'te 551 azaltmanın 2'sinde kaybolmuştur. Ayırt edici bir özellik bulunamadı (2018 ITCH'teki %4,2 istisnayla aynı tür).
- Tek yenilemesi olan kısmi görünme emirlerinde birden çok tepe değeri veriyle uyumludur; tahmin yanlış olabilir.
- Bir sapmadan sonra defter birkaç işlem boyunca farklı kalır; oranlar bu zincirleme etkiyi içerir.

### 3.5 Eşleştirme motoru: müzayede (açılış, kapanış, kapanış fiyatından işlemler)

- **Denge fiyatı:** 21.10.2026'da doğrulanan `veri/araclar/tek_fiyat_algoritma.py` motora bağlandı. Baz fiyat, pazar ve araç grubu gün sonu dosyasından; fiyat marjı ve Adım 4 referansı tarih parametresi tablosundan (`motor/parametreler.py`) okunur.
- **İşlem dağıtımı (kaynakta yazılı değil, veriden):** Alış ve satış tarafı ayrı ayrı öncelik sırasına dizilir: önce piyasa ve fiyatsız piyasadan limite emirler zaman sırasıyla, sonra denge fiyatına eşit ya da daha iyi limit emirler fiyat ve zaman sırasıyla. İki liste baştan yürünür; her adımda iki emrin kalanlarının küçüğü kadar işlem yazılır. THYAO.E 03.03 açılışında 1.872 işlemin tamamı aynı emir çiftleri ve sırayla üretildi.
- **Kalanlar:** piyasa emri, KİE ve dengeleyici iptal edilir; piyasadan limite emrin kalanı eşleşme fiyatından limit emre döner (`05-emirler.md` madde 14, 26, 36).
- **Kapanış:** sürekli işlem defteri öncelik sırasıyla kapanış müzayedesine geçer; aday fiyatlar son işlem fiyatının ±%3'ü ile sınırlıdır. Ardından kapanış fiyatından işlemler bölümünde bütün işlemler kapanış fiyatından olur.
- **AFK bulgusu:** GARAN.E 03.03 kapanışında emir toplama sırasında her saniye fiyatı ve miktarı değişmeden değiştirilen emirler önceliğini kaybetmişti; AKBNK.E 27.03'te benzer bir değişiklikte öncelik korunmuştu. İki durumu ayıran alan `afk`'dir (DataStore: "Acente / Fon Kodu Flag", dolu ise E). Gerçek işlem sırasıyla 5 sıra-günde ölçüldü: `H` emirlerde 176 kontrolün hepsinde öncelik korunur, `E` emirlerde 6 kontrolün hepsinde kaybolur. Bu, Ek-18 1.2'deki "emir bilgileri (MPF-AFK-Hesap No) değişince öncelik kaybolur" ifadesiyle uyumludur. Motor tekrar oynatmada bunu değişiklik olayının `gorunmeyen` bayrağıyla işler. Kullanıcı kararı (22.10.2026): sentetik emirlerde emir bilgisi değişikliği reddedilir (madde 24); tekrar oynatmada veride görülen öncelik kaybı uygulanır.

Sonuç (Mart 2025; açılıştan kapanış fiyatından işlemlere kadar bütün gün oynatıldı):

| Sıra-gün | Açılış | Sürekli işlem | Kapanış | Kapanış fiyatından |
|---|---|---|---|---|
| THYAO.E 03.03 | 1.872 / %100 | 74.046 / %99,81 | 716 / %100 | 178 / %100 |
| GARAN.E 03.03 | 462 / %100 | 54.468 / %99,89 | 280 / %100 | 54 / %100 |
| ASELS.E 03.03 | 1.464 / %100 | 98.284 / %99,54 | 346 / %100 | 160 / %100 |
| ALKLC.E 11.03 | 75 / %100 | 22.648 / %100 | 61 / %100 | 21 / %100 |
| AKBNK.E 27.03 | 565 / %100 | 93.759 / %99,42 | 630 / %100 | 197 / %100 |
| KRGYO.E 27.03 | 20 / %100 | 7.620 / %100 | 27 / %100 | 8 / %100 |

Hücreler: gerçek işlem sayısı / birebir aynı oran. Devre kesici ve EBDKS içeren günler 3.6'dadır.

Müzayede sonrası motorun kurduğu sürekli işlem defteri, 6 sıra-günün hepsinde veriden kurulan defterle emir, fiyat, kalan ve seviye sırası bakımından aynıdır.

### 3.6 Eşleştirme motoru: devre kesici ve EBDKS

Bir sıra-günün bütün bölüm akışı tek yerde oynatılır (`motor/gun.py`). Bölüm geçişleri ve eşleşme anları veriden alınır:
- Emir toplama bölümlerinde ve EBDKS durdurmasında emirler toplanır, eşleştirme yapılmaz.
- Eşleştirme, veride eşleştirme bölümü satırı varsa o anda yapılır. Toplamadan başka bir toplamaya geçişte (devre kesicinin kapanışa taşması, açılıştan EBDKS durdurmasına) eşleştirme yapılmaz.

Veriden öğrenilenler (`06-devre-kesici.md` Açık sorular):
- **Eşik:** son müzayede fiyatının (yoksa baz fiyatın) %5 altı, içe yuvarlanır. Eşik fiyatından işlem olur, altından olmaz.
- **Tetikleme:** eşiğin ötesinde eşleşecek gelen emrin kalanı iptal edilir (hiç işlem görmediyse tamamı) ve devre kesici tetiklenir. Tetiklemeden sonra veride bölüm adı birkaç yüz ms "sürekli işlem" kalır; bu sürede eşleşme olmaz, KİE emirleri müzayedeye taşınır.
- **EBDKS durdurması:** sistem iptalleri (sebep 117) görünür alanlardan ayırt edilemez; dışsal olay olarak alınır.
- **Kısmi görünme emirleri müzayedede:** görünen kısım kadar sırayla dağıtılır. Yalnız müzayedede işlem gören emirde tepe büyüklüğü bilinemez (`03-tek-fiyat.md` Açık sorular).

| Sıra-gün | Müzayedeler | Sürekli işlem | Kapanış fiyatından | Bütün gün |
|---|---|---|---|---|
| KRGYO.E 03.03 (devre kesici) | 286 / %100 | 21.217 / %99,92 | 22 / %100 | %99,92 |
| THYAO.E 19.03 (2 EBDKS, devre kesici) | 6.807 / %100; EBDKS 3.227 / %71,4 | 176.028 / %99,82 | 276 / %100 | %99,34 |

19.03 EBDKS müzayedelerinde fiyat, toplam miktar ve emir bazında gerçekleşen miktar aynıdır (3.213/3.213); farklı olan, tepe büyüklüğü bilinmeyen kısmi görünme emirlerinin karşı emir çiftleridir.

### 3.7 Emir doğrulama ve enjeksiyon

- **Doğrulama (`motor/dogrulama.py`):** sentetik emirler için. Kapsadığı kurallar:
  - Ek-19 bölüm × emir tipi ve değişiklik izinleri,
  - fiyat adımı ve günlük marj,
  - kapanış emir toplamada son işlem ±%3; kapanış fiyatından işlemlerde yalnızca kapanış fiyatı,
  - açığa satış kapsamı (tarih parametresi),
  - emir bilgisi değişikliğinin reddi (madde 24 kararı).
- **Enjeksiyon (`motor/gun.py`, `enjeksiyon.py`):** sentetik olaylar zamanlarına göre bölüme yerleşir ve o anki defter durumuyla doğrulanır; reddedilenler sebebiyle kaydedilir. Gerçek akış dışsaldır (gerçek katılımcılar tepki vermez).
- **Senaryolar (`motor/senaryolar.py`; `TASARIM.md` 5):** kapanış fiyatını etkileme, yanıltıcı emir (spoofing/layering), adım adım fiyat yükseltme, karşılıklı işlem.
- **Örnek:** KRGYO.E 27.03'te kapanış eşleştirmesinden 10 sn önce bandın üst ucundan 200.000 lotluk alış emri girildi. Kapanış fiyatı 11,80'den 12,05'e çıktı (+%2,1); sentetik aktör 120.948 lot aldı; 7.675 gerçek işlemin 7.640'ı değişmedi.

### 3.8 Görselleştirme arayüzü

`arayuz/uygulama.py` (Streamlit; `streamlit run arayuz/uygulama.py`). Veri hazırlığı `arayuz/hazirla.py` (Streamlit'ten bağımsız).
- **Seçimler:** gün, pay, senaryo ve parametreleri.
- **Grafikler:** işlem fiyatı (taban çizgisi ve enjeksiyonlu; sentetik işlemler işaretli) ve dakikalık hacim, iki ayrı grafik (tek eksen). Z-skor uyarıları ve bölüm bantları (müzayede, devre kesici, EBDKS, kapanış) iki grafikte de görünür.
- **Tablolar:** sentetik işlemler, reddedilen sentetik olaylar, dakikalık seri.
- **Görsel kontrol:** Streamlit test aracı (`AppTest`) ve tarayıcıda yapıldı. Renkler doğrulanmış paletten (iki seri, iki modda CVD ΔE ≥ 24).

### 3.9 Tespit: ilk sürüm

Bu bölüm tespit modülünün yapısını, kullanılan etiketleri ve iki değerlendirmeyi (SPK etiketleri, sentetik enjeksiyon) açıklar. Ölçütler: ROC-AUC (rastgele seçilen bir pozitifin rastgele bir negatiften yüksek puan alma olasılığı; 0,5 rastgele); "ilk 3" (enjekte edilen pencerelerden birinin günün en yüksek puanlı 3 penceresinde olma oranı); "kontrol" (aynı pencerelerin enjeksiyonsuz koşuda ilk 3'e girme oranı, yani yanlış alarm tabanı).

Kod `tespit/`:
- `ozellikler.py`: pay-gün özellikleri (6.2'deki emir akışı, işlem, defter ve referans grupları). Mart 2025: 20 gün × 590 sıra, gün başına ≈ 160 sn. Gün başına ara dosyalar tutulur, iş yarıda kalırsa kaldığı yerden devam eder. Çıktı `veri/gunici-dogrulama/2025-03/tespit/ozellikler.parquet` (git dışı).
- `yontemler.py`: Z-skor (payın önceki günlerine göre), iktisadi kurallar (VI-104.1 md 5/1 a, b, d, f; eşikler tasarım parametresidir), Isolation Forest, kesitsel karşılaştırma (aynı gün aynı pazardaki paylar içinde yüzdelik sıra; 5 günlük birikimli getiri ve hacim artışı dahil) ve SPK etiketlerinin pay-güne çevrilmesi.
- `degerlendir.py`: SPK etiketleriyle pay-gün sıralama ölçütleri.
- `motor_ozellikleri.py`: aynı özellikler motor çıktısından (enjeksiyonlu koşu için).
- `pencere.py`: 5 dakikalık pencere özellikleri ve puanları; kapanış penceresi payın geçmiş kapanışlarına göre.
- `sentetik_degerlendir.py`, `pencere_degerlendir.py`, `denetimli.py`: sentetik enjeksiyonla değerlendirme ve denetimli model.

**Özellikler.** 6.2'deki gruplara ek olarak:
- *Kısa ömürlü uzak emir payı:* sürekli işlemde aynı taraftaki en iyi fiyattan en az 3 adım uzakta girilip 60 sn içinde işlem görmeden iptal edilen emirlerin miktar payı. Yanıltıcı emir (spoofing/layering) göstergesidir; bent a/b kuralına bağlıdır. Verideki olay anındaki en iyi alış/satış fiyatından hesaplanır. Mart 2025 ortancası %1,2; ALKLC'nin manipülasyon günlerinde %7'nin üstünde.
- *Makas:* sürekli işlemde göreli makasın ortancası.

**SPK etiketleri.** A: dönemin işlem günleri. B: tedbirden önceki 20 işlem günü; pencere tedbirden 3 iş günü önce biter, tedbirden önceki 2 iş günü belirsizdir ve değerlendirmeden çıkarılır (kullanıcı kararı 22.10.2026; gerekçe: dönemi ve tedbiri birlikte bilinen 4 A vakasının dördünde de dönem tedbirden 3 iş günü önce biter; bu 2 gün eski kuralda pozitiflerin ≈ %10'unu oluşturuyordu ve dönem dışıydı, ancak SPK'nın inceleme penceresinin kesilmesinden kaynaklanabileceği için negatif de sayılmaz). Etiketsiz gün negatif değildir (bilinmiyor); ölçütler bu nedenle alt sınırdır.

**SPK etiketleriyle sonuç** (Mart 2025; `veri/gunici-dogrulama/2025-03/tespit/degerlendirme.csv`). Pozitifler: A ALKLC (12 pay-gün); B HEDEF, SEGMN, ENSRI, BAKAB, KRGYO, OZATD, SMRTG, VKFYO (64 pay-gün).

| Puan | ROC-AUC (A) | ROC-AUC (B) | ROC-AUC (A+B) |
|---|---|---|---|
| Z-skor (kendi geçmişi) | 0,65 | 0,52 | 0,53 |
| İktisadi kurallar | 0,47 | 0,59 | 0,57 |
| Isolation Forest (Z-skor) | 0,53 | 0,53 | 0,53 |
| Kesitsel uç sıra | 0,89 | 0,50 | 0,56 |
| Kesitsel Isolation Forest | 0,90 | 0,53 | 0,59 |

- Payın kendi geçmişine dayanan yöntemler haftalarca süren manipülasyonda zayıftır: geçmiş de manipülasyon içerir (ALKLC dönemi 04.02'de başlar).
- Kesitsel karşılaştırma bu kirlenmeye duyarlı değildir. ALKLC pay-günleri gün içinde ortalama 91. yüzdeliktedir. Yeni iki özellik ALKLC'de ROC-AUC'yi 0,85'ten 0,90'a çıkardı.
- B'de sonuç rastgeleye yakındır. B pencereleri bir varsayımdır (N = 20) ve B tedbirleri çoğunlukla "işlem bazlı piyasa dolandırıcılığı" şüphesine dayanır; Mart'a düşen günlerin bir kısmı pencerenin başındadır (KRGYO, OZATD, VKFYO).
- Pozitif sayısı azdır; sonuçlar 12 aylık veriyle yeniden ölçülmelidir.

**Sentetik enjeksiyonla değerlendirme.** Yöntem:
- Rastgele pay-günler: 10.03 sonrası, sürekli işlemde en az 300 işlem, özsermaye günleri ile SPK etiketli ve belirsiz günler hariç.
- Senaryolar sırayla, payın o günkü işlem miktarına (H) göre ölçekli:
  - kapanış: kapanış emir toplamanın sonunda H × %3, bandın ucundan;
  - yanıltıcı emir: 3 katman × H × %2, son işlem fiyatından 4–6 adım uzakta, 30 sn sonra iptal; arada karşı tarafta H × %0,2 agresif emir;
  - fiyat yükseltme: 20 sn arayla 10 agresif alış (KİE piyasadan limite), her biri H × %0,5;
  - karşılıklı işlem: 60 sn arayla 10 kez aynı aktörün satış ve alışı, her biri H × %0,5.
- Özellikler motor çıktısından hesaplanır. Kontrol: enjeksiyonsuz motor özellikleri veriden hesaplananlarla neredeyse aynıdır; kontrol kümesinde ROC-AUC ≈ 0,5 (yöntem farkı sahte tespit üretmez).

*Pay-gün düzeyi* (`veri/gunici-dogrulama/2025-03/tespit/sentetik/`): 80 enjeksiyonda yöntemler kısa süreli enjeksiyonları ayırt edemez: ROC-AUC 0,43–0,71, enjeksiyonsuz kontrol kümesinde 0,48–0,62. Kuralların kontrolde de 0,62 alması, seçilen likit pay-günlerin genel olarak daha yüksek puan almasındandır; enjeksiyonun katkısı ≈ 0,05'tir. Yeni iki özellik bu düzeyde sonucu değiştirmedi; motordan ve veriden hesaplanan değerleri birebir aynıdır. Kısa bir epizot (30 sn'lik yanıltıcı emir, 200 sn'lik fiyat yükseltme) günün toplamında kaybolur; bu, pencere düzeyine geçişin gerekçesidir.

*5 dakikalık pencere* (79 pay-gün, pozitif pencere oranı %1,5; `veri/gunici-dogrulama/2025-03/tespit/pencere/`). Pencere, aynı pay-günün diğer pencerelerine göre sağlam z (ortanca, MAD) ile puanlanır. Kapanış müzayedesi penceresi ise payın önceki günlerdeki kapanışlarına göre puanlanır (kapanışın AOF'den sapması, kapanış seansı hacim payı, kapanış öncesi getiri), çünkü bu pencere her gün aynı günün diğer pencerelerine göre uç değerdir. Denetimli model (gradyan artırmalı karar ağacı) yalnız sürekli işlem pencerelerinde, pay-güne göre gruplu 5 katlı çapraz doğrulamayla eğitilir. "İlk 3": pozitif pencerelerden biri günün en yüksek puanlı 3 penceresinde. "Kontrol": aynı pencerelerin enjeksiyonsuz koşuda ilk 3'e girme oranı (yanlış alarm tabanı).

| Senaryo | Kurallar: ROC-AUC / ilk 3 / kontrol | Denetimli: ROC-AUC / ilk 3 / kontrol |
|---|---|---|
| Yanıltıcı emir | 0,90 / %84 / %5 | 0,89 / %74 / %0 |
| Karşılıklı işlem | 0,49 / %0 / %0 | 0,89 / %80 / %20 |
| Fiyat yükseltme | 0,56 / %0 / %0 | 0,64 / %30 / %5 |
| Kapanış | 0,60 / %0 / %0 | — |

Yorum:
- *Yanıltıcı emir* iyi yakalanır: kısa ömürlü uzak emir payı bu senaryonun doğrudan izidir; kurallar enjekte edilen pencereyi 19 günün 16'sında günün ilk 3 penceresine koyar, enjeksiyonsuz günde yanlış alarm %5'tir.
- *Karşılıklı işlem* yalnız denetimli modelle yakalanır ve bunu hacim artışından yapar (modelin en önemli özelliği hacim z'sidir). Aktör kimliği olmadan "aynı kişinin iki tarafı" ayırt edilemez; kontrol yanlış alarmı %20'dir.
- *Fiyat yükseltme* en zor senaryodur: 10 küçük agresif alış, likit paylarda günün olağan dalgalanmasından ayrışmaz.
- *Kapanış:* kapanış penceresi aynı günün pencerelerine göre puanlandığında sonuç yüksek görünüyordu (ROC-AUC 0,84, ilk 3 %42), ama enjeksiyonsuz günde de aynı oranda alarm veriyordu; yani ayırt edicilik yoktu. Geçmiş kapanışlara göre puanlanınca yanlış alarm sıfıra iner ama günlük hacmin %3'ü büyüklüğündeki bir kapanış emri payın olağan kapanış oynaklığından ayrışmaz. Bu büyüklükte kapanış etkilemesi bu veriyle tespit edilemez; daha büyük senaryolarla ve 12 aylık geçmişle yeniden ölçülmelidir.
- Pay-gün düzeyi kısa epizotları kaçırır; pencere düzeyi gereklidir.
- Senaryo büyüklükleri bir varsayımdır; sonuçlar bu büyüklüklere bağlıdır (aşağıdaki duyarlılık analizi).

*Senaryo büyüklüğüne duyarlılık* (pencere düzeyi; büyüklükler ×0,3, ×1, ×3; her biri 80 enjeksiyon; `veri/gunici-dogrulama/2025-03/tespit/olcek_duyarlilik.csv`, `pencere_olcek_0.3/`, `pencere_olcek_3/`). Hücreler: ROC-AUC / ilk 3 / kontrol ilk 3.

| Senaryo | Ölçek | Kurallar | Denetimli |
|---|---|---|---|
| Yanıltıcı emir | ×0,3 | 0,90 / %84 / %5 | 0,86 / %58 / %0 |
| Yanıltıcı emir | ×1 | 0,90 / %84 / %5 | 0,89 / %74 / %0 |
| Yanıltıcı emir | ×3 | 0,90 / %84 / %5 | 0,91 / %79 / %0 |
| Karşılıklı işlem | ×0,3 | 0,44 / %0 / %0 | 0,79 / %45 / %25 |
| Karşılıklı işlem | ×1 | 0,49 / %0 / %0 | 0,89 / %80 / %20 |
| Karşılıklı işlem | ×3 | 0,57 / %0 / %0 | 0,96 / %100 / %5 |
| Fiyat yükseltme | ×0,3 | 0,54 / %0 / %0 | 0,65 / %20 / %10 |
| Fiyat yükseltme | ×1 | 0,56 / %0 / %0 | 0,64 / %30 / %5 |
| Fiyat yükseltme | ×3 | 0,57 / %0 / %0 | 0,62 / %35 / %0 |
| Kapanış | ×0,3 | 0,41 / %0 / %0 | — |
| Kapanış | ×1 | 0,60 / %0 / %0 | — |
| Kapanış | ×3 | 0,70 / %15 / %0 | — |

Yorum:
- Yanıltıcı emir kuralı ölçekten bağımsızdır: kısa ömürlü uzak emir payı bir orandır; katmanlar küçük olsa da pencerede bu tür emirlerin payını belirgin artırır. Bu, kuralın büyüklüğe değil davranış biçimine duyarlı olduğunu gösterir.
- Karşılıklı işlem tespiti büyüklüğe güçlü biçimde bağlıdır: model bunu hacim artışından yakalar; küçük karşılıklı işlemler olağan hacim dalgalanmasında kaybolur.
- Fiyat yükseltme her ölçekte zayıftır; mevcut özellikler bu senaryonun izini taşımaz. Yeni gösterge gerekir (sonraki adımlar).
- Kapanış etkilemesi ancak büyük emirlerde (günlük hacmin ≈ %9'u) belirmeye başlar.
- Denetimli modelin kapanış satırı yoktur: model yalnız sürekli işlem pencerelerinde çalışır, kapanış penceresi geçmiş kapanışlarla puanlanır.

Sonraki adımlar:
- fiyat yükseltme göstergesi: pencerede net agresif adım (agresif alışların fiyatı yukarı ittiği adım sayısı eksi agresif satışların aşağı ittiği adım sayısı), bent f kuralına bağlanır;
- kapanış etkilemesi için daha güçlü göstergeler (kapanış denge fiyatının son sürekli işlem fiyatından sapması, kapanış emir toplamadaki alış/satış dengesizliği ve son dakikalardaki değişiklikler);
- defter derinliği ve dengesizliği (motorla yeniden kurulan defterden);
- 12 aylık veriyle ve daha çok enjeksiyonla yeniden ölçüm; SPK etiketli pay-günlerde pencere düzeyi.

### 3.10 Toplu ölçüm (bütün paylar)

`motor/toplu_oynat.py` ile günün bütün `.E` sıraları baştan sona oynatıldı (`veri/gunici-dogrulama/2025-03/motor/toplu_GUN.csv`).

| Gün | Sıra | Gerçek işlem | Bütün gün | Sürekli işlem | Müzayedeler | EBDKS müzayedeleri | Kapanış fiyatından | %100 olan sıra | %95 altı sıra | Süre |
|---|---|---|---|---|---|---|---|---|---|---|
| 03.03.2025 | 588 | 4.915.057 | %99,85 | %99,85 | %99,69 | — | %99,58 | 419 / 586 | 1 | 17 dk |
| 19.03.2025 | 582 | 6.825.508 | %99,91 | %99,93 | %99,90 | %99,21 | %99,91 | 439 / 580 | 2 | 24 dk |

- Emir bazında gerçekleşen miktar: 03.03'te 5.433.516 emrin 5.432.976'sında, 19.03'te 7.717.972 emrin 7.717.497'sinde aynıdır.
- Bütün sıralar hatasız çalıştı. Tek fiyatla işlem gören sıralar da oynatıldı.
- 19.03'te 4 sıra (EGEPO, RALYH, RTALB, SELVA) özsermaye günüdür (bedelsiz). Gün sonu dosyasındaki önceki kapanış düzeltilmemiş olduğundan baz fiyat ve fiyat sınırları yanlış çıkar; motor bu sıralarda işlem üretemez. Tabloya alınmadı (`TASARIM.md` 8; düzeltilmiş baz fiyat kaynağı gerekir).
- 19.03 kriz günüdür (iki EBDKS, çok sayıda devre kesici); sonuç normal günden düşük değildir.

### 3.11 Testler

26 birim testi, hepsi geçer (`python -m pytest motor/testler tespit/testler`):
- `motor/testler/` (23):
  - sürekli işlem: Ek-18 2.2.2 piyasa emri ve 3.2.2 piyasadan limite örnekleri; KİE; işlemin pasif emrin fiyatından olması; öncelik kaybı ve korunması; fiyat değişikliğinin agresif eşleşmesi; iptal; kısmi görünme; görünmeyen alan değişikliği;
  - tek fiyat: dağıtım sırası, dengeleyici emirler, kalanlar, emir toplamada öncelik;
  - tepe tahmini: Mart 2025 verisinden alınmış dört örnek;
  - doğrulama: fiyat adımı ve sınırlar, Ek-19 izinleri, kapanış kuralları, değişiklik izinleri, açığa satış.
- `tespit/testler/` (3): B penceresi (20 işlem günü, yasaktan 3 iş günü önce biter, 2 belirsiz gün, bayram), Z-skorun yalnız geçmişi kullanması, kısa ömürlü uzak emir tanımı.

### 3.12 Bu oturumda üretilen dosyalar

| Tür | Dosya |
|---|---|
| Motor | `motor/emir.py`, `defter.py`, `surekli_islem.py`, `tek_fiyat.py`, `gun.py`, `dogrulama.py`, `veri.py`, `parametreler.py`, `senaryolar.py`, `tekrar_oynat.py`, `toplu_oynat.py`, `enjeksiyon.py` |
| Testler | `motor/testler/test_surekli_islem.py`, `test_tek_fiyat.py`, `test_tepe.py`, `test_dogrulama.py`; `tespit/testler/test_tespit.py` |
| Arayüz | `arayuz/uygulama.py`, `arayuz/hazirla.py` |
| Tespit | `tespit/ozellikler.py`, `yontemler.py`, `degerlendir.py`, `motor_ozellikleri.py`, `pencere.py`, `sentetik_degerlendir.py`, `pencere_degerlendir.py`, `denetimli.py` |
| Çıktılar | `veri/gunici-dogrulama/2025-03/motor/` (sıra-gün özetleri, `ozet.csv`, `toplu_*.csv`), `veri/gunici-dogrulama/2025-03/tespit/` (`degerlendirme.csv`, `kural_oranlari.csv`, `etiketli_siralama.csv`; `sentetik/`, `pencere/` alt klasörleri) |
| Belgeler | `TASARIM.md` (1, 4.5, 6.3, 6.5, 6.6), `kurallar/03-tek-fiyat.md`, `04-surekli-islem.md`, `05-emirler.md`, `06-devre-kesici.md` ([BİLGİ] notları ve kararlar), `veri/etiketler/etiket-cikarim-kurallari.md` (N ve B penceresi kararları), `DURUM.md`, `CLAUDE.md`, `veri/README.md`, `.gitignore`, `ekler/ek3.md`, `ek4.md` |

Commit'ler (22.10.2026): `c9a3f7e` (veri doğrulamaları, tasarım, kararlar), `5bd7ed1` (motor, arayüz, tespit ilk sürümü), `ae7e866` (5 dk pencere, denetimli model, sentetik değerlendirme) ve bu bölümdeki son güncellemeler. Ham veri ve parquet ara çıktıları git dışıdır.

### 3.13 Açık konular ve sonraki adımlar

- **Motor:**
  - kısmi görünme emirlerinde tepe belirsizliği; aynı fiyatta miktar azaltmada nadir öncelik kaybı;
  - özsermaye günlerinde düzeltilmiş baz fiyat (gün sonu dosyasındaki önceki kapanış düzeltilmemiştir);
  - kotasyonlar (`.F`) ve orta nokta emirleri (tespit pay sıralarında yapıldığından öncelikli değil);
  - seans durum makinesi gerekmiyor: ajan tabanlı simülasyon çıkarıldı, motor her zaman verideki bölüm geçişleriyle çalışır;
  - performans: bir günün bütün payları 17–30 dk; 12 ay için paralel çalıştırma ya da derlenmiş çekirdek gerekebilir.
- **Tespit:**
  - kapanış etkilemesi: senaryo büyüklüğüne duyarlılık ve uzun geçmişle yeniden ölçüm;
  - fiyat yükseltme için yeni gösterge (ör. ardışık agresif alışların fiyat etkisi);
  - defter derinliği ve dengesizliği (motorla yeniden kurulan defterden);
  - SPK etiketli pay-günlerde pencere düzeyi; 12 aylık veriyle yeniden ölçüm.
- **Kullanıcı kararları (22.10.2026):**
  - madde 24 kararı sentetik emirlerde geçerli kalır (emir bilgisi değişikliği reddedilir); tekrar oynatmada veride görülen öncelik kaybı uygulanır;
  - B penceresi yasaktan 3 iş günü önce biter; önceki 2 iş günü belirsiz, değerlendirme dışı (3.3).
- **Veri:** 2024-06…2025-02 dosyalarının indirilmesi; bu aylar için tarih parametrelerinin (marj, devre kesici, açığa satış) veriden yeniden ölçülmesi.
- **Rapor:** vize raporu için literatür bölümü.

### 3.14 Günün sonu: kaldığımız yer ve yapılacaklar

**Kaldığımız yer (22.10.2026 akşamı).**
- **Motor (`motor/`):** bir sıra-günü baştan sona (açılış, sürekli işlem, devre kesici ve EBDKS müzayedeleri, kapanış, kapanış fiyatından işlemler) tekrar oynatır. Bütün paylarla ölçüldü: 03.03.2025'te %99,85, 19.03.2025'te %99,91 işlem birebir (özsermaye günleri hariç). Sentetik emir doğrulama ve enjeksiyon çalışır. 26 test geçer.
- **Arayüz (`arayuz/`):** Streamlit; oynatma, enjeksiyon, fiyat ve hacim grafikleri, 5 dk pencere kural uyarıları.
- **Tespit (`tespit/`):**
  - pay-gün özellikleri (Mart 2025, yeni göstergelerle);
  - SPK etiketleriyle değerlendirme: A (ALKLC) kesitsel ROC-AUC 0,90, B ≈ 0,53;
  - 5 dk pencere ve denetimli model; sentetik enjeksiyonla değerlendirme ve büyüklük duyarlılığı.
  - Yanıltıcı emir iyi yakalanır; karşılıklı işlem hacimle ve büyüklüğe bağlı olarak; fiyat yükseltme ve kapanış etkilemesi zayıftır.
- **Veri:** yalnız Mart 2025 günlük bölümlenmiş ve doğrulanmış; 2025-04 ve 05 parquet var ama doğrulanmadı.
- **Kararlar:** 22.10.2026'da verilen bütün kararlar belgelere işlendi (veri aralığı, sistem kapsamı, N = 20, B penceresi bitişi, madde 24 / AFK).
- **Git:** bütün çalışma commit edildi (son commit: "Günün sonu: büyüklük duyarlılığı, kaldığımız yer ve yapılacaklar").

**Yapılacaklar (öncelik sırasıyla).**
1. **Fiyat yükseltme göstergesi:** pencerede net agresif adım (agresif alışların fiyatı yukarı ittiği adım sayısı eksi agresif satışların aşağı ittiği adım sayısı). `tespit/pencere.py`'ye eklenir, bent f kuralına bağlanır; `pencere_degerlendir.py` ve `denetimli.py` yeniden çalıştırılır.
2. **Kapanış etkilemesi göstergeleri:** kapanış denge fiyatının son sürekli işlem fiyatından sapması, kapanış emir toplamadaki alış/satış dengesizliği, son dakikalardaki değişiklik ve iptaller. Pay-gün özelliklerine ve kapanış penceresi puanına eklenir.
3. **Veri indirme:** 2024-06…2025-02 (DataStore gün içi emir, gün içi işlem, gün sonu; ITCH yalnız 2025-01 ve 2025-02). Her ay için parquet dönüşümü, günlük bölümleme, kayıpsızlık kontrolü (`rapor.md` 2.10). Aralık dışı dosyaların (2025-06…09) silinmesi kullanıcıdadır.
4. **Yeni aylar için tarih parametreleri:** marj, devre kesici yönü/oranı/süreleri, açığa satış kapsamı veriden yeniden ölçülür (`motor/tarih_parametreleri.csv`); ardından Mart doğrulama betikleri yeni aylarda çalıştırılır.
5. **12 ay ölçeğinde çalıştırma:** toplu oynatma ve özellik hesabı. Bir gün ≈ 17–30 dk (oynatma) ve ≈ 3 dk (özellik); paralel çalıştırma (en çok 2 iş, 16 GB RAM) ya da hızlandırma gerekir. Arka planda uzun işler bellek baskısında sistemce durdurulabiliyor; uzun işleri parçalara bölmek (özellik hesabı kaldığı yerden devam eder) gerekir.
6. **SPK etiketleriyle pencere düzeyi:** etiketli pay-günlerde pencere puanları; denetimli modelin SPK etiketleriyle sınanması (12 ay veriyle).
7. **Defter göstergeleri:** motorla yeniden kurulan defterden derinlik ve alış/satış dengesizliği.
8. **Vize raporu:** literatür bölümü; öneri formu farklar tablosunda `[kullanıcı]` gerekçeleri (Monte Carlo bandı, piyasa geneli/paya özgü ayrımı, sanal-reel paralel çalışma); bu rapordaki bölüm 3'ün vize metnine dönüştürülmesi.
9. **Kural dosyalarının kullanıcı onayı** (veriyle birlikte; 05, 06, 08 ve açık [DOĞRULA] maddeleri).
10. **Özsermaye günleri:** düzeltilmiş baz fiyat kaynağı (motor bu günlerde işlem üretemez).

**Çalıştırma notları.**
- Tek sıra-gün: `python -I motor/tekrar_oynat.py veri/gun-ici-emir/gunluk veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet GUN KOD --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet`.
- Bütün gün: `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv`.
- Özellikler: `python -I tespit/ozellikler.py GUNLUK ISLEM GUNSONU CIKTI.parquet [GUN ...]` (parça parça çalıştırılabilir).
- Değerlendirme: `tespit/degerlendir.py`, `tespit/pencere_degerlendir.py` (`OLCEK` ortam değişkeniyle büyüklük), `tespit/denetimli.py`.
- Arayüz: `streamlit run arayuz/uygulama.py`.
- Testler: `python -m pytest motor/testler tespit/testler`.

## 4. 23.10.2026 — Fiyat yükseltme ve kapanış etkilemesi göstergeleri

Bu oturumda, 22.10.2026 sonunda zayıf kalan iki senaryo için yeni göstergeler eklendi ve tespit yeniden ölçüldü. Ölçütler bölüm 3.9'dakiyle aynıdır: ROC-AUC (0,5 rastgele), "ilk 3" (enjekte edilen pencerelerden birinin günün en yüksek puanlı 3 penceresinde olma oranı) ve "kontrol" (aynı pencerelerin enjeksiyonsuz koşuda ilk 3'e girme oranı, yani yanlış alarm tabanı).

### 4.1 Fiyat yükseltme: net agresif adım

- **Tanım (`tespit/pencere.py`):** sürekli işlemde, ardışık iki işlem arasında fiyat yükselmiş ve işlemin aktif tarafı alıcıysa +1, fiyat düşmüş ve aktif taraf satıcıysa −1. Pencere toplamı "net agresif adım"dır. Adım adım fiyat yükseltmenin (ramping) doğrudan izidir: her agresif alış satış tarafındaki en iyi seviyeyi tüketip fiyatı bir adım yukarı iter. Müzayede işlemleri sayılmaz.
- **Kural:** bent f (fiyat yükseltici/düşürücü işlemler) kuralına eklendi: |z(net agresif adım)| ≥ 3.
- **Örnek (KRGYO.E 27.03, 10 agresif alış × 20.000 lot):** enjekte edilen pencerede net agresif adım −1'den +4'e çıktı (z = 1,35); aynı gün olağan pencerelerde −11 ile +29 arasında değişir. Oynak ve likit bir payda 10 küçük agresif alış öne çıkmaz.
- **Sonuç (pencere, ×1):** kurallarda ROC-AUC 0,56 → 0,61, ilk 3'te isabet %0 → %10 (kontrol %5). Denetimli modelde değişiklik yok (0,62 / %25).
- **Yorum:** gösterge doğru yönde ama bu büyüklükteki fiyat yükseltme, payın olağan fiyat hareketinden ayrışmaz. Ölçek büyüdükçe etkisi 4.3'te.

### 4.2 Kapanış etkilemesi: üç yeni gösterge

- **Tanımlar (`tespit/kapanis_ozellikleri.py`; pay-gün):**
  - *kapanış müzayedesi sapması:* kapanış müzayedesi fiyatı / günün son sürekli işlem fiyatı − 1. Kapanışı itmenin doğrudan sonucudur;
  - *kapanış emir toplama dengesizliği:* kapanış emir toplamada girilen yeni emirlerin alış−satış miktar dengesizliği, (A − S)/(A + S);
  - *son dakika payı:* kapanış emir toplamadaki yeni emir, değişiklik ve iptallerin son 60 saniyeye düşen payı.
- **Hesap:** veriden (yalnız kapanış bölümü satırları okunduğu için 20 gün 3 dakikada) ve motor çıktısından aynı tanımlarla; KRGYO.E 27.03'te iki hesap birebir aynıdır. Mart 2025'te kapanış müzayedesi sapmasının standart sapması %0,5, uç değerleri ±%4.
- **Kurallar:** bent d kuralına eklendi: |z(kapanış müzayedesi sapması)| ≥ 3 ve |z(toplama dengesizliği)| ≥ 2 aynı yönde. Pay-gün kuralında (`yontemler.py`) ve kapanış penceresinin geçmiş kapanışlarla puanlanmasında (`pencere.kapanis_gecmisi`) aynı kural kullanılır.
- **Örnek (KRGYO.E 27.03, günlük hacmin %3'ü kadar kapanış alışı):** kapanış müzayedesi sapması %0,9 → %3,0; toplama dengesizliği 0,34 → 0,71.
- **Sonuç (pencere, ×1):** kurallarda ROC-AUC 0,60 → 0,80, ilk 3'te isabet %0 → %20 (kontrol %5); Z-skorda 0,83 / %15 (kontrol %0).
- **Yorum:** kapanış etkilemesi artık iz bırakıyor; önceki göstergeler (AOF sapması, kapanış seansı payı) kapanış emrinin etkisini gün geneline yayıyordu. Yeni göstergeler doğrudan kapanış müzayedesine bakar.
- SPK etiketleriyle sonuç değişmedi (ALKLC kesitsel ROC-AUC 0,90): ALKLC ve B vakaları kapanış etkilemesi değil, gün içi işlem bazlı şüphelerdir.

### 4.3 Güncel pencere sonuçları ve büyüklük duyarlılığı

Bütün yeni göstergelerle, 80'er enjeksiyon; büyüklükler ×0,3, ×1, ×3 (`veri/gunici-dogrulama/2025-03/tespit/olcek_duyarlilik.csv`, `pencere/`, `pencere_olcek_0.3/`, `pencere_olcek_3/`). Hücreler: ROC-AUC / ilk 3 / kontrol ilk 3.

| Senaryo | Ölçek | Kurallar | Denetimli |
|---|---|---|---|
| Yanıltıcı emir | ×0,3 | 0,89 / %79 / %5 | 0,81 / %58 / %0 |
| Karşılıklı işlem | ×0,3 | 0,45 / %5 / %5 | 0,78 / %40 / %15 |
| Fiyat yükseltme | ×0,3 | 0,58 / %5 / %5 | 0,63 / %15 / %10 |
| Kapanış | ×0,3 | 0,66 / %5 / %5 | — |
| Yanıltıcı emir | ×1 | 0,89 / %79 / %5 | 0,88 / %63 / %0 |
| Karşılıklı işlem | ×1 | 0,49 / %5 / %5 | 0,90 / %75 / %20 |
| Fiyat yükseltme | ×1 | 0,61 / %10 / %5 | 0,62 / %25 / %5 |
| Kapanış | ×1 | 0,80 / %20 / %5 | — |
| Yanıltıcı emir | ×3 | 0,89 / %79 / %5 | 0,90 / %79 / %0 |
| Karşılıklı işlem | ×3 | 0,56 / %0 / %5 | 0,96 / %100 / %15 |
| Fiyat yükseltme | ×3 | 0,63 / %10 / %5 | 0,63 / %30 / %0 |
| Kapanış | ×3 | 0,87 / %45 / %5 | — |

Yorum:
- **Yanıltıcı emir:** kurallar ölçekten bağımsızdır (0,89 / %79 / %5). Kısa ömürlü uzak emir payı bir oran olduğundan küçük katmanlar da iz bırakır; kural büyüklüğe değil davranış biçimine duyarlıdır. Bent f'nin genişlemesiyle bazı pencereler yarıştığından isabet %84'ten %79'a indi.
- **Kapanış etkilemesi:** yeni göstergelerle büyüklükle ölçeklenir: ×0,3'te zayıf (0,66), ×1'de 0,80, ×3'te 0,87 ve ilk 3'te %45; yanlış alarm her ölçekte %5. Önceki sürümde (geçmiş kapanışlarla puanlama, yeni göstergeler yok) ×1'de 0,60 ve isabet %0'dı.
- **Karşılıklı işlem:** yalnız denetimli modelle ve hacim artışıyla yakalanır; büyüklüğe güçlü bağlıdır (×0,3'te %40, ×3'te %100). Aktör kimliği olmadan "aynı kişinin iki tarafı" ayırt edilemez; yanlış alarm %15–20'dir.
- **Fiyat yükseltme:** net agresif adım göstergesine rağmen her ölçekte zayıftır (kurallar 0,58–0,63, denetimli ilk 3 en çok %30). 10 agresif alışın bıraktığı iz, likit paylarda olağan fiyat hareketi içinde kalır. Bu senaryo için daha uzun pencere (15–30 dk) ya da payın likiditesine göre ölçeklenmiş gösterge gerekir.
- Denetimli modelin kapanış satırı yoktur: model yalnız sürekli işlem pencerelerinde çalışır; kapanış penceresi geçmiş kapanışlarla puanlanır.

*Pencere uzunluğu (fiyat yükseltme):* 15 dakikalık pencereyle (`PENCERE_DK=15`; `pencere_15dk/`) fiyat yükseltme iyileşmedi: kurallar ROC-AUC 0,55, denetimli 0,56 (ilk 3 %35, kontrol %15). 15 dakikalık pencerede günde ≈ 33 pencere olduğundan ilk 3 hem pozitifte hem kontrolde daha kolay tutar. Sonuç: bu büyüklükteki fiyat yükseltme (200 sn'de 10 agresif alış, toplam ≈ günlük hacmin %5'i) likit paylarda olağan fiyat yolundan ayrışan bir iz bırakmaz. Bu, göstergenin değil senaryonun özelliğidir; senaryo daha büyük ve uzun yükseltmelerle sınanmalıdır.


### 4.4 SPK etiketli günlerde pencere düzeyi

- **Yöntem (`tespit/spk_pencere.py`):** Mart 2025'te SPK etiketli 76 pay-gün (A 12, B 64; belirsiz günler hariç), aynı payların 100 etiketsiz günü ve rastgele 300 pay-gün motorla oynatıldı. 5 dakikalık pencereler puanlandı (kapanış penceresi geçmiş kapanışlara göre). Gün puanı olarak uyarı penceresi sayısı, bent bazında uyarı sayıları ve en yüksek pencere puanı kullanıldı. Sonuçlar: `veri/gunici-dogrulama/2025-03/tespit/spk_pencere/`.
- **Sonuç:**

| Grup | Uyarı penceresi (ortalama) | a/b | f | d |
|---|---|---|---|---|
| A (ALKLC) | 11,9 | 3,4 | 8,6 | 0,00 |
| B | 19,5 | 12,4 | 8,4 | 0,02 |
| Aynı payların etiketsiz günleri | 13,7 | 5,8 | 8,4 | 0,07 |
| Rastgele pay-günler | 16,3 | 10,7 | 7,0 | 0,03 |

  ROC-AUC (etiketsiz bütün günler negatif): A için uyarı sayısı 0,43; B için 0,61 (a/b uyarıları 0,57).
- **Yorum:**
  - Pencere puanı aynı günün diğer pencerelerine göre hesaplanır. Manipülasyon bütün güne ve haftalara yayıldığında (ALKLC) gün içinde öne çıkan pencere olmaz; bu vakalarda doğru araç gün düzeyinde kesitsel karşılaştırmadır (ROC-AUC 0,90).
  - B günlerinde a/b (iptal, yanıltıcı emir) uyarıları daha sıktır; zayıf bir sinyaldir ve gün içi iptal / yanıltıcı emir epizotlarına işaret edebilir.
  - İki düzey birbirini tamamlar: gün düzeyi (kesitsel) uzun süreli manipülasyonu, pencere düzeyi kısa epizotları yakalar.

### 4.5 Defter göstergeleri

- **Yöntem:** motor sürekli işlem sırasında defteri 10 saniyede bir örnekler (`motor/gun.py`, `defter_ornekleri`): en iyi 5 seviyedeki görünen alış ve satış miktarı ile en iyi fiyatlar. Pencere göstergeleri (`tespit/pencere.py`): derinlik dengesizliği, (A − S)/(A + S) ortalaması, ve toplam derinlik. Ek süre ihmal edilebilir (KRGYO.E 27.03'te 2.879 örnek).
- **Sonuç (pencere, ×1, 80 enjeksiyon):** kurallarda değişiklik yok (yanıltıcı emir 0,88 / %79; kapanış 0,79 / %20). Denetimli modelde yanıltıcı emir 0,88 / %74 / kontrol %0, karşılıklı işlem 0,84 / %75 / %15, fiyat yükseltme 0,62 → 0,69 / %35 ama kontrol %5 → %15. Modelin özellik önemlerinde derinlik göstergeleri sıfıra yakındır.
- **Yorum:** bu aşamada katkı yoktur. Olası nedenler: en iyi 5 seviye, 4–6 adım uzaktaki yanıltıcı katmanları ancak kısmen kapsar; 10 saniyelik örnekleme 30 saniyelik bir epizodu birkaç örnekle görür. Göstergeler korunur; daha derin seviyeler ve olay anında örnekleme ile yeniden denenebilir.

### 4.6 Testler ve dosyalar

- 29 birim testi, hepsi geçer (`python -m pytest motor/testler tespit/testler`). Yeni: net agresif adım (müzayede işlemleri sayılmaz), kapanış toplama dengesizliği ve son dakika payı, defter derinliğinin pencereye toplanması.
- Yeni dosyalar: `tespit/spk_pencere.py` (SPK etiketli günlerde pencere düzeyi), `tespit/kapanis_ozellikleri.py` (var olan özellik tablosuna sütun ekleyebilir: `python -I tespit/kapanis_ozellikleri.py GUNLUK ISLEM OZELLIKLER.parquet`).
- Değişen: `motor/gun.py` (defter örneklemesi), `tespit/pencere.py` (net agresif adım, defter göstergeleri, `PENCERE_DK` ile pencere uzunluğu; kural bayrakları `kural_ab`, `kural_f`, `kural_d` sütunlarında), `ozellikler.py`, `motor_ozellikleri.py`, `yontemler.py`, `arayuz/hazirla.py` (bentler kural bayraklarından), `TASARIM.md` 6.6, `DURUM.md`.

### 4.7 Kaldığımız yer ve yapılacaklar

**Kaldığımız yer (23.10.2026).**
- 22.10.2026 sonundaki listeden yapılanlar:
  - fiyat yükseltme göstergesi (net agresif adım) ve 15 dakikalık pencere denemesi: senaryo bu büyüklükte ayırt edilemiyor (4.1, 4.3);
  - kapanış etkilemesi göstergeleri: ×1'de ROC-AUC 0,80, ×3'te 0,87 (4.2);
  - SPK etiketli günlerde pencere düzeyi: A'da sinyal yok, B'de zayıf (4.4);
  - defter göstergeleri: şimdilik katkı yok (4.5).
- Motor, arayüz ve tespit kodları, 29 test ve belgeler güncel; bu bölümle birlikte commit edildi.

**Yapılacaklar (öncelik sırasıyla).**
1. **Veri indirme (kullanıcı):** 2024-06…2025-02 (DataStore gün içi emir, gün içi işlem, gün sonu; ITCH yalnız 2025-01 ve 2025-02). Ardından her ay için parquet dönüşümü, günlük bölümleme, kayıpsızlık kontrolü (`rapor.md` 2.10). Aralık dışı dosyaların (2025-06…09) silinmesi kullanıcıdadır.
2. **Yeni aylar için tarih parametreleri:** marj, devre kesici yönü/oranı/süreleri, açığa satış kapsamı veriden yeniden ölçülür; Mart doğrulama betikleri yeni aylarda çalıştırılır.
3. **12 ay ölçeğinde çalıştırma:** toplu oynatma ve özellik hesabı; SPK değerlendirmesinin (gün ve pencere düzeyi) 12 ayla tekrarı; denetimli modelin SPK etiketleriyle sınanması. Uzun işler parça parça çalıştırılmalı.
4. **Vize raporu:** literatür bölümü; öneri formu farklar tablosunda `[kullanıcı]` gerekçeleri; bölüm 3 ve 4'ün vize metnine dönüştürülmesi.
5. **Kural dosyalarının kullanıcı onayı** (veriyle birlikte).
6. **Tespit iyileştirmeleri (isteğe bağlı):** fiyat yükseltme senaryosunun daha büyük ve uzun hâliyle sınanması; defter göstergelerinin daha derin seviyelerle ve olay anında örneklenmesi.
7. **Özsermaye günleri:** düzeltilmiş baz fiyat kaynağı.

Çalıştırma notları `DURUM.md` başındadır.
