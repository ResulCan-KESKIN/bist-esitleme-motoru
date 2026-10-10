# SoupBinTCP Protokol Spesifikasyonu (Türkçe çeviri)

Kaynak: `soupbintcp-protocol-specification.pdf` — "SoupBinTCP", Sürüm 3.00 (tarihli son revizyon girdisi: 20.03.2014), 9 sayfa.
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir (PDF metni `pdftotext` ile alındı; paket tabloları elle yeniden yazıldı). Paket tipi karakterleri, alan adları ve sabitler çevrilmeden bırakılmış, Türkçe karşılıkları parantez içinde verilmiştir. Offset ve uzunluklar bayt cinsindendir.
Doğrulama: Sayfa görüntüsüyle karşılaştırma yapılmadı. PDF metin çıkarımında bazı tablolar karışıktı (alan sırası bozuk); offset/uzunluklar şu kontrolle toparlandı: Login Accepted'da 3+10 = 13 ve 13+20 = 33; Login Request'te 3+6 = 9, 9+10 = 19, 19+10 = 29, 29+20 = 49. Yani her alan bir öncekinin bittiği yerden başlıyor. Kullanıcı doğrulaması: bekliyor.
İlgili dosya: `bistech-itch-protokol-spesifikasyonu.md` (Appendix E: GLIMPSE servisi SoupBinTCP ile kodlanır).

---

## 1 Genel Bakış (Overview) [s. 1]

SoupBinTCP, TCP/IP soketleri üzerine kurulu, bir dizi sıralı mesajın sunucudan istemciye gerçek zamanlı teslimine imkân veren hafif bir noktadan noktaya (point-to-point) protokoldür. SoupBinTCP, altta yatan TCP/IP soket bağlantısı hatalarında bile istemcinin sunucunun ürettiği her mesajı sırayla almasını garanti eder.

SoupBinTCP istemcileri sunucuya mesaj gönderebilir. Bu mesajlar sıralı değildir ve TCP/IP soket hatasında kaybolabilir.

SoupBinTCP, bir sunucunun gerçek zamanlı olarak mantıksal bir sıralı mesaj akışını istemciye iletmesi gereken, ancak istemcinin ürettiği mesajlar için aynı garanti seviyesini gerektirmeyen sistemler için idealdir (veri akışı tek yönlü olduğu için ya da sunucu uygulaması önemli istemci mesajları için üst seviye sıralı onaylar ürettiği için).

SoupBinTCP, SoupBinTCP mesajlarının ilettiği mesajların içeriğini belirleyen üst seviye protokollerle birlikte kullanılmak üzere tasarlanmıştır. SoupBinTCP protokol katmanı üst seviye mesajlara karşı opaktır (içeriğini yorumlamaz). ASCII sürümünün aksine mesajlar herhangi bir baytı içerebilir.

SoupBinTCP ayrıca sunucunun istemciyi oturum açma (login) sırasında doğrulaması için basit bir şema içerir.

### 1.1 SoupBinTCP Mantıksal Paketleri

SoupBinTCP istemcisi ve sunucusu bir dizi mantıksal paket (logical packet) değiş tokuş ederek iletişim kurar.

Her SoupBinTCP mantıksal paketi şunlardan oluşur:

- A. Paketin geri kalanının uzunluğunu belirten iki baytlık big-endian uzunluk (yani yükün uzunluğu artı paket tipinin uzunluğu olan 1).
- B. Paket tipini belirten tek baytlık başlık.
- C. Değişken uzunluklu yük (payload).

Yapı: `[2 bayt Packet Length][1 bayt Packet Type][değişken uzunlukta payload]`

Notlar:

- SoupBinTCP mantıksal paketleri, altta yatan ağ soketindeki fiziksel paketlerle doğrudan eşleşmek zorunda değildir; TCP/IP yığını tarafından bölünebilir veya birleştirilebilir.
- SoupBinTCP protokolü en büyük yük uzunluğunu tanımlamaz.
- ASCII sürümünün aksine yük satır sonu (line feed) karakterini veya herhangi bir karakteri içerebilir. (Dikkat: Bkz. aşağıdaki "Çevirmenin ek notları" — Sequenced/Unsequenced Data tablolarında yükün gömülü satır sonu içermemesi gerektiği yazılıdır.)

### 1.2 Protokol Akışı

Bir SoupBinTCP bağlantısı, istemcinin sunucuya bir TCP/IP soketi açması ve bir Login Request Packet göndermesiyle başlar. Login isteği geçerliyse sunucu bir Login Accepted Packet ile yanıt verir ve Sequenced Data Packet'ler göndermeye başlar. Bağlantı, TCP/IP soketi kopana kadar sürer.

Her Sequenced Data Packet tek bir üst seviye protokol mesajı taşır.

Sequenced Data Packet'ler açık bir sıra numarası içermez; bunun yerine hem istemci hem sunucu mesajları sayarak sıra numarasını yerel olarak hesaplar.

Her oturumdaki ilk sıralı mesajın sıra numarası her zaman 1'dir.

Tipik olarak, bir sunucuya ilk kez giriş yaparken istemci Login Request Packet'teki Requested Sequence Number alanını 1 yapar ve Requested Session alanını boş bırakır. İstemci daha sonra etkin oturumu belirlemek için Login Accepted Packet'i inceler. 1'den başlayarak, her Sequenced Data Packet alındığında yerel sıra numarasını artırır. TCP/IP bağlantısı kopmuşsa istemci, mevcut oturumu ve beklediği bir sonraki sıra numarasını belirterek sunucuya yeniden giriş yapabilir. Böylece istemcinin, TCP/IP bağlantı hatalarına rağmen her sıralı mesajı sırayla alması garanti edilir.

SoupBinTCP ayrıca istemcinin Login Accepted Packet alındıktan sonra herhangi bir zamanda Unsequenced Data Packet'lerle sunucuya mesaj göndermesine izin verir. Bu mesajlar TCP/IP soket bağlantısı hatalarında kaybolabilir.

### 1.3 Kalp Atışları (Heartbeats)

SoupBinTCP bağlantı hatalarını hızla tespit etmek için mantıksal heartbeat paketleri kullanır. Sunucu, en son veri gönderiminden bu yana 1 saniyeden fazla geçtiğinde Server Heartbeat paketi göndermek zorundadır. Bu, istemcinin düzenli olarak veri almasını sağlar. İstemci uzun bir süre boyunca hiçbir şey (ne veri ne heartbeat) almazsa bağlantının koptuğunu varsayabilir ve yeni bir TCP/IP soketiyle yeniden bağlanmayı deneyebilir.

Benzer şekilde, giriş yapıldıktan sonra istemci en son bir şey göndermesinden bu yana 1 saniyeden fazla geçtiğinde Client Heartbeat paketi göndermek zorundadır. Sunucu istemciden uzun bir süre (tipik olarak 15 saniye) boyunca hiçbir şey almazsa mevcut soketi kapatıp yeni bir bağlantıyı dinleyebilir.

### 1.4 Oturum Sonu İşaretçisi (End of Session Marker)

Sunucu, mevcut oturumun sona erdiğini bir End of Session Message göndererek belirtir. Bu, bu oturumda başka mesaj olmayacağı anlamına gelir.

İstemci, sonraki kullanılabilir oturumun mesajlarını almaya başlamak için yeniden bağlanıp yeni Session ID ile veya boş (boşlukla doldurulmuş) Session ID ile giriş yapmak zorundadır.

### 1.5 Veri Tipleri

- Karakter veri alanları standart ASCII baytlarıdır.
- Tamsayı alanlar ikili big-endian değerlerdir.

## 2 SoupBinTCP Paket Tipleri

Her paketin ilk iki baytı `Packet Length` (Integer, big-endian; "bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı"), üçüncü bayt (offset 2) `Packet Type`'tır.

### 2.1 Debug Packet

Bir debug paketi SoupBinTCP bağlantısının her iki tarafından da herhangi bir zamanda gönderilebilir. Debug paketleri, sorunların ayıklanmasına yardımcı olabilecek, insan tarafından okunabilir metin sağlamak içindir. Debug Packet'ler hem istemci hem sunucu uygulama yazılımı tarafından **yok sayılmalıdır**.

**Debug Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "+" | Debug Packet. |
| Text (Metin) | 3 | Değişken | Alfanümerik | Serbest biçimli, insan tarafından okunabilir metin. |

### 2.2 SoupBinTCP Sunucusunun Gönderdiği Mantıksal Paketler

#### 2.2.1 Login Accepted Packet

SoupBinTCP sunucusu, istemciden geçerli bir Login Request aldığında yanıt olarak Login Accepted Packet gönderir. Bu paket, başarılı bir login isteğinden sonra sunucunun gönderdiği ilk debug-dışı paket olur.

**Login Accepted Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "A" | Login Accepted Packet. |
| Session | 3 | 10 | Alfanümerik | Şu anda giriş yapılmış oturumun Session ID'si. Soldan boşlukla doldurulmuş (left padded with spaces). |
| Sequence Number | 13 | 20 | Numeric | Gönderilecek bir sonraki Sequenced Message'ın ASCII olarak sıra numarası. Soldan boşlukla doldurulmuş. |

#### 2.2.2 Login Rejected Packet

SoupBinTCP sunucusu, istemcinin geçersiz bir Login Request Packet'ine yanıt olarak bu paketi gönderir. Sunucu, Login Reject Packet'i gönderdikten sonra soket bağlantısını kapatır. Başarısız bir login denemesinde Login Rejected Packet, sunucunun gönderdiği tek debug-dışı paket olur.

**Login Reject Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "J" | Login Rejected Packet. |
| Reject Reason Code | 3 | 1 | Alpha | Aşağıdaki Login Reject Codes'a bakın. |

**Login Reject Codes**

| Kod | Açıklama |
|---|---|
| "A" | Yetkili değil (Not Authorized). Login Request Message'da geçersiz bir kullanıcı adı ve parola kombinasyonu vardı. |
| "S" | Oturum kullanılamıyor (Session not available). Login Request Packet'teki Requested Session geçersizdi veya kullanılabilir değildi. |

#### 2.2.3 Sequenced Data Packet

Sequenced Data Packet'ler, sunucudan istemciye aktarılan asıl sıralı veri mesajlarını taşıyan bir zarf (envelope) görevi görür. Her Sequenced Data Packet üst seviye protokolden bir mesaj taşır. Her mesajın sıra numarası örtüktür; belirli bir TCP/IP bağlantısındaki ilk Sequenced Data Packet'in başlangıç sıra numarası Login Accepted Packet'te belirtilir ve sıra numarası iletilen her Sequenced Data Packet için 1 artar.

SoupBinTCP mantıksal paketleri TCP/IP soketleriyle taşındığı için mantıksal paketlerin kaybolmasının tek yolu bir TCP/IP soket bağlantısı hatasıdır. Bu durumda istemci sunucuya yeniden bağlanıp beklenen bir sonraki sıra numarasını isteyebilir ve kaldığı yerden devam edebilir.

**Sequenced Data Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "S" | Sequenced Data Packet. |
| Message | 3 | Değişken | Herhangi | Üst seviye protokol tarafından tanımlanır; ancak gömülü satır sonu (linefeed) içermemelidir. |

#### 2.2.4 Server Heartbeat Packet

Sunucu, istemciye hiçbir veri gönderilmeyen 1 saniyeden uzun her sürede Server Heartbeat Packet göndermelidir. İstemci daha sonra uzun bir süre boyunca hiçbir şey almazsa bağlantının koptuğunu varsayabilir.

**Server Heartbeat Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "H" | Server Heartbeat Packet. |

#### 2.2.5 End of Session Packet

Sunucu, mevcut oturumun bittiğini belirtmek için End of Session Packet gönderir. Bu paketten kısa bir süre sonra bağlantı kapatılır ve kullanıcı artık mevcut oturuma yeniden bağlanamaz.

**End of Session Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "Z" | End of Session Packet. |

### 2.3 SoupBinTCP İstemcisinin Gönderdiği Mantıksal Paketler

#### 2.3.1 Login Request Packet

SoupBinTCP istemcisi, sunucuyla yeni bir TCP/IP soket bağlantısı kurar kurmaz bir Login Request Packet göndermek zorundadır. İstemci ve sunucu, kullanıcı adı ve parola alanları üzerinde karşılıklı olarak anlaşmış olmalıdır. Bu alanlar, bir istemcinin yanlışlıkla yanlış sunucuya bağlanmasını önleyen basit bir kimlik doğrulama sağlar.

Hem Username hem Password büyük/küçük harfe duyarsızdır (case-insensitive) ve sağdan boşlukla doldurulmalıdır.

Sunucu, makul bir süre (tipik olarak 30 saniye) içinde Login Request Packet almazsa gelen TCP/IP soketini sonlandırabilir.

**Login Request Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "L" | Login Request Packet. |
| Username | 3 | 6 | Alfanümerik | Kullanıcı adı. |
| Password | 9 | 10 | Alfanümerik | Parola. |
| Requested Session | 19 | 10 | Alfanümerik | İstemcinin giriş yapmak istediği oturumu belirtir; ya da o an etkin oturuma giriş için tamamen boşluk. |
| Requested Sequence Number | 29 | 20 | Numeric | Bağlanıldığında istemcinin almak istediği bir sonraki sıra numarasını ASCII olarak belirtir; ya da en son üretilen mesajdan itibaren almaya başlamak için 0. |

#### 2.3.2 Unsequenced Data Packet

Unsequenced Data Packet'ler, istemciden sunucuya aktarılan asıl veri mesajlarını taşıyan bir zarf görevi görür. Bu mesajlar sıralı değildir ve soket hatası durumunda kaybolabilir. Üst seviye protokol, TCP/IP soket bağlantısı hatası durumunda bu kayıp mesajlarla başa çıkabilmelidir.

**Unsequenced Data Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "U" | Unsequenced Data Packet. |
| Message | 3 | Değişken | Alfanümerik | Üst seviye protokol tarafından tanımlanır; ancak gömülü satır sonu (linefeed) içermemelidir. |

#### 2.3.3 Client Heartbeat Packet

İstemci, sunucuya hiçbir veri gönderilmeyen 1 saniyeden uzun her sürede Client Heartbeat Packet göndermelidir. Sunucu daha sonra uzun bir süre boyunca hiçbir şey almazsa bağlantının koptuğunu varsayabilir.

**Client Heartbeat Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Integer | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "R" | Client Heartbeat Packet. |

#### 2.3.4 Logout Request Packet

İstemci, bağlantının sonlandırılmasını istemek için Logout Request Packet gönderebilir. Sunucu bir Logout Request Packet aldığında bağlantıyı hemen sonlandırır ve ilgili TCP/IP soketini kapatır.

**Logout Request Packet**

| Alan adı | Offset | Uzunluk | Değer | Notlar |
|---|---|---|---|---|
| Packet Length | 0 | 2 | Binary | Bu alandan sonra, bir sonraki pakete kadar olan bayt sayısı. |
| Packet Type | 2 | 1 | "O" | Logout Request Packet. |

## 3 Destek (Support)

SoupBinTCP spesifikasyonu hakkındaki sorular kaynakta belirtilen Nasdaq OMX geliştirici destek adresine e-postayla iletilir (adres kaynakta yazılıdır).

## 4 Mevcut Kısıtlamalar (Current Restrictions)

Bilinen yok.

## 5 Revizyon Geçmişi (Revision History)

| Sürüm | Tarih | Revizyon geçmişi |
|---|---|---|
| 1.0 | 09/01/1999 | İlk dağıtım. |
| 2.0 | 10/29/2001 | Bağlantı hatalarını tespit etmek için TCP/IP keepalive'a bağımlılığı kaldırmak üzere her iki yönde heartbeat eklendi. |
| 3.0 | tarih belirtilmemiş | Sunucu ve istemcinin ikisi de artık saniyede en az bir kez bir şey (veri veya heartbeat) göndermeyi garanti eder; böylece birkaç saniye boyunca soketten hiçbir şey duymazsanız soketin öldüğünü varsayıp kapatabilirsiniz. Hata ayıklamada işe yaradığı için Debug Message'lar eklendi (ör. sunucunun bağlantıyı kabul edince makine adını bildiren bir Debug Message göndermesi; böylece biri sunucuya TELNET ile bağlanıp doğru host'ta olduğunu hemen doğrulayabilir). |
| | 10/15/2008 | Hem çıkış yönlü Sequenced Message'ların hem de giriş yönlü Unsequenced Message'ların etrafına, heartbeat'lerden ayırt etmek için "zarflar" (envelopes) eklendi. SoupBinTCP 3.0'ın ilk dağıtımı, SoupTCP 3.0'dan alınmıştır. Paketler satır sonuyla bitirilmek yerine iki bayt uzunluk önekli; bunun dışında paket tipleri aynıdır. Login ile ilgili paketlerdeki Sequence Number alanları, 1 milyar veya daha büyük mesaj akışlarını desteklemek için genişletildi. |
| | 04/12/2011 ve 03/20/2014 | SoupTCP oturum katmanı kodunun bir SoupTCP oturumunun sonunu daha temiz algılayabilmesi için açık bir End of Session Packet eklendi. Sequenced Data Packet açıklamasından çelişen bir cümle kaldırıldı. Kullanıcının, sunucudaki mevcut en yüksek sıra numaralı mesajı aşan bir "beklenen bir sonraki sıra numarası" göndermesi senaryosunu ele alan ifade eklendi. |

---

## Çevirmenin ek notları (kaynakta yok)

- **Tutarsızlık:** Bölüm 1.1 "yük satır sonu karakterini veya herhangi bir karakteri içerebilir" der; Sequenced ve Unsequenced Data tablolarında ise mesajın "gömülü satır sonu içermemesi gerektiği" yazılıdır. Revizyon geçmişinin son girdisi "Sequenced data packet açıklamasından çelişen bir cümle kaldırıldı" der; yani bu tutarsızlık kaynağın kendi içinde kalmış olabilir. İkili ITCH mesajlarında 0x0A baytı olabileceğinden, kodda satır sonuna göre bölme yapılmamalı, `Packet Length` kullanılmalıdır (çıkarım, doğrulama gerekir).
- Login Accepted'da `Sequence Number` ve Login Request'te `Requested Sequence Number` alanları **ASCII sayı** olarak (20 karakter, boşlukla doldurulmuş) gönderilir; Packet Length ve ITCH mesajları ise ikili big-endian'dır.
- Revizyon geçmişi tablosunun satırları PDF metninde karışık sıralanmıştı (3.0 sürümüne ait tarih kaynakta belirgin değil); bu tabloda satır gruplaması çevirmen tarafından yapılmıştır.
- Bu belge GLIMPSE anlık görüntü akışının hangi ITCH mesajlarıyla başlayıp bittiğini anlatmaz; ITCH spesifikasyonundaki Appendix E ile birlikte okunmalıdır. BIST'in kullanıcı adı/parola ve oturum bilgileri bu belgede yoktur.
