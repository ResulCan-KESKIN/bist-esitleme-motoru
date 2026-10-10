# Fiyat
Kaynak: Pay Piyasası Prosedürü 5.1.1 İşlem Birimi (Lot) (s. 48–49), 5.1.4 Fiyat Gösterimi (s. 51), 5.1.6 Ağırlıklı Ortalama Fiyat (s. 51), 5.1.7 Baz Fiyat Aralıkları ve Fiyat Adımları (s. 51), 5.1.8 Baz Fiyat (s. 51–52), 5.1.9 Fiyat Adımları (s. 52–53), 5.1.10 Referans Fiyat (s. 53), 5.1.11 Fiyat Değişme Sınırları (s. 53), 5.1.15 Maddi Hata Nedeniyle İşlem İptali (s. 54), 5.6.2 Fiyat Değişme Sınırları (s. 91–92). Sayfa numaraları PDF sayfa numarasıyla aynıdır. İlgili Ekler (içerikleri bu dosyada tekrarlanmaz): `../ekler/ek3.md` (varant: hareketli fiyat değişme sınırları, maddi hata nedeniyle işlem iptali), `../ekler/ek4.md` (sertifika), `../ekler/ek5.md`, `../ekler/ek6.md`, `../ekler/ek7.md`, `../ekler/ek8.md` (araç bazında fiyat adımı ve fiyat marjı), `../ekler/ek18.md` madde 7 (AOF emri).
İlgili kod: emir doğrulama (fiyat adımı, lot, fiyat sınırları), baz fiyat ve fiyat limiti hesabı, ITCH çözümleyici fiyat ölçeği, eşleştirme motoru (fiyat sınırı kontrolü)

## Kurallar

### A. İşlem birimi (lot) (5.1.1)
1. Lot, bir sermaye piyasası aracından kendisi veya katları ile işlem yapılabilecek asgari miktarı veya değeri ifade eden işlem birimidir. [5.1.1, s. 48]
2. Tüm pay ve yeni pay alma hakkı işlemlerinde işlem birimi olarak "1,00 TL (nominal) = 1 adet = 1 lot" eşitliği uygulanır. [5.1.1, s. 48]
3. Küsurat sıraları (.KE özellik kodlu sıralar) haricinde işlem biriminden daha küçük miktarlı emir (küsurat emir) verilemez. [5.1.1, s. 48–49]
4. Nominal değere sahip olmayan T. İş Bankası A.Ş. Kurucu tipi paylarda emirler adet olarak iletilir. [5.1.1, s. 49]
5. BYF katılma belgelerinin lot büyüklüğü 1 adet katılım payıdır. [5.1.1, s. 49]
6. Yönetim Kurulu sermaye piyasası aracının niteliklerini göz önünde bulundurarak işlem birimini miktar veya değer olarak belirler ve KAP'ta ilan eder. [5.1.1, s. 49]

### B. Fiyat gösterimi (5.1.4)
7. Fiyat kuruş altı hassasiyette (10 bps veya diğer bir deyişle kuruş alanı 3 karakter olacak şekilde) gösterilir; örneğin 10,05 şeklinde gösterilen fiyat 10,050 olarak gösterilir. [5.1.4, s. 51]
8. Başlangıçta kuruş altında fiyat adımı belirlenmediğinden virgülden sonraki üçüncü hanede herhangi bir değer oluşmaz. [5.1.4, s. 51]
9. ISKUR payında fiyat gösterimi kuruş hassasiyetinde (virgülden sonra 2 hane) yapılır. [5.1.4, dipnot 33, s. 51]

### C. Ağırlıklı ortalama fiyat (AOF) (5.1.6)
10. AOF, işlem gören sermaye piyasası aracının miktar ağırlıklı fiyatıdır. [5.1.6, s. 51]
11. AOF hesaplanmasında aracın seans içinde işlem gördüğü değişik fiyatlardan ve miktarlardan gerçekleşen ve tescil edilen normal emir işlemleri dikkate alınır. [5.1.6, s. 51]
12. AOF Sistem tarafından hesaplanır. [5.1.6, s. 51]
13. Kapanış seansı ve kapanış fiyatından işlemler aşamasında gerçekleşen işlemlerin AOF hesabına dâhil edilmesi için bkz. 03-tek-fiyat.md madde 81 ve 94. [5.2.2.3.1, s. 64; 5.2.2, s. 65]
14. ".AOF" sıralarında AOF'den işlem gören emirlerin (AOF/TAR emri) işleyişi ve fiyat hesabı: bkz. `../ekler/ek18.md` madde 7. [Ek-18, s. 222–225]

### D. Baz fiyat aralıkları, baz fiyat ve fiyat adımları (5.1.7–5.1.9)
15. Alım ve satım emirlerinin karşılaştırılması esas olarak aracın fiyat kademelerine göre belirlenen fiyat adımlarına uygun fiyatlarla yapılır. [5.1.7, s. 51]
16. Baz fiyat, bir seans süresince aracın işlem görebileceği üst ve alt fiyat sınırlarının belirlenmesine esas teşkil eden fiyattır. [5.1.8, s. 51]
17. Önceki işlem gününün kapanış fiyatı baz fiyat olarak belirlenir. [5.1.8, s. 51]
18. Baz fiyat yoksa (önceki kapanış yoksa veya fiyat serbest bırakılmışsa) tek fiyat işlem yöntemi ile işlem gören sıralar için ilk fiyatın oluştuğu emir toplama aşaması sonrasında belirlenen eşleşme fiyatı baz fiyat olur. [5.1.8, s. 51]
19. Baz fiyat yoksa sürekli işlem yöntemi ile işlem gören sıralar için ilk işlemin fiyatı baz fiyat olarak alınır: açılış seansında fiyat oluşmuşsa bu fiyat, oluşmamışsa sürekli işlem aşamasında gerçekleşen ilk işlemin fiyatı. [5.1.8, s. 52]
20. İşlem görecek yeni pay alma haklarında ilk gün sonuna kadar (ilk işlem günü dâhil) baz fiyat uygulanmaz; işlem gördüğü ilk günün kapanış fiyatı ertesi günün baz fiyatını oluşturur. [5.1.8, s. 52]
21. Bir önceki günden baz fiyata sahip bir payda gün içinde herhangi bir işlem gerçekleşmemişse bu baz fiyat ertesi günün baz fiyatı olur. [5.1.8, s. 52]
22. Varant ve sertifika sıralarında baz fiyat uygulaması yoktur. [5.1.8, s. 52]
23. Temettü ödemeleri veya sermaye artırımları durumlarında Borsa tarafından hesaplanan teorik fiyatın en yakın fiyat adımına yuvarlanması sonucu elde edilen baz fiyat belirlenerek Sisteme girilir. [5.1.8, s. 52]
24. Fiyat adımı, her payın fiyatı için bir defada gerçekleşebilecek en küçük fiyat değişimidir. Payların fiyat adımları fiyat seviyelerine göre belirlenir; emir girilirken bu fiyat adımlarına uyulması zorunludur. [5.1.9, s. 52]
25. Paylar, yeni pay alma hakları ve BYF'ler için Tablo-7 ve Tablo-8'de belirtilen fiyat seviyeleri ve fiyat adımları uygulanır. [5.1.9, s. 52–53]
26. Varantlarda, sertifikalarda, emtia sertifikalarında ve Toptan Alış Satış (TAS) işlemlerinde her fiyat seviyesi için fiyat adımı 1 kuruştur. [5.1.9, s. 52]
27. Fiyat adımları baz fiyata bağlı olmaksızın ilgili fiyat seviyesine göre belirlenir. Seans içinde girilen emrin fiyatı bir fiyat eşiğini geçerse bir sonraki eşiğe kadar fiyat adımı baz fiyata bağlı olmaksızın o seviyenin fiyat adımı olarak değişir. [5.1.9, s. 52]
28. Sahipliğe dayalı kira sertifikaları ve gayrimenkul sertifikaları için paylarda uygulanan fiyat seviyeleri ve fiyat adımları (Tablo-7) geçerlidir; gayrimenkul yatırım fonu ve girişim sermayesi yatırım fonu katılma payları için BYF fiyat seviyeleri ve fiyat adımları (Tablo-8) geçerlidir; emtia sertifikalarında fiyat adımı her fiyat seviyesinde 1 kuruştur. [Ek-5, Ek-6, Ek-7, Ek-8; bkz. `../ekler/ek5.md`, `ek6.md`, `ek7.md`, `ek8.md`]

**Tablo-7: Paylarda ve Yeni Pay Alma Haklarında Geçerli Fiyat Adımları (tablodan)** [5.1.9, s. 52]

| Fiyat Seviyesi (TL) | Fiyat Adımı (TL) |
|---|---|
| 0,010 – 19,999 | 0,010 |
| 20,000 – 49,999 | 0,020 |
| 50,000 – 99,999 | 0,050 |
| 100,000 – 249,999 | 0,100 |
| 250,000 – 499,999 | 0,250 |
| 500,000 – 999,999 | 0,500 |
| 1000,000 – 2499,999 | 1,000 |
| 2500,000 – üzeri | 2,500 |

**Tablo-8: BYF Katılma Belgelerinde Geçerli Fiyat Adımları (tablodan)** [5.1.9, s. 53]

| Fiyat Seviyesi (TL) | Fiyat Adımı (TL) |
|---|---|
| 0,010 – 49,999 | 0,010 |
| 50,000 – 99,999 | 0,020 |
| 100,000 – 249,999 | 0,050 |
| 250,000 – 499,999 | 0,100 |
| 500,000 – 999,999 | 0,250 |
| 1000,000 – 2499,999 | 0,500 |
| 2500,000 – üzeri | 1,000 |

### E. Referans fiyat (5.1.10)
29. Referans fiyat; özsermaye hâlleri sonucunda ortaklık paylarının veya yeni pay alma haklarının ilgili Borsa düzenlemesi kapsamında belirtilen esaslara ve yöntemlere göre hesaplanan, ancak işlem görebileceği en üst ve en alt fiyat limitlerinin belirlenmesine esas teşkil etmeyen, fiyat tescili yapılıncaya kadar yatırımcılar tarafından referans değer olarak kullanılması amaçlanan fiyattır. [5.1.10, s. 53]
30. Özsermaye hâllerinde paylar için referans fiyat belirlenmesi durumunda fiyat değişme sınırları uygulanmaz. [5.6.2, s. 92]
31. Açılış seansı fiyat belirlemede kullanılan Açılış Referans Fiyatı (ARF) için bkz. 03-tek-fiyat.md madde 47. [5.2.2.2.1, s. 60–61]

### F. Fiyat değişme sınırları (fiyat marjı ve fiyat limitleri) (5.1.11 + 5.6.2)
32. Baz fiyat yöntemine göre işlem gören her sermaye piyasası aracı için seans sırasında tek fiyat veya sürekli işlem yöntemine göre oluşan fiyatlar, baz fiyattan madde 33'te belirtilen oranlardan daha fazla farklı olamaz. [5.1.11, s. 53]
33. Fiyat marjları: paylarda Yıldız Pazar ±%20, Ana Pazar ±%15, Alt Pazar, YİP ve PÖİP ±%10; BYF'lerde ±%20; yeni pay alma haklarında ve ISKUR.E'de ±%50; gayrimenkul yatırım fonlarında (GMF) ve girişim sermayesi yatırım fonlarında ±%20; gayrimenkul sertifikalarında (GMS) ve emtia sertifikalarında ±%5. [5.1.11, s. 53]
34. Yeni pay alma hakları ve T. İş Bankası Kurucu pay sıralarında ±%50 oranında fiyat marjı uygulanır. [5.6.2, s. 92]
35. Sahipliğe dayalı kira sertifikalarında serbest fiyat marjı uygulanır. [Ek-5; bkz. `../ekler/ek5.md`]
36. Fiyat değişme sınırları, baz fiyata aracın pazarında geçerli fiyat marjı uygulanarak bulunur. Bu fiyat aralığı aracın gün boyunca işlem görebileceği fiyat değişme sınırlarını oluşturur. [5.6.2, s. 91–92]
37. Fiyat değişme sınırları hesaplanırken baz fiyata fiyat marjı uygulandıktan sonra bulunan değerler yuvarlanır; yuvarlama işlem yapılabilecek fiyat aralığını daraltıcı şekilde içeri doğru yapılır: alt sınır en yakın yukarı fiyat adımına, üst sınır en yakın aşağı fiyat adımına yuvarlanır. [5.1.11, s. 53; 5.6.2, s. 92]
38. Yatırım kuruluşu varant ve sertifikalarında piyasa yapıcının seans boyunca ilettiği alış kotasyonlarını referans alan hareketli fiyat değişme sınırları uygulanır; uygulama esasları Ek-3'tedir: bkz. `../ekler/ek3.md` ("Hareketli Fiyat Değişme Sınırları Uygulaması") ve `../ekler/ek4.md` (sertifikalar için fiyat limitleri). [5.1.11, s. 53; 5.6.2, s. 92]
39. Kapanış seansında sürekli işlem bölümünde gerçekleşen son işlem fiyatı üzerine ±%3 uygulanması için bkz. 03-tek-fiyat.md madde 72–75. [5.1.11, s. 53; 5.2.2.3.1, s. 63–64]
40. PPD Direktörü, piyasanın gerektirdiği durumlarda resen fiyat değişme sınırlarını iki katına kadar genişletebilir. [5.6.2, s. 92]
41. Borsa Genel Müdürü, gereken durumlarda resen fiyat değişme sınırlarını kaldırabilir veya değiştirebilir. [5.6.2, s. 92]
42. Yönetim Kurulu fiyat değişme sınırlarını pazar ve emir türü bazında farklı olarak belirleyebilir. [5.6.2, s. 92]

### G. Maddi hata nedeniyle işlem iptali (5.1.15)
43. BİAŞ Yönetmeliği 33/b maddesi uyarınca işlem yapma yetkisi verilenlerden en az biri tarafından alım satım sistemine iletilen hatalı emir veya emirler sonucunda gerçekleşen işlemlerin iptal taleplerinde madde 44–46'daki yöntem izlenir. [5.1.15, s. 54]
44. Girilen hatalı emrin neden olduğu işlem veya işlemlerin taraflarından biri veya her iki taraf, işlem iptal isteğini işlemin saatinden 15 dakika içinde baş temsilci yetkili İşlem Terminalleri (TW, Omnet API) ve/veya yazılı, elektronik iletişim kanalları vb. araçlar yoluyla PPD'ye gönderir. [5.1.15, s. 54]
45. Normal fiyat oluşumunun dışında olmak üzere (a) işlem fiyatı ile aynı fiyattan farklı üyeler arasında başka işlem yapılmamışsa ve/veya (b) hatalı işlem/işlemlere ait fiyatlara %3'ten daha yakın fiyatlardan işlem/işlemler oluşmamışsa, iptal isteği gönderilen işlem/işlemler PPD tarafından değerlendirilir. [5.1.15, s. 54]
46. BİAŞ Yönetmeliği 33/b maddesi uyarınca Borsa personeli tarafından iletilen hatalı emir veya emirler sonucunda gerçekleşen işlemler Genel Müdür, görevlendirilen Genel Müdür Yardımcısı veya PPD Direktörü tarafından resen iptal edilir. [5.1.15, s. 54]
47. Varant (.V) ve sertifika (.C) işlemlerine ilişkin maddi hata nedeniyle işlem iptal talebi değerlendirme kriterleri Ek-3'te ayrıca belirlenmiştir: bkz. `../ekler/ek3.md` ("13) Maddi Hata Nedeniyle İşlem İptali"). [5.1.15, s. 54]

## Açık sorular
- [DOĞRULA] Madde 27 ve 5.1.9 örneği: Metindeki örnekte "20,00 TL'ye kadar fiyat adımı 1 kuruş, 20,00 TL'den sonra 2 kuruş" deniyor; Tablo-7'de 0,010–19,999 aralığı 0,010, 20,000–49,999 aralığı 0,020. Tam 20,00 TL'nin hangi adım aralığına girdiği örnek metninden kesin anlaşılmıyor (tabloya göre 0,020 aralığının ilk fiyatı).
- [DOĞRULA] Madde 25 ve Tablo-7/Tablo-8: Fiyat seviyeleri tabloda "1000,000" ve "2500,000" gibi binlik ayraçsız yazılmış, üst sınırlar "2499,999" ve "üzeri" olarak verilmiş; son aralığın üst sınırı yok. Fiyat seviyesi aralıklarının alt/üst sınır dâhil olup olmadığı (örn. 19,999 ile 20,000 arasındaki fiyatlar) yazılı değil; fiyat adımı zaten 0,010 olduğundan kod için geçerli fiyat kümesi yalnızca adımlı değerlerdir.
- [DOĞRULA] Madde 33 ve 36: 5.6.2 fiyat marjları için "bkz. Tablo-4 (Pazarlarda Uygulanacak İşlem Esasları)" diyor; Tablo-4 bu dosyanın kapsam sayfalarında yok. Marj yüzdeleri için 5.1.11'deki liste kullanıldı; Tablo-4 ile aynı olup olmadığı doğrulanmadı. Ayrıca 5.1.11 listesinde GSP (Girişim Sermayesi Pazarı) ve EP (Emtia Pazarı) paylarının marjı ayrıca yazılı değil.
- [DOĞRULA] Madde 33 ve 34: 5.1.11 "yeni pay alma haklarında ve ISKUR.E'de ±%50", 5.6.2 "yeni pay alma hakları ve T. İş Bankası Kurucu pay sıralarında ±%50" diyor. ISKUR.E ile "T. İş Bankası Kurucu pay sıraları"nın aynı sıra olduğu açıkça yazılı değil.
- [DOĞRULA] Madde 33 ve 35: Sahipliğe dayalı kira sertifikalarının marjı 5.1.11 listesinde yok; yalnızca Ek-5 "serbest fiyat marjı" diyor. "Serbest marj" için baz fiyat/limit hesabının nasıl yapılacağı (sınırsız mı) bu bölümde tanımlı değil; 03-tek-fiyat.md madde 74'teki kapanış seansı hükmü (serbest marjlı araçta sınırsız emir girişi) yalnızca kapanış seansını kapsıyor.
- [DOĞRULA] Madde 36–37 ve 5.1.11 ile 5.6.2: Yuvarlama kuralı iki yerde (5.1.11 ve 5.6.2) tekrar ediliyor ve tutarlı; baz fiyat marj uygulandıktan sonraki değerin "en yakın" adıma yuvarlanmasında tam ortada kalma durumu tanımlı değil.
- [DOĞRULA] Madde 39: 5.1.11'de "Kapanış seansında uygulanan ve sürekli işlem bölümünde gerçekleşen son işlem fiyatı üzerine ±%3 olarak uygulanır." cümlesinin öznesi (fiyat marjı mı) açık değil; 03-tek-fiyat.md'deki kapanış seansı kurallarıyla birlikte okunmalıdır.
- [DOĞRULA] Madde 45: "(a) ... ve/veya (b) ..." ifadesinde (a) ve (b) koşullarının birlikte mi alternatif olarak mı aranacağı ("ve/veya") ve "normal fiyat oluşumunun dışında" ifadesinin ölçütü yazılı değil. Ayrıca bu madde 15 dakikalık başvuru süresi veriyor; Ek-3 madde 13 (varant) 30 dakika (seans bitimine 30 dakikadan az kalmışsa 10 dakika) veriyor; iki süre farklı işlem sıraları için olduğundan çelişki sayılmadı, yalnızca not edildi.
- [DOĞRULA] Madde 20–23: Baz fiyat ile referans fiyat ilişkisi (teorik fiyat, referans fiyat, baz fiyat tespiti) "Endeks Direktörlüğü tarafından çıkarılmış olan düzenleme"ye (24/11/2015 tarihli ve 2015/116 sayılı Duyuru) bırakılmış; bu belge Prosedür PDF'inde yok. Temettü/sermaye artırımı sonrası baz fiyat hesabı bu dosyada kodlanamaz.
- [DOĞRULA] Madde 11 ve 13: AOF hesabında "normal emir işlemleri" dikkate alınır deniyor; Orta Nokta, AOF sırası ve özel işlem bildirimi işlemlerinin AOF'a dâhil olup olmadığı 5.1.6'da yazılı değil (Ek-18'de Orta Nokta işlemlerinin ayrıca yayımlanmadığı ve toplam miktar/hacme dâhil edildiği geçiyor; AOF sırası işlemleri .E sırasının istatistiklerine dâhil edilmez).
- [DOĞRULA] Madde 9: ISKUR payı için 2 hane kuralı dipnotta (dipnot 33 ve 34) geçiyor; aynı pay için fiyat adımının ne olduğu bu bölümde yazılı değil.
- Not: 5.1.2 (İşlem ve Özellik Kodu), 5.1.3, 5.1.5 (Fiyat İlanı), 5.1.12–5.1.14 görev listesinde olmadığı için bu dosyaya alınmadı.

## Test örnekleri
- Fiyat adımı örneği [5.1.9, s. 52]: Baz fiyatı (kapanış fiyatı) 19,97 TL olan bir pay sırasında 20,00 TL'ye kadar fiyat adımı 1 kuruş, 20,00 TL'den sonra 2 kuruş olur; seans içinde girilen emrin fiyatı 20,00 TL'yi geçerse bir sonraki fiyat eşiğine kadar fiyat adımı baz fiyata bağlı olmaksızın 2 kuruş olarak değişir.
- Fiyat gösterimi örneği [5.1.4, s. 51]: 10,05 olarak gösterilen fiyat 10,050 olarak gösterilir.
- Hareketli fiyat değişme sınırları (varant) örnekleri için `../ekler/ek3.md` "Hareketli Fiyat Değişme Sınırları Uygulaması" bölümündeki Örnek 1 ve Örnek 2 kullanılır (ilk alış kotasyonu 0,57 TL → sınırlar 0,53 / 0,63 TL; 0,60 TL → 0,54 / 0,68 TL; ilk alış kotasyonu 1 TL → 0,90 / 1,10 TL).
- Kapanış seansı fiyat marjı örneği (baz fiyat 3,00; sınırlar 2,40–3,60; son işlem 3,58 → 3,48–3,60): bkz. 03-tek-fiyat.md Test örnekleri.
