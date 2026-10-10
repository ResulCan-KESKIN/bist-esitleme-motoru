# Genium INET FIX for BIST — Emir İletimi (Order Entry) Protokol Spesifikasyonu (Türkçe çeviri, kapsamı sınırlı)

Kaynak: `kaynaklar/genium-inet-fix-protocol-specification.pdf` — "Genium INET FIX for BIST", sürüm 1.0.65, yayın tarihi 17.09.2026, 146 sayfa, etiket "HİZMETE ÖZEL/RESTRICTED". Telif: Nasdaq, Inc.
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir. FIX tag numaraları, alan adları, değerler ve sabitler çevrilmeden bırakılmıştır. Sayfa numaraları PDF sayfa numarasıdır.
**Kapsam (önemli):** Bu belge 146 sayfalık, büyük bölümü projeyle ilgisiz bir FIX protokol kılavuzudur. Projeye (Pay Piyasası emir davranışı, eşleştirme motoru, manipülasyon tespiti) ilişkin bölümler tam çevrilmiştir; geri kalanı çevrilmemiştir:
- **Çevrilenler:** 1–2 (Referanslar, Genel Bakış), 3.1–3.2 (CompID, SenderSubID; yalnızca anahtar bilgiler), 6 Order Management (6.1–6.9 metinleri tam; 6.10'da New Order Single, Order Cancel Request, Order Cancel Replace Request, Order Cancel Reject ve Execution Report'un Order Ack varyantı tam tablo; diğer Execution Report varyantları ve Business Message Reject özet tablo olarak), 11–14 Ekler A–D (eklenen alanlar, alan uzunlukları, Trade Types, Secondary Trade Types).
- **Çevrilmeyenler:** 3.3–3.14 (oturum katmanı: kimlik doğrulama, Logon, Heartbeat vb.), 4 (User Authentication), 5 (Business Level Party Identifiers), 6.10.11–6.10.17'nin tam alan tabloları (6.10.6 ile aynı alanları taşır), 7 (Multileg Orders), 8 (General Quote Handling), 9 (Reporting of privately negotiated Trades), 10 (Trade Confirmation and Management), Revision History. Gerektiğinde PDF'ten okunmalıdır.
Doğrulama: Tag numaraları PDF metninden çıkarılan listelerle karşılaştırılmıştır (dosya sonuna bakın). Metin çevirisi sayfa görüntüsüyle karşılaştırılmadı. Kullanıcı doğrulaması: bekliyor.
İlgili dosyalar: `ouch-protokol-spesifikasyonu.md`, `emrimle-eslesmesin-teknik-calisma-esaslari.md`, `../kurallar/04-surekli-islem.md` (madde 44–48), `../kurallar/05-emirler.md` (yazılacak).

---

## 1 Referanslar [s. 5]

[1] FIX 5.0 SP2 Protocol Specification — http://fixprotocol.org/specifications/fix5.0sp2spec
[2] FIX Protocol Limited, Market Data Optimization Working Group: Recommended Practices for Book Management, Version 2.00, 2007.

## 2 Genel Bakış [s. 5–6]

Bu belge Genium INET işlem sistemine FIX arayüzünün spesifikasyonunu içerir. Arayüz FIX Protocol 5.0 SP2 standardına dayanır. Genium INET'in uyguladığı arayüz FIX spesifikasyonlarını mümkün olduğunca izler. Mutlak çoğunlukla mesajların yapısı ve anlamı standartla aynıdır. Bazı durumlarda protokol, standardın dikkate almadığı işlevleri kapsayacak şekilde genişletilmiştir; bu uzantılar belgede açıkça ayrıntılandırılmıştır. Diğer durumlarda standart belirsizdir veya ayrıntıların ikili olarak kararlaştırılması gerektiğini belirtir; bu durumlarda belirsizliği önlemek için bu kılavuz ayrıntılı açıklama sağlar. Bilgi kaynaklarında tekrarı önlemek için bu belge standartla tam uyumlu konuların açıklamalarını içermez; standart belgeler bu kılavuzda açıkça kapsanmayan her konu için ana kaynaktır.

### 2.1 Desteklenen Mesajlar

- **Yönetsel mesajlar:** Logon, Logout, Sequence Reset, Resend Request, Reject, Heartbeat, Test Request.
- **Giriş yönlü uygulama mesajları:** User Request, New Order Single, Order Cancel Replace Request, Order Cancel Request, Mass Quote, Trade Capture Report, Security Definition Request.
- **Çıkış yönlü uygulama mesajları:** User Response, User Notification, Execution Report, Order Cancel Reject, Business Message Reject, Mass Quote Acknowledgement, Trade Capture Report, Trade Capture Report Ack, Security Definition – Registration Response.

### 2.2 Genium INET Deposu (Repository)

Bu spesifikasyon kullanılabilecek tüm mesajların, alanların ve numaralandırılmış değerlerin tam kümesini tanımlar. Çoğu FIX uygulamasında olduğu gibi, FIX 5.0 SP2'de tanımlı tüm mesaj, bileşen, alan ve numaralandırılmış değerlerin yalnızca küçük bir alt kümesini destekler. Bu spesifikasyona karşılık gelen FPL biçimli bir depo ayrıca teslim edilir. NOT: Bu spesifikasyona uymayan giriş yönlü mesajlar, oturum seviyesi bir Reject mesajıyla reddedilir.

## 3 FIX Oturumu (özet) [s. 7]

- Oturum katmanı standart FIX oturumuna uyar.
- Sender- ve TargetCompID FIX oturumunu benzersiz tanımlar; bir oturum aynı anda yalnızca iki ana makine arasında etkin olabilir; aynı CompID'lerle (ör. yedek ağ geçidine) paralel ikinci oturum kurma girişimi reddedilir. Borsaya giden işlemlerde TargetCompID üretimde "BI", test sistemlerinde "BI_TEST"; Borsadan gelen işlemlerde SenderCompID aynı değerlerdir.
- Her giriş yönlü iş işleminde SenderSubID (tag 50) doğrulanmış bir kullanıcıya ayarlanmalıdır; gelen işlemlerdeki SenderSubID çıkış yönlü işlemlerde TargetSubID (tag 57) olarak geri yansıtılır. Logon veya User Request'te SenderSubID, giriş yapılmak istenen kullanıcı kimliğine ayarlanmalıdır.

## 6 Emir Yönetimi (Order Management) [s. 21–67]

### 6.1 Geceyi geçen emirler (Overnight orders) [s. 21]

Geceyi geçen emir göndermek isteyen istemciler, ClOrdID'nin emrin tüm ömrü boyunca benzersiz olduğundan emin olmalıdır. Basit bir çözüm ClOrdID'ye bir tarih eklemektir.

### 6.2 Aktarım (pass-thru) alanları [s. 21]

Genium INET gelen işlemlerde öncelikle üç alanı aktarım alanı olarak sunar. Bu alanların değerleri sonraki çıkış yönlü işlemlerde istemciye geri yansıtılır:

| Alan | Tag | Eşlendiği | Uzunluk | Açıklama |
|---|---|---|---|---|
| Account | 1 | exchangeInfo (ex_client veya Client) | 10/15 | Hesap. Emir defteri için yapılandırılmış hesap modeline bakın. |
| Custodian Party (exClinet veya AFK) | 448 | n/a | 3 | AFK hesabı. Emir defteri için yapılandırılmış hesap modeline bakın. |
| AllocID | 70 | customer_info | 15 | |

NOT: Aktarım alanları ret mesajlarında geri yansıtılmaz.

### 6.3 Takas hesapları (Clearing Accounts) [s. 21–22]

Takas hesabı genel olarak iki parçaya ayrılır: Clearing Firm (takas kuruluşu) ve Clearing Account (takas hesabı). Takas hesabı bilgisini taşıyan alanlar, mesajın yönüne (Borsaya giriş yönlü veya çıkış yönlü) ve mesaj tipine bağlı olarak farklıdır:

| Mesajlar | Yön | Clearing Account | Clearing Firm | Açıklama |
|---|---|---|---|---|
| New Order Single, Cancel Replace Request, Execution Report | IN/OUT | Account (1) | örtük (implied) | Clearing Firm emrin sahibiyle aynıdır. |
| Trade Reports | IN/OUT | Account (1) | örtük | Clearing Firm işlemin sahibiyle aynıdır. |
| Rectify Trade | IN | AllocAccount (79) | Nested2PartyID (Nested2PartyRole = 4) | |
| Give-ups (Allocation Instruction, Allocation Report) | IN/OUT | AllocAccount (79) | NestedPartyID (NestedPartyRole = 14) | |

### 6.4 Enstrüman tanımlayıcıları [s. 22]

Herhangi bir işlem sistemi için menkul kıymetlerin FIX mesajında doğru tanımlanması son derece önemlidir. Bu uygulamada iki alternatif tanımlayıcı kullanılabilir:
- `Symbol (55)`: menkul kıymetin OMNet kısa adını (ins_id_s) içermelidir.
- `SecurityID (48)`: menkul kıymetin Orderbook ID'sini içerir; Symbol yerine kullanılabilecek alternatif sayısal tanımlayıcıdır. **NOT: Orderbook ID aynı menkul kıymet için işlem günleri arasında farklı olabilir.**

### 6.5 Ana İş Akışı (Main Workflow) [s. 22–25]

**6.5.1 Yeni emir:** Emir akışı, kullanıcının bir New Order Single mesajı göndermesiyle başlar. Yanıt olarak bir Execution Report üretilir. Execution Report emri gönderene yönelik bir yanıttır ve emrin ayrıntılarını içerir. Emir reddedilirse Execution Report ilgili hata mesajlarını içerir.

**6.5.2 Gerçekleşmeler (Fills):** Bir emir gerçekleştiğinde Execution Report gerçekleşme ayrıntılarını içerir (mesaj ayrıntıları için 6.10.15). Ayrıca bir Trade Capture Report üretilir. İkisi arasındaki temel farklar: Execution Report'lar emri gönderene yöneliktir ve öncelikle ön ofis amaçlıdır; emir durumu bilgisini ve (varsa) gerçekleşme bilgisini içerir. Trade Capture Report'lar işlemin kendisini kaydeden mesajlardır ve öncelikle aşağı akış (downstream) işleme içindir; işlem hakkında çeşitli tarafları (aracı kurum arka ofisi, takas kuruluşları, takas merkezleri, saklama kuruluşları ve düzenleyiciler) bilgilendirmek için kullanılır. Aşağı akış işleme farklı yerlerde ve farklı amaçlarla gerçekleştiği için Trade Capture Report mesajı alıcıya göre biraz farklı görünebilir. Trade Capture Report mesajları özel olarak müzakere edilmiş işlemlerin bildirimi ve işleme taraf olmayan taraflara işlemlerin aktarılması gibi pek çok başka amaçla da kullanılır; ancak bu bu bölümün kapsamı dışındadır. İşlem iptalleri (reversal) ve düzeltmeleri yalnızca Trade Capture Report olarak gönderilir.

**6.5.2.1 Trade Match ID:** `TrdMatchID` (880) sistemin ürettiği eşleşme kimliğini içerir. TrdMatchID, 16 baytlık onaltılık dizge olarak kodlanmış 64 bitlik ikili eşleşme kimliğini tutar. NOT: TrdMatchID, Trade Capture Report onay mesajlarında da ayarlanır.

**6.5.3 Emir değişikliği (Order Modification):** Emir değişikliği Order Cancel Replace Request mesajıyla yapılır. Adına rağmen, eski emrin kaldırılıp yenisinin konması değil, mevcut emrin değiştirilmesini temsil eder. Ancak emir değişikliği, emir talimatlarında delta bir değişiklik değildir; Cancel Replace'te ayarlanan değerler emrin istenen yeni durumunu temsil eder. Bir Execution Report emrin yeni durumunu iletir.
- Cancel Replace'te ayarlanmayan alanların önceki değerlerini koruduğu varsayılır.
- Zorunlu alanlar, değişsin değişmesin ayarlanmalıdır.

**6.5.3.1 Değişmesine izin verilen emir nitelikleri:** FIX hemen hemen tüm emir niteliklerinin değiştirilmesine izin verse de, arka uç Genium INET sisteminin izin verdiği değişikliklerde sınırlamalar vardır. Şu nitelikler değiştirilebilir: OrderQty (38); MaxFloor (111); TimeInForce (59) ile birlikte ExpireDate (432) veya TradingSessionID (336); AllocID (70) (aktarım alanı); Price (44).
- **NOT:** Bir emrin fiyatındaki her değişiklik veya miktarın artırılması emrin piyasadaki önceliğini kaybetmesine yol açar.
- NOT 2: Bir emri TimeInForce = IOC veya FoK olarak değiştirmeye izin verilmez.
- NOT 3: Bir emrin fiyatını sıfıra değiştirmeye izin verilmez. Sıfır fiyat isteniyorsa emir silinmeli ve fiyatı 0 olan yeni bir emir girilmelidir.
- NOT 4: MaxFloor, PartyID (PartyRole Custodian ise) veya TimeInForce'ın değişmesi istenmiyorsa bunları Cancel Replace mesajına eklemeyin. Emrin önceliğini kaybetmesine veya Cancel Replace'in reddedilmesine yol açabilirler.

**6.5.3.2 Yeniden bildirimler (Restatements):** Execution Report – Restatement mesajı, sabahları geceyi geçen emirleri (GTC/GTD) yeniden bildirmek için kullanılır. Bu durumda `ExecRestatementReason` 1 = GT renewal / restatement (kurumsal işlem yok) olarak ayarlanır (mesaj ayrıntıları için 6.10.14).

**6.5.3.3 FIX ile girilen emirlerin istek dışı değiştirilmesi:** FIX ile girilen emirler Omnet gibi başka protokollerle değiştirilebilir. Piyasanın mevcut emirleri değiştirmesi de mümkündür. Böyle bir durumda FIX üzerinden bir Execution Report – Unsolicited Order Update gönderilir (6.10.13).

**6.5.4 Emir iptali:** Kullanıcı daha önce gönderilmiş tek bir emri iptal etmek isterse Order Cancel Request mesajı kullanılır. İptal edilen her emrin durumunu bildiren Execution Report'lar düzenlenir. Sistem, her IOC ve FoK emri için iptal mesajları (Execution Report – IOC/FoK Order Cancel) üretir. Sistem, hemen eşleşemeyen Market-to-Limit emirleri için iptal mesajları (Execution Report – Market-to-Limit Order Cancel) üretir. Order Cancel Request kısmi iptal için kullanılamaz. İstek dışı iptaller (Execution Report – Unsolicited Cancel) istemciye gönderilir. **6.5.4.1:** Omnet veya başka yollarla girilmiş emirler de FIX ile iptal edilebilir; bunun için doğru OrderID (Omnet emir numarası), enstrüman tanımlayıcısı (Symbol veya SecurityID) ve Side verilmelidir; bu durumda OrigClOrdID "NONE" olarak ayarlanır. **6.5.4.2:** FIX ile girilen emirler başka protokollerle veya piyasa tarafından iptal edilebilir; bu durumda FIX üzerinden bir Execution Report – Unsolicited Cancel gönderilir (6.10.12).

**6.5.5 Bağlantı kaybında emir iptali:** Arka uç, bir FIX oturumu yapılandırılabilir bir süre kesintiye uğradığında bekleyen emirleri iptal edecek şekilde yapılandırılabilir. Üç seçenek: bağlantı koptuğunda iptal etme; tümünü iptal et (Cancel all); günlükleri iptal et (Cancel day). Emir iptalinden sonra şu ayrıntılarla bir Execution Report gönderilir: OrdStatus (39) = Canceled (4); ExecType (150) = Canceled (4); Text (58) = "Cancelled due to connection termination".

**6.5.6 Duraklatılmış emirler (Paused Orders):** Eşleştirme motoru (ME) tarafından duraklatılan emirler eşleşmeye uygun değildir. Bu emirler EP (denge) fiyatına katkıda bulunmaz ve piyasadaki fiyat resminin parçası değildir. ME, koşullar uygun olduğunda duraklatılmış emirleri özgün zaman önceliğiyle otomatik olarak yeniden etkinleştirir. Eşleştirme motoru emirleri şu durumlarda duraklatılmış olarak bildirir: etkin fiyat limiti aralığının dışına çıkan emirler; mesai dışı (off-hours) seanslarda mesai-dışı olmayan emirler.

*6.5.6.1 Fiyat limitleri dışına çıkan emirlerin duraklatılması — örnek:* #1 ve #2 numaralı iki emir farklı fiyatlardadır. a) Başlangıçta fiyat limitleri etkin değildir ve iki emir de aktiftir. b) Fiyat limitleri etkinleştirilir. İki emir de limitler içindedir ve aktif kalır. c) Referans fiyat değişir ve üst/alt fiyat limitleri kayar. #1 hâlâ limitler içindedir ve aktif kalır; #2 fiyat limitlerinin dışına düşer ve otomatik olarak duraklatılır. d) Fiyat limitleri devre dışı bırakılır. #2, özgün zaman önceliğiyle yeniden etkinleştirilir. e) Fiyat limitleri tekrar etkinleştirilir. #2 alt limitin dışına düşer ve otomatik olarak duraklatılır.

*6.5.6.2 Fiyat limitleri dışındaki ve off-hours seanstaki emirlerin duraklatılması — örnek:* Bu örnek gerçekçi bir iş senaryosu olmayabilir; duraklatma mekanizmasını açıklamak için verilmiştir. Üç emir farklı fiyatlardadır. #1 off-hours emridir; #2 ve #3 off-hours olmayan emirlerdir. a) Başlangıçta fiyat limiti izleme etkin değildir ve tüm emirler aktiftir. b) Fiyat limitleri etkinleştirilir; tüm emirler limitler içindedir ve aktif kalır. c) Referans fiyat değişir ve limitler kayar. #1 ve #2 hâlâ limitler içinde ve aktif kalır; #3 limitlerin dışına düşer ve otomatik olarak duraklatılır. d) Enstrüman off-hours (mesai dışı) moda girer. #2 ve #3 off-hours olmayan emirlerdir ve katılmamalıdır. #2 otomatik olarak duraklatılır; #3 zaten duraklatılmış durumdadır, değişikliğe gerek yoktur. e) Enstrüman off-hours modunda kalır. Fiyat limitleri devre dışı bırakılır, ancak O#2 ve O#3 off-hours olmayan emirler olduğu için duraklatılmış kalırlar. f) Enstrüman off-hours modundan çıkar ve normal seansta fiyat limiti denetimi olmadan işlem görmeye başlar. Off-hours olmayan O#2 ve O#3 otomatik olarak yeniden etkinleştirilir. g) Fiyat limitleri etkinleştirilir; O#3 limitlerin dışında olduğu için otomatik olarak yeniden duraklatılır.

Bir sınır dışı (outlier) emir¹ girilir girilmez duraklatılırsa veya emir seans değişikliği nedeniyle sistem tarafından duraklatılırsa, FIX ağ geçidi `OrdStatus(39) = Suspended(9)` ve `Text(58) = "Paused"` ile tanımlanan bir ER yayımlar; bu, emrin sistem tarafından duraklatıldığını gösterir.
¹ *Sınır dışı (outlier) emir:* üst fiyat limitinin üzerinde fiyatlı bir satış emri veya alt fiyat limitinin altında fiyatlı bir alış emridir.

### 6.6 Emir Özellikleri (Order Features) [s. 25–33]

**6.6.1 Emir tanımlama [s. 25–26]**

*6.6.1.1 Client Order ID:* Müşterinin gönderdiği emirle ilgili her mesaj (giriş, iptal, değişiklik) ClOrdID (11) alanında benzersiz bir tanımlayıcı içermelidir. Standardın belirttiği gibi, bu tanımlayıcıların benzersizliği işlem seansı boyunca korunmalıdır. Birden fazla işlem seansı süren emirler kullanılıyorsa gönderen, seanslar arası benzersizliği de sağlamalıdır. İşlem motoru mesajı kabul ettikten sonra istemci aynı ClOrdID'li ilgili onay mesajını alır. Kullanıcının bir emri gönderdikten hemen sonra değiştirmek veya iptal etmek istediği durumlarda, sonraki mesajda OrigClOrdID (41) alanında ilk emre başvurulur. *Firma birden çok FIX oturumu kullandığında Client Order ID'ler:* Birden çok ön yüz işlem uygulaması veya birden çok FIX oturumu kullanan firmalar şunlara dikkat etmelidir: Borsa, Execution Report'ların drop copy'lerini emri gönderen oturumdan başka FIX oturumlarına sunuyorsa, bu drop copy Execution Report'lar ClOrdID içermez (çünkü çeşitli FIX oturumları veya altta yatan işlem uygulamaları çakışan ClOrdID'ler kullanıyor olabilir). Yukarıdakiler, Borsa operasyonlarının emir sahibi adına emir yönetimi yaptığı durumlar için de geçerli olabilir.

*6.6.1.2 Order ID:* OrderID (37) alanı piyasanın atadığı emir tanımlayıcısıdır. Bu tanımlayıcı statiktir ve emir değiştirilse bile emirle birlikte kalır. **NOT: Genium INET OrderID'leri yalnızca emir defteri ve taraf (Side) başına benzersizdir.** Dolayısıyla aynı emir defterindeki bir alış emri ve bir satış emri aynı OrderID'ye sahip olabilir (Mass Quote'larda olduğu gibi). Emirlerin tanımlanması OrderID, emir defteri kimliği (SecurityID/Symbol) ve Side'a dayandırılmaya özen gösterilmelidir. Kullanıcılara, emir güncellemelerinde ve iptallerinde mümkün olduğunca (yeni emir onayı (Execution Report) alınmadan önce emir işlemleri göndermek dışındaki tüm durumlarda) OrigClOrdID yerine OrderID'yi sağlamaları önerilir. OrderID, emir değişikliği ve iptali için tercih edilen tanımlayıcıdır, çünkü işlem motorunda dahili olarak kullanılan tanımlayıcıdır; diğer tanımlayıcıların kullanımı bir arama gerektirir ve mesaj gecikmesini artırır. Standart FIX'te Cancel Replace ve Cancel mesajlarında OrigClOrdID alanı zorunludur. OrderID kullanmak istiyorsanız OrigClOrdID'yi "NONE" (tırnak işaretleri hariç) olarak ayarlamanız önerilir; Cancel veya Cancel Replace Request'te OrderID ayarlıysa sistem OrigClOrdID'yi yok sayar. OrderID kullanımı, kullanıcının işlem motorundan emir onayı beklemesini gerektirdiği için, anlık işlemler OrigClOrdID (41) başvuru alanının kullanılmasını gerektirir. Bu alan, piyasayla FIX dışındaki yollarla yapılan iletişimde emri tanımlamak için de gerekli olabilir.

*6.6.1.3 Execution ID:* ExecID (17) alanı işlemlerin tanımlayıcısı değildir. Piyasanın ürettiği her benzersiz Execution Report mesajına atanan, tüm FIX oturumu boyunca yinelenmeyen bir tanımlayıcıdır. ExecID bir tamsayı değeridir. İstisna olarak, 15'ten fazla işlem bacağı olan kombinasyon emirlerinde ExecID benzersiz değildir.

*6.6.1.4 ExecType:* Bir gerçekleşme olduğunda ExecType (150) alanı F = Trade olarak ayarlanır. NOT: İşlem sonrası düzeltmeler (corrects) veya iptaller (reversals) Execution Report'larda temsil edilmez; bu işlevsellik için Trade Capture Report'lara bakın.

**6.6.2 Emir durumları [s. 27]**

Emir durumu değişiklikleri Execution Report mesajlarıyla bildirilir. Her durum değişikliği bir Execution Report ile iletilir. Bir emir şu ara durumlarda olabilir:
- **New (Yeni):** Emir işlem motoru tarafından kabul edilmiş ve hemen başka bir duruma geçmemişse uygulanır: emir deftere konmuş ancak (kısmen) gerçekleşmemiştir; veya emir deftere konmamış, bir aktivasyon (ör. stop koşulu veya bir seans değişikliği için, Trigger emri gibi) beklemektedir.
- **Partially filled (Kısmen gerçekleşti).**

Şunlar nihai durumlardır; emrin artık defterde olmadığını ve güncellemeler ya da durum istekleri için kullanılamadığını gösterir:
- **Rejected (Reddedildi):** Emir doğrulama kurallarından geçemedi.
- **Canceled (İptal):** Emir bir iptal isteği nedeniyle veya TimeInForce nedenleriyle sistemden kaldırıldı.
- **Filled (Tamamen gerçekleşti):** Emir tamamen gerçekleşti.
- **Expired (Süresi doldu):** Bir GTD emrinin süresi dolduğunda.
- **Suspended (Askıya alındı):** Emir askıya alındı.

**6.6.3 Emir tipleri [s. 27–28]**

Emir tipi OrdType (40) alanında belirtilir. Üç emir tipi desteklenir: Market (Piyasa), Limit, Market-to-Limit (FIX'te "Market with leftover as limit" olarak adlandırılır).

*6.6.3.1 Piyasa emirleri:* Piyasa emirleri her zaman mümkün olan en iyi fiyattan gerçekleştirilir. Bir piyasa emri tamamen karşılanana kadar gerektiği kadar fiyat seviyesinden geçer. **Sürekli işlemde bir piyasa emri emir defterinde saklanamaz; TimeInForce'ı IOC veya FoK olmalıdır.** Piyasa emirlerinin eşleşmeyen (non-matching) durumlarda deftere girmesine izin verilebilir. Seans eşleşen bir duruma geçtiğinde emir gerçekleştirilir ve/veya iptal edilir.

*6.6.3.2 Market-to-Limit emirleri:* Market-to-Limit emri, kalan miktarın emrin bir kısmının gerçekleştiği fiyattan deftere konduğu bir piyasa emridir. Karşı tarafta emir yoksa Market-to-Limit emri hemen iptal edilir. Bir Piyasa emriyle karşılaştırıldığında, Market-to-Limit emri yalnızca en iyi fiyat seviyesinde gerçekleşir ve dolayısıyla defteri taramaz. TimeInForce'ı IOC veya FoK ayarlanırsa Market-to-Limit emri bir Piyasa emri gibi davranır ancak yalnızca en yüksek fiyat seviyesinde eşleşir. NOT: Emir bir Limit emre dönüştürüldüğünde sonraki Execution Report'ların (Order Ack dâhil) OrdType alanı Limit olarak ayarlanır ve Price alanı gerçekleşme fiyatına ayarlanır. NOT 2: Eşleşmeyen bir müzayede (auction) durumunda girilen Market to Limit emirlerin tüm miktarı, uncross (müzayede eşleştirmesi) sonrasında limit emre dönüştürülür. Bu senaryoda bir Unsolicited update mesajı gönderilir.

**6.6.4 Emir vadesi (Order Expiry) [s. 28]**

Bir emir, ne zaman veya nasıl sona ereceğini ya da defterden otomatik olarak kaldırılacağını belirten çeşitli koşullar tanımlayabilir. Bir GTD emrinin süresi dolduğu akşam, o emir için OrdStatus (39) = Cancelled olan bir Execution Report gönderilir (bkz. 6.10.17). Bir GTC emrinin de süresi dolabilir. Örnek: bir GTC emri askıya alınır; aynı gün silinmez veya yeniden etkinleştirilmezse (FIX ile mümkün değil), ertesi gün OrdStatus'u Cancelled olan bir ER gönderilir. NOT: Yalnızca bir GTC emrinin süresi enstrüman gün içinde sona erdiği için dolarsa veya bir GTD emri kurumsal işlemle iptal edilirse bir emir-süresi-doldu işlemi gönderilir.

Desteklenen TimeInForce (59) değerleri:

| Değer | Ad | Açıklama |
|---|---|---|
| 0 | Day | Gün |
| 1 | Good Till Cancel (GTC) | |
| 3 | Immediate Or Cancel (IOC) | |
| 4 | Fill or Kill (FoK) | FoK emirlerinde MatchIncrement (1089) ayarlanamaz. |
| 6 | Good Till Date (GTD) | GTD emirlerinde ExpireDate (432) ayarlanmalıdır. |
| S | Good till End of Session (GTS) | Emir, TradingSessionID (336) içinde belirtilen Good till End of Session durum tipine sahip ilk seansın sonunda sona erer. Aşağıdaki ayrıntılı açıklamaya bakın. |
| 9 | At Crossing | Dengeleyici (Imbalance) emirleri girmek için kullanılır. Tag 44 (Price) 0 olarak, Tag 40 (OrdType) 1 (Market) olarak ayarlanmalıdır. |

**6.6.5 Good till End of Session (GTS) [s. 28]:** GTS bir FIX uzantısıdır. GTS emri GTD emrine benzer, ancak sona erme tarihi yerine emrin hangi seans tipinde sona ereceği belirtilir. TimeInForce 'S' olarak ayarlanmalıdır. GTS emri TradingSessionID (336) ile verilen tipteki ilk seansın sonuna kadar geçerlidir. Geçerli seans değerleri için Borsayla iletişime geçilmelidir. Seans tipi, eşit emir davranışına sahip birkaç seansı, seansla ilgili emir işlemede kullanılacak tek bir varlıkta gruplamak için kullanılır. Aynı seans tipinin gün içinde birden fazla kez işletildiği durumlarda emir mümkün olan en erken fırsatta sona erer.

**6.6.6 Miktar koşulları (Quantity Conditions) [s. 28–29]**

Bir emir çeşitli miktar koşulları tanımlayabilir. **Match Increment (1089):** Bu çözümde MatchIncrement, Blok (Block) veya Küsurat (Odd Lot) emirlerini girmek için kullanılır. MatchIncrement, emrin emir defteri için Block Lot/Odd Lot olarak yapılandırılmış birim sayısına (lot büyüklüğü) ayarlanırsa blok lot/küsurat emri girilebilir. Bir enstrümanın lot büyüklükleri Reference Data'dan öğrenilmelidir (FIX Order Entry üzerinden sağlanmaz). Yanlış MatchIncrement değerli emir reddedilir. MatchIncrement ayarlanmazsa emir varsayılan olarak Round Lot'tur. NOT: FoK emirlerinde MatchIncrement'a izin verilmez.

**All-or-None (AON):** Bir emrin tamamen veya hiç gerçekleştirilmemesi talimatıdır; FoK'a benzer, ancak hemen gerçekleşmezse defterde kalır. AON emirleri için Tag 18 ExecInst kullanılır. NOT: AON emirlerinde MatchIncrement ayarlanamaz.

**Rezerv Miktar (Reserve Quantity) Emirleri** (a.k.a. "Hidden" veya "Iceberg"): Kullanıcıların emrin tam büyüklüğünü gizlemesine ve böylece fiyatlar üzerindeki etkisini potansiyel olarak sınırlamasına olanak tanır. **MaxFloor (111):** Kamuya açık Piyasa Verisinde gösterilen en yüksek emir miktarını belirtmek için kullanılır. NOT: MaxFloor = 0, yani tamamen gizli emir, Genium INET'te desteklenmez. MaxFloor'u sıfır yapmak emrin tamamını görünür kılar. NOT 2: MaxFloor, standart FIX'te beklendiği gibi davranacak şekilde değiştirilmiştir. Beklenen davranış, emir kısmen gerçekleştiğinde MaxFloor değerinin azaltılmasıdır; önceki uygulama MaxFloor'u özgün değerinde tutuyordu.

**6.6.7 Tetikleme Talimatları (Triggering Instructions) [s. 29–31]**

FIX'teki Triggering Instructions bloğu önceden tanımlı otomatik emir değişikliklerini ifade etmek için kullanılır. Tetikleyiciler farklı olaylara göre çalışabilir. `TriggerType` (1100) alanı neyin değişikliği tetikleyeceğini belirler. Desteklenen tek eylem, tetiklenen emrin etkinleştirilmesidir. Tetikleyici emir, tetikleme koşulu karşılanana kadar gizli ve pasif kalır. Tetikleme gerçekleştiğinde emir ya gerçekleşir ya da yeni bir emirmiş gibi deftere eklenir. Emir başına yalnızca bir tetikleme talimatına izin verilir. "Normal" bir emir için kullanılabilen tüm emir nitelikleri (ör. Order Type, Time In Force vb.) tetiklenecek emir için desteklenir. NOT: Sona erme günü = geçerli gün olan tetikleyici emirler, tetikleme koşulu henüz karşılanmamışsa gün sonunda kaldırılır.

| Tag | Ad | Açıklama |
|---|---|---|
| 1100 | TriggerType | Neyin emir değişikliğini tetikleyeceğini belirler. Geçerli değerler: 2 = Specified Trading Session; 4 = Price Movement |
| 1101 | TriggerAction | Tetikleyici gerçekleştiğinde yapılacak eylem tipini tanımlar. Geçerli değerler: 1 = Activate |
| 1102 | TriggerPrice | Fiyat hareketlerine karşı doğrulanacak belirli bir limit fiyat — fiyata ulaşıldığında tetikleme gerçekleşir. |
| 1113 | TriggerTradingSessionID | Emrin tetikleneceği seans tipinin tanımlayıcısı. StateID'ler FIX reference data'da 20032 numaralı tag'de gönderilir. |
| 1103 | TriggerSymbol | Fiyat tetikleyicileri için kullanılan sembol. |
| 1104 | TriggerSecurityID | Fiyat tetikleyicileri için kullanılan menkul kıymetin tanımlayıcısı. |
| 1105 | TriggerSecurityIDSource | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 1107 | TriggerPriceType | Fiyat hareketleri için hangi fiyatın izleneceğini belirler. Geçerli değerler: 1 = Best Offer; 2 = Last Trade; 3 = Best Bid |
| 1109 | TriggerPriceDirection | Tetiklemenin yalnızca yükselen (Up) veya düşen (Down) fiyatlarda gerçekleşip gerçekleşmeyeceğini belirtir. Geçerli değerler: U = Belirtilen tipteki fiyat belirtilen Trigger Price'a veya üstüne çıkarsa tetikle; D = Belirtilen tipteki fiyat belirtilen Trigger Price'a veya altına inerse tetikle |

TriggerPriceType ve TriggerPriceDirection birleştirilerek şu tetikleme talimatları elde edilir: Best Offer + U = Ask ≥; Last Trade + U = Last ≥; Best Bid + U = Bid ≥; Best Offer + D = Ask ≤; Last Trade + D = Last ≤; Best Bid + D = Bid ≤.

*6.6.7.1 Fiyat tetikleme:* Bir emir eşleştiğinde, saklandığında, değiştirildiğinde, süresi dolduğunda veya silindiğinde ve bu durum eşleştirme motorunun En İyi Alış/Satış'ını (BBO) veya Son Eşleşme Fiyatını etkilediğinde, sistem koşulu şimdi karşılanan "tetiklenmemiş" emir olup olmadığını kontrol eder. Fiyat hareketleri aynı emir defterinde veya farklı bir emir defterinde olabilir. Fiyat tetikleyicisi için şu alanlar ayarlanmalıdır: TriggerType (1100) = Price Movement; TriggerAction (1101) = Activate; TriggerPrice (1102) = tetikleme fiyatı; TriggerSymbol (1103) VEYA TriggerSecurityID + TriggerSecurityIDSource; TriggerSecurityID (1104) = tetikleyen enstrüman; TriggerSecurityIDSource (1105); TriggerPriceType (1107) = fiyat tipi (en iyi alış, en iyi satış veya son işlem); TriggerPriceDirection (1109) = fiyat hareket yönü.

*6.6.7.2 Seans değişikliklerinde tetikleme:* Seans değişikliğine göre tetikleme, bir emri belirtilen bir seansta etkinleştirmek için kullanılabilir. Şu alanlar ayarlanmalıdır: TriggerType (1100) = Specified Trading Session; TriggerAction (1101) = Activate; TriggerTradingSessionID (1113) = emrin etkinleştirileceği seans kimliği. StateTypeID'ler reference data'da 20032 numaralı tag'de gönderilir.

*6.6.7.3 Tetikleme iş akışı:* Bir tetikleyici emir girişte üç farklı duruma geçebilir: (1) Aktifleşmemiş — emir hemen tetiklenmez ve tetiklenmeyi beklemek üzere defterin dışına konur; (2) Hemen aktifleşip hemen gerçekleşir; (3) Hemen aktifleşip deftere konur — emir hemen tetiklenir ancak hemen işlem görmez. Bir tetikleyici emrin durumunu anlamak için istemcinin aldığı Execution Report mesajlarındaki ExecType (150) alanını incelemesi gerekir: ExecType = New (0) emrin girişte etkinleştirilmediği; ExecType = Triggered (L) emrin girişte etkinleştirildiği; ExecType = Trade (F) emrin kısmen veya tamamen gerçekleştiği anlamına gelir. Bir tetikleyici emir gerçekleşmeden önce her zaman etkinleştirilir. (Kaynakta bu bölümde "Figure 1, Trigger Order states and resulting messages" şekli vardır; metin dosyasına aktarılmamıştır.)

*6.6.7.4 Tetikleyici emirlerin iptali:* Tetikleme koşullu bir emir olağan Order Cancel Request mesajıyla iptal edilebilir. Arka uçta tetiklenmiş ve henüz tetiklenmemiş emirler için farklı iptal mesajları olduğundan, tetiklenmemiş bir emrin iptalinin reddedilip emrin defterde kalması olası değildir ama mümkündür. Bu yalnızca bir kez olabilir; iptal gönderilirken emir tetiklenirse. Bu (olası olmayan) durumda aynı emir için ikinci bir iptal gönderilmelidir.

**6.6.8 Açığa satış emirleri [s. 31]:** İşlem sistemi Açığa Satış Emirlerinin (sahip olunmayan bir varlığı, daha sonra daha düşük işlem fiyatından geri alma beklentisiyle satma emirleri) girilmesini destekler. Açığa satış emri girmek için Side (54) = 5 = Short Sell olarak ayarlanır. Bu emre ait sonraki tüm Execution Report mesajlarında (ret mesajları hariç) açığa satış bayrağı ayarlıdır.

**6.6.9 Dengeleyici (Imbalance) emirler [s. 32]:** İşlem sistemi Dengeleyici emirlerin girilmesini destekler. Bir Imbalance emri girmek için New Order Single'da şu bilgiler gönderilmelidir: Tag 59 (TimeInForce) = 9 (At crossing); Tag 44 (Price) = 0; Tag 40 (OrdType) = 1 (Market).

**6.6.10 Aç/Kapat göstergesi (Open Close Indicator) [s. 32]:** OpenCloseIndicator (20199) standart FIX'e bir uzantıdır. Aç/kapat göstergesi, bir işlemden sonraki pozisyonun açılan mı yoksa kapanan bir pozisyon mu olması gerektiğini belirtmek için giriş yönlü emirlerde, cancel replace'lerde veya bildirilen işlemlerde ayarlanabilir. Desteklenen değerler: 0 = Hesap için varsayılan (varsayılan değer) / Değişiklik yok (replace işlemleri için); 1 = Open; 2 = Close; 4 = Hesap için varsayılana ayarla (replace işlemleri için). ÖNEMLİ NOT: 128–255 arası değerlerle sağlanan bacak (per-leg) işlevselliği BIST tarafından desteklenmez. (Kaynakta kombinasyon enstrümanlarında bacak bazlı kullanım ve 20199=133 örneği açıklanır; bu BIST'te desteklenmediği için burada ayrıntılandırılmamıştır.)

**6.6.11 Kapanışta (On Close) emirler [s. 33]:** On close emri girmek için, geçerlilik süresi IOC (FAK) ve emir tipi piyasa olan bir seans durumu emri (SSO) girilir. SSO emirleri Trigger on Session işlevi kullanılarak girilir (bkz. Tetikleme Talimatları). On close emri girmek için New Order Single'da şu bilgiler gönderilmelidir: Tag 59 (TimeInForce) = 3 (IOC); Tag 44 (Price) = 0; Tag 40 (OrdType) = 1 (Market); TriggerType (1100) = Specified Trading Session; TriggerAction (1101) = Activate; TriggerTradingSessionID (1113) = emrin etkinleştirileceği seans kimliği (StateTypeID'ler FIX reference data'da 20032 numaralı tag'de gönderilir). NOT: On close emirleri düzgün yürütülmesi için off-hour niteliği olmadan gönderilmelidir.

### 6.7 Ret mesajlarında eksik zorunlu alanlar [s. 33]

Arka ucun çalışma biçimi nedeniyle, standart FIX 5.0 SP2'de uygulama seviyesi retler için zorunlu olan bazı alanlar eksik olacaktır. Emir retleri (Execution Report – reject) için şu zorunlu alan bulunmaz: Side (54). Ayrıca Execution Report – reject mesajlarında Symbol (55) alanı "[N/A]" olarak ayarlanır.

### 6.8 Business Message Reject [s. 33]

Business Message Reject, diğer ret mesajlarının kullanılamadığı durumlarda (ör. işlem kapalı olduğu veya yetkilendirme yetersiz olduğu için gelen mesajın işlem motoruna ulaşmaması) retleri bildirmek için kullanılır (mesaj ayrıntıları 6.10.18). NOT: Kullanıcı, bu mesajı diğer tüm iş mesajlarına alternatif bir yanıt olarak almaya hazır olmalıdır. NOT: Mesaj sayısı hız (pacing) sınırına ulaşırsa sonraki tüm mesajlar Business Message Reject ile reddedilir.

### 6.9 Mesaj ayrıntı listelerinin yorumlanması [s. 34]

**6.9.1 Required (Req'd) sütunu:** 'Y' alanın standart FIX'te zorunlu olduğunu (ve tabii bu uygulamada da); 'Q' alanın standart FIX'te zorunlu olmadığı hâlde bu uygulamada zorunlu olduğunu; hiçbir giriş olmaması alanın isteğe bağlı olduğunu gösterir.
**6.9.2 Tekrarlı gruplar:** FIX tekrarlı gruplarındaki alanlar mesaj listelerinde okla (→) işaretlenir (örnek: Parties bloğu; iç içe gruplar da görülebilir). NumInGroup alanındaki (NoPartyIDs, NoPartySubIDs) Req'd bayrağına dikkat edin: varsa (Y veya Q) tüm tekrarlı grubun her zaman mevcut olacağı anlamına gelir. Tekrarlı gruptaki tek bir alanda Q veya Y olması, tekrarlı grup mevcutsa o alanın her zaman mevcut olacağı anlamına gelir.

### 6.10 Mesaj Ayrıntıları [s. 34–67]

#### 6.10.1 New Order Single — Borsaya giriş yönlü (in) — MsgType = D [s. 34–37]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = D |
| 11 | ClOrdID | Y | İstemci tarafından belirlenen benzersiz tanımlayıcı. |
| 453 | NoPartyIDs | | İsteğe bağlı tekrarlı grup; vekil (on behalf of) işlemler ve/veya isteğe bağlı AFK/Custodian tanımlayıcısı için kullanılır. |
| → 448 | PartyID | Q | Taraf tanımlayıcısı. |
| → 447 | PartyIDSource | Q | Geçerli değerler: D = Özel/Özel kod (Proprietary/Custom code) |
| → 452 | PartyRole | Q | Belirtilen PartyID'nin rol tipi. Geçerli değerler: 1 = Executing Firm; 12 = Executing Trader; 14 = Giveup Clearing Firm; 28 = Custodian; 83 = Clearing Account |
| 1 | Account | Q | İstemci tarafından ayarlanan ve piyasa tarafından geri yansıtılan zorunlu aktarım alanı. |
| 528 | OrderCapacity | Q | Hesap tipi. Geçerli değerler: A = Customer (müşteri); P = Principal (portföy); F = Fund Order (fon emri); C = Primary Dealer Corp; K = Primary Dealer Govt; O = Portfolio Mgmt Company; T = Investment Trust; Y = Other Fund; S = Special Client; N = Other 2; D = Other 3. NOT: OrderCapacity türev piyasasında kullanılmaz. |
| 111 | MaxFloor | | Gizli (hidden) emirler için. |
| 21 | HandlInst | | Aracı kurumun işlem salonundaki emir işleme talimatları. Geçerli değerler: 1 = Otomatik yürütme emri, özel, aracı müdahalesi yok (varsayılan değer) |
| 18 | ExecInst | | Geçerli değerler: G = All or None (AON) |
| 55 | Instrument/Symbol | | OMNet kısa adı. Symbol veya SecurityID+SecurityIDSource ayarlanmalıdır. |
| 48 | Instrument/SecurityID | | Orderbook ID. |
| 22 | Instrument/SecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 54 | Side | Y | Geçerli değerler: 1 = Buy; 2 = Sell; 5 = Sell Short |
| 60 | TransactTime | Y | |
| 38 | OrderQtyData/OrderQty | Y | |
| 40 | OrdType | Y | Geçerli değerler: 1 = Market; 2 = Limit; K = Market With Left Over as Limit (gerçekleşmeyen miktarı son fiyattan limit emre dönüşen piyasa emri) |
| 44 | Price | | Limit emirleri için zorunlu. |
| 21101 | UnderlyingColPx | | Teminat Fiyatı — Special Repo Piyasalarında limit emirler için zorunlu. |
| 1100 | TriggeringInstruction/TriggerType | | Neyin emir değişikliğini tetikleyeceğini belirler. Geçerli değerler: 2 = Specified Trading Session; 4 = Price Movement |
| 1101 | TriggeringInstruction/TriggerAction | | Tetikleyici gerçekleştiğinde yapılacak eylem. Geçerli değerler: 1 = Activate |
| 1102 | TriggeringInstruction/TriggerPrice | | Fiyat hareketlerine karşı doğrulanacak belirli bir limit fiyat. |
| 1113 | TriggeringInstruction/TriggerTradingSessionID | | Emrin tetikleneceği seansın tanımlayıcısı. |
| 1103 | TriggeringInstruction/TriggerSymbol | | Fiyat tetikleyicileri için kullanılan sembol. |
| 1104 | TriggeringInstruction/TriggerSecurityID | | Fiyat tetikleyicileri için kullanılan menkul kıymetin tanımlayıcısı. |
| 1105 | TriggeringInstruction/TriggerSecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 1107 | TriggeringInstruction/TriggerPriceType | | İzlenecek fiyat tipi. Geçerli değerler: 1 = Best Offer; 2 = Last Trade; 3 = Best Bid |
| 1109 | TriggeringInstruction/TriggerPriceDirection | | Geçerli değerler: U = fiyat Trigger Price'a veya üstüne çıkarsa; D = fiyat Trigger Price'a veya altına inerse |
| 59 | TimeInForce | Q | Geçerli değerler: 0 = Day; 1 = Good Till Cancel (GTC); 3 = Immediate Or Cancel (IOC); 4 = Fill Or Kill (FoK); 6 = Good Till Date (GTD); 9 = At Crossing; S = Good till end of session (GTS) |
| 386 | NoTradingSessions | | Yalnızca GTS ve Off-hour emirleri için ayarlanır. Yalnızca 1 olabilir. |
| → 336 | TradingSessionID | Q | Emir vadesinin durum tipi. TimeInForce = GTS ise koşullu olarak zorunludur. Geçerli değerler: GTS için StateTypeId veya Off-hour emirleri için 'A'. |
| 432 | ExpireDate | | Emrin sona erme tarihi. TimeInForce = GTD ise koşullu olarak zorunludur. |
| 70 | AllocID | | İstemci tarafından ayarlanan ve piyasa tarafından geri yansıtılan isteğe bağlı aktarım alanı. |
| 1089 | MatchIncrement | | Ayarlanırsa doğru blok lot/küsurat lot büyüklüğünde olmalıdır, aksi hâlde reddedilir. |
| 1094 | PegPriceType | | Geçerli değerler: 2 = Mid-price peg (orta nokta) |
| 20199 | OpenCloseIndicator | | Açık/kapalı göstergesi: bir işlemden sonraki pozisyonun açılan mı kapanan mı olacağını denetler. 0 = Hesap için varsayılan (varsayılan); 1 = Open; 2 = Close |
| 21114 | SMP Level | | SMP kapsamını belirtir. Geçerli değerler: 1 = Üye içinde; 2 = Üyeler arasında |
| 21115 | SMP Method | | Olası bir eşleşmenin önlenmesi durumunda işlem sisteminin yapacağı eylem. Geçerli değerler: 1 = Agresif emri iptal et; 2 = Pasif emri iptal et; 3 = Her ikisini iptal et |
| 21116 | SMP ID | | 3 karakterli alfanümerik değer; emrin Emrimle Eşleşmesin özelliğine uygun olduğunu belirtir. SMP Level = 1 ise üye, SMP Level = 2 ise Borsa tarafından atanır. |
| | Standard Trailer | Y | |

#### 6.10.2 Order Cancel Request (in) — MsgType = F [s. 38]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = F |
| 41 | OrigClOrdID | Y | OrderID kullanılıyorsa "NONE" olarak ayarlanır. |
| 37 | OrderID | | OrigClOrdID yerine kullanılması önerilir. |
| 11 | ClOrdID | Y | İstemci tarafından belirlenen benzersiz tanımlayıcı. |
| 453 | NoPartyIDs | | İsteğe bağlı tekrarlı grup; yalnızca vekil (on behalf of) işlemler için. |
| → 448 | PartyID | Q | Taraf tanımlayıcısı. |
| → 447 | PartyIDSource | Q | Geçerli değerler: D = Özel/Özel kod |
| → 452 | PartyRole | Q | Geçerli değerler: 1 = Executing Firm; 12 = Executing Trader |
| 55 | Instrument/Symbol | | OMNet kısa adı. Symbol veya SecurityID+SecurityIDSource ayarlanmalıdır. |
| 48 | Instrument/SecurityID | | Orderbook ID. |
| 22 | Instrument/SecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 54 | Side | Y | Geçerli değerler: 1 = Buy; 2 = Sell; 5 = Sell Short |
| 60 | TransactTime | Y | |
| 38 | OrderQtyData/OrderQty | Y | NOT: FIX'te zorunlu ancak sistem tarafından yok sayılır. Kısmi iptal desteklenmez. |
| | Standard Trailer | Y | |

#### 6.10.3 Order Cancel Replace Request (in) — MsgType = G [s. 38–40]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = G |
| 37 | OrderID | | OrigClOrdID yerine kullanılması önerilir. |
| 453 | NoPartyIDs | | İsteğe bağlı tekrarlı grup; vekil işlemler ve/veya isteğe bağlı AFK/Custodian tanımlayıcısı için. |
| → 448 | PartyID | Q | Taraf tanımlayıcısı. |
| → 447 | PartyIDSource | Q | Geçerli değerler: D = Özel/Özel kod |
| → 452 | PartyRole | Q | Geçerli değerler: 1 = Executing Firm; 12 = Executing Trader; 14 = Giveup Clearing Firm; 28 = Custodian; 83 = Clearing Account |
| 41 | OrigClOrdID | Y | Değiştirilecek/iptal edilecek emrin ClOrdID'si. OrderID kullanılıyorsa "NONE". |
| 11 | ClOrdID | Y | İstemci tarafından belirlenen benzersiz tanımlayıcı. |
| 1 | Account | | İstemci tarafından ayarlanan ve piyasa tarafından geri yansıtılan aktarım alanı. |
| 528 | OrderCapacity | | Hesap tipi (6.10.1'deki değerler). NOT: OrderCapacity türev piyasasında kullanılmaz. |
| 70 | AllocID | | İsteğe bağlı aktarım alanı. |
| 111 | MaxFloor | | Gizli emirler için. |
| 21 | HandlInst | | Geçerli değerler: 1 = Otomatik yürütme emri (varsayılan) |
| 18 | ExecInst | | Geçerli değerler: G = All or None (AON) |
| 55 | Instrument/Symbol | | OMNet kısa adı. |
| 48 | Instrument/SecurityID | | Orderbook ID. |
| 22 | Instrument/SecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 54 | Side | Y | FIX'te zorunlu, ancak değiştirilmesine izin verilmez. Geçerli değerler: 1 = Buy; 2 = Sell; 5 = Sell Short |
| 60 | TransactTime | Y | |
| 38 | OrderQtyData/OrderQty | Y | |
| 40 | OrdType | Y | FIX'te zorunlu, ancak değiştirilmesine izin verilmez. Geçerli değerler: 1 = Market; 2 = Limit |
| 44 | Price | | Limit emirleri için zorunlu. |
| 21101 | UnderlyingColPx | | Teminat Fiyatı — Special Repo Piyasalarında limit emirler için zorunlu. |
| 59 | TimeInForce | | Geçerli değerler: 0 = Day; 1 = GTC; 3 = IOC; 4 = FoK; 6 = GTD; 9 = At Crossing; S = GTS |
| 432 | ExpireDate | | Emrin sona erme tarihi. TimeInForce = GTD ise koşullu olarak zorunludur. |
| 20199 | OpenCloseIndicator | | 0 = Değişiklik yok; 1 = Open; 2 = Close; 4 = Hesap için varsayılana ayarla |
| | Standard Trailer | Y | |

#### 6.10.4 Order Cancel Reject (out) — iptal isteği reddi — MsgType = 9, CxlRejResponseTo = 1 [s. 40]

Amaç: Order Cancel Request'in reddi. 6.10.5 (Order Cancel Reject – Cancel Replace; CxlRejResponseTo = 2) aynı alanlara sahiptir; yalnızca `OrdStatus`'a 5 = Replaced eklenir ve `CxlRejResponseTo` değeri 2 = Order cancel/replace request'tir.

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = 9 |
| 37 | OrderID | Y | Cancel'dan; CxlRejReason = 1 (Unknown order) ise OrderID "NONE" olarak ayarlanır. |
| 11 | ClOrdID | Y | İstemci tarafından belirlenen benzersiz tanımlayıcı. |
| 41 | OrigClOrdID | Y | Değiştirilecek/iptal edilecek emrin ClOrdID'si. FIX ile girilmemiş emirler veya emir bulunamadıysa "NONE". |
| 39 | OrdStatus | Y | Geçerli değerler: 0 = New; 1 = Partially filled; 2 = Filled; 4 = Canceled; 8 = Rejected; 9 = Suspended; C = Expired (6.10.5'te ek olarak 5 = Replaced) |
| 60 | TransactTime | Q | |
| 434 | CxlRejResponseTo | Y | Geçerli değerler: 1 = Order cancel request (6.10.5'te 2 = Order cancel/replace request) |
| 102 | CxlRejReason | | Geçerli değerler: 0 = Too late to cancel (iptal için çok geç); 1 = Unknown Order; 2 = Broker / Exchange Option; 6 = Duplicate ClOrdID (11) received |
| 58 | Text | | Hata açıklaması. |
| | Standard Trailer | Y | |

#### 6.10.6 Execution Report – Order Ack (out) — MsgType = 8, ExecType = 0 veya L [s. 41–44]

Amaç: Emir onayı (Order Acknowledgement). `ExecType = L`, sistem tarafından tetiklenen veya etkinleştirilen emir (Triggered or Activated by the system) demektir.

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = 8 |
| 37 | OrderID | Y | |
| 11 | ClOrdID | Q | İstemci tarafından belirlenen benzersiz tanımlayıcı. |
| 453 | NoPartyIDs | | İsteğe bağlı tekrarlı grup; vekil işlemler ve/veya isteğe bağlı AFK/Custodian tanımlayıcısı için. |
| → 448 | PartyID | Q | Taraf tanımlayıcısı. |
| → 447 | PartyIDSource | Q | Geçerli değerler: D = Özel/Özel kod |
| → 452 | PartyRole | Q | Geçerli değerler: 1 = Executing Firm; 7 = Entering Firm; 12 = Executing Trader; 14 = Giveup Clearing Firm; 28 = Custodian; 36 = Entering Trader; 83 = Clearing Account |
| 17 | ExecID | Y | |
| 150 | ExecType | Y | Geçerli değerler: 0 = New; L = Sistem tarafından tetiklendi veya etkinleştirildi |
| 39 | OrdStatus | Y | Geçerli değerler: 0 = New |
| 1 | Account | | İstemci tarafından ayarlanan ve piyasa tarafından geri yansıtılan isteğe bağlı aktarım alanı. Emirden. |
| 528 | OrderCapacity | | Hesap tipi. Emirden. NOT: OrderCapacity türev piyasasında kullanılmaz. |
| 55 | Instrument/Symbol | Q | OMNet kısa adı. |
| 48 | Instrument/SecurityID | Q | Orderbook ID. |
| 22 | Instrument/SecurityIDSource | Q | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 54 | Side | Y | Geçerli değerler: 1 = Buy; 2 = Sell; 5 = Sell Short |
| 38 | OrderQtyData/OrderQty | Q | |
| 40 | OrdType | Q | Geçerli değerler: 1 = Market; 2 = Limit; K = Market With Left Over as Limit |
| 44 | Price | | |
| 21101 | UnderlyingColPx | | Teminat Fiyatı (Special Repo Piyasaları). |
| 1100–1109 | TriggeringInstruction/… | | TriggerType (1100), TriggerAction (1101), TriggerPrice (1102), TriggerTradingSessionID (1113), TriggerSymbol (1103), TriggerSecurityID (1104), TriggerSecurityIDSource (1105), TriggerPriceType (1107), TriggerPriceDirection (1109); 6.6.7'deki ile aynı değerler. |
| 336 | TradingSessionID | | Geçerli değerler: Off-hour emirleri için 'A'. |
| 59 | TimeInForce | Q | Geçerli değerler: 0 = Day; 1 = GTC; 3 = IOC; 4 = FoK; 6 = GTD; 9 = At Crossing; S = GTS |
| 432 | ExpireDate | | Emrin sona erme tarihi. TimeInForce = GTD ise koşullu olarak zorunludur. |
| 18 | ExecInst | | Geçerli değerler: G = All or None (AON) |
| 151 | LeavesQty | Y | Emirde OrderQty'ye eşit olacaktır. |
| 14 | CumQty | Y | Order Ack'te 0 olacaktır. |
| 6 | AvgPx | Y | Not: Her zaman 0.0'dır. |
| 60 | TransactTime | Q | |
| 70 | AllocID | | İsteğe bağlı aktarım alanı. |
| 797 | CopyMsgIndicator | | Drop Copy mesajlarında 'Y' olarak ayarlanır. |
| 1089 | MatchIncrement | | Blok büyüklüğü (Block Size). |
| 1094 | PegPriceType | | Geçerli değerler: 2 = Mid-price peg |
| 111 | MaxFloor | | Gizli emirler için. Şu anda gösterilen miktarı içerir. |
| 119 | SettlCurrAmt | | Emir değeri. |
| 20015 | OptionPremiumAmt | | Prim değeri. |
| 20199 | OpenCloseIndicator | | 0 = Hesap için varsayılan (varsayılan); 1 = Open; 2 = Close; 4 = Hesap için varsayılana ayarla |
| 21114 | SMP Level | | 1 = Üye içinde; 2 = Üyeler arasında |
| 21115 | SMP Method | | 1 = Agresif emri iptal et; 2 = Pasif emri iptal et; 3 = Her ikisini iptal et |
| 21116 | SMP ID | | 3 karakterli alfanümerik; SMP Level = 1 ise üye, 2 ise Borsa atar. |
| | Standard Trailer | Y | |

#### 6.10.7 – 6.10.17 Diğer Execution Report varyantları [s. 45–66] (özet; alanlar 6.10.6 ile büyük ölçüde aynıdır)

| Bölüm | Ad | Tanımlayıcı (Identified by) | Amaç ve farklar |
|---|---|---|---|
| 6.10.7 | Execution Report – IOC/FoK/Internal Crossing Order Cancel | MsgType = 8 VE ExecType = 4 VE TimeInForce = 3 VEYA 4 | IOC veya FOK emrinin iptali. Hemen gerçekleşmeleri izleyen dizide her zaman son gönderilir. Emir cross trade zaman aşımı nedeniyle iptal edilirse mesaj tag 58'de "Internal crossing delete" metniyle gönderilir. ExecType = 4 (Canceled); OrdStatus = 4 (Canceled); TimeInForce = 3 veya 4; LeavesQty 0; AvgPx 0.0; PartyRole'a 1001–1007 değerleri (Confirmed by Firm … Give-up Account) eklenir. |
| 6.10.8 | Execution Report – Market to Limit Order Cancel | MsgType = 8 VE ExecType = 4 VE OrdType = K | Market to Limit emri hemen yürütülemezse (karşı tarafta emir yok) gönderilir. OrdType = K; ExecType = 4; OrdStatus = 4; LeavesQty 0; CumQty 0; AvgPx 0.0. |
| 6.10.9 | Execution Report – Order Reject | MsgType = 8 VE ExecType = 8 | Emir reddi. NOT: Bu mesajda zorunlu Side (54) alanı bulunmaz; Symbol alanı [N/A] olarak ayarlanır. OrderID "NONE"; ExecType = 8 (Rejected); OrdStatus = 8 (Rejected); OrdRejReason (103) = 0 (Broker / Exchange option); LeavesQty 0; CumQty 0; AvgPx 0.0; Text (58) hata mesajı. |
| 6.10.10 | Execution Report – Cancel Replace Ack | MsgType = 8 VE ExecType = 5 | Order Cancel Replace Request onayı. ExecType = 5 (Replaced); OrdStatus değerleri: 0 = New; 1 = Partially Filled; 2 = Filled; 4 = Canceled; OrigClOrdID (41) mevcuttur; OrderID Genium INET order_number'dır. |
| 6.10.11 | Execution Report – Cancel Ack | MsgType = 8 VE ExecType = 4 | Order Cancel Request onayı. ExecType = 4; OrdStatus = 4; LeavesQty Cancel Ack'te 0; Text (58) serbest biçimli metin; OrigClOrdID FIX ile girilmemiş emirler için ayarlanmaz. |
| 6.10.12 | Execution Report – Unsolicited Cancel | MsgType = 8 VE ExecType = 4 VE ExecRestatementReason = 8 VEYA 4 | Emir FIX dışında (başka protokolle veya piyasa tarafından) iptal edildi. ExecRestatementReason (378) = 8 (Market/Exchange option) (veya 4); Text (58) emrin neden iptal edildiğine ilişkin bilgi. |
| 6.10.13 | Execution Report – Unsolicited Order Update | MsgType = 8 VE ExecType = D VE ExecRestatementReason = 8 | Emir FIX dışında (başka protokolle veya piyasa tarafından) güncellendi. |
| 6.10.14 | Execution Report – Restatement | MsgType = 8 VE ExecType = D VE ExecRestatementReason = 1 | Geceyi geçen (GTC/GTD) emirlerin sabah yeniden bildirimi. ExecRestatementReason = 1 (GT renewal / restatement; kurumsal işlem yok). |
| 6.10.15 | Execution Report – Fill | MsgType = 8 VE ExecType = F | Emir gerçekleşmesi. ExecType = F (Trade); OrdStatus = 2 = Filled (kaynakta yalnızca bu değer listelenmiştir); ek alanlar: 880 TrdMatchID (Q) — eşleştirme motorunun atadığı Match ID; 32 LastQty (Q) — (son) gerçekleşmenin miktarı; 31 LastPx (Q) — (son) gerçekleşmenin fiyatı; 151 LeavesQty — daha fazla yürütme için açık miktar; 14 CumQty — kotasyon gerçekleşmelerinde 0 olacaktır; 6 AvgPx — her zaman 0.0. |
| 6.10.16 | Execution Report – Order Suspended | MsgType = 8 VE ExecType = 9 | Emir askıya alındı. ExecType = 9 (Suspended); OrdStatus = 9 (Suspended). (Duraklatılan emirler için bkz. 6.5.6: OrdStatus = 9 ve Text = "Paused".) |
| 6.10.17 | Execution Report – Expired | MsgType = 8 VE ExecType = C | Süre doldu. Ayrıntılar için Order Expiry bölümüne bakın. Bir GTD emri kurumsal işlem nedeniyle iptal edilirse Expired işlemi gönderilir. ExecType = C (Expired); OrdStatus = C (Expired). |

#### 6.10.18 Business Message Reject (out) — MsgType = j [s. 67]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = j |
| 45 | RefSeqNum | | Reddedilen mesajın MsgSeqNum değeri. |
| 372 | RefMsgType | Y | Başvurulan FIX mesajının MsgType değeri. |
| 380 | BusinessRejectReason | Y | Geçerli değerler: 0 = Other; 1 = Unknown ID; 2 = Unknown Security; 3 = Unsupported Message Type; 4 = Application not available; 5 = Conditionally required field missing |
| 58 | Text | | Hatayı açıklayan serbest biçimli metin. |
| | Standard Trailer | Y | |

## 11 Ek A — NASDAQ OMX Uzantıları [s. 132–133]

Bu bölüm çözümün standart FIX 5.0 SP2'den nasıl saptığını ayrıntılandırır. Sapma tipleri: eklenen alanlar, eklenen enum değerleri, alan tanımı değiştirilenler.

**11.1 Eklenen alanlar**

| Tag | Alan adı | Eklendiği mesaj(lar) | Tip / açıklama |
|---|---|---|---|
| 20034 | ComboMatchID | Execution Report | Match ID |
| 21060 | Fineness | Security Definition Request | Price |
| 20199 | OpenCloseIndicator | New Order Single; Order Cancel Replace Request; Execution Report; Trade Capture Report | int |
| 20200 | LegTrdMatchID | Execution Report | Match ID |
| 20015 | OptionPremiumAmt | Execution Report; Trade Capture Report | Amt |
| 21100 | LastUnderlyingPx | Trade Capture Report | Price |
| 21101 | UnderlyingColPx | New Order Single; Order Cancel Replace Request; Execution Report | Price |
| 21102 | DealNumber | Trade Capture Report | int |
| 20009 | OrderReference | Trade Capture Report | String |
| 20014 | ExternalTradeFeeType | Allocation Report | String |
| 20002 | DaysToPwdExpiry | Logon | int |
| 21103 | TradeReportState | Trade Capture Report | int |
| 21104 | TradeReportSubState | Trade Capture Report | int |
| 21105 | TradeReportInstrType | Trade Capture Report | int |
| 21106 | TradeReportReason | Trade Capture Report | int |
| 21107 | AuthorizationState | Trade Capture Report | int |
| 21108 | AffirmationState | Trade Capture Report | int |
| 21109 | DeliveryUnit | Trade Capture Report | int |
| 21110 | OrigClearingBusinessDate | Trade Capture Report | LocalMktDate |
| 21113 | DeferredPublicationTime | Security Definition | int |

**11.2 Eklenen enumerasyonlar:** SessionStatus alanına: 100 = Invalid BodyLength, session suspended; 101 = HeartBt interval too low. **11.3 Alan tanımı değişiklikleri:** Yok.

## 12 Ek B — Alan Uzunluğu Sınırları [s. 134]

| Tag | Alan adı | En büyük uzunluk | Açıklama |
|---|---|---|---|
| 11 | ClOrdID | 20 | |
| 41 | OrigClOrdID | 20 | |
| 117 | QuoteID | 20 | |
| 320 | SecurityRequestID | 20 | |
| 70 | AllocID | 15 | |
| 1 | Account | 15 | |
| 79 | AllocAccount | 10 | |
| 448 | PartyID | 7 | PartyRole = Executing Firm veya Contra Firm olduğunda |
| 448 | PartyID | 3 | PartyRole = Custodian olduğunda |
| 524 | NestedPartyID | 7 | |
| 757 | Nested2PartyID | 7 | |
| 571 | TradeReportID | 20 | |
| 572 | TradeReportRefID | 20 | |
| 881 | SecondaryTradeReportRefID | 20 | |
| 923 | UserRequestID | 20 | |
| 925 | NewPassword | 32 | |

## 13 Ek C — İşlem Tipleri (Trade Types, TrdType 828) [s. 135–136]

TrdType (828) alanının alabileceği tüm değerlerin tanımları (kaynaktaki adlar aynen; Pay Piyasası ve özel işlem bildirimi ile ilgili olanlar 501, 514, 515, 516'dır):

| Değer | Açıklama (kaynak) |
|---|---|
| 501 | EQWS - PAY PIYASASI TOPTAN SATISLAR |
| 514 | ELT0 - SON ISLEM FIYATI |
| 515 | EQNS - PAY PIYASASI TS TAKAS DISARIDA |
| 516 | ELT6 - SON ISLEM FIYATI +/- %6 |
| 621 | DIXF - BIST30 VIS OZEL EMIR |
| 622 | DIXO - BIST30 OPSIYON OZEL EMIR |
| 628 | DUSF - USDTRY VIS OZEL EMIR |
| 629 | DEUR - EURTRY VIS OZEL EMIR |
| 630 | DEUD - EURUSD VIS OZEL EMIR |
| 631 | DUSO - USDTRY OPSIYON OZEL EMIR |
| 632 | DXTR - GRAM ALTIN VIS OZEL EMIR |
| 633 | DXUS - ONS ALTIN VIS OZEL EMIR |
| 636 | DNUL - OZEL EMIR GIRISI YOK |
| 637 | DEL – AYLIK ELEKTRIK VIS OZEL EMIR |
| 638 | DSAS - SASX10 VIS OZEL EMIR |
| 643 | DONF - TLREF VIS OZEL EMIR |
| 645 | DRUB - RUBTRY VIS OZEL EMIR |
| 647 | DCNH - CNHTRY VIS OZEL EMIR |
| 678 | DPUF - FIZIKI TES. USDTRY VIS OZEL EMIR |
| 679 | DPUO – FIZIKI TES. USDTRY OPS OZEL EMIR |
| 684 | DELC – CEYREK YILLIK ELEKTRIK VIS OZEL EMIR |
| 685 | DGUD – GBPUSD VIS OZEL EMIR |
| 688 | DXLB – BIST LIKIT BANKA VIS OZEL EMIR |
| 689 | DX10 – BIST BD LIKIT 10 VIS OZEL EMIR |
| 700 | DGUS - ONS GUMUS VIS OZEL EMIR |
| 701 | DFPI – FIZIKI T. DIBS VIS OZEL EMIR |
| 702 | DXCU – TON BAKIR VIS OZEL EMIR |
| 703 | DXPD - ONS PALLADIUM VIS OZEL EMIR |
| 704 | DXPT - ONS PLATINUM VIS OZEL EMIR |
| 705 | DXSD - BIST SURDUR.25 VIS OZEL EMIR |
| 706 | DEF - PAY VIS OZEL EMIR |
| 707 | DEO - PAY OPSIYON OZEL EMIR |
| 812 | FTR1 - BAP TRADE REPORT – CLEARED |
| 818 | FTR2 - BAP TRADE REPORT - NON-CLEARED |
| 821 | FTRC - BAP TR - CLEARED - 400M |
| 831 | FC1K - BAP TR - CLEARED - 1k |
| 832 | FC10 - BAP TR - CLEARED - 10k |
| 833 | FC50 - BAP TR - CLEARED - 50k |
| 834 | FCHK - BAP TR - CLEARED - 100k |
| 835 | FC1M - BAP TR - CLEARED - 1M |
| 836 | FCKA - BAP TR - CLEARED – 100M |
| 837 | FCKX - BAP TR - CLEARED - 5m |
| 838 | FXAC - BAP TR - CLEARED - GOLD |
| 841 | FN1K - BAP TR - NON-CLEARED - 1k |
| 842 | FN10 - BAP TR - NON-CLEARED - 10k |
| 843 | FN50 - BAP TR - NON-CLEARED - 50k |
| 844 | FNHK - BAP TR - NON-CLEARED - 100k |
| 845 | FN1M - BAP TR - NON-CLEARED - 1M |
| 848 | FXAN - BAP TR - NON-CLEARED - GOLD |
| 901 | KSNI – PMD (KMP) TR CLEARED IN (On Exchange) |
| 902 | KSNO – PMD (KMP) TR CLEARED OUT (Off Exch.) |
| 903 | KSSI – BORSA ICI (NS) |
| 904 | KSSO – BORSA DISI (NS) |

## 14 Ek D — İkincil İşlem Tipleri (Secondary Trade Types) [s. 137–138]

| Değer | Açıklama |
|---|---|
| 0 | Dahili kullanım. Doğrudan takas alt sistemine bildirilen işlemler. |
| 1 | Sistem tarafından otomatik eşleştirildi. |
| 2 | Sistem tarafından manuel eşleştirildi. |
| 3 | Borsa dışında eşleştirildi, farklı katılımcılar. |
| 4 | Borsa dışında eşleştirildi, farklı katılımcılar, Borsa tarafından kaydedildi. |
| 5 | Borsa dışında eşleştirildi, tek katılımcı. |
| 6 | Borsa dışında eşleştirildi, tek katılımcı, Borsa tarafından kaydedildi. |
| 7 | Kombinasyon emri, Borsa tarafından elektronik eşleştirildiğinde başka bir kombinasyon emriyle eşleşti. |
| 8 | Swap Box enstrümanında işlem. |
| 9 | Elektronik eşleşti, üye içi. |
| 10 | Swap Box enstrümanında işlem, üye içi. |
| 11 | Piyasa kapanışından sonra, sistem dışı, farklı aracılar. |
| 12 | Piyasa kapanışından sonra, sistem dışı, farklı aracılar, Borsa tarafından kaydedildi. |
| 13 | Piyasa kapanışından sonra, sistem dışı, tek aracı. |
| 14 | Piyasa kapanışından sonra, sistem dışı, tek aracı, Borsa tarafından kaydedildi. |
| 15 | Dahili oluşturulan temel (basis) işlemi. |
| 16 | Borsa tarafından manuel yapılan geri çevirme (reversing) işlemi. |
| 17 | Temel (basis) işlemi. |
| 18 | İşlem düzeltmesi. |
| 19 | Dahili oluşturuldu. |
| 20 | Bir müzayedenin sonunda yapılan işlem. |
| 21 | Özel fiyat teklifi (private request for quote). |
| 22 | Paket özel fiyat teklifi. |
| 23 | Combo'dan dahili. |
| 24 | TM'den dahili. |
| 25 | Ortalamadan dahili. |
| 26 | Strip'ten dahili. |
| 27 | Delta hedge. |
| 28 | CL bundle işlemi. |
| 32 | Bulletin Board'dan işlem. |
| 33 | Bulletin Board'dan işlem, standart kombinasyon. |
| 34 | Bulletin Board'dan işlem, standart olmayan kombinasyon. |
| 35 | Bulletin Board'dan işlem, standart olmayan kombinasyon. |
| 36 | Özel (tailor-made) kombinasyon. |
| 37 | Standart olmayan kombinasyon. |
| 38 | Borsa dışında, blok işlem imkânı. |
| 39 | Borsa dışında eşleştirildi, kombinasyonlar. |
| 40 | Borsa dışında, blok işlem imkânı. |
| 41 | İşlem fiyatı yok (No Deal Price). |
| 42 | Öncelikli çapraz (Priority crossing). |
| 43 | Kombinasyon, eşleşen tekil bacaklar. |
| 44 | Borsa dışında eşleştirildi, aracı. |
| 53 | Müzakereli işlem ilan panosu. |
| 100–105 | deal_source_imp_rotation (100); deal_source_imp_normal (101); deal_source_imp_out_of_sequence (102); deal_source_imp_cab_trade (103); deal_source_imp_combo_single (104); deal_source_imp_combo_mix (105) |
| 110–118 | deal_source_fac_orig_order (110); deal_source_fac_counter_order (111); deal_source_exp_orig_order (112); deal_source_exp_counter_order (113); deal_source_unsolicited_order (114); deal_source_solicited_order (115); deal_source_block_order (116); deal_source_trade_rep (117); deal_source_trade_rep_no_settl (118) |
| 122 | deal_source_imp_combo_buy_write |
| 128 | Ortalama Fiyat İşlemi (Average Price Trade) sonucu oluşan işlem. |
| 129 | Ortalama Fiyat İşleminde oluşturulan ara işlem. |
| 131 | İşlem devri (Trade transfer). |
| 132 | Misclear. |
| 133 | Fiziki karşılığı olan takas (Exchange for physical, EFP). |
| 134 | Spread işlemi. |
| 135 | Ortalama fiyat sistemi (APS). |
| 136 | Fiyatsız düzeltme. |
| 137 | Fiyatlı düzeltme. |
| 138 | CTrade'de gerçekleştirilen işlem. |
| 139 | Çapraz ürün netleştirmesi (Cross product netting). |
| 140 | Taahhütlü işlem iadesi (Committed transaction return). |

---

## Çapraz kontrol (kaynakta yok; çevirenin gözlemi)

- Bölüm 6.10.1 (39 tag), 6.10.2 (13), 6.10.3 (25) ve 6.10.6 (47 tag) tablolarındaki tag numaraları PDF metninden çıkarılan listelerle karşılaştırılmıştır: ilk üçünde fark yoktur; 6.10.6'da PDF'teki 1101–1113 tetikleme tag'leri (8 adet) tabloda tek satırda (`1100–1109`) birleştirilmiştir, başka fark yoktur.
- Genium INET FIX'te `OrderID` yalnızca emir defteri ve taraf başına benzersizdir (6.6.1.2); bu, ITCH'teki `Order ID` kuralıyla aynıdır. `TrdMatchID` 64 bitlik ikili eşleşme kimliğidir (16 baytlık onaltılık dizge olarak kodlanır); ITCH `Match ID` 8 bayttır, OUCH `Match ID` 12 bayttır.
- Prosedür 5.6.5 (s. 94) "marj dışına çıkan emir iptal edilir" derken bu belge (6.5.6) duraklatma ve özgün öncelikle yeniden etkinleştirme anlatır; çelişki `../kurallar/04-surekli-islem.md` açık sorularında işaretlidir.
