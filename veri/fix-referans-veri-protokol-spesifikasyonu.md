# Genium INET FIX Reference Data Protokol Spesifikasyonu (Türkçe çeviri)

Kaynak: `kaynaklar/genium-inet-fix-reference-data-protocol-specification.pdf` — "FIX for BIST Phase 2 — REFERENCE DATA", kapakta sürüm 1.0.40 (2025-11-05), sayfa altbilgilerinde "GENIUM INET FIX REFERENCE DATA VERSION 1.0.30" yazar (kaynakta tutarsızlık; revizyon geçmişi 1.0.40'a kadar gider), 54 sayfa. Etiket: "HALKA AÇIK/PUBLIC". Telif: Nasdaq, Inc.
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir. FIX tag numaraları, alan adları, değerler ve sabitler çevrilmeden bırakılmıştır. Sayfa numaraları PDF sayfa numarasıdır.
Kapsam: Projeye ilişkin bölümler tam çevrilmiştir: 1 Referanslar, 2 Genel Bakış, 4 Uygulama Sıralaması, 5 Referans Veri (iş akışı ve tüm mesaj tabloları), 6 Ek A, 7 Revizyon geçmişi. **Çevrilmeyenler:** Bölüm 3 (FIX oturum katmanı: Logon, Logout, Sequence Reset, Resend Request, Heartbeat, Test Request, Reject, Standard Header/Trailer mesaj tabloları; standart FIX içeriği, oturum yönetimi) yalnızca özetlenmiştir (aşağıda "3 FIX Oturumu (özet)"). Bu bölümün tabloları gerekirse PDF s. 7–14'ten okunmalıdır.
Doğrulama: Mesaj tablolarındaki tag numaraları, PDF metninden çıkarılan listeyle karşılaştırılmıştır (dosya sonuna bakın). Metin çevirisi sayfa görüntüsüyle karşılaştırılmadı. Kullanıcı doğrulaması: bekliyor.
Proje açısından önemi: Enstrüman başına fiyat adımı (tick) tablosu, lot tipleri ve büyüklükleri, azami emir değeri, güncel fiyat limitleri, baz ve referans fiyat, açığa satış kuralı, ondalık sayısı, bölüm (partition) kimliği ve seans durumları (Trading Session List) bu mesajlarda verilir. Kural dosyaları: `../kurallar/02-fiyat.md`, `07-itch.md`.

---

## 1 Referanslar (References) [s. 5]

[1] FIX 5.0 SP2 Protocol Specification — http://fixprotocol.org/specifications/fix5.0sp2spec

## 2 Genel Bakış (Overview) [s. 5–6]

Bu belge Genium INET Reference Data'ya FIX arayüzünün spesifikasyonunu içerir. Arayüz FIX Protocol 5.0 SP2 standardına dayanır (Financial Information eXchange). Standart hakkında ayrıntılı bilgi FIX spesifikasyon belgesinde bulunur [1].

NASDAQ OMX tarafından uygulanan arayüz, FIX spesifikasyonlarını mümkün olduğunca izler. Çoğu durumda mesajların yapısı ve anlamı standartla aynıdır. Bazı durumlarda protokol, standardın dikkate almadığı işlevleri kapsayacak şekilde genişletilmiştir; bu uzantılar belgede açıkça ayrıntılandırılmıştır. Diğer durumlarda standart belirsizdir veya ayrıntıların taraflar arasında ikili olarak kararlaştırılması gerektiğini belirtir; bu durumlarda olası belirsizliği önlemek için bu kılavuz ayrıntılı bir açıklama sağlar.

Bilgi kaynaklarında tekrarı önlemek için bu belge, standartla tam olarak uyumlu konuların açıklamalarını içermez. Bu nedenle, bu kılavuzda açıkça kapsanmayan her konu için ana bilgi kaynağı standart dokümantasyondur. Bu spesifikasyon FIX standardında belirtileni tekrar etmemeye çalışır; ancak FIX standardı birçok durumda belirli bir piyasa için gerekenden zorunlu olarak daha geneldir. NASDAQ OMX, karışıklığı önlemek için FIX standart spesifikasyonundan sapmaları açık biçimde belirtmeye çalışır.

### 2.1 Desteklenen FIX Mesajları [s. 5–6]

**Yönetsel (administrative) mesajlar:** Logon, Logout, Sequence Reset, Resend Request, Test Request, Heartbeat, Reject.

**Giriş yönlü (inbound) uygulama mesajları:** Application Message Request, Security Definition Request, Security Status Request, Price Reference Request.

**Çıkış yönlü (outbound) uygulama mesajları:** Application Message Request Ack, Security Definition, Security Definition Update Report, Market Definition, Trading Session List, Security Status, Price Reference, AtTheMoneyUpdate.

### 2.2 FIX Üzerinden Referans Verinin Akışı (Streaming Reference Data over FIX) [s. 6]

Genium INET Market Data over FIX, Uygulama Sıralaması (Application Sequencing) kullanılarak uygulanmıştır.

## 3 FIX Oturumu (özet) [s. 7–14]

Oturum katmanı sınırlı standart FIX oturum desteği sunar. Olağan FIX mesaj kurtarma desteklenmez. Resend Request mesajı desteklenir ancak her zaman bir Sequence Reset – gap fill mesajıyla yanıtlanır. Mesaj kurtarma bunun yerine uygulama sıralamasıyla desteklenir (bkz. Bölüm 4).

- **Şirket kimlikleri (CompIDs):** Borsanın şirket kimliği "BI"'dır; giriş yönlü işlemlerde `TargetCompID`, çıkış yönlü işlemlerde `SenderCompID` olarak ayarlanır. İstemcinin şirket kimliği katılımcı kimliğidir (UC ve ardından 5 karakterlik firma kimliği); giriş yönlü işlemlerde `SenderCompID`, çıkış yönlü işlemlerde `TargetCompID` olarak ayarlanır. Bir oturum aynı anda yalnızca iki ana makine arasında etkin olabilir. [s. 7]
- **SenderSubID (tag 50):** Her giriş yönlü iş işleminde kimliği doğrulanmış bir kullanıcıya ayarlanmalıdır; gelen işlemlerdeki SenderSubID, çıkış yönlü işlemlerde `TargetSubID` (tag 57) olarak geri yansıtılır. [s. 7]
- **Kimlik doğrulama:** Kullanıcı, Logon mesajındaki `Username` (553) ve `Password` (554) ile doğrulanır; yeni parola `NewPassword` (925) ile belirlenir; süresi dolmuş parola için sistem `SessionStatus = 8 – Password expired` içeren Logout ile yanıt verir. [s. 7]
- **Heartbeat:** Heartbeat aralığı Logon'da `HeartBtInt` (108) ile müzakere edilir; 10 saniyeden büyük aralıklara izin verilir, önerilen 30 saniyedir; 10 saniyeden küçük değer Logout ile sonuçlanır. [s. 8]
- **Şifreleme:** Desteklenmez. **Karakter kodlaması:** standart US ASCII. [s. 8]
- **Oturum ömrü:** FIX oturum ömrü bir işlem günüyle sınırlıdır; bağlantı kopması veya Logout sonrası sıra numarası 1'den başlar. Standart Resend Request ile mesaj kurtarma desteklenmez; Application Sequencing kullanılır. [s. 9]
- **Yedeklilik (failover):** Her FIX oturumunun en az bir birincil ve bir ikincil ağ geçidi vardır; oturum durumları tam çoğaltılır. İstemci aynı FIX oturumunu aynı anda birden fazla ağ geçidine karşı etkin tutamaz. [s. 9]
- **Required (Req'd) sütunu:** "Y" alanın standart FIX'te de zorunlu olduğunu; "Q" alanın standart FIX'te zorunlu olmadığı hâlde bu uygulamada zorunlu olduğunu gösterir; boş bırakılmışsa alan isteğe bağlıdır. [s. 10]
- Standard Header alanları: 8 BeginString (`FIXT.1.1`), 9 BodyLength, 35 MsgType, 49 SenderCompID, 50 SenderSubID, 56 TargetCompID, 57 TargetSubID, 34 MsgSeqNum, 52 SendingTime (UTC). Standard Trailer: 10 CheckSum. [s. 9–10]
- Logon (MsgType = A): `EncryptMethod` 98 = 0; `HeartBtInt` 108; `ResetSeqNumFlag` 141 = Y (her Logon'da sıra numaralarının sıfırlanması gerekir); `Username` 553; `Password` 554; `NewPassword` 925; `DefaultApplVerID` 1137 = 9 (FIX50SP2). Çıkış yönlü Logon'da ek olarak `SessionStatus` 1409 ve `DaysToPwdExpiry` 20002 bulunur. [s. 11]

## 4 Uygulama Sıralaması (Application Sequencing) [s. 14–18]

### 4.1 Ayrıntılar [s. 14–16]

FIX Application Sequencing, FIX 5.0 ile gelen yeni bir kavramdır. Alıcının hangi içeriğin gönderileceğini belirleyebildiği daha ince taneli abonelik ve kurtarmaya izin verir. Bu nedenle Referans Veri dağıtımı için çok uygundur. Referans verinin etkinleştirilmesi istemci tarafından başlatılır; istemci bir Application Message Request gönderir.

**4.1.1 Application ID'ler:** Referans Veri, Application adı verilen mantıksal akışlara ayrılır. Her Application'a benzersiz bir Application ID atanır; her Application ayrı ayrı sıra numaralandırılır. Giriş yapıldığında istemci her Application için sıra numarasına göre referans verinin etkinleştirilmesini/kurtarılmasını ister. Tüm Application'ların aynı FIX oturumu üzerinden gönderildiğine dikkat edin. Referans Veri için kullanılan Application ID: **R = Reference Data** (tüm referans veri için tek Application ID).

**4.1.2 ApplicationSequenceControl grubu:** Her Referans Veri mesajı ApplicationSequenceControl grubunu içerir. Grup, kurtarmada kullanılan Application ID'yi ve sıra numarasını içerir. Alıcının her application için sıra numarasını izlemesi gerekir.

| Tag | Alan adı | Açıklama |
|---|---|---|
| 1180 | ApplicationSequenceControl/ApplID | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Bu Application ID için sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Bu Application ID için son sıra numarası. Sıradaki boşlukları belirtmek için kullanılır. Alıcı, gereksiz yeniden göndermeleri önlemek için bu alanı kontrol etmelidir. |
| 1352 | ApplicationSequenceControl/ApplResendFlag | Mesaj bir yeniden göndermenin sonucuysa Y olarak ayarlanır. Geçerli değerler: Y = Evet; N = Hayır (alan yoksa varsayılan). Yalnızca tam kurtarmayı destekleyen Application ID'ler için kurtarma yanıtlarında ayarlanır; Referans Veri için tam kurtarma yoktur (bkz. 4.2.1). |

**4.1.3 ApplIDRequestGrp:** Application Message Request mesajında, her Application ID için istenen sıra numaralarını içeren tekrarlı gruptur.

| Tag | Alan adı | Açıklama |
|---|---|---|
| 1351 | ApplIDRequestGrp/NoApplIDs | Bu istekteki Application ID sayısı. |
| 1355 | ApplIDRequestGrp/RefApplID | Application ID. Geçerli değerler: R = Reference Data |
| 1182 | ApplIDRequestGrp/ApplBegSeqNum | İstenen ilk sıra numarası. Kurtarılamayan Application ID'ler için yok sayılır. |
| 1183 | ApplIDRequestGrp/ApplEndSeqNum | Yalnızca 0 (sıfır) kabul edilir (abonelik her zaman etkinleştirilir). |

### 4.2 Referans Verinin İstenmesi ve Kurtarılması [s. 16–18]

Bu çözümde Referans Veri, bir Application Message Request gönderildikten sonra istemciye gönderilir.

**4.2.1 Referans Veri kurtarmasının sınırlamaları:** Application Message Request, kaybolan verinin kurtarılmasını yöneten application sıra numaralarını da içerir. Referans veri için tam kurtarmanın desteklenmediğine dikkat edin. Bir istek, istekteki Application ID'ler için verinin gerçek zamanlı iletiminin etkinleştirilmesiyle sonuçlanır. Gerçek zamanlı veriden önce mevcut durumu veren bir ilk anlık görüntü (snapshot) gelir. İstekte verilen sıra numaralarından bağımsız olarak yanıt her zaman gerçek zamanlı verinin bir sonraki sıra numarasıyla başlar (olası bir snapshot'ın ardından).

**4.2.2 Application Message Request:** Referans veriyi etkinleştirmek ve kaybolan referans veriyi kurtarmak için genel bir istektir. Mesaj, her Application ID için bir girdi içeren tekrarlı bir grup içerir. Mesajda bulunan her Application ID, o tip veri üzerindeki "aboneliği" etkinleştirir (kullanıcının söz konusu veriyi görme yetkisi varsa).
- `ApplEndSeqNum` (1183) kurtarılacak mesaj kümesinin sonunu tanımlar. 0 ise abonelik etkinleştirilir. Bu çözümde bir Application ID için yapılan istek her zaman aboneliği etkinleştirir; `ApplEndSeqNum` 0 olmalıdır. NOT: Aboneliğin her zaman etkinleştirilmesinin sonucu olarak, Logon'dan sonra aynı Application ID için yapılan sonraki istekler ret ile sonuçlanır.
- `ApplBegSeqNum` (1182) gönderilecek mesajların başlangıcını belirler: Kurtarılamayan Application ID'ler için bu değer yok sayılır, gerçek zamanlı mesajlardan önce her zaman bir snapshot gönderilir. Tam kurtarılabilen Application ID'ler için kurtarmanın başlangıç noktasını belirler; `ApplBegSeqNum` son sıra numarasından büyükse kurtarma yapılmadan gerçek zamanlı mesajlar etkinleştirilir.
- NOT: Alıcı, mesaj kaybolduğu her durumda kurtarabilmek için aldığı her Application ID'nin sıra numaralarını izlemelidir. NOT 2: Tüm referans veri için tam mesaj kurtarma mümkün değildir.

Application Message Request'e yanıt Application Message Request Ack'tir. İstek başarılıysa Ack'in ardından Referans Veri mesajları gelir.

**4.2.3 Application Message Request Ack:** `ApplResponseType` (1348) alanı isteğin başarılı olup olmadığını bildirir.
- *Başarılı istekler:* Tamamen başarılı istekte `ApplResponseType = 0` (istek başarıyla işlendi). Ack'ten sonra mesajlar her zaman şu sırayla gönderilir: 1. Market Definitions, 2. Trading Session List, 3. Security Definitions, 4. Security Statuses, 5. Price References. NOT: Bir istek bazı Application ID'ler için başarısız olurken diğerleri için başarılı olabilir.
- *Bir veya daha fazla Application ID için başarısız istekler:* Var olmayan bir application id için istek yapılırsa: `ApplResponseType = 1` (application yok) ve o Application ID için `ApplResponseError = 0`. Daha önce istenmiş bir application için istek yapılırsa: `ApplResponseType = 3` (application için yinelenen istek) ve o Application ID için `ApplResponseError = 3`. `ApplEndSeqNum` (1183) 0'dan farklı ayarlanmış application isteğinde: o Application ID için `ApplResponseError = 1` döner.

## 5 Referans Veri (Reference Data) [s. 19–47]

### 5.1 Giriş [s. 19]

Sistemler Security Definition (menkul kıymet tanımı), Market Definition (piyasa tanımı), Security Status (menkul kıymet durumu), Price Reference (fiyat referansı) ve Trading Session List (işlem seansı listesi) iletimine izin verir. Referans Veriyi etkinleştirmek için alıcı giriş yapar ve bir Application Message Request gönderir. Application Message Request referans veri için genel bir istektir; aynı mesaj kaybolan mesajları kurtarmak için de kullanılır. Başarılı bir Application Message Request bir veya daha fazla Referans Veri mesajı döndürür.

Sistem ayrıca Security Status, Security Definition ve Price Reference için, abonelik kurmadan tek bir enstrümanın bilgisini gönderen istekleri de destekler. İstek dışı göstergesi (unsolicited indicator, tag 325), Security Definition, Security Status veya Price Reference mesajının abonelik kapsamında gönderilip gönderilmediğini belirtir.

### 5.2 Referans Verinin İstenmesi [s. 19]

Bu çözümde Referans Veri, bir Application Message Request verildikten sonra istemciye gönderilir. Tüm Referans Veri mesajları bu tek istekle etkinleştirilir (bkz. Bölüm 4). Sistem ayrıca bir Application Message Request göndererek abonelik kurmadan Security Status, Security Definition ve Price Reference isteklerini de destekler.

### 5.3 Ana İş Akışı [s. 19–20]

**5.3.1 Security Definition:** Sistemdeki her işlem gören menkul kıymet için gün başı referans verisini yayımlamak için kullanılır. Gün içi güncellemeler için Security Definition Update Report kullanılır. Fiyat alanı ve kurumsal işlem (corporate action) güncellemeleri bir Security Definition Update mesajını tetiklemez.

**5.3.2 Market Definition:** Piyasanın yapısı hakkında bilgi yayımlamak için kullanılır. Her işlem gören menkul kıymet bir piyasaya (bir Market Definition mesajıyla temsil edilen) aittir.

**5.3.3 Trading Session List:** Enstrümanların içinde bulunabileceği tüm işlem durumlarını (Trading Sessions) içerir. Her durum için işlem kuralları (Trading Rules), eşleştirme kuralları (Matching Rules) ve izin verilen emir tipleri hakkında bilgi içerir. NASDAQ OMX Uzantısı: `TradingSessionID` (336), durumun gerçek kimliğini içerir. Security Status mesajları da ilgili durumu belirlemek için bu kimliği içerir. Bu, standart FIX'te `TradingSessionID`'nin DAY, HALFDAY gibi enum değerleri içermesinden farklıdır.

**5.3.4 Security Status:** Tüm seans durumu değişikliği bilgisi, Security Status mesajı kullanılarak enstrüman düzeyinde gönderilir. Security Status mesajı ayrıca son işlem fiyatı ve kurumsal işlemler hakkında bilgi de içerir.

**5.3.5 Price Reference:** Bir enstrüman için referans fiyatı, güncel üst ve alt limitleri, baz fiyatı ve bir önceki gün kapanış fiyatını içerir. Fiyat limitleri için hem statik hem güncel (dinamik) fiyat limitleri dikkate alınır; yayımlanan aralık, izin verilen en küçük aralıktır.
Örnek: Statik fiyat limitleri 10,00 – 10,50; dinamik fiyat limitleri 10,10 – 10,60 ise yayımlanan fiyat limitleri 10,10 – 10,50'dir.
Sabit eşleştirme (fixed matching) olduğunda izin verilen bir fiyat limiti aralığı yoktur; bu durumda FIX'te gönderilen üst ve alt limit değerleri baz fiyata eşittir. Fiyat limiti yoksa üst ve alt fiyat limiti tag'leri hiç gönderilmez.

### 5.4 Mesaj Ayrıntıları [s. 21–47]

Required sütunu: Y = standart FIX'te zorunlu; Q = bu uygulamada zorunlu; boş = isteğe bağlı. `→` ile başlayan satırlar tekrarlı grup içindeki alanlardır (`→ →` ikinci düzey).

#### 5.4.1 Security Definition (out) — MsgType = d [s. 21–29]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = d |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. Kaçınılamayan durumlarda bir uygulamanın sıra boşluklu mesaj yayımlamasına izin verir. |
| 55 | Symbol | Q | Kısa ad. |
| 107 | SecurityDesc | | Uzun ad. |
| 48 | SecurityID | Q | Orderbook ID (emir defteri kimliği). |
| 22 | SecurityIDSource | Q | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı (Marketplace-assigned identifier) |
| 167 | SecurityType | | Geçerli değerler: 1 = Options; 2 = Forward; 3 = Futures; 4 = FRA; 5 = Cash; 6 = Payment; 7 = Exchange Rate; 8 = Interest rate swap; 9 = REPO; 11 = Combination; 12 = Guarantee; 13 = OTC general; 14 = Equity warrant; 15 = Security lending; 17 = Strip; 18 = Certificates |
| 541 | MaturityDate | | Vade tarihi. |
| 20041 | NoCouponBlock | | Listelenen kupon sayısı. |
| → 223 | CouponRate | | |
| → 224 | CouponPaymentDate | | |
| 306 | UnderlyingIssuer | | |
| 231 | ContractMultiplier | | "Nominal" birimlerden (ör. sözleşme) toplam birimlere (ör. pay) dönüşüm oranını veya çarpanı belirtir. |
| 1244 | FlexibleIndicator | | Bir menkul kıymetin "standart olmayan" yollarla esnek (flexible) tanımlanıp tanımlanmadığını gösterir. |
| 1242 | FlexProductEligibilityIndictor | | Bir ürünün veya ürün grubunun esnek menkul kıymet oluşturmayı destekleyip desteklemediğini gösterir. |
| 711 | NoUnderlyings | | Dayanak enstrüman sayısı. Bu grup yalnızca enstrüman bir dayanak enstrümandan türetilmişse ayarlanır. NOT: Dayanak bilgisi yalnızca dayanak sistem içinde işlem görüyorsa ayarlanır. |
| → 311 | UnderlyingSymbol | | Dayanak kimliği. |
| → 309 | UnderlyingSecurityID | | Dayanağın Orderbook ID'si. |
| → 305 | UnderlyingSecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| → 318 | UnderlyingCurrency | | Dayanak menkul kıymetin para birimi. |
| 21019 | NoCollUnderlyings | | Teminat (collateral) dayanak enstrüman sayısı. Bu grup yalnızca enstrümanın ilgili bir teminatı varsa ayarlanır. |
| → 21020 | CollUnderlyingSymbol | | Dayanak kimliği. |
| → 21021 | CollUnderlyingSecurityID | | Dayanağın Orderbook ID'si. |
| → 21022 | CollUnderlyingSecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| → 21023 | CollUnderlyingCurrency | | Dayanak menkul kıymetin para birimi. |
| 200 | MaturityMonthYear | | Vade ay ve yılı. Biçim: YYYYMM |
| 201 | PutOrCall | | Opsiyon sözleşmesinin put mı call mı olduğunu gösterir. Geçerli değerler: 0 = Put; 1 = Call |
| 202 | StrikePrice | | Opsiyon için kullanım fiyatı. |
| 15 | Currency | | Kullanım / abonelik / strike fiyatının para birimi. |
| 21001 | InstClassification | | Enstrüman sınıflandırma grubu. |
| 20035 | LastTradingDate | | Son işlem tarihi. |
| 20037 | FirstTradingDate | | İlk işlem tarihi. |
| 20036 | LastTradingTime | | Son işlem saati. |
| 20038 | FirstTradingTime | | İlk işlem saati. |
| 20039 | SectorCode | | Sektör kodu. |
| 20040 | SectorCodeDesc | | Sektör kodu açıklaması. |
| 225 | IssueDate | | |
| 873 | DatedDate | | |
| 454 | NoSecurityAltID | | Alternatif Security tanımlayıcı sayısı. |
| 455 | SecurityAltID | | Uluslararası Menkul Kıymet Tanımlama Numarası (ISIN). |
| 456 | SecurityAltIDSource | | Geçerli değerler: 4 = ISIN numarası |
| 555 | NoLegs | | (Strateji/kombinasyon) enstrümanlar için bacak sayısı. NOT: Yalnızca stratejiler için kullanılır. |
| → 600 | LegSymbol | | Bacak enstrümanın kısa adı. |
| → 602 | LegSecurityID | | Bacak enstrümanın emir defteri kimliği. |
| → 603 | LegSecurityIDSource | | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| → 623 | LegRatioQty | | Bu bacağın miktarının tüm çok bacaklı menkul kıymete oranı. |
| → 624 | LegSide | | Bu bacağın tarafı (çok bacaklı menkul kıymet). Geçerli değerler: B = Tanımlandığı gibi (As Defined); C = Ters (Opposite) |
| 1310 | NoMarketSegments | Q | Menkul kıymetin işlem gördüğü piyasa segmenti sayısı. Her zaman 1'dir. |
| → 1301 | MarketID | Q | Piyasanın adı. |
| → 1300 | MarketSegmentID | | Piyasa Segmenti Kodu. Geçerli değerler: aşağıdaki "Piyasa segmenti kodları" tablosuna bakın. |
| → 1396 | MarketSegmentDesc | | Piyasa segmenti adı. |
| 1205 | NoTickRules | | Fiyat adımı (tick) kuralı sayısı. NOT: Tick kuralları menkul kıymetle ilişkilidir, piyasayla değil. |
| → → 1206 | StartTickPriceRange | | Belirtilen tick artışı için başlangıç fiyat aralığı. |
| → → 1207 | EndTickPriceRange | | Belirtilen tick artışı için bitiş fiyat aralığı. |
| → → 1208 | TickIncrement | | Belirtilen fiyat aralığı için tick artışı. Bir menkul kıymetin kote edilebileceği ve işlem görebileceği geçerli fiyat artışlarını belirtir. |
| 21015 | NoCollTickRules | | Tick kuralı sayısı. NOT: Tanımlıysa, bu menkul kıymet teminat olarak kullanıldığında kullanılan isteğe bağlı tick kuralları. |
| → → 21016 | CollTickIncrement | | Belirtilen fiyat aralığı için tick artışı. |
| → → 21017 | CollStartTickPriceRange | | Belirtilen tick artışı için başlangıç fiyat aralığı. |
| → → 21018 | CollEndTickPriceRange | | Belirtilen tick artışı için bitiş fiyat aralığı. |
| 1234 | NoLotTypeRules | | Lot tipi sayısı. NOT: Lot tipleri menkul kıymetle ilişkilidir, piyasayla değil. |
| → → 1093 | LotType | | Lot tipi. Geçerli değerler: 2 = Round Lot; 3 = Block Lot |
| → → 1231 | MinLotSize | | LotType (1093) ile belirtilen lot tipinin lot büyüklüğü. Bu lot tipi için emir girmek üzere MatchIncrement bu değere ayarlanmalıdır. Emir miktarının bu değerin katı olması gerektiğine dikkat edin. |
| → → 21010 | LotStartPrice | | |
| → → 21012 | LotMaxTradeVol | | Bir menkul kıymet için verilebilecek en yüksek emir miktarı. Yalnızca Normal Limit Fiyatlı Emirler için geçerlidir. |
| → → 21013 | LotMinQty | | Tanımlı fiyat seviyesi için bir emrin en düşük miktarı. |
| → → 21068 | LotMinQuote | | Bir menkul kıymet için verilebilecek en düşük kotasyon miktarı. |
| → → 21069 | LotMaxQuote | | Bir menkul kıymet için verilebilecek en yüksek kotasyon miktarı. |
| → → 21009 | LotDisplayHighQty | | Tanımlı fiyat seviyesi için bir emirde izin verilen en yüksek gösterim (show) miktarı. |
| → → 21014 | LotDisplayLowQty | | Tanımlı fiyat seviyesi için bir emirde izin verilen en düşük gösterim miktarı. |
| → → 21011 | LotDefaultQtyLimit | | Fiyat kaynağı serisi veya kapanış fiyatı bulunamazsa varsayılan limit. |
| 228 | Factor | | Fiyat kotasyon çarpanı. |
| 292 | CorporateAction | | Bu menkul kıymet için şu anda etkin kurumsal işlemler. Geçerli değerler: 01 = R.H. Kullandirilarak Bedelli Sermaye Art(ırımı) (rüçhan hakkı kullandırılarak bedelli sermaye artırımı); 02 = R.H. Kullandirilmadan Bedelli Sermaye Art(ırımı); 03 = Bedelsiz Sermaye Artirimi; 04 = Sermaye Azaltimi; 05 = Birlesme / Devralma; 06 = Temettu; 99 = Diger. Önemli not: Birden çok kurumsal işlem olduğunda tag 292 değerler arasında boşluk karakteriyle gönderilir (ör. "292=01 03"). |
| 1150 | TradingReferencePrice | | Referans fiyat. |
| 21003 | BasePrice | | Baz fiyat. |
| 1116 | NoRootPartyIDs | | Taraf kimliği girdi sayısı (bu menkul kıymetin piyasa yapıcılarını göstermek için kullanılır). |
| → 1117 | RootPartyID | Q | Taraf tanımlayıcısı. |
| → 1118 | RootPartyIDSource | Q | Geçerli değerler: D = Özel/Özel kod (Proprietary/Custom code) |
| → 1119 | RootPartyRole | Q | Belirtilen PartyID'nin rol tipi. Geçerli değerler: 35 = Liquidity Provider (likidite sağlayıcı); 66 = Market Maker (piyasa yapıcı) |
| → 1120 | NoRootPartySubIDs | | Taraf kimliği alt girdi sayısı (bu menkul kıymette piyasa yapıcının yükümlülüğünü göstermek için kullanılır). |
| → → 1121 | RootPartySubID | | Geçerli değerler: 11 = Market Hours Continuous Quoting; 12 = Market Hours Quote Request; 21 = Off Market Hours Continuous Quoting; 22 = Off Market Hours Quote Request |
| → → 1122 | RootPartySubIDType | | Geçerli değer: 4001 = Market Maker Obligations (piyasa yapıcı yükümlülükleri). |
| 21004 | TradingMethod | | Enstrüman Sınıfından iki karakterlik bilgi alanı. |
| 21005 | GrossSettlement | | Brüt takas Enstrüman Sınıfı düzeyinde uygulanıyorsa Y, aksi hâlde N. |
| 916 | StartDate | | Sabit getirili piyasa serileri için Value1 tarihi; pay piyasası serileri için olağanüstü (extra-ordinary) seriler için ilk işlem tarihi. Tarih tanımlı değilse None. |
| 917 | EndDate | | Sabit getirili piyasa serileri için Value2 tarihi; pay piyasası serileri için olağanüstü seriler için son işlem tarihi. Tarih tanımlı değilse None. |
| 577 | ClearingInstruction | | Değerler: 6 = Merkezi karşı tarafa karşı takas (Clear against Central Counterparty); 7 = Merkezi karşı taraf dışında tut (Exclude from central counterparty) |
| 325 | Unsolicited Indicator | | Mesajın bir abonelik isteğinin sonucu olarak gönderilip gönderilmediğini gösterir. İstemciye ilk başlangıç isteğinde 'N' olur; aksi hâlde 'Y'. |
| 21007 | TradingSessionName | | İşlem seansının adı. |
| 21008 | PartitionId | Q | Bu menkul kıymetin hangi bölümde (partition) işlem gördüğü. |
| 21026 | DerivativeLevel | | Enstrümanın türev düzeyi. Geçerli değerler: 0 = Spot; 1 = Spot üzerine türev; 2 = Düzey 1 türev üzerine türev |
| 21027 | NumberOfSharesIssued | | Bu menkul kıymet için ihraç edilen toplam pay sayısı. |
| 21028 | PhysicalDelivery | | Enstrümanın fiziki teslimatlı tanımlanıp tanımlanmadığı. Geçerli değerler: Y/N |
| 21029 | Multiplier | | Varantlar/Sertifikalar için ek bilgi sağlayan isteğe bağlı alan. |
| 21030 | Reference | | Varantlar/Sertifikalar için ek bilgi sağlayan isteğe bağlı alan. |
| 21032 | InstrumentType | Q | Enstrüman tipi. |
| 21031 | SeriesDesc | Q | Geçerli değerler: S – Standart Enstrüman; NS – Standart Olmayan Enstrüman |
| 1194 | ExerciseStyle | | Geçerli değerler: 0 = Avrupa; 1 = Amerikan; 2 = Bermuda |
| 965 | SecurityStatus | Q | Geçerli değerler: 1 = Etkin (Active); 2 = Etkin değil (Inactive) |
| 1148 | LowLimitPrice | | Fiyat limitleri için güncel alt limit. |
| 1149 | HighLimitPrice | | Fiyat limitleri için güncel üst limit. |
| 5011 | OrderMaxValue | | Azami emir değeri; yalnızca pay piyasası için geçerli. |
| 38 | OrderQty | | |
| 159 | AccuredInterestAmt | | Sabit getirili ürünler ve sabit getirili türevler için birikmiş faiz tutarı. |
| 1948 | CouponFrequencyPeriod | | Sabit getirili enstrümanlar için kupon ödeme sıklığının zaman birimi çarpanı. |
| 1949 | CouponFrequencyUnit | | Sabit getirili enstrümanlar için kupon ödeme sıklığıyla ilişkili zaman birimi. |
| 1950 | CouponDayCount | | Sabit getirili enstrümanlar için faiz hesaplarında kullanılan gün sayımı kuralı. Geçerli değerler: 1 = US30360; 4 = EU30360; 6 = ACT360; 7 = ACT365; 8 = ACTAFB; 9 = ACTACT ISMA; 17 = ACT364 |
| 21059 | CouponInterest | | Dayanak için kupon faizi (yalnızca faizle ilgili sabit getirili enstrümanlar için). |
| 21055 | OddFirstCoupon | | Düzensiz ilk kupon kullanılıyorsa Y, aksi hâlde N. |
| 21056 | OddLastCoupon | | Düzensiz son kupon kullanılıyorsa Y, aksi hâlde N. |
| 21057 | PremiumUnit | | Emir giriş fiyat birimi. Geçerli değerler: 1 = Price; 2 = Yield; 3 = Point; 7 = Basis point; 8 = Clean price; 9 = Dirty price; 12 = Rate |
| 21058 | FixedIncomeType | | Sabit getirili dayanağın tipi. Geçerli değerler: 12 = Tip 1 İskontolu menkul kıymetler; 13 = Tip 2 Sabit faizli tahviller; 14 = Tip 3A Değişken faizli tahviller (sonraki kupon biliniyor); 15 = Tip 4 Endekse bağlı stripler; 16 = Tip 5 Endekse bağlı tahviller; 17 = Tip 6 Eurobond USD; 18 = Tip 7 Eurobond EUR; 19 = Tip 8A Düzensiz Clean price; 20 = Tip 3B Değişken faizli tahviller (sonraki kupon bilinmiyor); 21 = Tip 8B Düzensiz Dirty price; 22 = Tip 10A TLREF'e bağlı tahviller – Basit ağırlıklı ortalama; 23 = Tip 10B TLREF'e bağlı tahviller – Bileşik; 24 = Tip 10C TLREF'e bağlı tahviller – Endeks bazlı |
| 1940 | AssetType | | Geçerli değer: Precious (kıymetli). |
| 1938 | AssetClass | | Geçerli değer: 5 = Commodity (emtia). |
| 1939 | AssetSubClass | | Geçerli değer: 13 = Metal. |
| 996 | UnitOfMeasure | | Metal ağırlık birimi. Kıymetli metalin sertifikalı ağırlığı. Geçerli değerler: KG = kilogram; GR = gram; OZ = Troy ons |
| 21061 | FinenessNotation | | Metal saflığının piyasa gösterim kuralı. |
| 21062 | MetalWeightConversionFactor | | Emir ve işlem fiyatını normalleştirmek için kullanılan dönüşüm çarpanı. |
| 21060 | Fineness | | Metalin saflığı, 4 ondalık hane duyarlılığıyla. Geçerli aralık: 0,0001 – 1,0000 |
| 1147 | UnitOfMeasureQty | | Kıymetli metalin sertifikalı ağırlığı. |
| 21050 | NoTradeReports | | İşlem bildirimi (Trade Report) sayısı. |
| → 21051 | TradeReportCode | | Trade Report'lardaki tag 828 TrdType'ta kullanılacak sayı. Piyasanın verdiği desteklenen Trade Type değerleri listesine bakın. |
| → 21052 | MinTradeRepQty | | Trade Report'ta en düşük miktar. |
| → 21053 | MaxTradeRepQty | | Trade Report'ta en yüksek miktar. |
| → 21064 | TrLotsize | | Trade Report lot büyüklüğü. |
| 60 | TransactTime | | Yayım zamanı = güncel zaman. |
| 2304 | NoAssetAttributes | | Varlık niteliği sayısı. |
| → 2305 | AssetAttributeType | | Geçerli değerler: MetalType; Shape; Refinery |
| → 2306 | AssetAttributeValue | | Varlık nitelik değerleri, daha önce seçilen tipe doğrudan bağlıdır. Metal tipleri için: AU – altın; AG – gümüş; PT – platin; PD – paladyum. Şekil (shape) tipleri için: BA – Bar; MB – Mini Bar; LB – Büyük Bar; GB – Granül torbası; NS – Standart olmayan; OR – Cevher. Rafineri tipleri için: I – GDL In; O – GDL Out |
| 21063 | DaysToMaturity / Repo Term | | Sabit getirili piyasa serileri için vadeye kalan gün sayısı / repo vadesi. |
| 8000 | ShortSaleRestriction | | Hangi açığa satış doğrulama kuralının kullanılması gerektiğini belirtir. Geçerli değerler: 0 = Kısıtlama yok (açığa satışa fiyat doğrulaması olmadan izin verilir); 1 = Menkul kıymet açığa satılamaz (açığa satışa izin verilmez); 2 = Menkul kıymet en iyi alış fiyatında veya altında açığa satılamaz (açığa satışa yukarı adım (uptick) kuralı fiyat doğrulamasıyla izin verilir) |
| 21065 | IndexClassification | | Geçerli bir Endeks Sınıflandırması belirtir. |
| 21066 | ValueDate | | Dayanak için valör tarihi. |
| 21067 | ResetDate | | |
| 743 | DeliveryDate | | Teslimat başlangıç tarihi. |
| 21071 | PositionIncreasingOrders | | Değerler: 0 = İzin verilir; 1 = Bildirim (*); 2 = Uyarı (*); 3 = İzin verilmez. (*) Şu anda kullanılamaz, ileride kullanılmak üzere ayrılmıştır. Yalnızca Türev Piyasası için geçerlidir. |
| 21072 | NumberOfDecimalInPrice | | Emir defteri için fiyatta kullanılan ondalık hane sayısı. |
| 21073 | InstrumentClass | | Enstrüman sınıfı kimliği. |
| | Standard Trailer | Y | |

**Piyasa segmenti kodları (`MarketSegmentID`, tag 1300) [s. 23–24]** — kaynaktaki kod = ad listesi aynen aktarılmıştır:

| Kod | Ad (kaynak) |
|---|---|
| CMF | VIOP – EMTIA VIS – TRY |
| CRF | VIOP – DOVIZ VIS – TRY |
| CRFU | VIOP – DOVIZ VIS – USD |
| CRO | VIOP – DOVIZ OPSIYON – TRY |
| ENF | VIOP – ENERJI VIS – TRY |
| ETF | VIOP – BORSA YATIRIM FONU VIS – TRY |
| FGAP | BAP – GAP – TL |
| FGRB | BAP – GCREPO-BANKALARARASI-TL |
| FGRK | BAP-GCREPO-KUCUK-TL |
| FGRN | BAP-GCREPO-NORMAL-TL |
| FKEE | BAP-KES-EUR |
| FKEK | BAP-KES-KUCUK-TL |
| FKET | BAP-KES-NORMAL-TL |
| FKEU | BAP-KES-USD |
| FMKR | BAP-MKTR-TL |
| FNYE | BAP-NIP-EUR |
| FNYT | BAP-NIP-TL |
| FNYU | BAP-NIP-USD |
| FRPY | BAP-PAY REPO – TL |
| FTAS | BAP-TAAHHUTLU-SUKUK-TL |
| FTME | BAP-TEMERRUT-EUR |
| FTMT | BAP-TEMERRUT-TL |
| FTMU | BAP-TEMERRUT-USD |
| FUTE | BAP-UTP-EUR |
| FUTU | BAP-UTP-USD |
| FIF | VIOP – YABANCI ENDEKSLER VIS – TRY |
| G | PAY-GELISEN ISLETMELER PAZARI |
| INF | VIOP – ENDEKS VIS – TRY |
| INO | VIOP – ENDEKS OPSIYON – TRY |
| IP | IHRAC PAZARI |
| K | PAY-KOLLEKTIF&YAPILANDIRILMIS UR. PAZARI |
| KCMH | KMP CUMHURIYET ALTINI |
| KES | KESIN ALIM SATIM |
| KFIX | KMP ALTIN FIKSING |
| KLEN | KMP ODUNC PIYASASI |
| KN1E / KN1T / KN1U | KMP ALTIN – S. DISI ve CEVHER (EUR / TRY / USD) |
| KN2E / KN2T / KN2U | KMP GUMUS – S. DISI ve CEVHER (EUR / TRY / USD) |
| KN3E / KN3T / KN3U | KMP PLATIN – S. DISI (EUR / TRY / USD) |
| KN4E / KN4T / KN4U | KMP PALADYUM – S. DISI (EUR / TRY / USD) |
| KS1E / KS1T / KS1U | KMP ALTIN – STANDART (EUR / TRY / USD) |
| KS2E / KS2T / KS2U | KMP GUMUS – STANDART (EUR / TRY / USD) |
| KS3E / KS3T / KS3U | KMP PLATIN – STANDART (EUR / TRY / USD) |
| KS4E / KS4T / KS4U | KMP PALADYUM – STANDART (EUR / TRY / USD) |
| KTEK | KMPALTIN TEK FIYAT |
| MTF | VIOP – METAL VIS – USD |
| N | PAY-ANA PAZAR |
| ONF | VIOP – GECELIK REPO VIS – TRY |
| PMF | VIOP – KIYMETLI MADENLER VIS – TRY |
| PMFU | VIOP – KIYMETLI MADENLER VIS – USD |
| Q | PAY-NITELIKLI YATIRIMCI ISLEMLERI PAZARI |
| S | PAY-PIYASA ONCESI ISLEM PLATFORMU |
| SSF | VIOP – PAY VIS – TRY |
| SSO | VIOP – PAY OPSIYON – TRY |
| W | PAY-YAKIN IZLEME PAZARI |
| Z | PAY-YILDIZ PAZAR |
| E | PAY-EMTIA PAZARI |

> **Çeviri notu:** Kaynakta KN1E…KS4U, "KMP ALTIN – S. DISI ve CEVHER (EUR/TRY/USD)" gibi üçlü kodlar ayrı satırlarda yazılıdır; burada aynı ad altında tek satırda birleştirilmiştir. Pay Piyasası için ilgili kodlar: Z = Yıldız Pazar, N = Ana Pazar, W = Yakın İzleme Pazarı, G = Gelişen İşletmeler Pazarı, S = Piyasa Öncesi İşlem Platformu, Q = Nitelikli Yatırımcı İşlemleri Pazarı, K = Kollektif & Yapılandırılmış Ürünler Pazarı, E = Emtia Pazarı, IP = İhraç Pazarı.

#### 5.4.2 Security Definition Request (in) — MsgType = c [s. 29]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = c |
| 320 | SecurityReqID | Y | İstemci tarafından üretilen tanımlayıcı. |
| 321 | SecurityRequestType | Y | Security Definition istek tipi. Geçerli değerler: 4 = Symbol |
| 55 | Symbol | Q | Kısa ad. |
| | Standard Trailer | Y | |

#### 5.4.3 Security Definition Update Report (out) — MsgType = BP [s. 30–40]

Alan listesi 5.4.1 Security Definition ile aynıdır (aynı tag'ler, aynı açıklamalar), şu farklarla: (a) ek alan **980 SecurityUpdateAction (Q)** vardır; geçerli değerler: A = Add (ekle); D = Delete (sil); M = Modify (değiştir). (b) Tag 325 `Unsolicited Indicator` bu mesajda listelenmemiştir. (c) `MsgType = BP`. Kaynakta alanlar satır kaymalarıyla yazılmış olsa da tablo içeriği 5.4.1 ile örtüşür.

#### 5.4.4 Market Definition (out) — MsgType = BU [s. 41]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = BU |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. |
| 1394 | MarketReportID | Y | FIX'te zorunludur. Ayarlanır ancak yok sayılabilir. |
| 1301 | MarketID | Y | Beş karakterlik piyasa tanımlayıcısı. |
| | Standard Trailer | Y | |

#### 5.4.5 Trading Session List (out) — MsgType = BJ [s. 42]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = BJ |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. |
| 386 | NoTradingSessions | Y | Bu mesajda listelenen işlem seansı (durum) sayısı. |
| → 336 | TradingSessionID | Y | İşlem seansının kimliği. |
| → 1326 | TradingSessionDesc | Q | İşlem seansının insan tarafından okunabilir adı. |
| → 1237 | NoOrdTypeRules | | Her zaman 1'dir. |
| → → 40 | OrdType | | Bu durumda piyasa emirlerine izin verilip verilmediğini gösterir. Geçerli değerler: 1 = Market |
| → 1239 | NoTimeInForceRules | | İzin verilen farklı emir tipi kuralı sayısını gösterir. |
| → → 59 | TimeInForce | | Bu durumda IOC veya FOK emirlerine izin verilip verilmediğini gösterir. Geçerli değerler: 3 = Immediate Or Cancel (IOC); 4 = Fill Or Kill (FOK) |
| → 1235 | NoMatchRules | | Her zaman 1'dir. |
| → → 1142 | MatchAlgorithm | | Grup varsa FIX'te zorunludur. Her zaman [N/A] olarak ayarlanır. |
| → → 574 | MatchType | | Geçerli değerler: 4 = Auto-match (otomatik eşleşme) |
| → 20032 | SessionStateTypeNumber | | NASDAQ uzantısı: Bir emri bu durum oluştuğunda tetiklemek için emirdeki TriggerTradingSessionID'de kullanılan sayı. |
| → 21024 | OffHoursTrading | | Bu bayrak bir seansın mesai dışı (off hours) olup olmadığını gösterir. |
| | Standard Trailer | Y | |

#### 5.4.6 Security Status Request (in) — MsgType = e [s. 42–43]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = e |
| 263 | Subscription Request Type | Q | Abonelik istek tipi. Geçerli değerler: 0 = Snapshot |
| 55 | Symbol | Q | Kısa ad. |
| 324 | SecurityStatusReqID | Q | İstemci tarafından üretilen tanımlayıcı. |
| | Standard Trailer | Y | |

#### 5.4.7 Security Status (out) — MsgType = f [s. 43]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = f |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. |
| 55 | Symbol | Q | Kısa ad. |
| 48 | SecurityID | Q | Orderbook ID. |
| 22 | SecurityIDSource | Q | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 336 | TradingSessionID | | Seans durumunun kimliği. |
| 326 | SecurityTradingStatus | | Bir menkul kıymet durdurulduğunda veya yeniden başlatıldığında gönderilir. Değerler: 2 = Trading Halt (işlem durdurma); 3 = Resume (yeniden başlama) |
| 325 | Unsolicited Indicator | | Mesajın bir abonelik isteğinin sonucu olarak gönderilip gönderilmediğini gösterir. İstemciye ilk başlangıç isteğinde 'N' olur; aksi hâlde 'Y'. |
| 292 | CorporateAction | | Bu menkul kıymet için şu anda etkin kurumsal işlemler. Geçerli değerler: 5.4.1'deki ile aynıdır (01 … 06, 99). Birden çok değer boşlukla ayrılır (ör. "292=01 03"). |
| 31 | LastPX | | İlgili menkul kıymetin son seanstaki son işlem fiyatı. Bu fiyat her işlemden sonra gerçek zamanlı güncellenmez. |
| | Standard Trailer | Y | |

#### 5.4.8 Price Reference Request (in) — MsgType = pp [s. 43]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = pp |
| 55 | Symbol | Q | Kısa ad. |
| | Standard Trailer | Y | |

#### 5.4.9 Price Reference (out) — MsgType = pr [s. 44]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = pr |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. |
| 55 | Symbol | Q | Kısa ad. |
| 48 | SecurityID | Q | Orderbook ID. |
| 22 | SecurityIDSource | Q | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 325 | Unsolicited Indicator | Q | Mesajın bir abonelik isteğinin sonucu olarak gönderilip gönderilmediğini gösterir. İstemciye ilk başlangıç isteğinde 'N' olur; aksi hâlde 'Y'. |
| 1148 | LowLimitPrice | | Fiyat limitleri için güncel alt limit. |
| 1149 | HighLimitPrice | | Fiyat limitleri için güncel üst limit. |
| 1150 | TradingReferencePrice | | Referans fiyat. |
| 21003 | Base Price | | Baz fiyat. |
| 21025 | TheoreticalPrice | | Teorik fiyat. |
| 140 | PrevClosePx | | Önceki günün kapanış fiyatı. |
| 60 | TransactTime | | Yayım zamanı = güncel zaman. |
| | Standard Trailer | Y | |

#### 5.4.10 At The Money Update (out) — MsgType = mm [s. 44–45]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = mm |
| 1180 | ApplicationSequenceControl/ApplID | Q | Application ID. Geçerli değerler: R = Reference Data |
| 1181 | ApplicationSequenceControl/ApplSeqNum | Q | Mesaja, mesajı üreten uygulama tarafından atanan application sıra numarası. |
| 1350 | ApplicationSequenceControl/ApplLastSeqNum | Q | Application sıra akışındaki önceki sıra numarası. |
| 55 | Symbol | Q | Kısa ad. |
| 48 | SecurityID | Q | Orderbook ID. |
| 22 | SecurityIDSource | Q | Geçerli değerler: M = Piyasa tarafından atanan tanımlayıcı |
| 202 | Strike Price | Q | Opsiyon için kullanım fiyatı. |
| 541 | MaturityDate | Q | Vade tarihi. Ek not: At-The-Money vade tarihi, Security Definition / Security Definition Update mesajlarındaki vade tarihinden farklı olabilir. Vade tarihi, Türev Piyasası kararıyla oluşturulduktan sonra değiştirilebilir. Bu değişiklik durumunda ATM vade tarihi özgün vade tarihini gösterir. |
| 21054 | ATMPrice | Q | At-The-Money fiyatı. |
| 21003 | BasePrice | Q | Kullanılan baz fiyat. |
| 201 | PutOrCall | Q | Opsiyon sözleşmesinin put mı call mı olduğunu gösterir. |
| 60 | TransactTime | | Yayım zamanı = güncel zaman. |
| | Standard Trailer | Y | |

#### 5.4.11 Application Message Request (in) — MsgType = BW [s. 46]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = BW |
| 1346 | ApplReqID | Y | İstek için benzersiz tanımlayıcı. |
| 1347 | ApplReqType | Y | Yapılan Application Message Request'in tipi. Geçerli değerler: 1 = Belirtilen Application'lara abonelik |
| 1351 | NoApplIDs | | Bu istekteki Application ID sayısı. |
| → 1355 | RefApplID | Q | İstenen Application ID. Geçerli değerler: R = Reference Data |
| → 1182 | ApplBegSeqNum | | Yeniden gönderilecek ilk mesajın sıra numarası. |
| → 1183 | ApplEndSeqNum | | Yeniden gönderilecek son mesajın sıra numarası veya tüm mesajlar için 0 (sıfır). |
| | Standard Trailer | Y | |

#### 5.4.12 Application Message Request Ack (out) — MsgType = BX [s. 47]

| Tag | Alan adı | Zor. | Açıklama |
|---|---|---|---|
| | Standard Header | Y | MsgType = BX |
| 1353 | ApplResponseID | Y | Application Message Request Ack için tanımlayıcı. |
| 1346 | ApplReqID | Q | Bu ACK mesajıyla ilişkili isteğin tanımlayıcısı. |
| 1347 | ApplReqType | Q | Yapılan Application Message Request'in tipi. Geçerli değerler: 1 = Belirtilen Application'lara abonelik |
| 1348 | ApplResponseType | Q | Gönderilen onayın tipini belirtir. Geçerli değerler: 0 = İstek başarıyla işlendi; 1 = Application mevcut değil; 2 = Mesajlar mevcut değil; 3 = Application için yinelenen istekler (NASDAQ OMX uzantısı) |
| 1351 | NoApplIDs | | Bu istekteki Application ID sayısı. |
| → 1355 | RefApplID | | İstenen Application ID. Geçerli değerler: R = Reference Data |
| → 1182 | ApplBegSeqNum | | Yeniden gönderilecek ilk mesajın sıra numarası. |
| → 1183 | ApplEndSeqNum | | Yeniden gönderilecek son mesajın sıra numarası veya tüm mesajlar için 0. |
| → 1354 | ApplResponseError | | Geçerli değerler: 0 = Application mevcut değil; 1 = İstenen mesajlar mevcut değil; 3 = Application için yinelenen istekler (NASDAQ OMX uzantısı) |
| 58 | Text | | |
| | Standard Trailer | Y | |

## 6 Ek A — NASDAQ OMX Uzantıları (Appendix A, NASDAQ OMX Extensions) [s. 48–50]

Bu bölüm çözümün standart FIX 5.0 SP2'den nasıl saptığını ayrıntılandırır. Standarda uymak için büyük özen gösterilmiş olsa da, ana sistemin sunduğu tüm mekanizmaları desteklemek için bir dizi sapma kaçınılmazdır. Sapma tipleri: (1) Eklenen alanlar: FIX 5.0 SP2'de bulunmayan arka uç işlevlerini karşılamak için bazı kullanıcı tanımlı alanların eklenmesi gerekmiştir. (2) Eklenen enum değerleri: Bazı alanlara enum eklenmiştir. (3) Alan tanımı değiştirilenler.

### 6.1 Eklenen Alanlar [s. 48–49]

| Tag | Alan adı | Eklendiği mesaj(lar) / grup | Tip |
|---|---|---|---|
| 20002 | DaysToPwdExpiry | Logon | int |
| 577 | ClearingInstruction | Security Definition; Security Definition Update Report | int |
| 20032 | SessionStateTypeNumber | Trading Session List | int |
| 20035 | LastTradingDate | Security Definition; Security Definition Update Report | Date |
| 21001 | InstClassification | Security Definition; Security Definition Update Report | String |
| 21003 | BasePrice | Security Definition; Security Definition Update Report; Price Reference; At The Money Update | Price |
| 21004 | TradingMethod | Security Definition; Security Definition Update Report | String |
| 21005 | GrossSettlement | Security Definition; Security Definition Update Report | Boolean |
| 21007 | TradingSessionName | Security Definition; Security Definition Update Report | String |
| 21008 | PartitionId | Security Definition; Security Definition Update Report | String |
| 21009 | LotDisplayHighQty | Tekrarlı grup: NoLotTypeRules | Qty |
| 21010 | LotStartPrice | Tekrarlı grup: NoLotTypeRules | Price |
| 21011 | LotDefaultQtyLimit | Tekrarlı grup: NoLotTypeRules | Boolean |
| 21012 | LotMaxTradeVol | Tekrarlı grup: NoLotTypeRules | Qty |
| 21013 | LotMinQty | Tekrarlı grup: NoLotTypeRules | Qty |
| 21014 | LotDisplayLowQty | Tekrarlı grup: NoLotTypeRules | Qty |
| 21015 | NoCollTickRules | Security Definition; Security Definition Update Report | int |
| 21016 | CollTickIncrement | Tekrarlı grup: NoCollTickRules | Price |
| 21017 | CollStartTickPriceRange | Tekrarlı grup: NoCollTickRules | Price |
| 21018 | CollEndTickPriceRange | Tekrarlı grup: NoCollTickRules | Price |
| 21019 | NoCollUnderlyings | Security Definition; Security Definition Update Report | int |
| 21020 | CollUnderlyingSymbol | Tekrarlı grup: NoCollUnderlyings | String |
| 21021 | CollUnderlyingSecurityID | Tekrarlı grup: NoCollUnderlyings | String |
| 21022 | CollUnderlyingSecurityIDSource | Tekrarlı grup: NoCollUnderlyings | String |
| 21023 | CollUnderlyingCurrency | Tekrarlı grup: NoCollUnderlyings | String |
| 21024 | OffHoursTrading | Tekrarlı grup: NoMatchRules | Boolean |
| 21025 | TheoreticalPrice | Price Reference | Price |
| 21026 | DerivativeLevel | Security Definition; Security Definition Update Report | int |
| 21027 | NumberOfSharesIssued | Security Definition; Security Definition Update Report | Qty |
| 21028 | PhysicalDelivery | Security Definition; Security Definition Update Report | Boolean |
| 21029 | Multiplier | Security Definition; Security Definition Update Report | String |
| 21030 | Reference | Security Definition; Security Definition Update Report | String |
| 21031 | SeriesDesc | Security Definition; Security Definition Update Report | String |
| 21032 | InstrumentType | Security Definition; Security Definition Update Report | String |
| 21050 | NoTradeReports | Security Definition; Security Definition Update Report | int |
| 21051 | TradeReportCode | Tekrarlı grup: NoTradeReports | int |
| 21052 | MinTradeRepQty | Tekrarlı grup: NoTradeReports | Qty |
| 21053 | MaxTradeRepQty | Tekrarlı grup: NoTradeReports | Qty |
| 21054 | AtTheMoneyPrice | At The Money Update | Price |
| 21063 | DaysToMaturity / Repo Term | Security Definition; Security Definition Update Report | int |

### 6.2 Eklenen Enumerasyonlar [s. 49–50]

| Enumerasyon | Eklendiği alan | Açıklama |
|---|---|---|
| 100 = Invalid body length in received message, session suspended; 101 = Heartbeat interval too low | SessionStatus | Alınan mesajda geçersiz gövde uzunluğu, oturum askıya alındı; Heartbeat aralığı çok düşük |
| 101 = All or None Lot (NASDAQ OMX Extension enum) | LotType | Hepsi ya da Hiçbiri lotu (revizyon geçmişine göre 1.0.7'de LotType'tan kaldırılmıştır) |
| 1 = Options; 2 = Forward; 3 = Futures; 4 = FRA; 5 = Cash; 6 = Payment; 7 = Exchange Rate; 8 = Interest rate swap; 9 = REPO; 11 = Combination; 12 = Guarantee; 13 = OTC general; 14 = Equity warrant; 15 = Security lending; 17 = Strip; 18 = Certificates | SecurityType | |
| 101 = Trade Report Close; 102 = System Available | TradSesStatus | İşlem bildirimi kapanışı; sistem kullanılabilir |
| 3 = Duplicate requests for application | ApplResponseType | Application için yinelenen istekler |
| 3 = Duplicate requests for application | ApplResponseError | Application için yinelenen istekler |

### 6.3 Alan Tanımı Değişiklikleri

Alan tanımı değişikliği yoktur.

## 7 Revizyon Geçmişi (Revision History) [s. 51–53]

| Tarih | Revizyon | Değişiklik açıklaması |
|---|---|---|
| 24 Haziran 2014 | 0.1 | İlk sürüm. |
| 8 Ağustos 2014 | 0.2 | Yeni FIX mesajları eklendi. |
| 3 Eylül 2014 | 0.3 | Yeni eklenen fix mesajları doğru alanlarla güncellendi. |
| 12 Eylül 2014 | 0.4 | Tag 21007 eklendi ve tag 1301 → 1396 olarak değiştirildi. |
| 17 Ekim 2014 | 0.5 | Tag 167 (Security Type) için tüm olası BIST değerleri eklendi. |
| 19 Kasım 2014 | 0.6 | Yeni logo eklendi. |
| 3 Aralık 2014 | 0.7 | Security Definition ve Security Definition Update Report'a MarketID eklendi; Security Definition'a Unsolicited indicator eklendi; tam eşleşme (exact match) ve 0 fiyat limitleri hakkında bilgi eklendi. |
| 26 Ocak 2015 | 0.8 | marketDefinition mesajından MarketSegmentDesc kaldırıldı. Security status ve Price reference, 5.3.2.1 bölümüne eklendi. |
| 12 Şubat 2015 | 0.9 | Kurumsal işlem güncellemeleri için açıklama eklendi. |
| 16 Mart 2015 | 0.9.1 | Tag 1119 için geçerli taraf rolü olarak Liquidity Provider eklendi. |
| 7 Nisan 2015 | 0.9.2 | Tag 292, 1300 ve 21007 için olası değerler eklendi. |
| 9 Haziran 2015 | 0.9.3 | Tag 20002 logon out mesajına eklendi. |
| 10 Temmuz 2015 | 0.9.4 | Tag 340 artık trading session list mesajında zorunlu değil. |
| 17 Ağustos 2015 | 0.9.5 | Tag 336 price reference mesajından kaldırıldı. |
| 21 Eylül 2015 | 0.9.6 | Sorumluluk reddi güncellendi. |
| 1 Şubat 2016 | 0.9.7 | TradingSessionName'den prv_ts kaldırıldı. |
| 23 Nisan 2015 | 1.0.0 | Faz 2 için ilk sürüm oluşturuldu. |
| 14 Eylül 2015 | 1.0.2 | Faz 2'ye özgü değişiklikler ve faz 1'den güncellemeler dahil edildi. |
| 5 Şubat 2016 | 1.0.3 | Trading session list'e tag 21024; security definition'a rootpartysubIdGroup, AtTheMoneyMessage eklendi. Security definition mesajına 21030, 21031, 1194, 965, 21032, 1148, 1149 tag'leri ve noTradeReports grubu eklendi. |
| 25 Şubat 2016 | 1.0.4 | TradingSessionName'e türev işlem seansları eklendi. |
| 14 Mart 2016 | 1.0.5 | Security Definition ve security definition update mesajları için tag 21026–21030'a ek bilgi eklendi. |
| 16 Mart 2016 | 1.0.6 | AtTheMoneyUpdate (out) bölümündeki MsgType tag'i düzeltildi. Price Reference (out) bölümüne tag 21025 eklendi. |
| 5 Nisan 2016 | 1.0.7 | Trading Session List ve Trading Session List (out) bölümlerinden tag 340 kaldırıldı. Yeni çıkış yönlü mesaj AtTheMoneyUpdate eklendi. Security Definition (out) ve Security Definition Update Report (out)'a yeni tag 1244/FlexibleIndicator, 1242/FlexProductEligibilityIndictor, yeni grup 21019/NoCollUnderlyings, 21015/NoCollTickRules eklendi. NoLotTypeRules grubuna yeni tag'ler 21010/LotStartPrice, 21013/LotMinQty, 21009/LotDisplayHighQty, 21014/LotDisplayLowQty, 21011/LotDefaultQtyLimit eklendi. Tag 1140/MaxTradeVol, 21012/LotMaxTradeVol ile değiştirildi. Yeni grup 1120/NoRootPartySubIDs eklendi. Tag 1093/LotType'tan iki izinli değer (1 = Odd Lot ve A = All or None Lot) kaldırıldı. |
| 24 Haziran 2016 | 1.0.8 | Faz 1 dokümantasyonuyla karşılaştırıldığında eksik girdiler eklenerek revizyon geçmişi tablosu güncellendi. |
| 27 Temmuz 2016 | 1.0.9 | Yeni SecurityType değeri "11 = Combination" eklendi. |
| 4 Ağustos 2016 | 1.0.10 | Tag 21013, 21009, 21014, 21011, 228, 21051, 1300, 1237, 1239, 1235, 31 için açıklamalar eklendi/güncellendi. |
| 24 Ekim 2016 | 1.0.11 | Özel alanlar listesi güncellendi. Security Definition ve Update Report mesajlarından tag 21028'in yinelenen tanımı kaldırıldı. |
| 15 Kasım 2016 | 1.0.12 | Tag 1121 RootPartySubID için geçerli değerler listesi güncellendi. |
| 16 Kasım 2016 | 1.0.13 | Telif hakkı ve sorumluluk reddi değişikliği. |
| 14 Haziran 2017 | 1.0.14 | Security Definition ve Update Report mesajlarına yeni tag'ler eklendi: 38, 159, 996, 1147, 1938, 1939, 1940, 1948, 1949, 1950, 2304, 2305, 2306, 5011, 21055–21062. |
| 16 Ekim 2017 | 1.0.15 | Security Definition ve Update Report mesajlarına yeni tag'ler eklendi: 223, 224, 306. Tag 21057 ve 1300 için geçerli değerler güncellendi. |
| 8 Ocak 2018 | 1.0.16 | Tag 21057 ve 1950 için geçerli değerler güncellendi. |
| 15 Ocak 2018 | 1.0.16 | Yeni SecurityType değeri "17 = Strip" eklendi. |
| 30 Ocak 2018 | 1.0.17 | Security Definition ve Update Report mesajlarına yeni tag'ler eklendi: 107, 20036, 20037, 20038, 20039, 20040, 225, 873. |
| 22 Şubat 2018 | 1.0.18 | Security Definition ve Update Report mesajlarına yeni tag eklendi: 20041. |
| 7 Mayıs 2018 | 1.0.19 | NoCollTickRules grubunda düzenleme. |
| 16 Mayıs 2018 | 1.0.20 | "Number of Tick Rules" tekrarlı grubu güncellendi. |
| 9 Ağustos 2018 | 1.0.21 | Security Definition ve Update Report mesajlarındaki tag'ler güncellendi: 916, 917. Yeni tag eklendi: 21063. |
| 13 Şubat 2018 | 1.0.22 | 167 tag değerleri yazım hatası güncellendi. (Kaynaktaki tarih sırası kaymış görünür.) |
| 26 Mart 2018 | 1.0.23 | "Shortsalerestriction" – tag 8000 ve "TrLotsize" – tag 21064 bilgileri, çıkış yönlü Security Definition / Security Definition Update Report mesajlarında FIX RD üzerinden kullanılabilir. (Kaynaktaki tarih sırası kaymış görünür.) |
| 18 Nisan 2019 | 1.0.24 | Logout mesajı (MsgType=5) için tag 1409'a yeni değerler eklendi. |
| 22 Ekim 2019 | 1.0.25 | Security Definition (out) (MsgType = d) ve Update Report (out) (MsgType = BP) için tag 21058'e yeni değerler (22, 23, 24) eklendi. |
| 6 Şubat 2020 | 1.0.26 | Sözdizimi hataları düzeltildi: 3.13.4 Logout (tag 1409), 3.13.9 Reject (tag 373), 5.4.1 Security Definition (tag 21057), 5.4.3 Security Definition Update Report (tag 21057), 5.4.5 Trading Session List (tag 59), 6.2 Eklenen Enumerasyonlar. |
| 18 Şubat 2020 | 1.0.27 | Security Definition (out) ve Update Report (out) için yeni tag 21065 (IndexClassification) ve 21066 (ValueDate) eklendi. |
| 22 Mayıs 2020 | 1.0.28 | Yeni tag 21067 (ResetDate) eklendi. |
| 5 Nisan 2021 | 1.0.29 | Yeni tag 743 (DeliveryDate) eklendi. 159 tag açıklaması "Sabit getirili ürünler ve sabit getirili türevler için birikmiş faiz tutarı" olarak güncellendi. |
| 13 Mayıs 2022 | 1.0.30 | Yeni tag'ler eklendi: 21068 (LotMinQuote), 21069 (LotMaxQuote). |
| 27 Ekim 2023 | 1.0.31 | Yeni tag eklendi: 21070 ShortSellValidation (Service Release 3.01 ile etkinleşir). |
| 28 Kasım 2023 | 1.0.32 | Tag 21070'e yeni enumerasyon (2) eklendi (Service Release 3.01 ile etkinleşir). |
| 6 Mart 2024 | 1.0.33 | "At the Money Update" mesajındaki 541 (Maturity Date) tag açıklaması güncellendi. Yeni tag eklendi: 21071 PositionIncreasingOrders (Service Release 3.10 ile etkinleşir). |
| 10 Haziran 2024 | 1.0.34 | 59 tag değeri düzeltildi. |
| 23 Temmuz 2024 | 1.0.35 | Tag 292 ve 1300 açıklamaları güncellendi. |
| 10 Eylül 2024 | 1.0.36 | Yeni tag'ler eklendi: 21072 NumberOfDecimalInPrice, 21073 InstrumentClass (Service Release 3.11 ile etkinleşir). |
| 14 Kasım 2024 | 1.0.37 | ShortSellValidation (tag 21070) enumerasyonu güncellendi. |
| 15 Kasım 2024 | 1.0.38 | ShortSaleRestriction (tag 8000) ve ShortSellValidation (tag 21070) enumerasyonu güncellendi. |
| 13 Ocak 2025 | 1.0.39 | ShortSaleRestriction (tag 8000) enumerasyonu güncellendi. ShortSellValidation (tag 21070) kaldırıldı. |
| 5 Kasım 2025 | 1.0.40 | ClearingInstruction (tag 577) enumerasyonu güncellendi. |

---

## Çapraz kontrol (kaynakta yok; çevirenin gözlemi)

- Security Definition tablosundaki 138 tag numarası PDF s. 21–29 metninden çıkarılan 140 tag ile karşılaştırıldı: PDF'teki tüm tag'ler tabloda vardır; PDF listesindeki fazladan iki tag (320, 321) bir sonraki mesaja (5.4.2 Security Definition Request) aittir ve orada yer alır.
- Kaynak tutarsızlıkları: kapak sürümü 1.0.40, altbilgi 1.0.30; Revizyon geçmişinde 1.0.22 ve 1.0.23 tarihleri sıra dışıdır; 6.2'de `LotType` için "101 = All or None Lot" listelenmeye devam eder ancak revizyon 1.0.7 bunu kaldırdığını söyler.
- **ITCH ile ilişki:** Bu mesajlardaki `ShortSaleRestriction` (tag 8000: 0/1/2) değerleri ITCH `V` mesajındaki `Short Sale Restriction` (0/1/2) ile aynıdır; `NumberOfDecimalInPrice` (21072) ITCH `R` mesajındaki "Number of decimals in Price" ile; `LotType` (2 = Round, 3 = Block) ITCH `A` mesajındaki `Lot Type` (yalnızca 2 listeli) ile; `PartitionId` (21008) enstrümanın hangi bölümde işlem gördüğünü bildirir (Prosedür 5.7.4'te dört bölüm/Partition).
