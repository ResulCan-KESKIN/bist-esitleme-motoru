# BIST ITCH Protokol Spesifikasyonu (Türkçe çeviri)

Kaynak: `bistech-itch-protocol-specification.pdf` — "ITCH Protocol Specification, BIST, Version: 2112, 28.02.2025", 30 sayfa (PDF sayfa numarası). Belge "HİZMETE ÖZEL" damgalıdır ve Nasdaq, Inc. veya bağlı kuruluşlarının mülkiyetindedir (Copyright © 2017 Nasdaq, Inc.); yalnızca proje içi kullanım içindir.
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir. Mesaj kodları, alan adları, değerler ve sabitler **çevrilmeden aynen** bırakılmıştır (ör. `Order Book ID`, `State Name`); alan adlarının yanına Türkçe karşılığı parantez içinde eklenmiştir. Offset (bayt konumu), uzunluk ve değer sütunları kaynakla aynıdır. Orijinaldeki "sayfa 25" gibi iç atıflar belgenin kendi sayfa numaralandırmasına göredir; bu dosyada karşılıkları bölüm adıyla verilmiştir.
Doğrulama: Mesaj tablolarındaki 130 alan satırının (Offset, Uzunluk) değerleri PDF'ten çıkarılan değerlerle otomatik karşılaştırıldı; hepsi birebir aynı çıktı. Alan adlarındaki "Order book" / "Order Book" yazım farkı bu çeviride "Order Book" olarak birleştirilmiştir. Metin çevirisi Claude tarafından yapılmış, kaynakla satır satır okunarak karşılaştırılmıştır; sayfa görüntüsüyle karşılaştırma yapılmadı. Kullanıcı doğrulaması: bekliyor.
Not: Bu dosyadaki "Çeviri notu" ve "Örnek veriyle çapraz kontrol" bölümleri kaynakta yoktur; çevirenin eklediği açıklamalardır ve ayrıca işaretlenmiştir.

---

## 1 Değişiklik Özeti (Summary of Changes) [s. 4]

Bu sürüm ile a1983 (4.0.1024) sürümü arasındaki değişiklikler.

| No  | Tarih          | Değişiklik                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Açıklama (Sürüm)     |
| --- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| 1   |                | Order Book Directory mesajından Market ID alanı kaldırıldı (Order Book Directory bölümü).                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                      |
| 2   |                | "4.5.1 Trade Message" içindeki "Order Book ID" alanının offset değeri düzeltildi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Sürüm 2102, 20190520 |
| 3   | 19 Aralık 2022 | "Appendix E, Protocol Flow" bölümü eklendi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Sürüm 2103, 20221219 |
| 4   | 20 Şubat 2023  | Tablo 2: Order Book Directory içindeki "Expiration Date" alanının veri tipi revize edildi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Sürüm 2104, 20230220 |
| 5   | 06 Mart 2024   | Yeni mesaj "Order Book Flush" eklendi (Bölüm 4.4.2.5). "4.5.2 Auction Messages", "4.4.2.4 Order Delete Message" ve "Appendix A, How to Build an Order Book View" bölümleri güncellendi.                                                                                                                                                                                                                                                                                                                                                                              | Sürüm 2105           |
| 6   | 18 Nisan 2024  | "4.2.3 Tick Size Table Entry" bölümünde "Tick Size" değeri "Price" yerine "Numeric" olarak düzeltildi.                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Sürüm 2106           |
| 7   | 11 Eylül 2024  | Yeni mesaj "Short Sell Status" eklendi (Bölüm 4.2.4). "3. ITCH Overview" bölümü güncellendi. (Short Sell Status mesajı Service Release 3.11 ile etkinleştirilir.)                                                                                                                                                                                                                                                                                                                                                                                                    | Sürüm 2107           |
| 8   | 12 Kasım 2024  | "Short Sell Validation" alanının sayılandırması (enumeration) güncellendi (Bölüm 4.2.4; mesaj Service Release 3.11 ile etkinleştirilir).                                                                                                                                                                                                                                                                                                                                                                                                                             | Sürüm 2108           |
| 9   | 13 Ocak 2025   | "4.2.1 Order Book Directory Message" mesajına yeni alan "Ranking Type" eklendi. "4.2.4 Short Sell Status" mesaj alanları güncellendi. "4.4.1 Add Order Messages" mesajından "Order Book Position" alanı, sıralama mantığının değişmesi nedeniyle kaldırıldı. "4.4.1 Add Order Messages" mesajına yeni alanlar "Ranking Time" ve "Ranking Sequence Number" eklendi. "Appendix A, How to Build an Order Book View" ve "Appendix E, Protocol Flow" bölümleri güncellendi. (Yeni sıralama mantığı ve yukarıdaki güncellemeler Service Release 3.12 ile etkinleştirilir.) | Sürüm 2109           |
| 10  | 17 Ocak 2025   | "4.4.1 Add Order Messages" bölümündeki offset değerleri güncellendi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Sürüm 2110           |
| 11  | 13 Şubat 2025  | "Appendix A, How to Build an Order Book View" bölümü güncellendi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Sürüm 2111           |
| 12  | 28 Şubat 2025  | "Appendix A, How to Build an Order Book View" bölümü güncellendi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Sürüm 2112           |

## 2 Kılavuz Hakkında (About the Manual) [s. 5]

Bu belgenin amacı ITCH protokolünü tanımlamaktır.

## 3 ITCH'e Genel Bakış (ITCH Overview) [s. 6]

Genium INET ITCH doğrudan bir veri akışı (direct data feed) ürünüdür. ITCH akışı, otomatik eşleşen piyasa(lar)da gerçekleşen tüm kamuya açık emirleri ve işlemleri gösterir.

ITCH yalnızca çıkış yönlü (outbound) bir piyasa veri akışıdır; protokol emir girişini desteklemez. ITCH'in başlıca veri öğeleri:

- **Emir seviyesinde veri (MBO) ve katılımcı ataması (attribution):** Sistem tüm emir derinliğini standart ITCH biçiminde sağlar. ITCH, bir müşteri emrinin ömrünü (emir gerçekleşmeleri dahil) izlemek için bir dizi emir mesajı kullanır. ITCH mesaj biçimleri, piyasa tarafından kullanılıyorsa piyasa katılımcısı atamasını (attribution) destekler.
- **İşlem (Trade) mesajları:** ITCH, sistemdeki görünmeyen (non-displayable) bir emrin eşleşmesini yansıtmak için bir işlem mesajını destekler.
- **Referans veri:**
  - Order Book Directory mesajları ISIN kodu ve Financial Product gibi temel enstrüman verilerini sağlar.
  - Tick Size Table Entry mesajları emir defterleri için fiyat adımlarını (tick size) iletir.
  - Short Sell Status mesajları bir emir defterinin açığa satış kurallarını gösterir (yalnızca pay piyasası enstrümanları için).
- **Olay kontrolleri:** Order Book State mesajı, alıcılara durum değişikliklerini bildirir.

> **Not:** ITCH bir emir defteri görünümü ve otomatik eşleşen işlemleri sağlar.
> - Eşleştirme mantığının mekanizmalarının ITCH akışı gözlemlenerek çıkarılabileceğini varsaymayın.
> - ITCH özel (private) emirleri yönetmek için kullanılamaz.
> - ITCH, piyasaya bildirilen özel olarak müzakere edilmiş (privately negotiated) işlemleri sağlamaz.

> **Not:** Çoklu para birimli sözleşmelerde işlem hacimleri döviz kuruyla çarpılmaz; çünkü ITCH'te para birimi dönüşümü desteği yoktur. TRL dışındaki sözleşmelerin piyasadaki gerçek hacimleri bu nedenle ITCH kayıtlarından farklı olabilir.

### 3.1 Mimari (Architecture) [s. 7]

ITCH akışı, sıra numaralı bir dizi mesajdan oluşur. Her mesaj, mesaj tipine göre değişken uzunluktadır. Mesajlar MoldUDP64 kullanılarak ikili (binary) kodlanır. ITCH protokolünü oluşturan mesajlar tipik olarak sıralama ve teslim garantilerini üstlenen daha üst seviyeli bir protokolle iletilir.

MoldUDP64, UDP üzerine kurulu hafif bir ağ protokolüdür; dinleyicilere kaybolan paketleri tespit etme ve yeniden isteme mekanizması sağlar. Her mesaj açıkça sıra numaralandırılmıştır. İstemci paket kaybı tespit ederse paketi MoldUDP64 geçidinden (gateway) yeniden isteyebilir; paket o istemciye UDP unicast olarak yeniden gönderilir.

### 3.2 Veri Tipleri (Data Types) [s. 7]

| Tip     | Boyut               | Notlar                                                                                                                                                                                                                                                                                                                                                                                               |
| ------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Numeric | 1, 2, 4 veya 8 bayt | İşaretsiz, big-endian ikili kodlu sayılar. (Not: Taşıma katmanı MoldUDP64 de sayısal değerleri big-endian kullanır.)                                                                                                                                                                                                                                                                                 |
| Alpha   | değişken            | Sola yaslı ve sağdan boşlukla doldurulmuş. Kontrol karakteri içermeyen ISO 8859-1 (Latin-1) kodlu baytlardan oluşur.                                                                                                                                                                                                                                                                                 |
| Price   | 4 bayt              | Fiyatlar işaretli tamsayı alanlardır. Ondalık hane sayısı Order Book Directory mesajında belirtilir. Not: Bit 31'i (en yüksek bit, MIN_INT) 1, diğer tüm bitleri 0 olan bir Price alanı (ondalık -2147483648) **fiyat bulunmadığı** anlamına gelir. Bu değer, Add Order mesajlarında **piyasa emrini** (market order) de temsil eder. Tick Size Table Entry mesajı 8 baytlık bir Price alanı içerir. |

## 4 Mesaj Formatları (Message Formats) [s. 9–25]

ITCH akışı, Genium INET işlem sistemine eklenen, sistemden çıkarılan ve sistemde gerçekleşen emirleri tanımlayan bir mesaj dizisinden oluşur. Ayrıca emir defterlerinin temel referans verilerine, durum değişikliklerine ve işlem durdurmalarına ilişkin mesajlar da içerir.

Tüm mesajlarda ilk alan `Message Type` (1 bayt, Alpha), ikinci alan (çoğu mesajda) `Timestamp – Nanoseconds` (Offset 1, 4 bayt, Numeric) alanıdır. Offset değerleri 0'dan başlar ve mesajın ilk baytına göredir.

### 4.1 Zaman Mesajları (Time Messages) [s. 9]

Bant genişliği verimliliği için zaman damgası (timestamp) iki parçaya ayrılmıştır:

| Zaman damgası parçası    | Mesaj tipi                  | Notlar                                                                                                                                                                |
| ------------------------ | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Seconds (saniye)         | Bağımsız mesaj              | Unix zamanı (1970-01-01 00:00:00 UTC'den itibaren geçen saniye sayısı). En az bir yük (payload) mesajı olan her saniye için bir Timestamp – Second mesajı yayınlanır. |
| Nanoseconds (nanosaniye) | Her mesajın içinde bir alan | Yük mesajının oluşturulduğu anın, en son Timestamp-Seconds mesajından itibaren geçen nanosaniye sayısını yansıtır.                                                    |

#### 4.1.1 Seconds Mesajı [s. 9]

Bu mesaj, en az bir ITCH mesajı üretilen her saniye gönderilir. Mesaj, 1970-01-01 00:00:00 UTC'den itibaren geçen saniye sayısını (Unix zamanı) içerir.

**Tablo 1: Timestamp – Seconds Mesajı**

| Name                      | Offset | Uzunluk | Değer   | Notlar                                                           |
| ------------------------- | ------ | ------- | ------- | ---------------------------------------------------------------- |
| Message Type (Mesaj tipi) | 0      | 1       | "T"     | T – Seconds Mesajı                                               |
| Second (Saniye)           | 1      | 4       | Numeric | Unix zamanı (1970-01-01 00:00:00 UTC'den itibaren saniye sayısı) |

### 4.2 Referans Veri Mesajları (Reference Data Messages) [s. 9–14]

#### 4.2.1 Order Book Directory [s. 9–11]

Her işlem gününün başında, Genium INET işlem sistemindeki durdurulmuş (halted) olanlar dahil tüm aktif enstrümanlar için Order Book Directory mesajları yayınlanır.

> **Not:** Gün içinde, sisteme yeni emir defterleri eklendiğinde bu mesaj tekrar iletilebilir. Mevcut emir defterlerindeki güncellemeler de gün içi Order Book Directory mesajlarıyla gösterilebilir.

**Tablo 2: Order Book Directory** (kaynakta iki sayfaya bölünmüştür)

| Name                                                                          | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------- | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type (Mesaj tipi)                                                     | 0      | 1       | "R"     | Order Book Directory Mesajı                                                                                                                                                                                                                                                                     |
| Timestamp – Nanoseconds                                                       | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                                                                                                                                              |
| Order Book ID (Emir defteri kimliği)                                          | 5      | 4       | Numeric | Bir emir defterinin birincil tanımlayıcısı. Not: Süresi dolmuş Order Book ID değerleri yeni enstrümanlar için yeniden kullanılabilir.                                                                                                                                                           |
| Symbol (Sembol)                                                               | 9      | 32      | Alpha   | Enstrümanın kısa adı.                                                                                                                                                                                                                                                                           |
| Long Name (Uzun ad)                                                           | 41     | 32      | Alpha   | Enstrümanın okunabilir uzun adı.                                                                                                                                                                                                                                                                |
| ISIN                                                                          | 73     | 12      | Alpha   | Enstrümanı tanımlayan ISIN kodu.                                                                                                                                                                                                                                                                |
| Financial Product (Finansal ürün)                                             | 85     | 1       | Numeric | Değerler: 1 = Option, 2 = Forward, 3 = Future, 4 = FRA, 5 = Cash, 6 = Payment, 7 = Exchange Rate, 8 = Interest Rate Swap, 9 = REPO, 10 = Synthetic Box Leg/Reference, 11 = Standard Combination, 12 = Guarantee, 13 = OTC General, 14 = Equity Warrant, 15 = Security Lending, 18 = Certificate |
| Trading Currency (İşlem para birimi)                                          | 86     | 3       | Alpha   | İşlem para birimi.                                                                                                                                                                                                                                                                              |
| Number of decimals in Price (Fiyattaki ondalık hane sayısı)                   | 89     | 2       | Numeric | Bu emir defterinin fiyatında kullanılan ondalık hane sayısı. Not: 256 değeri, enstrümanın kesirlerle işlem gördüğü anlamına gelir (her kesir 1/256).                                                                                                                                            |
| Number of decimals in Nominal Value (Nominal değerdeki ondalık hane sayısı)   | 91     | 2       | Numeric | Nominal değerdeki ondalık hane sayısı.                                                                                                                                                                                                                                                          |
| Odd Lot Size (Küsurat lot büyüklüğü)                                          | 93     | 4       | Numeric | Emir defteri için bir küsurat lotu (odd lot) temsil eden menkul kıymet sayısını gösterir. Not: 0 değeri, bu lot tipinin emir defteri için tanımsız olduğunu gösterir.                                                                                                                           |
| Round Lot Size (Tam lot büyüklüğü)                                            | 97     | 4       | Numeric | İhraç için bir tam lotu (round lot) temsil eden miktarı gösterir.                                                                                                                                                                                                                               |
| Block Lot Size (Blok lot büyüklüğü)                                           | 101    | 4       | Numeric | Emir defteri için bir küsurat lotu temsil eden menkul kıymet sayısını gösterir (kaynakta bu açıklama Odd Lot Size ile aynıdır). Not: 0 değeri, bu lot tipinin emir defteri için tanımsız olduğunu gösterir.                                                                                     |
| Nominal Value (Nominal değer)                                                 | 105    | 8       | Numeric | Nominal değer.                                                                                                                                                                                                                                                                                  |
| Number of Legs (Bacak sayısı)                                                 | 113    | 1       | Numeric | Bacak sayısı. Yalnızca kombinasyon enstrümanları için geçerlidir.                                                                                                                                                                                                                               |
| Underlying Order Book ID (Dayanak emir defteri kimliği)                       | 114    | 4       | Numeric | Dayanak enstrümanın Order Book ID değeri. Yalnızca kombinasyonlar dışındaki türev enstrümanlar için geçerlidir.                                                                                                                                                                                 |
| Strike Price (Kullanım fiyatı)                                                | 118    | 4       | Price   | Yalnızca türev enstrümanlar için geçerlidir.                                                                                                                                                                                                                                                    |
| Expiration Date (Vade tarihi)                                                 | 122    | 4       | Numeric | Emir/enstrüman vade tarihi. Yalnızca türev enstrümanlar için geçerlidir. Geçerli biçim "YYYYMMDD".                                                                                                                                                                                              |
| Number of decimals in Strike Price (Kullanım fiyatındaki ondalık hane sayısı) | 126    | 2       | Numeric | Bu emir defterinin Strike Price alanında kullanılan ondalık hane sayısı. Yalnızca türev enstrümanlar için geçerlidir.                                                                                                                                                                           |
| Put or Call                                                                   | 128    | 1       | Numeric | Opsiyon tipi. Değerler: 1 = Call, 2 = Put. 0 değeri, Put or Call'un emir defteri için tanımsız olduğunu gösterir. Yalnızca türev enstrümanlar için geçerlidir.                                                                                                                                  |
| Ranking Type (Sıralama tipi)                                                  | 129    | 1       | Numeric | Hangi sıralama tipinin kullanılacağını belirtir. 1 = Price Time (fiyat-zaman)                                                                                                                                                                                                                   |

> **Çeviri notu:** Kaynakta Block Lot Size alanının açıklaması "Odd Lot Size" ile aynı cümleyle ("emir defteri için bir küsurat lotu temsil eden menkul kıymet sayısı") verilmiştir; çeviri bu ifadeyi aynen korur. Block Lot Size'ın gerçek anlamı kaynakta ayrıca açıklanmamıştır.

#### 4.2.2 Combination Order Book Leg [s. 12]

Bu mesaj, bir kombinasyon emir defteri ile kombinasyon bacağı olan emir defterlerinden biri arasındaki eşlemeyi sağlar.

Bir kombinasyon enstrümanı (standart veya özel/Tailor-Made), iki veya daha fazla gerçek enstrümandan oluşan sentetik bir enstrümandır. Genium INET'te kombinasyon enstrümanları, içine emir verilebilen normal emir defterleri olarak kurulur.

Kombinasyon enstrümanı ve her bir bacak enstrümanı, ITCH'te Order Book Directory mesajlarıyla temsil edilir. Combination Order Book Leg mesajı, bir kombinasyon emir defteri ile bacak emir defterlerinden biri arasındaki eşlemeyi temsil eder. Her kombinasyon emir defteri için, kombinasyonu oluşturan her bacak başına bir Combination Order Book Leg mesajı üretilir.

Bu mesajın gün içi iletimleri, sisteme yeni kombinasyon emir defterleri eklendiğinde olabilir; bu durum tipik olarak özel (tailor-made) kombinasyonlar için geçerlidir. Mevcut kombinasyon emir defterlerindeki güncellemeler de gün içi Order Book Directory mesajlarıyla temsil edilebilir.

**Tablo 3: Combination Order Book Leg**

| Name                      | Offset | Uzunluk | Değer   | Notlar                                                                                                                                |
| ------------------------- | ------ | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type              | 0      | 1       | "M"     | Combination Order Book Leg Mesajı                                                                                                     |
| Timestamp – Nanoseconds   | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                    |
| Combination Order Book ID | 5      | 4       | Numeric | Bir emir defterinin birincil tanımlayıcısı. NOT: Süresi dolmuş Order Book ID değerleri yeni enstrümanlar için yeniden kullanılabilir. |
| Leg Order Book ID         | 9      | 4       | Numeric | Bacak enstrümanının Order Book ID değeri.                                                                                             |
| Leg Side                  | 13     | 1       | Alpha   | Değerler: B = Tanımlandığı gibi (As Defined), C = Ters yön (Opposite)                                                                 |
| Leg Ratio                 | 14     | 4       | Numeric |                                                                                                                                       |

#### 4.2.3 Tick Size Table Entry [s. 13]

Bu mesaj, bir fiyat aralığı için fiyat adımı (tick size) bilgisini içerir. Aynı Order Book ID değerine sahip tüm Tick Size mesajları birlikte eksiksiz bir fiyat adımı tablosunu (Tick Size Table) oluşturur. Her emir defterinin fiyat adımı tablosunu tanımlayan bir dizi Tick Size Table Entry vardır.

> **Not:** Fiyatlardaki ondalık hane sayısı, bu emir defterine ait Order Book Directory mesajında verilir.

**Tablo 4: Tick Size Table Entry**

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                              |
| ----------------------- | ------ | ------- | ------- | ------------------------------------------------------------------- |
| Message Type            | 0      | 1       | "L"     | Tick Size Mesajı                                                    |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                  |
| Order Book ID           | 5      | 4       | Numeric | Bu girdinin ait olduğu emir defteri.                                |
| Tick Size               | 9      | 8       | Numeric | Verilen fiyat aralığı için fiyat adımı.                             |
| Price From              | 17     | 4       | Price   | Bu girdinin fiyat aralığının başlangıcı.                            |
| Price To                | 21     | 4       | Price   | Bu girdinin fiyat aralığının sonu. Sıfır (0) sonsuz anlamına gelir. |

> **Çeviri notu:** Bölüm 3.2'deki Veri Tipleri tablosu "Tick Size Table Entry mesajı 8 baytlık bir Price alanı içerir" der; ancak Tablo 4'te Price From ve Price To alanları 4 bayt (Price), 8 baytlık alan ise Tick Size'dır (Numeric). Değişiklik özetindeki 6. madde de "Tick Size" tipinin Price'tan Numeric'e düzeltildiğini belirtir. Bu iki ifade arasındaki farkı bu dosyada kaynaktaki hâliyle bırakıyoruz.

#### 4.2.4 Short Sell Status [s. 14]

"V" Short Sell Status mesajı bir emir defterinin açığa satış kurallarını gösterir. Bu "V" mesajı ITCH Referans Veri Mesajlarının bir parçasıdır.

Sistemin başlangıcından önce, açığa satışa izin veriyor olabilecek emir defterleri için "V" mesajı gönderilir. Bir emir defteri "V" mesajında yoksa, istemciler gün başı referans veri mesajları sırasında emir defterinin açığa satış kuralı olmadığını varsaymalıdır.

Gün içinde bir emir defterinin açığa satış kurallarında değişiklik olursa, "V" mesajı o emir defteri için yeniden gönderilir.

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                                                                                                                                           |
| ----------------------- | ------ | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type            | 0      | 1       | "V"     | Short Sell Status Mesajı                                                                                                                                                                                                                                                         |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                                                                                                                               |
| Order Book ID           | 5      | 4       | Numeric | Emir defteri tanımlayıcısı. (Yalnızca Pay Piyasası enstrümanları için geçerlidir.)                                                                                                                                                                                               |
| Short Sale Restriction  | 9      | 1       | Numeric | Açığa satış durumunu ve hangi açığa satış doğrulama kuralının kullanılacağını belirtir. Geçerli değerler: 0 = Kısıtlama yok (açığa satışa fiyat doğrulaması olmadan izin verilir), 1 = Açığa satışa izin verilmez, 2 = Açığa satışa yukarı adım (up-tick) kuralıyla izin verilir |

### 4.3 Olay ve Durum Değişikliği Mesajları (Event and State Change Messages) [s. 15]

#### 4.3.1 System Event Message

Sistem olayı mesaj tipi, bir piyasa veya veri akışı işleyicisi (feed handler) olayını bildirmek için kullanılır.

**Tablo 5: System Event Message**

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                                                                                                                                                    |
| ----------------------- | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type            | 0      | 1       | "S"     | S – System Event Mesajı                                                                                                                                                                                                                                                                   |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                                                                                                                                        |
| Event Code (Olay kodu)  | 5      | 1       | Alpha   | Sistem günlük olarak aşağıdaki olay kodlarını destekler: "O" = Mesajların başlangıcı (Start of Messages). Zaman damgası mesajları dışında, gün başı mesajı bir işlem gününde gönderilen ilk mesajdır. "C" = Mesajların sonu (End of Messages). Bir işlem gününde gönderilen son mesajdır. |

#### 4.3.2 Order Book State Message

Order Book State mesajı, durum değişikliklerini iletir.

**Tablo 6: Order Book State Message**

| Name                    | Offset | Uzunluk | Değer   | Notlar                             |
| ----------------------- | ------ | ------- | ------- | ---------------------------------- |
| Message Type            | 0      | 1       | "O"     | Order Book State Mesajı            |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı. |
| Order Book ID           | 5      | 4       | Numeric | Emir defteri tanımlayıcısı.        |
| State Name (Durum adı)  | 9      | 20      | Alpha   | Emir defteri durumunun adı.        |

> **Çeviri notu:** Spesifikasyon `State Name` alanı için olası durum adlarının listesini vermez. Pay Piyasası seans durumu adları (P_ACILIS_EMIR_TPL, P_ARA vb.) için bkz. `../ekler/ek10.md`, `../ekler/ek11.md` ve `datastore-dosya-formatlari.md` (3.1.13 Session).

### 4.4 Emir Bazlı Mesajlar (Market by Order Messages) [s. 15–23]

> **Not:** Order ID değerleri yalnızca emir defteri ve taraf (yön) başına benzersizdir. Emirleri değiştirirken veya silerken, aynı Order ID birden fazla emir defterinde ve/veya tarafta bulunabileceğinden yalnızca doğru taraf ve emir defterindeki emri güncellemeye dikkat edin.

#### 4.4.1 Add Order Mesajları [s. 16–18]

Add Order mesajı, Genium INET işlem sistemi tarafından yeni bir emrin kabul edildiğini ve görünür (displayable) emir defterine eklendiğini gösterir. Mesaj, Genium INET işlem sisteminin emri izlemek için kullandığı, emir defteri ve taraf başına benzersiz bir Order ID içerir.

> Piyasa emirlerinin nasıl temsil edildiği için "Veri Tipleri" alt bölümüne (Bölüm 3.2, Price tipi) bakın.

Add Order mesajının iki biçimi desteklenir:
- **Add Order — No MPID Attribution:** Genium INET işlem sistemindeki atamasız (unattributed) emirler için üretilir.
- **Add Order — With MPID Attribution:** Sisteme girilen atamalı (attributed) emirler ve kotasyonlar için üretilir.

**Tablo 7: Add Order — No MPID Attribution**

| Name                                             | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                            |
| ------------------------------------------------ | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type                                     | 0      | 1       | "A"     | Add Order Mesajı                                                                                                                                                  |
| Timestamp – Nanoseconds                          | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                |
| Order ID (Emir kimliği)                          | 5      | 8       | Numeric | Yeni emre atanan tanımlayıcı. Not: Numara yalnızca emir defteri ve taraf başına benzersizdir.                                                                     |
| Order Book ID                                    | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                                                       |
| Side (Taraf/Yön)                                 | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                                                                                 |
| Ranking Sequence Number (Sıralama sıra numarası) | 18     | 4       | Numeric | İşlem bazlı, 1'den başlayan ardışık numara. Yalnızca "ranking time" ile birlikte sıralama mantığında kullanılır. Emir defterindeki konumu göstermez.              |
| Quantity (Miktar)                                | 22     | 8       | Numeric | Emrin görünür miktarı. Not: Açıklanmayan (gizli) miktara sahip emirlerde bu alan 0 olarak ayarlanır.                                                              |
| Price (Fiyat)                                    | 30     | 4       | Price   | Yeni emrin görüntülenen fiyatı. Alan işleme notları için "Veri Tipleri" alt bölümüne bakın.                                                                       |
| Order Attributes (Emir nitelikleri)              | 34     | 2       | Numeric | Ek emir nitelikleri. Değerler: 0 = Uygulanamaz (Not applicable), 8192 = Bait/implied (yem/ima edilen) emir. Not: Geçerli tipler piyasa tarafından tanımlanabilir. |
| Lot Type (Lot tipi)                              | 36     | 1       | Numeric | Lot tipi. Değerler: 2 = Round Lot (tam lot)                                                                                                                       |
| Ranking Time (Sıralama zamanı)                   | 37     | 8       | Numeric | Sıralama zaman damgası — nanosaniye. Sıralama mantığı için bkz. Appendix A.                                                                                       |

**Tablo 8: Add Order — With MPID Attribution** (Not: Bu mesaj kullanılmamaktadır; ileride başvurmak üzere spesifikasyonda bırakılmıştır.)

| Name                                          | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                                                                                        |
| --------------------------------------------- | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type                                  | 0      | 1       | "F"     | Add Order Mesajı                                                                                                                                                                                                              |
| Timestamp – Nanoseconds                       | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                                                                            |
| Order ID                                      | 5      | 8       | Numeric | Yeni emre atanan tanımlayıcı. Not: Numara yalnızca emir defteri ve taraf başına benzersizdir.                                                                                                                                 |
| Order Book ID                                 | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                                                                                                                   |
| Side                                          | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                                                                                                                                             |
| Order Book Position (Emir defterindeki konum) | 18     | 4       | Numeric | Emir defteri içindeki sıra. Ayrıntılar için bkz. Appendix A.                                                                                                                                                                  |
| Quantity                                      | 22     | 8       | Numeric | Emrin görünür miktarı. Not: Açıklanmayan miktara sahip emirlerde bu alan 0 olarak ayarlanır.                                                                                                                                  |
| Price                                         | 30     | 4       | Price   | Yeni emrin görüntülenen fiyatı.                                                                                                                                                                                               |
| Order Attributes                              | 34     | 2       | Numeric | Ek emir nitelikleri. Değerler: 0 = Uygulanamaz, 8192 = Bait/implied emir. Not: Geçerli tipler piyasa tarafından tanımlanabilir. Not: Bu alan bir bit haritasıdır (bit map); aynı anda birden fazla değer ayarlanmış olabilir. |
| Lot Type                                      | 36     | 1       | Numeric | Lot tipi. Değerler: 2 = Round Lot                                                                                                                                                                                             |
| Participant ID (Katılımcı kimliği)            | 37     | 7       | Alpha   | Girilen emirle ilişkili piyasa katılımcısı tanımlayıcısı.                                                                                                                                                                     |

#### 4.4.2 Modify Order Mesajları [s. 19–23]

Modify Order mesajları her zaman, güncellemenin uygulandığı Add Order'ın Order ID, Order Book ID ve Side bilgilerini içerir.

Bir emrin şu anda görüntülenen miktarını belirlemek için ITCH aboneleri, Modify mesajında belirtilen miktarı, aynı Order ID'ye sahip Add Order mesajındaki orijinal miktardan düşmelidir. Genium INET işlem sistemi aynı emir için birden fazla Modify Order mesajı gönderebilir ve etkiler kümülatiftir. Bir emrin görüntülenen miktarı sıfıra ulaştığında emir ölmüştür ve emir defterinden çıkarılmalıdır.

##### 4.4.2.1 Order Executed Mesajı

Bu mesaj, emir defterindeki bir emir tamamen veya kısmen gerçekleştiğinde gönderilir.

Eşleşmeye neden olan gelen emir tamamen doldurulamıyorsa, kalan kısım eşleşme gerçekleştikten sonra emir defterine konur.

Aynı emir birden fazla parçada gerçekleştiyse aynı emir için birden fazla Order Executed mesajı alınabilir. Aynı emir üzerindeki birden fazla Order Executed mesajı kümülatiftir.

**Tablo 9: Order Executed Message**

| Name                                   | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                    |
| -------------------------------------- | ------ | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type                           | 0      | 1       | "E"     | Order Executed Mesajı                                                                                                                                     |
| Timestamp – Nanoseconds                | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                        |
| Order ID                               | 5      | 8       | Numeric | Gerçekleşen emirle ilişkili Order ID.                                                                                                                     |
| Order Book ID                          | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                                               |
| Side                                   | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                                                                         |
| Executed Quantity (Gerçekleşen miktar) | 18     | 8       | Numeric | Gerçekleşen miktar.                                                                                                                                       |
| Match ID (Eşleşme kimliği)             | 26     | 8       | Numeric | Sistem tarafından gerçekleşen her eşleşmeye atanır.                                                                                                       |
| Combo Group ID                         | 34     | 4       | Numeric | Kombinasyon emir defteri gerçekleşmelerini ve bileşen emir defterlerindeki işlemleri birlikte gruplamak için kullanılır. Ayrıntılar için bkz. Appendix C. |
| Reserved (Ayrılmış)                    | 38     | 7       |         |                                                                                                                                                           |
| Reserved (Ayrılmış)                    | 45     | 7       |         |                                                                                                                                                           |

##### 4.4.2.2 Order Executed with Price Mesajı

Bu mesaj, emir defterindeki bir emrin ilk görüntülenen fiyattan farklı bir fiyatla tamamen veya kısmen gerçekleştiği nispeten nadir durumda gönderilir.

Eşleşmeye neden olan gelen emir tamamen doldurulamıyorsa, kalan kısım eşleşme gerçekleştikten sonra emir defterine konur.

Aynı emir birden fazla parçada gerçekleştiyse aynı emir için birden fazla Order Executed mesajı alınabilir. Aynı emir üzerindeki birden fazla Order Executed mesajı kümülatiftir. Gerçekleşmeler yazdırılamaz (non-printable) olarak işaretlenmiş olabilir. Bir katılımcı ITCH verisini işlem göstergelerinde (trade ticker) veya hacim hesaplarında kullanmak istiyorsa, çifte sayımı önlemek için non-printable olarak işaretlenmiş mesajları yok sayması önerilir.

> **Not:**
> - Emir defterindeki kombinasyon emirlerinin gerçekleşmeleri her zaman bu mesajla temsil edilir.
> - Gerçekleşen kombinasyon emirlerinin Printable bayrağı "N" olur. Kombinasyonun bacaklarında gerçekleşen işlemler printable olur. Bu, kombinasyon emri ile bacak işlemlerinin çifte sayımını önler. Bacak işlemleri Trade mesajı ile yayınlanır.

**Tablo 10: Order Executed with Price Message**

| Name                                     | Offset | Uzunluk | Değer   | Notlar                                                                                                                                    |
| ---------------------------------------- | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type                             | 0      | 1       | "C"     | Order Executed Mesajı                                                                                                                     |
| Timestamp – Nanoseconds                  | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                        |
| Order ID                                 | 5      | 8       | Numeric | Gerçekleşen emirle ilişkili Order ID.                                                                                                     |
| Order Book ID                            | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                               |
| Side                                     | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                                                         |
| Executed Quantity                        | 18     | 8       | Numeric | Gerçekleşen miktar.                                                                                                                       |
| Match ID                                 | 26     | 8       | Numeric | Sistem tarafından gerçekleşen her eşleşmeye atanır.                                                                                       |
| Combo Group ID                           | 34     | 4       | Numeric | Kombinasyon emir defteri gerçekleşmelerini ve bileşen emir defterlerindeki işlemleri birlikte gruplamak için kullanılır. Bkz. Appendix C. |
| Reserved                                 | 38     | 7       |         |                                                                                                                                           |
| Reserved                                 | 45     | 7       |         |                                                                                                                                           |
| Trade Price (İşlem fiyatı)               | 52     | 4       | Price   |                                                                                                                                           |
| Occurred at Cross (Cross'ta gerçekleşti) | 56     | 1       | Alpha   | Değerler: "Y" = Evet, işlem cross'ta (çapraz/kapanış-açılış eşleşmesinde) gerçekleşti; "N" = Hayır, işlem sürekli piyasada gerçekleşti    |
| Printable (Yazdırılabilir)               | 57     | 1       | Alpha   | İşlemin işlem göstergelerine ve hacim hesaplarına dahil edilip edilmeyeceğini belirtir. Değerler: "N" = non-printable, "Y" = printable    |

##### 4.4.2.3 Order Replace Mesajı

> **Not:** Order Replace mesajı kullanılmamaktadır; ileride başvurmak üzere spesifikasyonda bırakılmıştır.

Mevcut bir emrin değiştirilmesi (replace), bir Order Delete mesajını takiben bir Order Add mesajıyla temsil edilir, ancak orijinal Order ID aynı kalır.

Bu mesaj, emir defterindeki bir emir iptal-değiştirme (cancel-replace) yapıldığında gönderilir. Orijinal emirden kalan miktara artık erişilemez ve silinmelidir. Taraf (Side) ve Order Book ID, orijinal emirdekiyle aynı kalır.

**Tablo 11: Order Replace Message**

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                                                                                                                                                                              |
| ----------------------- | ------ | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type            | 0      | 1       | "U"     | Order Replace Mesajı                                                                                                                                                                                                |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                                                                                                  |
| Order ID                | 5      | 8       | Numeric | Değiştirilen emrin orijinal emir tanımlayıcısı. Notlar: Order ID yalnızca emir defteri ve taraf başına benzersizdir. Emir değiştirildiğinde Order ID değişmez.                                                      |
| Order Book ID           | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                                                                                                         |
| Side                    | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                                                                                                                                   |
| New Order Book Position | 18     | 4       | Numeric | Emir defterindeki yeni sıra. Ayrıntılar için bkz. Appendix A.                                                                                                                                                       |
| Quantity                | 22     | 8       | Numeric | Emrin yeni görünür miktarı.                                                                                                                                                                                         |
| Price                   | 30     | 4       | Price   | Emrin yeni fiyatı.                                                                                                                                                                                                  |
| Order Attributes        | 34     | 2       | Numeric | Ek emir nitelikleri. Değerler: 0 = Uygulanamaz, 8192 = Bait/implied emir. Not: Geçerli tipler piyasa tarafından tanımlanabilir. Not: Bu alan bir bit haritasıdır; aynı anda birden fazla değer ayarlanmış olabilir. |

##### 4.4.2.4 Order Delete Mesajı

Bu mesaj, emir defterindeki bir emir silindiğinde gönderilir. Kalan miktar kalmayacağı için emir emir defterinden çıkarılmalıdır.

Normalde bir emir tamamen gerçekleştiğinde Order Delete mesajı gönderilmez. Alıcının, aldığı her Order Executed mesajında kalan miktarı yeniden hesaplayarak tüm emirlerdeki kalan miktarı izlemesi gerekir. Kalan miktar 0'a ulaştığında emirler emir defterinden çıkarılmalıdır.

**Tablo 12: Order Delete Message**

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                                                                       |
| ----------------------- | ------ | ------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| Message Type            | 0      | 1       | "D"     | Order Delete Mesajı                                                                                          |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                           |
| Order ID                | 5      | 8       | Numeric | Silinen emrin orijinal emir tanımlayıcısı. Not: Order ID yalnızca emir defteri ve taraf başına benzersizdir. |
| Order Book ID           | 13     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                  |
| Side                    | 17     | 1       | Alpha   | "B" = alış emri, "S" = satış emri                                                                            |

##### 4.4.2.5 Order Book Flush Mesajı

Bu mesaj, bir emir defteri boşaltıldığında (flush) gönderilir. Kalan tüm emirlere artık erişilemez ve bunlar emir defterinden çıkarılmalıdır.

**Tablo 13: Order Book Flush Message**

| Name                    | Offset | Uzunluk | Değer     | Notlar                             |
| ----------------------- | ------ | ------- | --------- | ---------------------------------- |
| Message Type            | 0      | 1       | "Y"       | Order Book Flush Mesajı            |
| Timestamp – Nanoseconds | 1      | 4       | Timestamp | Zaman damgasının nanosaniye kısmı. |
| Order Book ID           | 5      | 4       | Integer   | Emir defteri tanımlayıcısı.        |

### 4.5 İşlem Mesajları (Trade Messages) [s. 24–25]

#### 4.5.1 Trade Mesajı

Trade mesajı, görünmeyen (non-displayable) emir tiplerini içeren normal eşleşme olayları için gerçekleşme ayrıntılarını sağlamak üzere tasarlanmıştır. Bu mesaj ayrıca tekil cross (çapraz) işlemlerini yayınlamak için de kullanılır.

Görünmeyen bir emir ilk alındığında Add Order mesajı üretilmediğinden, Order Executed mesajı tüm eşleşmeler için kullanılamaz. Trade mesajı, defterdeki görünmeyen bir emir için bir eşleşmeyi bildirmek için kullanılır.

Aynı emir birden fazla parçada gerçekleştiyse aynı emir için birden fazla Trade mesajı alınabilir. Aynı emir için Trade mesajları kümülatiftir.

Trade mesajları, işlem göstergelerine ve hacim ile diğer piyasa istatistiklerine dahil edilmelidir. Ancak Trade mesajları görüntülenen defteri etkilemediğinden, yalnızca emir defteri görünümünü kurmak ve izlemek isteyen katılımcılar bunları yok sayabilir.

**Tablo 14: Trade Message**

| Name                    | Offset | Uzunluk | Değer   | Notlar                                                                                                                                    |
| ----------------------- | ------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Message Type            | 0      | 1       | "P"     | Trade Mesajı                                                                                                                              |
| Timestamp – Nanoseconds | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.                                                                                                        |
| Match ID                | 5      | 8       | Numeric | Sistem tarafından gerçekleşen her eşleşmeye atanır.                                                                                       |
| Combo Group ID          | 13     | 4       | Numeric | Kombinasyon emir defteri gerçekleşmelerini ve bileşen emir defterlerindeki işlemleri birlikte gruplamak için kullanılır. Bkz. Appendix C. |
| Side                    | 17     | 1       | Alpha   | Eşleşen, defterdeki görünmeyen emrin tipi. "B" = alış emri, "S" = satış emri. Anonim piyasalarda boşluk (space) olarak ayarlanır.         |
| Quantity                | 18     | 8       | Numeric | Bu gerçekleşmede eşleşen miktar.                                                                                                          |
| Order Book ID           | 26     | 4       | Numeric | Emir defteri tanımlayıcısı.                                                                                                               |
| Trade Price             | 30     | 4       | Price   |                                                                                                                                           |
| Reserved                | 34     | 7       |         |                                                                                                                                           |
| Reserved                | 41     | 7       |         |                                                                                                                                           |
| Printable               | 48     | 1       | Alpha   | İşlemin işlem göstergelerine ve hacim hesaplarına dahil edilip edilmeyeceğini belirtir. Değerler: "N" = non-printable, "Y" = printable    |
| Occurred at Cross       | 49     | 1       | Alpha   | Değerler: "Y" = Evet, işlem cross'ta gerçekleşti; "N" = Hayır, işlem sürekli piyasada gerçekleşti                                         |

#### 4.5.2 Müzayede (Auction) Mesajları

Müzayedeler (auction) sırasında emir bazlı veri yayını yapılandırmayla devre dışı bırakılabilir. Bu durumlarda, ilgili emir defterindeki mevcut her emir, müzayededen hemen önce bir "Order Book Flush Message" ile emir defterinden çıkarılmalıdır.

> **Not:** Bu emirlerin sahipleri bunu emir iptali olarak yorumlamamalıdır. Emirlerinizin durumunu belirlemek için özel (private) emir akışını kullanın.

##### 4.5.2.1 Equilibrium Price Update (Denge Fiyatı Güncellemesi)

Bu mesaj müzayedeler gerçekleşirken kullanılır. Mesaj, denge fiyatındaki (equilibrium price) değişiklikleri sağlar.

Herhangi bir Price alanında bit 31 (en yüksek bit, MIN_INT) 1 ve diğer tüm bitler 0 ise (ondalık -2147483648), bu fiyatın mevcut olmadığı anlamına gelir.

**Tablo 15: Equilibrium Price Update**

| Name                                        | Offset | Uzunluk | Değer   | Notlar                                    |
| ------------------------------------------- | ------ | ------- | ------- | ----------------------------------------- |
| Message Type                                | 0      | 1       | "Z"     | Equilibrium Price Update Mesajı           |
| Timestamp – Nanoseconds                     | 1      | 4       | Numeric | Zaman damgasının nanosaniye kısmı.        |
| Order Book ID                               | 5      | 4       | Numeric | Emir defteri kimliği.                     |
| Available Bid Quantity at Equilibrium Price | 9      | 8       | Numeric | Denge fiyatında alış tarafındaki miktar.  |
| Available Ask Quantity at Equilibrium Price | 17     | 8       | Numeric | Denge fiyatında satış tarafındaki miktar. |
| Equilibrium Price                           | 25     | 4       | Price   | Denge fiyatı.                             |
| Best Bid Price                              | 29     | 4       | Price   | En iyi alış fiyatı.                       |
| Best Ask Price                              | 33     | 4       | Price   | En iyi satış fiyatı.                      |
| Best Bid Quantity                           | 37     | 8       | Numeric | En iyi alış miktarı.                      |
| Best Ask Quantity                           | 45     | 8       | Numeric | En iyi satış miktarı.                     |

## Appendix A — Emir Defteri Görünümü Nasıl Kurulur (How to Build an Order Book View) [s. 26]

ITCH mesaj akışından emir defteri görünümü kurmak için gereken bilgi Add Order mesajlarında ve Modify Order mesajlarında bulunur. Bu mesajlar:

- "A" Add Order – No MPID Attribution
- "F" Add Order – MPID Attribution (BIST piyasaları için geçerli değildir)
- "E" Order Executed
- "C" Order Executed with Price
- "U" Order Replace (BIST piyasaları için geçerli değildir)
- "D" Order Delete
- "Y" Order Book Flush

İki Add Order mesaj çeşidinin amacı emri deftere eklemektir.

Order Book Directory ("R") mesajında sıralama tipi (ranking type) "Price Time" olduğunda emirler aşağıdaki 3 parametre kullanılarak sıralanır. (Şu anda tüm BIST Pay ve Türev Piyasası enstrümanlarının sıralama tipi Price Time'dır.)

1. Price (Fiyat)
2. Ranking Time (Sıralama zamanı)
3. Ranking Sequence Number (Sıralama sıra numarası)

Alış/satış tarafı emirleri için sıralama mantığı aşağıdaki adımlardan oluşur:

1. **Alış tarafı emirlerinde** ilk adım olarak "price" kontrol edilir; fiyat daha yüksekse emrin sırası önceliklidir. **Satış tarafı emirlerinde** ilk adım olarak "price" kontrol edilir; fiyat daha düşükse emrin sırası önceliklidir.
2. İki emrin fiyatı birbirine eşitse "ranking time" kontrol edilir; sıralama zamanı daha erkense emrin sırası önceliklidir.
3. İki emrin fiyatı ve sıralama zamanı birbirine eşitse "ranking sequence number" kontrol edilir; sıralama sıra numarası daha küçükse emrin sırası önceliklidir.

Bir Order Replace için emir önceki konumundan çıkarılmalı ve New Order Book Position konumuna eklenmelidir. Mevcut bir konuma eklenen emir, o konumdaki emri (ve altındaki tüm emirleri de) bir aşağı kaydırır. Silinen veya tamamen gerçekleşen bir emir, altındaki mevcut emirlerin "boşluğu" doldurmak için bir adım yukarı kaymasına neden olur.

- Order Executed (with Price) mesajı kısmi veya tam gerçekleşmeyi bildirir. Emir miktarı, Order Executed mesajındaki miktar kadar azaltılmalıdır.
- Order Replace mesajı emrin değiştirildiğini bildirir. Mevcut sıralama bu süreçte kaybedilebilir veya kaybedilmeyebilir. Order Book Position yeni sıralamayı gösterir.
- Order Delete mesajı, alıcıya ilgili emri kaldırmasını söyler.
- Order Book Flush mesajı, alıcıya ilgili emir defterindeki tüm emirleri kaldırmasını söyler.

## Appendix B — İşlem Göstergesi (Trade Ticker) Nasıl Kurulur [s. 27]

İşlem göstergesi şu mesajlara dayanır:

- Order Executed
- Order Executed with Price
- Trade

> **Not:**
> - Çifte kayıt (double booking) oluşmasını önlemek için non-printable olarak işaretlenmiş Trade ve Order Executed with Price mesajları hariç tutulur.
> - Bildirilen (reported) işlemler ITCH'e dahil değildir.

## Appendix C — Kombinasyon Emir Defterlerinde İşlemler [s. 28]

Bir kombinasyon (Combination) emri gerçekleştiğinde, kombinasyonun tüm bacaklarında da işlemler oluşur. Kombinasyon enstrümanını ve bileşenlerini öğrenmek için Combination Order Book Directory mesajı sorgulanmalıdır.

- **Kombinasyon–kombinasyon gerçekleşmelerinin (Combo vs. Combo) iletişimi:**
  - Kombinasyon emir defteri için Printable bayrağı N olan Order Executed with Price mesajı (çifte sayımı önlemek için).
  - Bileşen emir defterlerinde Trade mesajları.
- **Kombinasyon–tekil (Combo vs. Outright) gerçekleşmelerinin iletişimi:**
  - Bileşen emir defterleri için Order Executed ve/veya Order Executed with Price mesajları.
  - Kombinasyon emir defterinde Trade mesajı; Printable bayrağı N (çifte sayımı önlemek için).
- Kombinasyon emir defteri gerçekleşmesi ile bileşen emir defteri gerçekleşmelerinin Match ID değerleri farklıdır, ancak Combo Group ID değerleri aynıdır. Bir kombinasyon gerçekleşmesine ait Order Executed ve Trade mesajlarını birlikte gruplamak için Combo Group ID alanı kullanılmalıdır. Not: Combo Group ID alanının zaman içinde benzersiz olduğu varsayılmamalıdır.

## Appendix D — Rezerv Emir Eşleşmesi (Reserve Order Matching) [s. 29]

Bir rezerv emir bir veya birkaç kez eşleştiğinde, aşağıdaki senaryolar için gönderilen mesajlar şunlardır:

| Senaryo                                                                 | Mesaj                                                                                     |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Rezerv emir tamamen doldu — hem görünür hem gizli miktara karşı eşleşme | **E** — rezerv emrin görünür miktarına karşı eşleşen miktarla                             |
|                                                                         | **P** — rezerv emrin gizli miktarına karşı eşleşen miktarla                               |
| Rezerv emir tamamen dolmadı — yalnızca gizli miktara karşı eşleşme      | **D** — rezerv emrin görünür miktarını emir defterinden kaldırır                          |
|                                                                         | **P** — toplam eşleşen miktarla (eşleşme yalnızca gizli miktara karşı gerçekleştiği için) |
|                                                                         | **A** — görünür miktarı emir defterine yeniden ekler                                      |

> **Not:** Rezerv emir, aynı zamanda Iceberg emri olarak da bilinir.

## Appendix E — Protokol Akışı (Protocol Flow) [s. 30]

Günlük ITCH veri akışının özeti:

İstemciler, ITCH IP/port(lar)ını kullanarak (birincil ve ikincil veri akışlarında) multicast grubuna katıldıktan sonra emir seviyesindeki veri, işlem mesajları, referans veri ve olay mesajları gibi ITCH veri akışını dinlemeye başlayabilir. ITCH akışı, sıra numaralı bir dizi mesajdan oluşur. Her mesaj açıkça sıra numaralandırılmıştır ve mesaj tipine göre değişken uzunluktadır. Mesajlar MoldUDP64 kullanılarak ikili kodlanır.

GLIMPSE (SoupBinTCP ile ikili kodlanmış) ve REWINDER (MoldUDP64 ile ikili kodlanmış) servisleri, geç katılım (late join) veya veri boşluğundan kurtarma işlemleri için ITCH veri akışının parçasıdır. SoupBinTCP ve MoldUDP64 hakkında daha fazla bilgi için lütfen ek spesifikasyonlara bakın.

REWINDER veya GLIMPSE servisleri kullanılmadan önce, ITCH'te kurtarma ve/veya geç katılım sorunlarına yönelik ilk adım olarak istemciler çalışıyor olmalı ve ITCH gerçek zamanlı veri akışını sürekli dinliyor olmalıdır.

Bir paket (belirli bir mesaj veya mesaj grubu) kaybı tespit edilirse ve ikincil veri akışından sağlanamıyorsa, istemci o paketi REWINDER sunucusundan yeniden isteyebilir; mesajlar o istemciye UDP unicast olarak yeniden gönderilir. Yeniden oynatma (rewind) sırasında UDP unicast mesajı 1440 bayt uzunluğunda paketlenir. Bu nedenle, yeniden oynatılan mesajların boyutu bu sınırı aşarsa, kalan mesajlar için rewinder servisine yeni istekler gönderilmelidir. GLIMPSE, emir defterlerinin mevcut durumunun anlık görüntüsünü (snapshot) sağlar. GLIMPSE, gerçek zamanlı ITCH akışıyla hızlıca senkronize olmak için kullanılabilir. GLIMPSE anlık görüntüsünün sonunda istemciler, gerçek zamanlı ITCH akışını GLIMPSE anlık görüntüsünde belirtilen sıra numarasından itibaren dinlemeye devam etmelidir.

GLIMPSE ve REWINDER servisleri, ITCH protokolüyle aynı mesaj biçimlerini kullanır.

Şema (kaynaktaki şekil): GLIMPSE — SoupBinTCP üzerinden anlık görüntü isteği (Snapshot Request) ve yanıtı (Snapshot Response); ITCH — MoldUDP64 üzerinden istemcilere (CLIENTS) akış; REWINDER — MoldUDP64 üzerinden paket isteği (Packet Request) ve istenen paket (Requested Packet).

---

## Örnek veriyle çapraz kontrol (kaynakta yok; çevirenin gözlemi)

`veri/itch/2018-10-08/` altındaki örnek veri (TXT ve ikili `.VRD`) bu spesifikasyonla karşılaştırılmıştır; ikili mesajlar alan alan çözülüp TXT ile eşleştirilmiştir (5.615.765 mesaj, fark 0). Ayrıntılar ve sonuçlar için bkz. `itch-ornek-veri-dogrulama.md`. Tablo, ilk satırlardan örneklerdir.

| TXT satır tipi                                                                                  | Spesifikasyondaki karşılığı                           | Gözlem                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `S,<zaman>,O`                                                                                   | System Event Message (`S`), Event Code `O` (gün başı) | Dosyanın ilk mesajı olarak görünüyor.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `R,<zaman>,70616,ACSEL.E,<uzun ad>,<ISIN>,5,TRY,3,0,0,1,0,1,0,5080,0,19881130,3,0` | Order Book Directory (`R`)                            | Sıra, tablo 2 ile uyumlu: Order Book ID = 70616; Symbol = ACSEL.E; Long Name; ISIN; Financial Product = 5 (Cash); Trading Currency = TRY; ondalık (fiyat) = 3; ondalık (nominal) = 0; Odd Lot = 0; Round Lot = 1; Block Lot = 0; Nominal Value = 1; Number of Legs = 0; Underlying Order Book ID = 5080; Strike Price = 0; Expiration Date = 19881130; ondalık (strike) = 3; Put or Call = 0. **Ranking Type alanı 2018 verisinde yok** (2025 sürümünde eklenmiş). |
| `L,<zaman>,ACSEL.E(70616),10,10,19999`                                                          | Tick Size Table Entry (`L`)                           | Tick Size = 10 (ondalık 3 ile 0,010), Price From = 10 (0,010), Price To = 19999 (19,999). Sonraki satırlar sırasıyla 20 → 20,000–49,999; 50 → 50,000–99,999; 100 → 100,000 ve üzeri (`Price To` = 999999999).                                                                                                                                                                                                                                                      |
| `T,1538948234` | Timestamp – Seconds (`T`) | Unix saniyesi; ikili karşılığı `00 05 54 5B BA 7C 8A`. |

Doğrulanmış fark: 2018 verisinde `R` mesajı 129 bayttır (2112: 130; `Ranking Type` yok) ve `A` mesajı 37 bayttır (2112: 45; offset 18'de `Order Book Position`, `Ranking Time` yok). `Short Sell Status` (`V`) ve `Order Book Flush` (`Y`) mesajları 2018 verisinde yoktur. Diğer mesaj tiplerinin (`T`, `S`, `L`, `O`, `E`, `D`, `P`, `Z`) uzunlukları ve alan konumları bu çevirideki tablolarla aynıdır.
