# Proje: BIST Pay Piyasası eşleştirme motoru ve manipülasyon tespiti

Bilgisayar mühendisliği bitirme projesi (tek kişilik). Başlık: "Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi". Parçalar: (1) DataStore'dan alınan tarihsel ITCH verisi için çözümleyici ve emir defteri yeniden kurucu, (2) BIST kurallarına uygun eşleştirme motoru (sürekli işlem + tek fiyat; gerçek ITCH emir akışı tekrar oynatılıp araya sentetik manipülatif emirler enjekte edilir), (3) manipülasyon tespiti (iktisadi kurallar + denetimsiz model + denetimli model, SPK vakalarıyla değerlendirme).

Kod yazarken kural dosyalarının tamamını okuma; aşağıdaki tablodan yalnızca işe lazım olanı aç. Güncel durum ve açık işler: `DURUM.md`. Kural dosyalarının yazım kuralları: `gorev-kural-yazimi.md`.

## Kural dosyaları (`kurallar/`)

| Dosya | İçerik | Ne zaman okunur |
|---|---|---|
| `01-seanslar.md` | Seans saatleri (tek seans, bölümler/aşamalar), geçici durdurma, seans uzama/iptal esasları, seans durumu adları ve saat dizileri (Ek-9/10/11) | Seans durumu makinesi, saat çizelgesi, durumlara göre emir izinleri, `Order Book State` doğrulaması |
| `02-fiyat.md` | Lot, fiyat gösterimi, baz fiyat, fiyat adımları, referans fiyat, fiyat değişme sınırları, AOF, maddi hata iptali | Emir doğrulama (fiyat adımı, lot, tavan/taban), fiyat ölçeği |
| `03-tek-fiyat.md` | Tek fiyat yöntemi: işleyiş, 9 adımlı açılış fiyatı algoritması, emir sırası, kapanış seansı, kapanış fiyatından işlemler (en kritik dosya) | Açılış/kapanış/gün ortası/devre kesici denge fiyatı hesabı, tek fiyat dağıtımı |
| `04-surekli-islem.md` | Sürekli işlem yöntemi, fiyat/zaman önceliği, değişikliklerde öncelik kaybı/korunması, SMP, FIX/OUCH kaynaklı emir kuralları | Sürekli işlem eşleştirme, emir defteri sıralaması, replace/iptal önceliği |
| `05-emirler.md` | Emir tipleri (limit, piyasa, piyasadan limite, dengeleyici, kısmi görünme, Orta Nokta, AOF, kotasyon), değiştirme/iptal, değer sınırları, geçerlilik süreleri, Ek-19 seans×emir tipi matrisi | Emir girişi doğrulama, emir tipi davranışı, geçerlilik/iptal mantığı |
| `06-devre-kesici.md` | Pay bazında devre kesici, endekse bağlı devre kesici (EBDKS), EBDKS seans akışları ve izinleri | Devre kesici tetikleme, dinamik tek fiyat geçişi, EBDKS durdurma/yeniden açılış |
| `07-itch.md` | ITCH mesaj kuralları, veri tipleri, `Order Book Position`, Appendix A–E, örnek veri doğrulamaları | ITCH ayrıştırıcı, emir defteri yeniden kurucu, replay girdisi |
| `08-pazarlar-tedbirler.md` | Pazarlar ve işlem esasları (Tablo-3/4), piyasa yapıcılık/likidite sağlayıcılık (kotasyon kuralları), brüt takas, gruplama, bülten/raporlar (bağlam özeti) | Pazar bazlı parametreler, kotasyon doğrulama, partition eşlemesi |

Her dosyada `Kurallar` (madde no sona yazılı), `Açık sorular` (`[DOĞRULA]` açık, `[DOĞRULANDI …]`/`[KISMEN DOĞRULANDI …]` kapalı, `[BİLGİ …]` ölçüm notu) ve `Test örnekleri` bölümleri vardır. Birim testi verisi `Test örnekleri`ndedir.

## Diğer kaynaklar (gerektiğinde)

| Yer | İçerik |
|---|---|
| `ekler/README.md` | Prosedür Ek-1…Ek-21 dosya listesi, hangi kural dosyasında hangi Ek okunur (tablolar doğrulanmıştır) |
| `veri/README.md` | Veri notları (endeks ölçek değişikliği 27.07.2020, veri tarihi ↔ Prosedür sürümü farkı, klasör düzeni) |
| `veri/*-protokol-spesifikasyonu.md` | ITCH 2112, MoldUDP64, SoupBinTCP, OUCH, FIX Reference Data, FIX Order Entry (kapsamı sınırlı) Türkçe çevirileri; `emrimle-eslesmesin-…md` (SMP); `datastore-dosya-formatlari.md` |
| `veri/itch-ornek-veri-dogrulama.md` | 08.10.2018 ITCH örnek verisi doğrulama sonuçları |
| `veri/araclar/` | Doğrulama betikleri (yollar oturuma özgüdür) |
| `kaynaklar/README.md` | Ham PDF'ler (git dışı) ve `_kullanilmayan/` |

## Çalışma kuralları

- Kaynakta olmayan kural ekleme. Belirsizliği yorumlama, `Açık sorular`a `[DOĞRULA]` ile yaz. Veriden gelen kanıt yine `[BİLGİ]` olarak işaretlenir; kullanıcı kararı `Uygulama kararı (kullanıcı)` olarak açıkça yazılır.
- Dosya adlarında Türkçe karakter kullanma. Tablolar GFM uyumlu olsun (başlık hücre sayısı = ayraç hücre sayısı). Büyük dosya yazımında Python heredoc yerine dosya yazıp çalıştır.
- Örnek veri 08.10.2018 tarihlidir; kurallar yürürlükteki Prosedürdür (rev. 21/09/2026). Tarihe bağlı parametreler (devre kesici süreleri, pazar eşikleri vb.) tarih parametresi olarak tutulmalıdır.
- Bir kural dosyasına kullanıcı kararı veya doğrulama işlediğinde, aynı işte `DURUM.md` satırını ve bu dosyadaki "Kodlamayı etkileyen kullanıcı kararları" listesini de güncelle; kullanıcıdan ayrıca isteme.
- `veri/itch/` ve `kaynaklar/` git dışıdır. Hiçbir şeyi kullanıcı istemeden commit etme.

## Kodlamayı etkileyen kullanıcı kararları (ayrıntı ilgili dosyada)

- Gün tek seanstır; parçalar "Bölüm/Aşama (Phase/State)" olarak adlandırılır ("her seans günde 5 kez" ve "açılış seansı" eski terminolojidir). → `01-seanslar.md` madde 3
- Seans uzama/iptal (4.3.3) kuralları otomatize edilmez, Olağanüstü Durum Yönetim Grubu'nun manuel kararına bağlıdır; yarım günlerde 14:00–16:00 ertelemesi yoktur. → `01-seanslar.md` madde 78–79, 82, 92
- Yarım iş günlerinde 3 kez tek fiyat uygulanır (saatler Ek-10 `P_TEK_FIY_YG`); gün ortası tek fiyat aşaması yalnızca tek fiyatla işlem gören araçlar için güncel. → `03-tek-fiyat.md` madde 11, 13
- Pay bazında devre kesici emir toplama süresi 10 dk (5.3.4 güncel; Tablo-4'ün 5/15/15 satırı eski), devre kesici eşleştirmesi sabit saatte. → `06-devre-kesici.md` madde 13, 16
- Kısmi görünme izni Ek-19 matrisine göre; askıya alma = iptal + yeni emir; marj dışı: tarihli emirler gün başı iptal, gün içi limit kayması duraklatma; açılışta piyasa emri paylarda yalnızca Yıldız/Ana Pazar; emir bilgisi alanları (MPF-AFK-Hesap No) değiştirilemez. → `05-emirler.md`, `03-tek-fiyat.md` madde 24
- Tek fiyat algoritması Adım 3–5 (piyasa yönü, eşit uzaklık, yuvarlama) ve referans fiyat kaynağı kaynaklarda ve ITCH'te kanıtlanamadı; uygulama kararı bekliyor (öneri: Seçenek 1, eşitlikte yüksek, yukarı yuvarlama, açılışta ARF/kapanışta son işlem). → `03-tek-fiyat.md` Açık sorular
- ITCH'te müzayede emir toplama aşamasında tek tek emir (`A`) yayımlanmaz, yalnızca `Z` (denge); açılış/kapanış defteri yeniden kurulamaz, motor tek fiyat çıktısı `Z`/`P` ile doğrulanır. DataStore `PP_GUNICIEMIR` ile tek günlük emir verisi bu soruları kapatabilir.
