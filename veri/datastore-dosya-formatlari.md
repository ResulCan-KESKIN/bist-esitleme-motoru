# DataStore Dosya Formatları (Veri Bildirim ve Kabul Formatları)

Kaynak: `DataStore_Veri_Bildirim_ve_Kabul_Formatları.pdf` (Borsa İstanbul DataStore Dosyaları Veri Bildirim ve Kabul Formatları, Sürüm 1.4 - 15.06.2016), s. 1–56.
Aktarım yöntemi: PDF'ten kelime konumlarıyla çıkarım; tablo hücreleri sayfadaki kenarlık ve dolgu çizgilerinden kurulmuştur. Yorum eklenmemiştir. Hücre içi satır sonları `<br>` ile gösterilir. Markdown tablolarında ilk satır, kaynakta başlık satırı olmasa da başlık satırı olarak yazılır. Her sayfanın altındaki "Sürüm 1.4 - 15.06.2016 ..." altbilgi satırı yazılmamıştır; sayfa işaretleri `**[Sayfa N]**` ile verilmiştir.
Otomatik doğrulama: sayfalardaki tüm kelimelerin dosyada bulunduğu kontrol edildi (eksik kelime: 0).
Görsel doğrulama (Claude, sayfa görüntüsü ile karşılaştırma): s. 5, 20, 21 ve 50 sayfa görüntüsüyle karşılaştırıldı (s. 21 elle düzeltildi); diğer sayfalar için görüntü incelenmedi. 121 tablonun tamamında başlık, ayırıcı ve satırların hücre sayısı eşit (otomatik kontrol).
Önemli not (kullanıcı tarafından DataStore sayfasından aktarıldı): 27.07.2020 tarihinden itibaren TL cinsi BIST Pay Endekslerinden ve Müşteri Endekslerinden iki sıfır atılmıştır; bu tarihten önceki dosyalardaki endeks değerleri 100'e bölünerek (bölen değerleri 100 ile çarpılarak) kullanılmalıdır. VİOP endeks vadeli işlem ve opsiyon sözleşmelerinde de değişiklik yapılmıştır. Ayrıntı ve projeye etkisi için bkz. `README.md`.
Kullanıcı doğrulaması: bekliyor

<!-- sayfa 1 -->
**[Sayfa 1]**

DATASTORE DOSYA FORMATLARI
Dökümanın Tarihçesi

| Sürüm | Tarih | Değişikliklerin Özeti |
|---|---|---|
| 1.1<br>1.2<br>1.3<br>1.4 | 26.11.2015<br>29.12.2015<br>13.01.2016<br>09.05.2016 | İlk Sürüm<br>Raporlardaki kolon eklenmesi/çıkarılması, isim değişiklikleri ve ondalık,binlik<br>ayraçların yeniden düzenlenmesi<br>Bazı raporlardaki kolon isimleri ve açıklamalarının düzenlenmesi<br>Bazı raporlardaki kolon isimleri ve açıklamalarının düzenlenmesi |

<!-- sayfa 2 -->
**[Sayfa 2]**

İÇERİK
1. GİRİŞ ..................................................................................................................... 4
1.1 Dokümanın Amacı .................................................................................................................................. 4
1.2 Hedef Kitle ............................................................................................................................................. 4
1.3 Dosya Formatları Hakkında Tanımlar ve Kabüller ................................................................................ 4
2. BORSA İSTANBUL DATASTORE DOSYALARI VERİ BİLDİRİM VE KABUL FORMATLARI ................................................................................................ 5
2.1 BORSA İSTANBUL Tarafından DataStore Portalında Satışı Yapılan Dosyalar ............................. 5
2.1.1 Fiyat Endeksleri ............................................................................................................................. 5
2.1.2 Getiri Endeksleri ............................................................................................................................ 5
2.1.3 Risk Kontrol Endeksleri ................................................................................................................. 6
2.1.4 BIST 30 ve BIST 100 Endeksi Tarihsel Volatilite Değerleri ......................................................... 7
2.1.5 Aylık Müşteri / Fon / Portföy İşlemleri .......................................................................................... 7
2.1.6 Toplam İşlem Hacmi, İşlem Miktarı ve Sözleşme Sayısı .............................................................. 8
2.1.7 Üye Bazında Günlük İşlem Sıralaması ........................................................................................ 11
2.1.8 İşlemlerin Üyelere Göre Aylık Dağılımı ...................................................................................... 12
2.1.9 İşlemlerin Üyelere Göre Yıllık Kümüle Dağılımı ........................................................................ 14
2.1.10 İşlem Hacmi, İşlem Miktarı, Sözleşme Sayıları ......................................................................... 16
2.1.11 Açığa Satış İşlemleri .................................................................................................................. 16
2.1.12 Kapanış, En Düşük ve En Yüksek Fiyatlar ile İşlem Hacmi, İşlem Miktarı .............................. 17
2.1.13 Kapanış, En Düşük ve En Yüksek Fiyatlar ile İşlem Hacmi, İşlem Miktarı (Aylık) ................. 18
2.1.14 En Aktif 20 Pay .......................................................................................................................... 19
2.1.15 En Aktif 20 Üye ......................................................................................................................... 20
2.1.16 Gün İçi Emir Defteri Bilgileri .................................................................................................... 20
2.1.17 Gün İçi İşlem Defteri Bilgileri ................................................................................................... 22
2.1.18 Günsonu Fiyat ve İşlem Hacmi Bilgileri.................................................................................... 23
2.1.19 Gün İçi Endeks Bilgileri (Bütün Endeksler) .............................................................................. 26
2.1.20 Gün Sonu Endeks ve İşlem Hacmi Bilgileri .............................................................................. 26
2.1.21 Yıl İçinde Gerçekleştirilen Bedelli Sermaye Artırımları ve Nakit Temettüler........................... 27
2.1.22 Tarih Bazında Sermaye Artırımı, Temettü Ödemesi ve Benzeri Şirket Bilgileri ....................... 29
2.1.23 Değerleme Oranları (Aylık) ....................................................................................................... 31
2.1.24 Değerleme Oranları (Haftalık) ................................................................................................... 32
2.1.25 Aylık Değişimler ve Bileşik Getiriler (1993 – 2015) ................................................................. 33
2.1.26 Sermaye Artırımları (Aylık) ....................................................................................................... 34
2.1.27 Sermaye Artırımları (Haftalık) ................................................................................................... 37
2.1.28 Temettü Ödemeleri .................................................................................................................... 39
2.1.29 2000 Yılından İtibaren Endekslerde Bulunan Şirketler ............................................................. 41
2.1.30 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Öncesi Endeks Bölen Raporu) ....................................................... 42
2.1.31 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Sonrası Endeks Bölen Raporu) ...................................................... 42
2.1.32 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Öncesi Endeks Ağırlık Raporu) ..................................................... 43
2.1.33 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Sonrası Endeks Ağırlık Raporu) .................................................... 44 EK
3.1 REFERANS TABLOLARI .................................................................................................................. 46
3.1.1 OrderType .................................................................................................................................... 46
3.1.2 ExchangeOrderType .................................................................................................................... 46
3.1.3 OrderCategory.............................................................................................................................. 47
3.1.4 ChangeReason.............................................................................................................................. 47
3.1.5 MarketSegment ............................................................................................................................ 48

<!-- sayfa 3 -->
**[Sayfa 3]**

3.1.6 Market .......................................................................................................................................... 49
3.1.7 OrderStatus .................................................................................................................................. 49
3.1.8 OrderDurationID .......................................................................................................................... 50
3.1.9 OrderPriceTypeID ........................................................................................................................ 50
3.1.10 OrderTypeIDSet ......................................................................................................................... 50
3.1.11 DealSource ................................................................................................................................. 51
3.1.12 CorporateAction ......................................................................................................................... 54
3.1.13 Session ....................................................................................................................................... 54
3.1.14 TradeType .................................................................................................................................. 55

<!-- sayfa 4 -->
**[Sayfa 4]**

1. GİRİŞ
1.1 Dokümanın Amacı
Pay Piyasası ve Endeks uygulamaları sonucu üretilerek Borsa İstanbul tarafından BIST DataStore portalında satışı yapılan dosyalarda yer alan alanlarla ilgili olarak bilgi vermektir.
1.2 Hedef Kitle
Bu doküman, Borsa İstanbul Pay Piyasası Alım-Satım sistemi ve Endeks Hesaplama Sistemi (ICSII) tarafından üretilip BIST DataStore portalında satışı yapılan dosyaları kullanacak kişilere yöneliktir.
1.3 Dosya Formatları Hakkında Tanımlar ve Kabüller
(*) işareti ilgili alanın uzunluğunun değişebileceğini, bu alanda yazılan rakam en üst sınır değerini göstermektedir. Alan uzunluğu bu sınırın altında kalırsa herhangi bir başka karakter/boşluk vb. ile üst sınıra tamamlanmak için doldurulmayacaktır.

<!-- sayfa 5 -->
**[Sayfa 5]**

2. BORSA İSTANBUL DATASTORE DOSYALARI VERİ BİLDİRİM VE KABUL FORMATLARI
2.1 BORSA İSTANBUL Tarafından DataStore Portalında Satışı Yapılan Dosyalar
2.1.1 Fiyat Endeksleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| EVM_FIYATEND.D.[YYYYAAGG].zip-><br>fiyatend(endeks_kodu).csv |  | Fiyat endekslerinin BISTECH geçişi öncesi<br>seanslık, geçiş sonrası günlük kapanış, en<br>düşük, en yüksek değerlerini gösteren<br>rapordur. |
| Örnek Dosya Adı | EVM_FIYATEND.D.20151207.zip<br>-> fiyatendXU100.csv | BIST 100 fiyat endeksinin gün sonu kapanış,<br>gün içi en yüksek ve en düşük değerleri |
| Örnek Dosya İçerikleri |  |  |
| 15.12.2015;XU100;BIST 100;BIST 100;TL;1;72156.79;69308.74;72391.87 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih<br>(GG.AA.YYYY) | Alfanümerik | 10 | Günün tarihi |
| 2 | Endeks Kodu | Alfanümerik | 80* | Endeks Kodu : “XU100”,<br>“XU100_CFNPTLER” gibi |
| 3 | Endeksler | Alfanümerik | 400* | Endeks Türkçe Adı : BIST 100, BIST100 EURO<br>gibi |
| 4 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 400* | Endeks İngilizce Adı |
| 5 | Kur Türü | Alfabetik | 3* | TL,EUR,USD |
| 6 | Seans No | Nümerik | 1 | Nasdaq geçişi öncesi seans kavramı olduğundan<br>1 ve 2 değerlerini, geçiş sonrası 1 değerini<br>almaktadır. |
| 7 | Kapanış Değeri | Ondalıklı,Nü<br>merik | 20* | Fiyat endeksinin gün sonu kapanış değeri |
| 8 | En Düşük Değer | Ondalıklı,Nü<br>merik | 20* | Fiyat endeksinin gün içerisinde gerçekleşen en<br>düşük değeri |
| 9 | En Yüksek Değer | Ondalıklı,Nü<br>merik | 20* | Fiyat endeksinin gün içerisinde gerçekleşen en<br>yüksek değeri |

2.1.2 Getiri Endeksleri

| Dosya Adı | Açıklama |
|---|---|
| EVM_GETIRIEND.D.[YYYYAAGG].zip-><br>getend(endeks_kodu).csv | Getiri endekslerinin BISTECH geçişi öncesi<br>seanslık, geçiş sonrası günlük kapanış<br>değerini gösteren rapordur. |

<!-- sayfa 6 -->
**[Sayfa 6]**

| Dosya Adı |  | Açıklama |
|---|---|---|
| Örnek Dosya Adı | EVM_GETIRIEND.D.2015<br>1207.zip-><br>getendXU100.csv | BIST 100 getiri endeksinin gün sonu kapanış<br>değeri |
| Örnek Dosya İçerikleri |  |  |
| 07.12.2015;XU100_CFNNTLER;BIST 100 GETIRI (EURO);BIST 100 RETURN<br>(EURO);EUR;1;2408.06 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih<br>(GG.AA.YYYY) | Alfanümerik | 10 | Günün tarihi |
| 2 | Endeks Kodu | Alfanümerik | 80* | Endeks Kodu |
| 3 | Endeksler | Alfanümerik | 400* | Endeks Türkçe Adı |
| 4 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 400* | Endeks İngilizce Adı |
| 5 | Kur Türü | Alfabetik | 3* | TL,EUR,USD |
| 6 | Seans No | Nümerik | 1 | Nasdaq geçişi öncesi seans kavramı olduğundan<br>1 ve 2 değerlerini, geçiş sonrası 1 değerini<br>almaktadır. |
| 7 | Kapanış Değeri | Ondalıklı,Nü<br>merik | 20* | Getiri endeksinin gün sonu kapanış değeri |

2.1.3 Risk Kontrol Endeksleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| RiskKontrolEndeksleri_YYYYAAGG.csv |  | BIST 100 ve BIST 30 endeksleri ile BIST-<br>KYD Repo endeksi (Net) günlük<br>getirilerinden, %10, %15, %20, %25 ve %30<br>hedef risk seviyelerine göre ayrı ayrı<br>hesaplanan RİSK KONTROL (TOPLAM<br>GETİRİ) endekslerinin değerleri ve sadece<br>BIST 100 ve BIST 30 endeksleri günlük<br>getirilerinden, %10, %15, %20, %25 ve %30<br>hedef risk seviyelerine göre ayrı ayrı<br>hesaplanan RİSK KONTROL (GETİRİ)<br>endekslerinin değerleri raporlanmaktadır. |
| Örnek Dosya Adı | RiskKontrolEndeksleri_20151<br>211.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 11.12.2015; BIST30 RK %30 (TOPLAM GETIRI);30;150;1.3032;548.0748 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Günün tarihi (GG.AA.YYYY) |
| 2 | Endeks Adı | Alfanümerik | 400* | Endeksin Adı Örneğin BIST 30 RK %10<br>(TOPLAM GETIRI)<br>BIST30 RK %15 (GETIRI) |
| 3 | Hedef Risk<br>Seviyesi(%) | Nümerik | 10* | Endeksin hedef risk seviyesi (%10, %15, %20,<br>%25 ve %30) |
| 4 | Dayanak Endeks<br>Maximum<br>Ağırlığı(%) | Nümerik | 10* | Dayanak Endeksin (BIST 30,BIST 100)<br>maksimum ağırlığı |
| 5 | Dayanak Endeks<br>Ağırlığı | Ondalıklı,Nü<br>merik | 20* | Dayanak Endeksin (BIST 30,BIST 100) ağırlığı |

<!-- sayfa 7 -->
**[Sayfa 7]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 6 | Endeks Değeri | Ondalıklı,Nü<br>merik | 20* | Endeksin gün sonu kapanış değeri |

2.1.4 BIST 30 ve BIST 100 Endeksi Tarihsel Volatilite Değerleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| EVM_ENDEKSVOLATILITE.D.[YYYYAAGG].zip-><br>volatilite_XU030.csv<br>volatilite_XU100.csv |  | BIST 30 ve BIST 100 endekslerinin tarihsel<br>volatilite değerlerini gösteren rapor |
| Örnek Dosya Adı | EVM_ENDEKSVOLATIL<br>ITE.D.20151207.zip-><br>volatilite_XU100.csv | BIST 100 endeksinin 21,42,63,126,252<br>günlük tarihsel volatilite değeri |
| Örnek Dosya İçerikleri |  |  |
| 30.11.2015;XU100;BIST 100;BIST 100;21;27.51<br>07.12.2015;XU100;BIST 100;BIST 100;252;22.07 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih<br>(GG.AA.YYYY) | Alfanümerik | 10 | Günün tarihi |
| 2 | Endeks Kodu | Alfanümerik | 80* | Endeksin Kodu |
| 3 | Endeksler | Alfanümerik | 400* | Endeksin Türkçe Adı |
| 4 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 400* | Endeksin İngilizce Adı |
| 5 | Gün Sayısı | Numerik | 10* | Volatilite değerlerinin hesaplandığı gün sayıları.<br>21,42,63,126,252 |
| 6 | Değer | Ondalıklı,Nü<br>merik | 20* | Endeksin Değeri |

2.1.5 Aylık Müşteri / Fon / Portföy İşlemleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_MFTHACIM.M.[YYYYAA].zip-><br>PP_MFTHACIM.M.[YYYYAA].csv |  | Aylık olarak Müşteri / Fon / Portföy<br>kırılımında, alış ve satış bazında işlem<br>toplamları raporlanmaktadır. |
| Örnek Dosya Adı | PP_MFTHACIM.M.201512.zip-><br>PP_MFTHACIM.M.201512.csv |  |
| Örnek Dosya İçerikleri |  |  |
| F;Alış;201512; 2323604880.95 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Yatırımcı Türü | Alfabetik | 4* | M: Müşteri, P:Portföy, F:Fon |
| 2 | Alış/Satış | Alfabetik | 10* | Alış veya Satış bilgisini içermektedir. |
| 3 | Ay(YYYYAA) | Nümerik | 20* | Yıl ay bilgisini içermektedir. |
| 4 | İşlem Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | İlgili ayda fon, portföy veya müşteri adına<br>gerçekleştirilen alış veya satış işlemlerinin hacim<br>bilgisini içermektedir. |

<!-- sayfa 8 -->
**[Sayfa 8]**

2.1.6 Toplam İşlem Hacmi, İşlem Miktarı ve Sözleşme Sayısı

| Dosya Adı |  | Açıklama |
|---|---|---|
| toppiy.zip -> toppiy.csv |  | Günlük olarak Pay Piyasası ve Piyasa<br>Öncesi İşlem Platformu’nda gerçekleşen<br>Toplam İşlem Hacmi (TL, ABD Doları<br>ve Euro bazında), İşlem Miktarı ve<br>Sözleşme Sayısı bilgilerinin Pazar<br>bazında kırılımını gösteren rapordur. |
| Örnek Dosya Adı | toppiy.zip -> toppiy.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 30.11.2015;3046550537.82;1046600892.45;989300385.72;463857332.00;206342;102740845.90;3529521<br>6.57;33362833.54;56816848.00;65512;2747739.89;943948.57;892268.19;1468032.00;5752;;;;;;4247710.<br>78;1459243.11;1379350.80;157465.00;718;177734998.69;61058435.09;57715537.81;82881538.00;37970<br>;23395739.40;8037287.23;7597252.61;66623803.00;8483;1032607.28;354738.15;335316.54;2338118.00;<br>1233;44799.35;15390.21;14547.61;16930.00;82 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | İşlem Tarihi<br>(GG.AA.YYYY) | Alfanümerik | 10 | Günün tarihi |
| 2 | Yıldız Pazar İşlem<br>Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen toplam işlem<br>hacminin TL değeridir. |
| 3 | Yıldız Pazar İşlem<br>Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen toplam işlem<br>hacminin USD değeridir. |
| 4 | Yıldız Pazar İşlem<br>Hacmi (EURO) | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen toplam işlem<br>hacminin EURO değeridir. |
| 5 | Yıldız Pazar İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen toplam işlem miktarı<br>bilgisidir. |
| 6 | Yıldız Pazar<br>Sözleşme Sayısı | Nümerik | 20* | Yıldız Pazar’da gerçekleşen sözleşme sayısı<br>bilgisidir. |
| 7 | Ana Pazar İşlem<br>Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen toplam işlem hacminin<br>TL değeridir. |
| 8 | Ana Pazar İşlem<br>Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen toplam işlem hacminin<br>USD değeridir. |
| 9 | Ana Pazar İşlem<br>Hacmi (EURO) | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen toplam işlem hacminin<br>EURO değeridir. |
| 10 | Ana Pazar İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen toplam işlem miktarı<br>bilgisidir. |
| 11 | Ana Pazar<br>Sözleşme Sayısı | Nümerik | 20* | Ana Pazar’da gerçekleşen sözleşme sayısı<br>bilgisidir. |
| 12 | Gelişen İşletmeler<br>Pazarı İşlem Hacmi<br>(TL) | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen toplam<br>işlem hacminin TL değeridir. |
| 13 | Gelişen İşletmeler<br>Piyasası İşlem<br>Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen toplam<br>işlem hacminin USD değeridir. |
| 14 | Gelişen İşletmeler<br>Piyasası İşlem<br>Hacmi (EURO) | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen toplam<br>işlem hacminin EURO değeridir. |
| 15 | Gelişen İşletmeler<br>Piyasası İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen toplam<br>işlem miktarı bilgisidir. |

<!-- sayfa 9 -->
**[Sayfa 9]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 16 | Gelişen İşletmeler<br>Piyasası Sözleşme<br>Sayısı | Nümerik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen<br>sözleşme sayısı bilgisidir. |
| 17 | Nitelikli Yatırımcı<br>İşlem Pazarı İşlem<br>Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>toplam işlem hacminin TL değeridir. |
| 18 | Nitelikli Yatırımcı<br>İşlem Pazarı İşlem<br>Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>toplam işlem hacminin USD değeridir. |
| 19 | Nitelikli Yatırımcı<br>İşlem Pazarı İşlem<br>Hacmi (EURO) | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>toplam işlem hacminin EURO değeridir. |
| 20 | Nitelikli Yatırımcı<br>İşlem Pazarı İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>toplam işlem miktarı bilgisidir. |
| 21 | Nitelikli Yatırımcı<br>İşlem Pazarı<br>Sözleşme Sayısı | Nümerik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>sözleşme sayısı bilgisidir. |
| 22 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>İşlem Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>fonlarına ilişkin toplam işlem hacminin TL<br>değeridir. |
| 23 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>İşlem Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>fonlarına ilişkin toplam işlem hacminin USD<br>değeridir. |
| 24 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>İşlem Hacmi<br>(EURO) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>fonlarına ilişkin toplam işlem hacminin EURO<br>değeridir. |
| 25 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>İşlem Miktarı | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>fonlarına ilişkin toplam işlem miktarı bilgisidir. |
| 26 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>Sözleşme Sayısı | Nümerik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonlarına (BYF) ilişkin sözleşme sayısı bilgisidir. |
| 27 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer İşlem Hacmi<br>(TL) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>fonları ve Varantlar hariç Diğer payların toplam<br>işlem hacminin TL değeridir. |

<!-- sayfa 10 -->
**[Sayfa 10]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 28 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer İşlem Hacmi<br>(USD) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonları ve Varantlar hariç Diğer payların toplam<br>işlem hacminin USD değeridir. |
| 29 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer İşlem Hacmi<br>(EURO) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonları ve Varantlar hariç Diğer payların toplam<br>işlem hacminin EURO değeridir. |
| 30 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer İşlem Miktarı | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonları ve Varantlar hariç Diğer payların toplam<br>işlem miktarı bilgisidir. |
| 31 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer Sözleşme<br>Sayısı | Nümerik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonları ve Varantlar hariç Diğer payların toplam<br>sözleşme sayısı bilgisidir. |
| 32 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant İşlem Hacmi<br>(TL) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda Varantlara ilişkin gerçekleşen<br>toplam işlem hacminin TL değeridir. |
| 33 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant İşlem Hacmi<br>(USD) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>toplam işlem hacminin USD değeridir. |
| 34 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant İşlem Hacmi<br>(EURO) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>toplam işlem hacminin EURO değeridir. |
| 35 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>toplam işlem miktarı bilgisidir. |
| 36 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant Sözleşme<br>Sayısı | Nümerik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>sözleşme sayısı bilgisidir. |

<!-- sayfa 11 -->
**[Sayfa 11]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 37 | Yakın İzleme<br>Pazarı İşlem Hacmi<br>(TL) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen toplam<br>işlem hacminin TL değeridir. |
| 38 | Yakın İzleme<br>Pazarı İşlem Hacmi<br>(USD) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen toplam<br>işlem hacminin USD değeridir. |
| 39 | Yakın İzleme<br>Pazarı İşlem Hacmi<br>(EURO) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen toplam<br>işlem hacminin EURO değeridir. |
| 40 | Yakın İzleme<br>Pazarı İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen toplam<br>işlem miktarı bilgisidir. |
| 41 | Yakın İzleme<br>Pazarı Sözleşme<br>Sayısı | Nümerik | 20* | Yakın İzleme Pazarı’nda gerçekleşen sözleşme<br>sayısı bilgisidir. |
| 42 | Piyasa Öncesi İşlem<br>Platformu İşlem<br>Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>toplam işlem hacminin TL değeridir. |
| 43 | Piyasa Öncesi İşlem<br>Platformu İşlem<br>Hacmi (USD) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>toplam işlem hacmi nin USD değeridir. |
| 44 | Piyasa Öncesi İşlem<br>Platformu İşlem<br>Hacmi (Euro) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>toplam işlem hacminin EURO değeridir. |
| 45 | Piyasa Öncesi İşlem<br>Platformu İşlem<br>Miktarı | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>toplam işlem miktarı bilgisidir. |
| 46 | Piyasa Öncesi İşlem<br>Platformu Sözleşme<br>Sayısı | Nümerik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>sözleşme sayısı bilgisidir. |

2.1.7 Üye Bazında Günlük İşlem Sıralaması

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_UYESIRA.S.YYYYAAGG1.zip-><br>PP_UYESIRA.S.YYYYAAGG1.csv |  | Üye Bazında Günlük İşlem Sıralaması<br>raporlanmaktadır. |
| Örnek Dosya Adı | PP_UYESIRA.S. 201512021.zip-><br>PP_UYESIRA.S.201512021.csv |  |
| Örnek Dosya İçerikleri |  |  |
| OYA; OYAK YATIRIM MENKUL DEGERLER A.S; 82244329.2;0.799 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Üye Kodu | Alfabetik | 20* | Üye Kodu bilgisini içermektedir. |
| 2 | Üye Adı | Alfabetik | 80* | Üye Adı bilgisini içermektedir. |
| 3 | İşlem Hacmi | Nümerik | 20* | İşlem hacmi bilgisini içermektedir. Birincil<br>piyasa, yeni pay alma hakları ve özel emirler ve<br>toptan satış işlemleri dahil edilmemektedir. |

<!-- sayfa 12 -->
**[Sayfa 12]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 4 | İşlem Hacmi Oranı | Ondalıklı,Nü<br>merik | 20* | İşlem hacmi oranı bilgisini içermektedir. Birincil<br>piyasa, yeni pay alma hakları ve özel emirler ve<br>toptan satış işlemleri dahil edilmemektedir. |

2.1.8 İşlemlerin Üyelere Göre Aylık Dağılımı

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_UYEISLEM.M.[YYYYAA].zip -><br>PP_UYEISLEM.M.[YYYYAA].xlsx |  | Aylık olarak, üyelerin pazar bazında<br>gerçekleştirdikleri işlemlerin dağılımını<br>gösteren rapordur. |
| Örnek Dosya Adı | PP_UYEISLEM.M.[201511].zip -><br>PP_UYEISLEM.M.[201511].xlsx |  |
| Örnek Dosya İçerikleri |  |  |
| ACP;A1 CAPITAL MENKUL DEGERLER A.Ş.;Üye (Member);Aracı Kurum (Brokerage House);0.00;<br>364703865.6;0.00; 4408357.72;0.00; 13117.24;0.00;0.00;0.00; 1451.53;0.00; 5875792.71;0.00;0.00;0.00;<br>10209469.11;0.00; 352.84;0.00; 1393.00; 385213799.75 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Üye Kodu | Alfabetik | 20* | Üyenin Kodu |
| 2 | Üye Adı | Alfabetik | 80* | Üyenin Adı |
| 3 | Durum | Alfabetik | 30* | Üyenin Durumu. Örneğin Üye (Member), Geçici<br>Kapalı (Suspended)vs |
| 4 | Tür | Alfabetik | 50* | Üyenin türü bilgisidir. |
| 5 | Yıldız Pazar (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen Özel İşlem Bildirimi<br>toplam değeridir. |
| 6 | Yıldız Pazar (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |
| 7 | Ana Pazar (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen Özel İşlem Bildirimi<br>toplam değeridir. |
| 8 | Ana Pazar (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |
| 9 | Gelişen İşletmeler<br>Pazarı (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen Özel<br>İşlem Bildirimi toplam değeridir. |
| 10 | Gelişen İşletmeler<br>Pazarı (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen Özel<br>İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |
| 11 | Nitelikli Yatırımcı<br>İşlem Pazarı (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>Özel İşlem Bildirimi toplam değeridir. |
| 12 | Nitelikli Yatırımcı<br>İşlem Pazarı (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |
| 13 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>(Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonlarına (BYF) ilişkin Özel İşlem Bildirimi<br>toplam değeridir. |

<!-- sayfa 13 -->
**[Sayfa 13]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 14 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>(Diğer Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonlarına (BYF) ilişkin Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |
| 15 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>Özel İşlem Bildirimi toplam değeridir. |
| 16 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |
| 17 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Sertifika (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Sertifikalara<br>ilişkin Özel İşlem Bildirimi toplam değeridir. |
| 18 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Sertifika (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Sertifikalara<br>ilişkin Özel İşlem Bildirimi hariç diğer işlemlerin<br>toplam değeridir. |
| 19 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen<br>BYF,Varant,Sertifika hariç, diğer payların Özel<br>İşlem Bildirimi toplam değeridir. |
| 20 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen<br>BYF,Varant,Sertifika hariç, diğer payların Özel<br>İşlem Bildirimi hariç diğer işlemlerinin toplam<br>değeridir. |
| 21 | Yakın İzleme<br>Pazarı (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen Özel İşlem<br>Bildirimi toplam değeridir. |
| 22 | Yakın İzleme<br>Pazarı (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen Özel İşlem<br>Bildirimi hariç diğer işlemlerin toplam değeridir. |
| 23 | Piyasa Öncesi İşlem<br>Platformu (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>Özel İşlem Bildirimi toplam değeridir. |
| 24 | Piyasa Öncesi İşlem<br>Platformu (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |

<!-- sayfa 14 -->
**[Sayfa 14]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 25 | Genel Toplam | Ondalıklı,Nü<br>merik | 20* | İlgili tarih aralığında üye bazında Pay<br>Piyasasındaki tüm pazarlarda ve Piyasa Öncesi<br>İşlem Platformu’nda gerçekleştirilen özel işlem<br>bildirimleri dahil tüm işlemlerin toplam değeridir. |

2.1.9 İşlemlerin Üyelere Göre Yıllık Kümüle Dağılımı

| Dosya Adı |  |  |  |  |  | Açıklama |
|---|---|---|---|---|---|---|
| PP_UYEISLEM.Y.[YYYY].zip -><br>PP_UYEISLEM.Y.[YYYY].xlsx |  |  |  |  |  | Yıllık üye bazında işlem dağılım<br>bilgileri raporlanmaktadır. |
| Örnek Dosya Adı |  | PP_UYEISLEM.Y.2015.zip -><br>PP_UYEISLEM.Y.2015.xlsx |  |  |  |  |
| Örnek Dosya İçerikleri |  |  |  |  |  |  |
| ACP;A1 CAPITAL MENKUL DEGERLER A.Ş.;Üye (Member);Aracı Kurum (Brokerage House);0.00;<br>364703865.6;0.00; 4408357.72;0.00; 13117.24;0.00;0.00;0.00; 1451.53;0.00; 5875792.71;0.00;0.00;0.00;<br>10209469.11;0.00; 352.84;0.00; 1393.00; 385213799.75 |  |  |  |  |  |  |
| Sıra | Alan Adı |  | Alan Türü | Uzunluk | Açıklama |  |
| 1 | Üye Kodu |  | Alfabetik | 20* | Üyenin Kodu |  |
| 2 | Üye Adı |  | Alfabetik | 80* | Üyenin Adı |  |
| 3 | Durum |  | Alfabetik | 30* | Üyenin Durumu. Örneğin Üye (Member), Geçici<br>Kapalı (Suspended)vs |  |
| 4 | Tür |  | Alfabetik | 50* | Üyenin türü bilgisidir. |  |
| 5 | Yıldız Pazar (Özel<br>İşlem Bildirimi) |  | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen Özel İşlem Bildirimi<br>toplam değeridir. |  |
| 6 | Yıldız Pazar (Diğer<br>Toplam) |  | Ondalıklı,Nü<br>merik | 20* | Yıldız Pazar’da gerçekleşen Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |  |
| 7 | Ana Pazar (Özel<br>İşlem Bildirimi) |  | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen Özel İşlem Bildirimi<br>toplam değeridir. |  |
| 8 | Ana Pazar (Diğer<br>Toplam) |  | Ondalıklı,Nü<br>merik | 20* | Ana Pazar’da gerçekleşen Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |  |
| 9 | Gelişen İşletmeler<br>Pazarı (Özel İşlem<br>Bildirimi) |  | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen Özel<br>İşlem Bildirimi toplam değeridir. |  |
| 10 | Gelişen İşletmeler<br>Pazarı (Diğer<br>Toplam) |  | Ondalıklı,Nü<br>merik | 20* | Gelişen İşletmeler Pazarı’nda gerçekleşen Özel<br>İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |  |
| 11 | Nitelikli Yatırımcı<br>İşlem Pazarı (Özel<br>İşlem Bildirimi) |  | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>Özel İşlem Bildirimi toplam değeridir. |  |
| 12 | Nitelikli Yatırımcı<br>İşlem Pazarı (Diğer<br>Toplam) |  | Ondalıklı,Nü<br>merik | 20* | Nitelikli Yatırımcı İşlem Pazarı’nda gerçekleşen<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |  |
| 13 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>(Özel İşlem<br>Bildirimi) |  | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonlarına (BYF) ilişkin Özel İşlem Bildirimi<br>toplam değeridir. |  |
| 14 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı BYF<br>(Diğer Toplam) |  | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Borsa Yatırım<br>Fonlarına (BYF) ilişkin Özel İşlem Bildirimi<br>hariç diğer işlemlerin toplam değeridir. |  |

<!-- sayfa 15 -->
**[Sayfa 15]**

| Dosya Adı |  |  |  |  | Açıklama |
|---|---|---|---|---|---|
| 15 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>Özel İşlem Bildirimi toplam değeridir. |  |
| 16 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Varant (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Varantlara ilişkin<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |  |
| 17 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Sertifika (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Sertifikalara<br>ilişkin Özel İşlem Bildirimi toplam değeridir. |  |
| 18 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Sertifika (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen Sertifikalara<br>ilişkin Özel İşlem Bildirimi hariç diğer işlemlerin<br>toplam değeridir. |  |
| 19 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen<br>BYF,Varant,Sertifika hariç, diğer payların Özel<br>İşlem Bildirimi toplam değeridir. |  |
| 20 | Kolektif Yatırım<br>Ürünleri ve<br>Yapılandırılmış<br>Ürünler Pazarı<br>Diğer (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Kolektif Yatırım Ürünleri ve Yapılandırılmış<br>Ürünler Pazarı’nda gerçekleşen<br>BYF,Varant,Sertifika hariç, diğer payların Özel<br>İşlem Bildirimi hariç diğer işlemlerinin toplam<br>değeridir. |  |
| 21 | Yakın İzleme<br>Pazarı (Özel İşlem<br>Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen Özel İşlem<br>Bildirimi toplam değeridir. |  |
| 22 | Yakın İzleme<br>Pazarı (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Yakın İzleme Pazarı’nda gerçekleşen Özel İşlem<br>Bildirimi hariç diğer işlemlerin toplam değeridir. |  |
| 23 | Piyasa Öncesi İşlem<br>Platformu (Özel<br>İşlem Bildirimi) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>Özel İşlem Bildirimi toplam değeridir. |  |
| 24 | Piyasa Öncesi İşlem<br>Platformu (Diğer<br>Toplam) | Ondalıklı,Nü<br>merik | 20* | Piyasa Öncesi İşlem Platformu’nda gerçekleşen<br>Özel İşlem Bildirimi hariç diğer işlemlerin toplam<br>değeridir. |  |
| 25 | Genel Toplam | Ondalıklı,Nü<br>merik | 20* | İlgili tarih aralığında üye bazında Pay<br>Piyasasındaki tüm pazarlarda ve Piyasa Öncesi<br>İşlem Platformu’nda gerçekleştirilen özel işlem<br>bildirimleri dahil tüm işlemlerin toplam değeridir. |  |

<!-- sayfa 16 -->
**[Sayfa 16]**

2.1.10 İşlem Hacmi, İşlem Miktarı, Sözleşme Sayıları

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_PAYTOPLAM.D.[YYYYAAGG].zip-><br>PP_PAYTOPLAM.D.[YYYYAAGG].csv |  | Günlük Seri kodu bazında İşlem<br>Hacmi, İşlem Miktarı, Sözleşme<br>Sayıları raporlanmaktadır. |
| Örnek Dosya Adı | PP_PAYTOPLAM.D.20151211.zip-><br>PP_PAYTOPLAM.D.20151211.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 11.12.2015;ACSEL.E;914663.08;226569.00;889 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih<br>(GG.AA.YYYY) | Alfanümerik | 10 | İşlem tarihi |
| 2 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili alan 32 karaktere kadar değer<br>alabilmektedir. Ör: XXXX.XX |
| 3 | İşlem Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Toplam İşlem hacmi bilgisidir |
| 4 | İşlem Miktarı | Ondalıklı,Nü<br>merik | 20* | Toplam İşlem Miktarı bilgisidir. |
| 5 | Sözleşme Sayısı | Nümerik | 20* | Toplam sözleşme sayısı bilgisidir. |

2.1.11 Açığa Satış İşlemleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_ACIGASATIS.M.YYYYAA.zip -><br>PP_ACIGASATIS.M.YYYYAA.xlsx |  | Aylık olarak pay bazında açığa satış<br>bilgileri raporlanmaktadır. |
| Örnek Dosya Adı | PP_ACIGASATIS.M.201511.zip<br>-><br>PP_ACIGASATIS.M.201511.xls<br>x |  |
| Örnek Dosya İçerikleri |  |  |
| AEFES.E;MSPOTEQT;Z;1180.880;58.000;20.360;20.360 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili alan 32 karaktere kadar değer<br>alabilmektedir. Ör: XXXX.XX |
| 2 | Enstrüman Tipi | Alfabetik | 32* | İlgili enstrümanın tipinin ne olduğu bilgisini<br>vermektedir. |
| 3 | Pazar Kodu | Alfabetik | 4* | Bkz. Tablo 3.1.1 MarketSegment |
| 4 | İşlem Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Payın ilgili ayda oluşan toplam açığa satış işlem<br>hacmidir. |
| 5 | İşlem Miktarı | Ondalıklı,Nü<br>merik | 20* | Payın ilgili ayda oluşan toplam açığa satış işlem<br>miktarıdır. |
| 6 | En Düşük Fiyat | Ondalıklı,Nü<br>merik | 20* | Payın ilgili ayda gerçekleşen açığa satış işlemleri<br>arasında oluşan en düşük fiyattır. |
| 7 | En Yüksek Fiyat | Ondalıklı,Nü<br>merik | 20* | Payın ilgili ayda gerçekleşen açığa satış işlemleri<br>arasında oluşan en yüksek fiyattır. |

<!-- sayfa 17 -->
**[Sayfa 17]**

2.1.12 Kapanış, En Düşük ve En Yüksek Fiyatlar ile İşlem Hacmi, İşlem Miktarı

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_HAFTALIKOZET.W.[YYYYHH].zip -><br>PP_HAFTALIKOZET.W.[YYYYHH].xlsx |  | Haftalık olarak Kapanış, En Düşük ve<br>En Yüksek Fiyatlar ile İşlem Hacmi,<br>İşlem Miktarı raporlanmaktadır. |
| Örnek Dosya Adı | PP_HAFTALIKOZET.W.201549.<br>zip -><br>PP_HAFTALIKOZET.W.201549.<br>xlsx |  |
| Örnek Dosya İçerikleri |  |  |
| Z; PAY-YILDIZ PAZAR; BIST Stars; ADANA.E; ADANA CIMENTO A<br>GRUBU;0.00;0.00;41,567.37;3,475,528.37;5,897.00;494,114.00;6.81;7.13;7.01 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Pazar Kodu | Alfabetik | 4* | Bkz. Tablo 3.1.5 MarketSegment. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan koddur. |
| 2 | Pazar Adı | Alfabetik | 255* | Bkz. Tablo 3.1.5 MarketSegment. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan pazardır. |
| 3 | İngilizce Pazar Adı | Alfabetik | 255* | Referans için Bkz. Tablo 3.1.5 MarketSegment<br>İngilizce Pazar Adı bilgisidir. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan pazardır. |
| 4 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili pay için raporun alındığı tarih aralığının<br>son gününde geçerli olan koddur. İlgili alan 32<br>karaktere kadar değer alabilmektedir. Ör:<br>XXXX.XX |
| 5 | Bülten Adı | Alfabetik | 32* | İlgili pay için raporun alındığı tarih aralığının son<br>gününde geçerli olan bülten adı bilgisidir. |
| 6 | Özel İşlem<br>Bildirimi İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında, ilgili payda<br>gerçekleşen Özel İşlem Bildirimi işlemlerinin<br>toplam hacim bilgisidir. |
| 7 | Özel İşlem<br>Bildirimi İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen Özel İşlem Bildirimi işlemlerinin<br>toplam işlem miktarı bilgisidir. |
| 9 | Açılış Seansı İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında açılış seansında<br>ilgili payda gerçekleşen işlemlerin toplam hacim<br>bilgisidir. |
| 8 | Toplam İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen işlemlerin toplam hacim bilgisidir. |
| 10 | Açılış Seansı İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında açılış seansında<br>ilgili payda gerçekleşen işlemlerin toplam işlem<br>miktarı bilgisidir. |
| 11 | Toplam İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen toplam işlem miktarı bilgisidir. |
| 12 | En Düşük Fiyat | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında gerçekleşen en<br>düşük fiyat bilgisidir. İlgili tarih aralığında<br>gerçekleştirilen sermaye artırımları/azaltımları ve<br>temettü ödemeleri vb özsermaye hallerine göre<br>düzeltilmiştir. |

<!-- sayfa 18 -->
**[Sayfa 18]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 13 | En Yüksek Fiyat | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında gerçekleşen en<br>yüksek fiyat bilgisidir. İlgili tarih aralığında<br>gerçekleştirilen sermaye artırımları/azaltımları ve<br>temettü ödemeleri vb özsermaye hallerine göre<br>düzeltilmiştir. |
| 14 | Kapanış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığındaki son kapanış<br>fiyatı bilgisidir. |

2.1.13 Kapanış, En Düşük ve En Yüksek Fiyatlar ile İşlem Hacmi, İşlem Miktarı (Aylık)

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_AYLIKOZET.M.[YYYYAA].zip -><br>PP_AYLIKOZET.M.[YYYYAA].xlsx |  | Aylık olarak Kapanış, En Düşük ve En<br>Yüksek Fiyatlar ile İşlem Hacmi, İşlem<br>Miktarı raporlanmaktadır. |
| Örnek Dosya Adı | PP_AYLIKOZET.M.201511.zip -><br>PP_AYLIKOZET.M.201511.xlsx |  |
| Örnek Dosya İçerikleri |  |  |
| Z;PAY-YILDIZ PAZAR;BIST Stars;ADANA.E;ADANA CIMENTO A<br>GRUBU;0.00;0.00;82.56;513,296.50;12.00;74,596.00;6.81;7.00;7.00 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Pazar Kodu | Alfabetik | 4* | Bkz. Tablo 3.1.5 MarketSegment. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan koddur. |
| 2 | Pazar Adı | Alfabetik | 255* | Bkz. Tablo 3.1.5 MarketSegment. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan pazardır. |
| 3 | İngilizce Pazar Adı | Alfabetik | 255* | Referans için Bkz. Tablo 3.1.5 MarketSegment<br>İngilizce Pazar Adı bilgisidir. İlgili pay için<br>raporun alındığı tarih aralığının son gününde<br>geçerli olan pazardır. |
| 4 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili pay için raporun alındığı tarih aralığının<br>son gününde geçerli olan koddur. İlgili alan 32<br>karaktere kadar değer alabilmektedir. Ör:<br>XXXX.XX |
| 5 | Bülten Adı | Alfabetik | 32* | İlgili pay için raporun alındığı tarih aralığının son<br>gününde geçerli olan bülten adı bilgisidir. |
| 6 | Özel İşlem<br>Bildirimi İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında, ilgili payda<br>gerçekleşen Özel İşlem Bildirimi işlemlerinin<br>toplam hacim bilgisidir. |
| 7 | Özel İşlem<br>Bildirimi İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen Özel İşlem Bildirimi işlemlerinin<br>toplam işlem miktarı bilgisidir. |
| 9 | Açılış Seansı İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında açılış seansında<br>ilgili payda gerçekleşen işlemlerin toplam hacim<br>bilgisidir. |
| 8 | Toplam İşlem<br>Hacmi (TL) | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen işlemlerin toplam hacim bilgisidir. |

<!-- sayfa 19 -->
**[Sayfa 19]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 10 | Açılış Seansı İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında açılış seansında<br>ilgili payda gerçekleşen işlemlerin toplam işlem<br>miktarı bilgisidir. |
| 11 | Toplam İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında ilgili payda<br>gerçekleşen toplam işlem miktarı bilgisidir. |
| 12 | En Düşük Fiyat | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında gerçekleşen en<br>düşük fiyat bilgisidir. İlgili tarih aralığında<br>gerçekleştirilen sermaye artırımları/azaltımları ve<br>temettü ödemeleri vb özsermaye hallerine göre<br>düzeltilmiştir. |
| 13 | En Yüksek Fiyat | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığında gerçekleşen en<br>yüksek fiyat bilgisidir. İlgili tarih aralığında<br>gerçekleştirilen sermaye artırımları/azaltımları ve<br>temettü ödemeleri vb özsermaye hallerine göre<br>düzeltilmiştir. |
| 14 | Kapanış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Raporun alındığı tarih aralığındaki son kapanış<br>fiyatı bilgisidir. |

2.1.14 En Aktif 20 Pay

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_AKTIFUYE.W.YYYYHH.zip -> hisse20.xlsx |  | Haftalık olarak pay piyasasında en çok<br>işlem gerçekleştirilen 20 Pay<br>raporlanmaktadır. |
| Örnek Dosya Adı | PP_AKTIFUYE.W.201550.zip -><br>hisse20.xlsx |  |
| Örnek Dosya İçerikleri |  |  |
| GARAN.E;GARANTI BANKASI;Z; 4783581075.66; 22.1067 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili alan 32 karaktere kadar değer<br>alabilmektedir. Ör: XXXX.XX |
| 2 | Bülten Adı | Alfabetik | 32* | Bu alanda payın bülten adı bilgisi bulunmaktadır. |
| 3 | Pazar Kodu | Alfabetik | 4* | Bkz. Tablo 3.1.1 MarketSegment |
| 4 | İşlem Hacmi (TL) | Ondalıklı,Nü<br>merik | 20* | Payın özel işlem bildirimi hariç toplam işlem<br>hacmi bilgisidir. |
| 5 | Payı (%) | Ondalıklı,Nü<br>merik | 20* | Payın özel işlem bildirimi haricindeki diğer<br>işlemlerinin, özel işlem bildirimleri hariç ilgili<br>haftanın toplam işlem hacmi içindeki yüzde<br>oranıdır. |

<!-- sayfa 20 -->
**[Sayfa 20]**

2.1.15 En Aktif 20 Üye

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_AKTIFUYE.W.YYYYHH.zip -> uye20.xlsx |  | Haftalık olarak pay piyasasında en çok<br>işlemi gerçekleştiren 20 Üye<br>raporlanmaktadır. |
| Örnek Dosya Adı | PP_AKTIFUYE.W.201550.zip -><br>uye20.xlsx |  |
| Örnek Dosya İçerikleri |  |  |
| IYM;IS YATIRIM MENKUL DEGERLER A.S.; 2897266421.21;6.6947 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Üye Kodu | Alfabetik | 20* | Üye kodu bilgisidir. |
| 2 | Üye Adı | Alfabetik | 80* | Üye Adı bilgisidir. |
| 3 | İşlem Hacmi(TL) | Ondalıklı,Nü<br>merik | 20* | Üyenin özel işlem bildirimi hariç olmak üzere<br>ilgili haftada gerçekleştirmiş olduğu işlemlerin<br>toplam hacim bilgisidir. |
| 4 | Payı(%) | Ondalıklı,Nü<br>merik | 20* | Özel işlem bildirimi hariç olmak üzere üyenin<br>gerçekleştirmiş olduğu işlemlerin, özel işlem<br>bildirimleri hariç ilgili haftanın toplam hacmi<br>içindeki yüzde oranıdır. |

2.1.16 Gün İçi Emir Defteri Bilgileri

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_GUNICIEMIR.M.YYYYAA.zip -><br>PP_GUNICIEMIR.M.YYYYAA.csv |  | Aylık bazda tüm emir bilgileri<br>raporlanmaktadır. |
| Örnek Dosya Adı | PP_GUNICIEMIR.M.201511.zip<br>-><br>PP_GUNICIEMIR.M.201511.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 18.09.2015;5BB633C100002926;18.09.2015 11:20;18.09.2015<br>11:20;ADANA.E;S;1;0;1;DAY;1;6;100;100;100;5.01;H;P_KESIR_SUREK_ISLEM;5;5.01;;;0;H;2;18.09.<br>2015 11:20 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Emrin girildiği Tarih bilgisidir. |
| 2 | Emir No | Alfanümerik | 60* | Sistem Açılış Zamanı, Partition Bilgisi ve tekil<br>bir değer içermektedir. Emrin sırası ile ilgili bir<br>bilgi içermemektedir. |
| 3 | Emir Giriş Tarihi<br>Ve Zamanı | Alfanümerik | 19* | Emrin giriş tarihini ve zamanını gösterir. Tarih<br>ve zaman arasında boşluk karakteri vardır. |
| 4 | Emir Değiştirilme<br>Tarihi Ve Zamanı | Alfanümerik | 19* | Emrin değiştirilme tarihini ve zamanını<br>gösterir. Tarih ve zaman arasında boşluk<br>karakteri vardır. Tüm emir defterindeki<br>sıralama bu kolondaki değer üzerinden<br>yapılmaktadır. |

<!-- sayfa 21 -->
**[Sayfa 21]**


| 5 | İşlem Kodu | Alfanümerik | 32* | Bu alanda enstrümanın seri kodu yer alır. İlgili<br>alan 32 karaktere kadar değer alabilmektedir.<br>Ör: XXXX.XX |
|---|---|---|---|---|
| 6 | Alış/Satış | Alfanümerik | 1 | A : Alış, S : Satış |
| 7 | Emir Fiyat Türü | Nümerik | 4* | Bkz. Tablo 3.1.1 OrderType |
| 8 | Emir Tipi | Nümerik | 4* | Bkz. Tablo 3.1.2 ExchangeOrderType |
| 9 | Emir Kategorisi | Nümerik | 4* | İlgili kaydın bir emre, kotasyona ya da özel<br>işlem bildirimine mi ait olduğunu belirtir.<br>Bkz. Tablo 3.1.3 OrderCategory |
| 10 | Emrin Geçerlilik<br>Turu | Nümerik | 15* | Bkz. Tablo 3.1.8 OrderDurationID |
| 11 | Emir Durumu | Nümerik | 4* | Emrin geçerlilik durumuna ilişkin bilgi verir.<br>Aktif olup olmadığını vb. bilgileri içerir.<br>Bkz. Tablo 3.1.7 OrderStatus |
| 12 | Emir Değişiklik<br>Sebebi | Nümerik | 4* | Emir üzerindeki değişikliğin sebebini gösterir.<br>Örneğin işlem görme, iptal, miktar değişikliği<br>vb.<br>Bkz. Tablo 3.1.4 ChangeReason |
| 13 | Emir Miktarı | Nümerik | 20* | Gönderilen emrin miktarını göstermektedir.<br>Emir üzerinde üye tarafından yapılan miktar<br>değişiklerini bu alanda görülecek ancak emrin<br>işleme dönüşmesi sonrası değişen miktar<br>bilgisi bu alanda görünmeyecektir. |
| 14 | Kalan Miktar | Nümerik | 20* | İlgili kayıt sonrası emrin kalan miktarını<br>göstermektedir. |
| 15 | Görünen Miktar | Nümerik | 20* | 2. Fazda kullanımına başlanacak Iceberg<br>emirlerinin kullanımına yöneliktir. |
| 16 | Fiyat | Ondalıklı,<br>nümerik | 20* | Emrin ilgili kayıtta geçerli olan fiyatını<br>göstermektedir. |
| 17 | Acente / Fon Kodu<br>Flag (Afk) | Alfabetik | 16* | Girilmemişse H girilmişse E karakteri görülür. |
| 18 | Seans | Alfanümerik | 40* | İlgili Emrin ait olduğu seansın bilgisini verir.<br>Bkz. Tablo 3.1.13. |
| 19 | En İyi Alış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Emir girildikten sonraki en iyi alış fiyatı<br>bilgisini verir. |
| 20 | En İyi Satış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Emir girildikten sonraki en iyi satış fiyatı<br>bilgisini verir. |
| 21 | Önceki Emir<br>Numarası | Alfanümerik | 20* | Bir önceki kotasyon emrinin numarasını<br>gösterir. |
| 22 | Ortak Sözleşme No | Alfanümerik | 20* | Alış ve satış işlemleri için oluşan üye işlem<br>numaralarının birleştirilmesi ile oluşan tekil<br>(unique) numaradır. |
| 23 | İşlem Adedi | Ondalıklı,Nümerik | 20* | Gerçekleşen işlemin miktarını gösterir. |
| 24 | Giveup Flag | Alfabetik | 1* | Give-up'lı bir emir ise E karakteri değilse H<br>karakteri görülür. |

<!-- sayfa 22 -->
**[Sayfa 22]**

| 25 | Güncelleme Numarası | Alfanümerik | 20* | Emir güncelleme numarasıdır. |
|---|---|---|---|---|
| 26 | Güncelleme<br>Zamanı | Alfanümerik | 20* | Emir güncelleme zamanı bilgisini verir. |

2.1.17 Gün İçi İşlem Defteri Bilgileri

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_GUNICIISLEM.M.YYYYAA.zip -><br>PP_GUNICIISLEM.M.YYYYAA.csv |  | Aylık Bazda işlem defteri bilgileri<br>raporlanmaktadır. |
| Örnek Dosya Adı | PP_GUNICIISLEM.M.201511.zi<br>p -><br>PP_GUNICIISLEM.M.201511.cs<br>v |  |
| Örnek Dosya İçerikleri |  |  |
| 2015-11-<br>09;ADANA.E;933438100000001;;A;1;5;5;5C00A401000020FB;18:48:55;1;P_SUREKLI_ISLEM;1;<br>;P;505;23;2015-11-09 16:48:55;H;1;2015-11-09 18:48:55 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | İşlemin yapıldığı tarih bilgisidir. |
| 2 | İşlem Kodu | Alfabetik | 32* | Bu alanda Seri kodu işlem kodu içerisinde yer<br>alır. İlgili alan 32 karaktere kadar değer<br>alabilmektedir. Ör: XXXX.XX |
| 3 | Ortak Sozlesme No | Alfanümerik | 20* | Alış ve satış işlemleri için oluşan üye işlem<br>nolarının birleştirilmesi ile oluşan tekil (unique)<br>numaradır. |
| 4 | Üye İşlem No | Alfanümerik | 70* | Üyenin her bir alış ve satış işlemi için oluşan tek<br>işlem numarasıdır.Bu alan boş gelmektedir. |
| 5 | Alış/Satış | Alfabetik | 1 | A : Alış, S : Satış |
| 6 | İşlem Adedi | Nümerik | 20* | Gerçekleşen işlemin miktarını gösterir |
| 7 | İşlem Fiyatı | Ondalıklı,Nümerik | 20* | Gerçekleşen işlemin fiyatını gösterir. |
| 8 | İşlem Hacmi | Ondalıklı,Nümerik | 20* | İşlem Fiyatı ile İşlem Adedinin çarpılması ile<br>elde edilir. |
| 9 | Emir No | Alfanümerik | 60* | Sistem Açılış Zamanı, Partition Bilgisi ve tekil<br>bir değer içermektedir. Emrin sırası ile ilgili bir<br>bilgi içermemektedir. |
| 10 | İşlem Zamanı | Alfanümerik | 10* | Burada saniyeye kadar HH24:MI:SS formatında<br>zaman bilgisi yazılacaktır. |
| 11 | Normal İşlem/ Özel<br>İşlem Bildirimi | Nümerik | 4* | Bkz. Tablo 3.1.11 DealSource |
| 12 | Seans | Alfanümerik | 40* | İlgili İşlemin ait olduğu seansın bilgisini verir.<br>Bkz. Tablo 3.1.13 |

<!-- sayfa 23 -->
**[Sayfa 23]**

| 13 | İşlem Durumu | Alfabetik | 4* | Bkz. Tablo 3.1.14 TradeType |
|---|---|---|---|---|
| 14 | Takas Tarihi | Alfanümerik | 10 | İşlemin takasının gerçekleşeceği günü<br>göstermektedir. |
| 15 | Aktif/Pasif | Alfabetik | 1 | İşlemin aktif ya da pasif olduğunu<br>göstermektedir. P:Pasif, A:Aktif |
| 16 | Takas Tarafı İşlem<br>No | Nümerik | 19* | CW ekranlarından görülen işlemin her bir<br>tarafının numarasını göstermektedir. |
| 17 | Takas Tarafı Ortak<br>Anlaşma No | Nümerik | 19* | CW ekranlarından görülen alış ve satış tarafları<br>için ortak anlaşma numarasını göstermektedir. |
| 18 | İşlemin Değistirilme<br>Tarihi Ve Zamanı | Alfanümerik | 19* | İşlemin oluşma veya son değişim zamanı<br>bilgisini göstermektedir. |
| 19 | Giveup Flag | Alfabetik | 1 | Give-up'lı bir işlem E değil ise H karakteri<br>gösterilir. |
| 20 | Güncelleme<br>Numarası | Alfanümerik | 20* | İşlem değiştirme veya iptal olduğunda bu işleme<br>ilişkin bir güncelleme numarası verilir. |
| 21 | Güncelleme Zamanı | Alfanümerik | 20* | İşlemin değiştirilme veya iptal zamanını<br>göstermektedir. |

2.1.18 Günsonu Fiyat ve İşlem Hacmi Bilgileri

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_GUNSONUFIYATHACIM.M.YYYYAA.zip -><br>PP_GUNSONUFIYATHACIM.M.YYYYAA.csv |  | Aylık olarak Gün Sonu Fiyat ve İşlem<br>Hacmi Bilgileri raporlanmaktadır. |
| Örnek Dosya Adı | PP_GUNSONUFIYATHACIM.<br>M.201511.zip -><br>PP_GUNSONUFIYATHACIM.<br>M.201511.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 2015-11-09;ADANA.E;ADANA CIMENTO A<br>GRUBU;A;Z;MSPOT;EQT;MSPOTEQT;MSPOTEQTADANA;SI;0;0;0;0;;0;0;6.93;0;6.93;6.74;9.98;9.9<br>8;9.98;0;8;9.98;6.979;109682.86;15717;175;0;5945.94;858;42;0;0;0;59.88;6;1;0;0;0;7;9.12;7;70018.24;10<br>002;84;0;0;0;0;0;0;0;0;0 |  |  |


| Sira | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | İşlem tarihini göstermektedir. |
| 2 | İşlem Kodu | Alfabetik | 32* | Bu alanda enstrüman seri kodu yer almaktadır.<br>İlgili alan 32 karaktere kadar değer alabilmektedir.<br>Ör: XXXX.XX |
| 3 | Bülten Adı | Alfabetik | 255* | İlgili seriyi tanımlamak için oluşturulan unvandan<br>farklı olan uzun ID’dir. |
| 4 | A, B, C, D Grubu | Alfabetik | 1 | Paylar dahil oldukları gruplara göre A, B, C veya<br>D değerlerini alabilirler. |
| 5 | Pazar | Alfabetik | 1 | Bkz. Tablo 3.1.5 MarketSegment |
| 6 | Yapısal Bazda | Alfabetik | 50* | Bkz. Tablo 3.1.6 Market |

<!-- sayfa 24 -->
**[Sayfa 24]**

Piyasa Alt Bölümü

| 7 | Enstrüman Grubu | Alfabetik | 14* | İlgili enstrümanın hangi gruba dahil olduğu<br>bilgisini vermektedir. Ör: ECW: Avrupa Tipi Alış<br>Varantları, EQT: Pay, SP: Spot Endeks vs. |
|---|---|---|---|---|
| 8 | Enstrüman Tipi | Alfabetik | 14* | İlgili enstrümanın tipinin ne olduğu bilgisini<br>vermektedir. Ör: BUYINEQT, MSPOTECW,<br>MSPOTRGT, MSPOTETF vs. |
| 9 | Enstrüman Sınıfı | Alfabetik | 14* | İlgili enstrümanın hangi class’a ait olduğu bilgisini<br>vermektedir. Ör: BUYINEQTGARAN,<br>BUYINECWGARDBL, MSPOTEQTGARAN vs. |
| 10 | İşlem Yöntemi | Alfabetik | 2 | Sİ: Sürekli İşlem, TF: Tek Fiyat PY: Piyasa<br>Yapıcılı |
| 11 | Piyasa Yapıcı | Nümerik | 1 | 0: Yok, 1:Var |
| 12 | BIST 100 Endeks | Nümerik | 1 | 0: Dahil değil, 1: Dahil |
| 13 | BIST 30 Endeks | Nümerik | 1 | 0: Dahil değil, 1: Dahil |
| 14 | Brüt Takas | Nümerik | 1 | 1: Brüt Takas; 0: Brüt Takas Değil |
| 15 | Özsermaye Hali | Alfanümerik | 17* | Aynı tarihte en fazla 6 tane Öz sermaye hali<br>oluşabilir. Bu durumda değerler birbirlerinden “-”<br>işareti ile ayrılır.<br>Bkz. Tablo 3.1.12 Corporate Action |
| 16 | Geçici Durdurma | Nümerik | 1 | 0: Açık, 1: Kapalı |
| 17 | Önceki Kapanış<br>Fiyatı | Ondalıklı,<br>Nümerik | 20* | İlgili rapor gününden önceki en son kapanış<br>fiyatıdır. |
| 18 | Açılış Fiyatı | Ondalıklı,<br>Nümerik | 20* | İlgili rapor gününde oluşan ilk fiyatıdır. |
| 19 | Açılış Seansı Fiyatı | Ondalıklı,<br>Nümerik | 20* | Açılış seansında oluşan fiyattır. |
| 20 | Gün ortası seansı<br>Fiyatı | Ondalıklı,<br>Nümerik | 20* | Gün ortası tek fiyat emir toplama sonrası oluşan<br>fiyattır. |
| 21 | En Düşük Fiyat | Ondalıklı,<br>Nümerik | 20* | Gün içinde oluşan en düşük fiyattır. |
| 22 | En Yüksek Fiyat | Ondalıklı,<br>Nümerik | 20* | Gün içinde oluşan en yüksek fiyattır. |
| 23 | Kapanış Fiyatı | Ondalıklı,<br>Nümerik | 20* | İlgili işlem gününde en son oluşan fiyatı<br>göstermektedir. |
| 24 | Kapanış Seansı<br>Fiyatı | Ondalıklı,<br>Nümerik | 20* | Kapanış seansında oluşan fiyattır. |
| 25 | Değişim (%) | Ondalıklı,<br>Nümerik | 20* | Bir önceki işlem günü kapanış fiyatına göre yüzde<br>(%) değişimi göstermektedir. |
| 26 | Bekleyen En İyi Alış<br>Fiyatı | Ondalıklı,<br>Nümerik | 20* | İşlem günü sonunda alış tarafında en iyi kademede<br>bekleyen emrin fiyatıdır. |
| 27 | Bekleyen En İyi<br>Satış Fiyatı | Ondalıklı,<br>Nümerik | 20* | İşlem günü sonunda satış tarafında en iyi<br>kademede bekleyen emrin fiyatıdır. |
| 28 | A.O.F. | Ondalıklı,<br>Nümerik | 20* | İşlem günü içinde gerçekleşen işlemlerin miktar<br>ağırlıklı ortalama fiyatıdır. |
| 29 | Toplam İşlem Hacmi | Ondalıklı,<br>Nümerik | 20* | Toplam işlem hacmidir. |
| 30 | Toplam İşlem Adedi | Ondalıklı,<br>Nümerik | 20* | Toplam işlem miktarıdır. |
| 31 | Toplam Sözleşme<br>Sayısı | Nümerik | 20* | Toplam sözleşme sayısıdır. |
| 32 | Referans Fiyat | Ondalıklı,<br>Nümerik | 20* | Enstrüman için baz fiyata esas teşkil etmeyen,<br>Borsa tarafından referans olarak alınmak üzere ilan<br>edilen fiyattır. |
| 33 | Açılış Seansı İşlem | Ondalıklı, | 20* | Açılış seansında oluşan toplam işlem hacmidir. |

<!-- sayfa 25 -->
**[Sayfa 25]**

Hacmi Nümerik

| 34 | Açılış Seansı İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Açılış seansında oluşan toplam işlem miktarıdır. |
|---|---|---|---|---|
| 35 | Açılış Seansı<br>Sözleşme Sayısı | Nümerik | 20* | Açılış seansında oluşan toplam sözleşme sayısıdır. |
| 36 | Gün ortası<br>Müzayede İşlem<br>Hacmi | Ondalıklı,<br>Nümerik | 20* | Günortası Müzayede seansında oluşan toplam<br>işlem hacmidir. |
| 37 | Gün ortası<br>Müzayede İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Günortası Müzayede seansında oluşan toplam<br>işlem miktarıdır. |
| 38 | Gün ortası<br>Müzayede Sözleşme<br>Sayısı | Nümerik | 20* | Günortası Müzayede seansında oluşan toplam<br>sözleşme sayısıdır. |
| 39 | Kapanış Seansı<br>İşlem Hacmi | Ondalıklı,<br>Nümerik | 20* | Kapanış seansında oluşan toplam işlem hacmidir. |
| 40 | Kapanış Seansı<br>İşlem Miktarı | Ondalıklı,<br>Nümerik | 20* | Kapanış seansında oluşan toplam işlem miktarıdır. |
| 41 | Kapanış Seansı<br>Sözleşme Sayısı | Nümerik | 20* | Kapanış seansında oluşan toplam sözleşme<br>sayısıdır. |
| 42 | Kapanış Fiyatından<br>İşlemler İşlem<br>Hacmi | Ondalıklı,<br>Nümerik | 20* | Kapanış Fiyatından İşlemler seansında oluşan<br>toplam işlem hacmidir. |
| 43 | Kapanış Fiyatından<br>İşlemler İşlem<br>Miktarı | Ondalıklı,<br>Nümerik | 20* | Kapanış Fiyatından İşlemler seansında oluşan<br>toplam işlem miktarıdır. |
| 44 | Kapanış Fiyatından<br>İşlemler Sözleşme<br>Sayısı | Nümerik | 20* | Kapanış Fiyatından İşlemler seansında oluşan<br>toplam sözleşme sayısıdır. |
| 45 | En Düşük Açığa<br>Satış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Gün içinde açığa satış emri ile gerçekleşen<br>işlemlerin en düşük fiyatıdır. |
| 46 | En Yüksek Açığa<br>Satış Fiyatı | Ondalıklı,<br>Nümerik | 20* | Gün içinde açığa satış emri ile gerçekleşen<br>işlemlerin en yüksek fiyattıdır. |
| 47 | Açığa Satış A.O.F. | Ondalıklı,<br>Nümerik | 20* | Gün içinde açığa satış emri ile gerçekleşen<br>işlemlerin miktar ağırlıklı ortalama fiyatıdır. |
| 48 | Açığa Satış İşlem<br>Hacmi | Ondalıklı,<br>Nümerik | 20* | Açığa satış işlemleri toplam işlem hacmidir. |
| 49 | Açığa Satış İşlem<br>Adedi | Ondalıklı,<br>Nümerik | 20* | Açığa satış işlemleri toplam işlem miktarıdır. |
| 50 | Açığa Satış<br>Sözleşme Sayısı | Nümerik | 20* | Açığa satış işlemleri toplam sözleşme sayısıdır. |
| 51 | Özel İşlem Bildirimi<br>En Düşük Fiyat | Ondalıklı,<br>Nümerik | 20* | İşlem günündeki en düşük özel işlem bildirimi<br>fiyatıdır. |
| 52 | Özel İşlem Bildirimi<br>En Yüksek Fiyat | Ondalıklı,<br>Nümerik | 20* | İşlem günündeki en yüksek özel işlem bildirimi<br>fiyatıdır. |
| 53 | Özel İşlem Bildirimi<br>A.O.F. | Ondalıklı,<br>Nümerik | 20* | İşlem günündeki özel işlem bildirimi miktar<br>ağırlıklı ortalama fiyatıdır. |
| 54 | Özel İşlem Bildirimi<br>İşlem Hacmi | Ondalıklı,<br>Nümerik | 20* | Özel İşlem Bildirimi işlemleri toplam işlem<br>hacmidir. |
| 55 | Özel İşlem Bildirimi<br>İşlem Adedi | Ondalıklı,<br>Nümerik | 20* | Özel İşlem Bildirimi işlemleri toplam işlem<br>miktarıdır. |
| 56 | Özel İşlem Bildirimi<br>Sözleşme Sayısı | Nümerik | 20* | Özel İşlem Bildirimi işlemleri toplam sözleşme<br>sayısıdır. |

<!-- sayfa 26 -->
**[Sayfa 26]**

2.1.19 Gün İçi Endeks Bilgileri (Bütün Endeksler)

| Dosya Adı |  | Açıklama |
|---|---|---|
| PP_GUNICITUMENDEKS.M.YYYYAA.zip-><br>PP_GUNICITUMENDEKS.M.YYYYAA.csv |  | Aylık olarak Fiyat Endekslerinin gün<br>içinde hesaplanan tüm değerleri zaman<br>sıralı olarak raporlanmaktadır. |
| Örnek Dosya Adı | PP_GUNICITUMENDEKS.M.20<br>1511.zip-><br>PP_GUNICITUMENDEKS.M.20<br>1511.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 30.11.2015;09:29:50;XU100;BIST100;75638.43 |  |  |


| S ı ra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | İşlem tarihi (GG.AA.YYYY) |
| 2 | Zaman | Alfanümerik | 20* | Zaman bilgisidir HH:MI:SEC |
| 3 | Endeks Kodu | Alfanümerik | 400* | Endeks kodu bilgisidir. Örneğin XU100 |
| 4 | Endeksler | Alfanümerik | 400* | Endeks Türkçe Adı |
| 5 | Fiyat Endeksi Değeri | Ondalıklı,<br>Nümerik | 20* | İlgili endeksin ilgili tarih ve zamandaki değeri. |

2.1.20 Gün Sonu Endeks ve İşlem Hacmi Bilgileri

| Dosya Adı |  |  |  |  |  | Açıklama |
|---|---|---|---|---|---|---|
| PP_GUNSONUENDEKSHACIM.M.YYYYAA.zip-><br>PP_GUNSONUENDEKSHACIM.M.YYYYAA.csv |  |  |  |  |  | Aylık olarak günlük bazda günsonu<br>endeks ve işlem hacmi bilgileri<br>raporlanmaktadır. |
| Örnek Dosya Adı |  | PP_GUNSONUENDEKSHACIM<br>.M.201511.zip-><br>PP_GUNSONUENDEKSHACIM<br>.M.201511.csv |  |  |  |  |
| Örnek Dosya İçerikleri |  |  |  |  |  |  |
| 30.11.2015;XU100;BIST<br>100;Fiyat;2109275.901;75232.79;75097.07;76535.24;3124100481.88;502916480 |  |  |  |  |  |  |
| Sıra | Alan Adı |  | Alan Türü | Uzunluk | Açıklama |  |
| 1 | Tarih |  | Alfanümerik | 10 | İşlem tarihi (GG.AA.YYYY) bilgisidir. |  |
| 2 | Endeks Kodu |  | Alfanümerik | 400* | Endeks kod bilgisidir. |  |
| 3 | Endeksler |  | Alfanümerik | 400* | Endeks Türkçe Adı |  |

<!-- sayfa 27 -->
**[Sayfa 27]**

| Dosya Adı |  |  |  |  | Açıklama |
|---|---|---|---|---|---|
| 4 | Endeks Türü | Alfabetik | 20* | Fiyat veya Getiri endeks türü bilgisidir. |  |
| 5 | Bölen | Ondalıklı,Nüm<br>erik | 20* | Endeksin ilgili tarihteki bölen değeridir. |  |
| 6 | Kapanış Değeri | Ondalıklı,Nüm<br>erik | 20* | Endeksin ilgili tarihteki kapanış değeridir. |  |
| 7 | En Düşük | Ondalıklı,Nüm<br>erik | 20* | Endeksin ilgili tarihteki en düşük değeridir. |  |
| 8 | En Yüksek | Ondalıklı,Nüm<br>erik | 20* | Endeksin ilgili tarihteki en yüksek değeridir. |  |
| 9 | İşlem Hacmi | Ondalıklı,Nüm<br>erik | 20* | Endekse dahil olan payların ilgili tarihteki işlem<br>hacmi bilgisidir. |  |
| 10 | İşlem Miktarı | Ondalıklı,Nüm<br>erik | 20* | Endekse dahil olan payların ilgili tarihteki işlem<br>miktarı bilgisidir. |  |

2.1.21 Yıl İçinde Gerçekleştirilen Bedelli Sermaye Artırımları ve Nakit Temettüler

| Dosya Adı |  | Açıklama |
|---|---|---|
| NakitSerTem[YYYY].zip-> NakitSerTem[YYYY].xls |  | Bu rapor yıl içinde gerçekleştirilen<br>bedelli sermaye artırımlarının, nakit<br>temettü (kar payı) ödemelerinin, birleşme<br>ve devralma nedeniyle gerçekleştirilen<br>sermaye artırımlarının ay bazında toplam<br>tutarlarını Bin TL ve Milyon ABD doları<br>olarak gösterir. |
| Örnek Dosya Adı | NakitSerTem2015.zip-><br>NakitSerTem2015.xls |  |
| Örnek Dosya İçerikleri |  |  |
| Haziran;June;97,000.00;36.24;888,564.00;327.57;---;---;317,939;118.52 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Ay (TR) | Alfabetik | 7* | Ayın Türkçe adı |
| 2 | Ay (EN) | Alfabetik | 9* | Ayın İngilizce adı |
| 3 | Rüçhan Hakkı<br>Kullandırılarak<br>Gerçekleştirilen<br>Bedelli Sermaye<br>Artırımı (Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından rüçhan hakkı<br>kullandırılarak gerçekleştirilen bedelli sermaye<br>artırım tutarı ile rüçhan hakkı kullandırma<br>fiyatının çarpımlarının ay bazında toplam tutarı<br>ve yıllık toplam tutarlarıdır. (Bin TL olarak) |

<!-- sayfa 28 -->
**[Sayfa 28]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 4 | Rüçhan Hakkı<br>Kullandırılarak<br>Gerçekleştirilen<br>Bedelli Sermaye<br>Artırımı (Milyon<br>ABD$) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından rüçhan hakkı<br>kullandırılarak gerçekleştirilen bedelli sermaye<br>artırım tutarı ile rüçhan hakkı kullandırma<br>fiyatının çarpımlarının ay bazında toplam<br>tutarları ve yıllık toplam tutarlarıdır. (Milyon<br>ABD$ olarak) |
| 5 | Rüçhan Hakkı<br>Kullandırılmadan<br>Gerçekleştirilen<br>Bedelli Sermaye<br>Artırımı (Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından rüçhan hakkı<br>kullandırılmadan gerçekleştirilen bedelli<br>sermaye artırım tutarı ile pay satış fiyatının<br>çarpımlarının ay bazında toplam tutarları ve<br>yıllık toplam tutarlarıdır. (Bin TL olarak) |
| 6 | Rüçhan Hakkı<br>Kullandırılmadan<br>Gerçekleştirilen<br>Bedelli Sermaye<br>Artırımı (Milyon<br>ABD$) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından Rüçhan hakkı<br>kullandırılmadan gerçekleştirilen bedelli<br>sermaye artırım tutarı ile pay satış fiyatının<br>çarpımlarının ay bazında toplam tutarları ve<br>yıllık toplam tutarlarıdır. (Milyon ABD$ olarak) |
| 7 | Birleşme ve<br>Devralma (Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından birleşme ve<br>devralma nedeniyle gerçekleştirilen sermaye<br>artırımlarının ay bazında toplam tutarları ve<br>yıllık toplam tutarlarıdır. (Bin TL olarak) |
| 8 | Birleşme ve<br>Devralma (Milyon<br>ABD$) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından birleşme ve<br>devralma nedeniyle gerçekleştirilen sermaye<br>artırımlarının ay bazında toplam tutarları ve<br>yıllık toplam tutarlarıdır. (Milyon ABD$ olarak) |
| 9 | Nakit Temettü Brüt<br>Toplam Tutarı (Bin<br>TL) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından nakit olarak<br>ödenen brüt temettülerin ay bazında toplam<br>tutarları ve yıllık toplam tutarlarıdır. (Bin TL<br>olarak) |
| 10 | Nakit Temettü Brüt<br>Toplam Tutarı<br>(Milyon ABD$) | Ondalıklı,<br>nümerik | 20* | İlgili yılda şirketler tarafından nakit olarak<br>ödenen brüt temettülerin ay bazında toplam<br>tutarları ve yıllık toplam tutarlarıdır. (Milyon<br>ABD$ olarak) |

<!-- sayfa 29 -->
**[Sayfa 29]**

2.1.22 Tarih Bazında Sermaye Artırımı, Temettü Ödemesi ve Benzeri Şirket Bilgileri

| Dosya Adı |  | Açıklama |
|---|---|---|
| SERMAYE_ARTIRIMI_[YYYYAAGG].csv |  | Bu rapor ilgili tarih itibariyle bedelli,<br>bedelsiz sermaye artırımı, sermaye<br>azaltımı, nakit kar payı ödemesi,<br>birleşme ve devralma nedeniyle sermaye<br>artırımı gerçekleştiren şirketlerin listesini<br>ve bu şirketlerin ilgili bilgilerini gösterir. |
| Örnek Dosya Adı | SERMAYE_ARTIRIMI_201604<br>18.csv |  |
| Örnek Dosya İçerikleri |  |  |
| 18.04.2016;CRFSA;CARREFOURSA;113839302.57;;;;;;;;;586160697.43;514.90186;;;700000000;Kaydi<br>Pay/Shares;;;; |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Başlangıç Tarihi<br>(GG.AA.YY) | Alfanümerik | 10 | Hak kullanımının gerçekleşeceği ilk gün |
| 2 | Pay Kodu | Alfabetik | 32* | İlgili payın kodu |
| 3 | Pay Adı | Alfabetik | 32* | İlgili payın adı |
| 4 | Önceki Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili payın hak kullanımı öncesi toplam<br>sermaye tutarıdır. |
| 5 | Azaltılan Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için azaltılacak sermaye tutarıdır. |
| 6 | Rüçhan Hakkı<br>Kullandırılarak<br>Artırılan Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için mevcut ortaklara rüçhan hakkı<br>kullandırılarak gerçekleştirilen bedelli sermaye<br>artırım tutarıdır. |
| 7 | Rüçhan Hakkı<br>Kullandırılarak<br>Artırılan Sermaye<br>(%) | Ondalıklı,<br>nümerik | 20* | İlgili pay için mevcut ortaklara rüçhan hakkı<br>kullandırılarak gerçekleştirilen bedelli sermaye<br>artırım tutarının, artırımdan önceki sermaye<br>tutarından varsa azaltılan sermaye tutarının<br>düşülmesiyle bulunan tutara yüzde olarak<br>oranıdır. |
| 8 | Rüçhan Hakkı<br>Kullandırma Fiyatı<br>(TL) | Ondalıklı,<br>nümerik | 20* | 1TL nominal değerli 1 adet pay için rüçhan<br>hakkı kullanma fiyatıdır. |

<!-- sayfa 30 -->
**[Sayfa 30]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 9 | Rüçhan Hakkı<br>Kısıtlanarak<br>Artırılan Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | Mevcut ortakların rüçhan hakları kısıtlanarak<br>gerçekleştirilen bedelli sermaye artırımı<br>tutarıdır. |
| 10 | Rüçhan Hakkı<br>Kısıtlanarak<br>Artırılan Sermaye<br>(%) | Ondalıklı,<br>nümerik | 20* | Mevcut ortakların rüçhan hakları kısıtlanarak<br>gerçekleştirilen bedelli sermaye artırımı<br>tutarının, artırımdan önceki sermaye tutarından<br>varsa azaltılan sermaye tutarının düşülmesiyle<br>bulunan tutara yüzde olarak oranıdır. |
| 11 | Rüçhan Hakkı<br>Kısıtlanarak<br>Artırılan Sermaye<br>Fiyat (TL) | Ondalıklı,<br>nümerik | 20* | Mevcut ortakların rüçhan hakları kısıtlanarak<br>gerçekleştirilen bedelli sermaye artırımında 1TL<br>nominal değerli payın satış fiyatıdır. |
| 12 | Birleşme Devralma<br>Nedeniyle Artırılan<br>Sermaye (TL) | Ondalıklı,<br>nümerik | 20* | Birleşme devralma nedeniyle artırılan sermaye<br>tutarıdır. |
| 13 | İç Kaynaklardan<br>Bedelsiz Artırılan<br>Sermaye (TL) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanmak suretiyle bedelsiz<br>olarak artırılan sermaye tutarıdır. |
| 14 | İç Kaynaklardan<br>Bedelsiz Artırılan<br>Sermaye (%) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanmak suretiyle bedelsiz<br>olarak artırılan sermaye tutarının, artırımdan<br>önceki sermaye tutarından varsa azaltılan<br>sermaye tutarının düşülmesiyle bulunan tutara<br>yüzde olarak oranıdır. |
| 15 | Temettüden<br>Bedelsiz Artırılan<br>Sermaye (TL) | Ondalıklı,<br>nümerik | 20* | Temettüden karşılanmak suretiyle bedelsiz<br>olarak artırılan sermaye tutarıdır. |
| 16 | Temettüden<br>Bedelsiz Artırılan<br>Sermaye (%) | Ondalıklı,<br>nümerik | 20* | Temettüden karşılanmak suretiyle bedelsiz<br>olarak artırılan sermaye tutarının, artırımdan<br>önceki sermaye tutarından varsa azaltılan<br>sermaye tutarının düşülmesiyle bulunan tutara<br>yüzde olarak oranıdır. |
| 17 | Ulaşılacak Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | Sermaye artırımı/azaltımı sonrası ulaşılacak<br>sermaye tutarıdır. |
| 18 | Artırılan Sermaye<br>Karşılığı (Kaydi<br>Pay/ Geçici Kaydi<br>Pay) | Alfabetik | 40* | Artırılan sermaye karşılığında pay sahiplerine<br>kaydi pay mı, geçici kaydi pay mı verileceği<br>bilgisidir. |
| 19 | Pay Başı Nakit Brüt<br>Kar Payı (TL) | Ondalıklı,<br>nümerik | 20* | 1 TL nominal değerli paya nakit olarak<br>ödenecek brüt kar payı tutarıdır. |
| 20 | Pay Başı Nakit Net<br>Kar Payı (TL) | Ondalıklı,<br>nümerik | 20* | 1 TL nominal değerli paya nakit olarak<br>ödenecek net kar payı tutarıdır. |

<!-- sayfa 31 -->
**[Sayfa 31]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 21 | Açıklamalar | Alfanümerik | 300* | İlgili günde gerçekleşen hak kullanımı ile ilgili<br>(eğer varsa) açıklamalar (Türkçe) |
| 22 | Notes | Alfanümerik | 300* | İlgili günde gerçekleşen hak kullanımı ile ilgili<br>(eğer varsa) açıklamalar (İngilizce) |

2.1.23 Değerleme Oranları (Aylık)

| Dosya Adı |  | Açıklama |
|---|---|---|
| degoran[YYYYAA].zip-> ORAN[YYYYAA].xls |  | İlgili ay sonu itibariyle; pay, pazar,<br>sektör ve endeks bazında piyasa değeri,<br>net kar, nakit net temettü, özsermaye<br>bilgileri ile, fiyat kazanç oranı, temettü<br>verimi oranı ve piyasa değerinin defter<br>değerine oranını gösterir. Şirket payları<br>bulundukları sektörlere göre<br>gruplandırılarak listelenmiştir. |
| Örnek Dosya Adı | degoran201511.zip -><br>ORAN201511.xls |  |
| Örnek Dosya İçerikleri |  |  |
| YILDIZ PAZAR;YILDIZ PAZAR<br>TOPLAM/ORT.;488,567,791;36,125,095;14,253,126;362,505,425;13.52;2.92;1.35 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Pazar Adı veya Pay<br>Kodu | Alfabetik | 90* | Piyasa değeri, net kar vb. bilgileri verilen payın<br>kodu ya da pazarın adı |
| 2 | Pay adı, Endeks<br>Adı, Sektör Adı<br>veya Pazar Adı | Alfanümerik | 130* | İlgili payın, pazarın, sektörün ya da endeksin adı |
| 3 | Piyasa Değeri (Bin<br>TL) | Ondalıklı,<br>nümerik | 20* | İlgili payın veya ilgili endekste/sektörde/pazarda<br>yer alan payların ayın son iş gününe ait toplam<br>piyasa değeridir. (*1000) |
| 4 | Net Kar (Son 4<br>Çeyrek) (Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin ya da ilgili<br>endekste/sektörde/pazarda yer alan tüm şirketlerin<br>son 4 üçer aylık dönemde elde ettiği net karlar-<br>zararlar toplamıdır. Gelişen İşletmeler Pazarı ve<br>Piyasa Öncesi İşlem Platformunda işlem gören<br>şirketler için son 2 altışar aylık dönemde elde<br>edilen karlar-zararlar toplamıdır. (*1000) |
| 5 | Nakit Net Temettü<br>(Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin ya da ilgili<br>endekste/sektörde/pazarda yer alan tüm şirketlerin<br>bir önceki mali yıla ilişkin olarak<br>dağıttıkları/dağıtacakları toplam nakit net temettü<br>tutarıdır. Bir önceki mali döneme ilişkin nakit net<br>temettü tutarı belli olmayan şirketler için belli<br>olan son nakit net temettü tutarıdır. (*1000) |
| 6 | Özsermaye (Bin<br>TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirket ya da ilgili endekste/sektörde/pazarda<br>yer alan tüm şirketler için KAP’ta en son ilan<br>edilen finansal raporlardaki özsermaye<br>tutarlarıdır. (*1000) |

<!-- sayfa 32 -->
**[Sayfa 32]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 7 | F/K | Ondalıklı,<br>nümerik | 20* | Fiyat/Kazanç oranıdır. İlgili pay veya ilgili<br>endekste/sektörde/pazarda yer alan tüm paylar<br>için piyasa değerinin net kar (Son 4 Çeyrek)<br>tutarına bölünmesiyle hesaplanır. |
| 8 | TV(%) | Ondalıklı,<br>nümerik | 20* | Temettü verimi oranıdır. İlgili pay veya ilgili<br>endekste/sektörde/pazarda yer alan tüm paylar<br>için Nakit Net Temettünün, Piyasa Değerine<br>oranını yüzde olarak gösterir. |
| 9 | PD/DD | Ondalıklı,<br>nümerik | 20* | Piyasa değerinin defter değerine oranıdır. İlgili<br>pay veya ilgili endekste/sektörde/pazarda yer alan<br>tüm paylar için piyasa değerinin özsermaye<br>tutarına bölünmesiyle hesaplanır. |

2.1.24 Değerleme Oranları (Haftalık)

| Dosya Adı |  | Açıklama |
|---|---|---|
| degoran[YYYY].zip-> ORAN[YYYY].xls |  | İlgili hafta sonu itibariyle; pay, pazar,<br>sektör ve endeks bazında piyasa değeri,<br>net kar, nakit net temettü, özsermaye<br>bilgileri ile, fiyat kazanç oranı, temettü<br>verimi oranı ve piyasa değerinin defter<br>değerine oranını, gösterir. Şirket payları<br>bulundukları sektörlere göre<br>gruplandırılarak listelenmiştir. |
| Örnek Dosya Adı | degoran2016.zip -><br>ORAN2016.xls |  |
| Örnek Dosya İçerikleri |  |  |
| YILDIZ PAZAR;YILDIZ PAZAR<br>TOPLAM/ORT.;532,550,738;41,826,895;12,044,335;382,766,183;12.73;2.26;1.39 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Pazar Adı veya Pay<br>Kodu | Alfabetik | 90* | Piyasa değeri, net kar vb. bilgileri verilen payın<br>kodu ya da pazarın adı |
| 2 | Pay Adı, Endeks<br>Adı, Sektör Adı<br>veya Pazar Adı | Alfanümerik | 130* | İlgili payın, pazarın, sektörün ya da endeksin adı |
| 3 | Piyasa Değeri (Bin<br>TL) | Ondalıklı,<br>nümerik | 20* | İlgili payın veya ilgili endekste/sektörde/pazarda<br>yer alan payların haftanın son iş gününe ait<br>toplam piyasa değeridir. (*1000) |
| 4 | Net Kar (Son 4<br>Çeyrek) (Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin ya da ilgili<br>endekste/sektörde/pazarda yer alan tüm şirketlerin<br>son 4 üçer aylık dönemde elde ettiği net karlar-<br>zararlar toplamıdır. Gelişen İşletmeler Pazarı ve<br>Piyasa Öncesi İşlem Platformunda işlem gören<br>şirketler için son 2 altışar aylık dönemde elde<br>edilen karlar-zararlar toplamıdır. (*1000) |

<!-- sayfa 33 -->
**[Sayfa 33]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 5 | Nakit Net Temettü<br>(Bin TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin ya da ilgili<br>endekste/sektörde/pazarda yer alan tüm şirketlerin<br>bir önceki mali yıla ilişkin olarak<br>dağıttıkları/dağıtacakları toplam nakit net temettü<br>tutarıdır. Bir önceki mali döneme ilişkin nakit net<br>temettü tutarı belli olmayan şirketler için belli<br>olan son nakit net temettü tutarıdır. (*1000) |
| 6 | Özsermaye (Bin<br>TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirket ya da ilgili endekste/sektörde/pazarda<br>yer alan tüm şirketler için KAP’ta en son ilan<br>edilen finansal raporlardaki özsermaye<br>tutarlarıdır. (*1000) |
| 7 | F/K | Ondalıklı,<br>nümerik | 20* | Fiyat/Kazanç oranıdır. İlgili pay veya ilgili<br>endekste/sektörde/pazarda yer alan tüm paylar<br>için piyasa değerinin net kar (Son 4 Çeyrek)<br>tutarına bölünmesiyle hesaplanır. |
| 8 | TV(%) | Ondalıklı,<br>nümerik | 20* | Temettü verimi oranıdır. İlgili pay veya ilgili<br>endekste/sektörde/pazarda yer alan tüm paylar<br>için nakit net temettünün, piyasa değerine oranını<br>yüzde olarak gösterir. |
| 9 | PD/DD | Ondalıklı,<br>nümerik | 20* | Piyasa değerinin defter değerine oranıdır. İlgili<br>pay veya ilgili endekste/sektörde/pazarda yer alan<br>tüm paylar için piyasa değerinin özsermaye<br>tutarına bölünmesiyle hesaplanır. |

2.1.25 Aylık Değişimler ve Bileşik Getiriler (1993 – 2015)

| Dosya Adı |  | Açıklama |
|---|---|---|
| getiriler.zip-> Getiriler_[YYYYAAGG]_[YYYYAAGG].xlsx |  | 04.01.1993 tarihinden itibaren Borsa<br>İstanbul’da işlem gören tüm şirketlerin<br>TL ve ABD Doları bazında aylık değişim<br>ve bileşik getiri verilerini içeren<br>dosyadır. |
| Örnek Dosya Adı | getiriler.zip-><br>Getiriler_20151231_19930104.xls<br>x |  |
| Örnek Dosya İçerikleri |  |  |
| 31.12.2015;ZOREN;ZOREN;E;22.79;2.22;23.30;0.47 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih<br>(GG/AA/YYYY) | Alfanümerik | 10 | Günün tarihi |
| 2 | İlk Kod | Alfanümerik | 32* | 04.01.1993 tarihinden önce işlem görmeye<br>başlamış paylar için 04.01.1993 tarihinde geçerli<br>olan, bu tarihten sonra işlem görmeye başlamış<br>olan paylar için payın ilk işlem görmeye başladığı<br>tarihte geçerli olan kodu |
| 3 | Cari Kod | Alfanümerik | 32* | Payın rapor tarihi itibariyle geçerli olan kodu |

<!-- sayfa 34 -->
**[Sayfa 34]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 4 | Özellik Kodu | Alfabetik | 2* | Özellik kodu |
| 5 | TL - Aylık Değişim<br>(%) | Ondalıklı,<br>nümerik | 25* | İlgili payın özsermaye hallerine göre geriye doğru<br>düzeltilmiş TL bazlı fiyatındaki yüzde olarak<br>aylık değişim oranıdır. |
| 6 | TL - Bileşik Getiri | Ondalıklı,<br>nümerik | 25* | İlgili payın TL bazlı bileşik getirisidir. |
| 7 | ABD$ - Aylık<br>Değişim (%) | Ondalıklı,<br>nümerik | 25* | İlgili payın özsermaye hallerine göre geriye doğru<br>düzeltilmiş ABD Doları bazlı fiyatındaki yüzde<br>olarak aylık değişim oranıdır. |
| 8 | ABD$ - Bileşik<br>Getiri | Ondalıklı,<br>nümerik | 25* | İlgili payın ABD Doları bazlı bileşik getirisidir. |

2.1.26 Sermaye Artırımları (Aylık)

| Dosya Adı |  | Açıklama |
|---|---|---|
| serart[YYYYAA].zip->SERM[YYYYAA].xls |  | Dosyanın ait olduğu ay sonu itibariyle,<br>yıl içinde gerçekleşmiş veya<br>gerçekleşecek sermaye artırımlarını pay<br>ve şirket bazında gösteren rapordur.<br>Şirket bazında verilen tutarlar şirkete ait<br>tüm payların toplam tutarlarıdır. |
| Örnek Dosya Adı | serart201512.zip-><br>SERM201512.xls |  |
| Örnek Dosya İçerikleri |  |  |
| TREACSS00017;ACSEL;Eski;ACISELSAN ACIPAYAM SELÜLOZ SANAYİ VE TİCARET<br>A.Ş.;ACIPAYAM<br>SELULOZ;;1083600;;;;;;;;;;;9638100;889.45182;;;;01.12.2015;;01.12.2015;ACSEL(Eski),TREACSS0001<br>7;PAY-ANA PAZAR; |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | ISIN | Alfanümerik | 12 | İlgili payın 12 haneli ISIN kodu. Şirket bazında<br>ilgili veri boştur. |
| 2 | Payın Kodu | Alfabetik | 32* | Payın Kodu. İşlem görmeyen paylar ve şirket<br>bazında ilgili veri boştur. |
| 3 | Özellik | Alfabetik | 25* | Payın türü (Eski, işlem görmüyor..vb.). Şirket<br>bazında ilgili veri boştur. |
| 4 | Ticaret Ünvanı | Alfabetik | 100* | Payın ait olduğu şirketin ticaret ünvanıdır. |
| 5 | Bülten Adı | Alfabetik | 32* | Payın bülten adıdır. İşlem görmeyen paylar ve<br>şirket bazında ilgili veri boştur. |
| 6 | Kayıtlı Sermaye<br>Tavanı (TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin kayıtlı sermaye tavan tutarıdır.<br>Şirket bazında verilmekte olup, pay bazında ilgili<br>veri boştur. Esas sermaye sisteminde olan<br>şirketler için boştur. |

<!-- sayfa 35 -->
**[Sayfa 35]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 7 | Önceki Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | Şirketin/payın sermaye artırımı/azaltımı öncesi<br>sermaye tutarıdır. |
| 8 | Sermaye Azaltımı<br>(TL) | Ondalıklı,<br>nümerik | 20* | Şirketin/payın azaltılacak sermaye tutarıdır. |
| 9 | Sermaye Azaltımı<br>(%) | Ondalıklı,<br>nümerik | 20* | Pay bazında sermaye azaltım tutarının önceki<br>sermaye tutarına yüzde olarak oranıdır. Pay<br>bazında verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 10 | Birleşme veya<br>Devralma<br>Nedeniyle Sermaye<br>Azaltımı (TL) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle azaltılacak<br>sermaye tutarıdır. |
| 11 | Birleşme veya<br>Devralma<br>Nedeniyle Sermaye<br>Azaltımı (%) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle azaltılacak<br>sermayenin önceki sermayeye yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |
| 12 | Rüçhan Hakkı<br>Kullandırılarak<br>(TL) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırılarak artırılacak sermaye<br>tutarıdır. |
| 13 | Rüçhan Hakkı<br>Kullandırılarak (%) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırma oranıdır. Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 14 | Pay Satış Fiyatı<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili payın rüçhan hakkı kullandırma fiyatıdır.<br>Pay bazında 1 TL nominal değerli bir adet pay<br>için verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 15 | Rüçhan Hakkı<br>Kullandırılmadan<br>(TL) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırılmadan artırılacak<br>sermaye tutarıdır. |
| 16 | Pay Satış Fiyatı<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için rüçhan hakkı kullandırılmadan<br>gerçekleştirilecek sermaye artırımında 1 TL<br>nominal değerli bir adet payın satış fiyatıdır. Pay<br>bazında verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 17 | Birleşme ve<br>Devralma (TL) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle artırılacak<br>sermaye tutarıdır. |
| 18 | İç Kaynaklardan<br>(TL) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarıdır. |

<!-- sayfa 36 -->
**[Sayfa 36]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 19 | İç Kaynaklardan<br>(%) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarının önceki sermaye<br>tutarından varsa sermaye azaltım tutarının<br>düşülmesiyle bulunan tutara yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |
| 20 | Kar Payından (TL) | Ondalıklı,<br>nümerik | 20* | Kar payından karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarıdır. |
| 21 | Kar Payından (%) | Ondalıklı,<br>nümerik | 20* | Kar payından karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırımının önceki sermaye<br>tutarından varsa sermaye azaltım tutarının<br>düşülmesiyle bulunan tutara yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |
| 22 | Cari Sermaye (TL) | Ondalıklı,<br>nümerik | 20* | İlgili tarih itibariyle cari sermaye tutarıdır. Şirket<br>bazında verilmekte olup, pay bazında ilgili veri<br>boştur. |
| 23 | Hak Kullanım<br>Başlangıç Tarihi | Alfanümerik | 10 | İlgili şirket paylarının ilgili hakları kullanılmış<br>olarak işlem göreceği ilk tarihtir<br>(GG.AA.YYYY). Pay bazında verilmekte olup,<br>şirket bazında ilgili veri boştur. |
| 24 | Hak Kullanım Bitiş<br>Tarihi | Alfanümerik | 10 | Hak kullanım işlemlerinin sona ereceği tarihtir<br>(GG.AA.YYYY). Pay bazında verilmekte olup,<br>şirket bazında ilgili veri boştur. |
| 25 | Pay Dağıtım Tarihi | Alfanümerik | 10 | Kaydi payların dağıtım tarihidir. Esas sermaye<br>sisteminde gerçekleştirilen bedelli sermaye<br>artırımlarında yeni pay alma haklarının kullanımı<br>sırasında verilen geçici kaydi payların kaydi paya<br>dönüşüm tarihidir (GG.AA.YYYY). Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 26 | Verilecek Menkul<br>Grubu | Alfanümerik | 80* | İlgili hak kullanımı karşılığında verilecek<br>menkulü tanımlamakta olup, hak kullanım tarihi<br>belli olduğunda verilecek menkulün grubunu,<br>özelliğini ve ISIN bilgisini içerir. Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 27 | Pazar | Alfanümerik | 60* | İlgili payın işlem gördüğü pazar bilgisidir. İşlem<br>görmeyen paylar ve şirket bazında ilgili veri<br>boştur. |
| 28 | Not | Alfanümerik | 600* | İlgili hak kullanımına ilişkin varsa ek bilgilerin<br>gösterildiği sütundur. |

<!-- sayfa 37 -->
**[Sayfa 37]**

2.1.27 Sermaye Artırımları (Haftalık)

| Dosya Adı |  | Açıklama |
|---|---|---|
| serart[YYYY].zip->sermaye_[YYYY].xls |  | Dosyanın ait olduğu hafta sonu itibariyle,<br>yıl içinde gerçekleşmiş veya<br>gerçekleşecek sermaye artırımlarını pay<br>ve şirket bazında gösteren rapordur.<br>Şirket bazında verilen tutarlar şirkete ait<br>tüm payların toplam tutarlarıdır. |
| Örnek Dosya Adı | serart2016.zip-><br>sermaye_2016.xls |  |
| Örnek Dosya İçerikleri |  |  |
| TREACSS00017;ACSEL;Eski;ACISELSAN ACIPAYAM SELÜLOZ SANAYİ VE TİCARET<br>A.Ş.;ACIPAYAM SELULOZ;;10721700;;;;;;;;;;;;;;;;;;;;PAY-ANA PAZAR; |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | ISIN | Alfanümerik | 12 | İlgili payın 12 haneli ISIN kodu. İşlem görmeyen<br>paylar ve şirket bazında ilgili veri boştur. |
| 2 | Payın Kodu | Alfabetik | 32* | Payın Kodu. İşlem görmeyen paylar ve şirket<br>bazında ilgili veri boştur. |
| 3 | Özellik | Alfabetik | 25* | Payın türü (Eski, işlem görmüyor..vb.). Şirket<br>bazında ilgili veri boştur. |
| 4 | Ticaret Ünvanı | Alfabetik | 100* | Payın ait olduğu şirketin ticaret ünvanıdır. |
| 5 | Bülten Adı | Alfabetik | 32* | Payın bülten adıdır. İşlem görmeyen paylar ve<br>şirket bazında ilgili veri boştur. |
| 6 | Kayıtlı Sermaye<br>Tavanı (TL) | Ondalıklı,<br>nümerik | 20* | İlgili şirketin kayıtlı sermaye tavan tutarıdır.<br>Şirket bazında verilmekte olup, pay bazında ilgili<br>veri boştur. Esas sermaye sisteminde olan<br>şirketler için boştur. |
| 7 | Önceki Sermaye<br>(TL) | Ondalıklı,<br>nümerik | 20* | Şirketin/payın sermaye artırımı/azaltımı öncesi<br>sermaye tutarıdır. |
| 8 | Sermaye Azaltımı<br>(TL) | Ondalıklı,<br>nümerik | 20* | Şirketin/payın azaltılacak sermaye tutarıdır. |
| 9 | Sermaye Azaltımı<br>(%) | Ondalıklı,<br>nümerik | 20* | Pay bazında sermaye azaltım tutarının önceki<br>sermaye tutarına yüzde olarak oranıdır. Pay<br>bazında verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 10 | Birleşme veya<br>Devralma<br>Nedeniyle Sermaye<br>Azaltımı (TL) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle azaltılacak<br>sermaye tutarıdır. |
| 11 | Birleşme veya<br>Devralma<br>Nedeniyle Sermaye<br>Azaltımı (%) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle azaltılacak<br>sermayenin önceki sermayeye yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |

<!-- sayfa 38 -->
**[Sayfa 38]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 12 | Rüçhan Hakkı<br>Kullandırılarak<br>(TL) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırılarak artırılacak sermaye<br>tutarıdır. |
| 13 | Rüçhan Hakkı<br>Kullandırılarak (%) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırma oranıdır. Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 14 | Pay Satış Fiyatı<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için rüçhan hakkı kullandırma fiyatıdır.<br>Pay bazında 1 TL nominal değerli bir adet pay<br>için verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 15 | Rüçhan Hakkı<br>Kullandırılmadan<br>(TL) | Ondalıklı,<br>nümerik | 20* | Rüçhan hakkı kullandırılmadan artırılacak<br>sermaye tutarıdır. |
| 16 | Pay Satış Fiyatı<br>(TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için rüçhan hakkı kullandırılmadan<br>gerçekleştirilecek sermaye artırımında 1 TL<br>nominal değerli bir payın satış fiyatıdır. Pay<br>bazında verilmekte olup, şirket bazında ilgili veri<br>boştur. |
| 17 | Birleşme ve<br>Devralma (TL) | Ondalıklı,<br>nümerik | 20* | Birleşme ve devralma nedeniyle artırılacak<br>sermaye tutarıdır. |
| 18 | İç Kaynaklardan<br>(TL) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarıdır. |
| 19 | İç Kaynaklardan<br>(%) | Ondalıklı,<br>nümerik | 20* | İç kaynaklardan karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarının önceki sermaye<br>tutarından varsa sermaye azaltım tutarının<br>düşülmesiyle bulunan tutara yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |
| 20 | Kar Payından (TL) | Ondalıklı,<br>nümerik | 20* | Kar payından karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarıdır. |
| 21 | Kar Payından (%) | Ondalıklı,<br>nümerik | 20* | Kar payından karşılanarak gerçekleştirilecek<br>bedelsiz sermaye artırım tutarının önceki sermaye<br>tutarından varsa sermaye azaltım tutarının<br>düşülmesiyle bulunan tutara yüzde olarak<br>oranıdır. Pay bazında verilmekte olup, şirket<br>bazında ilgili veri boştur. |
| 22 | Cari Sermaye (TL) | Ondalıklı,<br>nümerik | 20* | İlgili tarih itibariyle cari sermaye tutarıdır. Şirket<br>bazında verilmekte olup, pay bazında ilgili veri<br>boştur. |
| 23 | Hak Kullanım<br>Başlangıç Tarihi | Alfanümerik | 10 | İlgili şirket paylarının ilgili hakları kullanılmış<br>olarak işlem göreceği ilk tarihtir<br>(GG.AA.YYYY). Pay bazında verilmekte olup,<br>şirket bazında ilgili veri boştur. |

<!-- sayfa 39 -->
**[Sayfa 39]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 24 | Hak Kullanım Bitiş<br>Tarihi | Alfanümerik | 10 | Hak kullanım işlemlerinin sona ereceği tarihtir<br>(GG.AA.YYYY). Pay bazında verilmekte olup,<br>şirket bazında ilgili veri boştur. |
| 25 | Pay Dağıtım Tarihi | Alfanümerik | 10 | Kaydi payların dağıtım tarihidir. Esas sermaye<br>sisteminde gerçekleştirilen bedelli sermaye<br>artırımlarında yeni pay alma haklarının kullanımı<br>sırasında verilen geçici kaydi payların kaydi paya<br>dönüşüm tarihidir (GG.AA.YYYY). Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 26 | Verilecek Menkul<br>Grubu | Alfanümerik | 80* | İlgili hak kullanımı karşılığında verilecek<br>menkulü tanımlamakta olup, hak kullanım tarihi<br>belli olduğunda verilecek menkulün grubunu,<br>özelliğini ve ISIN bilgisini içerir. Pay bazında<br>verilmekte olup, şirket bazında ilgili veri boştur. |
| 27 | Pazar | Alfanümerik | 60* | İlgili payın işlem gördüğü pazar bilgisidir. İşlem<br>görmeyen paylar ve şirket bazında ilgili veri<br>boştur. |
| 28 | Not | Alfanümerik | 600* | İlgili hak kullanımına ilişkin varsa ek bilgilerin<br>gösterildiği sütundur. |

2.1.28 Temettü Ödemeleri

| Dosya Adı |  | Açıklama |
|---|---|---|
| temettu[YYYY].zip->temettu_[YYYY].xls |  | Dosyanın ait olduğu hafta itibariyle, yıl<br>içinde gerçekleşmiş veya gerçekleşecek<br>temettü dağıtımlarını gösteren rapordur. |
| Örnek Dosya Adı | temettu2015.zip-><br>temettu_2015.xls |  |
| Örnek Dosya İçerikleri |  |  |
| TREACSS00017;ACSEL;Eski;ACISELSAN ACIPAYAM SELÜLOZ SANAYİ VE TİCARET<br>A.Ş.;ACIPAYAM SELULOZ;Olağan;0;0;;0;0;0;;;01.01.2014;31.12.2014;PAY-ANA PAZAR; |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | ISIN | Alfanümerik | 12 | İlgili payın 12 haneli ISIN kodu. |
| 2 | Payın Kodu | Alfabetik | 32* | Payın Kodu. İşlem görmeyen paylar için ilgili veri<br>boştur. |
| 3 | Özellik | Alfabetik | 25* | Payın türü (Eski, işlem görmüyor..vb.) |
| 4 | Ticaret Ünvanı | Alfabetik | 100* | Payın ait olduğu şirketin ticaret ünvanıdır. |
| 5 | Bülten Adı | Alfabetik | 32* | Payın bülten adıdır. İşlem görmeyen paylar için<br>ilgili veri boştur. |

<!-- sayfa 40 -->
**[Sayfa 40]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 6 | Genel Kurul Kararı | Alfabetik | 10* | İlgili temettü ödemesinin görüşüldüğü genel<br>kurulun olağan ya da olağanüstü olduğu bilgisidir.<br>Henüz genel kurul toplantısı yapılmamış olan<br>şirketler için boştur. |
| 7 | Pay Biçiminde Kar<br>Payı Tutarı (TL) | Ondalıklı,<br>nümerik | 20* | Pay biçiminde dağıtılan kar payının toplam<br>tutarıdır. |
| 8 | Pay Biçiminde Kar<br>Payı (%) | Ondalıklı,<br>nümerik | 20* | Pay biçiminde dağıtılan toplam kar payının<br>toplam pay sayısına yüzde olarak oranıdır. |
| 9 | Dağıtım Tarihi | Alfanümerik | 10 | İlgili şirket paylarının kar payı alma hakları<br>üzerinden ayrılmış olarak işlem göreceği ilk<br>tarihtir (GG.AA.YYYY). Pay şeklinde kar payı<br>dağıtılmayacak olması halinde ilgili veri boştur. |
| 10 | Toplam Brüt Nakit<br>Kar Payı (TL) | Ondalıklı,<br>nümerik | 20* | İlgili pay için nakit olarak ödenecek brüt kar<br>payının toplam tutarıdır. |
| 11 | 1 TL Nominal<br>Değerli Paya Nakit<br>Kar Payı - Brüt<br>(TL) | Ondalıklı,<br>nümerik | 20* | 1 TL nominal değerli bir adet pay için nakit<br>olarak ödenecek brüt kar payı tutarıdır. |
| 12 | 1 TL Nominal<br>Değerli Paya Nakit<br>Kar Payı - Net (TL) | Ondalıklı,<br>nümerik | 20* | 1 TL nominal değerli bir adet pay için nakit<br>olarak ödenecek net kar payı tutarıdır. |
| 13 | Ödeme Şekli | Alfanümerik | 20* | Kar payının taksitli mi ya da avans temettü olarak<br>mı ödendiğini/ödeneceğini gösterir (Taksitli<br>temettü için T1, T2 vs, avans temettü için “A”).<br>Kar payının peşin olarak ödenecek veya kar payı<br>ödenmeyecek olması halinde ilgili veri boştur. |
| 14 | Ödeme Tarihi | Alfanümerik | 10 | İlgili şirket paylarının nakit kar payı alma hakları<br>üzerinden ayrılmış olarak işlem göreceği ilk<br>tarihtir (GG.AA.YYYY). Nakit kar payı<br>dağıtılmayacak olması halinde ilgili veri boştur. |
| 15 | Hesap Dönemi<br>Başlangıç Tarihi | Alfanümerik | 10 | Kar payı dağıtım bilgilerinin ait olduğu hesap<br>döneminin başlangıç tarihidir (GG.AA.YYYY).<br>Kar payı dağıtımına ilişkin genel kurul toplantısı<br>henüz yapılmamış şirketler ile kar payı dağıtımı<br>olağanüstü genel kurul toplantısında karar altına<br>alınan şirketler için ilgili veri boştur. Benzer<br>şekilde avans kar payı ödemeleri için de ilgili veri<br>boştur. |

<!-- sayfa 41 -->
**[Sayfa 41]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 16 | Hesap Dönemi Bitiş<br>Tarihi | Alfanümerik | 10 | Kar payı dağıtım bilgilerinin ait olduğu hesap<br>döneminin bitiş tarihidir (GG.AA.YYYY). Kar<br>payı dağıtımına ilişkin genel kurul toplantısı<br>henüz yapılmamış şirketler ile kar payı dağıtımı<br>olağanüstü genel kurul toplantısında karar altına<br>alınan şirketler için ilgili veri boştur. Benzer<br>şekilde avans kar payı ödemeleri için de ilgili veri<br>boştur. |
| 17 | Pazar | Alfanümerik | 60* | İlgili payın işlem gördüğü pazardır. İşlem<br>görmeyen paylar için ilgili veri boştur. |
| 18 | Not | Alfanümerik | 600* | İlgili hak kullanımına ilişkin varsa ek bilgilerin<br>gösterildiği sütundur. |

2.1.29 2000 Yılından İtibaren Endekslerde Bulunan Şirketler

| Dosya Adı |  | Açıklama |
|---|---|---|
| exsrk[YYYY].zip->exsrk[YYYY].xls |  | İlgili yıllarda her bir çeyrekte BIST 100,<br>BIST 50 ve BIST 30’da yer alan<br>şirketlerin listesini gösterir. |
| Örnek Dosya Adı | exsrk2015.zip-> exsrk2015.xls |  |
| Örnek Dosya İçerikleri |  |  |
| ADEL;ADEL KALEMCİLİK;;XU100;XU100;XU100 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Pay Kodu | Alfabetik | 32* | Payın kodu |
| 2 | Pay Adı | Alfabetik | 32* | Payın bülten adı |
| 3 | 1.Çeyrek | Alfanümerik | 5* | İlgili yılın ilk çeyreğinde payın BIST 100, BIST<br>50 veya BIST 30’dan hangilerine dahil olduğu<br>bilgisi verilmektedir (Endeksler sırasıyla diğerini<br>kapsamaktadır, sadece yer aldığı en az payı içeren<br>endeks belirtilmektedir.) |
| 4 | 2.Çeyrek | Alfanümerik | 5* | İlgili yılın ikinci çeyreğinde payın BIST 100,<br>BIST 50 veya BIST 30’dan hangilerine dahil<br>olduğu bilgisi verilmektedir.(Endeksler sırasıyla<br>diğerini kapsamaktadır, sadece yer aldığı en az<br>payı içeren endeks belirtilmektedir.) |
| 5 | 3.Çeyrek | Alfanümerik | 5* | İlgili yılın üçüncü çeyreğinde payın BIST 100,<br>BIST 50 veya BIST 30’dan hangilerine dahil<br>olduğu bilgisi verilmektedir. (Endeksler sırasıyla<br>diğerini kapsamaktadır, sadece yer aldığı en az<br>payı içeren endeks belirtilmektedir.) |

<!-- sayfa 42 -->
**[Sayfa 42]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 6 | 4.Çeyrek | Alfanümerik | 5* | İlgili yılın dördüncü çeyreğinde payın BIST 100,<br>BIST 50 veya BIST 30’dan hangilerine dahil<br>olduğu bilgisi verilmektedir. (Endeksler sırasıyla<br>diğerini kapsamaktadır, sadece yer aldığı en az<br>payı içeren endeks belirtilmektedir.) |

2.1.30 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Öncesi Endeks Bölen Raporu)

| Dosya Adı |  | Açıklama |
|---|---|---|
| Endeks_bolen_do_genel_[YYYYAAGG].csv |  | BIST pay endekslerinin ilgili tarihteki<br>kapanış / düzeltme öncesi bölen değerlerini<br>içermektedir. |
| Örnek Dosya Adı | endeks_bolen_do_genel_20<br>160412.csv |  |
| Örnek Dosya İçeriği |  |  |
| 12/04/2016;1400426.93112416;102526.1756;BEFORE ADJUSTMENT/DUZELTME<br>ONCESI;X030S;BIST 30 AGIRLIK SINIRLAMALI;BIST 30<br>CAPPED;TRY;TRAXIST00517;143580417474.7389 |  |  |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Günün tarihi (GG.AA.YYYY) |
| 2 | Endeks Bölen | Ondalıklı,Nü<br>merik | 24* | Endeks bölen değeri |
| 3 | Endeks Kapanış<br>Değeri | Ondalıklı,Nü<br>merik | 20* | Endeksin gün sonu kapanış değeri |
| 4 | Düzeltme<br>Öncesi/Düzeltme<br>Sonrası/Yeni Gün | Alfanümerik | 80* | Rapor içeriğinin oluşturulma zamanı (Before<br>Adjustment / Düzeltme Öncesi gibi) |
| 5 | Endeks Kodu | Alfanümerik | 20* | Endeks kodu |
| 6 | Endeksler | Alfanümerik | 100* | Endeks Türkçe adı |
| 7 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 100* | Endeks İngilizce adı |
| 8 | Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 9 | ISIN | Alfanümerik | 12 | Endeks ISIN kodu |
| 10 | FDP Katsayılı<br>Piyasa Değeri | Ondalıklı,Nü<br>merik | 20* | Endeksin FDP katsayılı piyasa değeri |

2.1.31 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Sonrası Endeks Bölen Raporu)

| Dosya Adı |  | Açıklama |
|---|---|---|
| Endeks_bolen_ds_genel_[YYYYAAGG].csv |  | BIST pay endekslerinin ilgili tarihteki<br>düzeltme sonrası bölen değerlerini<br>içermektedir. |
| Örnek Dosya Adı | endeks_bolen_ds_genel_20<br>160412.csv |  |
| Örnek Dosya İçeriği |  |  |
| 12/04/2016;1400426.93112416;102526.1756;AFTER ADJUSTMENT/DUZELTME<br>SONRASI;X030S;BIST 30 AGIRLIK SINIRLAMALI;BIST 30<br>CAPPED;TRY;TRAXIST00517;143580417474.7389 |  |  |

<!-- sayfa 43 -->
**[Sayfa 43]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Günün tarihi (GG.AA.YYYY) |
| 2 | Endeks Bölen | Ondalıklı,Nümerik | 24* | Endeks bölen değeri |
| 3 | Endeks Kapanış<br>Değeri | Ondalıklı,Nümerik | 20* | Endeksin gün sonu kapanış değeri |
| 4 | Düzeltme<br>Öncesi/Düzeltme<br>Sonrası/Yeni Gün | Alfanümerik | 80* | Rapor içeriğinin oluşturulma zamanı<br>(After Adjustment / Düzeltme Sonrası<br>gibi) |
| 5 | Endeks Kodu | Alfanümerik | 20* | Endeks kodu |
| 6 | Endeksler | Alfanümerik | 100* | Endeks Türkçe adı |
| 7 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 100* | Endeks İngilizce adı |
| 8 | Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 9 | ISIN | Alfanümerik | 12 | Endeks ISIN kodu |
| 10 | FDP Katsayılı<br>Piyasa Değeri | Ondalıklı,Nümerik | 20* | Endeksin FDP katsayılı piyasa değeri |

2.1.32 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Öncesi Endeks Ağırlık Raporu)

| Dosya Adı |  | Açıklama |
|---|---|---|
| Endeks_agirlik_do_genel_[YYYYAAGG].csv |  | BIST pay endekslerinde yer alan payların,<br>kapsamında yer aldığı her bir endeks için<br>kapanış / düzeltme öncesi toplam pay sayısı,<br>katsayı, Fiili Dolaşımdaki Pay Oranı ve %<br>olarak ağırlık değerlerini içermektedir. |
| Örnek Dosya Adı | endeks_agirlik_do_genel_2<br>0160412.csv |  |
| Örnek Dosya İçeriği |  |  |
| 12/04/2016;X030S;BIST 30<br>ADJUSTMENT/DUZELTME<br>1175 | AGIRLIK SINIRLAMALI;BIST<br>ONCESI;TRY;1;AKBNK.E;AKBANK;4000000000.0000;CLOSE(KAPANIS);0.52;0.860099990374;10. | 30 CAPPED;TRY;1;BEFORE |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Günün tarihi (GG.AA.YYYY) |
| 2 | Endeks Kodu | Alfanümerik | 20* | Endeks kodu |
| 3 | Endeksler | Alfanümerik | 100* | Endeks Türkçe adı |
| 4 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 100* | Endeks İngilizce adı |
| 5 | Endeks Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 6 | Endeks Kuru | Ondalıklı,Nümerik | 80* | TCMB tarafından ilgili tarihte belirlenen<br>gösterge niteliğindeki döviz alış kurunun<br>TL cinsinden değeri |
| 7 | Düzeltme<br>Öncesi/Düzeltme<br>Sonrası/Yeni Gün | Alfanümerik | 80* | Rapor içeriğinin oluşturulma zamanı<br>(Before Adjustment / Düzeltme Öncesi<br>gibi) |
| 8 | Pay Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 9 | Pay Kuru | Ondalıklı,Nümerik | 80* | TCMB tarafından ilgili tarihte belirlenen<br>gösterge niteliğindeki döviz alış kurunun<br>TL cinsinden değeri |

<!-- sayfa 44 -->
**[Sayfa 44]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 10 | Pay Kodu | Alfanümerik | 50* | Bu alanda Seri kodu pay kodu içerisinde<br>yer alır. İlgili pay için raporun alındığı<br>tarih itibarıyla geçerli olan koddur. |
| 11 | Pay Adı | Alfanümerik | 100* | Payın bülten adı |
| 12 | Toplam Pay Sayısı | Ondalıklı,Nümerik | 24* | Endeks hesabında kullanılan pay sayısı |
| 13 | Kapanış/AOF | Alfabetik | 20* | Endeksin hesaplamasında kullanılan fiyat<br>türü (Close(Kapanış) veya VWAP(AOF)<br>gibi) |
| 14 | Fiili Dolaşımdaki<br>Pay Oranı | Ondalıklı,Nümerik | 10* | Endeks hesabında kullanılan Fiili<br>Dolaşımdaki Pay Oranı |
| 15 | Katsayı | Ondalıklı,Nümerik | 28* | İlgili payın ilgili endeksin hesabında<br>kullanılan katsayısı |
| 16 | Ağırlık (%) | Ondalıklı,Nümerik | 20* | İlgili payın yüzde olarak ilgili endeks<br>içindeki ağırlığı |

2.1.33 Endeks Hesaplamasında Kullanılan Veriler: Fiili Dolaşımdaki Pay Oranları, Bölen Değerleri ve Pay Bazında Ağırlıklar (Düzeltme Sonrası Endeks Ağırlık Raporu)

| Dosya Adı |  | Açıklama |
|---|---|---|
| Endeks_agirlik_ds_genel_[YYYYAAGG].csv |  | BIST pay endekslerinde yer alan payların,<br>kapsamında yer aldığı her bir endeks için<br>düzeltme sonrası toplam pay sayısı, katsayı,<br>Fiili Dolaşımdaki Pay Oranı ve % olarak<br>ağırlık değerlerini içermektedir. |
| Örnek Dosya Adı | endeks_agirlik_ds_genel_2<br>0160412.csv |  |
| Örnek Dosya İçeriği |  |  |
| 12/04/2016;X030S;BIST 30<br>ADJUSTMENT/DUZELTME<br>0.1175 | AGIRLIK SINIRLAMALI;BIST<br>SONRASI;TRY;1;AKBNK.E;AKBANK;4000000000.0000;CLOSE(KAPANIS);0.52;0.860099990374;1 | 30 CAPPED;TRY;1;AFTER |


| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 1 | Tarih | Alfanümerik | 10 | Günün tarihi (GG.AA.YYYY) |
| 2 | Endeks Kodu | Alfanümerik | 20* | Endeks kodu |
| 3 | Endeksler | Alfanümerik | 100* | Endeks Türkçe adı |
| 4 | Endekslerin<br>İngilizce İsimleri | Alfanümerik | 100* | Endeks İngilizce adı |
| 5 | Endeks Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 6 | Endeks Kuru | Ondalıklı,Nümerik | 80* | TCMB tarafından ilgili tarihte belirlenen<br>gösterge niteliğindeki döviz alış kurunun<br>TL cinsinden değeri |
| 7 | Düzeltme<br>Öncesi/Düzeltme<br>Sonrası/Yeni Gün | Alfanümerik | 80* | Rapor içeriğinin oluşturulma zamanı<br>(After Adjustment / Düzeltme Sonrası<br>gibi) |
| 8 | Pay Kur Türü | Alfabetik | 3 | TRY,EUR,USD |
| 9 | Pay Kuru | Ondalıklı,Nümerik | 80* | TCMB tarafından ilgili tarihte belirlenen<br>gösterge niteliğindeki döviz alış kurunun<br>TL cinsinden değeri |

<!-- sayfa 45 -->
**[Sayfa 45]**

| Sıra | Alan Adı | Alan Türü | Uzunluk | Açıklama |
|---|---|---|---|---|
| 10 | Pay Kodu | Alfanümerik | 50* | Bu alanda Seri kodu pay kodu içerisinde<br>yer alır. İlgili pay için rapor tarihi<br>itibarıyla geçerli olan kod olup, ertesi<br>günden geçerli olmak üzere kodu değişen<br>payın yeni kodudur. |
| 11 | Pay Adı | Alfanümerik | 100* | Payın bülten adı |
| 12 | Toplam Pay Sayısı | Ondalıklı,Nümerik | 24* | Endeks hesabında kullanılan pay sayısı |
| 13 | Kapanış/AOF | Alfabetik | 20* | Endeksin hesaplamasında kullanılan fiyat<br>türü (Close(Kapanış) veya VWAP(AOF)<br>gibi) |
| 14 | FDPO | Ondalıklı,Nümerik | 10* | Endeks hesabında kullanılan Fiili<br>Dolaşımdaki Pay Oranı |
| 15 | Katsayı | Ondalıklı,Nümerik | 28* | İlgili payın ilgili endeksin hesabında<br>kullanılan katsayısı |
| 16 | Ağırlık (%) | Ondalıklı,Nümerik | 20* | İlgili payın yüzde olarak ilgili endeks<br>içindeki ağırlığı |

<!-- sayfa 46 -->
**[Sayfa 46]**

EK
3.1 REFERANS TABLOLARI
3.1.1 OrderType

| Undefined (Tanımlanmamış) | 0 |
|---|---|
| Limit | 1 |
| Market | 2 |
| Market to Limit | 3 |
| Pasif | 4 |
| Only At Best (Sadece En İyide) | 8 |
| Pegged to Best (En İyiye Sabitlenmiş) | 16 |
| Odd Lot (Küsürat Emri) | 32 |
| Imbalance (Dengeleyici) | 64 |

3.1.2 ExchangeOrderType

| Undefined (Tanımlanmamış) | 0 |
|---|---|
| Force | 1 |
| Short Sell | 2 |
| Market Bid | 4 |
| Price Stabilization | 8 |
| Override Crossing | 16 |
| Undisclosed Quantity | 32 |
| Mid Point | 64 |
| Always Inactive | 128 |
| Mid Point Crossing | 256 |

<!-- sayfa 47 -->
**[Sayfa 47]**

| Trigger On Session | 512 |
|---|---|
| Peg | 1024 |
| Mid Point Sweep | 2048 |
| Center Point Block | 4096 |

3.1.3 OrderCategory

| Unknown (Bilinmeyen) | 0 |
|---|---|
| Order (Normal Emir) | 1 |
| Quote (Kotasyon) | 4 |
| Trade Report (Özel İşlem Bildirimi) | 32 |

3.1.4 ChangeReason

| Undefined | 0 |
|---|---|
| CanceledByUser | 1 |
| Trade | 3 |
| Inactivate | 4 |
| ReplacedByUser | 5 |
| New | 6 |
| MarketOrderConverted | 7 |
| ConvertedBySystem | 8 |
| CanceledBySystem | 9 |
| CanceledOnBehalf | 10 |
| BaitRecalculated | 11 |
| TriggeredBySystem | 12 |
| RefreshedBySystem | 13 |
| CanceledBySystemLimitChange | 15 |

<!-- sayfa 48 -->
**[Sayfa 48]**

| Expired | 19 |
|---|---|
| CanceledDueToISS | 20 |
| InactivatedDueToISS | 21 |
| InactivatedDueToPurge | 23 |
| InactivatedDayOrder | 24 |
| InactivatedOtherOrder | 26 |
| InactivatedDueToOutsidePurgePriceLimits | 27 |
| OrderOwnershipTransferred | 28 |
| NewInactiveOrder | 29 |
| CanceledAfterAuction | 34 |
| InactivatedDueToOutsideLimits | 35 |
| ActivatedDueToOutsideLimits | 36 |
| TriggerOnSessionOrderTriggered | 37 |
| TriggerOnSessionOrderInactivated | 38 |
| UndisclosedQuantityOrderConverted | 39 |
| VolumeMatchOrderInactivated | 40 |
| QuoteCanceledDeltaMmProtection | 41 |
| QuoteCanceledAbsMmProtection | 42 |
| CrossingOrderDeleted | 43 |
| MidPointSweepMtlConverted | 48 |
| MaqMidPointBelowMinQuantity | 49 |
| MidPointSweepReloaded | 50 |

3.1.5 MarketSegment

| PAY-GELISEN ISLETMELER PAZARI | G |
|---|---|
| PAY-KOLLEKTIF&YAPILANDIRILMIS UR.<br>PAZARI | K |

<!-- sayfa 49 -->
**[Sayfa 49]**

| İKİNCİL ULUSAL PAZAR | L |
|---|---|
| PAY-ANA PAZAR | N |
| PAY-NITELIKLI YATIRIMCI ISLEMLERI<br>PAZARI | Q |
| PAY-PIYASA ONCESI ISLEM PLATFORMU | S |
| PAY-YAKIN IZLEME PAZARI | W |
| PAY-YILDIZ PAZAR | Z |

3.1.6 Market

| NCCP | NCCP |
|---|---|
| CCP | CCP |
| Pay – Pay Ana Pazarı (MainSptEQ) | MSPOT |
| Pay – Birincil Piyasa (Prim Mkt) | PMRKT |
| Pay – Birincil Tek Trf (PrmMktOneS) | PMOSA |
| Pay – Resmi Müzayede (Offi.Auct) | OFAUC |
| Pay – Temerrüt Pazarı (Buyin Mk) | BUYIN |
| Pay – Küsürat Pazarı (OddLots M) | ODDLT |
| Pay – Endeks (Index) | INDEX |
| PRV Market – For Test Use Only | _PRV |
| Collateral Market | COL |
| Market For External Price Data | PDATA |
| Interest Rate Market | INTRT |
| Payment Market | PMT |

3.1.7 OrderStatus

| Active | 1 |
|---|---|
| Not On Book (Emir Tablosunda Yok) | 2 |

<!-- sayfa 50 -->
**[Sayfa 50]**

| Untriggered (Tetiklenmemiş) | 3 |
|---|---|
| Inactive | 4 |

3.1.8 OrderDurationID

| Day (Günlük) | DAY |
|---|---|
| Good Till Cancelled (İptal Edilene Kadar) | GTC |
| Good Till Data (Belirlenen Tarihe Kadar) | GTD |
| Good Till Time (Belirlenen Zamana Kadar) | GTT |
| Immediate (Anlık Emir) | IMMEDIATE |
| Session (Seanslık) | SESSION |

3.1.9 OrderPriceTypeID

| Limit | L |
|---|---|
| Market | M |
| Trigger | T |
| Market To Limit | X |

3.1.10 OrderTypeIDSet

| Force | FOR | 1 |
|---|---|---|
| Short Sell (Açığa Satış) | SRT | 2 |
| Market Bid | MKT_BID | 4 |
| Price Stablisation | PSB | 8 |
| Override Crossing | OVR | 16 |
| Undisclosed | UDC | 32 |
| Mid Point Crossing | CEN | 64 |
| Always Active | ACTIVE | 128 |

<!-- sayfa 51 -->
**[Sayfa 51]**

| Mid Point Order | CENTER_PT | 256 |
|---|---|---|
| Trigger On Session | TRI | 512 |
| Peged Order | PEG | 1024 |
| Mid Point Sweep | CENTER_SWP | 2048 |
| Mid Point Block | CENTER_BLK | 4096 |

3.1.11 DealSource

| deal_source_none | 0 | Internal use. Trades reported<br>directly to the clearing<br>subsystem. |
|---|---|---|
| deal_source_auto | 1 | Matched by system,<br>automatically. |
| deal_source_manually | 2 | Matched by system, manually. |
| deal_source_outside_different | 3 | Matched Outside Exchange,<br>Different participants |
| deal_source_outside_different_om | 4 | Matched outside exchange,<br>different participants, reg. by<br>exchange. |
| deal_source_outside_same | 5 | Matched Outside Exchange,<br>One participant |
| deal_source_outside_same_om | 6 | Matched outside exchange,one<br>participant, reg. by exchange. |
| deal_source_auto_combo | 7 | Combination order matched<br>against another combination<br>order when matched by the<br>Exchange, electronically. |
| deal_source_swap_box | 8 | Deal in a Swap Box<br>instrument. |
| deal_source_auto_internal | 9 | Matched electronically,<br>member internal. |
| deal_source_swap_box_internal | 10 | Deal in a Swap Box<br>instrument,<br>member internal. |
| deal_source_after_outside_dif | 11 | After market closure, outside<br>system, different brokers |
| deal_source_after_outside_diff_om | 12 | After market closure, outside<br>system, different brokers,<br>registered by the exchange |
| deal_source_after_outside_same | 13 | After market closure, outside<br>system, one broker |
| deal_source_after_outside_same_om | 14 | After market closure, outside<br>system, one broker, registered<br>by the exchange. |

<!-- sayfa 52 -->
**[Sayfa 52]**

| deal_source_internally_basis | 15 | Internally created basis trade. |
|---|---|---|
| deal_source_manual_reversing | 16 | Reversing deal made by the<br>exchange manually. |
| deal_source_basis_trade | 17 | Basis trade. |
| deal_source_correction | 18 | Correction of trade. |
| deal_source_internally_created | 19 | Internally created. |
| deal_source_open_allocation | 20 | Deal made at the end of an<br>auction. |
| deal_source_pqr | 21 | Private request for quote. |
| deal_source_pqr_package | 22 | Package private request for<br>quote. |
| deal_source_internal_combo | 23 | Internally from combo. |
| deal_source_internal_tm | 24 | Internally from TM. |
| deal_source_internal_average | 25 | Internally from average. |
| deal_source_internal_strip | 26 | Internally from strip. |
| deal_source_delta_hedge | 27 | Delta hedge. |
| deal_source_internal_bundle | 28 | CL bundle deal. |
| deal_source_bb_trade | 32 | Trade from Bulletin Board. |
| deal_source_bb_trade_st_combo | 33 | Trade from Bulletin Board,<br>standard combo. |
| deal_source_bb_trade_nost_combo | 34 | Trade from Bulletin Board,<br>non-standard combo. |
| deal_source_bb_trade_nost_combo | 35 | Trade from Bulletin Board,<br>non-standard combo. |
| deal_source_tm_combo | 36 | Tailor-made combination. |
| deal_source_non_std_combo | 37 | Non-standard combination. |
| deal_source_block_trade_fac | 38 | Outside the Exchange, block<br>trade facility. |
| deal_source_outside_combo | 39 | Matched outside the<br>Exchange,<br>combinations. |
| deal_source_external_vendor | 40 | Outside the Exchange, block<br>trade facility. |
| deal_source_no_price | 41 | No deal price |
| deal_source_priority_crossing | 42 | Priority crossing. |
| deal_source_combo_vs_outright | 43 | Combination matched outright<br>legs. |

<!-- sayfa 53 -->
**[Sayfa 53]**

| deal_source_outside_otc | 44 | Matched outside exchange,<br>broker. |
|---|---|---|
| deal_source_imp_rotation | 100 |  |
| deal_source_imp_normal | 101 |  |
| deal_source_imp_out_of_sequence | 102 |  |
| deal_source_imp_cab_trade | 103 |  |
| deal_source_imp_combo_single | 104 |  |
| deal_source_imp_combo_mix | 105 |  |
| deal_source_fac_orig_order | 110 |  |
| deal_source_fac_counter_order | 111 |  |
| deal_source_exp_orig_order | 112 |  |
| deal_source_exp_counter_order | 113 |  |
| deal_source_unsolicited_order | 114 |  |
| deal_source_solicited_order | 115 |  |
| deal_source_block_order | 116 |  |
| deal_source_trade_rep | 117 |  |
| deal_source_trade_rep_no_settle | 118 |  |
| deal_source_imp_combo_buy_write | 122 |  |
| deal_source_av_price_trade | 128 | Trade resulting from an<br>Average<br>Price Trade transaction. |
| deal_source_intermediate_apt | 129 | Intermediate trade created in<br>an Average Price Trade<br>transaction. |
| deal_source_transfer_with_price | 131 | Trade transfer |
| deal_source_transfer_misclear | 132 | Misclear |
| deal_source_efp | 133 | Exchange for physical (EFP). |
| deal_source_spread | 134 | Spread trade. |
| deal_source_aps | 135 | Average price system (APS). |
| deal_source_adjust_wo_price | 136 | Adjustment without price. |
| deal_source_adjust_with_price | 137 | Adjustment with price. |

<!-- sayfa 54 -->
**[Sayfa 54]**

| deal_source_ctrade | 138 | Deal executed at CTrade. |
|---|---|---|
| deal_source_cross_product_netting | 139 | Cross product netting. |

3.1.12 CorporateAction

| R.H. Kullandirilarak Bedelli Sermaye Art | 01 |
|---|---|
| R.H. Kullandirilmadan Bedlli Sermaye Art | 02 |
| Bedelsiz Sermaye Artirimi | 03 |
| Sermaye Azaltimi | 04 |
| Birlesme / Devralma | 05 |
| Nakit Temettü | 06 |
| Diğer | 99 |
| Yok | 00 |

3.1.13 Session

| P_ACILIS_EMIR_TPL |
|---|
| P_ARA |
| P_BP_SUREKLI_ISLEM |
| P_BP_TEK_TARAF_CAGON |
| P_BP_TEK_TARAF_CAGSN |
| P_BP_TEK_TARAFLI_CAG |
| P_DK_TEKFIY_EMIR_TPL |
| P_ENDEKS_YAYIN |
| P_ENDEKS_YAYIN_YOK |
| P_ESLESTIRME |
| P_ESLESTIRME_B_H |
| P_ESLESTIRME_B_O |
| P_ESLESTIRME_FBS_B_H |
| P_ESLESTIRME_FBS_B_O |
| P_ESLESTIRME_FBS_I_H |
| P_ESLESTIRME_FBS_I_O |
| P_ESLESTIRME_FBS_SON |
| P_ESLESTIRME_I_H |
| P_ESLESTIRME_I_O |
| P_ESLESTIRMETEKFIYAT |

<!-- sayfa 55 -->
**[Sayfa 55]**

P_GECICI_DURDURMA

| P_GECICI_DURDURMA_KS |
|---|
| P_GECICI_DURDURMA_SI |
| P_GECICI_DURDURMA_TF |
| P_GUNSONU |
| P_GUNSONU_ISLEMLERI |
| P_GUNSONU_ISTATISTIK |
| P_KAPANIS_EMIR_TPL |
| P_KAPANIS_FIY_ISLEM |
| P_KESIR_KAPFIY_ISLEM |
| P_KESIR_SUREK_ISLEM |
| P_MAKBUZ_YAYINI_YOK |
| P_MARJ_YAYIN |
| P_SUREKLI_ISLEM |
| P_SUREKLI_ISLEM_AOF |
| P_TEKFIYAT_EMIR_TPL |
| P_TEKTARAF_CAGRI_AC |
| P_TEKTARAF_CAGRI_GZ |
| P_TEKTARAF_CAGRI_GZ |
| P_TEKTARAF_HLKARZ_AC |
| P_TEKTARAF_HLKARZ_GZ |
| P_TEKTRF_IPMO_CAG_AC |
| P_TEKTRF_IPMO_CAG_AC |
| P_TEKTRF_IPMO_CAG_GZ |
| P_TEKTRF_IPMO_CAG_GZ |
| P_TEKTRF_IPMO_HLA_AC |
| P_TEKTRF_IPMO_HLA_AC |
| P_TEKTRF_IPMO_HLA_GZ |
| P_TEKTRF_IPMO_HLA_GZ |
| PRV_CLOSE |
| PRV_OPEN |

3.1.14 TradeType

| 1 | Standart - The trade is a<br>normally registered trade. |
|---|---|
| 2 | Transitory<br>The trade is placed on a<br>transitory<br>account. |
| 3 | Overtaking. The trade is a<br>result of a rectify<br>operation. |

<!-- sayfa 56 -->
**[Sayfa 56]**

| 4 | Reversing. The trade is a<br>result of a rectify<br>operation. |
|---|---|
| 5 | Transfer. The trade is a result<br>of a transfer<br>from a daily account |
| 6 | Exercise. The trade is an<br>exercising part in<br>an exercise operation |
| 7 | Assign. The trade is an assign<br>part in an exercise<br>operation. |
| 8 | Closing. The trade is a result<br>of a closing series<br>operation. |
| 9 | Issue |
| 10 | New_contract. The trade is a<br>result where<br>delivery is new contract |
| 11 | Delivery |
| 12 | Dummy_trade |
| 13 | Alias |
| 14 | Offsetting |
| 15 | Superseding |
| 16 | State_change |
| 17 | Give_up |
| 18 | Take_up |
