# Çalışma raporu

Bu dosya, bitirme projesi vize raporunun yazılacağı kaynak kayıttır. Önce 21.10.2026'ya kadar yapılanlar özetlenir, sonra oturumlar tarih başlığı altında ayrıntılı kaydedilir (bölüm 2: 21.10.2026, bölüm 3: 22.10.2026). Ayrıntılı teknik sonuçlar ilgili dosyalardadır; bu raporda yalnız özetleri ve sayıları vardır.

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

`tespit/` (`TASARIM.md` 6.6):
- **Pay-gün özellikleri:** emir akışı (iptal, değişiklik ve emir/işlem oranları, piyasa / KİE / açığa satış / AFK payları, fiyat kademesi sayısı, açılış iptalleri, kapanış toplamadaki değişiklik yoğunluğu), işlem (getiri, aralık, aktif taraf dengesizliği, küçük işlem payı, kapanış seansı ve kapanış fiyatından işlem payları, kapanışın AOF'den sapması, kapanış öncesi getiri) ve referans. Mart 2025'te 20 gün × 590 sıra.
- **Yöntemler:**
  - Z-skor (payın kendi geçmişine göre);
  - VI-104.1 md 5/1 a, b, d, f bentlerine bağlı kurallar;
  - Isolation Forest;
  - kesitsel karşılaştırma (aynı gün aynı pazardaki paylar içinde yüzdelik sıra; 5 günlük getiri ve hacim artışı dahil).
- **Ölçülemeyen bentler:** aktör gerektiren bentler (c yön değiştiren emir, ç kendinden kendine işlem) gerçek veride ölçülemez; yalnız sentetik aktörde ölçülebilir.

Sonuç (SPK etiketli pay-günler: A 12, B 56; ROC-AUC):

| Puan | A | B | A+B |
|---|---|---|---|
| Z-skor (kendi geçmişi) | 0,64 | 0,50 | 0,52 |
| İktisadi kurallar | 0,47 | 0,57 | 0,55 |
| Isolation Forest (Z-skor) | 0,50 | 0,54 | 0,54 |
| Kesitsel uç sıra | 0,82 | 0,52 | 0,58 |
| Kesitsel Isolation Forest | 0,85 | 0,55 | 0,61 |

Yorum:
- Kendi geçmişine dayanan yöntemler haftalarca süren manipülasyonda zayıftır, çünkü geçmiş de manipülasyon içerir.
- Kesitsel karşılaştırmada ALKLC pay-günleri gün içinde ortalama 87. yüzdeliktedir.
- B pencereleri varsayımdır; Mart'taki B günlerinin bir kısmı pencere kenarındadır.
- Pozitif sayısı azdır. Sonuçlar 12 aylık veriyle ve sentetik enjeksiyon etiketleriyle yeniden ölçülmelidir.

Sentetik enjeksiyonla değerlendirme (`tespit/sentetik_degerlendir.py`, `motor_ozellikleri.py`; 80 rastgele pay-gün, dört senaryo, payın günlük hacmine göre ölçekli; `veri/gunici-dogrulama/2025-03/tespit/sentetik/`):
- Kontrol: enjeksiyonsuz motor özellikleri veriden hesaplananlarla neredeyse aynıdır; kontrol kümesinde ROC-AUC ≈ 0,5 (yöntem farkı sahte tespit üretmez).
- Pay-gün düzeyinde yöntemler kısa süreli enjeksiyonları ayırt edemez: ROC-AUC 0,40–0,74. En iyisi kapanış senaryosunda iktisadi kurallar (0,74). Kısa bir epizot günün toplamında kaybolur; 5 dakikalık pencere gerekir. Karşılıklı işlem aktör kimliği olmadan ölçülemez.
- Ardından yanıltıcı emir göstergesi eklendi: kısa ömürlü uzak emir payı (en iyi fiyattan ≥ 3 adım uzakta girilip 60 sn içinde işlem görmeden iptal edilen miktar payı) ve makas. ALKLC 11.03'te %7,4 (gün ortancası %1,4). Bu özelliklerle değerlendirme yeniden yapılacak.

5 dakikalık pencere ve denetimli model (`tespit/pencere.py`, `pencere_degerlendir.py`, `denetimli.py`; 77 pay-gün, pozitif pencere oranı %2; `veri/gunici-dogrulama/2025-03/tespit/pencere/`):

| Senaryo | Kurallar: ROC-AUC / ilk 3 | Denetimli: ROC-AUC / ilk 3 | Denetimli: kontrol ilk 3 |
|---|---|---|---|
| Yanıltıcı emir | 0,85 / %70 | 0,89 / %60 | %5 |
| Karşılıklı işlem | 0,47 / %5 | 0,86 / %68 | %5 |
| Fiyat yükseltme | 0,58 / %5 | 0,74 / %21 | %5 |
| Kapanış | 0,84 / %42 | 0,92 / %95 | %84 |
| Hepsi | 0,67 / %31 | 0,85 / %61 | %25 |

- "İlk 3": pozitif pencerelerden biri günün en yüksek puanlı 3 penceresinde. "Kontrol": aynı pencerelerin enjeksiyonsuz koşuda ilk 3'e girme oranı (yanlış alarm tabanı).
- Pencere düzeyi pay-gün düzeyinden belirgin biçimde iyidir. Yanıltıcı emir kurallarla da yakalanır ve kontrolde yanlış alarm yoktur.
- Kapanış senaryosunda sonuç şişkindir: kapanış müzayedesi penceresi her gün uç değerdir; denetimli model enjeksiyonsuz günde de %84 alarm verir.
- Denetimli modelin en önemli özelliği hacim z'sidir; karşılıklı işlem hacim artışıyla yakalanır, aktör belirlenemez. Fiyat yükseltme en zor senaryodur.
- Senaryo büyüklükleri bir varsayımdır; sonuçlar bu büyüklüklere bağlıdır (`TASARIM.md` 6.6).

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

`motor/testler/` altında 23 birim testi, hepsi geçer (`python -m pytest motor/testler`):
- sürekli işlem: Ek-18 2.2.2 piyasa emri ve 3.2.2 piyasadan limite örnekleri; KİE; işlemin pasif emrin fiyatından olması; öncelik kaybı ve korunması; fiyat değişikliğinin agresif eşleşmesi; iptal; kısmi görünme; görünmeyen alan değişikliği;
- tek fiyat: dağıtım sırası, dengeleyici emirler, kalanlar, emir toplamada öncelik;
- tepe tahmini: Mart 2025 verisinden alınmış dört örnek;
- doğrulama: fiyat adımı ve sınırlar, Ek-19 izinleri, kapanış kuralları, değişiklik izinleri, açığa satış.

### 3.12 Bu oturumda üretilen dosyalar

| Tür | Dosya |
|---|---|
| Motor | `motor/emir.py`, `defter.py`, `surekli_islem.py`, `tek_fiyat.py`, `gun.py`, `dogrulama.py`, `veri.py`, `parametreler.py`, `senaryolar.py`, `tekrar_oynat.py`, `toplu_oynat.py`, `enjeksiyon.py` |
| Testler | `motor/testler/test_surekli_islem.py`, `test_tek_fiyat.py`, `test_tepe.py`, `test_dogrulama.py` |
| Arayüz | `arayuz/uygulama.py`, `arayuz/hazirla.py` |
| Tespit | `tespit/ozellikler.py`, `yontemler.py`, `degerlendir.py` |
| Çıktılar | `veri/gunici-dogrulama/2025-03/motor/` (sıra-gün özetleri, `ozet.csv`, `toplu_*.csv`), `veri/gunici-dogrulama/2025-03/tespit/` (`degerlendirme.csv`, `kural_oranlari.csv`, `etiketli_siralama.csv`) |
| Belgeler | `TASARIM.md` (1, 4.5, 6.3, 6.5, 6.6), `kurallar/03-tek-fiyat.md`, `04-surekli-islem.md`, `05-emirler.md`, `06-devre-kesici.md` ([BİLGİ] notları ve kararlar), `veri/etiketler/etiket-cikarim-kurallari.md` (N kararı), `DURUM.md`, `CLAUDE.md`, `veri/README.md`, `.gitignore`, `ekler/ek3.md`, `ek4.md` |

Motor, arayüz, tespit kodları, testler, özet çıktılar ve belge güncellemeleri 22.10.2026'da commit edildi ("Eşleştirme motoru, arayüz ve tespit ilk sürümü"). Ham veri ve parquet ara çıktıları git dışıdır.

### 3.13 Açık konular ve sonraki adımlar

- **Motor:**
  - seans durum makinesi (simülasyonda Ek-10 çizelgesi ve rastlantısal eşleşme anı; tekrar oynatmada bölüm geçişleri veriden);
  - kotasyonlar (`.F`), orta nokta emirleri;
  - kısmi görünme emirlerinde tepe belirsizliği; aynı fiyatta miktar azaltmada nadir öncelik kaybı;
  - performans: bir günün bütün payları 17–30 dk; 12 ay için derlenmiş çekirdek ya da paralel çalıştırma gerekebilir.
- **Tespit:**
  - defter özellikleri ve 5 dakikalık pencere;
  - sentetik enjeksiyonla etiketli değerlendirme (kesinlik, duyarlılık, F1);
  - denetimli model;
  - arayüzde kural ve model uyarıları.
- **Kullanıcı kararı (22.10.2026):** madde 24 kararı sentetik emirlerde geçerli kalır (emir bilgisi değişikliği reddedilir); tekrar oynatmada veride görülen öncelik kaybı uygulanır.
- **Kullanıcı kararı bekleyen:** B seviyesi pencere bitişinin yasaktan 3 iş günü önceye alınıp alınmayacağı.
- **Veri:** 2024-06…2025-02 dosyalarının indirilmesi; bu aylar için tarih parametrelerinin (marj, devre kesici, açığa satış) veriden yeniden ölçülmesi.
- **Rapor:** vize raporu için literatür bölümü.
