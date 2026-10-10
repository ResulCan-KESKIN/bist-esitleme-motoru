# ITCH
Kaynak: Pay Piyasası Prosedürü 5.7 Pay Piyasasında Kullanılan Protokoller (s. 96) ve 5.7.4 ITCH (s. 97); BIST ITCH Protocol Specification, Version 2112, 28.02.2025: Türkçe çevirisi `../veri/bistech-itch-protokol-spesifikasyonu.md` (s. 4–30: veri tipleri, tüm mesaj formatları, Appendix A, B, C, D, E). Spesifikasyon içeriği (alan tabloları) bu dosyada tekrarlanmaz; mesaj alanlarının Offset/Uzunluk değerleri için çeviri dosyasına bakılır. Sayfa numaraları PDF sayfa numarasıdır. Prosedürde ITCH için başka madde yoktur. MoldUDP64 ve SoupBinTCP taşıma katmanı belgeleri: `../veri/moldudp64-protokol-spesifikasyonu.md`, `../veri/soupbintcp-protokol-spesifikasyonu.md`. Örnek veri (08.10.2018) ile yapılan doğrulamalar: `../veri/itch-ornek-veri-dogrulama.md`.
İlgili kod: ITCH ayrıştırıcı (MoldUDP64 paketi → mesaj), zaman damgası birleştirme, emir defteri yeniden kurucu, işlem (trade ticker) üretici, seans durumu (Order Book State) izleyici, eşleştirme motorunun yeniden oynatma girdisi

## Kurallar

### A. Prosedürdeki tanım (5.7.4)
1. Pay Piyasasında BISTECH İşlem Platformu'ndaki PP Alım Satım Sistemi'ne erişim için kullanılan protokoller: İşlem Terminalleri (TW, Omnet API), FixAPI, OUCH ve ITCH'tir. [5.7, s. 96]
2. ITCH, emir defteri içinde oluşan tüm kademelerde meydana gelen tüm değişiklikleri yansıtmaya yönelik, hızlı ve yoğun veri akışı sağlayan bir veri yayın protokolüdür. [5.7.4, s. 97]
3. ITCH, emir defterine ilişkin verilere çok düşük gecikme (latency) değerleriyle erişim sağlar; emir defterine ait tüm emir, işlem, iptal ve değişiklik bilgilerine hızlı erişim talep eden katılımcılar tarafından kullanılır. [5.7.4, s. 97]
4. BISTECH sisteminde her üyenin dört gruba (Partition) bağlı işlem sıralarının piyasa bilgilerine ITCH üzerinden erişebilmesi için en az dört ITCH oturumunun kurulması zorunludur. [5.7.4, s. 97]

### B. Protokolün kapsamı ve taşıma katmanı (Spesifikasyon bölüm 3)
5. ITCH yalnızca çıkış yönlü bir piyasa veri akışıdır; protokol emir girişini desteklemez. [Spesifikasyon 3]
6. ITCH, otomatik eşleşen piyasa(lar)da gerçekleşen tüm kamuya açık emirleri ve işlemleri gösterir. [Spesifikasyon 3]
7. ITCH bir emir defteri görünümü ve otomatik eşleşen işlemleri sağlar; eşleştirme mantığının mekanizmalarının ITCH akışı gözlemlenerek çıkarılabileceği varsayılmaz. [Spesifikasyon 3]
8. ITCH özel (private) emirleri yönetmek için kullanılamaz ve piyasaya bildirilen özel olarak müzakere edilmiş işlemleri sağlamaz; bildirilen (reported) işlemler ITCH'e dâhil değildir. [Spesifikasyon 3 ve Appendix B]
9. Çoklu para birimli sözleşmelerde işlem hacimleri döviz kuruyla çarpılmaz; ITCH'te para birimi dönüşümü yoktur. [Spesifikasyon 3]
10. ITCH akışı sıra numaralı mesajlardan oluşur; her mesaj mesaj tipine göre değişken uzunluktadır; mesajlar MoldUDP64 kullanılarak ikili (binary) kodlanır. [Spesifikasyon 3.1 ve Appendix E]
11. Sayısal (Numeric) alanlar 1, 2, 4 veya 8 baytlık işaretsiz big-endian ikili sayılardır; taşıma katmanı MoldUDP64 de sayısal değerleri big-endian kullanır. [Spesifikasyon 3.2]
12. Alpha alanlar sola yaslı ve sağdan boşlukla doldurulmuş, kontrol karakteri içermeyen ISO 8859-1 (Latin-1) baytlardır. [Spesifikasyon 3.2]
13. Price alanı 4 baytlık işaretli tamsayıdır; ondalık hane sayısı ilgili emir defterinin Order Book Directory (`R`) mesajındaki `Number of decimals in Price` alanından alınır. `Number of decimals in Price` değeri 256 ise enstrüman kesirlerle işlem görür (her kesir 1/256). [Spesifikasyon 3.2 ve Tablo 2]
14. Bit 31'i 1, diğer tüm bitleri 0 olan Price değeri (-2147483648, MIN_INT) fiyat bulunmadığı anlamına gelir; Add Order mesajlarında aynı değer piyasa emrini temsil eder. [Spesifikasyon 3.2 ve 4.5.2.1]

### C. Zaman damgası (4.1)
15. Zaman damgası iki parçadır: bağımsız `T` (Timestamp – Seconds) mesajındaki Unix saniyesi ve her mesajın içindeki `Timestamp – Nanoseconds` alanı. [Spesifikasyon 4.1]
16. Her `T` mesajı, en az bir yük mesajı üretilen saniye için gönderilir; mesajın zamanı, en son `T` mesajındaki saniyeden itibaren geçen nanosaniye sayısıyla yorumlanır. [Spesifikasyon 4.1]
17. Zaman damgası saniyesi, 1970-01-01 00:00:00 UTC'den itibaren geçen saniyedir (Unix zamanı). [Spesifikasyon 4.1.1]

### D. Mesaj kataloğu
Alan Offset/Uzunluk değerleri için `../veri/bistech-itch-protokol-spesifikasyonu.md` kullanılır. Toplam uzunluklar "son alanın offset + uzunluk" toplamından hesaplanmıştır (spesifikasyon toplam uzunluğu ayrıca yazmaz).

| Tip | Mesaj | Toplam uzunluk (bayt) | Kullanım | Spesifikasyon |
|---|---|---|---|---|
| `T` | Timestamp – Seconds | 5 | Saniye zamanı | 4.1.1 |
| `R` | Order Book Directory | 130 | Enstrüman tanımı; gün başı ve gün içi | 4.2.1 |
| `M` | Combination Order Book Leg | 18 | Kombinasyon bacağı | 4.2.2 |
| `L` | Tick Size Table Entry | 25 | Fiyat adımı tablosu girdisi | 4.2.3 |
| `V` | Short Sell Status | 10 | Açığa satış kuralı | 4.2.4 |
| `S` | System Event | 6 | Gün başı/sonu olayı | 4.3.1 |
| `O` | Order Book State | 29 | Emir defteri durumu | 4.3.2 |
| `A` | Add Order (No MPID) | 45 | Emir ekleme | 4.4.1 |
| `F` | Add Order (MPID) | 44 | Kullanılmıyor | 4.4.1 |
| `E` | Order Executed | 52 | Emir gerçekleşmesi | 4.4.2.1 |
| `C` | Order Executed with Price | 58 | Farklı fiyattan emir gerçekleşmesi | 4.4.2.2 |
| `U` | Order Replace | 36 | Kullanılmıyor | 4.4.2.3 |
| `D` | Order Delete | 18 | Emir silme | 4.4.2.4 |
| `Y` | Order Book Flush | 9 | Emir defterini boşaltma | 4.4.2.5 |
| `P` | Trade | 50 | Görünmeyen emirlerle eşleşme | 4.5.1 |
| `Z` | Equilibrium Price Update | 53 | Müzayede denge fiyatı | 4.5.2.1 |

18. `F` (Add Order With MPID Attribution) mesajı kullanılmaz; ileride başvurmak üzere spesifikasyonda bırakılmıştır. [Spesifikasyon Tablo 8]
19. `U` (Order Replace) mesajı kullanılmaz; mevcut bir emrin değiştirilmesi bir Order Delete mesajını takiben bir Order Add mesajıyla temsil edilir ve orijinal Order ID aynı kalır. [Spesifikasyon 4.4.2.3]
20. Order Replace ve MPID'li Add Order mesajları BIST piyasaları için geçerli değildir. [Spesifikasyon Appendix A]

### E. Referans veri mesajları (4.2)
21. Her işlem gününün başında, durdurulmuş olanlar dâhil tüm aktif enstrümanlar için Order Book Directory (`R`) mesajları yayınlanır. [Spesifikasyon 4.2.1]
22. Gün içinde yeni emir defterleri eklendiğinde veya mevcut emir defterleri güncellendiğinde Order Book Directory mesajı yeniden gönderilebilir. [Spesifikasyon 4.2.1]
23. Süresi dolmuş Order Book ID değerleri yeni enstrümanlar için yeniden kullanılabilir. [Spesifikasyon Tablo 2]
24. Aynı Order Book ID'ye sahip tüm Tick Size Table Entry (`L`) mesajları birlikte o emir defterinin eksiksiz fiyat adımı tablosunu oluşturur. [Spesifikasyon 4.2.3]
25. Tick Size Table Entry'de `Price To` alanının 0 olması sonsuz anlamına gelir; fiyatlardaki ondalık hane sayısı Order Book Directory mesajından alınır. [Spesifikasyon 4.2.3]
26. Her kombinasyon emir defteri için, kombinasyonu oluşturan her bacak başına bir Combination Order Book Leg (`M`) mesajı üretilir. [Spesifikasyon 4.2.2]
27. Short Sell Status (`V`) mesajı sistem başlangıcından önce açığa satışa izin veriyor olabilecek emir defterleri için gönderilir; bir emir defteri `V` mesajında yoksa istemci, gün başı referans veri mesajlarında emir defterinin açığa satış kuralı olmadığını varsayar. [Spesifikasyon 4.2.4]
28. Gün içinde bir emir defterinin açığa satış kuralı değişirse `V` mesajı o emir defteri için yeniden gönderilir; `Short Sale Restriction` değerleri: 0 = kısıtlama yok, 1 = açığa satışa izin verilmez, 2 = açığa satışa yukarı adım (up-tick) kuralıyla izin verilir. [Spesifikasyon 4.2.4]
29. Order Book ID, `V` mesajında yalnızca Pay Piyasası enstrümanları için geçerlidir. [Spesifikasyon 4.2.4]

### F. Olay ve durum mesajları (4.3)
30. System Event (`S`) mesajının `Event Code` değeri `O` (Start of Messages) ise bu mesaj, zaman damgası mesajları dışında, bir işlem gününde gönderilen ilk mesajdır; `C` (End of Messages) ise bir işlem gününde gönderilen son mesajdır. [Spesifikasyon 4.3.1]
31. Order Book State (`O`) mesajı, belirtilen Order Book ID için emir defteri durumundaki değişikliği `State Name` (20 karakter, Alpha) alanıyla bildirir. [Spesifikasyon 4.3.2]
32. `State Name` olası değerleri spesifikasyonda listelenmemiştir; Pay Piyasası seans durumu adları için `../ekler/ek10.md`, `../ekler/ek11.md`, `../ekler/ek19.md` ve `../veri/datastore-dosya-formatlari.md` (3.1.13 Session) kullanılır. Bkz. 01-seanslar.md. Örnek günde (08.10.2018) gözlenen 16 durum adı: `P_ACILIS_EMIR_TPL`, `P_ARA`, `P_DK_TEKFIY_EMIR_TPL`, `P_ESLESTIRME`, `P_ESLESTIRMETEKFIYAT`, `P_GECICI_DURDURMA`, `P_GUNSONU`, `P_GUNSONU_ISLEMLERI`, `P_GUNSONU_ISTATISTIK`, `P_KAPANIS_EMIR_TPL`, `P_KAPANIS_FIY_ISLEM`, `P_MARJ_YAYIN`, `P_MARJ_YAYIN_KAPANIS`, `P_MARJ_YAYIN_KAP_TF`, `P_SUREKLI_ISLEM`, `P_TEKFIYAT_EMIR_TPL`; hepsi Ek-11/Ek-19'da da geçer. [Spesifikasyon 4.3.2; örnek veri: `../veri/itch-ornek-veri-dogrulama.md` bölüm 4]

### G. Emir bazlı mesajlar ve emir defteri kurma (4.4, Appendix A)
33. Order ID yalnızca emir defteri ve taraf (Side) başına benzersizdir (FIX 6.6.1.2 ve OUCH Tablo 10 aynı bilgiyi verir); emir değiştirirken veya silerken yalnızca doğru taraf ve emir defterindeki emir güncellenir. Emir anahtarı (Order Book ID, Side, Order ID) olarak kullanılır. [Spesifikasyon 4.4 notu]
34. Add Order (`A`) mesajı yeni bir emrin kabul edildiğini ve görünür emir defterine eklendiğini gösterir. [Spesifikasyon 4.4.1]
35. Add Order `Quantity` alanı emrin görünür miktarıdır; açıklanmayan (gizli) miktara sahip emirlerde bu alan 0'dır. [Spesifikasyon Tablo 7]
36. Add Order `Lot Type` değeri 2 = Round Lot'tur; `Order Attributes` alanı bit haritasıdır ve tanımlı değerler 0 (uygulanamaz) ve 8192 (bait/implied emir)'dir. [Spesifikasyon Tablo 7–8]
37. Bir emrin o anda görüntülenen miktarı, aynı Order ID'li Add Order mesajındaki orijinal miktardan Modify mesajlarındaki miktarların toplamı düşülerek bulunur; birden fazla Modify Order mesajı aynı emre gönderilebilir ve etkiler kümülatiftir. [Spesifikasyon 4.4.2]
38. Order Executed (`E`) ve Order Executed with Price (`C`) mesajları kısmi veya tam gerçekleşmeyi bildirir; emir miktarı mesajdaki `Executed Quantity` kadar azaltılır; kalan miktar 0'a ulaşan emir emir defterinden çıkarılır. [Spesifikasyon 4.4.2.1, 4.4.2.2 ve Appendix A]
39. Bir emir tamamen gerçekleştiğinde normalde Order Delete mesajı gönderilmez; alıcı kalan miktarı her Order Executed mesajında yeniden hesaplayarak izler. [Spesifikasyon 4.4.2.4]
40. Eşleşmeye neden olan gelen emir tamamen doldurulamıyorsa, kalan kısım eşleşme gerçekleştikten sonra emir defterine konur. [Spesifikasyon 4.4.2.1, 4.4.2.2]
41. Order Delete (`D`) mesajı ilgili emrin emir defterinden kaldırılmasını söyler; silinen emrin kalan miktarı yoktur. [Spesifikasyon 4.4.2.4 ve Appendix A]
42. Order Book Flush (`Y`) mesajı ilgili emir defterindeki tüm kalan emirlerin emir defterinden çıkarılmasını söyler. [Spesifikasyon 4.4.2.5 ve Appendix A]
43. Sıralama tipi (Order Book Directory `Ranking Type`) "Price Time" (1) olduğunda emirler Price, Ranking Time ve Ranking Sequence Number parametreleriyle sıralanır; şu anda tüm BIST Pay ve Türev Piyasası enstrümanlarının sıralama tipi Price Time'dır. [Spesifikasyon Appendix A]
44. Alış tarafı emirlerinde fiyat daha yüksekse, satış tarafı emirlerinde fiyat daha düşükse emrin sırası önceliklidir. [Spesifikasyon Appendix A]
45. Fiyatlar eşitse `Ranking Time` daha erken olan emrin sırası önceliklidir. [Spesifikasyon Appendix A]
46. Fiyat ve `Ranking Time` eşitse `Ranking Sequence Number` daha küçük olan emrin sırası önceliklidir. [Spesifikasyon Appendix A]
47. `Ranking Sequence Number` işlem bazlı, 1'den başlayan ardışık bir numaradır; yalnızca `Ranking Time` ile birlikte sıralama mantığında kullanılır ve emir defterindeki konumu göstermez. [Spesifikasyon Tablo 7]
48. Order Book Position alanı Add Order (`A`) mesajından kaldırılmıştır (sıralama mantığının değişmesi nedeniyle); yeni sıralama mantığı Service Release 3.12 ile etkinleştirilir. [Spesifikasyon 1 (Değişiklik 9)]

### H. İşlem mesajları ve işlem göstergesi (4.4.2.2, 4.5, Appendix B, C, D)
49. Order Executed with Price (`C`) mesajı, emir defterindeki bir emrin ilk görüntülenen fiyattan farklı bir fiyatla gerçekleştiği durumda gönderilir. [Spesifikasyon 4.4.2.2]
50. Trade (`P`) mesajı, görünmeyen (non-displayable) emir tiplerini içeren normal eşleşme olayları için gerçekleşme ayrıntılarını sağlar ve tekil cross işlemlerini yayınlamak için de kullanılır. [Spesifikasyon 4.5.1]
51. Trade mesajları işlem göstergelerine, hacme ve diğer piyasa istatistiklerine dâhil edilir; görüntülenen defteri etkilemediklerinden yalnızca emir defteri görünümü kuran uygulamalar bunları yok sayabilir. [Spesifikasyon 4.5.1]
52. Trade (`P`) mesajında `Side`, eşleşen görünmeyen emrin tipidir ("B" veya "S"); anonim piyasalarda boşluk (space) olur. [Spesifikasyon Tablo 14]
53. Printable bayrağı "N" olan Order Executed with Price ve Trade mesajları, çifte sayımı önlemek için işlem göstergesi ve hacim hesaplarından hariç tutulur. [Spesifikasyon 4.4.2.2 ve Appendix B]
54. İşlem göstergesi (trade ticker) Order Executed (`E`), Order Executed with Price (`C`) ve Trade (`P`) mesajlarına dayanır. [Spesifikasyon Appendix B]
55. `Occurred at Cross` "Y" ise işlem cross'ta (müzayede/çapraz eşleşme), "N" ise sürekli piyasada gerçekleşmiştir. [Spesifikasyon Tablo 10 ve 14]
56. Match ID sistem tarafından gerçekleşen her eşleşmeye atanır; kombinasyon gerçekleşmesi ile bileşen emir defteri gerçekleşmelerinin Match ID değerleri farklı, Combo Group ID değerleri aynıdır; Combo Group ID zaman içinde benzersiz varsayılmaz. [Spesifikasyon Tablo 9 ve Appendix C]
57. Kombinasyon–kombinasyon gerçekleşmesinde kombinasyon emir defteri için Printable "N" olan Order Executed with Price, bileşen emir defterlerinde Trade mesajları; kombinasyon–tekil gerçekleşmesinde bileşen emir defterlerinde Order Executed ve/veya Order Executed with Price, kombinasyon emir defterinde Printable "N" olan Trade mesajı gönderilir. [Spesifikasyon Appendix C]
58. Rezerv (Iceberg) emir tamamen dolarsa (görünür ve gizli miktara karşı eşleşme): görünür miktara karşı eşleşen miktarla `E`, gizli miktara karşı eşleşen miktarla `P` gönderilir. [Spesifikasyon Appendix D]
59. Rezerv emir yalnızca gizli miktara karşı eşleşir ve tamamen dolmazsa: görünür miktarı emir defterinden kaldıran `D`, toplam eşleşen miktarla `P`, görünür miktarı emir defterine yeniden ekleyen `A` gönderilir. [Spesifikasyon Appendix D]

### I. Müzayede (auction) mesajları (4.5.2)
60. Müzayedeler sırasında emir bazlı veri yayını yapılandırmayla devre dışı bırakılabilir; bu durumda ilgili emir defterindeki mevcut her emir, müzayededen hemen önce bir Order Book Flush (`Y`) mesajıyla emir defterinden çıkarılır. [Spesifikasyon 4.5.2]
61. Order Book Flush ile kaldırılan emirlerin sahipleri bunu emir iptali olarak yorumlamamalıdır; emir durumu özel (private) emir akışıyla belirlenir. [Spesifikasyon 4.5.2]
62. Equilibrium Price Update (`Z`) mesajı müzayedeler sırasında denge fiyatındaki değişiklikleri sağlar; mesaj denge fiyatındaki alış ve satış miktarlarını, en iyi alış/satış fiyat ve miktarlarını içerir; herhangi bir Price alanı MIN_INT ise o fiyat mevcut değildir. [Spesifikasyon 4.5.2.1]
63. Tek fiyat yönteminde emir toplama aşamasındaki bilgi gösterimi ve denge fiyatı yayımı için bkz. 03-tek-fiyat.md madde 28–31.

### J. Protokol akışı (Appendix E)
64. İstemci ITCH IP/port(lar)ında (birincil ve ikincil veri akışlarında) multicast grubuna katılarak emir seviyesindeki veri, işlem mesajları, referans veri ve olay mesajlarını dinler. [Spesifikasyon Appendix E]
65. GLIMPSE (SoupBinTCP ile ikili kodlanmış) geç katılım için emir defterlerinin anlık görüntüsünü sağlar; anlık görüntü sonunda istemci, gerçek zamanlı ITCH akışını GLIMPSE anlık görüntüsünde belirtilen sıra numarasından itibaren dinlemeye devam eder. [Spesifikasyon Appendix E]
66. REWINDER (MoldUDP64 ile ikili kodlanmış) veri boşluğundan kurtarma içindir; paket kaybı tespit edilir ve ikincil veri akışından sağlanamazsa istemci paketi REWINDER'dan yeniden ister, mesajlar UDP unicast olarak yeniden gönderilir; yeniden oynatma paketleri 1440 bayt uzunluğundadır, mesajlar bu sınırı aşarsa kalanlar için yeni istek gönderilir. [Spesifikasyon Appendix E]
67. GLIMPSE ve REWINDER servisleri ITCH protokolüyle aynı mesaj biçimlerini kullanır. [Spesifikasyon Appendix E]
68. REWINDER veya GLIMPSE kullanılmadan önce istemciler çalışıyor olmalı ve gerçek zamanlı ITCH akışını sürekli dinliyor olmalıdır. [Spesifikasyon Appendix E]

## Örnek veriyle doğrulanan bulgular (kural değildir; yalnızca 08.10.2018 günü için gözlem)
Ayrıntı ve sayılar: `../veri/itch-ornek-veri-dogrulama.md`.
- `.VRD` (rewinder) dosyaları MoldUDP64 paket başlığı içermez; baştan sona `[2 bayt big-endian uzunluk][mesaj]` dizisidir (uzunluk, kendini içermez). TM-1/TR-1 ile TM-2/TR-2 bayt bayt aynıdır; GP-* dosyaları boştur.
- TXT ve ikili dosyalar 5.615.765 mesajın tamamında alan alan eşleşti (bölüm 1: 2.731.600; bölüm 2: 2.884.165 mesaj). TXT zamanları UTC'dir (İstanbul = UTC + 3).
- 2018 mesaj uzunlukları (uzunluk öneki hariç): `T` 5, `S` 6, `R` 129, `L` 25, `O` 29, `A` 37, `E` 52, `D` 18, `P` 50, `Z` 53. `R` 2018'de `Ranking Type` içermez; `A` 2018'de offset 18'de `Order Book Position` içerir ve `Ranking Time` içermez (2112 sürümü: `R` 130, `A` 45). `C`, `F`, `M`, `U`, `V`, `Y` mesajı bu günde yoktur.
- Emir defteri yeniden kurma testi (A/E/D): hata 0; gün sonunda defterde emir kalmaz; tamamen gerçekleşen emir için `D` gelmez.
- Müzayede durumlarında (`P_ACILIS_EMIR_TPL`, `P_KAPANIS_EMIR_TPL`, `P_TEKFIYAT_EMIR_TPL`, `P_DK_TEKFIY_EMIR_TPL`) `A` mesajı gelmez; defterler `Y` ile değil tek tek `D` ile boşaltılır.
- Her eşleştirmede tek fiyat oluşur ve bu fiyat son `Z` denge fiyatına eşittir; işlem hacmi `Z`'deki min(alış, satış) miktarından hiç küçük değildir.
- `A` fiyatlarının tamamı ilgili emir defterinin `L` fiyat adımının katıdır.
- `P` mesajında `Side` hep boşluk, `Printable` hep `Y`; `E`/`P` `Reserved` alanları boşluk baytıdır; `E` `Combo Group ID` hep 0.

## Açık sorular
- [DOĞRULANDI – örnek veri] `State Name` değerleri: örnek günde 16 ad gözlendi (madde 32). Spesifikasyon yine liste vermez; 2 sonekli, `_EIY`, `_PY`, `_APY` vb. adlar (Ek-10/Ek-11'de geçer) 2018 verisinde yoktur. 01-seanslar.md'deki saat/durum soruları kısmen kapandı (bkz. orada).
- [DOĞRULANDI – örnek veri; 2112 sürümü için AÇIK] Mesaj uzunlukları: 2018 ikili verisinde `R` 129, `A` 37 bayt; bu dosyadaki katalog uzunlukları 2112 sürümüne (`R` 130, `A` 45) göredir. 2112 sürümünde `Ranking Type`/`Ranking Time`/`Ranking Sequence Number` içeren gerçek veri yok; o sürümün uzunlukları yalnızca spesifikasyondan hesaplanmıştır.
- [DOĞRULANDI – örnek veri] Madde 25 ve Tablo 4: `L` mesajı 25 bayt; Tick Size 8 bayt (Numeric), Price From ve Price To 4 bayt (işaretli tamsayı). Spesifikasyonun veri tipleri bölümündeki "8 baytlık Price alanı" ifadesi Tick Size'a ilişkin olmalıdır.
- [KISMEN AÇIK] Madde 4 ve örnek veri: Prosedür her üye için en az dört ITCH oturumu (dört Partition) der; örnek pakette yalnızca iki bölüm (partition 1 ve 2) var. Bölümler ayrıktır (750 + 878 emir defteri, kesişim yok). `GP`, `TM`, `TR` ön eklerinin anlamı belgelerde yok: TM ve TR dosyaları aynı bayt içeriktedir; GP boştur.
- [DOĞRULANDI – örnek veri] Madde 10, 64–68: `.VRD` dosyalarında MoldUDP64 paket başlığı yoktur; dosya, MoldUDP64'ün `Message Block` yapısıyla (2 bayt uzunluk + mesaj) aynı biçimde ardışık mesajlardır. GLIMPSE/SoupBinTCP biçimi bu veriyle sınanamadı (GP dosyaları boş).
- [KISMEN DOĞRULANDI – Genium INET FIX Reference Data Protocol Specification 1.0.40, 5.4.1] `Lot Type` değerleri: 2 = Round Lot, 3 = Block Lot (FIX `LotType` 1093; sayfa 25). ITCH spesifikasyonu yalnızca 2'yi listeler. Örnek veride (2018) `A` mesajlarında 0 değeri de gözlendi (50 + 23 emir); 0'ın anlamı hiçbir belgede yok.
- [KISMEN AÇIK] Madde 4 ve bölümler: FIX Reference Data her enstrüman için `PartitionId` (21008) alanını taşır ("hangi bölümde işlem gördüğü"); değerler bu belgede listelenmez. `TM`/`TR`/`GP` ön eklerinin anlamı hiçbir dokümanda bulunamadı.
- [KISMEN AÇIK] Madde 36: `Order Attributes` için spesifikasyonda yalnızca 0 ve 8192 tanımlı; örnek günde 0 ve **2** gözlendi (2'nin anlamı belgede yok). `Lot Type` için yalnızca 2 (Round Lot) tanımlı; örnek günde bölüm 1'de 50, bölüm 2'de 23 emirde **0** gözlendi. `Reserved` alanları (`E`, `C`, `P`) bu günde hep boşluk baytıdır.
- [KISMEN AÇIK] Madde 55 ve 62: `Occurred at Cross` örnek günde `Y` yalnızca `P_ESLESTIRME` ve `P_ESLESTIRMETEKFIYAT` durumundaki işlemlerde (19.735 + 1.538); `N` `P_SUREKLI_ISLEM` (2.713), `P_DK_TEKFIY_EMIR_TPL` (158) ve `P_KAPANIS_FIY_ISLEM` (3) işlemlerinde, ayrıca `P_ESLESTIRME` (26) ve `P_ESLESTIRMETEKFIYAT` (2) içinde de görülür; bu istisnaların nedeni belgelerde yok. `Equilibrium Price Update` (`Z`) emir toplama durumlarında ve ayrıca `P_ARA`, `P_SUREKLI_ISLEM`, `P_MARJ_YAYIN_KAPANIS`, `P_ESLESTIRMETEKFIYAT`, `P_MARJ_YAYIN_KAP_TF` durumlarında da görülür.
- [AÇIK] Madde 38 ve 56: `Match ID` ve `Order ID` alanlarının günler arası benzersizliği yazılı değil; tek gün verisiyle sınanamaz.
- [AÇIK] Madde 7: Spesifikasyon "eşleştirme mantığı ITCH'ten çıkarılamaz" diyor; eşleştirme motoru kuralları ITCH'ten değil Prosedür kural dosyalarından kodlanır, ITCH yalnızca yeniden oynatılacak emir akışı ve doğrulama verisidir.
- [AÇIK] Block Lot Size: Order Book Directory tablosunda Block Lot Size açıklaması Odd Lot Size ile aynı cümledir; alanın gerçek anlamı yazılı değil (bkz. çeviri dosyasındaki çeviri notu). Örnek günde hep 0.
- [AÇIK] Madde 60: Spesifikasyon müzayedede emir defterinin `Y` (Order Book Flush) ile boşaltılabileceğini söyler; 2018 verisinde `Y` yok, müzayede girişinde defter tek tek `D` ile boşaltılıyor. Güncel (2024+) davranışı gösteren veri elde edilmedi.
- [AÇIK] ITCH'in ana (primary) ve ikincil (secondary) multicast akışlarının adresleri/portları Prosedürde ve spesifikasyonda yoktur (MoldUDP64 belgesi de adreslerin başka bir kaynakta olduğunu söyler).
- Not: 5.7.1 İşlem Terminalleri, 5.7.2 FixAPI ve 5.7.3 OUCH, görev listesinde olmadığı için bu dosyaya alınmadı.

## Test örnekleri
Kaynak belgelerde (Prosedür, spesifikasyon) sayısal örnek yoktur. Aşağıdakiler `../veri/itch/2018-10-08/txt/itch-partition-1-2018-10-08-0000.txt` dosyasından alınmış gerçek satırlardır; ilgili ikili (`.VRD`) mesajlarla alan alan eşleştiği doğrulanmıştır. `...` = zaman alanı kısaltılmıştır (biçim: `2018-10-07T21:37:14.841792820(1538948234841792820)`; zaman UTC).

| TXT satırı | Beklenen çözümleme |
|---|---|
| `T,1538948234` | `T` mesajı, Second = 1538948234. İkili: `00 05 54 5B BA 7C 8A`. |
| `S,...(1538948234841792820),O` | `S` mesajı, Event Code `O` (Start of Messages); birleşik zaman 1538948234 × 10⁹ + 841792820 ns. İkili: `00 06 53 32 2C BD 34 4F` (uzunluk 6; nanosaniye 0x322CBD34 = 841792820). |
| `R,...,70616,ACSEL.E,ACIPAYAM SELULOZ,TREACSS00017,5,TRY,3,0,0,1,0,1,0,5080,0,19881130,3,0` | `R` mesajı (2018 biçimi, 129 bayt): Order Book ID 70616; Symbol ACSEL.E; Long Name ACIPAYAM SELULOZ; ISIN TREACSS00017; Financial Product 5 (Cash); Trading Currency TRY; Number of decimals in Price 3; Number of decimals in Nominal Value 0; Odd Lot 0; Round Lot 1; Block Lot 0; Nominal Value 1; Number of Legs 0; Underlying Order Book ID 5080; Strike Price 0; Expiration Date 19881130; Number of decimals in Strike Price 3; Put or Call 0. `Ranking Type` yok. |
| `L,...,ACSEL.E(70616),10,10,19999` | `L` mesajı: Order Book ID 70616; Tick Size 10 (ondalık 3 ile 0,010); Price From 10; Price To 19999. Aynı emir defteri için sonraki satırlar: `20,20000,49999`; `50,50000,99999`; `100,100000,999999999`. |
| `O,2018-10-08T06:40:00.110645907(1538980800110645907),ACSEL.E(70616),P_ACILIS_EMIR_TPL` | `O` mesajı: Order Book ID 70616; State Name `P_ACILIS_EMIR_TPL`; 06:40:00 UTC = 09:40:00 İstanbul. |
| `A,2018-10-08T06:55:04.109485956(1538981704109485956),7050379173631984023,ACSEL.E(70616),B,1,376,2640,0,2` | `A` mesajı (2018 biçimi, 37 bayt): Order ID 7050379173631984023; Order Book ID 70616; Side B; Order Book Position 1; Quantity 376; Price 2640 (3 ondalıkla 2,640 TL); Order Attributes 0; Lot Type 2. |
| `P,2018-10-08T06:55:04.109485956(1538981704109485956),705037921228626276,0, ,1000,ACSEL.E(70616),2640,,,Y,Y` | `P` mesajı: Match ID 705037921228626276; Combo Group ID 0; Side boşluk; Quantity 1000; Order Book ID 70616; Trade Price 2640; Reserved alanları boşluk; Printable Y; Occurred at Cross Y (açılış tek fiyatı, 09:55 İstanbul). |
| `E,2018-10-08T07:00:00.081703781(1538982000081703781),7050379173632258990,AKBNK.E(70796),S,6100,705037921228629856,0,,` | `E` mesajı: Order ID 7050379173632258990; Order Book ID 70796; Side S; Executed Quantity 6100; Match ID 705037921228629856; Combo Group ID 0; Reserved alanları boşluk. |
| `D,2018-10-08T07:00:00.046300575(1538982000046300575),7050379173632142583,ALBTS.F1(71106),B` | `D` mesajı: Order ID 7050379173632142583; Order Book ID 71106; Side B. |
| `Z,2018-10-08T06:40:00.110645907(1538980800110645907),ACSEL.E(70616),0,0,-2147483648,-2147483648,-2147483648,0,0` | `Z` mesajı: Order Book ID 70616; her iki taraf miktarı 0; Equilibrium Price, Best Bid Price ve Best Ask Price = MIN_INT (fiyat yok); Best Bid/Ask Quantity 0. |

Tek fiyat doğrulama örneği: ACSEL.E (70616) 08.10.2018 açılışında son anlamlı `Z`: Available Bid Quantity 3500, Available Ask Quantity 2123, Equilibrium Price 2640 (2,640 TL), Best Bid Price 2650, Best Ask Price 2600, Best Bid Quantity 1000, Best Ask Quantity 1000; açılış eşleştirmesindeki `P` işlemlerinin tamamı 2640'tan gerçekleşti ve toplam 2124 adettir (`Z`'deki min(3500, 2123) = 2123'ten 1 fazla; bkz. `../veri/itch-ornek-veri-dogrulama.md` bölüm 5).
