# MoldUDP64 Protokol Spesifikasyonu (Türkçe çeviri)

Kaynak: `moldudp64-protocol-specification.pdf` — "MoldUDP64 Protocol Specification", Sürüm 1.0, belge sürümü 1.00, yayın tarihi 2009-07-07, 8 sayfa. Gizlilik: "Non-confidential" (kapak sayfası). Telif: The NASDAQ OMX Group, Inc.
Çeviri yöntemi: Metin Claude tarafından Türkçeye çevrilmiştir (PDF metni `pdftotext` ile alındı; belge kısa olduğu için tablolar elle yeniden yazıldı). Alan adları, değer tipleri (`ANUM`, `NUM`) ve sabitler çevrilmeden bırakılmış, Türkçe karşılıkları parantez içinde verilmiştir. Offset ve uzunluklar bayt cinsindendir ve kaynakla aynıdır.
Doğrulama: Sayfa görüntüsüyle karşılaştırma yapılmadı. Başlık tablosunun PDF metin çıkarımı karışıktı; offset/uzunluk eşleşmesi (0/10, 10/8, 18/2) alan adı sırası, sonraki metindeki "başlık paketin başından 20 bayttır" ifadesi ve 10+8+2 = 20 toplamıyla çapraz kontrol edildi. Kullanıcı doğrulaması: bekliyor.
İlgili dosya: `bistech-itch-protokol-spesifikasyonu.md` (Appendix E: ITCH mesajları MoldUDP64 ile taşınır; REWINDER MoldUDP64 kullanır).

---

## Adresleme (Addressing) [s. 3]

> **Not:** NASDAQ OMX MoldUDP ve MoldUDP64 protokol veri akışlarının güncel IP adresleri listesi için kaynakta http://www.nasdaqtrader.com/Trader.aspx?id=FeedIPS adresine yönlendirilir. (BIST ITCH için IP/port bilgisi bu belgede yoktur.)

## Genel Bakış (Overview) [s. 3]

MoldUDP64, "bir vericiden çok dinleyiciye" senaryosunda veri mesajlarının verimli ve ölçeklenebilir iletimini sağlayan bir ağ protokolüdür. MoldUDP64, UDP üzerine kurulu hafif bir protokol katmanıdır; dinleyicilere kaçırılan paketleri tespit etme ve yeniden isteme mekanizması sağlar.

MoldUDP64'te her çıkış yönlü paket, dinleyici sayısından bağımsız olarak yalnızca bir kez iletilir. Ağ trafiğini azaltmak için birden fazla mesaj tek bir ağ paketinde birleştirilebilir. Uzak alıcıların yakınına, WAN bağlantılarındaki gecikmeyi ve bant genişliğini azaltmak için isteğe bağlı önbellekli yeniden-istek sunucuları (Re-request Server) yerleştirilebilir.

Bu belge, bir MoldUDP64 sunucusu ile istemcileri arasında gönderilen mesajları tanımlar. MoldUDP64 vericileri, dinleyicilere normal veri akışını taşımak için UDP multicast ile Downstream (aşağı yönlü) paketler gönderir. Bu paketler, bir dinleyicinin gönderdiği Request (istek) mesajına yanıt olarak UDP unicast ile de gönderilir. MoldUDP64 istemcileri, veri akışındaki istedikleri paketlerin yeniden iletilmesini istemek için bu Request mesajlarını gönderebilir.

MoldUDP64 sunucusu, bir ağdaki her aşağı yönlü MoldUDP64 veri akışı tipi için bilinen bir multicast grubunda yayın yapar. Dinleyiciler aşağı yönlü veriyi almak için bu multicast grubuna abone olmalıdır. Belirli mesajların yeniden iletimi için gelen unicast istemci isteklerine hizmet vermek üzere bir veya daha fazla Re-request Server da konuşlandırılabilir. Dinleyiciler, isteklerini gönderebilecekleri bu IP adresi ve port kombinasyonlarıyla yapılandırılmalıdır.

## Varsayımlar (Assumptions) [s. 3]

Bu belgede belirtilen MoldUDP64 mesajlarındaki tüm sayı alanları (yani sıra numarası, mesaj sayıları ve mesaj uzunlukları vb.) **Big Endian** (önce en anlamlı bayt) biçimli ikili sayılardır. Not: Bu durum, Message Block'ların Message Data alanlarında bulunan veriler için geçerli olmak zorunda değildir.

## Terimler (Terms) [s. 3–5]

### Mesaj (Message)

Mesaj, MoldUDP64 protokolünün taşıdığı atomik bir bilgi parçasıdır. MoldUDP64 teorik olarak sıfır bayttan 64 KB'a kadar uzunluktaki tekil mesajları işleyebilir; ancak, tekil mesajların, ortaya çıkan MoldUDP64 paketlerinin altta yatan UDP ağ protokolü tarafından verimli taşınabilmesi için yeterince küçük tutulması gerekir.

Bir MoldUDP64 mesajının içeriği üst seviye uygulama tarafından tanımlanır.

### Oturum (Session)

Oturum, bir veya daha fazla mesajdan oluşan bir dizidir. Tek bir oturum süresiz sürebilse de uygulama tipik olarak oturumu, mesajları zaman sınırlamasına göre mantıksal olarak gruplamak için tanımlar.

Bir oturum sonlandırıldığında o oturumda daha fazla mesaj gönderilemez. MoldUDP64 sisteminin ve uygulamanın tasarımına bağlı olarak alıcılar, sonlandırılmış bir oturumdaki mesajları yine de yeniden isteyebilir. Bir oturum başlamış ancak henüz sonlandırılmamışsa etkin (active) sayılır.

### Aşağı Yönlü Paket (Downstream Packet) [s. 4–5]

Bir MoldUDP64 vericisi, MoldUDP64 dinleyicilerinin aldığı "aşağı yönlü" paketler gönderir. Bir MoldUDP64 paketi 0 veya daha fazla veri akışı mesajı içeren bir yük (payload) taşıyabilir.

Her MoldUDP64 paketi, bir Downstream Packet Header (başlık) ve bir dizi Message Block'tan oluşur. Message Block'lar akışın asıl verisini taşır.

#### Başlık (Header)

**Downstream Packet Header**

| Alan adı | Offset | Uzunluk | Değer tipi | Notlar |
|---|---|---|---|---|
| Session (Oturum) | 0 | 10 | ANUM | Paketin ait olduğu oturumu belirtir. |
| Sequence Number (Sıra numarası) | 10 | 8 | NUM | Paketteki ilk mesajın sıra numarası. |
| Message Count (Mesaj sayısı) | 18 | 2 | NUM | Bu pakette bulunan mesajların sayısı. |

(`ANUM` = alfanümerik, `NUM` = sayısal/ikili; kaynakta tanımı ayrıca verilmemiştir.)

**Sequence Number:** Paket başlığındaki Sequence Number alanı, paketteki ilk mesajın sıra numarasını belirtir. Pakette birden fazla mesaj varsa ilk mesajı izleyen mesajlar örtük (implicit) olarak sırayla numaralandırılır.

**Message Count:** Bir MoldUDP64 paketindeki Message Block sayısı, paket başlığındaki Message Count alanıyla belirtilir. Bir Downstream Packet'in en büyük yük (payload) boyutu gönderici tarafından belirlenir. **Message Count sıfır ise paket bir kalp atışıdır (heartbeat); Message Count 0xFFFF (onaltılık, ondalık 65535) ise oturumun sonunu belirtir.**

### Mesaj Bloğu (Message Block) [s. 6]

Bir Message Block'un ilk alanı iki baytlık Message Length'tir (mesaj uzunluğu). Message Block'un geri kalanı değişken uzunluklu Message Data alanıdır. İlk Message Block alanı her zaman Header'ın hemen ardından başlar; Header paketin başından itibaren 20 bayttır. Sonraki Message Block'lar bir önceki Message Block'un son baytından sonra başlar.

**Downstream Packet Message Block**

| Alan adı | Offset | Uzunluk | Değer tipi | Notlar |
|---|---|---|---|---|
| Message Length (Mesaj uzunluğu) | * | 2 | NUM | Bu Message Block'taki mesajın bayt cinsinden uzunluğunu belirtir. |
| Message Data (Mesaj verisi) | * | * | ANUM | Mesaj verisi. |

`*` = değişken değerler.

**Message Length:** İşaretsiz ikili sayıdır; bu Message Length alanını izleyen mesaj veri baytlarının sayısını gösterir. Message Length alanı değeri, Message Length alanının kapladığı iki baytı **içermez**. Message Block'un toplam boyutu, Message Length alanının değeri artı ikidir.

**Message Data:** MoldUDP64'ün ilettiği mesajın asıl verisidir. Değişken uzunluktadır ve sıfır uzunlukta olabilir. Verinin anlamı uygulamaya özgüdür.

### Kalp Atışları (Heartbeats) [s. 6]

Kalp atışları sunucu tarafından periyodik gönderilir; böylece alıcılar düşük trafik zamanlarında bile paket kaybını algılayabilir. Bu paketler tipik olarak saniyede bir iletilir ve bir sonraki beklenen Sequence Number'ı içerir. Heartbeat paketi, Message Count'u sıfır olan bir MoldUDP64 paketidir.

### Oturum Sonu (End of Session) [s. 6]

Mevcut oturum tamamlandığında, kısa bir süre boyunca Heartbeat yerine Message Count'u 0xFFFF (onaltılık, ondalık 65535) olan Downstream Packet'ler gönderilir. Bu Downstream Packet'ler de Heartbeat'ler gibi bir sonraki beklenen Sequence Number'ı içerir. End of Session mesajları sürdüğü sürece mevcut oturumda yeniden istek yapılabilir. Bu, tüm mesajların alındığından emin olmak için son fırsattır.

### İstek Paketi (Request Packet) [s. 6–7]

Request Packet, belirli bir mesajın veya mesaj grubunun yeniden iletilmesini istemek için gönderilir. Request Packet bir Re-request sunucusuna gönderilir. Alıcı, alınan mesajlarda sıra numarası boşluğu (gap) tespit ettiğinde bu isteği göndermek zorunda kalabilir. Geçerli bir Request Packet'e yanıt, yeniden iletim isteğinin kaynağına geri gönderilen standart bir Downstream Packet'tir (unicast). Böylece, istek multicast işleme soketinden yapıldıysa, aşağı yönlü MoldUDP64 kullanıcıları yeniden iletilen Downstream Packet'i kendi multicast işleme soketlerinden okuyabilir; yani istemcinin hem multicast'i dinlemek hem de yeniden iletimleri işlemek için yalnızca bir soket açık tutması yeterlidir (yeniden iletimler multicast olmasa da).

**Request Packet**

| Alan adı | Offset | Uzunluk | Değer tipi | Notlar |
|---|---|---|---|---|
| Session | 0 | 10 | ANUM | Paketin ait olduğu oturumu belirtir. |
| Sequence Number | 10 | 8 | NUM | İstenen ilk sıra numarası. |
| Requested Message Count (İstenen mesaj sayısı) | 18 | 2 | NUM | Yeniden iletilmesi istenen mesajların sayısı. |

**Sequence Number:** Paket başlığındaki Sequence Number alanı, istenen ilk mesajın sıra numarasını belirtir.

**Requested Message Count:** Kaç mesajın yeniden iletilmesi gerektiğini belirtir. İstenen mesajların toplam boyutu tek bir UDP paketinin en büyük yük boyutunu aşıyorsa, yalnızca tamamen sığan mesaj sayısı kadarı döndürülür. Sonraki mesajlar hâlâ isteniyorsa ek yeniden iletim istekleri yapılmalıdır.

### Alıcı Örneği (Receiver Example) [s. 8]

Tipik bir MoldUDP64 alıcı istemcisi şu parametrelerle yapılandırılır:

- Dinlenecek UDP portu ve katılınacak Multicast grubu.
- Bu akış için yeniden iletim isteklerine yanıt verebilecek bir veya daha fazla Request Server listesi. Her sunucu, isteklerin gönderileceği bir host IP adresi ve UDP portu olarak belirtilir.
- İstemci yeniden başlatılıyorsa, beklenen bir sonraki mesajın oturumu ve sıra numarası.

Tipik bir MoldUDP64 alıcı istemcisi şu akış şemasına uyabilir:

1. İlgili port için bir UDP soketi aç ve istenen multicast grubuna katıl.
2. Şu anda etkin olan oturumu belirlemek için alınan ilk paketi incele.
3. Alınan oturum beklenen oturumla eşleşmiyorsa durdur (abort) ve hatayı bildir.
4. Yakın zamanda alınan ilk paketin sıra numarasını incele.
5. Sıra numarası beklenen bir sonraki sıra numarasıyla eşleşmiyorsa, beklenen paket numarasıyla Request Server'a bir Request Packet gönder. Yeni bir paket bekle ve 4. adıma dön.
6. Paketteki alınan her mesajı işle. Message Count'u End of Session olarak ayarlanmış bir Downstream Packet alınırsa End of Session olayını işle.
7. Yeni bir paket bekle ve 4. adıma dön.

---

## Çevirmenin ek notları (kaynakta yok)

- **Paket yerleşimi özeti** (başlık offset'lerinden ve Message Block tanımından çıkarım): Downstream paket = 20 baytlık başlık (Session 10 + Sequence Number 8 + Message Count 2) + `Message Count` adet blok; her blok = 2 baytlık Message Length + o uzunlukta Message Data. Bu özet kaynak metindeki ifadelerden türetilmiştir ve `.VRD` ikili dosyası üzerinde ayrıca doğrulanmalıdır.
- Oturum alanı 10 baytlık ANUM'dur. ITCH spesifikasyonu veya bu belge Session alanının doldurma (padding) kuralını yazmaz. Doldurmanın boşlukla olup olmadığı örnek ikili dosyada doğrulanmalıdır.
- Bu belge ITCH mesajlarının kendisini (`T`, `R`, `A`...) tanımlamaz; onlar için bkz. `bistech-itch-protokol-spesifikasyonu.md`.
- REWINDER'ın yeniden oynatma paketlerinin 1440 bayt olduğu bilgisi ITCH spesifikasyonu Appendix E'de geçer; bu belgede bu sınır yoktur (gönderici belirler).
