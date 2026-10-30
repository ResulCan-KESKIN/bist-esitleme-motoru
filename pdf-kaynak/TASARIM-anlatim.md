---
kisa: Sistem tasarımının sade anlatımı
alt: `TASARIM.md` bölüm bölüm, hiç bilmeyen birine anlatır gibi: veri, eşleştirme motoru, sentetik manipülasyon, tespit, sonuçlar ve açık konular
tarih: 30.10.2026
---

# Sistem tasarımının sade anlatımı

Bu belge `TASARIM.md` dosyasının (sürüm 2, son güncellemesi 26.10.2026) sade dille, ayrıntılı anlatımıdır. `TASARIM.md` kısa ve teknik yazılmıştır: her cümlesi bir karar ya da bir ölçümdür, ama nedenini ve anlamını çoğu zaman söylemez. Burada her bölüm aynı numarayla ele alınır ve şu sorular cevaplanır:

1. `TASARIM.md` burada ne diyor?
2. Bu, sade Türkçeyle ne demek?
3. Bir örnekle nasıl görünür?
4. Neden böyle karar verildi, başka türlüsü neden olmazdı?

Sarı kutular benzetme, sayılı örnek ya da "akılda kalsın" özetidir. Borsa kavramlarının, istatistiğin ve makine öğrenmesinin en baştan anlatımı `ANLATIM.pdf`'dedir; bu belgede yalnız tasarımı anlamaya yetecek kadarı var. Bütün sayılar Mart 2025 verisinden ve 24.10.2026 tarihli son koşulardandır.

## 0. Başlamadan önce

### 0.1 Bilmen gereken kelimeler

| Kelime | Sade anlamı | Benzetme |
|---|---|---|
| Pay (hisse), işlem sırası | Bir şirketin ortaklık payı. Borsada her pay bir "sıra"dır, ör. `THYAO.E` (`.E` = pay) | Pazardaki bir tezgâh |
| Lot | İşlem birimi; paylarda 1 lot = 1 pay | Tane |
| Emir | "Şu paydan şu fiyattan şu kadar almak/satmak istiyorum" talimatı | Tezgâha bırakılan sipariş notu |
| İşlem | Bir alış emriyle bir satış emrinin eşleşmesi; fiyatı ve adedi vardır | El sıkışılan alışveriş |
| Emir defteri | Henüz işlem görmemiş, bekleyen emirlerin listesi; alış ve satış tarafı vardır | Tezgâhtaki iki sipariş panosu: "almak isteyenler" ve "satmak isteyenler" |
| Eşleştirme motoru | Emirleri kurallara göre eşleştiren program | Panoyu yöneten ve el sıkıştıran hakem |
| Sürekli işlem | Emir gelir gelmez uygun karşı emirle eşleşir | Kasada sıra: gelen hemen işini görür |
| Tek fiyat (müzayede) | Bir süre emir toplanır, sonra hepsi tek bir **denge fiyatından** eşleşir | Açık artırma: teklifler toplanır, tek fiyat ilan edilir |
| Baz fiyat | Günün referansı; normalde önceki günün kapanış fiyatı | Dünkü etiket fiyatı |
| Fiyat marjı (taban/tavan) | Fiyatın gün içinde baz fiyattan en çok ne kadar uzaklaşabileceği | Hız sınırı |
| Fiyat adımı | Fiyatın alabileceği en küçük artış (ör. 0,01 TL) | Merdiven basamağı: yarım basamak olmaz |
| Devre kesici (DK) | Bir payın fiyatı kısa sürede çok düşerse o payda işlemi kısa süre durdurup müzayede yapma | Sigorta atması |
| EBDKS | Endekse bağlı devre kesici: BIST 100 çok düşerse bütün piyasanın durması | Bütün binanın sigortası |
| AOF | Ağırlıklı ortalama fiyat = toplam tutar / toplam adet | Günün ortalama satış fiyatı |
| Piyasa yapıcı, kotasyon | Sürekli alış ve satış fiyatı vermekle yükümlü kurum ve verdiği fiyat çifti | Döviz bürosunun "alış/satış" tabelası |
| Manipülasyon | Fiyatı ya da hacmi yanıltıcı biçimde etkileme | Sahte kalabalıkla müşteri çekmek |
| SPK | Sermaye Piyasası Kurulu; manipülasyon kararlarını haftalık bültenlerde yayımlar | Hakem heyeti |
| DataStore | Borsa İstanbul'un tarihsel veri satış hizmeti | Arşiv |
| ITCH | Borsa İstanbul'un herkese yayımladığı canlı piyasa veri akışı | Maçın televizyon yayını |
| Parquet | Büyük tabloları sıkıştırılmış ve hızlı okunur biçimde saklayan dosya türü | Vakumlu paket |

### 0.2 Bir işlem günü

| Saat | Bölüm | Ne olur |
|---|---|---|
| 09:40–09:55 | Açılış emir toplama | Emirler toplanır, işlem yok. 09:50'den sonra bazı değişiklikler yasaktır |
| 09:55 | Açılış eşleştirmesi | Açılış fiyatı tek fiyatla belirlenir |
| 10:00–18:00 | Sürekli işlem | Gün içi işlemler |
| 18:01–18:05 | Kapanış emir toplama | Fiyatlar son işlem fiyatının ±%3'üyle sınırlı |
| 18:05 | Kapanış eşleştirmesi | Kapanış fiyatı tek fiyatla belirlenir |
| 18:08–18:10 | Kapanış fiyatından işlemler | Yalnız kapanış fiyatından emir girilir |
| 18:19 | Gün sonu | Kalan emirler süresi dolarak kapanır |

> **Akılda kalsın:** Günde iki "açık artırma" (açılış ve kapanış) ve arada uzun bir "kasada sıra" (sürekli işlem) vardır. Devre kesici atarsa gün ortasında da kısa bir açık artırma yapılır.

### 0.3 Tek sayfada tasarım

```
GERÇEK VERİ (DataStore, Mart 2025)
  emir olayları ─┐                gerçek işlemler ─────────────┐
                 ▼                                              │
         EŞLEŞTİRME MOTORU  ──►  motorun ürettiği işlemler ──►  karşılaştır: %99,85 aynı
                 ▲
                 │  + sentetik manipülatörün emirleri (senaryolar)
                 ▼
         ENJEKSİYONLU OYNATMA ──► göstergeler ──► puanlar (kurallar, Z-skor, Isolation Forest, model)
                                                     │
                                                     ▼
                             "Manipülasyonu koyduğumuz yer en yüksek puanı aldı mı?"
                             "SPK'nın manipülasyon dediği günler yüksek puan aldı mı?"
                                                     │
                                                     ▼
                             ARAYÜZ: fiyat grafiği, sentetik işlemler, uyarılar
```

Beş cümlede sistem:
1. Borsa İstanbul'un gerçek emir kayıtlarını (her emrin her hareketi) alıyoruz.
2. Bu emirleri, Prosedür kurallarıyla yazdığımız kendi eşleştirme motorumuza tek tek veriyoruz; motor borsanın gerçekte ürettiği işlemleri neredeyse birebir üretiyor.
3. Böylece elimizde gerçek piyasanın bir "laboratuvar kopyası" oluyor; bu kopyaya kendi uydurduğumuz bir manipülatörün emirlerini ekliyoruz.
4. Tespit yöntemlerinin bu manipülasyonu bulup bulamadığını ölçüyoruz, çünkü nereye ne koyduğumuzu biz biliyoruz.
5. Ayrıca SPK bültenlerinden çıkardığımız gerçek manipülasyon vakalarıyla da ölçüyoruz.

## 1. Amaç: ne yapıyoruz?

**`TASARIM.md` ne diyor?** Proje üç parçadır: veri katmanı, eşleştirme motoru, manipülasyon tespiti. Öneri formundaki ajan tabanlı yapay borsa simülasyonu bu sistemde yoktur (kullanıcı kararı, 22.10.2026).

**Sade anlatım.**

1. **Veri katmanı:** Borsadan aldığımız ham kayıtlar, olduğu gibi kullanılamaz. Bunları temizleyip, her pay ve her gün için "o gün o payın emir defteri saniye saniye nasıldı" sorusunu cevaplayabilecek hâle getiriyoruz.
2. **Eşleştirme motoru:** Borsanın kendi motoru kapalıdır, dışarıdan kullanılamaz. Biz Prosedür'ü okuyup aynı kurallarla çalışan bir motor yazdık. Gerçek emirleri bu motordan geçirince gerçek işlemler çıkıyorsa, motor doğru demektir. Sonra bu motorun içine sahte (sentetik) manipülatif emirler ekliyoruz ve bunların gerçek emirlerle nasıl eşleştiğini görüyoruz.
3. **Tespit:** Üç tür yöntemle manipülasyon arıyoruz:
   - **iktisadi kurallar:** SPK tebliğindeki manipülasyon tanımlarına bağlı eşikler ("iptal oranı çok yüksekse uyar" gibi);
   - **denetimsiz model:** neyin manipülasyon olduğunu bilmeden "olağandışı" olanı bulan model;
   - **denetimli model:** örneklerden "manipülasyon böyle görünür" diye öğrenen model.

**Ajan tabanlı simülasyon neden yok?** Öneri formunda, yapay yatırımcılardan (küçük, büyük, yabancı) oluşan bir sanal borsa kurmak vardı. Bunun yerine gerçek emir akışını kullanma kararı verildi. Gerekçe basit: yapay yatırımcılar gerçek piyasayı ancak kabaca taklit eder, gerçek emir akışı ise piyasanın kendisidir. Üstelik gerçek akışla motorun doğruluğu gerçek işlemlerle birebir ölçülebilir; yapay borsada böyle bir "doğru cevap" yoktur. Formdan basit ve yararlı olanlar korundu: Z-skor karşılaştırması, Isolation Forest ve görselleştirme arayüzü. Farklar vize raporunda açıklanacak (`rapor.md` bölüm 3).

> **Benzetme:** Ajan tabanlı simülasyon, futbol maçını oyuncu taklidi yapan robotlarla oynatmaya benzer. Bizim yaptığımız ise gerçek maçın kaydını alıp, sahaya bir tek sahte oyuncu (manipülatör) eklemektir. Diğer 21 oyuncu gerçektir.

## 2. Neden veri kaynağı değişti? (ITCH → DataStore)

**`TASARIM.md` ne diyor?** Sürüm 1 tasarım ITCH verisine dayanıyordu. Sürüm 2'de ana veri DataStore gün içi verisidir; ITCH yalnız 2 aylık örnek olarak çapraz doğrulamada kullanılır.

**Sade anlatım.** Borsa İstanbul'dan iki tür kayıt alınabilir:
- **ITCH:** borsanın herkese canlı yayımladığı akış. Ekranda gördüğün her şey buradan gelir. Ama yayın olduğu için bazı şeyleri göstermez.
- **DataStore gün içi verisi:** borsanın kendi iç kaydı. Her emrin her hareketi, her işlemin iki tarafı yazılıdır.

| Konu | ITCH | DataStore | Sade anlamı |
|---|---|---|---|
| Kapsam | 2 aylık örnek | Hedef 12 ay (2024-06…2025-05) | DataStore ana veridir |
| Müzayede sırasında gelen emirler | Tek tek yayımlanmaz; yalnız "şu an denge fiyatı şu" bilgisi (`Z`) | Her emir var | Açılış ve kapanış açık artırmasını yalnız DataStore ile baştan kurabiliriz |
| İşlemin tarafları | Yalnız defterde bekleyen (pasif) emir görünür | Her işlemin alış ve satış satırı, iki emir numarası, kimin aktif olduğu | Motorun işlemini gerçek işlemle "iki taraf da aynı mı" diye karşılaştırabiliriz |
| Emir özellikleri | Kısıtlı | Fiyat türü, açığa satış, kategori (emir/kotasyon), geçerlilik, AFK, değişiklik sebebi | Kuralları daha ayrıntılı sınayabiliriz |
| Gün sonu karşılaştırması | Yok | Bülten alanları işlemlerden birebir yeniden üretilebiliyor | Verinin kendi içinde tutarlı olduğunu kanıtlarız |
| Kimlik | Yok | Yok (yalnız AFK bayrağı) | İkisinde de "bu emri kim verdi" yoktur |
| Zaman | Nanosaniye, mesajlar sıralı | Emir mikrosaniye, işlem milisaniye; aynı mikrosaniyedeki emirlerin sırası yok | ITCH'in tek üstünlüğü sıradır |

> **Benzetme:** ITCH bir maçın televizyon yayınıdır: seyirci golü görür, ama soyunma odasında konuşulanı görmez. DataStore hakemin maç raporudur: her faul, her oyuncu değişikliği, kimin kime pas verdiği yazılıdır. Açık artırma (müzayede) bu benzetmede soyunma odasıdır: ITCH orada yalnız "skor şu an 1-0 olurdu" der, kimin ne teklif verdiğini söylemez.

**Bu neden bu kadar önemli?** Sürüm 1'de büyük bir kısıt vardı: açılış ve kapanış müzayedelerinin defteri kurulamıyordu, çünkü ITCH müzayede emirlerini yayımlamaz. Motorun müzayede kısmı yalnız "çıkan fiyat tuttu mu" diye dolaylı sınanabilirdi. DataStore'la bu kısıt kalktı: motor müzayedeler dâhil uçtan uca, işlem işlem doğrulanabiliyor. Kapanış fiyatını etkileme gibi en önemli manipülasyon türlerinden biri tam da kapanış müzayedesinde olduğu için bu fark kritiktir.

**ITCH'e hâlâ neden ihtiyaç var?** İki iş için:
- DataStore'dan kurduğumuz defterin, kamunun gördüğü defterle aynı olduğunu sınamak;
- aynı mikrosaniyede olan emirlerin sırasını öğrenmek (DataStore'da bu sıra yok).

## 3. Veri katmanı

### 3.1 Elimizdeki dosyalar

| Kaynak | Mart 2025'te satır | Bir satır nedir | Ne işe yarar |
|---|---|---|---|
| `PP_GUNICIEMIR` (gün içi emir) | 1.128.466.831 | Bir olaydan sonra bir emrin tam durumu | Motorun girdisi: kim ne zaman hangi emri verdi, değiştirdi, iptal etti |
| `PP_GUNICIISLEM` (gün içi işlem) | 234.387.516 | Bir işlemin bir tarafı (117.193.758 işlem × 2 taraf) | Motorun "doğru cevap anahtarı" |
| `PP_GUNSONUFIYATHACIM` (gün sonu) | 192.220 | Bir sıranın bir günü | Baz fiyat, pazar, işlem yöntemi, endeks üyeliği, piyasa yapıcı; gün sonu kontrolü |
| ITCH (2 ay) | — | Kamu yayını mesajı | Çapraz doğrulama |
| SPK bültenleri | 340 kod satırı | Bir vaka | Gerçek manipülasyon etiketleri |

> **Örnek:** 1,1 milyar satır ne demek? Saniyede bir satır okusan 35 yılda bitirirsin. Mart 2025'te 20 işlem günü var; günde ortalama 56 milyon emir olayı. Bu yüzden veriyi önce düzenlemek (bölüm 3.3) ve motoru hızlı yazmak gerekir.

Alan adları (`emir_no`, `islem_numarasi` gibi) dönüştürme betiklerindeki ASCII adlardır; alanların resmî tanımı `veri/datastore-dosya-formatlari.md` dosyasındadır.

### 3.2 Veride doğruladığımız özellikler

Bu bölüm, "veri ne diyor" sorusunun cevabıdır. Hepsi Mart 2025 verisinde sayılarak doğrulandı; ayrıntı `veri/gunici-veri-dogrulama.md`'de.

#### Her gün bağımsızdır

Verideki emirlerin geçerlilik türü yalnız iki çeşittir: `DAY` (gün sonuna kadar geçerli) ve `IMMEDIATE` (KİE, kalanı hemen iptal). Yani hiçbir emir ertesi güne geçmez. Gün sonunda (`P_GUNSONU`) defterde kalan bütün emirler sebep 19 (süre doldu) ile kapanır.

**Neden önemli?** Motor her günü sıfırdan, boş defterle başlatabilir. Önceki günden tek taşınan bilgi baz fiyattır. Bu, 20 günü birbirinden bağımsız ve paralel oynatabilmemizi sağlar.

> **Benzetme:** Her gün tahtası silinen bir sınıf. Dünden yalnız "dünkü son not" (baz fiyat) kalır.

#### Bir satır neyi anlatır: emrin fotoğrafı

Emir dosyasındaki her satır, bir olay olduktan **sonra** emrin tam durumudur. Yani bir emrin hayatı, ardışık fotoğraflardan oluşan bir albümdür. Her fotoğrafın altında "neden çekildi" yazar (değişiklik sebebi):

| Sebep | Anlamı | Kim yaptı |
|---|---|---|
| 6 | Yeni emir | Kullanıcı |
| 5 | Değişiklik (fiyat ve/veya miktar) | Kullanıcı |
| 1 | İptal | Kullanıcı |
| 3 | İşlem gördü | Sistem |
| 8 | Piyasadan limite emrin kalanı limit emre döndü | Sistem |
| 13 | Kısmi görünme emrinin görünen kısmı bitti, yenisi açıldı | Sistem |
| 9, 34 | Müzayededen sonra kalan emrin sistemce iptali | Sistem |
| 116, 117 | Sistem iptalleri (117 EBDKS durdurmasında); anlamları referans tablosunda yok | Sistem |
| 19 | Süre doldu (gün sonu) | Sistem |
| 4 | Pasifleştirme | Sistem |

> **Örnek:** Bir emrin albümü:
> 1. 10:15:02 — sebep 6: 1.000 lot alış, 45,20 TL (yeni emir)
> 2. 10:16:40 — sebep 3: 300 lot işlem gördü, kalan 700
> 3. 10:20:05 — sebep 5: fiyat 45,30'a çıkarıldı (değişiklik)
> 4. 10:22:41 — sebep 3: 700 lot işlem gördü, kalan 0 (emir bitti)
>
> Motor bu albümden yalnız 1. ve 3. satırları (kullanıcının yaptıkları) alır; 2. ve 4. satırları kendisi üretmelidir. Üretebiliyorsa doğrudur.

İki ince nokta:
- `guncelleme_no` (fotoğrafın sıra numarası) emir içinde artar. Pay grubunda ardışık satırların %0,9'unda 1'den fazla artar; yani arada yazılmamış bir olay vardır ve türü bilinmiyor (albümden sayfa kopmuş gibi).
- İşlem taşıyan satır yalnız sebep 3 değildir. `islem_numarasi` alanı dolu olan her satır bir işlem taşır; bunlar 13, 8, 9 ve 34 de olabilir. Örneğin kısmi görünme emrinin görünen kısmını bitiren işlem sebep 13 olarak yazılır.

#### Emir ile işlem nasıl bağlanır

İki dosya iki numarayla birbirine bağlanır:
- `emir.islem_numarasi = int(islem.ortak_sozlesme_no, 16)`. İşlem dosyasındaki numara on altılık tabanda (hex) yazılmıştır; onluk tabana çevrilince emir dosyasındaki numarayı verir. (Örnek: hex `1A` = onluk 26.)
- `islem.emir_no`, işlemin o tarafındaki emrin `emir.emir_no` değeridir.

**Neden önemli?** Motorun ürettiği bir işlemi gerçek işlemle "alış emri aynı mı, satış emri aynı mı" diye karşılaştırmak için bu bağ şarttır.

#### Zaman damgaları: hangi saat, hangi incelik

| Alan | Saat dilimi | İncelik |
|---|---|---|
| `emir_giris_zamani`, `emir_degistirilme_zamani` | İstanbul | Mikrosaniye (saniyenin milyonda biri) |
| emir `guncelleme_zamani` | UTC (İstanbul − 3 saat) | Saniye |
| `islem_zamani` | İstanbul | Milisaniye (saniyenin binde biri) |
| `islem_degistirilme_zamani`, işlem `guncelleme_zamani` | UTC | — |

> **Dikkat:** Aynı dosyada iki farklı saat dilimi var. Bir alanı yanlış dilimde okursan, 10:00'daki bir emir 07:00'de girilmiş gibi görünür ve "açılıştan önce işlem" gibi saçma sonuçlar çıkar.

#### Öncelik zamanı veride yazılı değil

Sürekli işlemde aynı fiyattaki emirler "önce gelen önce işlem görür" kuralıyla sıralanır (zaman önceliği). Doğal olarak "emrin giriş zamanı öncelik zamanıdır" diye düşünürsün. **Değildir.** `emir_giris_zamani` emir ömrü boyunca hiç değişmez; fiyatı değiştirilen emirde bile aynı kalır. Oysa fiyatı değişen emir sıranın sonuna gider.

Bu yüzden öncelik zamanını olay dizisinden kendimiz türetiyoruz. Öncelik zamanı şu olaylarda, o olayın zamanına güncellenir:
- yeni emir;
- fiyat değişikliği;
- **kalan** miktarın artması (dikkat: "emir miktarı" alanı değil, kalan miktar);
- kısmi görünme emrinin görünen kısmının yenilenmesi (sebep 13).

Miktar azaltmada öncelik korunur. Bu model veriyle %99,76 uyumludur.

> **Benzetme:** Fırın kuyruğu. Siparişini küçültürsen ("6 değil 4 ekmek") yerin korunur. Siparişini büyütürsen ya da başka ekmek istersen (fiyat değişikliği) "arkaya geç" denir. Kuyruğa giriş fişindeki saat ise hiç değişmez; o fiş sıranı göstermez.

#### Kısmi görünme emirleri (buzdağı emirleri)

Kısmi görünme koşullu emirde miktarın yalnız bir kısmı (tepe) defterde görünür. O kısım işlem görüp bitince yeni bir tepe açılır ve yeni tepe o fiyat seviyesinin **sonuna** geçer. Sorun: verideki `gorunen_miktar` alanı her satırda emir miktarına eşit yazılmıştır, yani tepe büyüklüğü veriden okunamaz. Buna karşın bu emirler vardır ve sebep 13 satırlarından tanınır.

> **Benzetme:** Buzdağının suyun üstündeki kısmı. 10.000 lotluk emrin yalnız 1.000'i görünür; o 1.000 bitince suyun altından yeni 1.000 çıkar ama kuyruğun sonuna geçer. Veri bize buzdağının toplam boyunu söylüyor, suyun üstündeki kısmı söylemiyor.

#### Kotasyonlar

Piyasa yapıcıların verdiği alış-satış fiyat çiftlerine kotasyon denir (kategori 4). Her güncelleme **yeni bir emir numarasıyla** gelir; önceki kotasyon `onceki_emir_no` alanıyla zincir hâlinde bağlıdır. Eski kotasyonun bittiğini gösteren ayrı bir satır yoktur. Defter kurulurken bir kotasyonun hangi anda geçersiz olduğu bu zincirden çıkarılmalıdır.

#### Kapsam dışı alanlar

- `giveup_flag` alanı bütün satırlarda `H`'dir; bilgi taşımaz.
- **Üye ya da hesap kimliği yoktur.** Bu, bütün tespit tasarımını belirleyen en önemli kısıttır (bölüm 6.1).

#### Gün sonu tanımları

Gün sonu dosyasındaki alanların işlemlerden nasıl hesaplandığını bulduk ve birebir yeniden üretebiliyoruz:
- **Toplam sözleşme, miktar, hacim** = normal işlemler + özel işlem bildirimleri.
- **AOF** = özel işlem bildirimleri hariç normal işlemlerin (açılış, sürekli, kapanış, kapanış fiyatından) hacim / miktar oranı, 3 haneye yuvarlanır.
- **Kapanış fiyatı** = son işlem fiyatı.
- **Değişim %** = (kapanış / önceki kapanış − 1) × 100, 3 hane, yarım yukarı yuvarlama.

> **Örnek:** Bir gün yalnız iki işlem olsun: 100 lot × 10,00 TL ve 300 lot × 10,20 TL. Hacim = 1.000 + 3.060 = 4.060 TL, miktar = 400 lot, AOF = 4.060 / 400 = 10,150. Son işlem 10,20 olduğu için kapanış fiyatı 10,20'dir; önceki kapanış 10,00 ise değişim % = (10,20 / 10,00 − 1) × 100 = 2,000.

### 3.3 Hazırlama akışı: ham dosyadan günlük dosyalara

```
CSV (DataStore, aylık, zip içinde)
  └─ dönüştürme betikleri  →  aylık parquet (kayıpsız)
       └─ günlük bölümleme  →  veri/gun-ici-emir/gunluk/YYYY-MM-DD/{pay,varant}-{0..7}.parquet
                               (sıra kodu, değiştirilme zamanı, güncelleme no) sırasına dizili, kayıpsız
```

Adım adım:
1. **CSV → parquet.** DataStore aylık CSV verir (emir dosyası zip olarak ≈ 20 GB, açılmış CSV olarak ayda ≈ 209 GB). Parquet'e çevrilince 17–21 GB'a iner ve çok daha hızlı okunur. "Kayıpsız" demek: satır sayısı karşılaştırılır, tek satır bile kaybolmaz.
2. **Günlük bölümleme.** Aylık emir dosyası tarihe göre sıralı değildir: dosyanın parçaları (satır grupları) 12 güne kadar yayılır. "Şu günün şu payını oku" demek, bütün ayı taramak anlamına gelir. Bu yüzden emirler gün gün ve pay grubu gün klasörlerine ayrılır, her dosya içinde pay kodu ve zamana göre sıralanır. Bu bölümlenmiş dosyalar motorun ve bütün doğrulamaların ortak girdisidir.
3. **İşlem dosyası** zaten tarihe göre sıralıdır; bölümlemeye gerek yoktur.

**Pay grubu ve varant grubu.** `pay` grubunda `.E` (pay), `.F` / `.F1` / `.F2` (borsa yatırım fonu), `.S1` (emtia sertifikası), `.R` (rüçhan hakkı), `.BE` (birincil piyasa) gibi sıralar vardır. `varant` grubunda `.V` ve `.C` vardır; bunların satırlarının çoğu piyasa yapıcı kotasyonudur. Manipülasyon tespitinin asıl konusu paylardır (`.E`).

> **Benzetme:** Aylık dosya, bütün ayın faturalarının karışık atıldığı bir çuvaldır. Günlük bölümleme, faturaları gün gün klasörlere ve her klasörde müşteri adına göre sıraya koymaktır. Bir kere zahmetlidir; sonra her arama saniyeler sürer.

### 3.4 Referans tablosu: her sıranın her günü için "kimlik kartı"

Gün sonu dosyasından, her sıra ve her gün için şu bilgiler çıkarılır:

| Bilgi | Gün sonu alanı | Ne işe yarar |
|---|---|---|
| Baz fiyat | `previous_last_price` | Taban/tavan ve müzayede hesabının başlangıcı |
| Pazar, grup | `market_segment`, `instrument_group` | Pazara göre değişen kurallar |
| İşlem yöntemi | `trading_method` | Sürekli işlem mi, yalnız tek fiyat mı |
| Piyasa yapıcı | `market_maker` | Kotasyon olup olmayacağı |
| Endeks üyeliği | `bist_30_index`, `bist_100_index` | Açığa satış kapsamı, tespitte karşılaştırma grubu |
| Brüt takas | `gross_settlement` | SPK/Borsa tedbiri göstergesi |
| Durdurma | `suspended` | O gün işlem görüp görmediği |
| Özsermaye hâli | `corporate_action` | Bedelsiz, temettü gibi günler (baz fiyat sorunu, bölüm 8) |

Fiyat marjı ve fiyat adımı, bu tablo ile tarih parametresi tablosundan (3.6) birlikte hesaplanır.

### 3.5 ITCH örneğinin (2 ay) rolü

**Hangi aylar?** 2025-01 ve 2025-02 (kullanıcı kararı, 21.10.2026; aynı gün önce 2025-03/04 onaylanmış, sonra değiştirilmişti). Gerekçe: bu aylar, dönemi kesin bilinen (A seviyesi) SPK vakalarını kapsar:
- KRGYO: 10.01–25.02.2025,
- TDGYO: 24.01–25.02.2025,
- ALKLC: 04.02–18.03.2025 (başlangıcı).

Aynı iki ay için DataStore emir, işlem ve gün sonu dosyaları da alınacak; böylece aynı günlerde iki kaynaktan kurulan defterler karşılaştırılabilir.

**ITCH ne için kullanılacak?**
1. DataStore'dan kurulan sürekli işlem defterinin, ITCH'in "emir eklendi / işlem gördü / silindi" (`A/E/D`) akışıyla aynı olduğunu sınamak.
2. A seviyesi vaka dönemlerinde kamuya görünen defteri ("piyasanın gördüğü" defter) ve ondan tespit göstergeleri üretmek. Müzayede emirleri yine DataStore'dan gelir.
3. Aynı mikrosaniyedeki olayların sırasını öğrenmek (ITCH mesaj sırası ve `Ranking Sequence Number`).
4. Müzayede sırasında yayımlanan denge bilgisi (`Z`) ile motorun hesapladığı denge fiyatını karşılaştırmak.

Mevcut ITCH çözümleyici ve 2018 örneğiyle yapılan doğrulamalar geçerlidir; 2025 sürümünün (2112) alanları örnek gelince sınanacak.

### 3.6 Tarih parametreleri: kurallar zamanla değişir

**Sorun.** Kural dosyalarımız yürürlükteki Prosedürü yazar (rev. 21/09/2026). Ama verimiz Mart 2025'tendir. O tarihte uygulanan eşikler bugünkü metinden farklıdır. Örneğin bugünkü metin Yıldız Pazar için ±%20 marj der; Mart 2025 verisinde ise bütün pazarlarda ±%10 uygulandığını ölçtük.

**Karar (kullanıcı, 21.10.2026).** Veride gözlenen fiili eşikler esas alınır. Metinle fark, "Borsa İstanbul Pay Piyasası Prosedürü Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayda geçer.

**Nasıl tutuluyor?** `motor/tarih_parametreleri.csv` dosyasında. Her satır: parametre, kapsam (pazar vb.), başlangıç tarihi, bitiş tarihi, değer, birim, kaynak (veri mi metin mi), not. Motor bir günü oynatırken o tarihe ve o pazara uyan **en özel** satırı okur.

> **Benzetme:** Trafik kuralları kitabı 2026 baskısı, ama sen 2025'teki bir kazayı inceliyorsun. O gün o yolda hız sınırı 90 değil 70'ti. Kitaba değil, o günkü tabelaya bakmak zorundasın. Tarih parametre tablosu, "hangi gün hangi tabela vardı" listesidir.

**Ölçüm kontrolü: `OlcumEksik` sigortası (24.10.2026).** Bir parametre veriden ölçülen türdense (en az bir satırının kaynağı "veri" ise) ve veri döneminde (01.06.2024–31.05.2025) oynatılan günü kapsayan ölçüm satırı yoksa, motor `OlcumEksik` hatasıyla **durur**. Sessizce yürürlükteki metin değerine (ör. marj %20, devre kesici iki yönlü) düşmez.

Neden? Yeni bir ay eklendiğinde (ör. Haziran 2024), o ayın marjını ölçmeyi unutursan motor yanlış kuralla çalışır ve sonuçlar sessizce bozulur. Sigorta, ölçülmemiş günleri ilk çalıştırmada ortaya çıkarır.

**Mart 2025 değerleri, tek tek:**

| Parametre | Mart 2025 (veri) | Bugünkü metin | Sade açıklama |
|---|---|---|---|
| Fiyat marjı | Bütün pazarlarda ±%10 | Yıldız %20, Ana %15, diğerleri %10 | 495 tavan ve 786 taban isabeti içe yuvarlanmış ±%10 sınırına tam eşit |
| Fiyat adımı | Tablo-7 / Tablo-8 (06.11.2023'ten beri) | Aynı | 797 milyon fiyatlı emir satırında adım dışı fiyat sıfır |
| Pay bazında DK yönü ve oranı | Yalnız düşüşte, son müzayede fiyatına göre −%5 | İki yönlü, %10 / %7,5 / %5 | 1.184 olayın hepsi düşüş; en büyük sapma −%5,00 |
| Pay bazında DK süreleri | 15 dk emir toplama + 2 dk eşleştirme bölümü; eşleştirme bölümün ilk 30 sn'sinde rastlantısal bir anda; 17:40'tan sonra tetiklenirse kapanışa aktarılır | 10 dk (+ uzatma) | Kullanıcı kararı: sabit emir toplama + tarihe bağlı rastlantısal pencere (Mart 2025: 30 sn; 2018: 0 sn) |
| EBDKS | İki eşik (%5 ve %7); paylarda 20 dk, `.V/.C/.F/.R` 30 dk durdurma | Tek eşik %6; 10 / 20 dk | 19 ve 21 Mart'ta ikişer EBDKS oldu |
| Varant akışı | Kotasyon bölümü 10:00:10'da (07.03.2025 öncesi 10:00:00), sürekli işlem 10:02 | Ek-10 | Borsa duyurusu ve veri |
| Açığa satış | 03–21.03.2025 yalnız BIST 50 paylarında; 24.03.2025'ten itibaren yasak | SPK kararları | Gün sonu alanları ve emir türüyle birebir |
| Tek fiyat Adım 4 referansı | Baz fiyat (önceki kapanış) | Yazılı değil | 146 vakanın 144'ü |
| Kapanış müzayedesi fiyat sınırı | Son işlem fiyatı ±%3 (içe yuvarlanmış), günlük sınırın içinde | Madde 72 | Veri |
| Tek fiyatta karışık yön | Referansa / son işlem fiyatına en yakın aday; eşitlikte orta nokta | Yazılı değil | Kullanıcı kararı; 4 vakanın 2'si uyar, 2'si istisna (`yon_karisik_istisna = 1`) |

> **Örnek: ±%10 ve içe yuvarlama.** Baz fiyat 47,30 TL olsun.
> - Tavan: 47,30 × 1,10 = 52,03. 50 TL'nin üstünde adım 0,05'tir; 52,03 bir adım değil. Aşağı (içe) yuvarlanır: **52,00**.
> - Taban: 47,30 × 0,90 = 42,57. 20–50 TL arasında adım 0,02'dir; 42,57 bir adım değil. Yukarı (içe) yuvarlanır: **42,58**.
>
> "İçe" demek, sınırın hiçbir zaman %10'u aşmaması demektir.

> **Örnek: devre kesici.** Son müzayede (ör. açılış) fiyatı 40,00 TL olsun. Mart 2025 kuralıyla eşik %5 aşağısı, yani 38,00 TL civarıdır. Fiyat bu eşiğin ötesine gidecek bir işlem doğacaksa, gelen emrin kalanı iptal edilir, sürekli işlem durur, 15 dakika emir toplanır, sonra 2 dakikalık bölümün ilk 30 saniyesinde rastlantısal bir anda müzayede yapılır. Fiyat yukarı %5 çıksa hiçbir şey olmaz (Mart 2025'te yalnız düşüş yönü vardı).

> **Örnek: kapanış ±%3.** Son işlem fiyatı 50,00 TL ise kapanış müzayedesinde fiyat 48,50 ile 51,50 arasında oluşabilir. Biri 55,00'ten alış emri girse bile kapanış fiyatı 51,50'yi aşamaz. Kapanış manipülasyonu senaryosu bu bandın ucunu kullanır (bölüm 5).

## 4. Eşleştirme motoru

### 4.1 İki çalışma modu

**1. Doğrulama (tekrar oynatma).** Gerçek emirler motora verilir. Motorun ürettiği işlemler ve emir durumları gerçek işlem ve emir dosyasıyla karşılaştırılır. Üç ölçüt:
- işlem eşleşme oranı: fiyat, miktar ve iki tarafın emir numarası aynı mı;
- müzayede fiyatı ve miktarı aynı mı;
- gün sonu bülten alanları yeniden üretiliyor mu.

> **Benzetme:** Cevap anahtarı elimizde olan bir sınav. Motor soruları (emirleri) çözer, biz cevaplarını borsanın cevaplarıyla (gerçek işlemlerle) tek tek karşılaştırırız.

**2. Enjeksiyon.** Gerçek emirlere, sentetik bir aktörün emirleri eklenir. Burada önemli bir varsayım var: **gerçek akış dışsaldır (tepkisizdir).** Gerçek katılımcılar sentetik emirleri görüp davranışlarını değiştirmez; aynı emirleri aynı anlarda vermeye devam ederler.

Bu varsayım gerçekçi değildir: gerçek hayatta biri büyük sahte alış emri koyarsa bazı yatırımcılar buna tepki verir. Ama kimin nasıl tepki vereceğini bilmenin yolu yoktur; tahmin etmek, ajan simülasyonuna geri dönmek olur. Bu, yöntemin bilinen ve raporda açıkça yazılan sınırıdır. Pratik sonucu: manipülasyonun piyasaya **doğrudan** etkisini ölçeriz, başkalarını kandırarak yarattığı **dolaylı** etkiyi ölçemeyiz.

> **Benzetme:** Bir maçın kaydına sonradan bir oyuncu ekliyorsun. Topa vurabilir, pas kesebilir; ama diğer oyuncular onu görüp koşularını değiştirmez, çünkü onlar kayıttır.

### 4.2 Motora ne verilir: niyet ve sonuç

Bir emrin albümünden (3.2) yalnız **kullanıcı eylemleri** alınır:
- yeni emir (sebep 6),
- değişiklik (sebep 5; fiyat ve/veya miktar),
- iptal (sebep 1).

Bunlara **niyet** diyoruz: yatırımcının ne istediği. Diğer satırlar (işlem 3, dönüşüm 8, sistem iptalleri 9/34/116/117, yenileme 13, süre dolumu 19, pasifleştirme 4) **sonuçtur**: motorun kendi üretmesi gereken şeylerdir ve karşılaştırmada kullanılır.

> **Neden böyle?** Sonuçları da motora verseydik, motor hiçbir şey hesaplamadan doğru cevabı kopyalardı. Sınavda cevap anahtarını öğrenciye vermek gibi. Motora yalnız niyetleri verip sonuçları onun üretmesini istiyoruz.

İki özel durum:
- **Kotasyonlar:** her güncelleme yeni numarayla geldiği için motor bunu "zincirdeki önceki kotasyonun yerini alan değişiklik" olarak işler. Kotasyonların müzayedeye katılıp katılmadığı veriden ayırt edilemedi; ilk sürümde müzayede hesabına alınmaz (kapanışta en iyi uyum bu varsayımla çıktı).
- **Kısmi görünme emirleri:** tepe büyüklüğü veride yok. Motor, sebep 13 satırlarında görülen yenileme anlarından ya da ilk yenilemedeki işlem miktarından tepeyi tahmin eder.

### 4.3 Motorun parçaları ve hangi kural dosyasına dayandıkları

| Parça | Kural dosyası | Veriyle doğrulanan davranış |
|---|---|---|
| Seans/aşama akışı | `01-seanslar.md`, Ek-10/11 | Bölüm adları ve saatleri; müzayede başlangıcı her aşamada bütün paylar için ortak bir rastlantısal saniye |
| Emir doğrulama | `02-fiyat.md`, `05-emirler.md` (Ek-19) | Fiyat adımı, ±%10 marj, hangi bölümde hangi emir tipine izin var, kapanış ±%3 |
| Sürekli işlem | `04-surekli-islem.md` | Fiyat-zaman önceliği; değişiklikte öncelik kaybı ya da korunması |
| Tek fiyat | `03-tek-fiyat.md` | Denge fiyatı algoritması, müzayede defterleriyle |
| Devre kesiciler | `06-devre-kesici.md` | Pay bazında DK ve EBDKS akışı (tarih parametresiyle) |
| Gün sonu | `02-fiyat.md`, `03-tek-fiyat.md` | Kapanış fiyatı, AOF, bülten alanları |

Üç tasarım ayrıntısı:
- Tek fiyat algoritmasının başvuru uygulaması `veri/araclar/tek_fiyat_algoritma.py`'dir; Prosedür Ek-16'daki örneklerin hepsini geçer. Motor bu işlevi kullanır, yani algoritma iki kez ayrı ayrı yazılmamıştır.
- **Seans takvimi:** tekrar oynatmada her sıranın bölüm geçişleri ve müzayede eşleşme anları veriden alınır. Borsanın rastlantısal saniyesi taklit edilmez, çünkü gerçek anı zaten biliyoruz. (Simülasyon için Ek-10 çizelgesi ve rastlantısal başlangıç kullanılabilir.)
- **EBDKS** bütün piyasayı ilgilendiren bir olaydır (endeks düşüşüne bağlıdır). Tek bir payı oynatan motor endeksi hesaplayamaz; bu yüzden tetikleme anı veriden okunup motora dışarıdan verilir.

### 4.4 Hız

Günde yaklaşık 50–80 milyon emir olayı vardır; bunların yaklaşık %58'i paylara aittir. Sıralar birbirinden bağımsızdır (THYAO'nun defteri ASELS'in defterini etkilemez) ve EBDKS dışarıdan verildiği için motor sıra bazında paralel çalışabilir. Önce doğruluk için Python sürümü yazıldı; çekirdeğin derlenmiş bir dille (numba, Rust ya da C++) hızlandırılması ölçümden sonraya bırakıldı.

Şu anki hız: büyük bir pay-gün 7–30 saniyede, bir günün bütün payları yaklaşık 17 dakikada oynatılıyor.

### 4.5 İlk sürüm (22.10.2026): dosyalar, akış, sonuçlar

**Dosyalar** (`motor/`; testler `motor/testler/`, 28 test; `tespit/testler/` ile toplam 35, hepsi geçer):

| Dosya | Ne yapar (sade) |
|---|---|
| `emir.py` | Emir, işlem ve girdi olaylarının (yeni, değişiklik, iptal) tanımı. Fiyatlar kuruş hatası olmasın diye tamsayı "milli-TL" tutulur. Bölümler arası ortak öncelik sayacı |
| `defter.py` | Emir defteri: fiyat seviyeleri ve her seviyede zaman sırası |
| `surekli_islem.py` | Sürekli işlem: limit, piyasa, piyasadan limite, KİE; öncelik kaybı/korunması; kısmi görünme; DK eşiği; kapanış fiyatından işlemler için sabit fiyat modu |
| `tek_fiyat.py` | Müzayede: emir toplama defteri, denge fiyatı, işlemlerin dağıtımı, dengeleyici emirler, kalanların sonraki bölüme aktarımı |
| `gun.py` | Bir sıra-günün baştan sona akışı: emir toplama, eşleştirme, sürekli işlem, kapanış, kapanış fiyatından işlemler; kapanış eşleşme anının kaydı (`kapanis_ani`); sürekli işlemde saniyede bir defter fotoğrafı (`defter_ornekleri`); enjeksiyon |
| `dogrulama.py` | Sentetik emirlerin kurala uygunluk kontrolü: Ek-19 izinleri, fiyat adımı, marj, kapanış ±%3, kapanış fiyatından işlemlerde fiyat, açığa satış, emir bilgisi değişikliği reddi |
| `parametreler.py` | Tarih parametre tablosunu okur; ölçümü yoksa `OlcumEksik` ile durur |
| `veri.py` | Günlük emir dosyasından girdi olayları, başlangıç defteri, buzdağı tepe tahmini, gerçek işlemler, gün sonu bilgisi |
| `senaryolar.py` | Sentetik manipülasyon senaryoları (bölüm 5) |
| `tekrar_oynat.py` | Doğrulama modu: bir sıra-gün, bölüm bölüm ve bütün gün karşılaştırma |
| `toplu_oynat.py` | Bir günün bütün pay sıralarını (`.E`) oynatır |
| `enjeksiyon.py` | Enjeksiyon modu: enjeksiyonsuz (taban) ve enjeksiyonlu oynatma, fark raporu |

**Bir günün akışı (`gun.py`), adım adım:**
1. Bölüm geçiş saatleri ve müzayede eşleşme anları veriden okunur.
2. Emir toplama bölümlerinde (açılış, kapanış, devre kesici, EBDKS, gün içi tek fiyat) ve EBDKS durdurmasında emirler deftere yazılır, eşleştirme yapılmaz.
3. Eşleştirme anında denge fiyatı hesaplanır: baz fiyat, ±marj (tarih parametresi), kapanışta ayrıca son işlem ±%3 ve Adım 4 referansı. İşlemler dağıtılır; kalan emirler öncelik sıralarıyla bir sonraki bölüme geçer.
4. Sürekli işlemde DK eşiği uygulanır (son müzayede fiyatına, yoksa baz fiyata göre; oran ve yön tarih parametresi). Eşiğin ötesinde eşleşecek gelen emrin kalanı iptal edilir ve DK tetiklenir; sonraki olaylar emir toplama olarak işlenir.
5. Kapanış fiyatından işlemler sabit fiyatla oynatılır.
6. Motorun girdisi: yeni emir, değişiklik, iptal ve dışarıdan gelen sistem iptalleri (116, 117).

**Enjeksiyonda:** sentetik olaylar zamanlarına göre ilgili bölüme yerleşir ve o anki bölüm ile defter durumuna göre kurala uygunluğu kontrol edilir. Kurala aykırı olanlar (ör. kapanış bandının dışında fiyat) reddedilir ve sebebiyle kaydedilir. Motor "manipülatör" için kuralları esnetmez.

**Kapsam dışı:** kotasyonlar, özel işlem bildirimleri, orta nokta emirleri.

**Sonuçlar** (Mart 2025; ölçüt: alış emri, satış emri, fiyat ve adedi birebir aynı işlemlerin oranı; bütün gün oynatıldı):

| Sıra-gün | Müzayedeler | Sürekli işlem | Kapanış fiyatından | Bütün gün |
|---|---|---|---|---|
| THYAO.E 03.03 | 2.588 / %100 | 74.046 / %99,81 | 178 / %100 | %99,82 |
| KRGYO.E 03.03 (devre kesici) | 286 / %100 | 21.217 / %99,92 | 22 / %100 | %99,92 |
| KRGYO.E 27.03 | 47 / %100 | 7.620 / %100 | 8 / %100 | %100 |
| THYAO.E 19.03 (2 EBDKS, devre kesici) | 6.807 / %100; EBDKS 3.227 / %71,4 | 176.028 / %99,82 | 276 / %100 | %99,34 |

Nasıl okunur: "74.046 / %99,81" demek, o gün THYAO'da sürekli işlemde 74.046 gerçek işlem oldu ve motor bunların %99,81'ini alıcısı, satıcısı, fiyatı ve adedi tıpatıp aynı üretti demektir. Eşleşen sürekli işlemlerin hepsinde aktif taraf (gelen emir) da aynıdır.

19.03'teki EBDKS müzayedelerinde %71,4 düşük görünür ama aslında fiyat, toplam miktar ve emir bazında gerçekleşen miktar tamamen aynıdır (3.213 / 3.213). Farklı olan yalnız "hangi alış emri hangi satış emriyle eşleşti" çiftleridir; sebebi tepe büyüklüğü bilinmeyen buzdağı emirleridir.

**Bütün paylar** (`toplu_oynat.py`; özsermaye günleri hariç):
- 03.03.2025: 586 sıra, 4.915.057 işlemin %99,85'i birebir;
- 19.03.2025 (iki EBDKS, çok sayıda devre kesici): 580 sıra, 6.825.508 işlemin %99,91'i birebir.

Özsermaye günlerinde (bedelsiz, temettü) gün sonu dosyasındaki baz fiyat düzeltilmemiş olduğu için motor doğru taban/tavanı bilemez ve işlem üretemez (bölüm 8).

**Veriden öğrenilip motora işlenen davranışlar.** Bunlar Prosedür'de açık yazmayan, veriye bakarak bulunan kurallardır:
- **Müzayede dağıtımı:** alış ve satış tarafı ayrı ayrı öncelik sırasına dizilir (önce piyasa ve fiyatsız piyasadan limite emirler zaman sırasıyla, sonra limit emirler fiyat ve zaman sırasıyla); iki liste baştan, fermuar gibi yürünür.
- **Kısmi görünme:** gelen emir aynı eşleşmede yenilenen tepeden de alırsa tek işlem yazılır. Tepe büyüklüğü sebep 13 satırlarından tahmin edilir.
- **AFK:** AFK alanı dolu bir emirde fiyatı ve kalanı değişmeyen bir değişiklik bile önceliği kaybettirir.
- **Devre kesici:** eşik ve tetikleme davranışı.

**Bilinen sapmalar** (kalan %0,15'lik farkın kaynakları):
- Tek yenilemesi olan ya da yalnız müzayedede işlem gören buzdağı emirlerinde tepe büyüklüğü belirsizdir.
- Aynı fiyatta miktar azaltmada öncelik nadiren kaybolur (THYAO.E 03.03: 551 vakada 2); nedeni veriden ayırt edilemez.
- Bir sapmadan sonra defter birkaç işlem boyunca farklı kalır; oran bu zincirleme etkiyi de içerir. Yani gerçek hata sayısı, oranın gösterdiğinden de azdır.

> **Akılda kalsın:** Motor, borsanın kapalı motorunu dışarıdan, yalnız kural metni ve veriyle %99,85 oranında taklit ediyor. Bu, enjeksiyon sonuçlarına güvenebilmemizin temelidir: motor gerçek günü doğru oynatıyorsa, içine eklenen sentetik emrin etkisini de doğru hesaplar.

## 5. Sentetik manipülasyon enjeksiyonu

**Fikir.** Gerçek veride "bu emir manipülasyondu" etiketi yoktur. Bir tespit yönteminin işe yarayıp yaramadığını ölçmek için doğru cevabı bilmek gerekir. Çözüm: manipülasyonu kendimiz, bilinen bir yere, bilinen büyüklükte koymak.

Senaryolar SPK'nın VI-104.1 sayılı Piyasa Bozucu Eylemler Tebliği'nin bentlerine bağlıdır (tebliğ metni `veri/etiketler/` altında):

| Senaryo | Ne zaman | Emir deseni (sade) | Motorun uyguladığı kural |
|---|---|---|---|
| Kapanış fiyatını etkileme | Kapanış emir toplama (18:01–18:05) | Denge fiyatını iten büyük emir | Kapanışta ±%3 bandı; değişiklik/iptal izinleri |
| Açılış fiyatını etkileme | Açılış emir toplama (09:40–09:55) | 09:50'den önce girip iptal; denge bilgisini yanıltma | 09:50'den sonra iptal, kötüleştirme, azaltma yasak |
| Yanıltıcı emir (spoofing / layering) | Sürekli işlem | En iyi fiyatın birkaç adım gerisine katman katman sahte emir; karşı yönde gerçek bir emir; sonra sahte emirlerin iptali | Fiyat adımı, marj, öncelik |
| Fiyatı adım adım yükseltme (ramping) | Sürekli işlem | Ardışık küçük agresif alımlar | DK eşiği |
| Karşılıklı / kendinle işlem | Sürekli işlem | Aynı aktörün aynı fiyattan satışı ve hemen ardından alışı, makasın içinden | Gerçek veride kimlik yok; yalnız sentetik aktörde etiketli |

Her senaryo günlük dille:
- **Kapanış fiyatını etkileme:** Kapanış fiyatı fon değerlemelerinde, teminat hesaplarında ve ertesi günün baz fiyatında kullanılır. Kapanış müzayedesinin sonunda büyük bir emirle denge fiyatını yukarı ya da aşağı itmek, birçok hesabı birden etkiler.
- **Açılış fiyatını etkileme:** Açılış müzayedesinde ekranda "şu an açılış fiyatı şu olurdu" bilgisi görünür. Büyük bir emir koyup herkesin bu fiyata göre davranmasını sağladıktan sonra emri 09:50'den önce çekmek. Kural 09:50'den sonra iptali tam da bunu önlemek için yasaklar.
- **Yanıltıcı emir:** Satmak istiyorsun ama fiyat düşük. Alış tarafına büyük alış emirleri koyuyorsun; herkes "büyük alıcı var" sanıyor. Sen bu sırada satıyor, sonra sahte alış emirlerini iptal ediyorsun. Sahte emirler hiç işlem görmez; tek izleri "girip hemen çekilen büyük, uzak emirler"dir.
- **Fiyat yükseltme:** Ardışık küçük agresif alımlarla fiyatı adım adım yukarı taşıyıp "yükselen hisse" görüntüsüyle başkalarını çekmek.
- **Karşılıklı işlem:** Aynı kişinin hem alıcı hem satıcı olduğu işlemler. Mülkiyet değişmez ama hacim şişer, pay "çok işlem görüyor" sanılır.

**Kodda hangileri var?** `motor/senaryolar.py`'de dört senaryo yazılıdır: kapanışı etkileme, yanıltıcı emir, fiyat yükseltme, karşılıklı işlem. Açılış fiyatını etkileme senaryosu tasarım tablosunda vardır ama henüz kodlanmadı; bütün sonuçlar (bölüm 6.6) bu dört senaryoyla alındı.

**Enjeksiyon kaydı.** Her sentetik eylem aktör, sıra, zaman, senaryo ve parametreleriyle kaydedilir. Bu kayıt denetimli model için "doğru cevap" (etiket) olur.

> **Benzetme:** Bir dedektif okulunda, öğrencileri sınamak için gerçek bir şehrin kamera kayıtlarına, yerini yalnız hocanın bildiği bir "sahte hırsız" yerleştirmek. Öğrenci hırsızı buluyorsa yöntemi çalışıyordur.

## 6. Manipülasyon tespiti

### 6.1 Neye puan veriyoruz: pay-gün ve pencere

**`TASARIM.md` ne diyor?** Veride üye/hesap kimliği olmadığından tespit birimi **pay-pencere**dir (pay-gün ve gün içi 5 dakikalık pencere). Aktör düzeyinde tespit yalnız sentetik aktör için ölçülebilir.

**Sade anlatım.** "Kim manipülasyon yaptı?" sorusunu soramayız, çünkü emirlerin sahibi veride yok. Sorabileceğimiz soru şudur: "Hangi payda, hangi gün, günün hangi 5 dakikasında olağandışı bir şey var?" Yani her pay-gün ve her pay-pencere bir puan alır; yüksek puan "buraya bak" demektir.

> **Benzetme:** Bir alışveriş merkezinde yüzleri bulanık kamera kayıtları. "Hırsız kim" diyemezsin, ama "2. kattaki mağazada 14:05–14:10 arasında tuhaf bir hareketlilik var" diyebilirsin.

İki düzey neden ayrı?
- **Pay-gün:** bütün günün özeti. Haftalarca süren manipülasyonu görür, ama 30 saniyelik bir epizot günün toplamında kaybolur.
- **5 dakikalık pencere:** kısa epizotları yakalar, ama bütün güne yayılmış bir manipülasyonda gün içinde öne çıkan bir pencere olmaz.

### 6.2 Göstergeler (özellikler)

Model ve kurallar doğrudan ham emirlere bakmaz; ham veriden hesaplanan sayılara, yani **göstergelere** (özelliklere) bakar. Dört grup:

**Emir akışı göstergeleri:**
- yeni emir, değişiklik ve iptal sayıları ve oranları; emir/işlem oranı;
- piyasa emri, KİE, açığa satış, AFK ve kotasyon payları;
- müzayede aşamalarındaki değişiklik ve iptal yoğunluğu;
- açılışın 09:40–09:50 dilimindeki iptaller (açılış manipülasyonunun izi).

**Defter göstergeleri:**
- en iyi seviyelerde derinlik, alış/satış dengesizliği, makas;
- müzayede denge fiyatının eşleşmeye doğru seyri.

**İşlem göstergeleri:**
- fiyat etkisi, aktif taraf dengesizliği, küçük işlem yoğunluğu;
- kapanış seansı ve kapanış fiyatından işlemlerin payı;
- kapanış fiyatının gün içi AOF'den sapması.

**Referans göstergeleri:** pazar, endeks üyeliği, piyasa yapıcı, tedbirler (brüt takas vb.).

> **Örnek:** "İptal oranı" göstergesi: bir payda bir günde 10.000 yeni emir girildi, bunların 9.000'i iptal edildiyse iptal oranı %90'dır. Tek başına bir şey kanıtlamaz (algoritmik işlem yapanlar çok iptal eder), ama aynı payın her zamanki %40'ıyla karşılaştırılınca anlam kazanır.

### 6.3 Yöntemler ve nasıl ölçüldükleri

| Yöntem | Ne yapar (sade) | Benzetme |
|---|---|---|
| İktisadi kurallar | VI-104.1 bentlerine bağlı eşikler: "kısa ömürlü uzak emir payı çok yüksekse uyar" gibi | Trafik radarı: hız sınırını aşanı yakalar |
| Z-skor (temel çizgi) | Bugünkü değerin, payın kendi geçmişinden kaç standart sapma uzak olduğu | "Bu öğrenci her zaman 60 alırdı, bugün 95 aldı" |
| Isolation Forest (denetimsiz) | Rastgele bölmelerle az bölmede yalnız kalan noktayı "aykırı" sayar; manipülasyonun ne olduğunu bilmez | Kalabalıkta tek başına duranı fark etmek |
| Denetimli model | Etiketli örneklerden (SPK vakaları, sentetik enjeksiyonlar) "manipülasyon böyle görünür" diye öğrenir | Çok sayıda sahte para görmüş veznedar |

**Z-skor neden "temel çizgi"?** Öneri formunda klasik yöntemlerle karşılaştırma vardı. Z-skor en basit yöntemdir; daha karmaşık bir yöntem Z-skordan iyi değilse, karmaşıklığa değmez. Her model bu temel çizgiyle karşılaştırılır.

**Değerlendirme zamana göre bölünür.** Model geçmiş günlerle eğitilip gelecek günlerle sınanır. Aksi hâlde model geleceği "görmüş" olur ve olduğundan iyi görünür.

**Ölçütler (en kısa anlatım):**
- **ROC-AUC:** rastgele seçilen bir pozitif (manipülasyonlu) örneğin, rastgele seçilen bir negatiften daha yüksek puan alma olasılığı. 0,5 yazı-tura demektir, 1,0 kusursuz ayırmadır. 0,9 üstü çok iyi, 0,6 altı zayıftır.
- **Kesinlik (precision):** "uyardıklarımın ne kadarı gerçekten manipülasyondu?"
- **Duyarlılık (recall):** "gerçek manipülasyonların ne kadarını yakaladım?"
- **F1:** ikisinin dengeli ortalaması.
- **İlk 3:** enjeksiyon yapılan pencere, o günün en yüksek puanlı 3 penceresine girdi mi? (Bir denetçi her gün her payda yalnız 3 pencereye bakabilseydi, manipülasyonu görür müydü?)
- **Kontrol:** aynı pencerenin enjeksiyonsuz oynatmada da ilk 3'e girme oranı. Bu, **yanlış alarm tabanıdır.** İlk 3 isabeti %80 ama kontrol de %80 ise, yöntem hiçbir şey yakalamıyor, zaten hep o pencereyi işaretliyor demektir.

> **Akılda kalsın:** Bir yöntemin iyi olduğunu söylemek için iki sayı birlikte gerekir: enjeksiyonlu günde yüksek isabet **ve** enjeksiyonsuz günde düşük alarm. Tasarımın en önemli dersi, ilk sürümdeki bazı "iyi" sonuçların kontrol kümesine bakınca boş çıkmasıdır (6.6).

Ayrıntılı istatistik anlatımı (ortalama, standart sapma, ortanca, MAD, karar ağacı, çapraz doğrulama) `ANLATIM.pdf` bölüm 6'dadır.

### 6.4 Veri kapsamı ve SPK etiketlerinin aylara düşmesi

**Sorun.** Elimizde doğrulanmış emir verisi şimdilik yalnız Mart 2025'tir. SPK vakalarından bu aya düşenler azdır:
- ALKLC (A seviyesi; iki kayıt: 2025-17 bülteninde dönem 07–18.03.2025, 2025-57 bülteninde 04.02–18.03.2025; Mart'a 12 pay-gün düşer),
- SMRTG (B, yasak 06.03.2025),
- HEDEF (B, yasak 28.03.2025).

**Etiket seviyeleri (kısaca).**
- **A:** SPK kararında manipülasyon dönemi açıkça yazılı. Dönemin işlem günleri "şüpheli"dir. En güvenilir etikettir.
- **B:** yalnız işlem yasağının başladığı tarih belli, dönem yazmıyor. Dönem, yasaktan önceki bir pencere olarak varsayılır (N = 20 işlem günü).
- C ve D seviyeleri pay-gün etiketi üretmez (dönemsiz ya da kodsuz kayıtlar).

**Kararlar (kullanıcı):**
- 21.10.2026: 2025-01 ve 2025-02 (ITCH ile aynı aylar; A: KRGYO, TDGYO, ALKLC), 2025-04 (A: EUREN 14–21.04; B: SEGMN, ENSRI, BAKAB, VKFYO) ve 2025-05 başı (B: OZATD, KRGYO, yasak 02.05) onaylandı.
- 22.10.2026: kapsam genişletildi. DataStore emir, işlem ve gün sonu verisi 2024-06…2025-05 arası (12 ay) alınır; gerekirse genişletilir.
- 2025-07 ITCH için alınmaz: o ayda A vakası yok, 4 B vakasının hepsi aynı bülten ve aynı yasak tarihindedir (29.07). Buna karşın 2025-02 üç A vakasıyla en zengin aydır.

Ay ay karşılaştırma `veri/etiketler/ay_etiket_ortusmesi.csv` dosyasındadır. İşlem verisi (Mart–Eylül 2025) daha geniş örtüşme sağlar ve işlem tabanlı göstergeler için kullanılabilir.

> **Neden 12 ay şart?** Mart 2025'te A seviyesi pozitif yalnız 12 pay-gündür. 12 pay-günle bir yöntemin iyi mi şanslı mı olduğunu ayırmak çok zordur. 12 ayla hem pozitif sayısı artar hem de "payın geçmişi" daha uzun olur.

### 6.5 Görselleştirme ve emir enjeksiyon arayüzü (zorunlu)

Görselleştirme kullanıcı kararıyla (22.10.2026) zorunludur. Arayüz Streamlit ile yazıldı: `streamlit run arayuz/uygulama.py` komutu tarayıcıda bir sayfa açar.

Şu an ekranda olanlar:
- pay ve gün seçimi; gerçek emir akışının motorda tekrar oynatılması;
- senaryo seçimi ve parametreleri (saat, miktar, katman sayısı, süre…);
- **fiyat grafiği:** enjeksiyonsuz (taban) fiyat ve enjeksiyonlu fiyat; sentetik aktörün işlemleri; 5 dakikalık pencere kural uyarıları (bent a/b, d, f); müzayede, devre kesici ve EBDKS bölümleri gri bant olarak;
- **dakikalık hacim grafiği** (ayrı eksen);
- seçilen pay-gün SPK etiketliyse seviyesi ve bülten numarası bir uyarı kutusunda (etiketler gün düzeyinde olduğu için bant yerine kutu);
- tablolar: uyarılar, sentetik işlemler, reddedilen sentetik olaylar (sebebiyle), dakikalık seri.

Henüz olmayanlar: defter derinliği grafiği, model (Isolation Forest, denetimli) uyarılarının grafikte gösterimi.

> **Örnek:** ASELS 19.03.2025'te "kapanış fiyatını etkileme" senaryosu, alış yönünde 200.000 lot: enjeksiyonlu kapanış fiyatı 112,30'dan 113,00'e kayar. Kapanış bandının dışında bir fiyatla emir girilirse "reddedilen sentetik olaylar" sekmesinde sebebi görünür; motor kuralı uygular.

### 6.6 İlk sürümün sonuçları

#### Kod dosyaları (`tespit/`)

| Dosya | Ne yapar |
|---|---|
| `ozellikler.py` | Pay-gün göstergeleri. Mart 2025: 20 gün × 590 sıra, gün başına ≈ 160 sn. Gün gün ara dosya tutar, yarıda kalırsa kaldığı yerden devam eder |
| `yontemler.py` | Z-skor, iktisadi kurallar (VI-104.1 md 5/1 a, b, d, f), Isolation Forest, kesitsel karşılaştırma, SPK etiketlerinin pay-güne çevrilmesi |
| `degerlendir.py` | SPK etiketleriyle pay-gün sıralama ölçütleri |
| `motor_ozellikleri.py` | Aynı göstergeleri motor çıktısından hesaplar (enjeksiyonlu koşu için) |
| `pencere.py` | 5 dakikalık pencere göstergeleri ve puanları |
| `sentetik_degerlendir.py`, `pencere_degerlendir.py`, `denetimli.py` | Sentetik enjeksiyonla değerlendirme ve denetimli model |

**Kesitsel karşılaştırma nedir?** Payı kendi geçmişiyle değil, **aynı gün aynı pazardaki diğer paylarla** karşılaştırmak; payın o günkü yüzdelik sırasına bakmak (5 günlük birikimli getiri ve hacim artışı dâhil). "Bu öğrenci geçen haftaki notuna göre nasıl?" yerine "bu öğrenci bugün sınıfın kaçıncısı?" sorusu.

#### İki yeni gösterge

- **Kısa ömürlü uzak emir payı:** sürekli işlemde, aynı taraftaki en iyi fiyattan en az 3 adım uzakta girilip 60 saniye içinde işlem görmeden iptal edilen emirlerin miktar payı. Yanıltıcı emrin doğrudan izidir (bent a/b). Verideki olay anındaki en iyi alış/satış fiyatından hesaplanır. Mart 2025 ortancası %1,2; ALKLC'nin manipülasyon günlerinde %7'nin üstünde. Ancak ALKLC'de dönem sonrasında da aynı düzeydedir (günlük ortanca: dönem 6,9, 19.03–30.06 arası 7,6; `rapor.md` 9). Yükseklik paya özgüdür, dönemi ayırt etmez.
- **Makas:** sürekli işlemde göreli makasın ortancası.

> **Örnek:** En iyi alış 45,20 TL, adım 0,02. Biri 45,10'dan (5 adım geride) 50.000 lot alış emri girip 20 saniye sonra hiç işlem görmeden iptal ederse, bu emir "kısa ömürlü uzak emir"dir. Gerçek alıcı en iyi fiyata yakın durur ve işlem görmeyi bekler; sahte alıcı uzakta durur (yanlışlıkla işlem görmemek için) ve çabuk kaçar.

#### SPK etiketleri pay-güne nasıl çevrilir

- **A:** dönemin işlem günleri pozitiftir.
- **B:** yasaktan önceki 20 işlem günü pozitiftir. Pencere yasaktan 3 iş günü önce biter; yasaktan hemen önceki 2 iş günü **belirsizdir** ve değerlendirmeden çıkarılır (kullanıcı kararı, 22.10.2026).
- **Etiketsiz gün negatif değildir, "bilinmiyor"dur.** SPK'nın karar vermediği bir günde manipülasyon olmadığını bilemeyiz. Bu yüzden bütün ölçütler bir **alt sınırdır**: gerçek başarı en az bu kadardır.

> **Örnek: B penceresi.** Yasak bir Pazartesi başlasın. Önceki Perşembe ve Cuma belirsizdir (dışarıda). Önceki Çarşamba pencerenin son günüdür. Çarşambadan geriye 20 işlem günü pozitif sayılır.
>
> **Neden 3 iş günü?** Dönemi ve yasak tarihi birlikte bilinen 4 A vakasının dördünde de dönem, yasaktan tam 3 iş günü önce bitiyor (ör. KRGYO: dönem 25.02.2025 Salı biter, yasak 28.02.2025 Cuma başlar). Aradaki 2 gün eski kuralda pozitiflerin ≈ %10'uydu ve dönem dışıydı; ama SPK'nın inceleme penceresinin kesilmesinden kaynaklanabileceği için negatif de sayılmaz.

#### SPK vakalarıyla sonuç (Mart 2025, pay-gün)

Pozitifler: A ALKLC (12 pay-gün); B HEDEF, SEGMN, ENSRI, BAKAB, KRGYO, OZATD, SMRTG, VKFYO (64 pay-gün).

| Puan | ROC-AUC (A) | ROC-AUC (B) | ROC-AUC (A+B) |
|---|---|---|---|
| Z-skor (kendi geçmişi) | 0,65 | 0,52 | 0,53 |
| İktisadi kurallar | 0,47 | 0,59 | 0,57 |
| Isolation Forest (Z-skor) | 0,53 | 0,53 | 0,53 |
| Kesitsel uç sıra | 0,89 | 0,50 | 0,56 |
| Kesitsel Isolation Forest | 0,90 | 0,53 | 0,59 |

Ne anlama geliyor:
- **Kendi geçmişine bakan yöntemler haftalarca süren manipülasyonda zayıftır**, çünkü geçmiş de manipülasyon içerir. ALKLC dönemi 04.02'de başlıyor; Mart'ta payın "normal geçmişi" zaten manipülasyonlu Şubat'tır. Z-skor "her zamanki gibi" der.
- **Kesitsel karşılaştırma bu kirlenmeye duyarlı değildir.** ALKLC pay-günleri gün içinde ortalama 91. yüzdeliktedir (100 paydan 91'inden daha olağandışı). İki yeni gösterge ALKLC'de ROC-AUC'yi 0,85'ten 0,90'a çıkardı.
- **B'de sonuç rastgeleye yakındır.** B pencereleri bir varsayımdır (N = 20); B yasakları çoğunlukla "işlem bazlı piyasa dolandırıcılığı" şüphesine dayanır; Mart'a düşen günlerin bir kısmı pencerenin başındadır (KRGYO, OZATD, VKFYO).
- Pozitif sayısı azdır; sonuçlar 12 aylık veriyle yeniden ölçülmelidir.

> **Benzetme:** Hep ateşi olan bir hastanın ateşini kendi "normal" ateşiyle karşılaştırırsan hasta görünmez. Aynı gün aynı odadaki diğer hastalarla karşılaştırınca ateşi hemen göze çarpar.

#### Sentetik enjeksiyon: yöntem

1. **Pay-gün seçimi:** 10.03 ve sonrası (Z-skor için en az 5 günlük geçmiş gerekir), sürekli işlemde en az 300 işlem; özsermaye günleri, SPK etiketli ve belirsiz günler hariç. Sürekli işlem senaryolarının saati 10:30–17:00 arasında rastgele seçilir.
2. **Senaryolar**, payın o günkü işlem miktarına (**H**) göre ölçeklenir:
   - **kapanış:** kapanış emir toplamanın sonunda H × %3, bandın ucundan;
   - **yanıltıcı emir:** 3 katman × H × %2, aynı tarafın en iyi fiyatından 4–6 adım geride, 30 sn sonra iptal; arada karşı tarafta H × %0,2 agresif emir (piyasadan limite, KİE). Katmanların, katman toplamının %1'inden fazlası işlem görürse vaka "temiz değil" sayılır ve dışarıda bırakılır;
   - **fiyat yükseltme:** 20 sn arayla 10 agresif alış, her biri H × %0,5;
   - **karşılıklı işlem:** 60 sn arayla 10 kez aynı aktörün satışı ve alışı, her biri H × %0,5; fiyat makasın içinden (en iyi alışın bir adım üstü); makas tek adımsa, makasın en az iki adım açıldığı ilk an beklenir. Aktörün kendi emirleri arasındaki işlem satış miktarının yarısından azsa vaka temiz değildir;
   - bütün sentetik olayları reddedilen vaka (ör. EBDKS durdurması sırasında) değerlendirmeye alınmaz.
3. **Göstergeler motor çıktısından** hesaplanır. Kontrol: enjeksiyonsuz motor göstergeleri veriden hesaplananlarla neredeyse aynıdır; kontrol kümesinde ROC-AUC ≈ 0,5. Yani motor ile veri arasındaki küçük farklar "sahte tespit" üretmez.

> **Örnek: H = 2.000.000 lot olan bir pay-gün.**
> - Kapanış: 60.000 lotluk tek emir.
> - Yanıltıcı emir: 40.000'er lotluk 3 katman (toplam 120.000), karşı tarafta 4.000 lotluk gerçek emir.
> - Fiyat yükseltme: 10.000'er lotluk 10 alış (toplam 100.000 = günün %5'i), 200 saniyeye yayılmış.
> - Karşılıklı işlem: 10 kez 10.000 lot sat + 10.000 lot al.

**Neden "temiz vaka" ölçütü?** Yanıltıcı emir tanımı gereği işlem görmeyen emirdir. Katmanlar işlem görürse artık yanıltıcı emir değil, gerçek alımdır; bu vakayla yöntemi ölçmek yanlış olur. Karşılıklı işlemde de aktörün alışı gerçek bir satıcıyla eşleşirse, o işlem "kendi kendine" değildir. (24.10.2026 düzeltmesinden önce katmanlar son işlem fiyatına göre yerleşiyordu ve karşı emir makas genişse pasif kalıyordu; karşılıklı işlemde kendi emirleri arası işlem ortalama %75'ti, düzeltmeden sonra %89.)

#### Pay-gün düzeyinde sonuç

80 seçimden 76 temiz vaka (24.10.2026 ikinci koşu). Yöntemler kısa süreli enjeksiyonları gün düzeyinde ayırt edemiyor:
- bütün yöntemlerde ROC-AUC 0,57–0,73, ama enjeksiyonsuz kontrol kümesinde de 0,50–0,64;
- kuralların kontrolde bile 0,64 alması, seçilen likit pay-günlerin genel olarak daha yüksek puan almasındandır; enjeksiyonun gerçek katkısı ≈ 0,09;
- senaryo bazında kurallar: kapanış 0,81, fiyat yükseltme 0,72, karşılıklı işlem 0,70, yanıltıcı emir 0,68.

Sonuç: 30 saniyelik bir yanıltıcı emir ya da 200 saniyelik bir yükseltme, günün toplamında kaybolur. Pencere düzeyine geçişin gerekçesi budur.

> **Akılda kalsın:** 0,73 ilk bakışta "fena değil" görünür. Kontrol kümesi 0,64 alınca, yöntemin gerçekte yalnız 0,09 kadar bir şey yakaladığı anlaşılır. Kontrol kümesi olmasaydı yöntemi olduğundan iyi sanırdık.

#### 5 dakikalık pencerede sonuç

**Nasıl puanlanır?** Her pencere, aynı pay-günün diğer pencerelerine göre **sağlam z** ile puanlanır (ortalama yerine ortanca, standart sapma yerine MAD; birkaç uç değer ölçeği bozmasın diye).

**Kapanış penceresi istisnadır.** Kapanış müzayedesi penceresi her gün, aynı günün diğer pencerelerine göre uç değerdir (günün en yoğun anıdır). Bu yüzden payın **önceki günlerdeki kapanışlarıyla** karşılaştırılır: kapanışın AOF'den sapması, kapanış seansı hacim payı, kapanış öncesi getiri. Kapanış penceresi, motorun kaydettiği kapanış eşleşme anından bulunur (`Gun.kapanis_ani`).

> **Dikkat: bulunan bir hata.** 24.10.2026'ya kadar kapanış penceresi `P_ESLESTIRME` bölüm adından bulunuyordu. Ama açılış müzayedesi de aynı adı taşır! Sonuç: açılış penceresi de "kapanış" sayılıyordu. Düzeltmeyle motor kapanış eşleşme anını ayrıca kaydediyor.

Isolation Forest ve denetimli model kapanış penceresini puanlamaz; kapanış senaryosunda pozitif pencere yalnız kapanış müzayedesi penceresidir. **Denetimli model** (gradyan artırmalı karar ağaçları) yalnız sürekli işlem pencerelerinde, **pay-güne göre gruplu 5 katlı çapraz doğrulamayla** eğitilir: veriler 5 parçaya bölünür, model 4 parçayla öğrenip 5.'de sınanır; aynı pay-günün pencereleri hep aynı parçada tutulur ki model "aynı günün komşu penceresini" ezberleyerek kopya çekmesin.

#### Senaryo büyüklüğüne duyarlılık

Senaryo büyüklükleri bir varsayımdır. Bu yüzden her senaryo üç büyüklükte denendi: ×0,3 (küçük), ×1 (temel), ×3 (büyük). 80'er enjeksiyon; bütün yeni göstergeler ve düzeltmelerle (24.10.2026 ikinci koşu). Hücreler: ROC-AUC / ilk 3 isabeti / kontrol ilk 3 (yanlış alarm).

| Senaryo | Ölçek | Kurallar | Denetimli |
|---|---|---|---|
| Yanıltıcı emir | ×0,3 | 0,95 / %89 / %5 | 0,94 / %79 / %0 |
| Karşılıklı işlem | ×0,3 | 0,42 / %5 / %5 | 0,79 / %35 / %15 |
| Fiyat yükseltme | ×0,3 | 0,56 / %5 / %5 | 0,68 / %25 / %5 |
| Kapanış | ×0,3 | 0,58 / %5 / %5 | — |
| Yanıltıcı emir | ×1 | 0,95 / %89 / %5 | 0,95 / %95 / %0 |
| Karşılıklı işlem | ×1 | 0,48 / %5 / %5 | 0,90 / %80 / %10 |
| Fiyat yükseltme | ×1 | 0,60 / %10 / %5 | 0,71 / %30 / %5 |
| Kapanış | ×1 | 0,77 / %20 / %5 | — |
| Yanıltıcı emir | ×3 | 0,95 / %89 / %5 | 0,95 / %89 / %0 |
| Karşılıklı işlem | ×3 | 0,54 / %0 / %5 | 0,95 / %95 / %0 |
| Fiyat yükseltme | ×3 | 0,62 / %10 / %5 | 0,67 / %25 / %0 |
| Kapanış | ×3 | 0,87 / %45 / %5 | — |

Senaryo senaryo, sade dille:
- **Yanıltıcı emir — iyi yakalanıyor, büyüklükten bağımsız.** Kurallar her ölçekte 0,95 / %89 / %5. Kısa ömürlü uzak emir payı bir oran olduğu için küçük katmanlar da iz bırakır; kural büyüklüğe değil davranış biçimine bakar. (Senaryo düzeltmesinden önce 0,89 / %79'du.)
- **Kapanış etkilemesi — büyüklükle ölçekleniyor.** Günlük hacmin %1'i (×0,3) görünmüyor (0,58), %3'ü (×1) sınırda (0,77), %9'u (×3) açıkça görünüyor (0,87, ilk 3'te %45). Yanlış alarm her ölçekte %5; kontrol kümesinde ROC-AUC 0,49 (rastgele), yani alarm gerçekten enjeksiyondan geliyor. Önceki sürümde ×1'de 0,60 ve isabet %0'dı; kapanış göstergeleri (kapanış fiyatının son sürekli işlem fiyatından sapması, kapanış emir toplamadaki alış−satış dengesizliği, son 60 saniyenin payı) bunu değiştirdi.
- **Karşılıklı işlem — yalnız denetimli model, hacimden.** Kurallar ayırt edemiyor (0,42–0,54). Denetimli model yakalıyor ve bunu hacim artışından yapıyor (modelin en önemli göstergesi hacim z'si). Büyüklüğe güçlü bağlı: ilk 3 isabeti ×0,3'te %35, ×1'de %80, ×3'te %95. Aktör kimliği olmadan "aynı kişinin iki tarafı" görülemez; model yalnız "bu pencerede hacim olağandışı arttı" diyebiliyor.
- **Fiyat yükseltme — her ölçekte zayıf.** Net agresif adım göstergesine (ardışık işlemlerde fiyatı yukarı iten agresif alış sayısı eksi aşağı iten agresif satış sayısı) rağmen kurallar 0,56–0,62, denetimli model ilk 3'te en çok %30. 10 agresif alışın bıraktığı iz likit paylarda olağan fiyat hareketi içinde kayboluyor.

> **Neden "ilk 3" ile ROC-AUC birbirini tutmayabilir?** ROC-AUC bütün pencerelerdeki sıralamaya bakar; ilk 3 ise yalnız en tepeye. Kapanış ×1'de ROC-AUC 0,77 ama ilk 3 %20: enjekte edilen pencere çoğu zaman ortalamanın üstünde, ama günün en tuhaf 3 penceresi arasına nadiren giriyor.

#### 15 dakikalık pencere denemesi (fiyat yükseltme için)

Fiyat yükseltme 200 saniyeye yayıldığı için 5 dakikalık pencerelerin sınırına bölünebilir diye 15 dakikalık pencere denendi. İyileşmedi: kurallar ROC-AUC 0,51, denetimli 0,63 (ilk 3 %25, kontrol %15). Ayrıca 15 dakikalık pencerede günde yalnız ≈ 33 pencere olduğundan "ilk 3" hem pozitifte hem kontrolde kolay tutar; bu yüzden ilk 3 burada yanıltıcıdır.

Sonuç: bu büyüklükte (200 saniyede 10 agresif alış, toplam ≈ günlük hacmin %5'i) fiyat yükseltme, likit paylarda olağan fiyat yolundan ayrışan bir iz bırakmıyor. Bu, göstergenin değil **senaryonun** özelliğidir; daha büyük ve uzun yükseltmelerle sınanmalıdır.

#### SPK etiketli günlerde pencere düzeyi

76 etiketli ve 400 etiketsiz pay-günde, gün başına uyarı penceresi sayısına bakıldı (`tespit/spk_pencere.py`):
- A'yı ayırt etmiyor (ROC-AUC 0,44);
- B'de zayıf bir sinyal var (0,61; a/b uyarıları 0,57).

Neden A'da çalışmıyor? Pencere puanı aynı günün diğer pencerelerine göredir. Bütün güne ve haftalara yayılan bir manipülasyonda, gün içinde öne çıkan pencere olmaz; ALKLC'nin her penceresi "aynı derecede manipülasyonlu"dur. Bu vakalarda doğru araç gün düzeyindeki kesitsel karşılaştırmadır (0,90).

> **Akılda kalsın:** İki düzey birbirini tamamlar. Gün düzeyi (kesitsel) uzun süreli manipülasyonu, pencere düzeyi kısa epizotları yakalar. Biri diğerinin yerini tutmaz.

#### Defter göstergeleri

Motor sürekli işlemde defterin fotoğrafını saniyede bir çeker (24.10.2026'ya kadar 10 saniyede bir): en iyi 5 seviyedeki görünen alış ve satış miktarı. Pencerede derinlik dengesizliği ve toplam derinlik hesaplanır. Şimdilik katkısı yok (denetimli modelde önem ≈ 0). Sebebi: yanıltıcı emir katmanları en iyi fiyattan 4–6 adım uzakta, en iyi 5 seviye bunları ancak kısmen görüyor.

#### Sonraki adımlar

- Fiyat yükseltme senaryosunun daha büyük ve uzun hâliyle sınanması.
- Defter göstergelerinin daha derin seviyelerle örneklenmesi.
- 12 aylık veriyle ve daha çok enjeksiyonla yeniden ölçüm (pay-gün, pencere ve SPK günlerinde pencere düzeyi).

## 7. Klasör yapısı

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
motor/                       eşleştirme motoru
tespit/                      göstergeler, kurallar, modeller, değerlendirme
arayuz/                      görselleştirme ve emir enjeksiyon arayüzü
```

Sade anlamı:
- **`kurallar/` ve `ekler/`:** "kanun kitabı". Prosedür'den çıkarılmış kurallar; motor bunlara göre yazılır.
- **`veri/`:** ham veri ve ondan üretilenler. Büyük veri klasörleri **git dışıdır** (yüzlerce GB; sürüm kontrolüne konmaz, ayrıca kişisel/lisanslı veridir).
- **`motor/`:** borsanın taklidi.
- **`tespit/`:** dedektif.
- **`arayuz/`:** vitrin: sonuçları grafikle gösteren sayfa.

## 8. Açık konular: henüz çözülmemiş olanlar

| Konu | Sade anlamı | Neden önemli |
|---|---|---|
| Özsermaye günlerinde baz fiyat | Bedelsiz ya da temettü günlerinde baz fiyat "teorik fiyat"a düzeltilir; gün sonu dosyasındaki önceki kapanış düzeltilmemiş | Doğru taban/tavan bilinmeden motor o günü oynatamaz; bu günler şimdilik dışarıda |
| Mart 2025'teki ±%10 marjın dayanağı | Tablo-4 dipnotu "ikinci bir duyuruya kadar" geçerli duyurulara atıf yapıyor; duyuru metni elimizde değil | Değeri veriden kesin biliyoruz; yazılı kaynağı eksik |
| Aynı mikrosaniyedeki olayların sırası | DataStore'da genel sıra numarası yok | Çok nadir sapmalara yol açar; ITCH ile çözülebilir |
| Üye/hesap kimliği yok | Kimin emir verdiği bilinmiyor | Aktör düzeyinde tespiti imkânsız kılar; bent c ve gerçek veride karşılıklı işlem ölçülemez |
| Yalnız Mart 2025 doğrulandı | 2025-04 emir (1.026.868.890 satır), 2025-05 emir (947.232.947 satır), 2025-04…09 işlem ve 2025-04…08 gün sonu parquet'e çevrildi ama doğrulanmadı | Yeni aylarda parametreler ölçülmeden motor çalışmaz (`OlcumEksik`) |
| Tek fiyatta karışık yön, 2 istisna | ZPBDL.F ve ZRE20.F (öncesinde işlem olmayan BYF açılışları) karar verilen kurala uymuyor | Kural 4 vakadan 2'sine dayanıyor; ek veriyle yeniden bakılmalı |
| 2025-01/02 verisi bekliyor | Emir, işlem ve gün sonu dosyaları indirilmedi | A vakalarının (KRGYO, TDGYO, ALKLC) asıl dönemi bu aylarda |
| Disk | Aylık parquet ve günlük bölümleme birlikte tutulursa 12 ay D: sürücüsüne (440 GB) sığmaz | Saklama biçimine karar verilmeli |
| Sebep 116/117 ve `guncelleme_no` atlamaları | Anlamları bilinmiyor | Motor bunları dışarıdan verilen olay olarak işliyor; anlamı bilinirse modellenebilir |

## 9. Akılda kalsın: tasarımın on cümlelik özeti

1. Ana veri DataStore gün içi verisidir, çünkü müzayede emirlerini yalnız o içerir; ITCH yalnız 2 aylık çapraz doğrulama örneğidir.
2. Her emir satırı bir olaydan sonraki tam durumdur; motora yalnız kullanıcı niyetleri (yeni, değişiklik, iptal) verilir, gerisini motor üretir.
3. Her gün bağımsızdır; önceki günden yalnız baz fiyat gelir.
4. Öncelik zamanı veride yazılı değildir; olay dizisinden türetilir (%99,76 uyum).
5. Kurallar zamanla değişir; veri tarihindeki fiili eşikler tarih parametre tablosunda tutulur ve ölçülmemiş günde motor durur.
6. Motor gerçek işlemlerin %99,85'ini (bütün paylar, bir gün) birebir üretir; müzayedeler %100.
7. Enjeksiyonda gerçek akış tepkisiz kabul edilir; bu, yöntemin bilinen sınırıdır.
8. Kimlik olmadığı için tespit birimi pay-gün ve 5 dakikalık penceredir.
9. Yanıltıcı emir kurallarla, karşılıklı işlem denetimli modelle, kapanış etkilemesi büyük olduğunda yakalanıyor; fiyat yükseltme bu büyüklükte yakalanamıyor; uzun süreli gerçek manipülasyon (ALKLC) kesitsel karşılaştırmayla yakalanıyor.
10. Her sonuç kontrol kümesiyle (enjeksiyonsuz gün) birlikte okunur; sonuçlar 12 aylık veriyle yeniden ölçülecek.
