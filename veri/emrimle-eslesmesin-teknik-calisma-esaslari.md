# Emrimle Eşleşmesin (Self-Match Prevention, SMP) Özelliği — Teknik Çalışma Esasları (Türkçe)

Kaynak: `kaynaklar/emrimle-eslesmesin-ozelligi-teknik-calisma-esaslari.pdf` — Borsa İstanbul, "Emrimle Eşleşmesin Özelliği (Self-Match Prevention) Teknik Çalışma Esasları", Versiyon 2, Şubat 2025, 6 sayfa. Kaynak belge Türkçedir; bu dosya kaynağın metnini sayfa sırasıyla aktarır (çeviri değil, biçimlendirilmiş aktarım). İngilizce alan adları ve değerler kaynaktaki gibidir.
Aktarım yöntemi: PDF'ten metin çıkarıldı, tablo biçimindeki değer listeleri tabloya çevrildi. Yorum eklenmemiştir.
Doğrulama: Claude tarafından kaynak metinle karşılaştırıldı; sayfa görüntüsüyle karşılaştırma yapılmadı. Kullanıcı doğrulaması: bekliyor.
Kural dosyası: bu belgedeki kurallar `../kurallar/04-surekli-islem.md` madde 34–43'te toplanmıştır.

## Dökümanın Tarihçesi [s. 2]

| Versiyon | Tarih | Değişikliklerin Özeti |
|---|---|---|
| 1 | 20/01/2025 | İlk yayım |
| 2 | 19/02/2025 | Üye defterlerinde yapılacak değişiklikler ve yeni emir değişiklik sebebine ilişkin değer bilgisi eklenmiştir. |

## Emrimle Eşleşmesin (Self-Match Prevention, SMP) Özelliği [s. 3]

Pay Piyasası ve Vadeli İşlem ve Opsiyon Piyasası'nda, algoritmik emir iletim sistemleri için Emrimle Eşleşmesin (Self-Match Prevention, SMP) özelliğinin devreye alınması planlanmaktadır. Bu özellik SMP ID ile işaretlenmiş emirlerin aynı işareti taşıyan diğer emirler ile eşleşmesini önlemek üzere geliştirilmiştir.

Emrimle Eşleşmesin özelliği, üyelerimiz tarafından yapılacak başvuru ile tercihe bağlı olarak kullanılabilecektir.

Özellik kapsamında FIX, OUCH ve TW kanallarına "SMP Seviyesi", "SMP Yöntemi" ve "SMP ID" alanları eklenmiştir. Özelliğin geçerli olabilmesi için söz konusu alanların FIX ve OUCH kanalları üzerinden emir iletiminde doldurulması gerekmekte olup emir girildikten sonra bu alanların değiştirilmesi mümkün değildir.

### SMP Seviyesi (SMP Level)

"SMP Seviyesi", Emrimle Eşleşmesin özelliğinin geçerli olacağı seviyenin (üye içi ya da üyeler arası) belirlenmesinde kullanılmaktadır.

| Alan | Değerler |
|---|---|
| SMP Seviyesi (SMP Level) | 1: Üye içinde<br>2: Üyeler arasında |

Emrimle Eşleşmesin özelliğinin tetiklenebilmesi için SMP Seviyesinin potansiyel eşleşmenin her iki tarafındaki emir için aynı değere (1 veya 2) sahip olması gerekmektedir. SMP seviyesi 1 seçildiğinde özellik sadece aynı üye tarafından iletilen emirler arasında, 2 seçildiğinde ise üyenin kendisi dahil tüm üyeler arasında geçerli olur.

### SMP Yöntemi (SMP Method)

"SMP Yöntemi", Emrimle Eşleşmesin özelliğinin tetiklenmesi durumunda, sistemin potansiyel eşleşmenin önüne geçmek için alacağı aksiyonu belirtir.

| Alan | Değerler |
|---|---|
| SMP Yöntemi (SMP Method) | 1: Agresif emri iptal et<br>2: Pasif emri iptal et<br>3: Her iki emri iptal et |

Potansiyel eşleşmenin önüne geçilmesi için;
- agresif emrin (daha sonra girilmiş olan emrin) iptal edilmesi tercih ediliyorsa 1,
- pasif emrin (defterde bekleyen emrin) iptal edilmesi tercih ediliyorsa 2,
- hem pasif hem agresif emrin iptal edilmesi tercih ediliyorsa 3 değerinin kullanılması gerekmektedir.

Farklı SMP Yöntemi belirlenmiş emirlerin potansiyel bir eşleşmeye konu olması durumunda agresif emirde belirtilen SMP Yöntemi geçerli olur. [s. 3–4]

### SMP ID [s. 4]

SMP ID, üç haneli, büyük-küçük harfe duyarlı, alfanümerik bir değerdir. Özelliğin tetiklenmesi için, SMP ID'nin potansiyel eşleşmenin her iki tarafındaki emir için aynı değere sahip olması gerekmektedir.

Emrimle Eşleşmesin özelliğinin yalnızca aynı üyeye ait emirler arasında kullanılması isteniyorsa (SMP Seviyesi: 1) SMP ID emir ileten üye tarafından belirlenir. Özelliğin farklı üyeler tarafından iletilen emirler arasında da kullanılmasının (SMP Seviyesi: 2) istenmesi durumunda ise SMP ID Borsa tarafından belirlenir.

### Geçerli seans bölümleri ve emir tipleri [s. 5]

Emrimle Eşleşmesin özelliği sadece sürekli işlem yönteminin uygulandığı seans bölümlerinde geçerlidir. Dolayısıyla tek fiyat işlem yönteminin uygulandığı seans bölümlerinde özelliğin kullanımı mümkün değildir. Tek fiyatlı seans bölümlerinde SMP alanları dolu olarak emir iletilmesi halinde emir sisteme kabul edilecek ancak özellik tetiklenmeyecektir. Tek fiyatlı seans bölümlerinde girilen ilgili emrin sürekli işlem seans bölümüne taşınması halinde özellik tetiklenebilir duruma geçecektir.

Özellik yalnızca Limit Emirler ile Gün ve Kalanı İptal Et geçerlilik sürelerinde kullanılabilir. Piyasa ve Piyasadan Limite Emirler, Özel İşlem Bildirimleri, Vadeler Arası Strateji Emirleri, Şarta Bağlı Emirler, Kısmi Görünme Koşullu Emirler, Dengeleyici Emirler ve Orta Nokta Emirlerde kullanılamayacaktır.

### Devreye alınma ve değişiklikler [s. 5–6]

Emrimle Eşleşmesin özelliği 3.12 servis güncellemesi ile birlikte teknik olarak devreye alınacak ancak kullanılmaya başlanabileceği tarih daha sonra duyurulacaktır. Bununla birlikte 3.12 geçişi ile bu özellik kullanıma açılmasa dahi mesajlara eklenen yeni alanların üyelerimizin sistemlerine tanıtılması gerekmektedir. Özelliğin devreye alımı kapsamında FIX, OUCH ve TW kanallarında ve üye defterlerinde aşağıda belirtilen değişiklikler yapılacak olup, veri bildirim kabul formatlarında emir değişiklik sebeplerine yeni bir değer eklenecektir. Söz konusu değişiklikler özelliği kullanmayacak olanlar dahil tüm piyasa katılımcılarını etkileyeceğinden detaylı test edilmesi gerekmektedir:

- FIX Order Entry 'New Order Single (MsgType=D)' ve 'Execution Report (MsgType=8)' mesajlarına 'SMP Level (tag=21114)', 'SMP Method (tag=21115)' ve 'SMP ID (tag=21116)' alanları eklenecektir. FIX Drop Copy execution mesajlarında da ilgili alanlar yer alacaktır.
- OUCH "Enter Order" ve "Order Accepted" mesajlarına "SMP Level", "SMP Method" ve "SMP ID" alanları eklenecektir.
- BISTECH İşlem Terminali (TW) uygulamasında 'Emir Defteri' ve 'Emir Geçmişi' pencerelerine 'SMP Level', 'SMP Method' ve 'SMP ID' alanları eklenecektir.
- Emir iptal ve ret mesajlarına Emrimle Eşleşmesin özelliği nedeniyle iptal edilen ve reddedilen emirler için ilgili açıklamalar eklenecektir.
- Pay Piyasası için Tüm Emir Defteri'ne ve Borsa Payına Esas Emir İptal ve Değişiklik Defteri'ne "SMP Seviyesi", "SMP Yöntemi" ve "SMP ID" alanları eklenecektir.
- Vadeli İşlem ve Opsiyon Piyasası için VİOP Tüm Emir Defteri, VİOP Akşam Seansı Tüm Emir Defteri ve Filtresiz Emirler Raporu dosyalarına "SMP Seviyesi", "SMP Yöntemi" ve "SMP ID" alanları eklenecektir.
- EMİR DEĞİŞİKLİK SEBEBİ alanına Emrimle Eşleşmesin özelliği nedeniyle gerçekleşen emir iptallerini gösteren yeni bir değer eklenecektir. (OrderDeletedDueToSMP - ChangeReason: 46)

Emrimle Eşleşmesin özelliğine ilişkin devreye alınacak mesaj güncellemelerine ilişkin detaylara ve bu özellik nedeni ile iptal edilen ve reddedilen emirler için oluşturulan yeni hata kodlarına Borsa İstanbul web sitesinde yer alan Teknik Dokümanlar sekmesinden erişilebilir. (https://www.borsaistanbul.com/tr/sayfa/441/teknik-dokumanlar).
