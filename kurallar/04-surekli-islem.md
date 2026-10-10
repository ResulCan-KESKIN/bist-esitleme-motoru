# Sürekli İşlem ve Öncelik Kuralları
Kaynak: Pay Piyasası Prosedürü 5.2.1 Sürekli İşlem Yöntemi ve Tablo-9 (s. 55), 5.6.1 Öncelik Kuralları (s. 91). Öncelik kaybı/korunması için aynı konuyu düzenleyen hükümler bu dosyada birleştirilmiştir: 5.5.1 (s. 90), 5.6.5 (s. 94), kotasyon öncelikleri 5.3.1 (s. 67, 68, 74), kısmi görünme koşullu emir 5.4.5 ç (s. 89). İlgili Ek: Ek-18 1.2 Öncelik Kuralları (s. 204) ve sürekli işlem örnekleri 2.2.2 (s. 208) ile 3.2.2 (s. 210) (`../ekler/ek18.md`; tablo sütun kayması riski yok, Ek-18 tabloları koordinat tabanlı aktarılmıştır). Sayfa numaraları PDF sayfa numarasıdır.
Ek kaynaklar (Prosedür dışı teknik dokümanlar; `../kaynaklar/`): Emrimle Eşleşmesin (SMP) Teknik Çalışma Esasları v2 (Şubat 2025), Genium INET FIX Protocol Specification 1.0.65 (6.5.3.1, 6.5.6, 6.6.3), BISTECH OUCH Protocol Specification (4.1.2.2, 17.09.2026). Bu kaynaklardan gelen kuralların sonunda kaynak adı yazılıdır.
İlgili kod: eşleştirme motoru (sürekli işlem bölümü; emir defteri sıralaması ve öncelik), emir defteri yeniden kurucu (ITCH sıralama doğrulaması)

## Kurallar

### A. Sürekli işlem yöntemi (5.2.1)
1. Sürekli işlem yöntemi, bir sermaye piyasası aracı için Sisteme iletilen emirlerin Borsa tarafından belirlenen işlem süreleri boyunca sürekli bir şekilde, öncelik ve işlem kurallarına uygun olarak farklı fiyat seviyelerinden eşleştirilmesi yöntemidir. [5.2.1, s. 55]
2. Sürekli işlem yöntemi "Çok Fiyat Yöntemi" olarak da adlandırılır. [5.2.1, s. 55]
3. Bu yöntemin uygulamasında ilgili enstrümanda üyelerin alış ve satış emirlerinin ve gerçekleşen işlemlerin ilgililerin izleyebileceği biçimde gösterilmesi esastır. [5.2.1, s. 55]
4. Alım satım emirleri belirlenmiş kurallar çerçevesinde Sisteme iletilir. [5.2.1 a, s. 55]
5. Emir girişlerinde miktar veya tutar olarak Yönetim Kurulunca getirilen azami sınırlara uyulur. [5.2.1 b, s. 55]
6. Emirler, Sisteme iletildikleri andan itibaren öncelik kurallarına göre işlem görebilir. [5.2.1 c, s. 55]
7. Üyeler, daha önce başka üyeler tarafından Sisteme girilmiş olan emirler üzerinde tamamen veya kısmen işlem gerçekleştirebilir. [5.2.1 ç, s. 55]
8. Bir sermaye piyasası aracının ana işlem sırasına bağlı ve geçici olarak, belirli bir süre için açılan işlem sıralarında tek fiyat yöntemi uygulanmaz. [5.2.1, s. 55]
9. Resmî müzayede işlemlerinde (ME, MR, MF, MV, MF1, MF2, MG, MC, MS, MS1) işlem yöntemi sürekli işlemdir. (tablodan) [Tablo-9, s. 55]
10. Birincil piyasada yeni pay alma hakkı kullanımından kalan payların satışında işlem yöntemi sürekli işlemdir. (tablodan) [Tablo-9, s. 55]
11. Temerrüt işlemlerinde işlem yöntemi sürekli işlemdir. (tablodan) [Tablo-9, s. 55]
12. Yeni Pay Alma Hakkı işlemlerinde işlem yöntemi sürekli işlemdir. (tablodan) [Tablo-9, s. 55]
13. Toptan Alış Satış işlemleri özel işlem bildirimi yoluyla Pay Piyasası uzmanları tarafından gerçekleştirilir. (tablodan) [Tablo-9, s. 55]

### B. Öncelik kuralları (5.6.1)
14. Sisteme kaydedilen emirler karşılanırken, önceliklerin belirlenmesinde aşağıdaki kurallar sırasıyla uygulanır. [5.6.1, s. 91]
15. Fiyat önceliği: Daha düşük fiyatlı satım emirleri daha yüksek fiyatlı satım emirlerinden; daha yüksek fiyatlı alım emirleri daha düşük fiyatlı alım emirlerinden önce karşılanır. [5.6.1, s. 91]
16. Zaman önceliği: Fiyat eşitliği hâlinde, Sisteme zaman açısından daha önce kaydedilen emirler öncelikle karşılanır. [5.6.1, s. 91]
17. Öncelik kuralları aksi belirtilmedikçe limit fiyatlı emirlere ilişkindir; bu kurallar BISTECH sistemi üzerinde parametriktir ve önceden duyurularak Borsa tarafından değiştirilebilir. [Ek-18 1, s. 203]
18. Pay Piyasasında geçerli olan fiyat ve zaman önceliği kuralları kotasyon emirleri için de geçerlidir. [5.3.1, s. 67]
19. Girilen bir normal emir, öncelik kurallarına uygun olarak bir kotasyonla veya kotasyon haricindeki başka bir emirle eşleşerek işlem görebilir. [5.3.1, s. 67]

### C. Emir üzerinde değişiklikte önceliğin korunması veya kaybı
20. Emir önceliği miktar azaltıldığında korunur. [Ek-18 1.2, s. 204]
21. Emir önceliği miktar artırıldığında kaybolur; emir Sisteme yeni girilmiş bir emir olarak değerlendirilir ve zaman önceliğini kaybeder. [Ek-18 1.2, s. 204; 5.5.1, s. 90]
22. Emir önceliği fiyat değiştirildiğinde (hem iyileştirmede hem kötüleştirmede) kaybolur; emir Sisteme yeni girilmiş bir emir olarak değerlendirilir ve zaman önceliğini kaybeder. Fiyat iyileştirildiğinde emir ilgili kademede en sona gider. [Ek-18 1.2, s. 204; 5.5.1, s. 90]
23. Emir iyileştirilmesi alış emri için fiyatı yükseltmek, satış emri için fiyatı düşürmek; emir kötüleştirilmesi alış emri için fiyatı düşürmek, satış emri için fiyatı yükseltmek anlamındadır. [5.5.1, s. 90]
24. Emir önceliği emir bilgileri (MPF-AFK-Hesap No) değiştiğinde kaybolur; bu alanların değiştirilmesine izin verilmez. [Ek-18 1.2, s. 204]
25. Emir önceliği süre uzatıldığında kaybolur, süre kısaltıldığında korunur. [Ek-18 1.2, s. 204; 5.6.5, s. 94]
26. Kotasyon emri değiştirildiğinde eskisi iptal edilip yenisi girilir; bu nedenle öncelik kaybolur. [Ek-18 1.2, s. 204]
27. Kotasyon emirlerinin güncellenmesinde yapılan her değişiklikte (miktar azaltılsa dahi) öncelik kaybolur; çünkü her kotasyon değişikliği iptal ve yeni emir girişi olarak addedilir. [5.3.1, s. 68]
28. Alış-satış kotasyonlarının fiyatı ayrı ayrı ya da birlikte piyasa yapıcı üye tarafından yükseltilebilir ya da düşürülebilir; fiyatı değişen kotasyon önceliğini yitirir ve girilen yeni kotasyon Sistem tarafından öncelik kurallarına göre emir defterine yeniden yerleştirilir. [5.3.1, s. 74]
29. Alış-satış kotasyonlarının miktarları ayrı ayrı ya da birlikte piyasa yapıcı üye tarafından yükseltilebilir ya da düşürülebilir; miktarı değiştirilen kotasyonlar önceliğini yitirir. [5.3.1, s. 74]
30. Kısmen görünen (kısmi görünme koşullu) emirde, görülmesi istenen kısmın tamamı işlem gördüğünde gizli bölümden belirlenen miktar kadar kısım açığa çıkar; açığa çıkan kısım, açığa çıktığı anda girilmiş yeni bir emir gibi fiyat ve zaman önceliğine göre emir defterinde yerini alır. [5.4.5 ç, s. 89]
31. Seansın sürekli işlem bölümünde günlük ya da tarihli gönderilen bir emir KİE'ye dönüştürülemez; günlük ya da tarihli gönderilen bir Orta Nokta-Limit emir de KİE'ye dönüştürülemez. [Ek-18 1.2, s. 204]
32. Açılış/kapanış ya da tek fiyat bölümünde KİE olarak girilen bir emir tarihli ya da günlük emre dönüştürülebilir ve dönüştürüldüğünde önceliğini kaybeder (emir numarası değişmez). [Ek-18 1.2, s. 204]
33. Açılış/kapanış ya da tek fiyat bölümünde günlük veya tarihli girilmiş bir emir KİE'ye dönüştürülebilir ve dönüştürüldüğünde önceliğini kaybeder (emir numarası değişir). [Ek-18 1.2, s. 204]

### D. Emrimle Eşleşmesin (Self-Match Prevention, SMP) — teknik doküman
34. Emrimle Eşleşmesin özelliği SMP ID ile işaretlenmiş emirlerin aynı işareti taşıyan diğer emirlerle eşleşmesini önlemek üzere geliştirilmiştir; algoritmik emir iletim sistemleri için planlanmıştır ve üyenin başvurusuyla tercihe bağlı olarak kullanılır. [SMP, s. 3]
35. Özellik FIX ve OUCH kanallarında emir iletiminde `SMP Seviyesi`, `SMP Yöntemi` ve `SMP ID` alanlarının doldurulmasıyla geçerli olur; emir girildikten sonra bu alanlar değiştirilemez. [SMP, s. 3]
36. `SMP Seviyesi`: 1 = üye içinde, 2 = üyeler arasında. Özelliğin tetiklenmesi için potansiyel eşleşmenin her iki tarafındaki emirde SMP Seviyesi aynı değerde (1 veya 2) olmalıdır. Seviye 1'de yalnızca aynı üyenin emirleri arasında, seviye 2'de üyenin kendisi dâhil tüm üyeler arasında geçerlidir. [SMP, s. 3; OUCH Tablo 2: 0 = boş, 1 = üye içi, 2 = üyeler arası]
37. `SMP Yöntemi`: 1 = agresif emri iptal et, 2 = pasif emri iptal et, 3 = her iki emri iptal et. Agresif emir daha sonra girilen emirdir, pasif emir defterde bekleyen emirdir. [SMP, s. 3–4; OUCH Tablo 2: 0 = boş]
38. Farklı SMP Yöntemi belirlenmiş emirler potansiyel bir eşleşmeye konu olursa agresif emirde belirtilen SMP Yöntemi geçerli olur. [SMP, s. 4]
39. `SMP ID` üç haneli, büyük-küçük harfe duyarlı, alfanümerik bir değerdir; özelliğin tetiklenmesi için potansiyel eşleşmenin her iki tarafındaki emirde aynı değerde olmalıdır. Seviye 1'de SMP ID emri ileten üye, seviye 2'de Borsa tarafından belirlenir. [SMP, s. 4]
40. Özellik yalnızca sürekli işlem yönteminin uygulandığı seans bölümlerinde geçerlidir. Tek fiyatlı seans bölümlerinde SMP alanları dolu olarak iletilen emir kabul edilir ancak özellik tetiklenmez; emir sürekli işlem bölümüne taşınırsa özellik tetiklenebilir duruma geçer. [SMP, s. 5]
41. Özellik yalnızca Limit Emirler ile Gün ve Kalanı İptal Et geçerlilik sürelerinde kullanılabilir. Piyasa, Piyasadan Limite, Özel İşlem Bildirimi, Vadeler Arası Strateji, Şarta Bağlı, Kısmi Görünme Koşullu, Dengeleyici ve Orta Nokta emirlerinde kullanılamaz. [SMP, s. 5]
42. SMP nedeniyle iptal edilen emirlerin Emir Değişiklik Sebebi (ChangeReason) değeri 46'dır (OrderDeletedDueToSMP). [SMP, s. 5; OUCH Tablo 10: 46 = Order deleted due to SMP]
43. Özellik 3.12 servis güncellemesiyle teknik olarak devreye alınır; kullanıma açılış tarihi sonradan duyurulacaktır. [SMP, s. 5]

### E. Emir tipleri ve sürekli işlemde bekleme/öncelik — teknik dokümanlar
44. Sürekli işlemde piyasa emri emir defterinde saklanamaz; Kalanı İptal Et (IOC) veya Hepsi ya da Hiçbiri (FoK) geçerlilik süresinde olmalıdır. Piyasa emirleri eşleşmeyen durumlardaki seanslarda deftere girebilir; seans eşleşen duruma geçince işleme dönüşür ve/veya iptal edilir. [FIX 6.6.3.1]
45. Piyasadan Limite (Market-to-Limit) emir yalnızca en iyi fiyat seviyesinde eşleşir (defteri taramaz); karşı tarafta emir yoksa hemen iptal edilir; kalan miktar işlemin gerçekleştiği fiyattan limit emir olarak deftere yazılır ve sonraki raporlarda emir tipi Limit olur. [FIX 6.6.3.2]
46. Emrin fiyatı değiştirildiğinde veya miktarı artırıldığında emir piyasadaki önceliğini kaybeder; fiyat 0'a değiştirilemez. Replace'te değişmesi istenmeyen alanlar boş bırakılmalıdır, aksi hâlde öncelik kaybedilebilir veya replace reddedilebilir; sistem öncelik kaybettirecek replace'leri reddedecek şekilde yapılandırılabilir. [FIX 6.5.3.1; OUCH 4.1.2.2]
47. Etkin fiyat limitleri dışına çıkan emir sistem tarafından duraklatılır (paused): duraklatılmış emir eşleşmeye girmez, denge fiyatı hesabına katılmaz ve fiyat resminde yer almaz; koşullar uygun hâle geldiğinde emir özgün zaman önceliğiyle yeniden etkinleştirilir. Fiyat limiti dışında kalan emir: üst limitin üzerinde fiyatlı satış veya alt limitin altında fiyatlı alış emridir. [FIX 6.5.6, 6.5.6.1]
48. Emir Order ID'si (OrderID) Borsa tarafından atanır, emir değiştirilse de sabit kalır ve yalnızca emir defteri ve taraf başına benzersizdir; emir tanımlamasında Order ID, emir defteri ve taraf birlikte kullanılmalıdır. [FIX 6.6.1.2; ITCH `A` Tablo 7]

## Açık sorular
- [DOĞRULA] Madde 1, 14–16: Sürekli işlemde bir eşleşmenin hangi fiyattan gerçekleştiği (pasif/bekleyen emrin fiyatı mı) 5.2.1 ve 5.6.1'de yazılı değildir. Ek-18 örnekleri (s. 208, 210) işlemlerin karşı taraftaki bekleyen emirlerin fiyatından gerçekleştiğini gösterir (örnek: 80 adet 11,00 TL'den, 70 adet 11,05 TL'den). Kural olarak yazılmadı; örnekten çıkarım (bkz. Test örnekleri). ITCH `E` mesajı fiyat taşımaz (08.10.2018 verisinde `C` mesajı yok), bu nedenle işlem fiyatı emir defterindeki bekleyen emrin fiyatıyla izlenir.
- [DOĞRULA] Madde 16: "Sisteme zaman açısından daha önce kaydedilen" ifadesinde zaman ölçüsünün çözünürlüğü ve aynı zamana düşen iki emrin sıralaması yazılı değil. 2018 ITCH verisinin `A` mesajında zaman damgası nanosaniye çözünürlüklüdür; 2112 sürümünde ek olarak `Ranking Time` ve `Ranking Sequence Number` alanları vardır (bkz. 07-itch.md, Appendix A).
- [DOĞRULA] Madde 17: Ek-18 1, s. 203: "Hâlihazırda devrede olmayan uygulamalar bu nedenle paylaşılmıştır" deniyor; hangi öncelik kurallarının devrede olmadığı yazılı değil.
- [DOĞRULA] Madde 17: Öncelik kuralları "aksi belirtilmedikçe limit fiyatlı emirlere ilişkin" olarak verilmiştir. Piyasa, piyasadan limite, dengeleyici, Orta Nokta, AOF ve diğer emir tiplerinin öncelik sırası 5.6.1'de yok; tek fiyat yöntemindeki sıralaması Ek-18 2.1 ve 3.1'de (s. 207, 209) ve 03-tek-fiyat.md'de; diğerleri için 05-emirler.md.
- [DOĞRULA] Madde 24: Ek-18 1.2'de "Emir bilgileri (MPF-AFK-Hesap No) değiştiğinde [öncelik] kaybolur (bu alanların değiştirilmesine izin verilmez)" yazıyor; değiştirilmesine izin verilmiyorsa öncelik kaybının ne zaman oluştuğu belirsiz.
- [DOĞRULA] Madde 20: Miktar azaltmada önceliğin korunduğu Prosedür ana metninde (5.5.1) açıkça yazılı değil; yalnızca Ek-18 1.2'de var. 5.5.1 miktarın "azaltılıp artırılabileceğini" ve yalnızca artırımda zaman önceliği kaybını söylüyor (kaynakta çelişki yok, azaltımdaki koruma yalnızca Ek'te).
- [DOĞRULA] Madde 13: Tablo-9'un "İşlem Yöntemi" sütununda Toptan Alış Satış için bir yöntem adı değil, "özel işlem bildirimi yoluyla ... gerçekleştirilir" ifadesi var; özel işlem bildirimi esasları Ek-17'dedir (`../ekler/ek17.md`), bu dosyanın kapsamı dışındadır.
- [DOĞRULA] Madde 8 ve Tablo-9: "Ana işlem sırasına bağlı ve geçici olarak açılan işlem sıraları"nın hangi sıra uzantılarını (ör. `.BE`, `.TE` vb.) kapsadığı yazılı değil; Tablo-9 yalnızca işlem türlerini sayar.
- [DOĞRULA] Madde 5: Yönetim Kurulunca belirlenen azami miktar/tutar sınırlarının değerleri 5.2.1'de yok; 5.6.3–5.6.4 ve Tablo-14 için bkz. 05-emirler.md.
- [DOĞRULA] Madde 47 ve Prosedür 5.6.5 (s. 94): Prosedür "emrin fiyatı belirlenen zaman içinde marj dışına çıktığında ... ilgili emir iptal edilir" der; FIX spesifikasyonu (6.5.6) marj dışına çıkan emrin iptal edilmediğini, duraklatıldığını ve özgün zaman önceliğiyle yeniden etkinleştirildiğini söyler. İki belge çelişiyor görünür; hangisinin geçerli olduğu bu çalışmada belirlenmedi (Prosedür metni Tarihli/Süreli emirlere ilişkin cümle içinde yer alıyor).
- [DOĞRULA] Madde 34–43: SMP, Prosedürde yer almayan ayrı bir teknik dokümandan alınmıştır; kullanıma açılış tarihi duyurulmamıştır (belgede "sonradan duyurulacaktır"). 08.10.2018 örnek verisinde SMP alanları yoktur. SMP nedeniyle iptal edilen emrin ITCH'te nasıl göründüğü (yalnızca `D`) yazılı değildir.
- [DOĞRULA] Madde 44–45: FIX ve OUCH spesifikasyonları protokol dokümanlarıdır; Prosedürdeki emir tipi tanımlarıyla (5.4.2–5.4.3) uyumu 05-emirler.md'de karşılaştırılacaktır.
- [DOĞRULA] Ek-18 tabloları: Ek-18 s. 204'teki öncelik listesi düz metin (tablo değil); s. 208 ve s. 210 tabloları ikişer sütun grubudur (Alış/Satış); sütun kayması riski yok (koordinat tabanlı aktarım, kullanıcı doğrulaması yapılmış).

## Test örnekleri
Prosedür 5.2.1 ve 5.6.1'de sayısal örnek yoktur. Aşağıdakiler Ek-18'deki sürekli işlem örnekleridir (birebir; `../ekler/ek18.md`).

**Ek-18 2.2.2 Sürekli işlem yönteminde piyasa emri (s. 208)** — emir defteri (piyasa emri girilmeden önce):

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 100 | 10,50 | 11,00 | 80 |
| 90 | 10,45 | 11,05 | 90 |
| 80 | 10,40 | 11,10 | 100 |

150 lot alış piyasa emri girilirse: 80 adet satış tarafındaki 11,00 TL seviyesinden, kalan 70 adet 11,05 TL seviyesinden işleme dönüşür. Sonrasında emir defteri:

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 100 | 10,50 | 11,05 | 20 |
| 90 | 10,45 | 11,10 | 100 |
| 80 | 10,40 | | |

**Ek-18 3.2.2 Sürekli işlem yönteminde piyasadan limite emir (s. 210)** — aynı başlangıç emir defteri (yukarıdaki ilk tablo). 150 lot piyasadan limite alış emri girilirse: 80 adet 11,00 TL seviyesinden işleme dönüşür, kalan 70 adet işlemin gerçekleştiği fiyat olan 11,00 TL'den alış tarafında pasife yazılır. Sonrasında emir defteri:

| Alış Miktar | Alış Fiyat | Satış Fiyat | Satış Miktar |
|---|---|---|---|
| 70 | 11,00 | 11,05 | 90 |
| 100 | 10,50 | 11,10 | 100 |
| 90 | 10,45 | | |
| 80 | 10,40 | | |

**Örnek ITCH verisinden doğrulama gözlemleri (08.10.2018; kaynak belge örneği değil, kural doğrulaması)** — ayrıntı: `../veri/itch-ornek-veri-dogrulama.md` bölüm 9:
- Emir defterinde alış tarafı fiyata göre azalan, satış tarafı artan sırada tutulduğunda, `A` mesajındaki `Order Book Position` ile yerleştirilen 2.504.057 emrin (bölüm 1: 1.219.236; bölüm 2: 1.284.821) hiçbirinde komşu emirlere göre fiyat sırası bozulmadı (fiyat önceliği ihlali: 0).
- Sürekli işlemde ve kapanış fiyatından işlemlerde gelen 846.386 `E` mesajının (bölüm 1: 421.084 + 923; bölüm 2: 423.287 + 1.092) tamamında gerçekleşen emir, o taraftaki emir defterinin en önündeki (konum 1) emirdir.
- Aynı fiyatta zaman sırasının bozulduğu yerleştirmeler (bölüm 1: 2.815; bölüm 2: 2.905), tamamı daha önce `D` ile silinmiş aynı Order ID'nin yeniden eklenmesidir (bu, "miktar azaltıldığında öncelik korunur" kuralının uygulanması olabilir; **doğrulanmadı**).
