# Sistem tasarımı

Sürüm 2 — 21.10.2026. Ana veri kaynağı ITCH'ten DataStore gün içi verisine (gün içi emir, gün içi işlem, gün sonu fiyat-hacim) geçmiştir; ITCH yalnızca 2 aylık örnek olarak alınacaktır. Proje amacı değişmemiştir. Bu belgedeki veri özellikleri Mart 2025 verisiyle doğrulanmıştır; ayrıntı ve sayılar `veri/gunici-veri-dogrulama.md` dosyasındadır.

## 1. Amaç (değişmedi)

"Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi". Üç parça:

1. Veri katmanı: tarihsel emir ve işlem verisinden emir defterinin pay ve gün bazında yeniden kurulması.
2. Eşleştirme motoru: BIST kurallarına uygun (sürekli işlem, tek fiyat, devre kesiciler). Gerçek emir akışı tekrar oynatılır, araya sentetik manipülatif emirler enjekte edilir ve bunların gerçek emirlerle etkileşimi hesaplanır.
3. Manipülasyon tespiti: iktisadi kurallar, denetimsiz model ve denetimli model. Değerlendirme SPK vakalarıyla yapılır.

Öneri formundaki ajan tabanlı yapay borsa simülasyonu (yatırımcı ajanları, GA/PSO kalibrasyonu, Monte Carlo olasılık bandı, sanal-reel paralel çalışma) bu sistemde yoktur (kullanıcı kararı, 22.10.2026). Farklar ve gerekçe vize raporunda açıklanır (`rapor.md` bölüm 3).

## 2. Neden değişti

| Konu | ITCH (sürüm 1) | DataStore gün içi (sürüm 2) |
|---|---|---|
| Kapsam | 2 aylık örnek | Emir, işlem ve gün sonu verisi aylık, hedef 2024-06…2025-05 (12 ay; 22.10.2026). Eldeki parquet (22.10.2026): emir 2025-03…07, işlem 2025-03…09, gün sonu 2025-03…08 |
| Müzayede (emir toplama) aşamasındaki emirler | Yayımlanmaz (yalnız denge `Z`) | Her emir olayı var; açılış, kapanış, tek fiyat, devre kesici ve EBDKS defterleri yeniden kurulabilir |
| İşlemin tarafları | `E`/`C` yalnız pasif emri gösterir | Her işlem için alış ve satış satırı, iki tarafın emir numarası, aktif/pasif bayrağı |
| Emir tipi ve özellikleri | Kısıtlı (`A` alanları) | Fiyat türü, emir türü (açığa satış, orta nokta), kategori (emir, kotasyon, özel işlem bildirimi), geçerlilik, AFK bayrağı, değişiklik sebebi |
| Gün sonu karşılaştırması | Yok | Bülten alanları işlemlerden birebir yeniden üretilebiliyor |
| Kimlik | Yok | Yok (üye/hesap kimliği yok; yalnız AFK bayrağı) |
| Zaman | ns, global mesaj sırası | Emir µs (İstanbul saati), işlem ms; aynı µs içinde emirler arası sıra bilgisi yok |

Sonuç: Sürüm 1'de "açılış/kapanış defteri yeniden kurulamaz, motor yalnız `Z`/`P` ile doğrulanır" kısıtı vardı. Sürüm 2'de bu kısıt kalkar ve motor müzayedeler dâhil uçtan uca doğrulanabilir. ITCH'in rolü ikincildir: DataStore'dan kurulan defterin kamu yayınıyla eşdeğerliğini sınamak ve "piyasanın gördüğü" defteri (tespit özellikleri için) üretmek.

## 3. Veri katmanı

### 3.1 Kaynaklar

| Kaynak | Klasör | Satır (Mart 2025) | Birim | Rol |
|---|---|---|---|---|
| `PP_GUNICIEMIR` | `veri/gun-ici-emir/` | 1.128.466.831 | Emir olayı sonrası emrin tam durumu | Birincil girdi: emir niyetleri, defter |
| `PP_GUNICIISLEM` | `veri/gun-ici-islem/` | 234.387.516 (117.193.758 işlem × 2 taraf) | İşlemin bir tarafı | Motorun doğruluk hedefi; işlem özellikleri |
| `PP_GUNSONUFIYATHACIM` | `veri/gun-sonu-fiyat-hacim/` | 192.220 | Sıra-gün | Referans veri (baz fiyat, pazar, işlem yöntemi, endeks üyeliği, piyasa yapıcı); gün sonu doğrulaması |
| ITCH (2 ay) | `veri/itch/` | — | Kamu yayını mesajı | Çapraz doğrulama (bkz. 3.5) |
| SPK bültenleri | `veri/etiketler/` | 340 kod satırı | Vaka | Değerlendirme etiketleri |

Alan adları `veri/araclar/gunici_*_csv2parquet.py` dosyalarındaki ASCII adlardır. Alan tanımları için `veri/datastore-dosya-formatlari.md` (2.1.16–2.1.18 ve 3.1 referans tabloları) kullanılır.

### 3.2 Doğrulanmış veri özellikleri (Mart 2025)

- **Gün bağımsızlığı:** Geçerlilik türü yalnız `DAY` ve `IMMEDIATE` (KİE). Her emir girildiği gün içinde yaşar; günün sonunda aktif kalan emirler `P_GUNSONU` bölümünde sebep 19 (Expired) ile kapanır. Bu yüzden motor her günü bağımsız oynatabilir. Önceki günden yalnız baz fiyat gelir.
- **Satır anlamı:** Her satır, bir olaydan sonra emrin tam durumudur. Olay sebepleri:
  - 6 yeni, 5 değişiklik, 1 kullanıcı iptali,
  - 3 işlem, 8 sistem dönüşümü, 13 yenileme,
  - 9/34/116/117 sistem iptalleri, 19 süre dolumu, 4 pasifleştirme.

  `guncelleme_no` emir içinde artar; pay grubunda ardışık satırların %0,9'unda 1'den fazla artar (arada yazılmamış olay vardır, türü bilinmiyor). İşlem taşıyan satırlar `islem_numarasi` dolu satırlardır; bunlar yalnız sebep 3 değil, 13, 8, 9 ve 34 de olabilir.
- **Anahtarlar:** `emir.islem_numarasi = int(islem.ortak_sozlesme_no, 16)`. `islem.emir_no`, ilgili tarafın `emir.emir_no` değeridir.
- **Zaman:**
  - `emir_giris_zamani` ve `emir_degistirilme_zamani` İstanbul saatidir, µs çözünürlüklüdür.
  - `guncelleme_zamani` UTC'dir, saniye çözünürlüklüdür (yerel − 3 saat).
  - `islem_zamani` İstanbul saatidir, ms çözünürlüklüdür.
  - `islem_degistirilme_zamani` ve işlem dosyasındaki `guncelleme_zamani` UTC'dir.
- **Öncelik zamanı veride yazılı değildir:** `emir_giris_zamani` emir ömrü boyunca hiç değişmez (fiyat değişikliğinde bile), bu yüzden zaman önceliği anahtarı değildir. Öncelik zamanı olay dizisinden türetilir. Bu zaman şu olaylarda o olayın zamanına güncellenir:
  - yeni emir,
  - fiyat değişikliği,
  - **kalan** miktarın artması (emir miktarı alanı değil),
  - kısmi görünme koşullu emrin görünen kısmının yenilenmesi (sebep 13).

  Veriyle uyum için bkz. doğrulama raporu, öncelik bölümü.
- **Kısmi görünme koşullu emirler:** `gorunen_miktar` her satırda `emir_miktari`'na eşit yazılmıştır, görünen kısım bu alandan okunamaz. Buna karşın bu emirler vardır ve sebep 13 (RefreshedBySystem) satırlarından tanınır. Görünen kısım işlem görüp yenilendiğinde emir fiyat seviyesinin sonuna gider.
- **Kotasyonlar (kategori 4):** her güncelleme yeni bir emir numarasıyla gelir (`onceki_emir_no` zinciri). Eski kotasyonun bitişi ayrı satırla yazılmaz. Defter kurulurken bir kotasyonun hangi anda geçersizleştiği zincirden türetilmelidir.
- **Kapsam dışı alanlar:** `giveup_flag` tümüyle `H`'dir. Üye/hesap kimliği yoktur.
- **Gün sonu tanımları:**
  - Toplam sözleşme, miktar ve hacim = normal işlemler + özel işlem bildirimleri.
  - AOF = özel işlem bildirimi hariç normal işlemlerin (açılış, sürekli, kapanış, kapanış fiyatından) hacim/miktar oranı, 3 haneye yuvarlanır.
  - Kapanış fiyatı = son işlem fiyatı.
  - Değişim % = (kapanış / önceki kapanış − 1) × 100, 3 hane, yarım yukarı yuvarlama.

### 3.3 Hazırlama akışı

```
CSV (DataStore, aylık)
  └─ gunici_{emir,islem}_csv2parquet.py, gunsonu_fiyat_hacim_csv2parquet.py   → aylık parquet (kayıpsız)
       └─ gunici_emir_gunluk_bol.py   → veri/gun-ici-emir/gunluk/YYYY-MM-DD/{pay,varant}-{0..7}.parquet
                                         (islem_kodu, emir_degistirilme_zamani, guncelleme_no) sıralı, kayıpsız
```

- Aylık emir dosyasındaki satır grupları 12 güne kadar yayıldığından, gün ve pay bazında okuma bölümlemeden önce pratik değildir. Bölümlenmiş dosya motorun ve tüm doğrulamaların ortak girdisidir.
- `pay` grubu: `.E`, `.F`, `.F1`, `.F2`, `.S1`, `.R`, `.BE` vb. `varant` grubu: `.V`, `.C`. Varantların satırlarının çoğu piyasa yapıcı kotasyonudur; manipülasyon tespitinin birincil kapsamı paylardır (`.E`).
- İşlem dosyası tarihe göre zaten sıralıdır (satır grupları bir güne düşer); bölümleme gerekmez.

### 3.4 Referans (sıra-gün) tablosu

Gün sonu dosyasından üretilir:

| Alan | Kaynak |
|---|---|
| Baz fiyat | `previous_last_price` (özsermaye hâllerinde teorik fiyat ayrıca gerekir; bkz. açık konular) |
| Pazar, grup | `market_segment`, `instrument_group` |
| İşlem yöntemi | `trading_method` |
| Piyasa yapıcı | `market_maker` |
| Endeks üyeliği | `bist_30_index`, `bist_100_index` |
| Brüt takas | `gross_settlement` |
| Durdurma | `suspended` |
| Özsermaye hâli | `corporate_action` |

Fiyat marjı ve fiyat adımı tablosu bu tablodan ve **tarih parametresi tablosundan** (3.6) türetilir.

### 3.5 ITCH örneğinin (2 ay) rolü

- Seçilen aylar (kullanıcı kararı, 21.10.2026; aynı gün önce onaylanan 2025-03/2025-04 seçiminin yerine): **2025-01 ve 2025-02**.
  - Bu aylar A seviyesi (dönemi kesin) SPK vakalarını kapsar: KRGYO 10.01–25.02.2025, TDGYO 24.01–25.02.2025, ALKLC 04.02–18.03.2025 (başlangıcı). Bkz. 6.4.
  - Bu aylar için DataStore gün içi emir ve gün içi işlem dosyaları da alınacaktır (kullanıcı kararı, 21.10.2026). Böylece aynı günlerde ITCH ve DataStore'dan kurulan defterler karşılaştırılabilir. Baz fiyat, pazar ve işlem yöntemi için aynı ayların gün sonu fiyat-hacim dosyası da gerekir.
- Kullanım:
  - DataStore olay dizisinden kurulan sürekli işlem defterinin ITCH `A/E/D` akışıyla eşdeğerliği (2025-01/02, aynı günler).
  - A seviyesi vaka dönemlerinde kamuya yayımlanan defter ("piyasanın gördüğü" defter) ve tespit özellikleri. Müzayede emirleri ise DataStore emir dosyasından gelir.
  - Aynı µs'deki olayların sırası (ITCH mesaj sırası ve `Ranking Sequence Number`).
  - Müzayedede yayımlanan denge bilgisi (`Z`) ile motorun teorik denge fiyatının karşılaştırılması.
- Mevcut ITCH çözümleyici ve 2018 doğrulamaları (`kurallar/07-itch.md`, `veri/itch-ornek-veri-dogrulama.md`) geçerliliğini korur. 2025 ITCH sürümü (2112) alanları örnek gelince sınanacaktır.

### 3.6 Tarih parametresi tablosu

Kural dosyaları yürürlükteki Prosedürü (rev. 21/09/2026) yazar. Tarihsel veri oynatılırken veri tarihindeki kurallar kullanılır.

Kullanıcı kararı (21.10.2026): veride gözlenen fiili eşikler esas alınır. Yürürlükteki metinle fark "Borsa İstanbul Pay Piyasası Prosedürü Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayda geçer.

Motorun okuyacağı makine okunur tablo `motor/tarih_parametreleri.csv`'dir (parametre, kapsam, başlangıç, bitiş, değer, birim, kaynak, not). Ölçüm kontrolü (`motor/parametreler.py`, 24.10.2026): veriden ölçülen bir parametre için (en az bir tarihli satırının kaynağı "veri") veri dönemindeki (01.06.2024–31.05.2025) bir günü kapsayan ölçüm satırı yoksa motor `OlcumEksik` hatasıyla durur; sessizce yürürlükteki metin değerine (ör. marj %20, devre kesici iki yönde) düşmez. Yeni bir ay eklenirken parametreleri ölçülmemiş günler böylece ilk çalıştırmada ortaya çıkar. Aşağıdaki tablo özetidir. Mart 2025 için veriden belirlenen ya da Ek-21'den okunan değerler:

| Parametre | Mart 2025 | Yürürlükteki metin | Kanıt |
|---|---|---|---|
| Pay fiyat marjı (tüm pazarlar) | ±%10 | Tablo-4: Yıldız %20, Ana %15, Alt/YİP/PÖİP %10 | Veri: 495 tavan / 786 taban isabeti, içe yuvarlanmış sınırlara tam eşit |
| Fiyat adımı | Tablo-7 / Tablo-8 (06.11.2023 sonrası) | Aynı | Veri: 797.067.974 fiyatlı emir satırında adım dışı 0 |
| Pay bazında DK yönü ve oranı | Yalnız düşüş, son müzayede fiyatına göre −%5 (Yıldız, Ana, Alt aynı) | İki yönlü; %10 / %7,5 / %5 (Tablo-4) | Veri: 1.184 olayın tamamı düşüş, en büyük sapma −%5,00 |
| Pay bazında DK süreleri | 15 dk emir toplama + 2 dk eşleştirme bölümü; eşleştirme bölümün ilk 30 sn'sinde rastlantısal; T ≥ 17:40 ise kapanışa aktarılır | 10 dk (+ uzatma 17:45–18:00) | Veri; Ek-21 eski metni (Yıldız 5, Ana/Alt 15 dk) de uymaz. Kullanıcı kararı: sabit emir toplama + tarihe bağlı rastlantısal eşleştirme penceresi (Mart 2025: 30 sn; 2018: 0 sn) |
| EBDKS eşikleri ve durdurma | %5 ve %7 (iki eşik); `.E` vb. 20 dk, `.V/.C/.F/.R` 30 dk | %6 tek eşik; 10 dk / 20 dk | Ek-21 Rev. 51 eski metni; veri (19 ve 21 Mart'ta ikişer EBDKS) |
| Varant/sertifika akışı | `P_SALTKOTASYON` 10:00:10'da başlar (07.03.2025 öncesi 10:00:00), sürekli işlem 10:02 | Ek-10 `P_SI_KOT` | Ek-21 (Duyuru 2025/33431); veri |
| Açığa satış | 03–21.03.2025 yalnız 50 payda (BIST 50); 24.03.2025'ten itibaren yok | SPK kararları | Veri (gün sonu açığa satış alanları ve emir türü 2) `DURUM.md` notuyla birebir uyumlu |
| Tek fiyat Adım 4 referansı | Baz fiyat (önceki kapanış) | Yazılı değil (ARF / Referans Fiyat) | Veri: 146 vakanın 144'ü |
| Kapanış müzayedesi fiyat sınırı | Son işlem fiyatı ±%3 (içe yuvarlanmış) ∩ günlük sınır | Madde 72 | Veri |
| Tek fiyatta karışık yön | Referansa (baz) / son işlem fiyatına en yakın aday; eşitlikte orta nokta; uymayan `yon_karisik_istisna = 1` | Yazılı değil | Kullanıcı kararı 21.10.2026; Mart 2025'te 4 vakanın 2'si kurala uyar, 2'si istisna |

## 4. Eşleştirme motoru

### 4.1 Çalışma modları

1. **Doğrulama (tekrar oynatma):** Gerçek emir niyetleri motora verilir. Motorun ürettiği işlemler ve emir durumları gerçek `PP_GUNICIISLEM` / `PP_GUNICIEMIR` ile karşılaştırılır. Ölçütler:
   - işlem eşleşme oranı (fiyat, miktar, iki tarafın emir numarası),
   - müzayede fiyatı ve miktarı eşleşme oranı,
   - gün sonu bülten alanlarının yeniden üretimi.
2. **Enjeksiyon:** Gerçek niyetlere sentetik aktörün niyetleri eklenir. Gerçek akış dışsal (tepkisiz) kabul edilir: gerçek katılımcılar enjeksiyona tepki vermez. Bu, yöntemin bilinen sınırıdır ve raporda belirtilir.

### 4.2 Girdi: emir niyetleri

Her emrin satır dizisinden yalnız kullanıcı eylemleri alınır: yeni emir (sebep 6), değişiklik (5; fiyat ve/veya miktar) ve iptal (1). Diğer satırlar (işlem 3, dönüşüm 8, sistem iptalleri 9/34/116/117, yenileme 13, süre dolumu 19, pasifleştirme 4) motorun üretmesi beklenen çıktılardır ve karşılaştırmada kullanılır.

İki özel durum:
- **Kotasyonlar (kategori 4):** her güncelleme yeni kimlikle gelir; motor girdisinde bir kotasyon, aynı zincirdeki önceki kotasyonun yerini alan değişiklik olarak işlenir. Müzayedeye katılımları veriden ayırt edilemedi; bu yüzden ilk sürümde müzayede hesabına alınmaz (kapanışta en iyi uyum bu varsayımla elde edildi).
- **Kısmi görünme koşullu emirler:** görünen kısım büyüklüğü veride yoktur. Motor, sebep 13 satırlarından gözlenen yenileme anlarını kullanır ya da görünen kısmı ilk yenilemedeki işlem miktarından tahmin eder.

### 4.3 Bileşenler ve kural dosyaları

| Bileşen | Kural dosyası | Veriyle doğrulanan davranış (Mart 2025) |
|---|---|---|
| Seans/aşama durum makinesi | `01-seanslar.md`, Ek-10/11 | Bölüm adları ve saatler; müzayede başlangıcı aşama başına ortak rastlantısal saniye |
| Emir doğrulama | `02-fiyat.md`, `05-emirler.md` (Ek-19) | Fiyat adımı, ±%10 marj, bölüm × emir tipi izinleri, kapanış ±%3 |
| Sürekli işlem | `04-surekli-islem.md` | Fiyat-zaman önceliği; değişiklikte öncelik kaybı/korunması |
| Tek fiyat | `03-tek-fiyat.md` | Denge fiyatı algoritması müzayede defterleriyle (bkz. doğrulama raporu) |
| Devre kesiciler | `06-devre-kesici.md` | Pay bazında DK ve EBDKS akışı (eski kurallar, tarih parametresi) |
| Gün sonu | `02-fiyat.md`, `03-tek-fiyat.md` | Kapanış fiyatı, AOF, bülten alanları |

- Tek fiyat algoritmasının başvuru uygulaması `veri/araclar/tek_fiyat_algoritma.py`'dir (Ek-16 örneklerinin tamamını geçer). Motor bu işlevi kullanır.
- Seans takvimi:
  - Tekrar oynatmada her sıranın bölüm geçişleri ve müzayede eşleşme anları veriden alınır (rastlantısal saniye taklit edilmez).
  - Simülasyonda Ek-10 çizelgesi ve rastlantısal başlangıç kullanılır.
- EBDKS piyasa geneli bir olaydır; tekrar oynatmada veriden okunan tetikleme anı motor dışından verilir.

### 4.4 Performans

Günde yaklaşık 50–80 milyon emir olayı vardır (payların payı yaklaşık %58). Sıralar birbirinden bağımsızdır; EBDKS dışarıdan verildiği için motor sıra bazında paralel çalışır. Önerilen yol: önce Python başvuru uygulaması (doğruluk), sonra çekirdek döngünün derlenmiş bir uygulaması (numba, Rust veya C++). Karar ölçüm sonrasına bırakılmıştır.

### 4.5 İlk sürüm (22.10.2026)

Kod `motor/`, testler `motor/testler/` (23 test).

| Dosya | İçerik |
|---|---|
| `emir.py` | Emir, işlem ve girdi olayları (yeni emir, değişiklik, iptal); fiyat milli-TL; bölümler arası ortak öncelik sayacı |
| `defter.py` | Fiyat seviyeleri ve seviye içi zaman önceliği |
| `surekli_islem.py` | Limit, piyasa, piyasadan limite, KİE; öncelik kaybı/korunması; kısmi görünme; pay bazında devre kesici eşiği; sabit fiyat modu (kapanış fiyatından işlemler) |
| `tek_fiyat.py` | Emir toplama defteri, denge fiyatı (`tek_fiyat_algoritma.denge`), işlem dağıtımı, dengeleyici emirler, kalanların bir sonraki bölüme aktarımı |
| `gun.py` | Bir sıra-günün bölüm akışı: emir toplama (EBDKS durdurması dahil), eşleştirme, sürekli işlem, kapanış fiyatından işlemler; enjeksiyon |
| `dogrulama.py` | Sentetik emir doğrulama: Ek-19 izinleri, fiyat adımı, marj, kapanış ±%3, kapanış fiyatından işlemlerde kapanış fiyatı, açığa satış, emir bilgisi değişikliği reddi |
| `parametreler.py` | `tarih_parametreleri.csv` okuyucu (tarih ve pazara göre en özel satır) |
| `veri.py` | Günlük emir dosyasından girdi olayları, başlangıç defteri, kısmi görünme tepe tahmini; gerçek işlemler; gün sonu bilgisi |
| `senaryolar.py` | Sentetik manipülasyon senaryoları (5. bölüm): kapanışı etkileme, yanıltıcı emir, fiyat yükseltme, karşılıklı işlem |
| `tekrar_oynat.py` | Doğrulama modu: bir sıra-gün, bölüm bölüm ve bütün gün karşılaştırma |
| `toplu_oynat.py` | Bir günün bütün pay sıraları (`.E`) |
| `enjeksiyon.py` | Enjeksiyon modu: taban çizgisi ve enjeksiyonlu oynatma, fark raporu |

Akış (tekrar oynatma, `gun.py`):
1. Bölüm geçişleri ve müzayede eşleşme anları veriden alınır.
2. Emir toplama bölümlerinde (açılış, kapanış, devre kesici, EBDKS tek fiyat, gün içi tek fiyat) ve EBDKS durdurmasında emirler toplanır, eşleştirme yapılmaz.
3. Eşleştirmede denge fiyatı baz fiyat, ±marj (tarih parametresi), kapanışta ayrıca son işlem ±%3 ve Adım 4 referansıyla hesaplanır; işlemler dağıtılır, kalanlar öncelik sırasıyla sonraki bölüme geçer.
4. Sürekli işlemde pay bazında devre kesici eşiği uygulanır (son müzayede fiyatı, yoksa baz; oran ve yön tarih parametresi). Eşiğin ötesinde eşleşecek gelen emrin kalanı iptal edilir ve devre kesici tetiklenir; sonraki olaylar emir toplama olarak işlenir.
5. Kapanış fiyatından işlemler sabit fiyatla oynatılır.
6. Girdi olayları: yeni emir, değişiklik, iptal ve dışsal sistem iptalleri (116, 117).

Enjeksiyon: sentetik olaylar zamanlarına göre bölüme yerleşir, o anki bölüm ve defter durumuyla doğrulanır; reddedilenler sebebiyle kaydedilir. Gerçek akış dışsal kabul edilir.

Kapsam dışı: kotasyonlar, özel işlem bildirimi, orta nokta emirleri.

Sonuç (Mart 2025; `veri/gunici-dogrulama/2025-03/motor/`). Ölçüt: alış emri, satış emri, fiyat ve adedi birebir aynı işlem oranı; bütün gün oynatıldı.

| Sıra-gün | Müzayedeler | Sürekli işlem | Kapanış fiyatından | Bütün gün |
|---|---|---|---|---|
| THYAO.E 03.03 | 2.588 / %100 | 74.046 / %99,81 | 178 / %100 | %99,82 |
| KRGYO.E 03.03 (devre kesici) | 286 / %100 | 21.217 / %99,92 | 22 / %100 | %99,92 |
| KRGYO.E 27.03 | 47 / %100 | 7.620 / %100 | 8 / %100 | %100 |
| THYAO.E 19.03 (2 EBDKS, devre kesici) | 6.807 / %100; EBDKS 3.227 / %71,4 | 176.028 / %99,82 | 276 / %100 | %99,34 |

Hücreler: gerçek işlem sayısı / birebir aynı oran. Eşleşen sürekli işlemlerin hepsinde aktif taraf da aynıdır. 19.03 EBDKS müzayedelerinde fiyat, toplam miktar ve emir bazında gerçekleşen miktar aynıdır (3.213/3.213); farklı olan, tepe büyüklüğü bilinmeyen kısmi görünme emirlerinin karşı emir çiftleridir.

Bütün paylar (`toplu_oynat.py`; özsermaye günleri hariç): 03.03.2025'te 586 sıra, 4.915.057 işlemin %99,85'i; 19.03.2025'te (iki EBDKS, çok sayıda devre kesici) 580 sıra, 6.825.508 işlemin %99,91'i birebir. Özsermaye günlerinde gün sonu dosyasındaki baz fiyat düzeltilmemiş olduğundan motor işlem üretemez (8. bölüm).

Veriden öğrenilen ve motora işlenen davranışlar:
- **Müzayede dağıtımı:** alış ve satış tarafı ayrı ayrı öncelik sırasına dizilir (piyasa ve fiyatsız piyasadan limite emirler zaman sırasıyla, sonra limit emirler fiyat ve zaman sırasıyla); iki liste baştan yürünür (`03-tek-fiyat.md` Açık sorular).
- **Kısmi görünme:** gelen emir yenilenen kısımdan aynı eşleşmede tekrar alırsa tek işlem yazılır. Tepe büyüklüğü sebep 13 satırlarından tahmin edilir (`veri.tepe_tahmini`); sebep 13 görünen kısmı bitiren işlemde yazılır, yenilemeden (ve müzayededen sürekli işleme geçişten) sonraki ilk işlem 3 ya da 13 olabilir.
- **AFK:** AFK alanı dolu emirde fiyatı ve kalanı değişmeyen değişiklik önceliği kaybettirir (`Degistir.gorunmeyen`; `04-surekli-islem.md` Açık sorular).
- **Devre kesici:** eşik ve tetikleme davranışı (`06-devre-kesici.md` Açık sorular).

Bilinen sapmalar:
- Tek yenilemesi olan ya da yalnız müzayedede işlem gören kısmi görünme emirlerinde tepe büyüklüğü belirsizdir.
- Aynı fiyatta miktar azaltmada öncelik nadiren kaybolur (THYAO.E 03.03: 551'de 2); nedeni veriden ayırt edilemez.
- Bir sapmadan sonra defter birkaç işlem boyunca farklı kalır; oran bu zincirleme etkiyi de içerir.

Performans: Python sürümü büyük bir pay-günü 7–30 sn'de, bir günün bütün payları yaklaşık 17 dk'da oynatır.

## 5. Sentetik manipülasyon enjeksiyonu

Senaryolar VI-104.1 Tebliği bentlerine bağlanır (`veri/etiketler/kaynak-vi-104-1-piyasa-bozucu-eylemler-tebligi.md`):

| Senaryo | Bölüm | Emir deseni | Kural kısıtı (motor uygular) |
|---|---|---|---|
| Kapanış fiyatını etkileme | Kapanış emir toplama (18:01–18:05) | Denge fiyatını iten emirler | Kapanışta ±%3 sınırı; değişiklik/iptal izinleri |
| Açılış fiyatını etkileme | Açılış emir toplama (09:40–09:55) | 09:50'den önce girip iptal; denge bilgisi yanıltma | 09:50 sonrası iptal/kötüleştirme/azaltma yasak (`_EIY` bölümleri) |
| Yanıltıcı emir (spoofing/layering) | Sürekli işlem | Aynı tarafın en iyi fiyatının gerisinde katmanlar + karşı yönde agresif (ya da pasif) emir + iptal; katmanlar işlem görmez | Fiyat adımı, marj, öncelik |
| Fiyatı adım adım yükseltme (ramping) | Sürekli işlem | Ardışık küçük agresif alımlar | DK tetikleme sınırı |
| Karşılıklı/kendinle işlem | Sürekli işlem | Aynı aktörün iki tarafı | Gerçek veride aktör kimliği yoktur; yalnız sentetik aktörde etiketlenir |

Enjeksiyon kaydı her sentetik eylemi (aktör, sıra, zaman, senaryo, parametreler) tutar ve denetimli model için etiket üretir.

## 6. Manipülasyon tespiti

### 6.1 Birim ve kısıt

Veride üye/hesap kimliği olmadığından tespit birimi **pay-pencere**dir (pay-gün ve gün içi 5 dakikalık pencere). Aktör düzeyinde tespit yalnız sentetik aktör için ölçülebilir.

### 6.2 Özellik grupları

- **Emir akışı:**
  - yeni/değişiklik/iptal sayıları ve oranları, emir/işlem oranı;
  - piyasa emri, KİE, açığa satış, AFK ve kotasyon payları;
  - müzayede aşamalarındaki değişiklik ve iptal yoğunluğu;
  - açılışın 09:40–09:50 dilimindeki iptaller.
- **Defter:**
  - en iyi seviyelerde derinlik, alış/satış dengesizliği, makas (yeniden kurulan defterden);
  - müzayede denge fiyatının eşleşmeye doğru seyri.
- **İşlem:**
  - fiyat etkisi, aktif taraf dengesizliği, küçük işlem yoğunluğu;
  - kapanış seansı ve kapanış fiyatından işlemlerin payı;
  - kapanış fiyatının gün içi AOF'den sapması.
- **Referans:** pazar, endeks üyeliği, piyasa yapıcı, tedbirler (brüt takas vb.).

### 6.3 Modeller ve değerlendirme

- İktisadi kurallar: VI-104.1 bentlerine bağlı eşik kuralları.
- Temel çizgi: Z-skor (fiyat, getiri, hacim ve emir/iptal oranlarının pay bazında geçmişe göre sapması). Öneri formundaki klasik yöntem karşılaştırması bu temel çizgiyle korunur.
- Denetimsiz: pay-pencere özellikleri üzerinde aykırı değer modeli (ör. Isolation Forest; eklenebilirse).
- Denetimli: SPK etiketleri (A: dönem kesin; B: tedbir penceresi, `veri/etiketler/`) ve sentetik enjeksiyon etiketleri.
- Değerlendirme zamana göre bölünür:
  - SPK vakalarında pay-gün sıralama metrikleri;
  - sentetik enjeksiyonda kesinlik (precision), duyarlılık (recall) ve F1;
  - her model Z-skor temel çizgisiyle karşılaştırılır.

### 6.4 Veri kapsamı ve etiket örtüşmesi

Emir verisi şu an yalnız Mart 2025'tir. SPK etiketlerinden bu aya düşenler:
- ALKLC (A seviyesi, 07–18.03.2025 dönemi),
- SMRTG (B, tedbir 06.03.2025),
- HEDEF (B, tedbir 28.03.2025).

Emir verisi alınacak aylar:
- **Onaylandı (kullanıcı, 21.10.2026):** 2025-01 ve 2025-02 (emir ve işlem; ITCH örneğiyle aynı aylar; A: KRGYO, TDGYO, ALKLC), 2025-04 (A: EUREN 14–21.04; B: SEGMN, ENSRI, BAKAB, VKFYO) ve 2025-05 başı (B: OZATD, KRGYO, tedbir 02.05).
- **Kapsam genişletildi (kullanıcı, 22.10.2026):** DataStore emir, işlem ve gün sonu verisi 2024-06…2025-05 arası alınır (12 ay; gerekirse genişletilir). Aralık 12.10.2026 planından gelir (ITCH + gün sonu için seçilmişti); 2025-01/02 içindedir.
- **2025-07 ITCH için alınmaz** (emir ve işlem verisi yukarıdaki kapsamda alınır). A seviyesi vakaların bulunduğu 2025-01 ve 2025-02 ITCH örneği olarak seçildi (kullanıcı kararı, 21.10.2026; 3.5). Ay ay karşılaştırma `veri/etiketler/ay_etiket_ortusmesi.csv` dosyasındadır (betik `veri/araclar/etiket_ay_ortusmesi.py`).
  - 2025-02, üç A vakasıyla (KRGYO, TDGYO, ALKLC) en çok A vakası içeren aydır; ayrıca N = 20 varsayımıyla 3 B vakası vardır.
  - 2025-07'de A vakası yoktur. 4 B vakası vardır (IPEKE, TMSN, TUCLK, DZGYO); hepsi aynı bültende (2025-41), aynı tedbir tarihindedir (29.07).
  - 2025-01/02 için emir ve işlem dosyaları da alınacaktır (kullanıcı kararı, 21.10.2026). Gün sonu dosyası da gerekir (baz fiyat, pazar, işlem yöntemi).

İşlem verisi (Mart–Eylül 2025) daha geniş örtüşme sağlar ve işlem tabanlı özellikler için kullanılabilir.

### 6.5 Görselleştirme ve emir enjeksiyon arayüzü (zorunlu)

İlk sürüm (22.10.2026): `arayuz/uygulama.py` (Streamlit; çalıştırma `streamlit run arayuz/uygulama.py`), veri hazırlığı `arayuz/hazirla.py`. Fiyat ve dakikalık hacim iki ayrı grafikte (tek eksen); taban çizgisi ve enjeksiyonlu fiyat, sentetik aktörün işlemleri, Z-skor uyarıları ve bölüm bantları gösterilir; tablolar: sentetik işlemler, reddedilen sentetik olaylar, dakikalık seri. Kural ve model uyarıları tespit modülü tamamlandıkça eklenecektir.

Kullanıcı kararı (22.10.2026): görselleştirme zorunludur. Öneri formundan basit ve yararlı olanlar eklenir. Arayüzün içeriği:
- Pay ve gün seçimi; gerçek emir akışının motorda tekrar oynatılması.
- Fiyat ve hacim grafiği; isteğe bağlı emir defteri derinliği.
- Sentetik emir enjeksiyonu: senaryo (5. bölüm), zaman, miktar ve fiyat parametreleri. Enjekte edilen emirler grafikte işaretlenir.
- Manipülasyon uyarıları grafikte zaman ekseni üzerinde gösterilir: kural, model ve Z-skor uyarıları ayrı işaretle; SPK etiket dönemleri arka plan bandı olarak.
- Gerçek ve enjeksiyonlu akışın fiyat/işlem farkı.

### 6.6 İlk sürüm (22.10.2026)

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
  - yanıltıcı emir: 3 katman × H × %2, aynı tarafın en iyi fiyatından 4–6 adım geride (en iyi fiyat taban oynatmasının defter örneğinden), 30 sn sonra iptal; arada karşı tarafta H × %0,2 agresif emir (piyasadan limite, KİE). Katmanlardan katman toplamının %1'inden fazlası işlem görürse vaka temiz sayılmaz ve değerlendirmeye alınmaz (24.10.2026 düzeltmesi; öncesinde katmanlar son işlem fiyatına göre yerleşiyordu ve karşı emir makas genişse pasif kalıyordu);
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

*Senaryo büyüklüğüne duyarlılık ve 23.10.2026 göstergeleri.* Fiyat yükseltme için pencerede net agresif adım (`pencere.py`; ardışık işlemlerde fiyatı yukarı iten agresif alış sayısı eksi aşağı iten agresif satış sayısı; bent f) ve kapanış etkilemesi için üç pay-gün göstergesi (`kapanis_ozellikleri.py`: kapanış müzayedesi fiyatının son sürekli işlem fiyatından sapması, kapanış emir toplama alış−satış dengesizliği, son 60 sn payı; bent d) eklendi. Bütün yeni göstergelerle ve düzeltilmiş yanıltıcı emir senaryosuyla (24.10.2026), 80'er enjeksiyon; büyüklükler ×0,3, ×1, ×3 (`veri/gunici-dogrulama/2025-03/tespit/olcek_duyarlilik.csv`, `pencere/`, `pencere_olcek_0.3/`, `pencere_olcek_3/`). Hücreler: ROC-AUC / ilk 3 / kontrol ilk 3.

| Senaryo | Ölçek | Kurallar | Denetimli |
|---|---|---|---|
| Yanıltıcı emir | ×0,3 | 0,95 / %89 / %5 | 0,94 / %89 / %0 |
| Karşılıklı işlem | ×0,3 | 0,44 / %5 / %5 | 0,73 / %25 / %20 |
| Fiyat yükseltme | ×0,3 | 0,57 / %5 / %5 | 0,70 / %25 / %5 |
| Kapanış | ×0,3 | 0,64 / %5 / %5 | — |
| Yanıltıcı emir | ×1 | 0,95 / %89 / %5 | 0,95 / %95 / %0 |
| Karşılıklı işlem | ×1 | 0,48 / %5 / %5 | 0,87 / %80 / %10 |
| Fiyat yükseltme | ×1 | 0,60 / %10 / %5 | 0,71 / %25 / %10 |
| Kapanış | ×1 | 0,79 / %20 / %5 | — |
| Yanıltıcı emir | ×3 | 0,95 / %89 / %5 | 0,94 / %95 / %0 |
| Karşılıklı işlem | ×3 | 0,54 / %0 / %5 | 0,95 / %100 / %0 |
| Fiyat yükseltme | ×3 | 0,62 / %10 / %5 | 0,75 / %40 / %0 |
| Kapanış | ×3 | 0,87 / %45 / %5 | — |

Yorum:
- **Yanıltıcı emir:** kurallar ölçekten bağımsızdır (0,95 / %89 / %5; 24.10.2026 senaryo düzeltmesinden sonra, öncesi 0,89 / %79). Kısa ömürlü uzak emir payı bir oran olduğundan küçük katmanlar da iz bırakır; kural büyüklüğe değil davranış biçimine duyarlıdır.
- **Kapanış etkilemesi:** yeni göstergelerle büyüklükle ölçeklenir: ×0,3'te zayıf (0,66), ×1'de 0,80, ×3'te 0,87 ve ilk 3'te %45; yanlış alarm her ölçekte %5. Önceki sürümde (geçmiş kapanışlarla puanlama, yeni göstergeler yok) ×1'de 0,60 ve isabet %0'dı.
- **Karşılıklı işlem:** yalnız denetimli modelle ve hacim artışıyla yakalanır; büyüklüğe güçlü bağlıdır (×0,3'te %40, ×3'te %100). Aktör kimliği olmadan "aynı kişinin iki tarafı" ayırt edilemez; yanlış alarm %15–20'dir.
- **Fiyat yükseltme:** net agresif adım göstergesine rağmen her ölçekte zayıftır (kurallar 0,58–0,63, denetimli ilk 3 en çok %30). 10 agresif alışın bıraktığı iz, likit paylarda olağan fiyat hareketi içinde kalır. Bu senaryo için daha uzun pencere (15–30 dk) ya da payın likiditesine göre ölçeklenmiş gösterge gerekir.
- Denetimli modelin kapanış satırı yoktur: model yalnız sürekli işlem pencerelerinde çalışır; kapanış penceresi geçmiş kapanışlarla puanlanır.

*Pencere uzunluğu (fiyat yükseltme):* 15 dakikalık pencereyle (`PENCERE_DK=15`; `pencere_15dk/`) fiyat yükseltme iyileşmedi: kurallar ROC-AUC 0,55, denetimli 0,56 (ilk 3 %35, kontrol %15). 15 dakikalık pencerede günde ≈ 33 pencere olduğundan ilk 3 hem pozitifte hem kontrolde daha kolay tutar. Sonuç: bu büyüklükteki fiyat yükseltme (200 sn'de 10 agresif alış, toplam ≈ günlük hacmin %5'i) likit paylarda olağan fiyat yolundan ayrışan bir iz bırakmaz. Bu, göstergenin değil senaryonun özelliğidir; senaryo daha büyük ve uzun yükseltmelerle sınanmalıdır.

*SPK etiketli günlerde pencere düzeyi* (`tespit/spk_pencere.py`; 76 etiketli, 400 etiketsiz pay-gün): gün başına uyarı penceresi sayısı A'yı ayırt etmez (ROC-AUC 0,43), B'de zayıf sinyal verir (0,61; a/b uyarıları 0,57). Pencere puanı aynı günün diğer pencerelerine göre olduğundan bütün güne yayılan manipülasyon gün içinde öne çıkmaz; bu vakalarda gün düzeyi kesitsel karşılaştırma (0,90) doğru araçtır. İki düzey birbirini tamamlar.

*Defter göstergeleri:* motor sürekli işlemde defteri 10 sn'de bir örnekler (en iyi 5 seviyedeki görünen alış/satış miktarı); pencerede derinlik dengesizliği ve toplam derinlik. Bu aşamada katkı yoktur (denetimli modelde önem ≈ 0); en iyi 5 seviye 4–6 adım uzaktaki katmanları ancak kısmen kapsar.

Sonraki adımlar:
- fiyat yükseltme senaryosunun daha büyük ve uzun hâliyle sınanması (15 dk pencere ve net agresif adım bu büyüklükte yetmedi);
- defter göstergelerinin daha derin seviyelerle ve olay anında örneklenmesi;
- defter derinliği ve dengesizliği (motorla yeniden kurulan defterden);
- 12 aylık veriyle ve daha çok enjeksiyonla yeniden ölçüm; SPK etiketli pay-günlerde pencere düzeyi.

## 7. Klasör yapısı (öneri)

```
kurallar/, ekler/            Prosedür kuralları (değişmez kaynak)
veri/
  gun-ici-emir/              aylık parquet + gunluk/ (git dışı)
  gun-ici-islem/             aylık parquet (git dışı)
  gun-sonu-fiyat-hacim/      aylık parquet (git dışı)
  itch/                      ITCH örnekleri (git dışı)
  etiketler/                 SPK etiketleri
  araclar/                   hazırlama ve doğrulama betikleri
  gunici-dogrulama/YYYY-MM/  doğrulama çıktıları (özet tablolar)
motor/                       eşleştirme motoru (seans, doğrulama, sürekli işlem, tek fiyat, devre kesici, oynatıcı)
tespit/                      özellik çıkarımı, kurallar, modeller, değerlendirme
arayuz/                      görselleştirme ve emir enjeksiyon arayüzü
```

## 8. Açık konular

- Özsermaye hâllerinde (bedelsiz, temettü) baz fiyat: gün sonu dosyasındaki önceki kapanış düzeltilmemiştir. Teorik fiyat kaynağı gerekir (`02-fiyat.md` madde 20–23 [DOĞRULA]).
- Mart 2025'teki ±%10 marjın dayanağı: Tablo-4 dipnot (9) "ikinci bir duyuruya kadar geçerli" duyurulara atıf yapar. Duyuru metni elde değildir.
- Aynı µs içindeki olayların sırası: DataStore'da global sıra yoktur. Çakışmalar ITCH örneğiyle çözülebilir.
- Üye/hesap kimliğinin olmaması aktör düzeyinde tespiti engeller (6.1).
- Doğrulamalar yalnız Mart 2025 ile yapıldı; 2025-04 emir (1.026.868.890 satır), 2025-05 emir (947.232.947 satır), 2025-04…09 işlem ve 2025-04…08 gün sonu dosyaları parquet'e dönüştürüldü ama doğrulanmadı.
- Tek fiyatta karışık yönde 2 istisna vaka (ZPBDL.F, ZRE20.F; öncesinde işlem olmayan BYF açılışları) kurala uymaz; ek veriyle yeniden bakılmalı.
- 2025-01/02 emir, işlem ve gün sonu dosyalarının indirilip dönüştürülmesi bekliyor. Dikkat edilecekler `rapor.md` 2.10'dadır.
- 2024-06…2025-05 kapsamının diskte saklanma biçimi: aylık parquet ve günlük bölümleme birlikte tutulursa D: sürücüsü (440 GB) yetmez.
- Değişiklik sebebi 116 ve 117'nin anlamı ile `guncelleme_no` atlamalarının nedeni bilinmiyor.
