# Proje: BIST Pay Piyasası eşleştirme motoru ve manipülasyon tespiti

Bilgisayar mühendisliği bitirme projesi (tek kişilik). Başlık: "Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi". Parçalar:

1. DataStore gün içi verisi (gün içi emir `PP_GUNICIEMIR`, gün içi işlem `PP_GUNICIISLEM`, gün sonu fiyat-hacim `PP_GUNSONUFIYATHACIM`) için hazırlama ve emir defteri yeniden kurucu. ITCH yalnız 2 aylık örnektir ve çapraz doğrulamada kullanılır.
2. BIST kurallarına uygun eşleştirme motoru (sürekli işlem + tek fiyat + devre kesiciler). Gerçek emir akışı (DataStore emir olayları) tekrar oynatılır, araya sentetik manipülatif emirler enjekte edilir.
3. Manipülasyon tespiti: iktisadi kurallar + denetimsiz model + denetimli model; SPK vakalarıyla değerlendirme.

Sistem tasarımı: `TASARIM.md`.

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
| `07-itch.md` | ITCH mesaj kuralları, veri tipleri, `Order Book Position`, Appendix A–E, örnek veri doğrulamaları | ITCH ayrıştırıcı, ITCH örneğiyle defter çapraz doğrulaması (ana tekrar oynatma girdisi DataStore emir olaylarıdır, `TASARIM.md`) |
| `08-pazarlar-tedbirler.md` | Pazarlar ve işlem esasları (Tablo-3/4), piyasa yapıcılık/likidite sağlayıcılık (kotasyon kuralları), brüt takas, gruplama, bülten/raporlar (bağlam özeti) | Pazar bazlı parametreler, kotasyon doğrulama, partition eşlemesi |

Her dosyada `Kurallar` (madde no sona yazılı), `Açık sorular` (`[DOĞRULA]` açık, `[DOĞRULANDI …]`/`[KISMEN DOĞRULANDI …]` kapalı, `[BİLGİ …]` ölçüm notu) ve `Test örnekleri` bölümleri vardır. Birim testi verisi `Test örnekleri`ndedir.

## Diğer kaynaklar (gerektiğinde)

| Yer | İçerik |
|---|---|
| `Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.docx` | Bölüme verilen öneri formu: başlık, 12 adım, yarıyıl hedefleri, iş-zaman çizelgesi (Eylül–Mayıs) |
| `Başvuru Dilekçesi.pdf` | Borsa İstanbul DataStore veri talebi (13.10.2026): istenen veri türleri ve tarih aralıkları |
| `ekler/README.md` | Prosedür Ek-1…Ek-21 dosya listesi, hangi kural dosyasında hangi Ek okunur (tablolar doğrulanmıştır) |
| `veri/README.md` | Veri notları (endeks ölçek değişikliği 27.07.2020, veri tarihi ↔ Prosedür sürümü farkı, klasör düzeni) |
| `veri/*-protokol-spesifikasyonu.md` | ITCH 2112, MoldUDP64, SoupBinTCP, OUCH, FIX Reference Data, FIX Order Entry (kapsamı sınırlı) Türkçe çevirileri; `emrimle-eslesmesin-…md` (SMP); `datastore-dosya-formatlari.md` |
| `TASARIM.md` | Sistem tasarımı (sürüm 2: DataStore gün içi verisi): veri katmanı, tarih parametreleri, motor modları, enjeksiyon, tespit |
| `motor/` | Eşleştirme motoru (Python): sürekli işlem, tek fiyat (müzayede), DataStore okuyucu, tekrar oynatma (`tekrar_oynat.py`, toplu: `toplu_oynat.py`), testler (`testler/`); `TASARIM.md` 4.5 |
| `tespit/` | Tespit: pay-gün özellikleri (`ozellikler.py`, kapanış: `kapanis_ozellikleri.py`), Z-skor, iktisadi kurallar, Isolation Forest, SPK etiketleri (`yontemler.py`), 5 dk pencere (`pencere.py`), denetimli model (`denetimli.py`), değerlendirme (`degerlendir.py`, `sentetik_degerlendir.py`, `pencere_degerlendir.py`); `TASARIM.md` 6 |
| `arayuz/` | Görselleştirme ve enjeksiyon arayüzü (Streamlit: `streamlit run arayuz/uygulama.py`); `TASARIM.md` 6.5 |
| `motor/tarih_parametreleri.csv` | Tarihe bağlı kural parametreleri (marj, DK, EBDKS, fiyat adımı, açığa satış, müzayede pencereleri); veriden ya da metinden, geçerlilik aralığı ve kaynakla |
| `rapor.md` | Çalışma raporu (vize raporunun kaynağı): 21.10.2026'ya kadar yapılanların özeti ve oturum kayıtları |
| `veri/gunici-veri-dogrulama.md` | Mart 2025 DataStore gün içi verisi doğrulamaları (alan anlamları, gün sonu, marj, seans, Ek-19, emir kuralları, öncelik, tek fiyat, devre kesiciler, tarih parametreleri) |
| `veri/itch-ornek-veri-dogrulama.md` | 08.10.2018 ITCH örnek verisi doğrulama sonuçları |
| `veri/araclar/` | Doğrulama betikleri (yollar oturuma özgüdür) |
| `kaynaklar/README.md` | Ham PDF'ler (git dışı) ve `_kullanilmayan/` |

## Çalışma kuralları

- Kaynakta olmayan kural ekleme. Belirsizliği yorumlama, `Açık sorular`a `[DOĞRULA]` ile yaz. Veriden gelen kanıt yine `[BİLGİ]` olarak işaretlenir; kullanıcı kararı `Uygulama kararı (kullanıcı)` olarak açıkça yazılır.
- Dosya adlarında Türkçe karakter kullanma. Tablolar GFM uyumlu olsun (başlık hücre sayısı = ayraç hücre sayısı). Büyük dosya yazımında Python heredoc yerine dosya yazıp çalıştır.
- Ana veri Mart 2025 DataStore gün içi verisidir (ITCH örneği 08.10.2018); kurallar yürürlükteki Prosedürdür (rev. 21/09/2026). Tarihe bağlı parametreler (fiyat marjı, devre kesici yön/oran/süreleri, EBDKS, pazar eşikleri vb.) tarih parametresi olarak tutulmalıdır; Mart 2025 değerleri `TASARIM.md` 3.6'dadır.
- Bir kural dosyasına kullanıcı kararı veya doğrulama işlediğinde, aynı işte `DURUM.md` satırını ve bu dosyadaki "Kodlamayı etkileyen kullanıcı kararları" listesini de güncelle; kullanıcıdan ayrıca isteme.
- `veri/itch/`, `veri/gun-ici-emir/`, `veri/gun-ici-islem/`, `veri/gun-sonu-fiyat-hacim/` ve `kaynaklar/` git dışıdır. Hiçbir şeyi kullanıcı istemeden commit etme.

## Kodlamayı etkileyen kullanıcı kararları (ayrıntı ilgili dosyada)

- Gün tek seanstır; parçalar "Bölüm/Aşama (Phase/State)" olarak adlandırılır ("her seans günde 5 kez" ve "açılış seansı" eski terminolojidir). → `01-seanslar.md` madde 3
- Seans uzama/iptal (4.3.3) kuralları otomatize edilmez, Olağanüstü Durum Yönetim Grubu'nun manuel kararına bağlıdır; yarım günlerde 14:00–16:00 ertelemesi yoktur. → `01-seanslar.md` madde 78–79, 82, 92
- Yarım iş günlerinde 3 kez tek fiyat uygulanır (saatler Ek-10 `P_TEK_FIY_YG`); gün ortası tek fiyat aşaması yalnızca tek fiyatla işlem gören araçlar için güncel. → `03-tek-fiyat.md` madde 11, 13
- Pay bazında devre kesici: yürürlükteki metinde emir toplama 10 dk (Tablo-4'ün 5/15/15 satırı eski). Eşleştirme, sabit emir toplama süresinden sonra **tarihe bağlı rastlantısal pencere** içinde başlar (21.10.2026 kararı; Mart 2025: 30 sn, 2018: 0 sn). → `06-devre-kesici.md` madde 13, 16
- Tablo-4 ile veri farkı (marj, DK yön/oran/süre): verideki fiili eşikler kullanılır. Fark "Borsa İstanbul Pay Piyasası Prosedürü Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak not edilir. Değerler `motor/tarih_parametreleri.csv`'de (Mart 2025: marj ±%10, DK yalnız düşüşte %5 / 15 dk). → `02-fiyat.md`, `06-devre-kesici.md`, `08-pazarlar-tedbirler.md`
- Kısmi görünme izni Ek-19 matrisine göre; askıya alma = iptal + yeni emir; marj dışı: tarihli emirler gün başı iptal, gün içi limit kayması duraklatma; açılışta piyasa emri paylarda yalnızca Yıldız/Ana Pazar; emir bilgisi alanları (MPF-AFK-Hesap No) değiştirilemez (sentetik emirlerde reddedilir; tekrar oynatmada AFK dolu emirde fiyatı/kalanı değişmeyen değişiklik önceliği kaybettirir, 22.10.2026 kararı). → `05-emirler.md`, `03-tek-fiyat.md` madde 24, `04-surekli-islem.md` madde 24
- Tek fiyat algoritması: Adım 3 (kalan miktarın yönü, kullanıcı kararı) ve Adım 4 referansı Mart 2025 müzayedeleriyle doğrulandı (referans = baz fiyat; 29.633 müzayedenin %99,96'sında fiyat tutar). Kapanışta aday fiyatlar son işlem ±%3'üne sınırlıdır. Karışık yön (21.10.2026 kararı): referansa / son işlem fiyatına en yakın aday, eşitlikte orta nokta; uymayan vakalar `yon_karisik_istisna = 1` (Mart 2025: 2 uyan, 2 istisna). Açık kalan: Adım 4 eşit uzaklık ve Adım 5 yuvarlama (veride hiç oluşmadı). → `03-tek-fiyat.md` Açık sorular
- ITCH'te müzayede emir toplama aşamasında tek tek emir (`A`) yayımlanmaz; DataStore `PP_GUNICIEMIR` ile müzayede defterleri yeniden kurulabilir ve motor uçtan uca doğrulanır (`TASARIM.md`).
- Veri ayları (21.10.2026): ITCH örneği **2025-01 ve 2025-02** (A seviyesi vakalar KRGYO, TDGYO, ALKLC; önce onaylanan 03/04 yerine); bu iki ay için DataStore emir, işlem ve gün sonu dosyaları da alınır. DataStore emir, işlem ve gün sonu verisi **2024-06…2025-05** arası, 12 ay (12.10.2026 planı ITCH + gün sonu içindi; DataStore geçişiyle bu dosyalara aktarıldı, 22.10.2026); 2025-01/02 bu aralığın içindedir; gerekirse genişletilir. "2025-07 alınmaz" yalnız ITCH içindir (karşılaştırma `veri/etiketler/ay_etiket_ortusmesi.csv`). → `TASARIM.md` 3.5, 6.4
- Sistem kapsamı (22.10.2026): öneri formundaki ajan tabanlı simülasyon (yatırımcı ajanları, GA/PSO, Monte Carlo bandı) yapılmaz; sistem eşleştirme motoru + denetimsiz ML + denetimli ML (SPK etiketleri) + iktisadi kurallardır. Formdan basit ve yararlı olanlar eklenir: Z-skor temel çizgisi, görselleştirme (zorunlu; emir enjeksiyonu ve uyarılar grafikte), eklenebilirse Isolation Forest. Formla farklar vize raporunda açıklanır. B seviyesi etiket penceresi N = 20 işlem günü, yasaktan 3 iş günü önce biter; yasaktan önceki 2 iş günü belirsizdir, değerlendirme dışıdır (22.10.2026 kararı; `veri/etiketler/etiket-cikarim-kurallari.md`). Veri: dilekçedeki 01.06.2024–31.05.2025 aralığında DataStore emir, işlem ve gün sonu; ITCH yalnız 2025-01/02. → `TASARIM.md` 1, 6.3, 6.5, `rapor.md` 3
- Zaman önceliği: `emir_giris_zamani` öncelik zamanı değildir. Öncelik; yeni emir, fiyat değişikliği, kalan miktar artışı ve kısmi görünme yenilemesinde (sebep 13) güncellenir (veri, %99,76). → `04-surekli-islem.md` Açık sorular
