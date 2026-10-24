# Sistemin anlatımı (sıfırdan, ayrıntılı)

Bu belge projeyi hiç bilmeyen birinin baştan sona anlayabilmesi için yazıldı. Önce borsa kavramları, sonra veri, eşleştirme motoru, sentetik manipülasyon, tespit, sonuçlar ve sınırlar anlatılır. Her bölümde "ne yapıyoruz, neden yapıyoruz, kodda nerede" sorularının cevabı vardır. Sonda sunumda sorulabilecek sorular ve cevapları bulunur.

Belgedeki sayılar Mart 2025 verisinden ve 24.10.2026 tarihli son koşulardandır. Ayrıntılı kayıt `rapor.md`, tasarım `TASARIM.md`, güncel durum `DURUM.md` dosyasındadır.

---

## 0. Tek paragrafta proje

Borsa İstanbul'un gerçek emir kayıtlarını (Mart 2025, her emrin her olayı) alıyoruz. Bu emirleri, Borsa İstanbul Pay Piyasası Prosedürü'ndeki kurallarla yazdığımız kendi **eşleştirme motorumuza** tek tek veriyoruz. Motor işlemleri borsanın gerçekte ürettiği işlemlerle %99,85 birebir aynı üretiyor. Böylece elimizde gerçek piyasanın "laboratuvar kopyası" oluyor. Bu kopyanın içine kendi uydurduğumuz bir **sentetik manipülatörün** emirlerini ekliyoruz: kapanış fiyatını itmek, sahte emirle baskı yapmak, fiyatı adım adım yükseltmek, kendi kendine işlem yapmak. Ardından **tespit yöntemleri** (iktisadi kurallar, Z-skor, Isolation Forest, denetimli makine öğrenmesi) bu manipülasyonu yakalayabiliyor mu diye ölçüyoruz. Ayrıca SPK bültenlerinden çıkardığımız gerçek manipülasyon vakalarıyla da ölçüyoruz.

Neden böyle: gerçek veride "bu emir manipülasyondu" etiketi yoktur. Üye ve hesap kimliği de yoktur. Etiketi biz üretiriz. Manipülasyonun nerede, ne zaman ve ne büyüklükte olduğunu bildiğimiz için tespit yöntemini dürüstçe ölçebiliriz.

---

## 1. Borsa kavramları (en baştan)

### 1.1 Emir, işlem, emir defteri

- **Pay (hisse):** bir şirketin ortaklık payı. Borsada her pay bir **işlem sırası**dır, ör. `THYAO.E`. `.E` pay sırası demektir.
- **Lot:** işlem birimi. Paylarda 1 lot = 1 pay.
- **Emir:** "şu paydan şu fiyattan şu kadar almak/satmak istiyorum" talimatı. Alış ya da satış yönlüdür.
- **İşlem:** bir alış emriyle bir satış emrinin eşleşmesi. İşlemin bir fiyatı ve bir miktarı (adedi) vardır.
- **Emir defteri:** henüz işlem görmemiş, bekleyen emirlerin listesi. İki tarafı vardır:
  - alış tarafı: en yüksek fiyattan aşağı doğru sıralanır;
  - satış tarafı: en düşük fiyattan yukarı doğru sıralanır.
- **En iyi alış / en iyi satış:** alış tarafının en yüksek fiyatı ve satış tarafının en düşük fiyatı.
- **Makas (spread):** en iyi satış − en iyi alış.

Örnek defter (bu örnek Prosedür Ek-18'den, birim testlerimizde de var):

| Alış miktarı | Alış fiyatı | Satış fiyatı | Satış miktarı |
|---|---|---|---|
| 100 | 10,50 | 11,00 | 80 |
| 90 | 10,45 | 11,05 | 90 |
| 80 | 10,40 | 11,10 | 100 |

En iyi alış 10,50, en iyi satış 11,00, makas 0,50 TL.

### 1.2 Fiyat adımı, baz fiyat, taban / tavan

- **Fiyat adımı:** fiyat her değeri alamaz. 10 TL civarında bir pay 10,00 / 10,01 / 10,02 olabilir, 10,005 olamaz. Adım fiyat bandına göre değişir (Prosedür Tablo-7): 20 TL'ye kadar 0,01; 20–50 TL 0,02; 50–100 TL 0,05; 100–250 TL 0,10; 250–500 TL 0,25; 500–1000 TL 0,50; 1000–2500 TL 1; üstü 2,50.
- **Baz fiyat:** günün referansı; normalde bir önceki günün kapanış fiyatı.
- **Fiyat marjı (taban / tavan):** fiyat gün içinde baz fiyattan en çok belli bir oranda uzaklaşabilir. Yürürlükteki metinde Yıldız Pazar için %20'dir, ama **Mart 2025'te veride bütün pazarlarda ±%10 uygulandığını ölçtük** (495 tavan, 786 taban isabeti; sınırlar içe yuvarlanmış: taban yukarı, tavan aşağı adıma).

### 1.3 Emir türleri

| Tür | Ne demek | Motorda |
|---|---|---|
| Limit | "En kötü şu fiyattan" (alışta en çok, satışta en az) | Uygun fiyatlı karşı seviyelerle eşleşir; kalanı deftere yazılır |
| Piyasa | Fiyat yok; karşı taraftaki bütün seviyelerden alır/satar | Kalanı iptal edilir |
| Piyasadan limite | Fiyat yok; yalnız karşı taraftaki **en iyi** seviyeden işlem görür | Kalanı o işlem fiyatından limit emre döner; karşı taraf boşsa iptal |
| KİE (kalanı iptal et) | Geçerlilik türü: hemen ne işlem görürse görsün, kalanı iptal | Deftere yazılmaz |
| GÜN | Geçerlilik türü: gün sonuna kadar defterde bekler | Varsayılan |
| Kısmi görünme (iceberg) | Miktarın yalnız bir kısmı (tepe) defterde görünür; o kısım bitince yenisi açılır | Yenilenen kısım seviyenin sonuna geçer |
| Dengeleyici | Yalnız müzayedede; fiyat hesabına girmez, açıkta kalan emirleri karşılar | Fiyat belirlendikten sonra eşleşir, kalanı iptal |

Açığa satış (elde olmayan payı satmak) Mart 2025'te 21 Mart'a kadar yalnız BIST 50 paylarında serbestti, 24 Mart'tan itibaren yasaktı. Bunu da veriden ölçtük.

### 1.4 Fiyat-zaman önceliği

Sürekli işlemde emirler iki kurala göre sıraya girer:
1. **Fiyat önceliği:** daha iyi fiyat (alışta yüksek, satışta düşük) önce işlem görür.
2. **Zaman önceliği:** aynı fiyatta önce gelen önce işlem görür.

Bir emir değiştirilirse önceliği ne olur? Bu konuda veriden şunları öğrendik (doğruluk %99,76):
- fiyat değişirse öncelik kaybolur (emir yeni gibi sona geçer);
- kalan miktar artırılırsa öncelik kaybolur;
- miktar azaltılırsa öncelik korunur;
- kısmi görünme emrinin görünen kısmı yenilenirse yenilenen kısım sona geçer;
- AFK (aracı kurum / fon kodu) alanı dolu emirde fiyatı ve miktarı değişmeyen bir değişiklik bile önceliği kaybettirir (verideki emir bilgisi değişikliği).

Önemli bir bulgu: verideki `emir_giris_zamani` alanı öncelik zamanı **değildir**; emir ömrü boyunca hiç değişmez. Öncelik zamanını olay dizisinden kendimiz türetiyoruz.

### 1.5 İki işlem yöntemi: sürekli işlem ve tek fiyat (müzayede)

- **Sürekli işlem:** emir geldiği anda karşı taraftaki uygun emirlerle eşleşir. İşlem, **defterde bekleyen (pasif) emrin fiyatından** olur. Gelen emre **aktif**, bekleyene **pasif** taraf denir.
- **Tek fiyat (müzayede):** bir süre emirler toplanır, hiç eşleşme olmaz. Sonra bütün emirler **tek bir denge fiyatından** eşleşir. Açılışta, kapanışta, devre kesiciden sonra kullanılır.

### 1.6 Bir işlem günü (tam gün, standart pay akışı)

| Saat | Bölüm (veride seans adı) | Ne olur |
|---|---|---|
| 09:40 | Açılış emir toplama (`P_ACILIS_EMIR_TPL`) | Emir toplanır, eşleşme yok |
| 09:50 | Bazı sıralarda iptal / azaltma / fiyat kötüleştirme yasak (`..._EIY`) | Son dakikada sahte emri çekip açılışı yanıltmayı önler |
| 09:55 | Eşleştirme (`P_ESLESTIRME`) | Açılış fiyatı belirlenir; an, aşamanın başında rastlantısal bir saniyedir |
| 10:00 | Sürekli işlem (`P_SUREKLI_ISLEM`) | Gün içi işlemler |
| 18:01 | Kapanış emir toplama (`P_KAPANIS_EMIR_TPL`) | Fiyatlar son işlem fiyatının ±%3'üyle sınırlı |
| 18:05 | Eşleştirme (`P_ESLESTIRME`) | Kapanış fiyatı belirlenir |
| 18:08 | Kapanış fiyatından işlemler (`P_KAPANIS_FIY_ISLEM`) | Yalnız kapanış fiyatından emir; 2 dakika |
| 18:19 | Gün sonu (`P_GUNSONU`) | Kalan emirler süre dolumuyla kapanır |

Emirler gün içinde yaşar, ertesi güne geçmez. Bu yüzden her gün bağımsız oynatılabilir. Önceki günden yalnız baz fiyat gelir.

### 1.7 Denge fiyatı nasıl bulunur (müzayede algoritması)

Prosedür 5.2.2.2.1'deki adımlar:
1. Her aday fiyatta "o fiyattan ya da daha iyisinden alıcı" (D) ve "o fiyattan ya da daha iyisinden satıcı" (S) toplanır. İşlem görebilecek miktar min(D, S)'dir. **En çok işlem miktarını** veren fiyat seçilir.
2. Birden çok fiyat eşitse, **arta kalan miktarı** (|D − S|) en az olan seçilir.
3. Hâlâ eşitse **piyasanın yönüne** bakılır: kalan miktar alış yönündeyse en yüksek, satış yönündeyse en düşük aday.
4. Hâlâ eşitse **referans fiyata** en yakın aday (Mart 2025 verisinde referansın baz fiyat olduğunu ölçtük: 146 vakanın 144'ü).
5. Referans yoksa en yüksek ve en düşük adayın ortalaması, en yakın adıma yuvarlanır.
- Adaylar: en düşük limit fiyattan bir adım aşağıdan en yüksekten bir adım yukarıya kadar bütün geçerli fiyatlar, taban/tavan içinde.
- Piyasa emirleri her fiyatta sayılır; dengeleyici emirler sayılmaz.

**Sayısal örnek** (motorun birim testindeki defter; fiyat adımı 0,01):

| Taraf | Emir | Fiyat | Miktar |
|---|---|---|---|
| Alış | B1 | piyasa | 50 |
| Alış | L1 | 10,10 | 40 |
| Alış | L2 | 10,00 | 30 |
| Alış | L3 | 10,10 | 20 |
| Satış | S1 | 10,00 | 60 |
| Satış | S2 | 9,90 | 30 |
| Satış | S3 | 10,20 | 50 |

| Aday fiyat | D (alıcı) | S (satıcı) | İşlem min(D, S) | Kalan D − S |
|---|---|---|---|---|
| 9,90 | 140 | 30 | 30 | +110 |
| 10,00 | 140 | 90 | **90** | +50 |
| 10,01 … 10,10 | 110 | 90 | **90** | **+20** |
| 10,11 | 50 | 90 | 50 | −40 |
| 10,20 | 50 | 140 | 50 | −90 |

- Adım 1: 90 lotu 11 fiyat verir (10,00–10,10).
- Adım 2: kalan miktar 10,01–10,10 arasında en azdır (20); 10 aday kalır.
- Adım 3: kalan alış yönündedir (+20), en yüksek aday seçilir: **10,10**.

Dağıtım: alış tarafı önce piyasa emirleri, sonra limitler fiyat ve zamana göre dizilir (B1, L1, L3). L2 (10,00) denge fiyatının altında kaldığı için katılmaz. Satış tarafı S2, S1 olarak dizilir; S3 (10,20) katılmaz. İki liste baştan yürünür: B1–S2 30 lot, B1–S1 20 lot, L1–S1 40 lot. Toplam 90 lot, hepsi 10,10'dan. L3 (20), L2 (30) ve S3 (50) sürekli işleme aktarılır.

Bu "iki liste baştan yürünür" dağıtım biçimi Prosedür'de açık yazmıyordu. Veriden öğrendik: THYAO 03.03.2025 açılışındaki 1.872 işlemin tamamı bu sırayla çıkıyor.

### 1.8 Devre kesiciler

- **Pay bazında devre kesici (DK):** bir payın fiyatı son müzayede fiyatından belli bir oranda uzaklaşırsa o payda sürekli işlem durur, kısa bir müzayede yapılır. Mart 2025 verisinde: **yalnız düşüşte, %5**, 15 dakika emir toplama + 2 dakika eşleştirme bölümü (eşleştirme bölümün ilk 30 saniyesinde rastlantısal bir anda). 17:40'tan sonra tetiklenirse doğrudan kapanış müzayedesine aktarılır. 1.184 olayın tamamı düşüş yönündedir. Yürürlükteki metin ise iki yönlü ve %10 / %7,5 / %5 der. Bu fark tarih parametresi olarak tutulur (bölüm 3.3).
- **Endekse bağlı devre kesici (EBDKS):** BIST 100 endeksi belli oranda düşerse bütün piyasa durur. Mart 2025'te iki eşik vardı (%5 ve %7); 19 ve 21 Mart'ta ikişer kez çalıştı. Durdurma payda 20 dakikadır, ardından tek fiyat müzayedesi yapılır.

### 1.9 Manipülasyon nedir, hangi türleri ele alıyoruz

SPK'nın VI-104.1 sayılı Piyasa Bozucu Eylemler Tebliği'nin 5. maddesi, fiyatı veya hacmi yanıltacak nitelikteki eylemleri sayar. Ele aldığımız bentler:

| Bent | Eylem | Bizdeki senaryo / gösterge |
|---|---|---|
| a | Emir verme, iptal, değiştirme (yanıltıcı) | Yanıltıcı emir (spoofing); iptal oranı |
| b | Farklı fiyat kademelerine emir | Katmanlı yanıltıcı emir (layering); fiyat kademesi sayısı, kısa ömürlü uzak emir payı |
| c | Bir dakikadan kısa sürede yön değiştiren emir | Aktör kimliği gerekir; veride ölçülemez |
| ç | Kendinden kendine / karşılıklı işlem | Karşılıklı işlem senaryosu (yalnız sentetik aktörde etiketli) |
| d | Açılış veya kapanış fiyatını etkileme | Kapanış etkileme senaryosu; kapanış göstergeleri |
| f | Fiyat yükseltici / düşürücü işlem | Adım adım fiyat yükseltme (ramping); net agresif adım |

---

## 2. Projenin parçaları ve öneri formundan farkı

Üç parça:
1. **Veri katmanı:** DataStore verisinden pay ve gün bazında emir defterinin yeniden kurulması.
2. **Eşleştirme motoru:** BIST kurallarına uygun sürekli işlem, müzayede ve devre kesiciler. Gerçek emir akışı tekrar oynatılır; araya sentetik manipülatif emirler eklenir.
3. **Manipülasyon tespiti:** iktisadi kurallar, Z-skor temel çizgisi, denetimsiz model (Isolation Forest), denetimli model (gradyan artırmalı karar ağaçları). Değerlendirme SPK vakaları ve sentetik enjeksiyonla yapılır.

Öneri formunda ajan tabanlı yapay borsa vardı: yatırımcı ajanları, GA/PSO ile kalibrasyon, Monte Carlo bandı. 22.10.2026'da bunun yerine gerçek emir akışını kullanma kararı verildi. Gerekçe:
- Ajanlar gerçek piyasayı ancak kabaca taklit eder. Gerçek emir akışı ise piyasanın kendisidir.
- Motorun doğruluğu gerçek işlemlerle birebir ölçülebilir. Ajan simülasyonunda böyle bir ölçüt yoktur.
- Formdaki Z-skor karşılaştırması, Isolation Forest ve görselleştirme sistemde korundu.

---

## 3. Veri

### 3.1 Kaynaklar

| Kaynak | Ne içerir | Mart 2025 büyüklüğü | Rolü |
|---|---|---|---|
| `PP_GUNICIEMIR` (gün içi emir) | Her emir olayından sonra emrin tam durumu (bir satır = bir olay) | 1.128.466.831 satır | Motorun girdisi |
| `PP_GUNICIISLEM` (gün içi işlem) | Her işlemin alış ve satış tarafı, iki tarafın emir numarası, aktif/pasif bayrağı | 117.193.758 işlem (× 2 satır) | Motorun doğruluk hedefi |
| `PP_GUNSONUFIYATHACIM` (gün sonu) | Sıra-gün başına baz fiyat, kapanış, pazar, endeks üyeliği, hacimler | 192.220 satır | Referans veri ve gün sonu kontrolü |
| ITCH (kamu yayın akışı) | Piyasaya yayımlanan mesajlar | 2025-01/02 bekleniyor; 08.10.2018 örneği çözüldü | Çapraz doğrulama |
| SPK bültenleri | Manipülasyon kararları, işlem yasakları | 197 bülten (2024–2026) | Gerçek vaka etiketleri |

Hedef kapsam 01.06.2024–31.05.2025 (12 ay). Şu an doğrulanmış ve kullanılan ay Mart 2025'tir (20 işlem günü, ≈ 590 pay sırası).

### 3.2 Bir satır ne anlatır: bir emrin hayatı

Gün içi emir dosyasında bir emir birden çok satırla görünür. Her satır bir olaydan **sonraki** durumdur. `degisiklik_sebebi` alanı olayı söyler:

| Sebep | Anlamı | Kimden gelir |
|---|---|---|
| 6 | Yeni emir | Kullanıcı |
| 5 | Değişiklik (fiyat ve/veya miktar) | Kullanıcı |
| 1 | İptal | Kullanıcı |
| 3 | İşlem (emir kısmen ya da tamamen gerçekleşti) | Borsa (eşleştirme) |
| 13 | Kısmi görünme emrinin görünen kısmının yenilenmesi | Borsa |
| 8 | Sistem dönüşümü (ör. piyasadan limite → limit) | Borsa |
| 9, 34, 116, 117 | Sistem iptalleri | Borsa |
| 19 | Süre dolumu (gün sonu) | Borsa |

Örnek: bir alış emri 10:15'te 1.000 lot 50,00 TL'den girilir (sebep 6). 10:20'de 400 lotu işlem görür (sebep 3, kalan 600). 10:30'da fiyatı 50,05'e çekilir (sebep 5). 11:00'de iptal edilir (sebep 1). Dört satırdır.

**Motorun anahtar fikri:** kullanıcının yaptıkları (6, 5, 1) **girdi**dir. Borsanın yaptıkları (3, 13, 8, iptaller, süre dolumu) motorun **üretmesi gereken çıktı**dır. Motor yalnız girdileri alır, işlemleri kendisi üretir; sonra gerçek işlemlerle karşılaştırırız. Tek istisna, nedenini veriden türetemediğimiz sistem iptalleridir (116, 117): bunlar dışarıdan verilir.

### 3.3 Veride doğruladığımız özellikler (Mart 2025)

Kuralları Prosedür'den yazdık, ama veri tarihindeki uygulama yürürlükteki metinden farklı olabilir. Her kuralı veriyle sınadık (`veri/gunici-veri-dogrulama.md`, 13 bölüm). Öne çıkanlar:
- Fiyat adımı: 797.067.974 fiyatlı emir satırında adım dışı fiyat 0.
- Marj ±%10 (metinde %20 / %15 / %10).
- Devre kesici yalnız düşüşte %5 (metinde iki yönlü).
- Tek fiyat algoritması 29.633 müzayedenin %99,96'sında fiyatı tutturuyor.
- Öncelik: fiyat önceliği %99,998, zaman önceliği kuralı %99,76 uyumlu.
- Zaman: emir zamanı µs çözünürlükte, İstanbul saati; işlem zamanı ms. `guncelleme_zamani` UTC'dir (3 saat geri).

Bu farklar **tarih parametresi** olarak `motor/tarih_parametreleri.csv` dosyasında tutulur: parametre, kapsam (pazar), başlangıç, bitiş, değer, kaynak. Motor bir gün için en özel satırı seçer (`motor/parametreler.py`).

**Ölçüm kontrolü (24.10.2026):** veriden ölçülen bir parametre için veri dönemindeki bir günü kapsayan ölçüm satırı yoksa motor `OlcumEksik` hatasıyla durur. Örnek: Nisan 2025'i oynatmaya kalkarsak, Nisan için marj ölçülmediği için motor durur. Sessizce metindeki %20'yi kullanıp yanlış sonuç üretmez. Parametre o pazara hiç uygulanmıyorsa (ör. YİP'te devre kesici oranı) hata vermez, parametre uygulanmaz.

### 3.4 Hazırlama: neden günlük bölümleme

Aylık emir dosyası tarih sırasında değildir; satır grupları 12 güne kadar yayılır. "THYAO'nun 19 Mart emirleri" gibi bir okuma her seferinde bütün ayı taramak demektir. Bu yüzden `veri/araclar/gunici_emir_gunluk_bol.py` dosyası ayı gün ve pay kovası bazında böler (`veri/gun-ici-emir/gunluk/YYYY-MM-DD/pay-0..7.parquet`). Her dosya (pay, zaman, güncelleme no) sırasındadır. Bölümleme kayıpsızdır: sonda satır sayısı denetlenir (Mart: 1.128.466.831 satır).

### 3.5 Kısmi görünme emirlerinde görünen kısım tahmini

Veride `gorunen_miktar` alanı her satırda emir miktarına eşit yazılmıştır, yani tepe (görünen kısım) bilinmez. Oysa motor görünen kısmı bilmek zorundadır: pasif emir yalnız görünen kısmı kadar eşleşir, sonra kısım yenilenip sıranın sonuna gider. `motor/veri.py` içindeki `tepe_tahmini` işlevi bunu emrin kendi olay dizisinden tahmin eder:
- İlk aday: ilk yenilemeye (sebep 13) kadar pasif olarak gerçekleşen miktar.
- Bu aday sebep 13 dizisini tutarlı üretemiyorsa, emrin işlem miktarlarından ve yenileme aralıklarından üretilen adaylar denenir; tutarlı olan en büyüğü seçilir (`_tepe_tutarli`).
- Tutarlılık kuralları da veriden öğrenildi. Örneğin sebep 13 görünen kısmı bitiren işlemde yazılır. Aynı gelen emir yenilenen kısımdan da alırsa veride tek işlem yazılır.

---

## 4. Eşleştirme motoru (`motor/`)

### 4.1 Dosyalar ve görevleri

| Dosya | Görev |
|---|---|
| `emir.py` | Veri tipleri: Emir, İşlem, YeniEmir, Degistir, Iptal. Fiyatlar **milli-TL tamsayı** (10,05 TL = 10050): kayan nokta yuvarlama hatası olmasın diye |
| `defter.py` | Emir defteri: her taraf için fiyat seviyeleri; seviye içinde ekleme sırası = zaman önceliği |
| `surekli_islem.py` | Sürekli işlem eşleştirmesi |
| `tek_fiyat.py` | Müzayede: emir toplama, denge fiyatı, dağıtım |
| `veri/araclar/tek_fiyat_algoritma.py` | Denge fiyatı algoritması (Prosedür Ek-16 örneklerinin hepsini geçer) |
| `gun.py` | Bir pay-günün bütün bölüm akışı; enjeksiyon |
| `veri.py` | Veriden girdi olayları, kısmi görünme tahmini, gerçek işlemler |
| `parametreler.py`, `tarih_parametreleri.csv` | Tarihe bağlı kurallar |
| `dogrulama.py` | Sentetik emirlerin kurallara uygunluk kontrolü |
| `senaryolar.py` | Sentetik manipülasyon senaryoları |
| `tekrar_oynat.py`, `toplu_oynat.py` | Doğrulama: motor işlemleri ile gerçek işlemlerin karşılaştırması |
| `enjeksiyon.py` | Enjeksiyon modu, komut satırından |

### 4.2 Emir defteri (`defter.py`)

Her taraf için `fiyat → {emir_no: Emir}` sözlüğü tutulur. Python sözlükleri ekleme sırasını korur, bu sıra zaman önceliğidir. Fiyatlar ayrıca sıralı bir listededir (`bisect`): alışta en iyi fiyat listenin sonu, satışta başıdır. Önceliğini kaybeden emir seviyesinin sonuna taşınır (`sona_al`).

### 4.3 Sürekli işlem (`surekli_islem.py`), adım adım

Yeni bir emir geldiğinde (`_yerlestir` → `_eslestir`):
1. Karşı tarafın en iyi fiyatına bakılır. Karşı taraf boşsa dur.
2. Gelen emir limitse ve karşı en iyi fiyat limitinden kötüyse dur.
3. Devre kesici eşiği varsa ve karşı fiyat eşiğin ötesindeyse dur, devre kesiciyi tetikle (aşağıda).
4. Piyasadan limite emir ilk işlemden sonra başka fiyat seviyesine geçmez.
5. O seviyenin ilk emriyle (zaman önceliği) eşleş: miktar = min(gelenin kalanı, pasifin görünen kısmı). **Fiyat pasif emrin fiyatıdır.**
6. Pasif emir bittiyse defterden çıkar. Görünen kısmı bittiyse yenile ve seviyenin sonuna al.
7. Gelen emrin kalanı varsa 1'e dön.

Sonra gelen emrin kalanına karar verilir: KİE ya da piyasa emriyse iptal edilir. Piyasadan limiteyse ilk işlem fiyatından limit emir olarak deftere yazılır. Limit GÜN emriyse kendi fiyatından deftere yazılır.

Örnek (bölüm 1.1'deki defter): 150 lotluk piyasa alış emri gelir. 11,00'daki 80 lotu alır, sonra 11,05'ten 70 lot alır. Kalan 0'dır. 11,05 seviyesinde 20 lot kalır. Aynı emir piyasadan limite olsaydı yalnız 11,00'dan 80 lot alırdı. Kalan 70 lot 11,00'dan alış emri olarak deftere yazılırdı.

**Değişiklik (`degistir`):** fiyat değişirse emir defterden çıkarılıp yeni emir gibi yeniden yerleştirilir (gerekirse hemen eşleşir). Kalan artarsa ya da görünmeyen alan değişirse sona geçer. Kalan azalırsa yerinde kalır. Değişiklik "kalan farkı" olarak verilir. Böylece motorun kalanı bir sapma yüzünden gerçekten farklıysa da değişiklik uygulanabilir.

**Devre kesici:** sürekli işlem bölümü başlarken eşik hesaplanır: son müzayede fiyatı × (1 − %5), içe yuvarlanır. Mart 2025'te yalnız alt eşik vardır. Bir gelen emir eşiğin altındaki bir seviyeyle eşleşecekse eşleşme orada durur, gelen emrin kalanı iptal edilir ve devre kesici tetiklenir. Bu davranışı veriden öğrendik (THYAO 19.03, KRGYO 03.03). Sonraki olaylar müzayede emir toplaması olarak işlenir.

### 4.4 Müzayede (`tek_fiyat.py`)

- Emir toplama sırasında eşleşme yapılmaz. Değişiklik ve iptaller yine öncelik kurallarıyla işlenir.
- Eşleştirme anında denge fiyatı hesaplanır (bölüm 1.7). Sınırlar: günlük taban/tavan; kapanış müzayedesinde ayrıca son işlem fiyatının ±%3'ü.
- Dağıtım iki listeyle yapılır (bölüm 1.7). Dengeleyici emirler önce karşı taraftaki karşılanmamış emirlerle, sonra birbirleriyle eşleşir.
- Kalanlar: piyasa emri, KİE ve dengeleyici iptal edilir. Fiyatsız piyasadan limite emir denge fiyatından limit emre döner. Diğerleri öncelik sırasıyla sürekli işlemin başlangıç defterine geçer.

### 4.5 Bir günün akışı (`gun.py`)

`Gun` sınıfı bir pay-günü baştan sona oynatır:
1. Gün sonu dosyasından fiyat adımı tablosu, pazar ve baz fiyat okunur. Tarih parametrelerinden marj, devre kesici oranı ve yönü, açığa satış kapsamı ve Adım 4 referansı alınır.
2. Payın emir satırları zamana göre dizilir ve aynı bölümdeki ardışık satırlar **koşu**lara ayrılır (`kosular`), ör. açılış toplama → eşleştirme → sürekli işlem → kapanış toplama → eşleştirme → kapanış fiyatından → gün sonu. **Bölüm geçişleri ve müzayede anları veriden alınır.** Rastlantısal eşleştirme saniyesini taklit etmeyiz, gerçekte ne olduysa onu kullanırız.
3. Her koşunun türüne göre:
   - toplama: olaylar `TekFiyat`'a verilir;
   - eşleştirme: toplanan defter eşleştirilir; işlemler bu anın zamanıyla yazılır. Kapanış müzayedesinin anı `kapanis_ani` olarak saklanır;
   - sürekli işlem: `SurekliIslem` çalışır. Defter 1 saniyede bir örneklenir: en iyi 5 seviyedeki alış ve satış miktarı, en iyi fiyatlar (`defter_ornekleri`). Bunlar hem derinlik göstergelerinde hem senaryo fiyatlarında kullanılır;
   - kapanış fiyatından işlemler: bütün işlemler kapanış fiyatından;
   - gün sonu: eşleşmemiş toplama defteri kaldıysa eşleştirilir, kalan sentetik olaylar reddedilir.
4. Sentetik olaylar zamanlarına göre ilgili koşuya yerleşir ve o anki bölüm ve defter durumuyla `Dogrulayici`dan geçer. Reddedilenler sebebiyle `reddedilen` listesine yazılır.

### 4.6 Sentetik emir doğrulama (`dogrulama.py`)

Gerçek emirleri doğrulamayız: borsa zaten kabul etmiştir. Sentetik emirleri ise borsanın yapacağı gibi kontrol ederiz:
- **Ek-19 matrisi:** her bölümde hangi emir türü girilebilir, hangi değişiklik yapılabilir (ör. EBDKS durdurmasında emir girilemez; açılışın son 5 dakikasında iptal yapılamaz).
- Fiyat adımı, taban/tavan, kapanış toplamada ±%3, kapanış fiyatından işlemlerde yalnız kapanış fiyatı.
- Açığa satış kapsamı (tarihe göre).
- Emir bilgisi (MPF-AFK-Hesap No) değişikliği reddedilir.

### 4.7 Motor ne kadar doğru

Ölçüt sıkıdır: bir işlem ancak **alış emri numarası, satış emri numarası, fiyat ve adedi** gerçek bir işlemle birebir aynıysa doğru sayılır.

| Sıra-gün | Müzayedeler | Sürekli işlem | Kapanış fiyatından | Bütün gün |
|---|---|---|---|---|
| THYAO.E 03.03 | 2.588 / %100 | 74.046 / %99,81 | 178 / %100 | %99,82 |
| KRGYO.E 03.03 (devre kesici) | 286 / %100 | 21.217 / %99,92 | 22 / %100 | %99,92 |
| THYAO.E 19.03 (2 EBDKS + devre kesici) | 6.807 / %100; EBDKS 3.227 / %71,4 | 176.028 / %99,82 | 276 / %100 | %99,34 |

Bütün paylar: 03.03.2025'te 586 sıranın 4.915.057 işleminin %99,85'i; 19.03.2025'te 580 sıranın 6.825.508 işleminin %99,91'i birebir aynıdır.

Kalan farkların nedenleri:
- Kısmi görünme emirlerinin tepe büyüklüğü bazen belirsizdir. EBDKS müzayedelerindeki %71,4'ün nedeni budur. Fiyat ve emir bazında gerçekleşen miktarlar yine aynıdır (3.213/3.213); farklı olan karşı emir eşleşmeleridir.
- Aynı µs'deki olayların sırası veride yoktur.
- Bir sapma olursa defter birkaç işlem boyunca farklı kalır (zincirleme etki).
- Özsermaye günlerinde (bedelsiz, temettü) gün sonu dosyasındaki baz fiyat düzeltilmemiştir; bu günler hariç tutulur.

---

## 5. Sentetik manipülasyon (`motor/senaryolar.py`)

### 5.1 Fikir

Aynı pay-gün iki kez oynatılır:
1. **Taban çizgisi:** yalnız gerçek emirlerle.
2. **Enjeksiyonlu:** gerçek emirler + sentetik aktörün emirleri.

Fark, manipülasyonun piyasadaki izidir. Sentetik emirlerin numarası `SENT-<senaryo>-<n>` biçimindedir, bu yüzden aktörün her işlemini biliriz.

**Temel varsayım ("gerçek akış dışsaldır"):** gerçek katılımcılar sentetik emirlere tepki vermez. Gerçekte bir yanıltıcı emir başkalarını da etkileyebilirdi, bizim oynatmamızda etkilemez. Bu yöntemin bilinen sınırıdır. Tespit için "en kötü durum"dur: aktörün etkisi yalnız kendi emirleriyle sınırlı kalır.

### 5.2 Senaryolar

Büyüklükler payın o günkü işlem miktarına (H, lot) göre ölçeklenir. Böylece büyük ve küçük paylarda manipülasyon aynı göreli büyüklüktedir.

| Senaryo | Ne yapar | Değerlendirmedeki büyüklük | Bent |
|---|---|---|---|
| Kapanış etkileme | Kapanış emir toplamanın sonunda, eşleşmeden 10 sn önce, ±%3 bandın ucundan büyük bir emir | H × %3 | d |
| Yanıltıcı emir | Bir tarafta, o tarafın en iyi fiyatının 4, 5, 6 adım gerisinde 3 büyük emir (katman); 15 sn sonra karşı tarafta küçük agresif emir; 30 sn sonra katmanların iptali | Katman H × %2, karşı emir H × %0,2 | a, b |
| Fiyat yükseltme | 20 sn arayla 10 agresif alış (piyasadan limite + KİE): her biri en iyi satışı tüketir, fiyatı yukarı iter | Her biri H × %0,5 | f |
| Karşılıklı işlem | 60 sn arayla 10 kez aynı aktörün aynı fiyattan satışı ve hemen ardından alışı | Her biri H × %0,5 | ç |

Ayrıntılar:
- **Yanıltıcı emir:** katmanlar defterin derinindedir, işlem görmesi beklenmez. Amaç karşı tarafa "büyük satıcı var" görüntüsü vermek, sonra karşı yönde küçük işlemi yapıp sahte emirleri çekmektir. En iyi fiyat, taban oynatmasının defter örneğinden alınır.
- **Temiz vaka ölçütü:** katmanlardan, katman toplamının %1'inden fazlası işlem görürse senaryo artık "yanıltıcı emir" değil "büyük agresif işlem"dir. Bu vaka değerlendirmeye alınmaz.
- **Karşılıklı işlem:** gerçek bir karşılıklı işlemde aktörün alışı kendi satışıyla eşleşmelidir. Bu yüzden emir makasın içinden girilir (en iyi alışın bir adım üstü). Satış o fiyatta tek başına en iyi satış olur, ardından gelen alış onu karşılar. Makas tek adımsa içine fiyat girilemez. O zaman aktör kendi 60 saniyelik aralığında makasın en az iki adım açıldığı ilk anı bekler. Ölçüm (20 vaka): senaryo miktarının ortalama %89'u aktörün kendi emirleri arasında işlem görüyor. Satışın yarısından azı kendi alışıyla eşleşirse vaka temiz sayılmaz.
- **Kapanış etkileme:** emir bandın ucundan girilir: alışta son işlem fiyatı + %3, satışta − %3. Kapanış müzayedesinin denge fiyatını o yöne iter.

### 5.3 Enjeksiyon nasıl çalıştırılır

- Komut satırı: `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]`. Çıktıda sentetik işlemler, reddedilen olaylar, taban ve enjeksiyonlu kapanış fiyatları ve "gerçek işlemlerin kaçı değişmedi" bilgisi yer alır.
- Arayüz: bölüm 7.

---

## 6. Tespit (`tespit/`)

### 6.1 Neyi tespit ediyoruz: birim

Veride kimin emir verdiği (üye, hesap) yoktur. Bu yüzden "şu kişi manipülasyon yaptı" diyemeyiz. Birim **pay-zaman dilimi**dir:
- **pay-gün:** "THYAO 19 Mart'ta şüpheli mi?";
- **5 dakikalık pencere:** "THYAO 19 Mart 14:05–14:10 arasında şüpheli mi?".

### 6.2 Pay-gün özellikleri (`ozellikler.py`)

Her pay-gün için 24 özellik (göstergeler) hesaplanır, her biri bir bentle ilişkilidir:

| Grup | Özellik | Ne ölçer |
|---|---|---|
| Fiyat | `getiri` | Kapanış / baz − 1 |
| Fiyat | `aralik` | (Gün içi en yüksek − en düşük) / baz |
| Fiyat | `kapanis_oncesi_getiri` | 17:45 sonrası sürekli işlemdeki getiri |
| Hacim | `hacim_tl` | İşlem hacmi (TL) |
| Kapanış | `kapanis_aof_sapma` | Kapanış fiyatının gün içi ağırlıklı ortalama fiyattan (AOF) sapması |
| Kapanış | `kapanis_seansi_payi`, `kfi_payi` | Kapanış müzayedesi ve kapanış fiyatından işlemlerin hacim payı |
| Kapanış | `kapanis_muzayede_sapma` | Kapanış müzayedesi fiyatı / son sürekli işlem fiyatı − 1 |
| Kapanış | `kapanis_toplama_dengesizlik` | Kapanış toplamadaki yeni emirlerde (alış − satış) / (alış + satış) |
| Kapanış | `kapanis_son_dakika_payi` | Kapanış toplama olaylarının son 60 sn'ye düşen payı |
| Kapanış | `kapanis_degisiklik_yogunlugu` | Kapanış toplamada değişiklik + iptal / yeni emir |
| Açılış | `acilis_sapma` | Açılış müzayedesi fiyatının bazdan sapması |
| Açılış | `acilis_iptal_orani` | 09:40–09:50 iptalleri / yeni emirler |
| Emir akışı | `iptal_orani`, `degisiklik_orani` | İptal ve değişiklik / yeni emir |
| Emir akışı | `emir_islem_orani` | Yeni emir / işlem sayısı |
| Emir akışı | `piyasa_payi`, `kie_payi`, `afk_payi` | Yeni emirler içindeki paylar |
| Emir akışı | `fiyat_kademesi` | Yeni limit emirlerdeki farklı fiyat sayısı |
| Emir akışı | `kisa_omurlu_uzak_pay` | Aynı tarafın en iyi fiyatından en az 3 adım uzakta girilip 60 sn içinde işlem görmeden iptal edilen emirlerin miktar payı (yanıltıcı emrin doğrudan izi) |
| İşlem | `aktif_dengesizlik` | Agresif alış − agresif satış miktarı / toplam |
| İşlem | `kucuk_islem_payi` | 1.000 TL altı işlemlerin payı |
| Defter | `makas` | Göreli makasın ortancası |

Referans alanlar (pazar, BIST 100 üyeliği, piyasa yapıcı, brüt takas, özsermaye) modele girmez, yalnız açıklama içindir.

`motor_ozellikleri.py` aynı tanımlarla aynı özellikleri **motor çıktısından** hesaplar. Enjeksiyonlu bir günün özellikleri ancak böyle hesaplanabilir. Kontrol: enjeksiyonsuz motor özellikleri veriden hesaplananlarla neredeyse aynıdır (fark ortancası 0).

### 6.3 Yöntemler (`yontemler.py`)

**Z-skor (temel çizgi).** Her özellik için payın kendi geçmiş günleriyle karşılaştırma yapılır:

z = (bugünkü değer − önceki günlerin ortalaması) / önceki günlerin standart sapması

En az 5 günlük geçmiş gerekir. Yalnız geçmiş kullanılır, gelecek kullanılmaz (bir testle sınanır). Pay-gün puanı, özelliklerin |z| değerlerinin en büyüğüdür. Örnek: bir payın iptal oranı her gün %20 civarındaysa (standart sapma %3) ve bugün %35 ise z = 5'tir. Bu olağan dışıdır.

**İktisadi kurallar (VI-104.1 bentleri).** Eşikler: ESIK = 3, ESIK_2 = 2 (bunlar tasarım parametresidir, Prosedür kuralı değildir).
- a: z(iptal oranı) ≥ 3 ya da z(emir/işlem oranı) ≥ 3;
- b: z(fiyat kademesi) ≥ 3 ya da z(kısa ömürlü uzak emir payı) ≥ 3;
- d: kapanış AOF'den ≥ 3 sapmış ve kapanış seansı hacim payı z ≥ 2; ya da kapanış müzayedesi sapması ≥ 3 ve kapanış toplama dengesizliği ≥ 2, ikisi aynı yönde; ya da açılış iptal oranı ≥ 3 ve açılış sapması ≥ 2;
- f: |z(getiri)| ≥ 3 ve |z(aktif dengesizlik)| ≥ 2, aynı yönde; ya da z(küçük işlem payı) ≥ 3 ve |z(getiri)| ≥ 2.

Puan: tetiklenen bent sayısıdır. Eşitlikte Z-skor puanı belirler.

**Isolation Forest (denetimsiz).** Ağaçlar veriyi rastgele özellik ve rastgele eşiklerle bölerek her noktayı yalnız bırakmaya çalışır. Olağan dışı noktalar az bölmeyle yalnız kalır, yani ağaçta sığdadır. Puan, ortalama derinliğin tersidir. Etiket gerekmez.

**Kesitsel karşılaştırma.** Pay kendi geçmişiyle değil, **aynı gün aynı pazardaki diğer paylarla** karşılaştırılır: her özellikte yüzdelik sıra. Ayrıca 5 günlük birikimli getiri ve hacim artışı eklenir. Neden gerekli: manipülasyon haftalarca sürerse payın geçmişi de "kirlenir" ve Z-skor olağan dışılığı göremez. Kesitsel karşılaştırma buna duyarlı değildir.

### 6.4 SPK etiketleri

SPK bültenlerinden (197 PDF) manipülasyon kararları çıkarıldı (`veri/araclar/spk_bulten_etiket.py`, kurallar `veri/etiketler/etiket-cikarim-kurallari.md`, elle doğrulama `dogrulama-kaydi.md`). Seviyeler:
- **A:** manipülasyon dönemi bültende gün düzeyinde yazılı. O dönemin işlem günleri pozitiftir. Mart 2025'te ALKLC (12 pay-gün).
- **B:** yalnız işlem yasağı (tedbir) tarihi biliniyor. Varsayım: manipülasyon yasaktan önceki **20 işlem günüdür**, pencere yasaktan 3 iş günü önce biter. Gerekçe: dönemi ve yasağı birlikte bilinen 4 vakanın dördünde de dönem yasaktan 3 iş günü önce bitiyor. Yasaktan önceki 2 iş günü **belirsiz**dir ve değerlendirmeye alınmaz. Mart 2025'te 8 pay, 64 pay-gün.
- Tatiller iş günü sayılmaz (`TATILLER`, 2024–2026 resmî tatilleri).
- **Etiketsiz gün negatif değildir:** SPK'nın yakalamadığı manipülasyon olabilir. Bu yüzden ölçütler alt sınır olarak okunur.

### 6.5 Değerlendirme ölçütleri (sezgisel)

- **ROC-AUC:** rastgele seçilen bir pozitifin (manipülasyonlu) rastgele seçilen bir negatiften daha yüksek puan alma olasılığı. 0,5 yazı-turadır, 1 mükemmeldir.
- **Ortalama kesinlik (AP):** pozitifler az olduğunda daha zorlayıcı bir sıralama ölçütü.
- **İlk 3 isabeti (pencere):** bir günde ≈ 100 pencere vardır. Enjekte edilen pencerelerden biri günün en yüksek puanlı 3 penceresine giriyor mu? Bu, "analist her gün her payda en şüpheli 3 pencereye bakarsa manipülasyonu görür mü" sorusudur.
- **Kontrol (yanlış alarm tabanı):** aynı pencereler **enjeksiyonsuz** oynatmada da ilk 3'e giriyor mu? Bir yöntem kontrolde de yüksekse ayırt ettiği şey manipülasyon değil, o pencerenin kendisidir.

### 6.6 5 dakikalık pencere (`pencere.py`)

Neden gerekli: 30 saniyelik bir yanıltıcı emir bütün günün toplamında kaybolur. Bunu pay-gün değerlendirmesinde gördük (bölüm 8).

Pencere özellikleri (motor çıktısından):

| Özellik | Ne ölçer |
|---|---|
| `islem_sayisi`, `hacim` | İşlem sayısı ve lot |
| `getiri` | Pencere son fiyatı / önceki pencere son fiyatı (log) |
| `aktif_dengesizlik` | Agresif alış − satış dengesizliği |
| `yeni`, `iptal`, `iptal_orani` | Emir olayları |
| `uzak_kisa_pay` | Kısa ömürlü uzak emir miktar payı |
| `fiyat_kademesi` | Farklı limit fiyat sayısı |
| `net_adim` | Ardışık sürekli işlemlerde fiyatı yukarı iten agresif alış sayısı − aşağı iten agresif satış sayısı (fiyat yükseltme izi) |
| `derinlik_dengesizlik`, `derinlik` | Defter örneklerinden en iyi 5 seviyede alış/satış dengesizliği ve toplam derinlik |

Puanlama: her özellik **aynı pay-günün diğer pencerelerine göre** sağlam z ile ölçülür: (x − ortanca) / (1,4826 × MAD). Ortalama ve standart sapma yerine ortanca ve MAD kullanılır, çünkü tek bir uç pencere ortalamayı da bozar. Kurallar:
- a/b: z(iptal oranı) ≥ 3 ya da z(kısa ömürlü uzak emir payı) ≥ 3;
- f: |z(getiri)| ≥ 3 ve |z(aktif dengesizlik)| ≥ 2 aynı yönde, ya da |z(net adım)| ≥ 3;
- d: kapanış müzayedesi penceresinde, aşağıdaki geçmiş kapanışlara göre.

**Kapanış penceresi özel durumu:** kapanış müzayedesi penceresi her gün aynı günün diğer pencerelerinden farklıdır: hacim çok yüksektir, fiyat sıçrar. Aynı günle kıyaslanırsa her gün "şüpheli" görünür. Bu yüzden kapanış penceresi **payın önceki günlerdeki kapanışlarına göre** puanlanır (`kapanis_gecmisi`): kapanışın AOF'den sapması, kapanış seansı payı, kapanış öncesi getiri, kapanış müzayedesi sapması, toplama dengesizliği, son dakika payı. Isolation Forest ve denetimli model bu pencereyi puanlamaz. Kapanış penceresi motorun kaydettiği kapanış eşleşme anından (`kapanis_ani`) bulunur.

### 6.7 Denetimli model (`denetimli.py`)

- Model: `HistGradientBoostingClassifier` (gradyan artırmalı karar ağaçları). Çok sayıda küçük karar ağacı sırayla kurulur, her yeni ağaç öncekilerin hatasını düzeltir.
- Etiket: sentetik enjeksiyon. Enjekte edilen pencereler pozitif, diğer pencereler negatiftir. Girdi: pencere özellikleri ve sağlam z'leri.
- **Gruplu çapraz doğrulama (GroupKFold, 5 kat):** aynı pay-günün pencereleri hem eğitimde hem testte bulunmaz. Yoksa model "bu günü" ezberleyip şişkin sonuç verirdi.
- Testteki pay-günlerin enjeksiyonsuz pencereleri de puanlanır. Bu, yanlış alarm kontrolüdür.
- Kapanış senaryosu modelin dışındadır (kapanış penceresi geçmişe göre kuralla puanlanır).

### 6.8 SPK günlerinde pencere düzeyi (`spk_pencere.py`)

SPK etiketli pay-günler (76), aynı payların etiketsiz günleri (100) ve rastgele 300 pay-gün motorla oynatılır. Pencere uyarı sayıları gün puanına çevrilir ve etiketlerle karşılaştırılır.

---

## 7. Görselleştirme arayüzü (`arayuz/`)

Çalıştırma: `streamlit run arayuz/uygulama.py` (tarayıcıda açılır).

Ekranda:
- Sol menü: gün, pay, senaryo ve senaryo parametreleri (saat, miktar, katman sayısı, süre…), **Oynat** düğmesi.
- SPK etiketi kutusu: seçilen pay-gün SPK etiketliyse seviye ve bülten numarası görünür (ör. ALKLC 11.03: A, bülten 2025-17).
- Dört gösterge: taban kapanış, enjeksiyonlu kapanış ve farkı, sentetik işlem sayısı / adedi, 5 dk pencere kural uyarısı sayısı.
- Fiyat grafiği: gerçek akışın motorla üretilen fiyatı (mavi) ve enjeksiyonlu fiyat (turuncu, yalnız ayrıştığı yerde görünür). Sentetik aktörün işlemleri nokta, kural uyarıları üçgen ile işaretlenir. Müzayede, devre kesici ve EBDKS bölümleri gri bantlarla gösterilir.
- Dakikalık hacim grafiği (ayrı eksen).
- Sekmeler: uyarı tablosu (hangi bent, hangi z), sentetik işlemler, reddedilen sentetik olaylar (sebebiyle), dakikalık tablo.

**Sunum için önerilen gösterim:**
1. ALKLC.E 11.03.2025, senaryo yok: SPK etiketi A görünür; gerçek bir manipülasyon gününün fiyatı ve uyarıları.
2. Aynı gün ya da likit bir pay (THYAO.E, ASELS.E), "Yanıltıcı emir", 14:00:00: turuncu çizgi, sentetik işlem (karşı emir), o pencerede a/b uyarısı.
3. "Kapanış fiyatını etkileme", alış, büyük miktar: enjeksiyonlu kapanış fiyatı yukarı kayar (ör. ASELS 19.03, 200.000 lot: 112,30 → 113,00).
4. Bir sentetik emri kurala aykırı girmek (ör. kapanış bandı dışı): "Reddedilen sentetik olaylar" sekmesinde sebebi görülür. Motor kuralları uyguluyor.

---

## 8. Sonuçlar

### 8.1 SPK vakaları, pay-gün (Mart 2025)

| Puan | ROC-AUC (A) | ROC-AUC (B) | ROC-AUC (A+B) |
|---|---|---|---|
| Z-skor (kendi geçmişi) | 0,65 | 0,52 | 0,53 |
| İktisadi kurallar | 0,47 | 0,59 | 0,57 |
| Isolation Forest | 0,53 | 0,53 | 0,53 |
| Kesitsel uç sıra | 0,89 | 0,50 | 0,56 |
| Kesitsel Isolation Forest | 0,90 | 0,53 | 0,59 |

A vakasında (ALKLC) kesitsel karşılaştırma iyi çalışıyor; kendi geçmişine bakan yöntemler zayıf kalıyor, çünkü manipülasyon Şubat'ta başladı ve geçmiş de kirli. B'de sonuç rastgeleye yakın: B penceresi bir varsayım.

### 8.2 Sentetik enjeksiyon, 5 dakikalık pencere (×1, 80 enjeksiyon)

Hücreler: ROC-AUC / ilk 3 isabeti / kontrol ilk 3 (yanlış alarm).

| Senaryo | Z-skor | Kurallar | Isolation Forest | Denetimli |
|---|---|---|---|---|
| Yanıltıcı emir | 0,94 / %74 / %0 | 0,95 / %89 / %5 | 0,82 / %5 / %0 | 0,95 / %95 / %0 |
| Karşılıklı işlem | 0,48 / %0 / %0 | 0,48 / %5 / %5 | 0,49 / %5 / %5 | 0,90 / %80 / %10 |
| Fiyat yükseltme | 0,58 / %0 / %0 | 0,60 / %10 / %5 | 0,59 / %5 / %5 | 0,71 / %30 / %5 |
| Kapanış | 0,78 / %15 / %0 | 0,77 / %20 / %5 | — | — |

Büyüklüğe göre (kurallar; karşılıklı işlemde denetimli): kapanış ×0,3'te 0,58, ×1'de 0,77, ×3'te 0,87 (ilk 3 %45). Karşılıklı işlem ilk 3: ×0,3 %35, ×1 %80, ×3 %95. Yanıltıcı emir bütün ölçeklerde 0,95. Fiyat yükseltme bütün ölçeklerde ve 15 dk pencerede zayıf (0,51–0,62).

Ne anlama geliyor:
- **Yanıltıcı emir** kurallarla iyi yakalanıyor: kısa ömürlü uzak emir payı bu davranışın doğrudan izi.
- **Karşılıklı işlem** yalnız denetimli modelle, hacim artışından yakalanıyor (aktör kimliği yok).
- **Kapanış etkilemesi** büyüklükle ölçekleniyor. Günlük hacmin %3'ü sınırda, %9'u açıkça görünüyor.
- **Fiyat yükseltme** bu büyüklükte (200 sn'de 10 agresif alış) likit paylarda olağan fiyat hareketinden ayrışmıyor.

### 8.3 Sentetik enjeksiyon, pay-gün düzeyi

Aynı senaryolar bütün günün özelliklerine bakılarak ölçülünce (76 temiz vaka; 4 vaka temizlik ölçütüyle dışarıda), kurallar kapanışta 0,81, fiyat yükseltmede 0,72, karşılıklı işlemde 0,70, yanıltıcı emirde 0,68 alıyor. Ama enjeksiyonsuz kontrol kümesi de 0,64 alıyor, çünkü seçilen likit pay-günler zaten yüksek puan alıyor. Enjeksiyonun gerçek katkısı ≈ 0,09'dur. Sonuç: 30 saniyelik bir yanıltıcı emir ya da 200 saniyelik bir yükseltme günün toplamında kaybolur. Pencere düzeyine geçmenin gerekçesi budur.

### 8.4 SPK günlerinde pencere düzeyi

76 etiketli ve 400 etiketsiz pay-gün motorla oynatıldı. Gün başına kural uyarısı sayısı A'yı (ALKLC) ayırt etmiyor (ROC-AUC 0,44). B'de zayıf bir sinyal var (0,61; iptal / yanıltıcı emir uyarıları 0,57).

Neden: pencere puanı aynı günün diğer pencerelerine göredir. Bütün güne ve haftalara yayılan bir manipülasyonda gün içinde öne çıkan pencere olmaz. Bu vakalarda doğru araç gün düzeyindeki kesitsel karşılaştırmadır (0,90).

İki düzey birbirini tamamlar:
- gün düzeyi uzun süreli manipülasyonu yakalar;
- pencere düzeyi kısa epizotları yakalar.

---

## 9. Sınırlar ve dürüst notlar

- **Gerçek akış dışsaldır:** gerçek katılımcılar sentetik emirlere tepki vermez (bölüm 5.1).
- **Aktör kimliği yok:** bent c (yön değiştiren emir) ve gerçek veride bent ç (karşılıklı işlem) doğrudan ölçülemez.
- **Tek ay:** bütün sonuçlar Mart 2025'tendir. Pozitif sayısı azdır (A 12, B 64 pay-gün). 12 aylık veriyle tekrarlanmalıdır.
- **B etiketi varsayımdır** (20 işlem günü). B tedbirleri çoğunlukla "işlem bazlı" şüpheye dayanır ve pencere sınırı tahminidir.
- **Senaryo büyüklükleri varsayımdır.** Bu yüzden ×0,3, ×1 ve ×3 duyarlılık analizi yapıldı.
- **Eşikler (3 ve 2) tasarım parametresidir**, Prosedür kuralı değildir.
- **Kapsam dışı:** kotasyonlar (piyasa yapıcı), orta nokta emirleri, özel işlem bildirimleri.
- **Özsermaye günleri:** düzeltilmiş baz fiyat kaynağı yok; bu günler dışarıda.
- **Bilinmeyenler:** değişiklik sebebi 116/117'nin anlamı; `guncelleme_no` atlamaları (%0,9); aynı µs içindeki olayların sırası (ITCH ile çözülebilir).
- **Bölüm sınırları payın kendi satırlarından** okunur. Çok seyrek işlem gören bir payda sentetik emir, gerçekte başlamış bir bölüme (ör. sürekli işlem) payın ilk satırı gelene kadar yerleştirilemez. Değerlendirmede en az 300 işlemli paylar kullanıldığı için etkisizdir.

---

## 10. 24.10.2026 taramasında bulunan ve düzeltilen hatalar

Bütün kod ve belgeler satır satır okundu, şüpheli noktalar gerçek veriyle sınandı. Bulunanlar etki sırasıyla:

1. **Kapanış penceresi yanlış işaretleniyordu.** Pencere tespiti kapanış müzayedesi penceresini `P_ESLESTIRME` bölüm adından buluyordu. Açılış müzayedesi (09:55) ve bazı devre kesici müzayedeleri de bu adı taşıdığından, onlar da "kapanış penceresi" sayılıyordu. Sonuçları:
   - kapanış senaryosunda açılış penceresi de pozitif sayıldı (20 vakanın 19'unda);
   - açılış penceresine geçmiş kapanışlara göre puan ve bent d verildi;
   - denetimli model açılış penceresini hiç görmedi.

   Düzeltme: motor kapanış müzayedesinin eşleşme anını kaydeder (`Gun.kapanis_ani`). Kapanış penceresi ve motor tarafındaki kapanış göstergeleri (kapanış seansı payı, kapanış müzayedesi sapması) bu andan bulunur.
2. **Isolation Forest kapanış penceresini aynı günle kıyaslıyordu.** Bu pencere her gün uç değer olduğundan kapanış senaryosunda enjeksiyonsuz kontrol de ROC-AUC 0,83 alıyordu (enjeksiyonlu 0,84). Yani yöntem bir şey ayırt etmiyordu. Düzeltme: Isolation Forest yalnız sürekli işlem pencerelerinde çalışır. Kapanış penceresini yalnız geçmiş kapanışlara dayanan Z-skor ve kural puanlar. Kapanış senaryosunda pozitif pencere yalnız kapanış müzayedesi penceresidir; denetimli model bu senaryoyu dışarıda bırakır.
3. **Karşılıklı işlem senaryosu çoğu zaman karşılıklı işlem değildi.** Fiyat "son işlem + 1 adım" idi. O fiyatta ya da altında gerçek satıcılar varsa aktörün alışı önce onlarla eşleşiyordu. Ölçüm (20 vaka): senaryo miktarının ortalama %75'i aktörün kendi emirleri arasında işlem görüyordu; 3 vakada yalnız %10–35. Düzeltme: makasın içinden fiyat. Makas tek adımsa aktör aralıkta makasın açıldığı ilk anı bekler. Temizlik ölçütü: satışın yarısından azı kendi alışıyla eşleşirse vaka değerlendirmeye alınmaz. Sonuç: ortalama %89; 13/20 vakada %90'ın üstü (önce 5/20).
4. **Ölçüm kontrolü devre kesici ve açığa satışta yutuluyordu.** `gun.py`'deki `except KeyError` blokları `OlcumEksik`'i de yakalıyordu (`OlcumEksik`, `KeyError`'ın alt sınıfıdır). Marjı ölçülmüş ama devre kesicisi ölçülmemiş bir ayda devre kesici sessizce kapanırdı. Düzeltme: `parametreler.varsa`. Ölçüm eksikse motor durur; parametre o pazara hiç uygulanmıyorsa (YİP/PÖİP'te devre kesici) uygulanmaz. Ölçüm kontrolü artık pazara göre yapılır.
5. **Kapanış müzayedesi gün sonunda eşleştirilmeyebiliyordu.** Veride kapanış eşleştirme ve kapanış fiyatından işlemler satırı olmayan pay-günlerde (kapanışta işlem olmamışsa) toplanan defter eşleştirilmeden kalıyordu. Enjeksiyonla kapanışta işlem doğabileceği için artık gün sonu bölümünde eşleştirilir.
6. **Defter örnekleme aralığı 10 sn'den 1 sn'ye indi.** Senaryoların kullandığı en iyi fiyat 10 saniyeye kadar eskiyebiliyordu. 1 sn ile yanıltıcı emir katmanları ve karşılıklı işlem fiyatı daha doğru yerleşir. Önceki pay-gün koşusunda katmanları dolduğu için dışarıda kalan vaka (AVHOL 12.03) artık temizdir. `Defter.derinlik` bütün fiyat listesini kopyalamak yerine dilim alır.
7. **SPK etiketlerinde tatil listesi eksikti.** 2024'ün ilk yarısı (1 Ocak, Ramazan Bayramı 10–12 Nisan, 23 Nisan, 1 Mayıs), 2025 Kurban Bayramı (6 ve 9 Haziran), 2025 sonu ve 2026 tatilleri yoktu. B pencereleri iş günüyle sayıldığı için 1.588 etiket satırının 102'si değişti. Veri döneminde değişen 2 satır var (SONME 28–29.05.2025); Mart 2025'te değişen yok.
8. **Sessiz atlamalar.** Bütün sentetik olayları reddedilen vaka (ör. VAKBN 21.03 11:32: o anda EBDKS durdurması vardı, doğrulayıcı emirleri doğru şekilde reddetti) pencere değerlendirmesinde sessizce atlanıyordu. Pay-gün değerlendirmesinde ise "enjekte edilmiş" sayılıyordu, oysa manipülasyon hiç girmemişti. Artık iki değerlendirme de bu vakayı sebebiyle yazıp dışarıda bırakır.
9. **Açıklama hataları.** `yontemler.py`'deki bent b tanımında kısa ömürlü uzak emir payı eksikti. `ozellikler.py`'de karşılıklı işlem bendi "c" yazılmıştı (doğrusu ç). `TASARIM.md`'de test sayısı, arayüz açıklaması ve tamamlanmış "sonraki adımlar" eskimişti.
10. **Arayüz.** SPK etiketi kutusu eklendi (tasarımda vardı, yapılmamıştı). Uyarı fiyatı pencere uzunluğuna bağlandı (5 dk sabit yazılıydı). Enjeksiyon özetindeki "kapanış müzayedesi fiyatı" artık kapanış anından alınır; önceden kapanışta fiyat oluşmazsa açılış fiyatını gösterebiliyordu. Arayüz bütün senaryolarla uçtan uca çalıştırılarak sınandı (Streamlit AppTest).

Doğrulama: 35 birim testi geçer (yeni testler: pazara göre ölçüm kontrolü, karşılıklı işlemin makas içi fiyatı ve bekleme, kapanış penceresinin açılıştan ayrılması, Kurban Bayramı'nda B penceresi). Motorun tekrar oynatma doğruluğu değişmedi (THYAO 19.03: müzayedeler %100, sürekli işlem %99,82, bütün gün %99,34).

---

## 11. Sunumda sorulabilecek sorular

**"Motorunuzun doğru olduğunu nereden biliyorsunuz?"** Gerçek emirleri verip gerçek işlemleri birebir (iki tarafın emir numarası, fiyat, adet) karşılaştırıyoruz. Bütün paylarda %99,85 ve %99,91 aynı. Müzayedelerde %100. Ayrıca 35 birim testi var; testler Prosedür'ün kendi örneklerini (Ek-16, Ek-18) içeriyor.

**"Prosedür'de yazan kuralı mı uyguladınız, verideki kuralı mı?"** Kural dosyaları yürürlükteki Prosedür'ü yazar. Veri tarihinde farklı uygulanan kurallar (marj ±%10, devre kesici yalnız düşüşte %5, EBDKS eski eşikleri) veriden ölçüldü ve tarih parametresi olarak tutuldu. Fark "Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayıtlıdır.

**"Neden ajan tabanlı simülasyon yapmadınız?"** Gerçek emir akışı ajanlardan daha gerçekçidir ve motorun doğruluğu ölçülebilir. Ajan simülasyonunun kalibrasyonu (GA/PSO) da doğrulanamayan bir varsayımlar zinciri olurdu.

**"Sentetik manipülasyon gerçekçi mi?"** Senaryolar Tebliğ bentlerine bağlı. Motor sentetik emirleri borsa kurallarıyla doğruluyor (aykırıları reddediyor). Temizlik ölçütleri var: yanıltıcı emir katmanları işlem görmemeli, karşılıklı işlem aktörün kendi emirleri arasında olmalı. Büyüklükler varsayım olduğu için üç ölçekte sınandı. Sınır: gerçek katılımcılar tepki vermiyor.

**"Neden bazı senaryoları yakalayamıyorsunuz?"** Fiyat yükseltme (200 saniyede 10 agresif alış) likit paylarda olağan fiyat hareketinden ayrışmıyor. Bu bir bulgudur: bu büyüklükte bir yükseltme bu göstergelerle görünmez. Karşılıklı işlem aktör kimliği olmadan ancak hacim artışıyla görülebilir. Bunu yalnız denetimli model yakalıyor.

**"SPK vakalarında neden sonuç zayıf?"** Etiketler kaba: B için tarih penceresi varsayım, etiketsiz gün negatif değil, pozitif sayısı az. A vakasında (ALKLC) kesitsel karşılaştırma ROC-AUC 0,90 veriyor. Kendi geçmişine bakan yöntemler zayıf kalıyor, çünkü manipülasyon haftalarca sürünce geçmiş de kirleniyor.

**"Pencere düzeyi SPK günlerinde neden çalışmıyor?"** Pencere puanı aynı günün diğer pencerelerine göredir. Bütün güne yayılan bir manipülasyonda öne çıkan pencere olmaz. Bu yüzden iki düzey birbirini tamamlar: gün düzeyi uzun süreli manipülasyonu, pencere düzeyi kısa epizotları yakalar.

**"Veri sızıntısı (leakage) var mı?"** Z-skor yalnız geçmiş günleri kullanır (testle sınanıyor). Denetimli model pay-güne göre gruplu çapraz doğrulamayla ölçülür. Kapanış penceresi geçmiş kapanışlara göre puanlanır. Brüt takas gibi tedbir alanları modele girmez (etiketle sızıntı yaratırdı).

---

## 12. Dosya haritası ve komutlar

| Ne | Komut |
|---|---|
| Testler | `python -m pytest motor/testler tespit/testler` |
| Bir pay-günü oynat ve karşılaştır | `python -I motor/tekrar_oynat.py veri/gun-ici-emir/gunluk veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet 2025-03-19 THYAO.E --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet` |
| Bir günün bütün payları | `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv` |
| Enjeksiyon | `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]` |
| Pay-gün özellikleri | `python -I tespit/ozellikler.py GUNLUK ISLEM GUNSONU CIKTI.parquet` |
| SPK değerlendirmesi | `python -I tespit/degerlendir.py OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI` |
| Pencere değerlendirmesi | `python -I tespit/pencere_degerlendir.py OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI 80 11` (`OLCEK`, `PENCERE_DK` ortam değişkenleri) |
| Denetimli model | `python -I tespit/denetimli.py CIKTI/pencereler.parquet CIKTI` |
| Arayüz | `streamlit run arayuz/uygulama.py` |

Sözlük:

| Terim | Anlamı |
|---|---|
| AOF | Ağırlıklı ortalama fiyat (hacim / miktar) |
| Aktif / pasif | Gelen (eşleşmeyi başlatan) emir / defterde bekleyen emir |
| Baz fiyat | Günün referans fiyatı (önceki kapanış) |
| Denge fiyatı | Müzayedede bütün işlemlerin yapıldığı tek fiyat |
| EBDKS | Endekse bağlı devre kesici |
| KİE | Kalanı iptal et |
| MAD | Ortancadan mutlak sapmaların ortancası |
| Pay-gün | Bir payın bir işlem günü |
| Pencere | 5 dakikalık zaman dilimi |
| Tepe | Kısmi görünme emrinde görünen kısım |
| Z-skor | Değerin ortalamadan kaç standart sapma uzak olduğu |
