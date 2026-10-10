# OUCH Protokol Spesifikasyonu (Türkçe çeviri)

Kaynak: `kaynaklar/bistech-ouch-protocol-specification.pdf` — "OUCH Protocol Specification", yayın tarihi 17 Eylül 2026, 31 sayfa (PDF sayfa numarası). Etiket: "HALKA AÇIK/PUBLIC".
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir. Mesaj kodları, alan adları, değerler ve sabitler çevrilmeden bırakılmış; alan adlarının yanında Türkçe karşılıkları parantez içinde verilmiştir. Offset (bayt konumu), uzunluk ve değer sütunları kaynakla aynıdır.
Doğrulama: Tablolardaki (Offset, Uzunluk) çiftleri PDF metninden otomatik çıkarılıp bu dosyayla karşılaştırıldı (ayrıntı dosya sonunda). Metin çevirisi sayfa görüntüsüyle karşılaştırılmadı. Kullanıcı doğrulaması: bekliyor.
İlgili dosyalar: `bistech-itch-protokol-spesifikasyonu.md` (OUCH, emir verisini ITCH'ten alır), `emrimle-eslesmesin-teknik-calisma-esaslari.md` (SMP alanları), `../kurallar/04-surekli-islem.md`.
Not: Bu belge emir iletim protokolüdür (istemciden Borsaya). ITCH yalnızca çıkış yönlüdür; emir girişini OUCH/FIX/TW yapar.

---

## 1 Değişiklik Özeti (Summary of Changes) [s. 4]

| No | Değişiklik |
|---|---|
| 1 | "Message Formats" bölümünde "Enter Order" alt bölümüne `OffHours` alanı eklendi ve mevcut `Reserved` alanı güncellendi (s. 8). |
| 2 | `Order Accepted` mesajı off-hours bayrağıyla güncellendi. |
| 3 | `MassQuote (Q)` ve `MassQuoteAck (K)` mesajlarıyla Mass Quote işlevi eklendi. |
| 4 | `MassQuoteAck` mesajı güncellendi. |
| 5 | `MassQuoteAck` mesajı offset'i güncellendi. |
| 6 | `Order Replaced` mesaj açıklaması güncellendi. |
| 7 | Tablo 6: Mass Quote'taki `Client/Account` alanı notlarında geçerli değerler büyük harfe çevrilerek güncellendi. |
| 8 | Tablo 2 ve 3'teki `Customer Info` alanına bir not eklenerek güncellendi. |
| 9 | `Order Canceled` mesajındaki `Reason` alanı notları güncellendi. |
| 10 | `Order Cancelled` mesajına yeni bir değişiklik sebebi (125) eklendi. |
| 11 | Tablo 2 ve 3'teki `Customer Info` notu güncellendi. |
| 12 | `Enter Order` mesajı SMP işleviyle güncellendi; `Order Accepted` mesajı SMP işleviyle güncellendi; `Order Canceled` mesajına yeni değişiklik sebebi (46) eklendi. |
| 13 | `Order Canceled` mesajına yeni değişiklik sebebi (47) eklendi. |

Kaynaktaki tarihler satırlara hizalı değildir ve hangi tarihin hangi maddeye ait olduğu metin çıkarımından kesin olarak anlaşılamamıştır. Tarihler kaynakta şu sırayla geçer: R.2.11 (21 Mayıs 2020), R.2.11 (1 Temmuz 2020), 10 Temmuz 2020, 5 Mayıs 2021, 8 Eylül 2021, 29 Eylül 2021, 23 Ekim 2023, 10 Eylül 2024, 06 Şubat 2025, 17 Eylül 2026 (10 tarih, 13 madde). Madde–tarih eşleşmesi gerekirse PDF s. 4'ten doğrulanmalıdır. (Yayın tarihi 17 Eylül 2026'dır.)

## 2 Kılavuz Hakkında (About the Manual) [s. 5]

Bu belgenin amacı OUCH protokolünü tanımlamaktır. Daha fazla bilgi için başvurulacak belgeler: Genium INET ITCH Protocol Specification; System Error Message Reference.

## 3 OUCH'a Genel Bakış (OUCH Overview) [s. 6–7]

OUCH protokolü sistem katılımcılarından limit emirleri kabul eder ve mümkün olduğunda eşleşen emirleri gerçekleştirir. Eşleşmeyen emirler, eşleştirme öncelik modeline göre eşleşmeyi bekledikleri emir defterine eklenebilir.

OUCH, Genium INET Trading kullanıcılarının emir girmesine, mevcut emirleri değiştirmesine ve iptal etmesine ve gerçekleşmeleri almasına olanak tanıyan basit bir protokoldür. Katılımcıların ve yazılım geliştiricilerinin Genium INET Trading'i kendi işlem sistemlerine entegre etmesi veya özel ön yüzler geliştirmesi için tasarlanmıştır.

OUCH yalnızca katılımcıların Genium INET Trading'e emir göndermesi ve girdikleri emirlere ilişkin güncellemeleri alması için bir yöntem sağlar. Genium INET Trading defterine girilen ve orada gerçekleşen tüm emirlere ilişkin bilgi için ITCH protokol spesifikasyonuna bakılmalıdır.

OUCH, Genium INET Trading sistemine bağlanmak için kullanılan düşük seviyeli yerel (native) protokoldür; esneklik ve kullanım kolaylığı pahasına mümkün olan en yüksek performansı sunmak üzere tasarlanmıştır. Bu aşırı performans düzeyini gerektirmeyen uygulamalar için Genium INET Trading daha uygun ve geliştirmesi daha kolay başka standart arayüzler sunar.

### 3.1 Mimari (Architecture)

OUCH protokolü, OUCH sunucusu (host) ile istemci uygulaması arasında geçen mantıksal mesajlardan oluşur. Her mesaj tipinin sabit bir mesaj uzunluğu vardır. Mesajlar ikili (binary) kodludur; yani tüm sayısal değerler ikili değer olarak gösterilir. Karakter veya dizge değerleri kontrol karakteri içermeyen ISO 8859-9 (Latin-9) kodlu baytlardan oluşur.

OUCH sisteminden istemciye gönderilen tüm (çıkış yönlü) mesajların sıralı olduğu ve teslimlerinin alt seviye protokolle garanti edildiği varsayılır. Sunucudan istemciye giden OUCH mesajlarının teslimini ve sıralanmasını garanti etmek için SoupBinTCP protokolü kullanılır (ayrı bir spesifikasyon; bkz. `soupbintcp-protokol-spesifikasyonu.md`).

OUCH istemcisinden sunucuya gönderilen mesajlar, TCP/IP soketleri gibi teslimi garanti eden bir alt seviye protokolle taşınsalar bile doğası gereği garantili değildir. Bu nedenle sunucuya giden tüm mesajlar, bağlantı ve uygulama hatalarından sağlam bir şekilde kurtarma için zararsızca (benign) yeniden gönderilebilecek şekilde tasarlanmıştır.

Her fiziksel OUCH sunucu portu, piyasa tarafından atanan bir OUCH Hesabına (Account) bağlıdır. Belirli bir günde OUCH üzerinden girilen her emir, mantıksal OUCH Hesabı ile katılımcının oluşturduğu `Token` alanının birleşimiyle benzersiz olarak tanımlanır.

### 3.2 Veri Tipleri (Data Types) [s. 6–7]

Tüm tamsayı alanlar ikili kodlanmış sayılardan oluşur.

**Tablo 1: Veri Tipleri**

| Tip | Boyut | Notlar |
|---|---|---|
| Numeric | 1, 2, 4, 8 veya 12 bayt | İşaretsiz, big-endian ikili kodlu sayılar. NOT: İstisna, `Reject Code` işaretli tamsayıdır. |
| Alpha | değişken | Sola yaslı ve sağdan boşlukla doldurulmuş. Kontrol karakteri içermeyen ISO 8859-9 (Latin-9) kodlu baytlardan oluşur. |
| Price | 4 bayt | Fiyatlar işaretli tamsayı alanlardır. Ondalık hane sayısı ve izin verilen fiyat adımları ITCH Order book Directory mesajında (Number of decimals in Price) belirtilir. NOT: Emir defterleri kesirlerle de işlem görebilir; bu da Order book Directory mesajında belirtilir. |
| Timestamp | 8 bayt | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren geçen nanosaniye sayısı). |

### 3.3 Hata Toleransı (Fault Redundancy) [s. 7]

Tek bir OUCH Hesabı iki fiziksel OUCH ağ geçidine (gateway) bağlanabilir. Bu ağ geçitleri hata toleransı için birbirinin aynası (mirror) gibi çalışır. Bu yapılandırmada istemci ağ geçitlerinden herhangi birine bağlanabilir. Aynı anda ikisine birden giriş yapmasına izin verilmez; aynı hesap için ikinci oturum kurulduğunda sistem ilk istemci oturumunu kapatır.

OUCH ağ geçidi, başka bir OUCH Hesabının, zaten kullanımda olan birincil ağ geçidi portunun yedek (standby) ağ geçidi portuna erişmesini ne destekler ne de engeller.

## 4 Mesaj Formatları (Message Formats) [s. 8–25]

### 4.1 Giriş Yönlü Mesajlar (Inbound Messages) [s. 8]

Giriş yönlü mesajlar katılımcının uygulamasından OUCH sunucusuna gönderilir. Sıralı değildir. Tüm giriş yönlü mesajlar zararsızca tekrarlanabilir. Bu, bağlantı kaybı veya uygulama hatası durumunda Genium INET Trading sisteminin bir mesajı alıp almadığı belirsizse istemcinin herhangi bir giriş yönlü mesajı yeniden gönderebilmesini sağlar.

Zararsız (benign) giriş yönlü mesaj yeniden iletimi ve uçtan uca onay fikri, OUCH'un kesinti durumunda yedek sisteme geçiş (fail-over) yedekliliğinin temelidir. Bağlantınız koparsa, bekleyen mesajların hata öncesinde bağlantıdan geçip geçmediğini bilmenin yolu yoktur. Sağlam bir OUCH istemcisi, tekrarlı mesaj oluşturma endişesi olmadan bekleyen mesajları ayna bağlantıdan güvenle yeniden gönderebilir. Bu, Genium INET Trading'in felaket kurtarma (disaster failover) yeteneği için de geçerlidir: Sistem yedek merkeze geçmek zorunda kalırsa, hatanın olduğu anda gönderilen bazı mesajlar kaybolabilir. Sağlam bir uygulama bekleyen mesajları basitçe yeniden göndererek geçişi son kullanıcı için kesintisiz hâle getirebilir.

Bir OUCH portundaki tüm giriş yönlü mesajlar sırayla işlenir. Bu, aynı bağlantıda art arda iki emir girilirse ilk girilen emrin her zaman önce kabul edileceğini garanti eder.

#### 4.1.1 Enter Order (Emir Girişi) [s. 8–10]

Enter Order, sisteme yeni bir emir girmek için kullanılır. Başarılı bir Enter Order'a yanıt `Order Accepted` mesajıdır. Emir reddedilirse `Order Rejected` mesajı döner.

> **Not:**
> - OUCH üzerinden girilen tüm emirler varsayılan olarak Round Lot (tam lot) tipindedir. Emrin miktarı Round Lot Size'ın katı olmalıdır. Belirli bir emir defterinin Round Lot Size değeri ITCH Order book Directory mesajında bulunur.
> - Hepsi ya da Hiçbiri (All Or None) emirleri desteklenmez.
> - Hesap bilgisi (Account Info), türev piyasası için `Client/Account` alanını, pay piyasası için `Exchange Info` alanını kullanmalıdır.

**Tablo 2: Enter Order Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "O" | Enter Order Mesajı. |
| Order Token | 1 | 14 | Alpha | İstemci tarafından üretilen emir tanımlayıcısı. |
| Order book ID | 15 | 4 | Numeric | Emir defteri tanımlayıcısı. |
| Side | 19 | 1 | Alpha | Değerler: "B" = Alış emri; "S" = Satış emri; "T" = Açığa satış (Short sell) |
| Quantity | 20 | 8 | Numeric | Miktar. |
| Price | 28 | 4 | Price | İşaretli tamsayı fiyat. Ondalık hane sayısı ve izin verilen fiyat adımları ITCH'teki Order book Directory mesajından alınır. Bu alan güvenliğin kesirlerle işlem görüp görmediğini de belirtir. |
| Time In Force | 32 | 1 | Numeric | Değerler: 0 = Day (Gün); 3 = Immediate or Cancel (FaK); 4 = Fill or Kill |
| Open Close | 33 | 1 | Numeric | Hesap için pozisyon güncellemesi. Değerler: 0 = Hesap için varsayılan; 1 = Open (aç); 2 = Close/Net (kapat/netle) |
| Client/Account | 34 | 16 | Alpha | Aktarım (pass-thru) alanı. Fon emirleri için zorunludur. Agency/Fund Code (AFK). Not: Hesap bilgisi türev piyasası için bu alanı kullanmalıdır. |
| Customer Info | 50 | 15 | Alpha | Aktarım (pass-thru) alanı. Müşteri referans alanı. Not: Bu alanda yazdırılamaz ASCII karakterleri (SOH, DC1, RS, ..) bulunmamalıdır. |
| Exchange Info | 65 | 32 | Alpha | Müşteri hesap numarası. Yalnızca ilk 16 bayt kullanılır; ilk 16 bayttan fazlasının kullanılması işlemin reddedilmesine yol açabilir. Not: Hesap bilgisi pay piyasası için bu alanı kullanmalıdır. |
| Display Quantity | 97 | 8 | Numeric | Rezerv (reserved) emirse görüntülenen miktar, değilse sıfır (0). |
| Client Category | 105 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client (müşteri); 2 = House (portföy); 7 = Fund (fon); 9 = Investment Trust (yatırım ortaklığı); 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company (portföy yönetim şirketi). Not: Client Category türev piyasasında kullanılmaz. |
| OffHours | 106 | 1 | Numeric | Değerler: 1 = Off-hour emirleri (mesai dışı); 0 = Normal saatler. Diğer değerler isteğin reddedilmesine yol açar. Not: Off-hours türev piyasasında kullanılacaktır. |
| SMP Level | 107 | 1 | Numeric | SMP Level, SMP'nin kapsamını belirtir. Değerler: 0 = Boş; 1 = Üye içinde (Within a member); 2 = Üyeler arasında (Across members) |
| SMP Method | 108 | 1 | Numeric | SMP Method, olası bir eşleşmenin önlenmesi durumunda işlem sisteminin yapacağı eylemi belirtir. Değerler: 0 = Boş; 1 = Agresif emri iptal et; 2 = Pasif emri iptal et; 3 = Her ikisini iptal et |
| SMP ID | 109 | 3 | Alpha | SMP ID, emrin Emrimle Eşleşmesin özelliğine uygun olduğunu belirtir. SMP Level 1 için SMP ID üye tarafından, SMP Level 2 için Borsa tarafından atanır. Not: Bu alanda yazdırılamaz ASCII karakterleri bulunmamalıdır. |
| Reserved | 112 | 2 | | Gelecekte kullanım için ayrılmıştır. |

> **Çeviri notu:** Kaynakta `Time In Force` = 3 için "Immediate or Cancel (FaK)" yazılıdır (FaK = Fill and Kill; FIX'te IOC). Çeviri bu ifadeyi korur.

#### 4.1.2 Replace Order (Emir Değiştirme) [s. 10–12]

Replace Order, OUCH üzerinden girilmiş mevcut bir emri değiştirmek için kullanılır. Sistemin yapılandırmasına bağlı olarak bazı emir parametrelerinin değiştirilmesine izin verilmeyebilir; bu durumda `Order Rejected` döner.

Replace mesajında iki emir token'ı vardır:
- **Existing Order Token:** Değiştirilecek emri referans göstermek için kullanılır. Order Token, ara değişikliklerden değil, özgün Enter Order'dan alınmalıdır. Mevcut uygulama ara token'ların kullanılmasına izin verir ancak bu gelecekte desteklenmeyebilir.
- **Replacement Order Token:** Değiştirme başarılı olursa emre atanacak yeni Order Token'dır. Replacement Order Token, daha önce Enter Order veya Replace Order işlemlerinde kullanılmış bir token olmamalıdır.

Replace Order'a yanıt:
- Değiştirme başarılıysa `Order Replaced`. Order Replaced, emrin güncel durumunu içerir (emir miktarları için aşağıya bakın).
- Değiştirme başarısızsa `Order Rejected`.

**Tablo 3: Replace Order Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "U" | Replace Order Mesajı. |
| Existing Order Token | 1 | 14 | Alpha | Ara değişikliklerden değil, özgün Enter Order'daki Order Token olmalıdır. |
| Replacement Order Token | 15 | 14 | Alpha | |
| Quantity | 29 | 8 | Numeric | Emrin istenen açık (open) miktarı. |
| Price | 37 | 4 | Price | İşaretli tamsayı fiyat. Ondalık hane sayısı ve izin verilen fiyat adımları ITCH'teki Order book Directory mesajından alınır. Bu alan güvenliğin kesirlerle işlem görüp görmediğini de belirtir. Price = 0, "değişiklik yok" anlamına gelir. |
| Open Close | 41 | 1 | Numeric | Hesap için pozisyon güncellemesi. Değerler: 0 = Değişiklik yok; 1 = Open; 2 = Close/Net; 4 = Hesap için varsayılan |
| Client/Account | 42 | 16 | Alpha | Aktarım alanı. Not: Hesap bilgisi türev piyasası için bu alanı kullanmalıdır. |
| Customer Info | 58 | 15 | Alpha | Aktarım alanı. Not: Bu alanda yazdırılamaz ASCII karakterleri (SOH, DC1, RS, ..) bulunmamalıdır. |
| Exchange Info | 73 | 32 | Alpha | Müşteri hesap numarası. Yalnızca ilk 16 bayt kullanılır; ilk 16 bayttan fazlasının kullanılması işlemin reddedilmesine yol açabilir. Not: Hesap bilgisi pay piyasası için bu alanı kullanmalıdır. |
| Display Quantity | 105 | 8 | Numeric | İstenen görüntülenen miktar (değişmemesi için sıfır). |
| Client Category | 113 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client; 2 = House; 7 = Fund; 9 = Investment Trust; 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company. Not: Client Category türev piyasasında kullanılmaz. |
| Reserved | 114 | 8 | | Gelecekte kullanım için ayrılmıştır. |

##### 4.1.2.1 Emir Miktarları (Order Quantities) [s. 12]

Genium INET OUCH Replace mesajlarında `Quantity` alanı, emrin istenen **toplam** miktarını içerir (Emir Miktarı = açık miktar + gerçekleşen miktar; açık miktar emrin emir defterindeki miktarıdır).

**Örnek 1:**
1. OUCH üzerinden 1000 miktarlı bir emir girilir. Quantity = 1000 olan bir `Order Accepted` döner.
2. 200'lük kısmi gerçekleşme olur. Emir defterinde 800 kalır. Traded Quantity = 200 olan bir `Order Executed` döner.
3. İstemci açık miktarı (defterdeki miktar) 750'ye düşürmek ister. Quantity = 950 olan bir `Order Replace` gönderir. Quantity = 750 olan bir `Order Replaced` döner.

**Örnek 2:**
1. OUCH üzerinden 1000 miktarlı bir emir girilir. Quantity = 1000 olan bir `Order Accepted` döner.
2. İstemci açık miktarı (defterdeki miktar) 500'e düşürmek ister. Quantity = 500 olan bir `Order Replace` gönderir.
3. Aynı anda emrin 600'ü (kısmen) gerçekleşir. Traded Quantity = 600 olan bir `Order Executed` döner.
4. İstemci, defterde miktar kalmadığı için Quantity = 0 ve Order Status = Not on book olan bir `Order Replaced` alır.

##### 4.1.2.2 Emir Defteri Önceliğinin Korunması (Retaining Order book Priority) [s. 12]

Genium INET'te emir niteliklerinin çoğunun değiştirilmesine izin verilir. Belirli bir niteliğin değiştirilmesi, hangi değerlerin değiştirildiğine, sistemin nasıl yapılandırıldığına vb. bağlı olarak emrin önceliğini kaybetmesine yol açabilir. Bir değişikliğin ne zaman öncelik kaybına yol açtığının ayrıntılı açıklaması bu belgenin kapsamı dışındadır.

Bir emir değiştirilirken önceliğini koruma ihtimalini artırmak için, değişmesi istenmeyen tüm alanlar ayarlanmamış (unset) bırakılmalıdır:
- Sayısal (Numeric) emir parametreleri için bu, 0 (sıfır) olarak ayarlamak demektir.
- Dizge (Alpha) alanlar için, önceki değerin korunması amacıyla ilk bayt ikili sıfır `'\0'` olarak ayarlanmalıdır.

> **Not:**
> - Sistem, sıfır olarak ayarlanan alanlarda "değişiklik yok" varsaydığı için Price'ı 0'a değiştirmek mümkün değildir.
> - Sistem, öncelik kaybına yol açacak replace'leri reddedecek şekilde yapılandırılabilir.

#### 4.1.3 Cancel Order (Emir İptali) [s. 12–13]

Kısmi iptaller Cancel Order mesajıyla desteklenmez; mevcut bir emri değiştirmek için Order Replace kullanılmalıdır.

Başarılı bir Cancel Order'a yanıt `Order Canceled` mesajıdır. Başarısız Cancel Order mesajları `Order Reject` mesajıyla reddedilir.

> **Not:** Order Token, ara değişikliklerden değil, özgün Enter Order'dan alınmalıdır. Mevcut uygulama ara token'ların kullanılmasına izin verir ancak bu gelecekte desteklenmeyebilir.

**Tablo 4: Cancel Order Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "X" | Cancel Order Mesajı |
| Order Token | 1 | 14 | Alpha | Ara değişikliklerden değil, özgün Enter Order'daki Order Token olmalıdır. |

#### 4.1.4 Cancel by Order ID (Order ID ile İptal) [s. 13–14]

Sistemin ürettiği Order ID kullanılarak bu mesajla, emrin hangi seansta girildiğinden bağımsız olarak defterdeki herhangi bir emir iptal edilebilir.

Başarılı bir Cancel by Order ID'ye yanıt `Order Canceled` mesajıdır. Başarısız Cancel by Order ID mesajları `Order Reject` mesajıyla reddedilir.

**Tablo 5: Cancel By Order ID Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "Y" | Cancel By Order ID Mesajı |
| Order book ID | 1 | 4 | Numeric | Emir defteri tanımlayıcısı. |
| Side | 5 | 1 | Alpha | Değerler: "B" = Alış emri; "S" = Satış emri |
| Order ID | 6 | 8 | Numeric | Sistemin emre atadığı tanımlayıcı. |

#### 4.1.5 Mass Quote (Toplu Kotasyon) [s. 14–16]

Mass Quote mesajı, piyasa yapıcılar tarafından piyasaya kotasyon göndermek için kullanılır. Kotasyon mesajları tipik olarak işlem yapılabilir kotasyonlu piyasalarda sürekli, istek dışı (unsolicited) kotasyon göndermek için kullanılır. Bir kotasyon çift taraflı olmalıdır; yani normalde hem alış hem satış fiyatı ve miktarını içerir. Tüm kotasyonlar günün sonuna kadar (veya iptal edilene kadar) geçerlidir.

Mass Quote mesajı kullanıcının tek mesajda birden çok kotasyon göndermesine izin verir (şu anda 5 kotasyonla sınırlı). Mass quote mesajındaki farklı güvenliklerin kotasyonları aynı bölüme (partition) ait olmalıdır. Katılımcı başına enstrüman başına bir (çift taraflı) kotasyona izin verilir.

Mass Quote'a dönüş mesajı olarak "Mass Quote Acknowledgement (MsgType = K)" veya "Mass Quote Rejection (MsgType = R)" gönderilir. Kotasyon akışı "Appendix A, Workflows for Quoting" bölümünde örneklerle ayrıntılandırılmıştır. Dönüş akışı özeti:

- **Tüm kotasyonlar reddedildiğinde:** Mass quote'taki kotasyonların hiçbiri kabul edilmezse, mass quote bloğuna yanıt olarak OrderBookID içermeyen yalnızca bir "Mass Quote Rejection" mesajı gönderilir.
- **Tüm kotasyonlar kabul edildiğinde:** Mass quote'taki her kabul edilen kotasyon için "Mass Quote Acknowledgement (MsgType = K)" gönderilir. Yanıt olarak alış ve satış tarafı için toplam iki "K" mesajı gönderilir.
- **Bazı kotasyonlar kabul, bazıları reddedildiğinde:** Mass quote'taki her tekil kotasyon için "Mass Quote Acknowledgement (MsgType = K)" veya "Mass Quote Rejection (MsgType = R)" gönderilir. Reddedilen kotasyonlar için ilgili tekil kotasyona özel OrderbookID'li bir "R" mesajı; kabul edilen kotasyonlar için ilgili tekil kotasyon için (alış ve satış tarafı) iki "K" mesajı gönderilir.

Kotasyonlar, aynı enstrüman(lar) için yeni bir Mass Quote göndererek değiştirilebilir. Çift taraflı bir kotasyonun yalnızca bir tarafı değiştirilip diğer taraf değiştirilmeden bırakılabilir (örneğin önceliği kaybetmemek için). Kotasyonun bir tarafını değişmeden bırakmak için o taraftaki miktar 0 yapılır (Bid Size = 0 VEYA Offer Size = 0). Bu, mevcut kotasyon fiyatı sıfır olsa bile geçerlidir (bazı enstrümanlar için sıfır geçerli bir fiyattır). Hem fiyat hem miktar sıfır yapılırsa kotasyon iptali olarak yorumlanır (aşağıya bakın).

Kotasyonlar, alış ve satış fiyatlarının ve miktarlarının hepsi sıfır olan yeni bir Mass Quote göndererek iptal edilebilir. Çift taraflı bir kotasyonun yalnızca bir tarafını, o taraftaki fiyat ve miktarı sıfır yaparak iptal etmek de mümkündür. (Bid Price = 0 && Offer Price = 0 && Bid Size = 0 && Offer Size = 0)

Ekleme/güncelleme/iptal istekleri "Appendix B, Quote Matrix" bölümünde ayrıntılandırılmıştır.

> **Not:**
> - "QuoteSet" OrderbookID (4), BidPx (4), OfferPx (4), BidSize (8), OfferSize (8) alanlarını içerir ve 28 karakter gerektirir.
> - Mass quote sayısı (kullanıcı tarafından `NoQuoteEntries` içinde tanımlanır) 5 kotasyonla sınırlıdır.

**Tablo 6: Mass Quote**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "Q" | Mass Quote |
| OrderToken | 1 | 14 | Alpha | İstemci tarafından üretilen kotasyon tanımlayıcısı. Her istek (yeni, güncelleme, iptal) için benzersizdir. |
| Client Category | 15 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client; 2 = House; 7 = Fund; 9 = Investment Trust; 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company |
| Client/Account | 16 | 16 | Alpha | Agency/Fund Code. Değerler: PYM (piyasa yapıcı müşteri / market maker client); PYP (piyasa yapıcı portföy / market maker portfolio) |
| Exchange Info | 32 | 16 | Alpha | Müşteri hesap numarası |
| NoQuoteEntries | 48 | 2 | Numeric | QuoteSet içindeki çift taraflı kotasyon sayısı. Her QuoteSet, Mass Quote mesajı için, her girdinin tekil bir çift taraflı kotasyonu temsil ettiği tekrarlı bir QuoteEntries grubu içerir. Şu anda en fazla 5 kotasyona izin verilir: 1. kotasyon offset 50–77, 2. kotasyon offset 78–105, 3. kotasyon offset 106–133, 4. kotasyon offset 134–161, 5. kotasyon offset 162–189. Not: Mass quote mesaj uzunluğu `NoQuoteEntries` değerine göre dinamik olmalıdır. |
| →OrderBookID | 50 | 4 | Numeric | İlk kotasyonun emir defteri tanımlayıcısı |
| →BidPx | 54 | 4 | Price | Fiyat. Ondalık hane sayısı ve izin verilen fiyat adımları ITCH'teki Order book Directory mesajından alınır. |
| →OfferPx | 58 | 4 | Price | Fiyat. Ondalık hane sayısı ve izin verilen fiyat adımları ITCH'teki Order book Directory mesajından alınır. |
| →BidSize | 62 | 8 | Numeric | Miktar |
| →OfferSize | 70 | 8 | Numeric | Miktar |

> **Çeviri notu:** `→` ile başlayan alanlar tekrarlı gruptaki (QuoteSet) alanlardır; offset'ler ilk kotasyon içindir (50–77). Sonraki kotasyonlar 28'er bayt ileridedir.

### 4.2 Çıkış Yönlü Mesajlar (Outbound Messages) [s. 16–25]

Çıkış yönlü mesajlar sistem tarafından üretilir ve OUCH istemcisine gönderilir.

#### 4.2.1 Order Accepted (Emir Kabul Edildi) [s. 16–18]

Bu mesaj, geçerli bir Enter Order mesajının alındığını ve kabul edildiğini onaylar. Enter Order mesajındaki veri alanları bu mesajda geri yansıtılır. Bazı alanlar için kabul edilen değerlerin girilen değerlerden farklı olabileceğine dikkat edilmelidir. Accepted mesajlarının, bir emre ait Executed veya Canceled mesajlarından önce gelmesi garanti edilir.

> **Not:** Emir girişte hemen gerçekleşir veya başka bir şekilde değişirse, `Order Accepted` bu işlemlerden sonraki emir durumunu gösterir. Farklılıkları hesaba katmak için ardından execution ve/veya cancel mesajları gelir.

**Tablo 7: Order Accepted Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "A" | Order Accepted Mesajı. |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | |
| Order book ID | 23 | 4 | Numeric | Emir defteri tanımlayıcısı. |
| Side | 27 | 1 | Alpha | Değerler: "B" = Alış emri; "S" = Satış emri; "T" = Açığa satış |
| Order ID | 28 | 8 | Numeric | Yeni emre atanan tanımlayıcı. Numaranın yalnızca emir defteri ve taraf başına benzersiz olduğuna dikkat edin. |
| Quantity | 36 | 8 | Numeric | Defterde şu anda açık olan miktar. |
| Price | 44 | 4 | Price | İşaretli tamsayı fiyat. Ondalık hane sayısı ITCH'teki Order book Directory mesajından alınır. Bu alan güvenliğin kesirlerle işlem görüp görmediğini de belirtir. |
| Time In Force | 48 | 1 | Numeric | Değerler: 0 = Day; 3 = Immediate or Cancel (FaK); 4 = Fill or Kill |
| Open Close | 49 | 1 | Numeric | Hesap için pozisyon güncellemesi. Değerler: 0 = Değişiklik yok; 1 = Open; 2 = Close/Net; 4 = Hesap için varsayılan |
| Client/Account | 50 | 16 | Alpha | Aktarım alanı. Not: Hesap bilgisi türev piyasası için bu alanı kullanmalıdır. |
| Order State | 66 | 1 | Numeric | Değerler: 1 = On book (defterde); 2 = Not on book (defterde değil); 98 = Paused (duraklatılmış) |
| Customer Info | 67 | 15 | Alpha | Aktarım alanı. |
| Exchange Info | 82 | 32 | Alpha | Yalnızca ilk 16 bayt kullanılır; ilk 16 bayttan fazlasının kullanılması işlemin reddedilmesine yol açabilir. Not: Hesap bilgisi pay piyasası için bu alanı kullanmalıdır. |
| Pre Trade Quantity | 114 | 8 | Numeric | İşlem öncesi miktar. |
| Display Quantity | 122 | 8 | Numeric | Rezerv emirse görüntülenen miktar, değilse sıfır (0). |
| Client Category | 130 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client; 2 = House; 7 = Fund; 9 = Investment Trust; 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company. Not: Client Category türev piyasasında kullanılmaz. |
| OffHours | 131 | 1 | Numeric | Değerler: 1 = Off-hour emirleri; 0 = Normal saatler. Diğer değerler isteğin reddedilmesine yol açar. Not: Off-hours türev piyasasında kullanılacaktır. |
| SMP Level | 132 | 1 | Numeric | SMP Level, SMP'nin kapsamını belirtir. Değerler: 0 = Boş; 1 = Üye içinde; 2 = Üyeler arasında |
| SMP Method | 133 | 1 | Numeric | SMP Method, olası bir eşleşmenin önlenmesi durumunda işlem sisteminin yapacağı eylemi belirtir. Değerler: 0 = Boş; 1 = Agresif emri iptal et; 2 = Pasif emri iptal et; 3 = Her ikisini iptal et |
| SMP ID | 134 | 3 | Alpha-numeric | SMP ID, emrin Emrimle Eşleşmesin özelliğine uygun olduğunu belirtir. SMP Level 1 için üye tarafından, SMP Level 2 için Borsa tarafından atanır. |

#### 4.2.2 Order Rejected (Emir Reddedildi) [s. 18]

Bu mesaj, Enter Order, Cancel Order ve Replace Order mesajlarını reddetmek için kullanılır.

**Tablo 8: Order Rejected Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "J" | Order Rejected Mesajı. |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | Gelen emirden doldurulur; geçersiz değerler korunur. |
| Reject Code | 23 | 4 | Numeric | Arka uç (backend) hata kodu. Daha fazla bilgi için System Error Messages Reference'a bakın. |

#### 4.2.3 Order Replaced (Emir Değiştirildi) [s. 18–21]

Bu mesaj, geçerli bir Replace Order mesajının alındığını ve kabul edildiğini onaylar. Replace Order mesajındaki veri alanları bu mesajda geri yansıtılır. Bazı alanlar için kabul edilen değerlerin girilen değerlerden farklı olabileceğine dikkat edilmelidir. Her değiştirme için bu ikisinden yalnızca birini alırsınız.

Accepted mesajları gibi Replaced mesajları da, bir değiştirmenin kabul edildiğini ve ardından `Order State` değeri Not on book (2) olduğunda otomatik olarak iptal edildiğini belirtmek için `Order State` alanını kullanır.

> **Not:**
> - Bir emir sistem tarafından değiştirilirse, Replacement Order Token boşluklarla silinir. Previous Order Token, istemcinin girdiği güncel Order Token'ı içerir.
> - Bir emir başka bir protokolle değiştirilirse, o emrin sahipliği o protokole/oturuma geçmiş sayılır. Emri girmiş olan OUCH istemcisi, Order State = 99 (OUCH order ownership lost; OUCH emir sahipliği kaybedildi) olan bir Order Replaced alır. Bundan sonra başka emir güncellemesi alınmaz. "Kaybedilmiş" emirde yapılabilecek tek işlem Cancel by Order ID'dir.

**Tablo 9: Order Replaced Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "U" | Order Replaced Mesajı. |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Replacement Order Token | 9 | 14 | Alpha | |
| Previous Order Token | 23 | 14 | Alpha | |
| Order book ID | 37 | 4 | Numeric | Emir defteri tanımlayıcısı. |
| Side | 41 | 1 | Alpha | Değerler: "B" = Alış emri; "S" = Satış emri; "T" = Açığa satış |
| Order ID | 42 | 8 | Numeric | Yeni emre atanan tanımlayıcı. Numaranın yalnızca emir defteri ve taraf başına benzersiz olduğuna dikkat edin. |
| Quantity | 50 | 8 | Numeric | Defterde şu anda açık olan miktar. |
| Price | 58 | 4 | Price | İşaretli tamsayı fiyat. Ondalık hane sayısı ITCH'teki Order book Directory mesajından alınır. Bu alan güvenliğin kesirlerle işlem görüp görmediğini de belirtir. |
| Time In Force | 62 | 1 | Numeric | Değerler: 0 = Day; 3 = Immediate or Cancel (FaK); 4 = Fill or Kill |
| Open Close | 63 | 1 | Numeric | Hesap için pozisyon güncellemesini tanımlar. Değerler: 0 = Değişiklik yok; 1 = Open; 2 = Close/Net; 4 = Hesap için varsayılan |
| Client/Account | 64 | 16 | Alpha | Aktarım alanı. Not: Hesap bilgisi türev piyasası için bu alanı kullanmalıdır. |
| Order State | 80 | 1 | Numeric | Değerler: 1 = On book; 2 = Not on book; 98 = Paused orders (duraklatılmış emirler); 99 = OUCH order ownership lost |
| Customer Info | 81 | 15 | Alpha | Aktarım alanı. |
| Exchange Info | 96 | 32 | Alpha | Yalnızca ilk 16 bayt kullanılır; ilk 16 bayttan fazlasının kullanılması işlemin reddedilmesine yol açabilir. Not: Hesap bilgisi pay piyasası için bu alanı kullanmalıdır. |
| Pre Trade Quantity | 128 | 8 | Numeric | İşlem öncesi miktar. |
| Display Quantity | 136 | 8 | Numeric | Emir bir rezerv emirse görüntülenen miktar, değilse sıfır. |
| Client Category | 144 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client; 2 = House; 7 = Fund; 9 = Investment Trust; 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company. Not: Client Category türev piyasasında kullanılmaz. |

#### 4.2.4 Order Canceled (Emir İptal Edildi) [s. 21–22]

Canceled mesajı bir emrin iptal edildiğini bildirir. Bu, bir Cancel Order mesajının onayı olabilir veya emrin sistem tarafından iptalinin sonucu olabilir.

> **Not:** Bağlantı kaybı nedeniyle emirler askıya alındığında Order Canceled mesajları gönderilir. Emirler yeniden etkinleştirilemez ancak askıya alınmış bir emrin iptali mümkündür; bu nedenle aynı emir için birden fazla Order Canceled mesajı alınabilir.

**Tablo 10: Order Canceled Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "C" | Order Canceled Mesajı. |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | |
| Order book ID | 23 | 4 | Numeric | Emir defteri tanımlayıcısı. |
| Side | 27 | 1 | Alpha | Değerler: "B" = Alış emri; "S" = Satış emri; "T" = Açığa satış |
| Order ID | 28 | 8 | Numeric | İptal edilen emre atanan tanımlayıcı. Numaranın yalnızca emir defteri ve taraf başına benzersiz olduğuna dikkat edin. |
| Reason | 36 | 1 | Numeric | Sistem değişiklik sebebi değerlerini içerir (aşağıdaki tabloya bakın). |

**`Reason` alanı değerleri** (kaynaktaki değer adları aynen bırakılmıştır; Türkçe açıklamalar çevirmen tarafından eklenmiştir)

| Değer | Ad (kaynak) | Türkçe açıklama |
|---|---|---|
| 1 | Canceled by user / Canceled by Other User | Kullanıcı tarafından / başka kullanıcı tarafından iptal |
| 3 | Trade | İşlem (gerçekleşme) |
| 4 | Inactivate | Pasifleştirme |
| 5 | Replaced by User | Kullanıcı tarafından değiştirildi |
| 6 | New | Yeni |
| 8 | Converted by System | Sistem tarafından dönüştürüldü |
| 9 | Canceled by System | Sistem tarafından iptal |
| 10 | Canceled by Proxy | Vekil (proxy) tarafından iptal |
| 11 | BaitRecalculated | Bait yeniden hesaplandı |
| 12 | Triggered by System | Sistem tarafından tetiklendi |
| 13 | Refreshed by System | Sistem tarafından yenilendi |
| 15 | Canceled by System Limit Change | Sistem limit değişikliği nedeniyle iptal |
| 17 | Linked Leg Canceled | Bağlı bacak iptal edildi |
| 18 | Linked Leg Modified | Bağlı bacak değiştirildi |
| 19 | Expired | Süresi doldu |
| 20 | Canceled Due to ISS | ISS nedeniyle iptal |
| 21 | Inactivated Due to ISS | ISS nedeniyle pasifleştirildi |
| 23 | Inactivated Due to Purge | Purge (temizleme) nedeniyle pasifleştirildi |
| 24 | Inactivated Day Order | Gün emri pasifleştirildi |
| 25 | Inactivated Due to DeList | Kayıttan çıkarma (delist) nedeniyle pasifleştirildi |
| 26 | Inactivated Due to Expiry | Vade sonu nedeniyle pasifleştirildi |
| 27 | Inactivated Due to Outside Limits | Limit dışı nedeniyle pasifleştirildi |
| 28 | Transfer of Ownership | Sahiplik devri |
| 29 | New Inactive | Yeni pasif |
| 30 | Reloaded | Yeniden yüklendi |
| 31 | Reloaded Intraday | Gün içi yeniden yüklendi |
| 34 | Canceled After Auction | Müzayededen (tek fiyat) sonra iptal |
| 35 | Inactivated Due to Outside Price Limits | Fiyat limitleri dışı nedeniyle pasifleştirildi |
| 36 | Activated Due to Outside Limits | Limit dışı nedeniyle etkinleştirildi |
| 37 | Trigger on Session Order Triggered | Seansa bağlı emir tetiklendi |
| 39 | Undisclosed Quantity Order Converted | Gizli miktarlı emir dönüştürüldü |
| 40 | Inactivated Due to Order Value | Emir değeri nedeniyle pasifleştirildi |
| 41 | Canceled by System Delta Protection | Sistem delta koruması nedeniyle iptal |
| 42 | Canceled by System Quantity Protection | Sistem miktar koruması nedeniyle iptal |
| 43 | Internal Crossing Delete | İç eşleşme (crossing) silmesi |
| 44 | Canceled Due to Participant Block on Market | Piyasada katılımcı engeli nedeniyle iptal |
| 45 | Inactivated Due to Participant Block on Market | Piyasada katılımcı engeli nedeniyle pasifleştirildi |
| 46 | Order deleted due to SMP | SMP (Emrimle Eşleşmesin) nedeniyle silindi |
| 47 | Cancelled due to connection termination | Bağlantı sonlanması nedeniyle iptal |
| 52 | Paused | Duraklatıldı |
| 53 | Activated Paused Order | Duraklatılmış emir etkinleştirildi |
| 56 | Linked Leg Activated | Bağlı bacak etkinleştirildi |
| 115 | Deleted: PTRM misc | Silindi: PTRM çeşitli |
| 116 | Deleted: PTRM user limits auto | Silindi: PTRM kullanıcı limitleri (otomatik) |
| 117 | Deleted: PTRM user limits manual | Silindi: PTRM kullanıcı limitleri (manuel) |
| 118 | Deleted: PTRM market limits | Silindi: PTRM piyasa limitleri |
| 119 | Deleted: PTRM investor limits | Silindi: PTRM yatırımcı limitleri |
| 120 | Deleted: PTRM margin breach | Silindi: PTRM teminat aşımı |
| 121 | Deleted: PTRM participant suspension | Silindi: PTRM katılımcı askıya alma |
| 122 | Deleted: PTRM mra suspension | Silindi: PTRM MRA askıya alma |
| 123 | Deleted: PTRM mca suspension | Silindi: PTRM MCA askıya alma |
| 124 | Deleted: PTRM ta suspension | Silindi: PTRM TA askıya alma |
| 125 | Canceled By Ptrm Suspension Product due to Investor Position Value Limit | PTRM ürün askıya alma nedeniyle iptal (yatırımcı pozisyon değeri limiti) |

> **Çeviri notu:** Değer 125'in adı kaynakta iki satıra bölünmüştür ("Canceled By Ptrm Suspension" / "Product due to Investor Position Value Limit"); burada tek ad olarak birleştirilmiştir. Bu tablo, DataStore `ChangeReason` (3.1.4) listesiyle (`datastore-dosya-formatlari.md`) karşılaştırılabilir; DataStore'da 7 = MarketOrderConverted ve 10 = CanceledOnBehalf adları farklı yazılmıştır (OUCH listesinde 7 yok, 10 "Canceled by Proxy").

#### 4.2.5 Order Executed (Emir Gerçekleşti) [s. 22–24]

Bu mesaj kısmi veya tam gerçekleşme olduğunda döner. Kombinasyon emri gerçekleşmesinde her bacak için bir Order Executed mesajı alınır.

**Tablo 11: Order Executed Message**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "E" | Order Executed Mesajı. |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | |
| Order book ID | 23 | 4 | Numeric | Kombinasyon gerçekleşmeleri için gereklidir (her bacak için Order Executed gönderilir). |
| Traded Quantity | 27 | 8 | Numeric | Gerçekleşen miktar. |
| Trade Price | 35 | 4 | Price | İşaretli tamsayı işlem fiyatı. Ondalık hane sayısı ITCH'teki Order book Directory mesajından alınır. Bu alan güvenliğin kesirlerle işlem görüp görmediğini de belirtir. |
| Match ID | 39 | 12 | Numeric | Arka uç tarafından üretilen tanımlayıcı. İşlem mesajı başına benzersizdir. |
| Client Category | 51 | 1 | Numeric | Müşteri tipi. Değerler: 1 = Client; 2 = House; 7 = Fund; 9 = Investment Trust; 10 = Primary Dealer Govt; 11 = Primary Dealer Corp; 12 = Portfolio Mgmt Company. Not: Client Category türev piyasasında kullanılmaz. |
| Reserved | 52 | 16 | | Gelecekte kullanım için ayrılmıştır. |

> **Çeviri notu:** `Match ID` OUCH'ta 12 baytlıktır; ITCH `E` mesajında `Match ID` 8 bayttır (bkz. `bistech-itch-protokol-spesifikasyonu.md`). Kaynaklar arasındaki bu uzunluk farkı belgelerde açıklanmamıştır.

#### 4.2.6 Mass Quote Acknowledgement (Toplu Kotasyon Onayı) [s. 24–25]

Mass Quote Acknowledgement, bir Mass Quote mesajına olumlu yanıt olarak kullanılır. Mass quote mesajındaki her kotasyona ayrı bir mesajla (Mass Quote Acknowledgement VEYA Mass Quote Rejection) yanıt verilmelidir.

Olumlu onaylar için onay mesajı gönderilebilir. `QuoteStatus` alanı kotasyonun durumunu (kabul, güncellendi, iptal edildi, istek dışı güncelleme/iptal) açıklar.

Mass quote içindeki tekil kotasyon kabul edilirse sistem alış ve satış tarafı için iki Mass Quote Acknowledgement mesajı gönderir.

**Tablo 12: Mass Quote Acknowledgement**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "K" | Mass Quote Acknowledgement |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | İstemci tarafından üretilen kotasyon tanımlayıcısı. |
| OrderBookID | 23 | 4 | Numeric | Emir defteri tanımlayıcısı |
| Quantity | 27 | 8 | Numeric | Kalan (leaves) miktar |
| TradedQuantity | 35 | 8 | Numeric | |
| Price | 43 | 4 | Price | MassQuote mesajındaki fiyat. (İstisna: Gerçekleşen fiyat.) |
| Side | 47 | 1 | Alpha | Değerler: "B" = Alış tarafı (bid); "S" = Satış tarafı (offer) |
| QuoteStatus | 48 | 4 | Numeric | Mass quote onayının durumunu belirtir. Geçerli değerler: 0 = Kabul (Accept); 1 = Güncellendi (Updated); 2 = İptal edildi (Canceled); 3 = İstek dışı güncelleme (Unsolicited update); 4 = İstek dışı iptal (Unsolicited cancel); 5 = Gerçekleşti (Traded) |

#### 4.2.7 Mass Quote Rejection (Toplu Kotasyon Reddi) [s. 25]

(Kaynakta bu bölümün numarası yanlışlıkla "4.2.1" olarak yazılmıştır.)

Mass Quote Rejection, bir Mass Quote mesajına olumsuz yanıt olarak kullanılır. Bu mesajın iki kullanımı vardır:
- Mass quote içindeki tekil kotasyon reddedilirse, OrderbookID içeren her kotasyon için tek bir "Mass Quote Rejection" gönderilir.
- Mass quote mesajındaki tüm kotasyonlar reddedilirse, sistem tüm kotasyon isteği için OrderbookID içermeyen yalnızca bir "Mass Quote Rejection" gönderir. Tüm kotasyonlar aşağıdaki nedenlerle reddedilebilir:
  - Duplicate Order Token (yinelenen Order Token)
  - Invalid number of quote (mass quote isteğindeki kotasyon sayısı izin verilen sınırı aşıyor)
  - Invalid Price – Bid & Offer Price are equal for all quotes in mass quote (mass quote'taki tüm kotasyonlarda alış ve satış fiyatı eşit)

**Tablo 13: Mass Quote Rejection**

| Name | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Message Type | 0 | 1 | "R" | Mass Quote Rejection |
| Timestamp – Nanoseconds | 1 | 8 | Timestamp | UNIX zamanı (1970-01-01 00:00:00 UTC'den itibaren nanosaniye sayısı). |
| Order Token | 9 | 14 | Alpha | İstemci tarafından üretilen kotasyon tanımlayıcısı. |
| OrderBookID | 23 | 4 | Numeric | Emir defteri tanımlayıcısı |
| Reject Code | 27 | 4 | Numeric | Mass quote'un reddedilme nedenini belirtir. Ayrıntılar için hata kodu kataloğuna bakın. |

## 5 Appendix A — Kotasyon İş Akışları (Workflows for Quoting) [s. 26–29]

Bu bölümün amacı mass quote seçeneklerinin akışını açıklamaktır. Her akışta sol sütun Quote Issuer (kotasyon veren), sağ sütun Trading System (işlem sistemi) yönündedir; "→" istemciden sisteme, "←" sistemden istemciye gönderilen mesajı gösterir (kaynakta oklar sütun içindedir).

### 5.1 Tüm kotasyonların kabul edildiği Mass Quote onayı

| # | Yön | Açıklama |
|---|---|---|
| 1 | → | 3 girdili bir mass quote gönderilir (MsgType = Q), benzersiz OrderToken |
| 2 | ← | İlk alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 3 | ← | İlk satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 4 | ← | İkinci alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 5 | ← | İkinci satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 6 | ← | Üçüncü alış kotasyonu için olumlu onay (MsgType = K). OrderToken + OrderBookID + Side ile benzersiz |
| 7 | ← | Üçüncü satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |

### 5.2 Bazı kotasyonların kabul edildiği, bazılarının reddedildiği Mass Quote onayı

| # | Yön | Açıklama |
|---|---|---|
| 1 | → | 3 girdili bir mass quote gönderilir (MsgType = Q), benzersiz OrderToken |
| 2 | ← | İlk alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 3 | ← | İlk satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 4 | ← | İkinci kotasyon için ret (MsgType = R). OrderToken + OrderBookID ile benzersiz |
| 5 | ← | Üçüncü alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |
| 6 | ← | Üçüncü satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken + OrderBookID + Side ile benzersiz |

### 5.3 Tüm kotasyonların reddedildiği Mass Quote

| # | Yön | Açıklama |
|---|---|---|
| 1 | → | 3 girdili bir mass quote gönderilir (MsgType = Q), benzersiz OrderToken |
| 2 | ← | Mass quote için ret: OrderBookID içermeyen yalnızca bir emir ret mesajı gönderilir (MsgType = R), benzersiz OrderToken |

### 5.4 Bir mass quote'un değiştirilmesi ve ardından iptal isteği

| # | Yön | Açıklama |
|---|---|---|
| 1 | → | 2 girdili bir mass quote gönderilir (MsgType = Q), OrderToken = Q1 |
| 2 | ← | İlk alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken = Q1, OrderBookID1 ve Side ile benzersiz |
| 3 | ← | İlk satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken = Q1, OrderBookID1 ve Side ile benzersiz |
| 4 | ← | İkinci alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken = Q1, OrderBookID1 ve Side ile benzersiz |
| 5 | ← | İkinci satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken = Q1, OrderBookID2 ve Side ile benzersiz |
| 6 | → | Kotasyon değişikliği (değiştirme için yeni bir mass quote gönderilir): ilk kotasyonun çift tarafı değiştirilir, ikinci kotasyonun bir tarafı değiştirilir (MsgType = Q), OrderToken = Q2. 1. kotasyon (Bid Price = X && Offer Price = Y && Bid Size = W && Offer Size = Z); 2. kotasyon (Bid Price = X && Offer Price = Y && Bid Size = W && Offer Size = 0) |
| 7 | ← | İlk alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 1). OrderToken2, OrderBookID1 ve Side ile benzersiz |
| 8 | ← | İlk satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 1). OrderToken2, OrderBookID1 ve Side ile benzersiz |
| 9 | ← | İkinci alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 1). OrderToken2, OrderBookID2 ve Side ile benzersiz |
| 10 | ← | İkinci satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 1). OrderToken2, OrderBookID2 ve Side ile benzersiz |
| 11 | → | Tekil bir güvenlik için iptal isteği gönderilir: ilk kotasyonun çift tarafı iptal edilir, ikinci kotasyonun bir tarafı iptal edilir (MsgType = Q), OrderToken = Q3. 1. kotasyon (Bid Price = 0 && Offer Price = 0 && Bid Size = 0 && Offer Size = 0); 2. kotasyon (Bid Price = 0 && Offer Price = <<boş>> && Bid Size = 0 && Offer Size = <<boş>>) |
| 12 | ← | İlk alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 2). OrderToken3, OrderBookID1 ve Side ile benzersiz |
| 13 | ← | İlk satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 2). OrderToken3, OrderBookID1 ve Side ile benzersiz |
| 14 | ← | İkinci alış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 2). OrderToken3, OrderBookID2 ve Side ile benzersiz |
| 15 | ← | İkinci satış kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 2). OrderToken3, OrderBookID2 ve Side ile benzersiz |

### 5.5 Mass quote girişinde işlem senaryosu

| # | Yön | Açıklama |
|---|---|---|
| 1 | → | 1 girdili bir mass quote gönderilir (MsgType = Q), benzersiz OrderToken |
| 2 | ← | Alış tarafı kotasyonu için olumlu onay (MsgType = K ve QuoteStatus = 0). OrderToken = Q1, OrderBookID1 ve Side ile benzersiz |
| 3 | ← | Satış tarafı kotasyonu için kısmi/tam gerçekleşme onayı (MsgType = K ve QuoteStatus = 5). Quantity (leavesQty), TradedQuantity, TradedPrice. OrderToken = Q1, OrderBookID1 ve Side ile benzersiz |

> *QuoteStatus = 5 (Traded) olan MassQuoteAck mesajı bir tür onay mesajıdır; bu nedenle QuoteStatus = 0 (accept) olan ek bir MassQuoteAck mesajı olmayacaktır.*

## 6 Appendix B — Kotasyon Matrisi (Quote Matrix) [s. 30]

| İstek tipi | BidPx | BidSize | OfferPx | OfferSize |
|---|---|---|---|---|
| Yeni çift taraflı kotasyon (New two-sided quote) | >0 | >0 | >0 | >0 |
| Yeni tek taraflı (alış) kotasyon | >0 | >0 | 0 | 0 |
| Yeni tek taraflı (satış) kotasyon | 0 | 0 | >0 | >0 |
| Çift taraflı kotasyonu değiştir (Fiyat ve Miktar) | >0 | >0 | >0 | >0 |
| Çift taraflı kotasyonu değiştir (Fiyat) | >0 | 0 | >0 | 0 |
| Çift taraflı kotasyonu değiştir (Miktar) | >0 | >0 | >0 | >0 |
| Tek taraflı (alış) kotasyonu değiştir (Fiyat ve Miktar) | >0 | >0 | >0 | 0 |
| Tek taraflı (alış) kotasyonu değiştir (Fiyat) | >0 | 0 | >0 | 0 |
| Tek taraflı (alış) kotasyonu değiştir (Miktar) | >0 | >0 | >0 | 0 |
| Tek taraflı (satış) kotasyonu değiştir (Fiyat ve Miktar) | >0 | 0 | >0 | >0 |
| Tek taraflı (satış) kotasyonu değiştir (Fiyat) | >0 | 0 | >0 | 0 |
| Tek taraflı (satış) kotasyonu değiştir (Miktar) | >0 | 0 | >0 | >0 |
| Çift taraflı kotasyonu iptal et | 0 | 0 | 0 | 0 |
| Tek taraflı (alış) kotasyonu iptal et | 0 | 0 | >0 | >0 |
| Tek taraflı (satış) kotasyonu iptal et | >0 | >0 | 0 | 0 |

> **Çeviri notu:** Kaynaktaki "Replace two-sided quote (Px)" ve "(Size)" satırlarının değerleri kaynakta olduğu gibi aktarılmıştır; "(Size)" satırı "(Px&Size)" satırıyla aynı değerlere sahiptir ve "tek taraflı (alış/satış) ... (Px)" satırlarında bile hem bir tarafın miktarı 0 gösterilmiştir. Bu tutarlılık sorunları kaynaktan gelir, çeviriyle ilgili değildir; kotasyon kullanılacaksa PDF sayfa 30 doğrulanmalıdır.

---

## Çapraz kontrol (kaynakta yok; çevirenin gözlemi)

- Tablolardaki `(Offset, Uzunluk)` çiftleri PDF metninden regex ile çıkarılan 117 çiftle karşılaştırıldı: PDF'teki hiçbir çift eksik değildir; bu dosyada fazladan yalnızca tipi boş "Reserved" satırları (112/2, 114/8, 52/16) ve Quote Matrix'teki 0 değerleri bulunur.
- OUCH `Order Executed` mesajında `Match ID` 12 bayt, ITCH `E` mesajında 8 bayttır (yukarıdaki not).
- OUCH `Reason` (ChangeReason) listesi, DataStore'daki `ChangeReason` listesiyle büyük ölçüde örtüşür; ayrıntı `kurallar/04-surekli-islem.md` madde 42 notundadır.
