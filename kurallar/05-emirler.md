# Emir Tipleri, Değiştirme/İptal, Değer Sınırları ve Geçerlilik Süreleri
Kaynak: Pay Piyasası Prosedürü 5.4.1–5.4.10 Emir Tipleri (s. 87–90), 5.5 Emirlerde Değiştirme ve İptal (s. 90), 5.6.3 Maksimum Kotasyon Miktarı (s. 92), 5.6.4 Emirlerde Uygulanan Değer Sınırları ve Tablo-14 (s. 92–93), 5.6.5 Emirlerde Geçerlilik Süresi (s. 93–94). Sayfa numaraları PDF sayfa numarasıdır (basılı numarayla aynı).
İlgili Ekler: Ek-18 Emir Tiplerine İlişkin Örnekler, s. 203–225 (`../ekler/ek18.md`; tablolar koordinat tabanlı aktarılmıştır, sütun kayması riski yok); Ek-19 Seansın Bölümlerine Göre Girilebilecek Emir Tipleri Çizelgesi, s. 226–229 (`../ekler/ek19.md`; sütun kayması riski yok, 16 sütunlu matris, sütun adları madde 139'da); Ek-11 Seansın Bölümleri ve Açıklamaları (`../ekler/ek11.md`).
Ek kaynaklar (Prosedür dışı teknik dokümanlar; `../kaynaklar/`, Türkçe çeviriler `../veri/`): Genium INET FIX Protocol Specification 1.0.65 (6.5.3.1, 6.5.6, 6.6.3, 6.6.4, 6.6.6), BISTECH OUCH Protocol Specification (17.09.2026; 4.1.1, 4.1.2, 4.1.3, 4.2.4). Bu kaynaklardan gelen kuralların sonunda kaynak adı yazılıdır.
Bu dosyada tekrarlanmayanlar: öncelik kaybı/korunması kuralları → `04-surekli-islem.md` madde 20–33; SMP → `04-surekli-islem.md` madde 34–43; tek fiyat yönteminde emirlerin işlem görme sırası ve dengeleyici emir eşleşmesi → `03-tek-fiyat.md` madde 48–55; fiyat adımı ve fiyat limitleri → `02-fiyat.md`; kotasyon/piyasa yapıcılık ayrıntısı → `08-pazarlar-tedbirler.md`.
İlgili kod: eşleştirme motoru (emir tipi doğrulama, emir girişi/değiştirme/iptal, geçerlilik süresi yönetimi), sentetik emir üretici

## Kurallar

### A. Genel (5.4 giriş)
1. Aksi belirtilmedikçe girilen her emir, girildiği gün boyunca geçerlidir; emirler geçerli oldukları süre veya son tarih belirtilerek de verilebilir. [5.4, s. 87]
2. Pay Piyasasına iletilebilecek emir tipleri Ek-18'de örneklenir; seansın bölümlerine göre girilebilecek emir tipleri Ek-19'da verilir. [5.4, s. 87]
3. Ek-18 1.1 tablosundaki değerler parametriktir; önceden duyurularak işlem sırası bazında ya da tüm piyasa için değiştirilebilir. [Ek-18 1.1, s. 203]

### B. Limit Fiyatlı Emirler (LFE) (5.4.1)
4. Limit fiyatlı emir, fiyatın ve miktarın belirtildiği emirdir. [5.4.1, s. 87]
5. Limit emrin gerçekleşmeyen bölümü işlem görmedikçe Sistemde pasif olarak geçerlilik süresi sonuna kadar bekletilir; KİE olarak girilmişse bekletilmez. [5.4.1, s. 87; 5.6.5, s. 94]

### C. Piyasa Emirleri (5.4.2; Ek-18 2)
6. Piyasa emri (market order), fiyat olmaksızın yalnızca miktar belirtilerek girilen emirdir. [5.4.2, s. 87; Ek-18 2, s. 206]
7. Piyasa emri karşı taraftaki en iyi fiyatlı emirlerle eşleşerek işleme dönüşür; en iyi fiyattan başlayarak emir tamamen işlem görene kadar tüm fiyat seviyelerindeki emirlerle eşleşir. [5.4.2, s. 87; Ek-18 2.1, s. 206]
8. Piyasa emri yalnızca KİE olarak girilebildiğinden karşı tarafta eşleşecek hiçbir emir yoksa otomatik olarak iptal edilir. [5.4.2, s. 87; Ek-18 2.1, s. 206]
9. Piyasa emri, Ek-18 2.1'e göre Kalanı İptal Et, Gerçekleşmezse İptal Et ve Gün koşullarıyla kullanılabilir; BISTECH Sisteminin ilk aşamasında yalnızca Kalanı İptal Et koşuluyla kullanımına izin verilmiştir. [Ek-18 2.1, s. 206]
10. Piyasa (Kalanı İptal Et): Karşı taraftaki en iyi fiyatlı emirlerden işleme dönüşür; karşılanmadan kalan kısım iptal edilir. [Ek-18 2.1, s. 206]
11. Piyasa (Gerçekleşmezse İptal Et): Girilen emir miktarının tamamının karşılanması esastır; tamamının karşılanmaması durumunda emrin tümü iptal edilir. [Ek-18 2.1, s. 207]
12. Piyasa (Gün): Kesir Sürekli İşlem ve Kesir Kapanış Fiyatından İşlem seansında kullanılabilir; emir gün sonuna kadar geçerlidir. [Ek-18 2.1, s. 207]
13. Kapanış bölümünde ve tek fiyat yönteminde emir toplama aşamasında girilen piyasa emirleri, eşleştirme başlayana kadar emir defterinde bekletilir; eşleştirme başladığında belirlenen eşleştirme fiyatından işleme dönüşür. [5.4.2, s. 87; Ek-18 2.1, s. 207]
14. İşleme dönüşmeyen piyasa emirleri seansın sürekli işlem veya takip eden tek fiyat bölümüne aktarılmaz, iptal edilir. [5.4.2, s. 87–88; Ek-18 2.1, s. 207]
15. Tek fiyat yönteminde piyasa emirlerinin limit fiyatlı emirlere göre fiyat önceliği vardır; piyasa emirleri kendi aralarında zaman önceliğine göre değerlendirilir. [Ek-18 2.1, s. 207]
16. Piyasa emirlerinde sabit maksimum emir değeri sınırı uygulanmaz; her pay sırası için o sırada geçerli maksimum emir değeri sınırı kullanılır (bkz. bölüm L). [5.4.2, s. 88]
17. Piyasa emrinin tutarı en son işlem fiyatı üzerinden hesaplanır; son işlem fiyatı yoksa bir önceki kapanış fiyatına bakılır; her ikisi de yoksa Borsa tarafından manuel girilmiş bir fiyat varsa ona bakılır; yoksa işlem olana kadar Sistem tarafından piyasa emri girilmesine izin verilmez. [5.4.2, s. 88]
18. Serbest marj uygulanan ve ilk işlem fiyatının baz fiyatı oluşturduğu işlem sıralarında baz fiyatın oluştuğu seansın sonuna kadar piyasa emri girilemez. [5.4.2, s. 88]
19. Yıldız Pazarda, Ana Pazarda ve açılış seansına dâhil olan pay dışındaki sermaye piyasası araçlarında açılış seansında piyasa ve piyasadan limite emir türleriyle emir girilebilir (15/09/2023 tarihli ve 2023/19885 sayılı Duyuru; 25/09/2023 tarihinden itibaren geçerli). Açılış seansında piyasa ve piyasadan limite emirlerinin girilebileceği payların kapsamı için bkz. `03-tek-fiyat.md` madde 24. [5.4.2 dipnot 53, s. 87] Uygulama kararı (kullanıcı): paylarda açılışta piyasa ve piyasadan limite emri yalnızca Yıldız Pazar ve Ana Pazar'da girilebilir (Tablo-4); pay dışı araçlarda girilebilir (dipnot 53).
20. Sürekli işlemde piyasa emri emir defterinde saklanamaz; Kalanı İptal Et (IOC) veya Hepsi ya da Hiçbiri (FoK) geçerlilik süresinde olmalıdır; eşleşmeyen durumlardaki seanslarda deftere girebilir, seans eşleşen duruma geçince işleme dönüşür ve/veya iptal edilir. (`04-surekli-islem.md` madde 44 ile aynı kural.) [FIX 6.6.3.1]

### D. Piyasadan Limite Emirler (5.4.3; Ek-18 3)
21. Piyasadan limite emri (Market To Limit), piyasa emri gibi fiyatsız, yalnızca miktar belirtilerek girilen emirdir. [5.4.3, s. 88; Ek-18 3, s. 208]
22. Piyasadan limite emri karşı taraftaki yalnızca en iyi fiyat kademesinde bekleyen emirlerle eşleşerek işleme dönüşür. [5.4.3, s. 88; Ek-18 3.1, s. 208]
23. İşleme dönüşmeyen kısım, gerçekleştiği son işlem fiyatını alarak limit fiyatlı emre dönüşür ve emir defterinde pasif olarak yazılır; KİE olarak girilirse pasife yazılmaz. Kısmen gerçekleşen emrin kalanı, işlemin kısmi olarak gerçekleştiği fiyattan limit fiyatlı olarak pasife yazılır. [5.4.3, s. 88; Ek-18 3.1, s. 208]
24. Seansın sürekli işlem bölümünde girildiği anda hiç işleme dönüşmemiş piyasadan limite emri iptal edilir. [5.4.3, s. 88; Ek-18 3, s. 208]
25. Kapanış bölümünde ve tek fiyat yönteminde emir toplama aşamasında girilen piyasadan limite emirleri, eşleştirme başlayana kadar emir defterinde bekletilir; eşleştirme başladığında belirlenen eşleştirme fiyatından işleme dönüşür. [5.4.3, s. 88; Ek-18 3.1, s. 209]
26. Tek fiyat yönteminde işleme dönüşmeyen kısım eşleştirme fiyatından limit fiyatlı emre dönüşerek emir defterinde pasif tutulur ve bir sonraki seansa aktarılır (sürekli işlem aşamasına geçerken gerçekleştiği son işlem fiyatını alır; KİE ise pasife yazılmaz). [5.4.3, s. 88; Ek-18 3.1, s. 209; Ek-18 3.3, s. 210]
27. İlgili açılış, kapanış ve tek fiyat bölümünde fiyat oluşmaması hâlinde piyasadan limite emri iptal edilir. [5.4.3, s. 88]
28. Piyasadan limite emirleri Kalanı İptal Et, Gerçekleşmezse İptal Et, Gün ve Tarih koşullarıyla kullanılabilir; tek fiyat yöntemiyle gerçekleştirilen seanslarda Gerçekleşmezse İptal Et koşuluyla birlikte kullanılamaz. [Ek-18 3.1, s. 208]
29. Piyasadan limite (Kalanı İptal Et): Karşı taraftaki yalnızca en iyi fiyat kademesindeki emirlerle işleme dönüşür; karşılanmadan kalan kısım iptal edilir. [Ek-18 3.1, s. 209]
30. Piyasadan limite (Gerçekleşmezse İptal Et): Emir miktarının tamamının karşı taraftaki en iyi fiyat kademesindeki emirlerle karşılanması esastır; karşılanmazsa emrin tümü iptal edilir. [Ek-18 3.1, s. 209]
31. Piyasadan limite (Gün): En iyi fiyat kademesindeki emirlerle işleme dönüşür; karşılanmadan kalan kısım gün sonuna kadar geçerli olmak üzere gerçekleşen işlem fiyatı üzerinden pasife yazılır. [Ek-18 3.1, s. 209]
32. Piyasadan limite (Tarih): En iyi fiyat kademesindeki emirlerle işleme dönüşür; karşılanmadan kalan kısım girilen tarih sonuna kadar geçerli olmak üzere gerçekleşen işlem fiyatı üzerinden pasife yazılır. [Ek-18 3.1, s. 209]
33. Tek fiyat yönteminde piyasadan limite emirleri limit fiyatlı emirlere göre fiyat önceliğine sahiptir; varsa diğer piyasa emirleri ve piyasadan limite emirleriyle zaman önceliğine göre değerlendirilir. [Ek-18 3.1, s. 209]
34. Piyasadan limite emri maksimum emir değeri sınırına tabidir; tutar piyasa emirlerinde olduğu gibi belirlenir (madde 17). [5.4.3, s. 88]
35. Serbest marj uygulanan ve ilk işlem fiyatının baz fiyatı oluşturduğu işlem sıralarında baz fiyatın oluştuğu seansın sonuna kadar piyasadan limite emri girilemez. [5.4.3, s. 88]
36. Piyasa ve piyasadan limite emirleri arasındaki farklar (Ek-18 3.3, s. 210): piyasa emri tüm fiyat seviyelerinden eşleşir, piyasadan limite emri yalnızca en iyi fiyat kademesinden; eşleşmeden kalan kısım piyasa emrinde iptal edilir, piyasadan limite emrinde işlem gerçekleşen fiyattan pasife yazılır; tek fiyat yönteminde piyasa emrinin eşleşmeyen kısmı iptal edilir ve sonraki seansa aktarılmaz, piyasadan limite emrinin eşleşmeyen kısmı eşleşme fiyatından pasife yazılarak sonraki seansa aktarılabilir; birlikte girilebilen koşullar piyasa emrinde Kalanı İptal Et, Gerçekleşmezse İptal Et, Gün; piyasadan limite emrinde Kalanı İptal Et, Gerçekleşmezse İptal Et, Gün, Tarih'tir. [Ek-18 3.3, s. 210]
37. Piyasadan limite (Market-to-Limit) emir yalnızca en iyi fiyat seviyesinde eşleşir (defteri taramaz); karşı tarafta emir yoksa hemen iptal edilir; kalan miktar gerçekleşme fiyatından limit emir olarak deftere yazılır ve sonraki raporlarda emir tipi Limit, fiyat gerçekleşme fiyatı olur. Eşleşmeyen müzayede (auction) durumunda girilen piyasadan limite emirlerin tüm miktarı uncross sonrasında limit emre dönüştürülür. (`04-surekli-islem.md` madde 45 ile aynı kural.) [FIX 6.6.3.2]

### E. Dengeleyici Emirler (5.4.4; Ek-18 4)
38. Dengeleyici emir (Imbalance/IMB), açılış ve kapanış seansları dâhil tek fiyat yönteminin uygulandığı tüm seans bölümlerinde, fiyat belirleme sürecinde hesaba katılmayan ancak belirlenen eşleşme fiyatı seviyesinde karşılanmadan kalan emirlerle işlem yapmak üzere girilen emirdir. [5.4.4, s. 88; Ek-18 4, s. 211]
39. Dengeleyici emirler, eşleşme fiyatından kalan emirler bittiğinde veya eşleşme fiyatından kalan emir yoksa birbirleriyle de eşleşme fiyatından işleme dönüşebilir. [5.4.4, s. 88]
40. Eşleşmeden kalan dengeleyici emirler iptal edilir. [5.4.4, s. 88; Ek-18 4, s. 211]
41. Dengeleyici emir yalnızca KİE olabilir ve açığa satış olarak yalnızca açığa satışa izin verilen seans bölümlerinde girilebilir (yalnızca yukarı adım kuralı uygulanmayan sıralarda). [Ek-18 1.1 (1)(2)(3), s. 203]
42. Dengeleyici emir FIX'te TimeInForce = 9 (At Crossing), Price = 0 ve OrdType = 1 (Market) olarak girilir. [FIX 6.6.4, 6.6.9]
43. Dengeleyici emir kuralları (hesaba katılmama, işlem görme sırası, öncelik) için bkz. `03-tek-fiyat.md` madde 44–55. [5.4.4, s. 88]

### F. Koşullu emirler (5.4.5; Ek-18 5)
44. Koşullu emirler, girilen emrin aktif hâle gelmesi veya işleme dönüşebilmesi için bazı koşulların tanımlanabildiği emirlerdir; dört şekilde verilebilir: miktar koşullu, fiyat koşullu, zaman koşullu, kısmi görünme koşullu. [5.4.5, s. 88]
45. Miktar koşullu emirler (Hepsi ya da Hiçbiri – AON; Gerçekleşmezse İptal Et – FoK), fiyat koşullu emirler (durdurma/stop emirleri) ve zaman koşullu emirler (açılışta/kapanışta geçerli, at open/at close) için Prosedür "devreye alınma zamanı ayrıca duyurulacaktır" der; Ek-18 5 bunları yeni sistemin ilk etabında kullanılmayacak emirler olarak niteler. Bu dosyada kural olarak kodlanmaz. [5.4.5 a, b, c, s. 88–89; Ek-18 5, s. 211]
46. Ek-18'de yer alan ancak devreye alınmamış emir davranışı özetleri (kodlanmaz, yalnızca bilgi): AON — tamamı tek seferde karşılanmazsa emir pasife yazılır (5.1.1, s. 211); FoK — tamamı tek seferde karşılanmazsa emrin tamamı iptal olur (5.1.2, s. 213); durdurma emri — fiyat şartı gerçekleşene kadar emir defterinde yer almaz (5.2.1, s. 214); kapanış/açılış emirleri — Seans Zamanına Kadar Geçerli koşuluyla girilir, ilgili seans başlayana kadar emir defterinde yer almaz ve seans başlangıcıyla tetiklenerek seansa dâhil edilir (5.3.1–5.3.2, s. 216). [Ek-18 5.1–5.3, s. 211–216]

#### Kısmi görünme koşullu emirler (5.4.5 ç; Ek-18 5.4)
47. Limit fiyatlı emirler kısmen görünme koşuluyla girilebilir. [5.4.5 ç, s. 89; Ek-18 5.4, s. 216]
48. Emir defterinde görülmesi istenen kısmın tamamı işlem gördüğünde gizli bölümden, tamamı işlem görmüş olan miktar kadar kısım açığa çıkar ve girilmiş olan limit fiyatından emir defterine yazılır. [5.4.5 ç, s. 89; Ek-18 5.4, s. 216]
49. Açığa çıkan kısım, açığa çıktığı anda girilmiş yeni bir emir gibi fiyat ve zaman önceliğine göre emir defterinde yerini alır ve yenilenen kısım aynı emir numarasını alır. (Öncelik hükmü için `04-surekli-islem.md` madde 30.) [5.4.5 ç, s. 89; Ek-18 5.4, s. 217]
50. Bu süreç emrin tamamı karşılanıp bitinceye, geçerlilik süresi sona erinceye veya emir iptal edilinceye kadar devam eder. [5.4.5 ç, s. 89; Ek-18 5.4, s. 216]
51. Açılış ve/veya kapanış seanslarında girildiğinde emrin toplam miktarı (görünen + gizli) eşleşme fiyatı hesaplamasında dikkate alınır. [Ek-18 5.4, s. 217]
52. Emrin görünen miktarı ile toplam miktarı arasındaki oran asgari %20 olabilir; bu oran emrin girişi ya da değiştirilmesi sırasında geçerlidir (örnek: toplam 200 lotluk emirde görünen miktar 40 lot ve fazlası olabilir, 40 lottan az belirlenemez). [Ek-18 5.4, s. 217]
53. Emrin görünen kısmının tamamı işlem gördüğünde gizli bölümden işlem gören miktar kadar kısım veya emrin kalan kısmı görünen miktardan küçükse kalan miktar, girilmiş olan limit fiyatından emir defterine yazılır. [Ek-18 5.4, s. 217]
54. Tek fiyat belirleme aşamalarında ve sürekli işlem bölümlerinde, karşı taraftaki emir miktarına bağlı olarak emrin görünen kısımdan daha fazla miktarı ya da emrin tamamı (görünen + görünmeyen) tek seferde işlem görebilir. [Ek-18 5.4, s. 217]
55. Kısmi görünme koşullu emir, E (eski), F (borsa yatırım fonu), V (varant), C (sertifika) ve R (yeni pay alma hakkı) özellik kodlu sıralarda girilebilir. [Ek-18 5.4, s. 217]
56. Kısmi görünme koşullu emir, yukarı adım kuralının uygulanmadığı açığa satışa izin verilen sıralarda açığa satış olarak verilebilir. [Ek-18 5.4, s. 217]
57. Kısmi görünme koşullu emir limit emirlerde geçerli miktar ve tutar sınırlamalarına tabidir; bu sınırlamaların hesabında emrin toplam miktarı ve tutarı (yalnızca görünen kısım değil) dikkate alınır. [Ek-18 5.4, s. 217; Ek-18 1.1 (5), s. 203; 5.6.4, s. 92]
58. Kısmi görünme koşullu emir KİE olarak girilebilir (emrin özelliğiyle uyumlu bir kullanım olmadığı belirtilmiştir). [Ek-18 5.4, s. 217]
59. Limit fiyatlı emirlere ilave olarak piyasa ve piyasadan limite emirler de kısmen görünme koşuluyla girilebilir. [Ek-18 5.4, s. 217]
60. Kısmi görünme koşullu emirler TW'den piyasa emri olarak girilebilir ancak FIX'ten piyasa emri olarak girilemez; TW'den piyasadan limite/KİE olarak girilebilir ancak FIX'ten bu şekilde girilemez; TW'den ve FIX'ten piyasadan limite/GÜN olarak girilebilir; OUCH kullanıcıları tarafından iletilemez. [Ek-18 5.4, s. 217–218]
61. Kısmi görünme koşullu emir FIX'le değiştirilirken `max floor` alanı gönderilmezse ilk gönderilen `max floor` bilgisi değişiklik isteğine otomatik eklenir; bu ekleme emrin görünen kısmında artışa yol açıyorsa toplam miktar azalmış olsa dahi emir önceliğini kaybeder. [Ek-18 5.4, s. 217]
62. FIX'te kısmi görünme `MaxFloor (111)` ile belirtilir; `MaxFloor = 0` (tamamen gizli emir) desteklenmez, sıfırlamak emrin tamamını görünür kılar; emir kısmen gerçekleştiğinde MaxFloor değeri azaltılır. [FIX 6.6.6]
63. Kısmi görünme koşullu emir, Ek-19'da yalnızca G sütunu 1 olan seans bölümlerinde girilebilir (bkz. madde 139–140). [Ek-19, s. 226–229] Uygulama kararı (kullanıcı): Ek-19 matrisi esastır; Ek-18 5.4'teki "tüm bölümlerde girilebilir" ifadesi genel tanım sayılır.

### G. Kotasyon emirleri (5.4.6, 5.6.3)
64. Kotasyon emri, limit fiyatlı alış ve satış emrinden oluşan ve yalnızca piyasa yapıcı/likidite sağlayıcı üyeler tarafından girilebilen emir tipidir; kotasyonu oluşturan alış ve satış emrine kotasyon emri denir. [5.4.6, s. 89]
65. Kotasyon emri bir bütün olarak iptal edilebileceği gibi yalnızca alış veya satış tarafı da iptal edilebilir. [5.4.6, s. 89]
66. Paylarda piyasa yapıcı üyenin bir kerede girebileceği maksimum kotasyon tutarı, ilgili sermaye piyasası aracının maksimum emir değeri gruplandırmasındaki grubuna karşılık gelen miktarla sınırlıdır (Tablo-14, madde 115). [5.6.3, s. 92]
67. Kotasyon açığa satış olarak verilemez ve KİE olarak girilemez. (tablodan) [Ek-18 1.1, s. 203]
68. Kotasyon emri OUCH'ta Mass Quote (en çok 5 kotasyon) ile iletilir; bir kotasyonun tarafı fiyat ve miktar sıfır yapılarak iptal edilir; bir tarafı değişmeden bırakmak için o taraftaki miktar 0 yapılır. [OUCH 4.1.5]

### H. Orta Nokta emirleri (5.4.7; Ek-18 6)
69. Orta Nokta emri (Mid-Point), normal emir defterine kıyasla daha büyük miktarlı emirlerin kendi aralarında eşleşmesine imkân sağlayan emir türüdür. [5.4.7, s. 89; Ek-18 6, s. 219]
70. Emirler sürekli olarak otomatik eşleşmeye tabidir; normal emir defterinde bekleyen en iyi alış ve en iyi satış emirlerinin fiyatlarının aritmetik ortalaması ile fiyatlanır ve ayrı ve kapalı bir emir defterinde işlem görür. [5.4.7, s. 89; Ek-18 6, s. 219]
71. Orta Nokta emirleri kendi içinde Orta Nokta Piyasa (MPM) ve Orta Nokta Limit (MPL) olarak ikiye ayrılır; her ikisi de eşleşme anında normal emir defterinde oluşan Orta Nokta fiyattan işleme dönüşür. [Ek-18 6.2, s. 219–220]
72. MPL emri, Orta Nokta fiyatının emrin limit fiyatına eşit veya daha iyi olması durumunda işleme dönüşür; Orta Nokta fiyat limit fiyattan daha kötüyse işleme dönüşmez ve emir defterinde yerini alır. [Ek-18 6.2, s. 220]
73. Orta Nokta emirler yalnızca kendi aralarında eşleşir ve yalnızca zaman önceliğine göre sıralanır (MPM emirlerinin MPL emirlere karşı fiyat önceliği yoktur). [Ek-18 6.2, s. 220]
74. Orta Nokta emrin girişi ve miktarının değiştirilmesi sırasında minimum ve maksimum tutar kontrolü yapılır; değer asgari 100.000 TL, azami 30 milyon TL olabilir. Kısmi işlem görme durumunda kalan kısım, kalan miktarda değişiklik yapılmadığı sürece asgari sınırın altına düşse bile bu kısıt aranmaz. [5.4.7, s. 89; Ek-18 6.2, s. 220; 5.6.4, s. 93]
75. Tutar hesabı: MPL alış emrinde limit fiyat mevcut Orta Nokta fiyatından düşükse limit fiyat, yüksekse Orta Nokta fiyat kullanılır; MPL satış emrinde limit fiyat mevcut Orta Nokta fiyatından yüksekse limit fiyat, düşükse Orta Nokta fiyat kullanılır; MPM'de Orta Nokta fiyat kullanılır. [Ek-18 6.2, s. 221]
76. İşlem gerçekleşmesinin ardından miktar bilgisi piyasaya gönderilir; işlemin miktarı ve hacmi ilgili sıranın miktar ve hacmine dâhil edilir ancak fiyat istatistikleri (en yüksek, en düşük, son işlem fiyatı vb.) piyasada yayımlanmaz; Orta Nokta emir defterine ilişkin bilgi yayını yapılmaz. [5.4.7, s. 89; Ek-18 6.2, s. 220]
77. İlgili payın sırasında alış veya satış tarafında bekleyen bir emir yoksa fiyat aralığı (spread) oluşmayacağından Orta Nokta emir girişine veya eşleşmesine izin verilmez. [Ek-18 6.2, s. 220]
78. Fiyat aralığı varken girilmiş Orta Nokta emir, aralık ortadan kalktığında iptal olmaz ve beklemeye devam eder ancak yeni Orta Nokta emir girilemeyeceği için işleme dönüşemez; fiyat aralığının olmadığı durumlarda aralık varken girilmiş emrin değiştirilmesine de izin verilmez. [Ek-18 6.2, s. 220]
79. Orta Nokta emirler yalnızca seanslık olarak, seansın yalnızca sürekli işlem bölümünde ve BIST 30 kapsamındaki paylarda girilebilir; açığa satış olarak verilemez; kısmi görünme koşullu olarak girilemez; KİE olarak girilebilir ancak günlük ya da tarihli gönderilen bir Orta Nokta limit emir KİE'ye dönüştürülemez. [5.4.7, s. 89; Ek-18 6.2, s. 220–221; Ek-18 1.1, s. 203]
80. Sürekli işlem bölümünde girilen ancak işleme dönüşmeyen Orta Nokta emirler, seans sürekli işlem dışında bir bölüme geçtiğinde Sistem tarafından iptal edilir. [Ek-18 6.2, s. 220]
81. Normal emir Orta Nokta emre, Orta Nokta emir de normal emre dönüştürülemez; MPM ve MPL birbirine dönüştürülemez. [Ek-18 6.2, s. 220]
82. Sistem, MPL emrin fiyat limitleri dışında girilmesine ya da fiyat limitleri dışına değiştirilmesine engel olmaz; alış-satış emirleri ve fiyat aralığı fiyat limitleri dışında oluşamayacağından fiyat limitleri dışında işlem gerçekleşmez. MPL emrin fiyatı fiyat adımı kuralına uygun olmalıdır. [Ek-18 6.2, s. 220–221]
83. MPL emrinde her türlü fiyat değişikliği, MPL ve MPM emirlerinde miktar artırma emrin zaman önceliğini kaybettirir. [Ek-18 6.2, s. 221]
84. Orta Nokta fiyattan gerçekleşen işlemlerin fiyatı terminal, emir ve işlem raporlarında virgülden sonra 3 hane olarak yer alır; takas pozisyonları işlem bazında virgülden sonra iki haneye yuvarlanarak oluşturulur. [Ek-18 6.2, s. 221]

### I. Ağırlıklı Ortalama Fiyat (AOF/TAR) emirleri (5.4.8; Ek-18 7)
85. AOF emri (TAR – Trade At Reference), işlem günü sonunda ilgili pay sırasında oluşacak AOF ya da kapanış fiyatı gibi bir fiyatı referans alarak işlem yapılmasına imkân tanıyan emir/işlem türüdür; işlem günü sonunda oluşacak AOF veya AOF ± Borsa tarafından belirlenecek sayıda fiyat adımı seviyesinden gün içinde işlem yapılır. [5.4.8, s. 89; Ek-18 7, s. 222]
86. AOF emirleri merkezi emir defterinden ayrı bir sırada (örnek: GARAN.AOF) kapalı emir defteri ve sürekli işlem esasıyla işlem görür ve yalnızca kendi aralarında eşleşir. [5.4.8, s. 89–90; Ek-18 7.1, s. 223]
87. AOF emrinin Sisteme iletilebilmesi için ilgili pay sırasında (.E) gün içinde işlem olması gerekir. [Ek-18 7.1, s. 223]
88. Girişte ve miktar değişikliğinde minimum 100.000 lot ve maksimum 10 milyon lot kontrolü yapılır; miktar 100.000 ve üzerinde 1.000'in katları olarak girilir (100.001 veya 100.999 gibi değerlere izin verilmez); maksimum TL sınırı kontrolü yapılmaz. [5.4.8, s. 90; Ek-18 7.1, s. 223–224; 5.6.4, s. 93]
89. AOF emri fiyatsız (piyasa emri; fiyat alanı boş veya 0,00) ya da limit fiyatlı olarak girilebilir; limit fiyatlı girilirse fiyat alanına −0,02, −0,01, 0,00, 0,01 veya 0,02 değerleri girilebilir (fark/delta). Piyasadan limite olarak verilemez; piyasa emri ya da KİE olarak verilebilir. [Ek-18 7.1, s. 223]
90. AOF işlem fiyatı = gün sonunda ilgili payın .E sırasında oluşan AOF + girilen fark (delta); fiyat adımına göre yuvarlama yapılmaz, fiyat virgülden sonra 3 basamak olabilir; AOF sıralarında fiyat adımı 0,01 TL'dir. Takas pozisyonları işlem bazında virgülden sonra iki haneye yuvarlanır. [Ek-18 7.1, s. 223–224]
91. Fiyatsız girilen AOF emirleri gün sonunda oluşacak AOF ile fiyatlanır; fiyatsız piyasa emri olarak girilirse karşıda bekleyen emirlere göre farklı fiyatlardan işlem gerçekleşmesi mümkündür; işlemler öncelik kurallarına göre pasifteki emrin fiyatına bağlı olarak girilen emrin fiyatından daha iyi bir fiyattan gerçekleşebilir. [Ek-18 7.1, s. 223]
92. AOF emirleri yalnızca seanslık emir olarak, yalnızca BIST-30 kapsamındaki paylarda girilebilir ve açığa satış olarak girilemez. [5.4.8, s. 90; Ek-18 7.1, s. 223]
93. AOF işlemleri sonrasında piyasaya bilgi verilmez; AOF işlemlerine ilişkin toplam işlem miktarı ve hacmi yayımlanmaz, işlem bilgileri Günlük Bültende yer alır ve toplam piyasa işlem miktarı ve hacim bilgilerine ilave edilir. AOF işlemi .E sırasında gerçekleşen miktar ve hacme dâhil edilmez. [5.4.8, s. 90; Ek-18 7.1, s. 223; Ek-18 7.2, s. 225]
94. .AOF sırasının bağlı olduğu payın işlemleri durdurulursa .AOF sırasındaki işlemler de durdurulur; durdurulma gün sonuna kadar devam ederse durdurma anında paylarda oluşan AOF, .AOF sırasındaki işlemlerin fiyatını belirlemekte kullanılır. [Ek-18 7.1, s. 224]
95. Gün sonunda AOF'nin tavan ya da taban fiyattan oluşması hâlinde delta eklenince .AOF fiyatı .E sırasındaki fiyat limitlerinin dışında oluşabilir; .AOF sırasındaki işlemler .E sırasındaki fiyat istatistiklerini etkilemez. [Ek-18 7.1, s. 224]

### J. Küsurat emirleri (5.4.9)
96. Küsurat emirler, işlem biriminin içerdiği miktardan daha az miktarda verilmiş emirlerdir; yalnızca miktar girilir, fiyat yazılmaz. [5.4.9, s. 90]
97. Küsurat işlemi, ilgili sermaye piyasası aracının ".E" sırasındaki son işlem fiyatından gerçekleştirilir; ayrı işlem sırasında (örnek: ABCDE.KE) bir adedin altındaki miktarlarla gerçekleşen işlemler aynı paya ait normal emir defterinde oluşan en son işlem fiyatı ile fiyatlandırılır. [5.4.9, s. 90]
98. Küsurat emirler karşı küsurat emirlerle kısmen eşleşebilir. [5.4.9, s. 90]
99. Küsurat emirlerinin devreye alınma zamanı ayrıca duyurulacaktır. [5.4.9, s. 90]
100. Küsurat emirleri hesaplamaya dâhil edilmez (tek fiyat yöntemi). (Bkz. `03-tek-fiyat.md` madde 45.) [Ek-16, s. 196]

### K. Emirlerde değiştirme ve iptal (5.5; Ek-18 1.2–1.3)
101. Sisteme girilmiş ve henüz işleme dönüşmemiş emirlerin üyeler tarafından değiştirilmesine ve iptal edilmesine ilişkin usul ve esaslar Yönetim Kurulu tarafından belirlenir. [5.5, s. 90]
102. Emir iptalinin koşulsuz olarak serbest bırakılması uygulamasıyla birlikte Sisteme girilmiş emirlerin miktarları azaltılıp artırılabilir ve fiyatları düşürülüp yükseltilebilir. [5.5.1, s. 90]
103. Miktar artırıldığında ve fiyat değiştirildiğinde emir Sisteme yeni girilmiş bir emir olarak değerlendirilir ve zaman önceliğini kaybeder. Öncelik kaybı/korunması kuralları için bkz. `04-surekli-islem.md` madde 20–29. [5.5.1, s. 90]
104. Emir iyileştirilmesi alış emri için fiyatı yükseltmek, satış emri için fiyatı düşürmek; emir kötüleştirilmesi alış emri için fiyatı düşürmek, satış emri için fiyatı yükseltmek anlamındadır. [5.5.1, s. 90]
105. Emirlerin işlem görmeyen kısmı istenildiği an iptal edilebilir. [5.5.2, s. 90]
106. Emir bilgileri (MPF-AFK-Hesap No) değiştirilemez. [Ek-18 1.2, s. 204] Uygulama kararı (kullanıcı): değiştirme isteği bu alanları değiştiriyorsa reddedilir; "öncelik kaybolur" ifadesi kodlanmaz.
107. FIX'te değiştirilebilen emir nitelikleri: OrderQty (38); MaxFloor (111); TimeInForce (59) ile birlikte ExpireDate (432) veya TradingSessionID (336); AllocID (70) (aktarım alanı); Price (44). Cancel Replace'te ayarlanmayan alanların önceki değerlerini koruduğu varsayılır; zorunlu alanlar değişsin değişmesin ayarlanmalıdır. [FIX 6.5.3, 6.5.3.1]
108. FIX'te emrin TimeInForce değeri IOC veya FoK olarak değiştirilemez; fiyat 0'a değiştirilemez (sıfır fiyat isteniyorsa emir silinip fiyatı 0 olan yeni emir girilmelidir); Order Cancel Request kısmi iptal için kullanılamaz. [FIX 6.5.3.1, 6.5.4]
109. OUCH Replace Order'da `Quantity` emrin istenen toplam miktarıdır (açık miktar + gerçekleşen miktar); `Price = 0` "değişiklik yok" anlamına gelir; OUCH Cancel Order kısmi iptali desteklemez, kısmi azaltma için Replace Order kullanılır. [OUCH 4.1.2, 4.1.2.1, 4.1.3]
110. Kullanıcı tipleri arasındaki değiştirme/iptal yetkileri (Ek-18 1.3, s. 204–206; matris s. 206): her kullanıcı tipi kendi emirlerini değiştirebilir ve iptal edebilir (D/İ); işlem terminali temsilcisi başka kullanıcının emrini değiştiremez ve iptal edemez (X/X); işlem terminali baş temsilcisi ve piyasa yapıcı kullanıcıları kendi kurumlarının tüm kullanıcılarının emirlerini değiştirebilir ve iptal edebilir (D/İ); FixAPI kullanıcıları kendi kurumlarındaki başka kullanıcıların emirlerini değiştiremez ancak iptal edebilir (X/İ); OUCH kullanıcıları yalnızca kendi emirlerini değiştirebilir ve iptal edebilir, başkalarının emirlerini değiştiremez ve iptal edemez (X/X). [Ek-18 1.3, s. 205–206]
111. Bir OUCH kullanıcısının girdiği emir aynı kuruma ait bir baş temsilci tarafından işlem terminaliyle değiştirilirse emri giren OUCH kullanıcısının bu emir üzerindeki değiştirme ve iptal yetkisi sona erer; emri ancak değişikliği yapan baş temsilci tekrar değiştirebilir ya da iptal edebilir. Terminalden girilen emir başka bir baş temsilci tarafından değiştirilirse bu durum söz konusu olmaz (emri giren kullanıcı emri tekrar değiştirebilir veya iptal edebilir). [Ek-18 1.3, s. 205]
112. Emirlerin değiştirilmesi/iptali ve ücretlendirmesi (Ek-20, kademeli ücret modeli) bu dosyanın kapsamı dışındadır; emir/işlem oranı (OTR) ve ücret muafiyeti ilkeleri kodlanmaz. [5.5.3, s. 90–91]

### L. Değer sınırları (5.6.4, 5.6.3; Ek-18 1.1)
113. PP'de işlem görmekte olan sıralara gönderilen limit, piyasa, piyasadan limite, dengeleyici, kısmi görünme koşullu emirlerde ve kotasyonlarda maksimum emir değeri sınırı (maksimum TL kuralı) uygulanır; bir sıraya bir seferde girilen emrin veya kotasyonun TL değeri belirlenen sınırı geçemez. [5.6.4, s. 92]
114. Maksimum emir değeri sınırı Orta Nokta ve AOF emirlerine uygulanmaz. [5.6.4, s. 92–93]
115. Paylar günlük ortalama işlem hacmi ve piyasa değeri sıralamasına göre 6 gruba ayrılmıştır; grup başına maksimum emir değeri (Tablo-14): 1. Grup 10 milyon TL; 2. Grup 7,5 milyon TL; 3. Grup 5 milyon TL; 4. Grup 2,5 milyon TL; 5. Grup 1 milyon TL; 6. Grup 0,5 milyon TL. (tablodan) [5.6.4, s. 92–93]
116. Paylar 6 ayda bir son 6 aylık verilerle yeniden değerlendirilir; her pay için belirlenen sınırlar en az iki gün önceden duyurularak Ocak ve Temmuz aylarında yürürlüğe girmek üzere güncellenir. [5.6.4, s. 93]
117. PP'de yeni işlem görmeye başlayacak pay sırasının maksimum emir değeri PPD tarafından resen belirlenir. [5.6.4, s. 93]
118. Varantlar (.V) için maksimum emir değeri 250.000 TL; sertifikalar (.C) için 1 milyon TL; Borsa Yatırım Fonu, Gayrimenkul Yatırım Fonu, Girişim Sermayesi Yatırım Fonu katılma payları ve Gayrimenkul Sertifikaları için 5 milyon TL; emtia sertifikaları için 1 milyon TL'dir. [5.6.4, s. 93]
119. Temerrüt ve Resmî Müzayede sıraları için maksimum emir değeri 2,5 milyon TL, birincil piyasada (.BE sıralarında) 500.000 TL'dir; bu sınırlar PPD tarafından satışı/alışı talep edilen miktara göre farklı belirlenebilir. [5.6.4, s. 93]
120. Yeni Pay Alma Hakkı Kuponlarının (.R) maksimum emir değeri ilgili pay sırasının maksimum emir değeri ile aynıdır. [5.6.4, s. 93]
121. Orta Nokta emirlerde miktar sınırı olmaksızın alt sınır 100.000 TL, üst sınır 30 milyon TL; AOF emirlerinde TL sınırı olmaksızın miktar bazında alt sınır 100.000 adet, üst sınır 10 milyon adettir. [5.6.4, s. 93]
122. Ek-18 1.1 emir türlerine göre açığa satış, KİE ve sınır özet tablosu (tablodan; "M" = milyon TL/adet; sütun kayması riski yok):

| Emir türü | Açığa satış olarak verilebilir mi? | KİE olarak girilebilir mi? | Min–maks TL sınırı (*) | Min–maks miktar sınırı (*) |
|---|---|---|---|---|
| Limit | Evet | Evet | 0,010 – 10 M | 1 – 10 M |
| Piyasa | Evet (1) (2) | Evet (3) | 0,010 – 10 M | 1 – 10 M |
| Piyasadan Limite | Evet (1) (2) | Evet | 0,010 – 10 M | 1 – 10 M |
| Dengeleyici | Evet (1) (2) | Evet (3) | 0,010 – 10 M | 1 – 10 M |
| Özel İşlem Bildirimi (1. Kademe) | Hayır | Hayır | 10 M – 50 M | --- (4) |
| Özel İşlem Bildirimi (2. Kademe) | Hayır | Hayır | 50.000.001 – 250 M | --- (4) |
| Kısmi Görünme Koşullu | Evet | Evet | 0,010 – 10 M (5) | 1 – 10 M (5) |
| Kotasyon | Hayır | Hayır | 0,010 – 10 M | 1 – 10 M |
| Orta Nokta | Hayır | Evet | 100.000 – 30 M | --- |
| AOF (TAR) | Hayır | Evet | --- | 100.000 – 10 M |

(1) Yalnızca yukarı adım (up-tick) kuralı uygulanmayanlarda açığa satış olarak verilebilir. (2) Piyasa, piyasadan limite ve dengeleyici emirler yalnızca açığa satışa izin verilen seans bölümlerinde "açığa satış" olarak girilebilir. (3) Yalnızca KİE olabilir. (4) Sınır tanımlanmamıştır ancak Sistemde mevcuttur, önceden duyurularak tanımlanabilir. (5) Maksimum TL ve maksimum miktar sınırı için yalnızca görünen kısım değil, toplam tutar ve toplam miktar dikkate alınır. [Ek-18 1.1, s. 203]

### M. Geçerlilik süreleri (5.6.5)
123. Sisteme iletilen emirler dört farklı geçerlilik süresine sahip olabilir: Günlük, Kalanı İptal Et (KİE), İptale Kadar Geçerli (İKG), Tarihli. [5.6.5, s. 93]
124. Günlük: PP'deki bütün pazarlarda aksi belirtilmedikçe girilen her emir girildiği gün boyunca geçerlidir; işlem görmezse gün sonunda iptal edilir. [5.6.5, s. 93]
125. Kalanı İptal Et (KİE): Fiyat ve miktar belirtilerek girilen ve emrin girildiği anda karşılanmayan bölümünün otomatik olarak iptal edildiği emir türüdür. [5.6.5, s. 94]
126. İptale Kadar Geçerli (İKG): Borsa Birincil Piyasada Değişken ve Sabit Fiyatla Talep Toplama yöntemlerinde halka arz süresinin sonuna kadar geçerli emir girişi mümkündür; bu geçerlilik türü talep toplama yöntemiyle halka arzların gerçekleştirildiği birincil piyasada (.HE sıralarında) kullanılır. [5.6.5, s. 94; Ek-18 1.1, s. 204]
127. Tarihli: Fiyat adımı ve fiyat değişme sınırları çerçevesinde geçerli olacakları son tarih belirtilerek Sisteme girilen, işlem görene veya iptal edilene kadar Sistemde geçerliliğini koruyan emirlerdir; geçerli olabilecekleri azami süre Yönetim Kurulu tarafından belirlenir. [5.6.5, s. 94]
128. Bir emrin süresinin değiştirilmesine izin verilir; süre uzatıldığında emir önceliğini kaybeder, süre kısaltıldığında korur. (`04-surekli-islem.md` madde 25 ile aynı kural.) [5.6.5, s. 94; Ek-18 1.2, s. 204]
129. Gerçekleşmeyip süresi dolan emirler Sistem tarafından iptal edilir. [5.6.5, s. 94]
130. Emrin fiyatı belirlenen zaman içinde marj dışına çıktığında veya fiyat adımlarına uymadığında ilgili emir iptal edilir. [5.6.5, s. 94] Uygulama kararı (kullanıcı): bu iptal tarihli/süreli emirler için gün başında baz fiyat ve marjın yeniden belirlenmesi sırasında uygulanır; gün içi fiyat limiti kayması için madde 137'deki duraklatma uygulanır.
131. İlgili payın baz fiyatında sermaye artırımı ve/veya diğer nedenlerle bir değişme olmuşsa, ya da emrin sahibi olan üyenin kodu değişmişse bütün tarihli ve süreli emirler iptal edilir. [5.6.5, s. 94]
132. PP'de işlem yapma yetkileri geçici olarak kaldırılan veya kapatılan üyelere ait tarihli girilen emirler Borsa tarafından başka bir uyarıya gerek duyulmaksızın silinir. [5.6.5, s. 94]
133. Üye temsilcisi emirlerini kendi isteğiyle askıya alıp gün içinde istediği zaman tekrar aktif hâle getirebilir; bağlantının kopması gibi belirli durumlarda emirler Sistem tarafından otomatik olarak askıya alınabilir (gerekli tanımlamanın yapılması durumunda). [5.6.5, s. 94]
134. Emirlerin askıya alınması Sistem açısından iptal edilmesi ile eşdeğerdir; yalnızca bu emirler temsilci bilgisayarında tutulur, istenirse tekrar gönderilebilir. [5.6.5, s. 94] Uygulama kararı (kullanıcı): motor için askıya alınan emir iptal edilmiş sayılır; yeniden etkinleştirme yeni emir girişidir (yeni numara, öncelik kaybı); istemci tarafı (TW) kapsam dışıdır.
135. Askıya alma ve yeniden etkinleştirme imkânı FixAPI'de mevcut değildir; yalnızca temsilci iş istasyonlarında (TW) kullanılabilir. [5.6.5, s. 94]
136. FIX ve OUCH geçerlilik süreleri: FIX `TimeInForce (59)` değerleri 0 = Day, 1 = GTC, 3 = IOC, 4 = FoK, 6 = GTD (ExpireDate zorunlu), S = Good till End of Session (TradingSessionID ile), 9 = At Crossing (dengeleyici emir); OUCH `Time In Force` değerleri 0 = Day, 3 = Immediate or Cancel (FaK), 4 = Fill or Kill. OUCH'ta yalnızca limit emirler ve kotasyonlar kullanılabilir; Hepsi ya da Hiçbiri (AON) emirleri desteklenmez; Side değerleri B, S ve T (açığa satış). [FIX 6.6.4; OUCH 4.1.1; Prosedür 5.7.3, s. 97]
137. FIX emir durumları: New, Partially filled; nihai durumlar Rejected, Canceled, Filled, Expired, Suspended. Fiyat limitleri dışına çıkan emir duraklatılır (paused): eşleşmeye girmez, denge fiyatı hesabına katılmaz, fiyat resminde yer almaz; koşullar uygun hâle gelince özgün zaman önceliğiyle yeniden etkinleştirilir; `OrdStatus = Suspended (9)` ve `Text = "Paused"`. OUCH Order Accepted `Order State`: 1 = On book, 2 = Not on book, 98 = Paused. (`04-surekli-islem.md` madde 47 ile aynı kural.) [FIX 6.5.6, 6.6.2; OUCH 4.2.1] Uygulama kararı (kullanıcı): gün içi fiyat limitlerinin kayması nedeniyle limit dışında kalan emir iptal edilmez, duraklatılır; tarihli/süreli emirlerin gün başı marj iptali madde 130'dadır.
138. OUCH `Order Canceled` mesajındaki `Reason` (ChangeReason) değerlerinden eşleştirme motoru çıktısıyla ilgili olanlar (kaynak adları aynen): 1 = Canceled by user / Canceled by Other User; 3 = Trade; 5 = Replaced by User; 8 = Converted by System; 9 = Canceled by System; 12 = Triggered by System; 13 = Refreshed by System; 19 = Expired; 24 = Inactivated Day Order; 34 = Canceled After Auction; 35 = Inactivated Due to Outside Price Limits; 36 = Activated Due to Outside Limits; 39 = Undisclosed Quantity Order Converted; 40 = Inactivated Due to Order Value; 46 = Order deleted due to SMP; 47 = Cancelled due to connection termination; 52 = Paused; 53 = Activated Paused Order. [OUCH 4.2.4, Tablo 10]

### N. Seans bölümüne göre girilebilecek emir tipleri (Ek-19; Ek-11)
139. Ek-19 matrisi seans bölümü (satır) × emir tipi/işlem (sütun) izinlerini verir; 1 = var, 0 = yok; "1*" = yalnızca İKG limit fiyatlı emirler girilebilir. Sütunlar: A Limit, B Piyasa, C Piyasadan Limite, D Kalanı İptal Et, E Orta Nokta, F Dengeleyici, G Kısmi Görünme Koşullu, H Kotasyon, I Fiyat kötüleştirme, J Fiyat iyileştirme, K Miktar azaltma, L Miktar artırma, M Emir iptali, N Özel işlem bildirimi, O Açığa satış, P Emir derinlik bilgisi açık mı? [Ek-19, s. 226–229]
140. Ek-19'da A–O sütunlarından en az birinde 1 bulunan seans bölümleri (tablodan; P sütunu dâhil; 39 seans bölümü):

| Seans bölümü | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P_ACS_EMR_TP_EIY | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| P_ACS_EMR_TP_PY | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_ACS_EMR_TP_PY_EIY | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| P_ACS_EMR_TP2_PY | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P_ACS_EMR_TP2_PY_EIY | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| P_ACILIS_EMIR_TPL | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P_ACILIS_EMIR_TPL2 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P_BP_SUREKLI_ISLEM | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_BP_SUR_ISL_EBDK | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_DK_TEKFIY_EMIR_TPL | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_DK_TEKFIY_EMR_TPL2 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_TF_EMIR_TPL_EBDK | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_TF_EMIR_TPL2_EBDK | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_GECICI_DURDURMA_KS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DRDURMA_KS2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DURDURMA_SI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| P_GECICI_DURDURMA_TF | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DRDURMA_TF2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DUR_EBDK_SI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DUR_EBDK_KT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_GECICI_DUR_EBDK_BP | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| P_KAPANIS_EMIR_TPL | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_KAPANIS_EMIR_TPL2 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| P_KAPANIS_FIY_ISLEM | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| P_KESIR_KAPFIY_ISLEM | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_KESIR_SUREK_ISLEM | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_SUREKLI_ISLEM | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| P_TEKFIYAT_EMIR_TPL | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| P_TEKFIYAT_EMIR_TPL2 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| P_TEKTARAF_CAGRI_AC | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_TEKTARAF_CAGRI_GZ | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P_TEKTARAF_HLKARZ_AC | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P_TEKTARAF_HLKARZ_GZ | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P_TEKTRF_IPMO_CAG_AC | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| P_TEKTRF_IPMO_CAG_GZ | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P_TEKTRF_IPMO_HLA_AC | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| P_TEKTRF_IPMO_HLA_GZ | 1* | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P_SALTKOTASYON | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| P_SUREKLI_ISLEM_HFL | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |

141. Ek-19'da A–O sütunlarının tamamı 0 olan seans bölümlerinde hiçbir emir tipi girilemez, emir değiştirilemez ve iptal edilemez; bu bölümlerden P = 1 olanlar: P_ARA, P_ESLESTIRME, P_ESLESTIRME_B_H, P_ESLESTIRME_B_O, P_ESLESTIRME_I_H, P_ESLESTIRME_I_O, P_ESLESTIRME_EBDK, P_GUNSONU_ISLEMLERI, P_GUNSONU_ISTATISTIK, P_GUNSN_ISLM_EBDK_BP, P_GUNSN_ISTK_EBDK_BP, P_MARJ_YAYIN, P_MARJ_YAYIN_KAPANIS, P_MARJ_YAYIN_KAP_TF, P_MARJ_YAYIN_EBDK_BP, P_ESLESTIRME_FBS_B_H, P_ESLESTIRME_FBS_B_O, P_ESLESTIRME_FBS_I_H, P_ESLESTIRME_FBS_I_O, P_ESLESTIRMETEKFIYAT; P = 0 olanlar: P_BP_TEK_TARAF_CAGON, P_BP_TEK_TARAF_CAGSN, P_BP_TEK_TARAFLI_CAG, P_ENDEKS_YAYIN, P_ENDEKS_YAYIN_YOK, P_GECICI_DURDURMA, P_GECICI_DURDUR_EBDK, P_GUNSONU, P_MAKBUZ_YAYINI_YOK. (tablodan) [Ek-19, s. 226–228]
142. Sürekli işlem seansı (P_SUREKLI_ISLEM): limit emir, piyasa emri, piyasadan limite, KİE, Orta Nokta emri ve kısmi görünme koşullu emirler girilebilir; emirler üzerinde miktar ve fiyat değişikliği yapılabilir, emirlerin geçerlilik süreleri değiştirilebilir; özel işlem bildirimi yapılabilir; açığa satış yapılabilir; kotasyon emirleri girilebilir, değiştirilebilir, iptal edilebilir; emirler iptal edilebilir. [Ek-11 P_SUREKLI_ISLEM, s. 187]
143. Varant ve sertifikalarda hareketli fiyat değişme sınırlarının hesaplandığı sürekli işlem durumunda (P_SUREKLI_ISLEM_HFL) alış kotasyonu girilmeden önce emir girilemez; yalnızca limit emir ve KİE emirler girilebilir. [Ek-11 P_SUREKLI_ISLEM_HFL, s. 187]

## Açık sorular
- [DOĞRULANDI (davranış) – gün içi veri Mart 2025; profil `../veri/gunici-dogrulama/2025-03/profil/`] Sonuç: 4.712.234 yeni piyasa emrinin (sürekli işlem) 4.712.232'si ve müzayede bölümlerindeki yeni piyasa emirlerinin tamamı `IMMEDIATE` (KİE) geçerliliklidir, 2'si `DAY`'dir; Mart 2025'te piyasa emri fiilen yalnız KİE ile kullanılmıştır. Madde 8–9: 5.4.2 piyasa emrinin "sadece KİE olarak girilebildiğini" söyler; Ek-18 2.1 aynı emrin Kalanı İptal Et, Gerçekleşmezse İptal Et ve Gün koşullarıyla kullanılabileceğini, ilk aşamada yalnızca KİE'nin açık olduğunu söyler; FIX (6.6.3.1) sürekli işlemde IOC veya FoK ister. Güncel durumda hangi koşulların açık olduğu belgelerden belirlenemez.
- [DOĞRULA] Madde 12: "Kesir Sürekli İşlem ve Kesir Kapanış Fiyatından İşlem" seansları ve "Piyasa (Gün)" koşulu Ek-19'daki P_KESIR_SUREK_ISLEM / P_KESIR_KAPFIY_ISLEM (B = 1, D = 1) ile uyumlu görünür; küsurat emirlerinin devreye alınma tarihi ayrıca duyurulacaktır (5.4.9) ve belgelerde yoktur.
- [DOĞRULANDI – kullanıcı kararı (öneri onaylandı)] Madde 19: 5.4.2 dipnot 53'ün cümlesi ("Yıldız Pazarda, Ana Pazarda ve açılış seansına dahil olan pay dışındaki sermaye piyasası araçlarında açılış seansında piyasa ve piyasadan limite emir türleri ile emir girilebilir") ile `03-tek-fiyat.md` madde 24'teki ("Yıldız Pazar ve Ana Pazar'da yer almayan paylarda açılış seansında piyasa ve piyasadan limite emir türleri ile emir girilemez") ifade birbiriyle uyumsuz görünür; hangisinin geçerli olduğu belirlenemedi. Karar: Paylar için Tablo-4 esastır (Yıldız Pazar VAR, Ana Pazar VAR, Alt Pazar/YİP/PÖİP YOK); pay dışı araçlarda dipnotun "girilebilir" hükmü uygulanır; 03-tek-fiyat.md madde 24 ile aynıdır.
- [DOĞRULA] Madde 23, 26: "Sürekli işlem aşamasına geçerken ... son işlem fiyatını alarak" ifadesindeki "son işlem fiyatı" ile tek fiyatta eşleşme fiyatı arasındaki ilişki 5.4.3'te açık değildir; Ek-18 3.1 tek fiyatta kalanın eşleşme fiyatından tutulduğunu söyler. Sürekli işleme geçişte hangi fiyatın kullanıldığı kaynaktan kesin belirlenemedi.
- [DOĞRULA] Madde 26, 36: Ek-18 3.1 piyasadan limite emrinin tek fiyatta kalanının "bir sonraki seansa aktarıldığını" söyler; 5.4.3 "fiyat oluşmaması hâlinde ... iptal edilir" der. Bir sonraki seansın hangi seans (sürekli işlem veya sonraki tek fiyat) olduğu ve aktarım sırasında önceliğin nasıl belirlendiği yazılı değil.
- [DOĞRULA] Madde 20, 37: FIX 6.6.3.1–6.6.3.2 (04-surekli-islem.md madde 44–45) ile Prosedür 5.4.2–5.4.3 karşılaştırıldı: piyasa emrinin sürekli işlemde defterde saklanamaması ve piyasadan limite emrinin yalnızca en iyi fiyat kademesinde eşleşmesi Prosedürle uyumludur. FIX'in "TimeInForce IOC/FoK ise piyasadan limite emri piyasa emri gibi davranır" ifadesinin Prosedürdeki karşılığı yoktur.
- [DOĞRULA] Madde 45–46: AON, FoK, durdurma (stop) ve zaman koşullu emirlerin devreye alınma tarihleri kaynaklarda yoktur ("ayrıca duyurulacaktır"); OUCH AON'u desteklemez, FIX AON'u `ExecInst` ile destekler (FIX 6.6.6). Bu emir tipleri bu dosyada kodlanmadı.
- [KISMEN DOĞRULANDI – gün içi veri Mart 2025; ayrıntı `../veri/gunici-veri-dogrulama.md` bölüm 2 ve 9] Kısmi görünme koşullu emirler veride vardır ama `gorunen_miktar` alanı her satırda emir miktarına eşit yazıldığından görünen kısım ve oran (asgari %20) sınanamaz; görünen kısmın yenilenmesi sebep 13 (Refreshed by System) satırıyla görülür ve yenilenen emir fiyat seviyesinin sonuna gider (madde 30 / 04-surekli-islem.md madde 30 ile tutarlı). Madde 52, 62: Ek-18 5.4 görünen/toplam oranı için "asgari %20" der; FIX'te `MaxFloor` değişikliğinde davranış (emir kısmen gerçekleşince MaxFloor azaltılır) ile Ek-18'deki "açığa çıkan kısım görünen miktar kadar" kuralının (görünen miktarın sabit mi azalan mı olduğu) birbiriyle ilişkisi belirtilmemiştir.
- [DOĞRULANDI – kullanıcı kararı (öneri onaylandı)] Madde 63: Ek-18 5.4 "Seansın emir girilebilen tüm bölümlerinde girilebilirler" der; Ek-19'da G (Kısmi Görünme Koşullu) sütunu bazı emir girilebilen bölümlerde 0'dır (ör. P_BP_SUREKLI_ISLEM, P_BP_SUR_ISL_EBDK, P_KESIR_SUREK_ISLEM, P_KESIR_KAPFIY_ISLEM, P_SUREKLI_ISLEM_HFL, P_TEKTARAF_*). İki hüküm çelişir görünür; bu dosyada Ek-19 matrisi esas alındı. Karar: Ek-19 matrisi esastır; kısmi görünme koşullu emir yalnızca Ek-19'da G sütunu 1 olan seans bölümlerinde girilebilir (Ek-18'deki "tüm bölümlerde" ifadesi genel tanımdır).
- [DOĞRULA] Madde 66, 67: Kotasyon emrinin KİE olarak girilememesi ve açığa satış olarak verilememesi yalnızca Ek-18 1.1 tablosundan alındı (tabloda "Hayır"); Prosedür 5.4.6 bunu yazmıyor.
- [DOĞRULA] Madde 74: Orta Nokta emir değeri Prosedür 5.4.7 ve 5.6.4'te "asgari 100.000 TL, azami 30 milyon TL" olarak geçer; Ek-18 1.1'de de aynıdır. Orta Nokta fiyatı ve tutar hesabının fiyat adımına yuvarlanıp yuvarlanmadığı (Orta Nokta fiyatın 3 ondalık haneli olması dışında) yazılı değildir.
- [DOĞRULA] Madde 80: Ek-18 6.2 "seansın sürekli işlem bölümünde girilen ... Orta Nokta emirleri, seansın sürekli işlem haricinde bir bölüme geçmesi durumunda sistem tarafından iptal edilirler" der; geçici durdurma (P_GECICI_DURDURMA_*) durumunda iptal edilip edilmediği ayrıca yazılı değil (Ek-19'da bu bölümlerde E = 0).
- [DOĞRULA] Madde 88: Prosedür 5.4.8 AOF miktarının "yapılan düzenleme uyarınca" 100.000–10 milyon lot olmasını ister; Ek-18 7.1 ayrıca 1.000'in katı koşulunu ekler ve Ek-18 7.1 başka bir yerde "AOF (TAR) ... kapanış fiyatından da işlem görme özelliği" der. Kapanış fiyatıyla işlem seçeneğinin nasıl belirtildiği yazılı değil.
- [DOĞRULA] Madde 89, 90: Ek-18 7.1 "AOF sıralarında adım 0,01 TL'dir" (örnek: ISCTR.AOF fiyat adımı 0,10 TL, ISCTR.E fiyat adımı 0,50 TL) der; AOF sıralarındaki fiyat adımının sıraya göre değişip değişmediği ve girilebilecek delta değerleri (−0,02…0,02) ile "AOF ± Borsa tarafından belirlenecek sayıda fiyat adımı" ifadesinin ilişkisi belirsizdir. Ek-18 7.2 Örnek 2'de delta ±0,10 kullanılmıştır (−0,02…0,02 aralığı dışında).
- [DOĞRULA] Madde 97: Küsurat işleminin fiyatı Prosedürde ".E sırasındaki son işlem fiyatı" olarak yazılıdır; son işlem yoksa ne olacağı yazılı değildir. Ek-16 s. 196 küsurat emirlerinin tek fiyatta hesaplamaya dâhil edilmediğini söyler (03-tek-fiyat.md madde 45).
- [DOĞRULANDI – kullanıcı kararı (öneri onaylandı)] Madde 103, 106: Miktar azaltmada önceliğin korunduğu yalnızca Ek-18 1.2'de yazılıdır (bkz. 04-surekli-islem.md Açık sorular, madde 20); emir bilgileri (MPF-AFK-Hesap No) "değiştirilemez" iken "değiştiğinde öncelik kaybolur" denmesi tutarsızdır. Karar: Motor, emir bilgisi alanlarının (MPF-AFK-Hesap No) değiştirilmesini reddeder; "değiştiğinde öncelik kaybolur" ifadesi eski bir kalıntı sayılır, kodlanmaz.
- [DOĞRULA] Madde 110: Ek-18 1.3 matrisinin s. 206'daki "2" numaralı satırları (İşlem Terminali 2, FixAPI 2, OUCH 2 vb.) aynı kurumdaki başka bir kullanıcıyı temsil eder; matris tabloda sütun başlıklarında "2" kullanıcılar yoktur. Yetki özeti matristen çıkarılmıştır;
- [DOĞRULA] Madde 115: Maksimum emir değeri grupları (6 grup) tablodan alınmıştır; hangi payın hangi grupta olduğu Prosedürde yoktur (Borsa internet sitesindeki dosyalarda). Ek-18 1.1'de limit emir üst sınırı "10 M" yazılıdır; bu Tablo-14 1. Grup ile aynıdır, diğer gruplar (7,5 / 5 / 2,5 / 1 / 0,5 milyon TL) Ek-18 1.1 tablosunda yansıtılmamıştır (Ek-18 1.1 parametriktir).
- [DOĞRULA] Madde 116: "Ocak ve Temmuz aylarında yürürlüğe girmek üzere" güncelleme tarihleri gelecek tarihleri gerektirir; motorun tarihsel veriyi (ör. 2018) oynatırken o günkü maksimum emir değeri sınırlarını nereden alacağı belirtilmemiştir (01.06.2017 tarihli yeni uygulama öncesinde tüm paylarda 3 milyon TL uygulanıyordu; 5.6.4, s. 92).
- [DOĞRULA] Madde 126: İKG geçerlilik süresi Prosedürde "halka arz süresinin sonuna kadar" geçerli olarak tanımlanır; FIX GTC (1) ile eşlemesi belgelerde açıkça yazılı değildir.
- [DOĞRULANDI – kullanıcı kararı (öneri onaylandı)] Madde 130 ve Madde 137: Prosedür 5.6.5 "emrin fiyatı belirlenen zaman içinde marj dışına çıktığında ... ilgili emir iptal edilir" der; FIX 6.5.6 marj dışına çıkan emrin duraklatıldığını ve özgün zaman önceliğiyle yeniden etkinleştirildiğini söyler (bkz. 04-surekli-islem.md Açık sorular, madde 47). Karar: İki durum ayrıdır. Tarihli/süreli emirlerde, gün başında baz fiyat ve marj değiştiğinde fiyatı marj dışına çıkan veya fiyat adımına uymayan emir iptal edilir (5.6.5). Gün içinde fiyat limitlerinin kayması nedeniyle limit dışında kalan emir duraklatılır ve özgün zaman önceliğiyle yeniden etkinleştirilir (FIX 6.5.6).
- [DOĞRULANDI – kullanıcı kararı (öneri onaylandı)] Madde 133–135: 5.6.5'in iki paragrafı çelişir görünür: birinci paragraf "Sistem tarafından askıya alınan ve daha sonra TW kullanılarak yeniden aktif hâle getirilen emirler için yeni emir numarası verilmez" der; ikinci paragraf "TW kanalıyla askıya alınan ve daha sonra yeniden aktif hâle getirilen emirler yeni bir emir numarası alır ve emir defterinde yeniden sıralanırlar" der. "Sistem tarafından askıya alınan" ile "TW ile askıya alınan" ayrımı kaynakta yapılmış olabilir; bu ayrım yorumlanmadı. OUCH Order Canceled notu (4.2.4): bağlantı kaybı nedeniyle askıya alınan emirler yeniden etkinleştirilemez, ancak iptal edilebilir. Karar: Motor açısından askıya alma = iptal + yeni emir girişi (yeni emir numarası, öncelik kaybı); iki paragraf arasındaki çelişki kodlamayı etkilemez. Askıya alma ve yeniden etkinleştirme temsilci iş istasyonu (TW) özelliğidir, motor kapsamı dışında istemci tarafıdır.
- [DOĞRULA] Madde 136: OUCH belgesi `Time In Force` = 3 için "Immediate or Cancel (FaK)" yazar; FaK = Fill and Kill (FIX'te IOC). Prosedürdeki "Kalanı İptal Et (KİE)" ile eşlemesi belgelerde doğrudan yazılı değildir.
- [KISMEN DOĞRULANDI – gün içi veri Mart 2025; betik `../veri/araclar/gunici_emir_kural_kontrol.py`, tablo `sistem_sebep.csv`] Sebeplerin veride gözlenen anlamı: 13 = kısmi görünme koşullu emrin görünen kısmının işlem sonrası yenilenmesi (satır işlem taşır, `islem_numarasi` dolu); 8 = piyasadan limite emrin kalanının limit emre dönüşmesi (fiyat türü 1 ve fiyat = işlem fiyatı olur; madde 23 ile tutarlı); 9 ve 34 = müzayede eşleştirmesinden sonra karşılanmayan emirlerin sistemce iptali (KİE, piyasa emri vb.); 19 = gün sonunda (18:19:00, `P_GUNSONU`) süre dolumu; 4 = pasifleştirme (`emir_durumu` 4). 116 ve 117 kodları DataStore referans tablosunda (3.1.4) ve OUCH listesinde yoktur; 117 EBDKS durdurmasında (`P_GECICI_DURDUR_EBDK`), 116 sürekli işlemde iptal olarak görülür, anlamları yazılı değildir. Madde 138: ChangeReason değerlerinin anlamı OUCH belgesinde yalnızca ad olarak verilir (ör. 13 = Refreshed by System, 39 = Undisclosed Quantity Order Converted); kısmi görünme koşullu emirdeki yenileme ve dönüşümle eşlemesi örnek veriyle doğrulanmadı (ITCH örnek verisinde yalnızca `A`, `D`, `E` vb. mesajlar vardır).
- [DOĞRULA] Madde 140–141: Ek-19'daki "P_ESLESTIRMETEKFIYAT" adı Ek-11'deki "P_ESLESTIRME_TEKFIYAT" başlığıyla birebir aynı değildir (yazım farkı kaynaktadır); Ek-19 matrisinde P_ESLESTIRME_TEKFIYAT yerine P_ESLESTIRMETEKFIYAT, Ek-11'de P_ESLESTIRME_FBS_* ve P_SUREKLI_ISLEM_HFL satırlarının açıklaması ayrı verilmiştir (ayrıntı `../ekler/ek11.md`). Seans durumu adlarının ITCH `State Name` ile eşlemesi için bkz. `07-itch.md`.
- [DOĞRULA] Madde 5.4.10 (Açığa Satış Emirleri, s. 90) bu dosyanın madde listesinde (5.4.1–5.4.9) yer almadığı için kural olarak yazılmadı: "SPK ve Borsa düzenlemeleri uyarınca yapılan açığa satış işlemlerine ilişkin emirlerdir; bu emirlerde SPK ve Borsa düzenlemeleri ile belirlenen fiyat sınırlamalarına uyulur." Açığa satışa izin verilen seans bölümleri Ek-19 O sütunundadır.
- [DOĞRULA] Ek-18 5.4 Örnek 2 (s. 218–219): metin "20 lotluk (Gizli miktar = 100 lot) Kısmi Görünme Koşullu satış emri" der; alış tarafındaki toplam 60 lotla eşleşme sonrası kalan tablo görünen 20 + gizli 20 (toplam 40) gösterir. Toplam 120 lot (20 + 100) olsaydı kalan 60 (20 görünen + 40 gizli) olurdu; tablo ile metin tutarlı değildir (metindeki "100" muhtemelen toplam miktardır). Test örneğinde tablo esas alındı ve not düşüldü.
- [DOĞRULA] Ek-18 6.3 Örnek 1 (s. 221–222): işlem öncesi Orta Nokta emir defterinde 200.000@MPM satış tarafındadır; işlem sonrası tabloda kalan 100.000@MPM "ALIŞ" sütununda gösterilir. Kaynaktaki yerleşim hatası olabilir; kalan emir satış tarafı kabul edildi (taraf değişimi için kaynakta açıklama yok).
- [DOĞRULA] Ek-18 tabloları: s. 209'daki "Alış Tafı" kaynaktaki yazım hatasıdır (Alış Tarafı); s. 203 tablosundaki AOF (TAR) satırında fazladan boş hücreler kaynakta vardır, buraya aktarılmamıştır. Ek-19 matrisi Ek-11 açıklamalarıyla çapraz doğrulanmıştır (`../ekler/ek19.md` başlık notu).

- [BİLGİ – örnek veri, 08.10.2018; betik `../veri/araclar/ayni_id_yeniden_ekleme_kontrol.py`] Madde 49 (kısmi görünme koşullu emirde açığa çıkan kısım aynı emir numarasını alır) sınanamadı: iki bölümde de görünen miktarı `E` ile tükenmiş bir emrin ardından aynı Order ID ile yeni `A` gelen hiçbir durum yok (aynı Order ID'li tüm yeniden eklemeler `D` sonrasıdır: 449.063 çift aynı fiyat/≥1 sn, 167.708 farklı fiyat/aynı nanosaniye, 16.326 aynı fiyat/aynı nanosaniye, 2.014 farklı fiyat/≥1 sn; ≥1 sn aynı fiyat çiftleri müzayede geçişlerinde silinip yeniden yazılan emirlerdir). Bu günün verisinde yenilenme deseni yok ya da farklı mesajlarla yayımlanıyor; madde 49–53 veriden doğrulanamadı.

- [BİLGİ – gün içi veri Mart 2025; betik `../veri/araclar/gunici_ek19_kontrol.py`; ayrıntı `../veri/gunici-veri-dogrulama.md` bölüm 7] Madde 139–141 (Ek-19): 230.819.084 yeni emir (sebep 6) bölüm × tip olarak sayıldı; Ek-19'da 0 olan hücrelerde yeni emir sayısı 0'dır.
  - Açılış bölümlerinde piyasa ve piyasadan limite emir yalnız Yıldız ve Ana pazar sıralarında görülür; `TP2_PY` bölümlerinde (Alt Pazar, YİP, PÖİP) yoktur. Bu, 03-tek-fiyat.md madde 24'teki kullanıcı kararıyla uyumludur.
  - Açılış bölümlerinde açığa satış yoktur.
  - Orta Nokta emri yalnız sürekli işlemde (3.226 yeni), dengeleyici emir yalnız tek fiyat bölümlerinde görülür.
  - Piyasadan limite emir `DAY` ve `IMMEDIATE` ile, dengeleyici emir yalnız `IMMEDIATE` ile girilmiştir.

## Test örnekleri
Prosedür 5.4–5.6'da sayısal örnek yoktur (yalnızca Tablo-14 sınırları madde 115'te). Aşağıdakiler Ek-18'deki örneklerdir (birebir; `../ekler/ek18.md`). Sürekli işlem örnekleri `04-surekli-islem.md`, dengeleyici emir örneği `03-tek-fiyat.md` Test örneklerinde de atıf verilmiştir.

**Ek-18 2.2.1 Tek fiyat yönteminde piyasa emirleri (s. 207)** — açılış seansı; alış tarafında 10 lot piyasa emri (MKT):

| Alış Toplam Miktar | Alış Emir Miktarı | Fiyat | Satış Emir Miktarı | Satış Toplam Miktar | İşlem Miktar | Kalan Miktar | Taraf |
|---|---|---|---|---|---|---|---|
| 10 | 10 | MKT |  | 105 | 10 | 95 | Satış |
| 10 |  | 20,50 | 10 | 105 | 10 | 95 | Satış |
| 10 |  | 20,40 | 10 | 95 | 10 | 85 | Satış |
| 40 | 30 | 20,30 | 15 | 85 | 40 | 45 | Satış |
| 55 | 15 | 20,20 | 15 | 70 | 55 | 15 | Satış |
| 60 | 5 | 20,10 | 5 | 55 | 55 | 5 | Alış |
| 80 | 20 | 20,00 | 20 | 50 | 50 | 30 | Alış |
| 95 | 15 | 19,90 | 30 | 30 | 30 | 65 | Alış |
| 105 | 10 | 19,80 |  |  |  | 105 | Alış |
| 110 | 5 | 19,70 |  |  |  | 110 | Alış |

Beklenen sonuç: alış tarafındaki piyasa (MKT) emirleri fiyat önceliğine sahip olarak diğer fiyat kademelerindeki limit fiyatlı emirlerden önce, eşleştirme fiyatı olan 20,10'dan işleme dönüşür.

**Ek-18 2.2.2 Sürekli işlem yönteminde piyasa emirleri (s. 208)** — emir defteri (piyasa emri girilmeden önce):

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 100 | 10,50 | 11,00 | 80 |
| 90 | 10,45 | 11,05 | 90 |
| 80 | 10,40 | 11,10 | 100 |

150 lot alış piyasa emri girilirse: 80 adet 11,00 TL'den, kalan 70 adet 11,05 TL'den işleme dönüşür. Sonrasında emir defteri:

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 100 | 10,50 | 11,05 | 20 |
| 90 | 10,45 | 11,10 | 100 |
| 80 | 10,40 |  |  |

**Ek-18 3.2.1 Tek fiyat yönteminde piyasadan limite emirleri (s. 209–210)** — açılış seansı; alış tarafında 10 lot piyasadan limite (MTL) ve 25 lot piyasa (MKT) emri:

| Alış Toplam Miktar | Alış Emir Miktarı | Fiyat | Satış Emir Miktarı | Satış Toplam Miktar | İşlem Miktar | Kalan Miktar | Taraf |
|---|---|---|---|---|---|---|---|
| 10 | 10 | MTL |  | 105 | 10 | 95 | Satış |
| 35 | 25 | MKT |  | 105 | 35 | 70 | Satış |
| 35 |  | 20,50 | 10 | 105 | 35 | 70 | Satış |
| 35 |  | 20,40 | 10 | 95 | 35 | 60 | Satış |
| 65 | 30 | 20,30 | 15 | 85 | 65 | 20 | Satış |
| 80 | 15 | 20,20 | 15 | 70 | 70 | 10 | Alış |
| 85 | 5 | 20,10 | 5 | 55 | 55 | 30 | Alış |
| 105 | 20 | 20,00 | 20 | 50 | 50 | 55 | Alış |
| 120 | 15 | 19,90 | 30 | 30 | 30 | 90 | Alış |
| 130 | 10 | 19,80 |  |  |  | 130 | Alış |
| 135 | 5 | 19,70 |  |  |  | 135 | Alış |

Beklenen sonuç: alış tarafındaki piyasadan limite (MTL) emri fiyat önceliğine sahip olarak diğer fiyat kademelerindeki limit fiyatlı emirlerden ve (zaman önceliğine sahip olduğu) piyasa (MKT) emirlerinden önce, eşleştirme fiyatı olan 20,20'den işleme dönüşür.

**Ek-18 3.2.2 Sürekli işlem yönteminde piyasadan limite emirler (s. 210)** — başlangıç emir defteri 2.2.2'dekiyle aynı. 150 lot piyasadan limite alış emri girilirse: 80 adet 11,00 TL'den işleme dönüşür; kalan 70 adet işlemin gerçekleştiği fiyat olan 11,00 TL'den alış tarafında pasife yazılır. Sonrasında emir defteri:

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 70 | 11,00 | 11,05 | 90 |
| 100 | 10,50 | 11,10 | 100 |
| 90 | 10,45 |  |  |
| 80 | 10,40 |  |  |

**Ek-18 4.1 Dengeleyici emir (s. 211)** — açılış seansı; alış tarafında 50 lot dengeleyici (IMB) emri:

| Alış Toplam Miktar | Alış Emir Miktarı | Fiyat | Satış Emir Miktarı | Satış Toplam Miktar | İşlem Miktar | Kalan Miktar | Taraf |
|---|---|---|---|---|---|---|---|
| 20 | 20 | 20,50 | 10 | 105 | 20 | 85 | Satış |
| 20 | --- | 20,40 | 10 | 95 | 20 | 75 | Satış |
| 50 | 30 | 20,30 | 15 | 85 | 50 | 35 | Satış |
| 65 | 15 | 20,20 | 15 | 70 | 65 | 5 | Satış |
| 70 | 5 | 20,10 | 5 | 55 | 55 | 15 | Alış |
| 90 | 20 | 20,00 | 20 | 50 | 50 | 40 | Alış |
| 105 | 15 | 19,90 | 30 | 30 | 30 | 75 | Alış |
| 115 | 10 | 19,80 |  |  |  | 115 | Alış |
| 120 | 5 | 19,70 |  |  |  | 120 | Alış |
|  | 50 | IMB |  |  |  |  |  |

Beklenen sonuç: eşleştirme fiyat seviyesinde eşleşmeden kalan 5 lotluk satış emri 50 lotluk dengeleyici (IMB) emirle eşleşir; eşleşmeden kalan 45 lotluk dengeleyici emir iptal edilir.

**Ek-18 5.4 Örnek 1 — Pasifte bekleyen kısmi görünme koşullu emir (s. 218)** — alış tarafı ilk sıradaki emir 100 lotluk kısmi görünme koşullu emirdir, 20 lotu görünür (gizli 80):

| Alış Gizli Miktar | Alış Miktar | Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|---|
| 80 | 20 | 10,50 | 11,00 | 10 |
|  | 10 | 10,50 | 11,10 | 10 |
|  | 10 | 10,50 |  |  |

10,50 TL'den 30 lot satış emri gelirse: alış tarafında 10,50'de bekleyen kısmi görünümlü emrin görünen 20 lotu ve diğer 10 lotluk emir işleme dönüşür; gizli 80 lotun 20 lotu yeni bir emir gibi açığa çıkarak fiyat-zaman önceliğine göre 10,50'den emir defterinde beklemeye başlar. Yeni görünüm:

| Alış Gizli Miktar | Alış Miktar | Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|---|
|  | 10 | 10,50 | 11,00 | 10 |
| 60 | 20 | 10,50 | 11,10 | 10 |

**Ek-18 5.4 Örnek 2 — Aktif olarak girilen kısmi görünme koşullu emir (s. 218–219)** — başlangıç:

| Alış Gizli Miktar | Alış Miktar | Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|---|
|  | 20 | 10,50 | 11,00 | 10 |
|  | 20 | 10,50 | 11,10 | 10 |
|  | 20 | 10,50 |  |  |
|  | 10 | 10,40 |  |  |

10,50 TL limit fiyatlı, 20 lotluk (kaynakta "Gizli miktar = 100 lot") kısmi görünme koşullu satış emri, alış tarafında 10,50'de bekleyen toplam 60 lotluk emirlerle eşleşerek işleme dönüşür. Son görünüm (kaynakta olduğu gibi; bkz. Açık sorular, "Ek-18 5.4 Örnek 2" maddesi):

| Alış Gizli Miktar | Alış Miktar | Fiyat | Satış Fiyat | Satış Miktar | Satış Gizli Miktar |
|---|---|---|---|---|---|
|  | 10 | 10,40 | 10,50 | 20 | 20 |
|  |  |  | 11,00 | 10 |  |
|  |  |  | 11,10 | 10 |  |

**Ek-18 6.3 Orta Nokta emirlerinin eşleşmesi (s. 221–222)**

Örnek 1 — emir defteri alış 10@10,00, satış 10@12,00; Orta Nokta emir defteri satış 200.000@MPM. 100.000@12,00 bir MPL (alış) emri gelirse: (10+12)/2 = 11,00 fiyat seviyesinden 100.000 lotluk Orta Nokta işlemi gerçekleşir. İşlem sonrası Orta Nokta emir defteri: satış tarafında 100.000@MPM kalır (kaynakta bu kalan emir "ALIŞ" sütununda gösterilir; bkz. Açık sorular, "Ek-18 6.3 Örnek 1" maddesi).

Örnek 2 — emir defteri alış 10@14,00, satış 10@16,00; Orta Nokta emir defteri alış 100.000@MPL/14, satış 100.000@MPM. Potansiyel Orta Nokta fiyatı (14+16)/2 = 15,00; alışta bekleyen MPL limit fiyatından (14,00) daha kötü olduğundan eşleşme gerçekleşmez. Piyasa şartları değişip emir defteri alış 10@12,00, satış 10@16,00 olduğunda: potansiyel Orta Nokta fiyatı (12+16)/2 = 14,00; MPL limit fiyatına eşittir; 14,00 fiyat seviyesinden 100.000 lotluk Orta Nokta işlemi gerçekleşir.

**Ek-18 7.2 AOF emirlerinin eşleşmesi (s. 224–225)**

Örnek 1 — GARAN.E ve GARAN.AOF sıraları:

| İşlem Sırası | Emir | İşlem |
|---|---|---|
| GARAN.E | Alış 40@8,50 | - |
| GARAN.E | Satış 20@8,50 | GARAN.E 20@8,50 |
| GARAN.E | Alış 40@8,60 | - |
| GARAN.E | Satış 10@8,60 | GARAN.E 10@8,60 |
| GARAN.AOF | Alış 150.000@0,00 (Kullanıcı 1) | - |
| GARAN.AOF | Satış 100.000@0,00 (Kullanıcı 2) | GARAN.AOF 100.000@0.00 |

Gün sonunda GARAN.E'de oluşan AOF = (20 × 8,50 + 10 × 8,60)/(20 + 10) = 8,533. Kullanıcı 1: GARAN.E 100.000@8,533 alır. Kullanıcı 2: GARAN.E 100.000@8,533 satar. AOF işlemi GARAN.E işlem sırasında gerçekleşen miktar ve hacme dâhil edilmez, ayrıca duyurulur.

Örnek 2 — ISCTR.E (fiyat adımı 0,50) ve ISCTR.AOF (fiyat adımı 0,10). Kullanıcı-1 AOF +1 adım ile alış (en iyi alıcı), Kullanıcı-2 AOF −1 adım ile alış (ikinci en iyi alıcı), Kullanıcı-3 piyasa fiyatlı satış girmiştir:

| İşlem Sırası | Emir | İşlem |
|---|---|---|
| ISCTR.AOF | Alış 100 @ 0,10 (Kullanıcı-1) | - |
| ISCTR.AOF | Alış 100 @ -0,10 (Kullanıcı-2) | - |
| ISCTR.AOF | Satış 150@ Mkt (Kullanıcı-3) | 100@0,10 - 50@-0,10 |

Gün sonunda ISCTR.E'de oluşan AOF = 59,78. Kullanıcı-1: 59,88 fiyattan 100 lot ISCTR.E alır. Kullanıcı-2: 59,68 fiyattan 50 lot ISCTR.E alır. Kullanıcı-3: 59,88 fiyattan 100 lot ve 59,68 fiyattan 50 lot satar. Not (kaynakta): İşlem fiyatları payın normal işlem sırasında (.E) oluşan AOF üzerine AOF işlem sırasında (.AOF) geçerli olan fiyat adımlarının uygulanması ile oluşmaktadır.

**Ek-18 AOF tavan/taban örneği (s. 224)** — GARAN.E sırasında baz fiyat 10,00 TL, fiyat limitleri 8,00–12,00 TL, gün sonu AOF 12,00 TL iken .AOF sırasında +0,02 fiyatla gerçekleşen işlemin fiyatı 12,02 TL olur; bu fiyat GARAN.E maksimum fiyatını etkilemez.

**OUCH Replace miktar örneği (OUCH 4.1.2.1; Ek-18 değil)** — Örnek 1: 1000 miktarlı emir girilir (Order Accepted, Quantity = 1000); 200 gerçekleşir (Traded Quantity = 200, defterde 800); açık miktarı 750'ye düşürmek için Quantity = 950 gönderilir; Order Replaced Quantity = 750 döner. Örnek 2: 1000 miktarlı emir; açık miktarı 500'e düşürmek için Quantity = 500 gönderilir; aynı anda 600 gerçekleşir (Traded Quantity = 600); Order Replaced Quantity = 0 ve Order State = Not on book (2) döner. [OUCH 4.1.2.1, s. 12]
