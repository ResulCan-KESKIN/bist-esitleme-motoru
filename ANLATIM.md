# Sistemin anlatımı (sıfırdan, ayrıntılı)

Bu belge projeyi hiç bilmeyen birinin baştan sona anlayabilmesi için yazıldı. Hiçbir ön bilgi varsayılmaz: borsa kavramları, istatistik (ortalama, standart sapma, Z-skor), makine öğrenmesi (model, eğitim, karar ağacı, Isolation Forest) ve değerlendirme ölçütleri (ROC-AUC, kesinlik, duyarlılık) sayılı örneklerle anlatılır. Her yöntem için şu dört soru cevaplanır:

1. Bu nedir?
2. Nasıl hesaplanır (elle yapılabilecek bir örnekle)?
3. Bu projede neden kullanıldı?
4. Neyi yapamaz?

Belgedeki sayılar Mart 2025 verisinden ve 24.10.2026 tarihli son koşulardandır. Ayrıntılı kayıt `rapor.md`, tasarım `TASARIM.md`, güncel durum `DURUM.md` dosyasındadır.

**Okuma sırası önerisi:** bölüm 0 → 1 (borsa) → 2 (fikir) → 3–4 (veri ve motor) → 5 (sentetik manipülasyon) → 6 (istatistik ve makine öğrenmesi temelleri, en uzun bölüm) → 7 (tespit sistemimiz) → 8 (sonuçlar) → 9–13.

---

## 0. Büyük resim

### 0.1 Tek paragrafta proje

Borsa İstanbul'un gerçek emir kayıtlarını alıyoruz (Mart 2025, her emrin her olayı, ayda 1,1 milyar satır). Bu emirleri, Borsa İstanbul Pay Piyasası Prosedürü'ndeki kurallarla yazdığımız kendi **eşleştirme motorumuza** tek tek veriyoruz. Motor, borsanın gerçekte ürettiği işlemleri %99,85 oranında birebir aynı üretiyor. Böylece elimizde gerçek piyasanın bir "laboratuvar kopyası" oluyor. Bu kopyanın içine kendi uydurduğumuz bir **sentetik manipülatörün** emirlerini ekliyoruz: kapanış fiyatını itmek, sahte emirle baskı yapmak, fiyatı adım adım yükseltmek, kendi kendine işlem yapmak. Sonra **tespit yöntemlerinin** bu manipülasyonu yakalayıp yakalayamadığını ölçüyoruz: iktisadi kurallar, Z-skor, Isolation Forest, denetimli makine öğrenmesi. Ayrıca SPK bültenlerinden çıkardığımız gerçek manipülasyon vakalarıyla da ölçüyoruz.

### 0.2 Neden böyle bir düzen

Gerçek borsa verisinde iki şey yoktur:
- **"Bu emir manipülasyondu" etiketi.** Bir yöntemin işe yarayıp yaramadığını ölçmek için doğru cevabı bilmek gerekir.
- **Kimin emir verdiği** (üye, hesap). Bu yüzden "şu kişi manipülasyon yaptı" diyemeyiz.

Çözümümüz: manipülasyonu kendimiz, bilinen bir yere, bilinen büyüklükte koyarız. Doğru cevabı biz bildiğimiz için tespit yöntemini dürüstçe sınayabiliriz. Bunu yapabilmek için gerçek piyasayı aynen üreten bir motor gerekir. Motoru gerçek işlemlerle karşılaştırarak doğruluğunu da kanıtlarız.

### 0.3 Akış şeması

```
DataStore verisi (Mart 2025)
   │  emir olayları (yeni / değişiklik / iptal)
   ▼
EŞLEŞTİRME MOTORU (motor/) ──► motorun işlemleri ──► gerçek işlemlerle karşılaştır (%99,85 aynı)
   ▲
   │  + sentetik manipülatörün emirleri (motor/senaryolar.py)
   ▼
ENJEKSİYONLU OYNATMA ──► özellikler (tespit/) ──► puanlar (kurallar, Z-skor, Isolation Forest, model)
                                                    │
                                                    ▼
                      DEĞERLENDİRME: manipülasyonu koyduğumuz yer en yüksek puanı aldı mı?
                      + SPK vakaları: gerçek manipülasyon günleri yüksek puan aldı mı?
                                                    │
                                                    ▼
                      GÖRSELLEŞTİRME (arayuz/): fiyat grafiği, sentetik işlemler, uyarılar
```

---

## 1. Borsa kavramları (en baştan)

### 1.1 Emir, işlem, emir defteri

- **Pay (hisse):** bir şirketin ortaklık payı. Borsada her pay bir **işlem sırası**dır, ör. `THYAO.E`. `.E` pay sırası demektir.
- **Lot:** işlem birimi. Paylarda 1 lot = 1 pay.
- **Emir:** "şu paydan şu fiyattan şu kadar almak/satmak istiyorum" talimatı. Alış ya da satış yönlüdür.
- **İşlem:** bir alış emriyle bir satış emrinin eşleşmesi. İşlemin bir fiyatı ve bir miktarı (adedi) vardır.
- **Emir defteri:** henüz işlem görmemiş, bekleyen emirlerin listesi. İki tarafı vardır:
  - alış tarafı en yüksek fiyattan aşağı doğru sıralanır;
  - satış tarafı en düşük fiyattan yukarı doğru sıralanır.
- **En iyi alış / en iyi satış:** alış tarafının en yüksek fiyatı ve satış tarafının en düşük fiyatı.
- **Makas (spread):** en iyi satış − en iyi alış.

Örnek defter (Prosedür Ek-18'den; birim testlerimizde de var):

| Alış miktarı | Alış fiyatı | Satış fiyatı | Satış miktarı |
|---|---|---|---|
| 100 | 10,50 | 11,00 | 80 |
| 90 | 10,45 | 11,05 | 90 |
| 80 | 10,40 | 11,10 | 100 |

En iyi alış 10,50, en iyi satış 11,00, makas 0,50 TL. Kimse 10,50'den fazla vermek, kimse 11,00'den ucuza satmak istemiyor; bu yüzden şu an işlem yok.

### 1.2 Fiyat adımı, baz fiyat, taban / tavan

- **Fiyat adımı:** fiyat her değeri alamaz. 10 TL civarındaki bir pay 10,00 / 10,01 / 10,02 olabilir, 10,005 olamaz. Adım fiyata göre değişir (Prosedür Tablo-7):

  | Fiyat aralığı (TL) | Adım (TL) |
  |---|---|
  | 0–20 | 0,01 |
  | 20–50 | 0,02 |
  | 50–100 | 0,05 |
  | 100–250 | 0,10 |
  | 250–500 | 0,25 |
  | 500–1000 | 0,50 |
  | 1000–2500 | 1,00 |
  | 2500 ve üstü | 2,50 |

- **Baz fiyat:** günün referansı; normalde bir önceki günün kapanış fiyatı.
- **Fiyat marjı (taban / tavan):** fiyat gün içinde baz fiyattan en çok belli bir oranda uzaklaşabilir. Yürürlükteki metinde Yıldız Pazar için %20'dir. **Mart 2025 verisinde ise bütün pazarlarda ±%10 uygulandığını ölçtük:** 495 tavan ve 786 taban isabeti var. Sınırlar "içe" yuvarlanır: taban bir üst adıma, tavan bir alt adıma.

### 1.3 Emir türleri

| Tür | Ne demek | Motorda ne olur |
|---|---|---|
| Limit | "En kötü şu fiyattan" (alışta en çok, satışta en az) | Uygun fiyatlı karşı seviyelerle eşleşir, kalanı deftere yazılır |
| Piyasa | Fiyat yok; karşı taraftaki bütün seviyelerden alır/satar | Kalanı iptal edilir |
| Piyasadan limite | Fiyat yok; yalnız karşı taraftaki **en iyi** seviyeden işlem görür | Kalanı o işlem fiyatından limit emre döner; karşı taraf boşsa iptal edilir |
| KİE (kalanı iptal et) | Geçerlilik türü: ne işlem görürse görsün, kalanı hemen iptal | Deftere yazılmaz |
| GÜN | Geçerlilik türü: gün sonuna kadar defterde bekler | Varsayılan |
| Kısmi görünme (iceberg) | Miktarın yalnız bir kısmı (tepe) defterde görünür; o kısım bitince yenisi açılır | Yenilenen kısım seviyenin sonuna geçer |
| Dengeleyici | Yalnız müzayedede; fiyat hesabına girmez, açıkta kalan emirleri karşılar | Fiyat belirlendikten sonra eşleşir, kalanı iptal edilir |

Açığa satış (elde olmayan payı satmak) Mart 2025'te 21 Mart'a kadar yalnız BIST 50 paylarında serbestti, 24 Mart'tan itibaren yasaktı. Bunu da veriden ölçtük.

### 1.4 Fiyat-zaman önceliği

Sürekli işlemde emirler iki kurala göre sıraya girer:
1. **Fiyat önceliği:** daha iyi fiyat (alışta yüksek, satışta düşük) önce işlem görür.
2. **Zaman önceliği:** aynı fiyatta önce gelen önce işlem görür.

Bir emir değiştirilirse önceliği ne olur? Veriden öğrendiklerimiz (uyum %99,76):
- fiyat değişirse öncelik kaybolur (emir yeni gibi sona geçer);
- kalan miktar artırılırsa öncelik kaybolur;
- miktar azaltılırsa öncelik korunur;
- kısmi görünme emrinin görünen kısmı yenilenirse yenilenen kısım sona geçer;
- AFK (aracı kurum / fon kodu) alanı dolu emirde fiyatı ve miktarı değişmeyen bir değişiklik bile önceliği kaybettirir.

Önemli bir bulgu: verideki `emir_giris_zamani` alanı öncelik zamanı **değildir**; emir ömrü boyunca hiç değişmez. Öncelik zamanını olay dizisinden kendimiz türetiyoruz.

### 1.5 İki işlem yöntemi: sürekli işlem ve tek fiyat (müzayede)

- **Sürekli işlem:** emir geldiği anda karşı taraftaki uygun emirlerle eşleşir. İşlem, **defterde bekleyen emrin fiyatından** olur. Gelen emre **aktif** (agresif), bekleyene **pasif** taraf denir.
- **Tek fiyat (müzayede):** bir süre emirler toplanır, hiç eşleşme olmaz. Sonra bütün emirler **tek bir denge fiyatından** eşleşir. Açılışta, kapanışta ve devre kesiciden sonra kullanılır. Amacı, bir anda gelen çok sayıda emir için adil tek bir fiyat bulmaktır.

### 1.6 Bir işlem günü (tam gün, standart pay akışı)

| Saat | Bölüm (veride seans adı) | Ne olur |
|---|---|---|
| 09:40 | Açılış emir toplama (`P_ACILIS_EMIR_TPL`) | Emir toplanır, eşleşme yok |
| 09:50 | Bazı sıralarda iptal / azaltma / fiyat kötüleştirme yasak (`..._EIY`) | Son dakikada sahte emri çekip açılışı yanıltmayı önler |
| 09:55 | Eşleştirme (`P_ESLESTIRME`) | Açılış fiyatı belirlenir; an, aşamanın başında rastlantısal bir saniyedir |
| 10:00 | Sürekli işlem (`P_SUREKLI_ISLEM`) | Gün içi işlemler |
| 18:01 | Kapanış emir toplama (`P_KAPANIS_EMIR_TPL`) | Fiyatlar son işlem fiyatının ±%3'üyle sınırlı |
| 18:05 | Eşleştirme (`P_ESLESTIRME`) | Kapanış fiyatı belirlenir |
| 18:08 | Kapanış fiyatından işlemler (`P_KAPANIS_FIY_ISLEM`) | Yalnız kapanış fiyatından emir; 2 dakika |
| 18:19 | Gün sonu (`P_GUNSONU`) | Kalan emirler süre dolumuyla kapanır |

Dikkat: açılış ve kapanış eşleştirmesinin ikisinin de adı `P_ESLESTIRME`'dir. Bu ayrıntı bölüm 11'deki en önemli hatanın kaynağıydı.

Emirler gün içinde yaşar, ertesi güne geçmez. Bu yüzden her gün bağımsız oynatılabilir; önceki günden yalnız baz fiyat gelir.

### 1.7 Denge fiyatı nasıl bulunur (müzayede algoritması)

Prosedür 5.2.2.2.1'deki adımlar:
1. Her aday fiyatta "o fiyattan ya da daha iyisinden almak isteyenler" (D) ve "o fiyattan ya da daha iyisinden satmak isteyenler" (S) toplanır. O fiyatta işlem görebilecek miktar min(D, S)'dir. **En çok işlem miktarını** veren fiyat seçilir.
2. Birden çok fiyat eşitse, **arta kalan miktarı** (|D − S|) en az olan seçilir.
3. Hâlâ eşitse **piyasanın yönüne** bakılır: kalan miktar alış yönündeyse en yüksek, satış yönündeyse en düşük aday seçilir.
4. Hâlâ eşitse **referans fiyata** en yakın aday seçilir. Mart 2025 verisinde referansın baz fiyat olduğunu ölçtük (146 vakanın 144'ü).
5. Referans yoksa en yüksek ve en düşük adayın ortalaması alınır ve en yakın adıma yuvarlanır.

Adaylar, en düşük limit fiyatın bir adım altından en yüksek limit fiyatın bir adım üstüne kadar, taban/tavan içindeki bütün geçerli fiyatlardır. Piyasa emirleri her fiyatta sayılır, dengeleyici emirler sayılmaz.

**Sayısal örnek** (motorun birim testindeki defter; fiyat adımı 0,01):

| Taraf | Emir | Fiyat | Miktar |
|---|---|---|---|
| Alış | B1 | piyasa | 50 |
| Alış | L1 | 10,10 | 40 |
| Alış | L2 | 10,00 | 30 |
| Alış | L3 | 10,10 | 20 |
| Satış | S1 | 10,00 | 60 |
| Satış | S2 | 9,90 | 30 |
| Satış | S3 | 10,20 | 50 |

| Aday fiyat | D (alıcı) | S (satıcı) | İşlem min(D, S) | Kalan D − S |
|---|---|---|---|---|
| 9,90 | 140 | 30 | 30 | +110 |
| 10,00 | 140 | 90 | **90** | +50 |
| 10,01 … 10,10 | 110 | 90 | **90** | **+20** |
| 10,11 | 50 | 90 | 50 | −40 |
| 10,20 | 50 | 140 | 50 | −90 |

Nasıl okunur: 10,00'da alıcılar piyasa emri (50) + 10,00 ve üstündeki bütün limitler (40 + 30 + 20) = 140; satıcılar 10,00 ve altındakiler (60 + 30) = 90. İşlem görebilecek miktar 90'dır.

- Adım 1: 90 lotu 11 fiyat verir (10,00–10,10).
- Adım 2: kalan miktar 10,01–10,10 arasında en azdır (20); 10 aday kalır.
- Adım 3: kalan alış yönündedir (+20), en yüksek aday seçilir: **10,10**.

Dağıtım: alış tarafı önce piyasa emirleri, sonra limitler fiyat ve zaman sırasıyla dizilir (B1, L1, L3). L2 (10,00) denge fiyatının altında kaldığı için katılmaz. Satış tarafı S2, S1 olarak dizilir; S3 (10,20) katılmaz. İki liste baştan yürünür: B1–S2 30 lot, B1–S1 20 lot, L1–S1 40 lot. Toplam 90 lot, hepsi 10,10'dan. L3 (20), L2 (30) ve S3 (50) sürekli işleme aktarılır.

"İki liste baştan yürünür" dağıtım biçimi Prosedür'de açık yazmıyordu; veriden öğrendik. THYAO 03.03.2025 açılışındaki 1.872 işlemin tamamı bu sırayla çıkıyor.

### 1.8 Devre kesiciler

- **Pay bazında devre kesici (DK):** bir payın fiyatı son müzayede fiyatından belli bir oranda uzaklaşırsa o payda sürekli işlem durur ve kısa bir müzayede yapılır. Panik anında fiyatın birkaç saniyede çökmesini önler. Mart 2025 verisinde:
  - yalnız düşüşte tetiklenir, eşik %5'tir;
  - 15 dakika emir toplama ve 2 dakika eşleştirme bölümü vardır; eşleştirme, bölümün ilk 30 saniyesinde rastlantısal bir anda yapılır;
  - 17:40'tan sonra tetiklenirse doğrudan kapanış müzayedesine aktarılır;
  - 1.184 olayın tamamı düşüş yönündedir.

  Yürürlükteki metin ise iki yönlü ve %10 / %7,5 / %5 der. Bu fark tarih parametresi olarak tutulur (bölüm 3.3).
- **Endekse bağlı devre kesici (EBDKS):** BIST 100 endeksi belli oranda düşerse bütün piyasa durur. Mart 2025'te iki eşik vardı (%5 ve %7). 19 ve 21 Mart'ta ikişer kez çalıştı. Durdurma paylarda 20 dakikadır, ardından tek fiyat müzayedesi yapılır.

### 1.9 Manipülasyon nedir, hangi türleri ele alıyoruz

SPK'nın VI-104.1 sayılı Piyasa Bozucu Eylemler Tebliği'nin 5. maddesi, fiyatı veya hacmi yanıltacak nitelikteki eylemleri sayar. Bentleri ve bizim karşılığımız:

| Bent | Eylem | Bizdeki senaryo / gösterge |
|---|---|---|
| a | Emir verme, iptal, değiştirme (yanıltıcı) | Yanıltıcı emir (spoofing); iptal oranı |
| b | Farklı fiyat kademelerine emir | Katmanlı yanıltıcı emir (layering); fiyat kademesi sayısı, kısa ömürlü uzak emir payı |
| c | Bir dakikadan kısa sürede yön değiştiren emir | Aktör kimliği gerekir; veride ölçülemez |
| ç | Kendinden kendine / karşılıklı işlem | Karşılıklı işlem senaryosu (yalnız sentetik aktörde etiketli) |
| d | Açılış veya kapanış fiyatını etkileme | Kapanış etkileme senaryosu; kapanış göstergeleri |
| f | Fiyat yükseltici / düşürücü işlem | Adım adım fiyat yükseltme (ramping); net agresif adım |

Dört manipülasyon türünü günlük dille anlatalım:
- **Yanıltıcı emir (spoofing):** satmak istiyorsun ama fiyat düşük. Alış tarafına büyük alış emirleri koyuyorsun; herkes "büyük alıcı var, fiyat çıkacak" sanıyor ve fiyatı yükseltiyor. Sen bu sırada pahalıdan satıyor, sonra sahte alış emirlerini iptal ediyorsun. Sahte emirler hiç işlem görmez; iz yalnız "girip hemen çekilen büyük, uzak emirler"dir.
- **Kapanış fiyatını etkileme:** kapanış fiyatı fon değerlemelerinde, kredi teminatlarında ve ertesi günün baz fiyatında kullanılır. Kapanış müzayedesinin son saniyelerinde büyük bir emirle denge fiyatını yukarı ya da aşağı itmek.
- **Adım adım fiyat yükseltme (ramping):** ardışık küçük agresif alımlarla fiyatı yavaş yavaş yukarı taşımak, "yükselen hisse" görüntüsüyle başkalarını çekmek.
- **Karşılıklı işlem (wash trade):** aynı kişinin (ya da birlikte hareket edenlerin) hem alıcı hem satıcı olduğu işlemler. Mülkiyet değişmez, ama hacim yapay olarak şişer ve pay "çok işlem görüyor" sanılır.

---

## 2. Projenin fikri ve öneri formundan farkı

### 2.1 Üç parça

1. **Veri katmanı:** DataStore verisinden pay ve gün bazında emir defterinin yeniden kurulması.
2. **Eşleştirme motoru:** BIST kurallarına uygun sürekli işlem, müzayede ve devre kesiciler. Gerçek emir akışı tekrar oynatılır, araya sentetik manipülatif emirler eklenir.
3. **Manipülasyon tespiti:** iktisadi kurallar, Z-skor temel çizgisi, denetimsiz model (Isolation Forest) ve denetimli model (gradyan artırmalı karar ağaçları). Değerlendirme SPK vakaları ve sentetik enjeksiyonla yapılır.

### 2.2 Neden kendi motorumuzu yazdık

- Borsanın eşleştirme motoru kapalı bir sistemdir; dışarıdan kullanılamaz.
- Hazır açık kaynak motorlar BIST'e özgü kuralları bilmez: Mart 2025'teki ±%10 marj, yalnız düşüşte çalışan devre kesici, kapanışta ±%3 bandı, BIST'in müzayede dağıtım sırası, kısmi görünme davranışı.
- Manipülasyonu enjekte edebilmek için motorun içine girebilmemiz gerekir: "gerçek emirler + benim emirlerim" ile gün yeniden oynatılmalıdır.

### 2.3 Öneri formundan fark

Öneri formunda ajan tabanlı yapay borsa vardı: yatırımcı ajanları, GA/PSO ile kalibrasyon, Monte Carlo bandı. 22.10.2026'da bunun yerine gerçek emir akışını kullanma kararı verildi. Gerekçe:
- Ajanlar gerçek piyasayı ancak kabaca taklit eder; gerçek emir akışı piyasanın kendisidir.
- Motorun doğruluğu gerçek işlemlerle birebir ölçülebilir. Ajan simülasyonunda böyle bir ölçüt yoktur.
- Formdaki Z-skor karşılaştırması, Isolation Forest ve görselleştirme sistemde korundu.

---

## 3. Veri

### 3.1 Kaynaklar

| Kaynak | Ne içerir | Mart 2025 büyüklüğü | Rolü |
|---|---|---|---|
| `PP_GUNICIEMIR` (gün içi emir) | Her emir olayından sonra emrin tam durumu (bir satır = bir olay) | 1.128.466.831 satır | Motorun girdisi |
| `PP_GUNICIISLEM` (gün içi işlem) | Her işlemin alış ve satış tarafı, iki tarafın emir numarası, aktif/pasif bayrağı | 117.193.758 işlem (× 2 satır) | Motorun doğruluk hedefi |
| `PP_GUNSONUFIYATHACIM` (gün sonu) | Sıra-gün başına baz fiyat, kapanış, pazar, endeks üyeliği, hacimler | 192.220 satır | Referans veri ve gün sonu kontrolü |
| ITCH (kamu yayın akışı) | Piyasaya yayımlanan mesajlar | 2025-01/02 bekleniyor; 08.10.2018 örneği çözüldü | Çapraz doğrulama |
| SPK bültenleri | Manipülasyon kararları, işlem yasakları | 197 bülten (2024–2026) | Gerçek vaka etiketleri |

Hedef kapsam 01.06.2024–31.05.2025'tir (12 ay). Şu an doğrulanmış ve kullanılan ay Mart 2025'tir: 20 işlem günü, yaklaşık 590 pay sırası.

### 3.2 Bir satır ne anlatır: bir emrin hayatı

Gün içi emir dosyasında bir emir birden çok satırla görünür. Her satır bir olaydan **sonraki** durumdur. `degisiklik_sebebi` alanı olayı söyler:

| Sebep | Anlamı | Kimden gelir |
|---|---|---|
| 6 | Yeni emir | Kullanıcı |
| 5 | Değişiklik (fiyat ve/veya miktar) | Kullanıcı |
| 1 | İptal | Kullanıcı |
| 3 | İşlem (emir kısmen ya da tamamen gerçekleşti) | Borsa (eşleştirme) |
| 13 | Kısmi görünme emrinin görünen kısmının yenilenmesi | Borsa |
| 8 | Sistem dönüşümü (ör. piyasadan limite → limit) | Borsa |
| 9, 34, 116, 117 | Sistem iptalleri | Borsa |
| 19 | Süre dolumu (gün sonu) | Borsa |

Örnek: bir alış emri 10:15'te 1.000 lot olarak 50,00 TL'den girilir (sebep 6). 10:20'de 400 lotu işlem görür (sebep 3, kalan 600). 10:30'da fiyatı 50,05'e çekilir (sebep 5). 11:00'de iptal edilir (sebep 1). Bu emir dört satırdır.

**Motorun anahtar fikri:** kullanıcının yaptıkları (6, 5, 1) **girdi**dir. Borsanın yaptıkları (3, 13, 8, iptaller, süre dolumu) motorun **üretmesi gereken çıktı**dır. Motor yalnız girdileri alır ve işlemleri kendisi üretir; biz de gerçek işlemlerle karşılaştırırız. Tek istisna, nedenini veriden türetemediğimiz sistem iptalleridir (116, 117); bunlar dışarıdan verilir.

### 3.3 Veride doğruladığımız özellikler ve tarih parametreleri

Kuralları Prosedür'den yazdık. Ama veri tarihindeki uygulama yürürlükteki metinden farklı olabilir. Bu yüzden her kuralı veriyle sınadık (`veri/gunici-veri-dogrulama.md`, 13 bölüm). Öne çıkanlar:
- Fiyat adımı: 797.067.974 fiyatlı emir satırında adım dışı fiyat yok.
- Marj ±%10 (metinde %20 / %15 / %10).
- Devre kesici yalnız düşüşte, %5 (metinde iki yönlü).
- Tek fiyat algoritması 29.633 müzayedenin %99,96'sında fiyatı tutturuyor.
- Öncelik: fiyat önceliği %99,998, zaman önceliği kuralı %99,76 uyumlu.
- Zaman: emir zamanı µs çözünürlükte ve İstanbul saatinde, işlem zamanı ms çözünürlükte. `guncelleme_zamani` UTC'dir (3 saat geri).

Bu farklar **tarih parametresi** olarak `motor/tarih_parametreleri.csv` dosyasında tutulur. Her satırda parametre, kapsam (pazar), başlangıç, bitiş, değer ve kaynak yazar. Motor bir gün için en özel satırı seçer (`motor/parametreler.py`). Örnek: 10.03.2025 Yıldız Pazar için `fiyat_marji` → "2025-03-03…2025-03-28, 0,10, veri Mart 2025" satırı seçilir; tarihsiz "0,20, Prosedür Tablo-4" satırı daha az özel olduğu için seçilmez.

**Ölçüm kontrolü:** veriden ölçülen bir parametre için veri dönemindeki bir günü kapsayan ölçüm satırı yoksa motor `OlcumEksik` hatasıyla durur. Örneğin Nisan 2025'i oynatmaya kalkarsak, Nisan için marj ölçülmediğinden motor durur. Sessizce metindeki %20'yi kullanıp yanlış sonuç üretmez. Parametre o pazara hiç uygulanmıyorsa (ör. YİP'te devre kesici oranı) hata vermez; parametre uygulanmaz.

### 3.4 Hazırlama: neden günlük bölümleme

Aylık emir dosyası tarih sırasında değildir; satır grupları 12 güne kadar yayılır. "THYAO'nun 19 Mart emirleri" gibi bir okuma her seferinde bütün ayı taramak demektir. Bu yüzden `veri/araclar/gunici_emir_gunluk_bol.py` ayı gün ve pay kovası bazında böler (`veri/gun-ici-emir/gunluk/YYYY-MM-DD/pay-0..7.parquet`). Her dosya (pay, zaman, güncelleme no) sırasındadır. Bölümleme kayıpsızdır: sonda satır sayısı denetlenir (Mart: 1.128.466.831 satır).

Parquet, sütun bazlı sıkıştırılmış bir dosya biçimidir. Yalnız gereken sütunları ve satır gruplarını okumayı sağlar; CSV'ye göre hem küçük hem hızlıdır.

### 3.5 Kısmi görünme emirlerinde görünen kısım tahmini

Veride `gorunen_miktar` alanı her satırda emir miktarına eşit yazılmıştır; yani tepe (görünen kısım) bilinmez. Oysa motor bunu bilmek zorundadır: pasif emir yalnız görünen kısmı kadar eşleşir, sonra kısım yenilenip sıranın sonuna gider. `motor/veri.py` içindeki `tepe_tahmini` işlevi tepeyi emrin kendi olay dizisinden tahmin eder:
- İlk aday: ilk yenilemeye (sebep 13) kadar pasif olarak gerçekleşen miktar. Ör. 20.000 lotluk bir emir 4.000 lot işlem görünce yenileniyorsa tepe 4.000'dir.
- Bu aday sebep 13 dizisini tutarlı üretemiyorsa, emrin işlem miktarlarından ve yenileme aralıklarından üretilen adaylar denenir; tutarlı olan en büyüğü seçilir (`_tepe_tutarli`).
- Tutarlılık kuralları da veriden öğrenildi. Örneğin sebep 13, görünen kısmı bitiren işlemde yazılır. Aynı gelen emir yenilenen kısımdan da alırsa veride tek işlem yazılır.

---

## 4. Eşleştirme motoru (`motor/`)

### 4.1 Dosyalar ve görevleri

| Dosya | Görev |
|---|---|
| `emir.py` | Veri tipleri: Emir, İşlem, YeniEmir, Degistir, Iptal. Fiyatlar **milli-TL tamsayı** (10,05 TL = 10050): kayan nokta yuvarlama hatası olmasın diye |
| `defter.py` | Emir defteri: her taraf için fiyat seviyeleri; seviye içinde ekleme sırası = zaman önceliği |
| `surekli_islem.py` | Sürekli işlem eşleştirmesi |
| `tek_fiyat.py` | Müzayede: emir toplama, denge fiyatı, dağıtım |
| `veri/araclar/tek_fiyat_algoritma.py` | Denge fiyatı algoritması (Prosedür Ek-16 örneklerinin hepsini geçer) |
| `gun.py` | Bir pay-günün bütün bölüm akışı; enjeksiyon |
| `veri.py` | Veriden girdi olayları, kısmi görünme tahmini, gerçek işlemler |
| `parametreler.py`, `tarih_parametreleri.csv` | Tarihe bağlı kurallar |
| `dogrulama.py` | Sentetik emirlerin kurallara uygunluk kontrolü |
| `senaryolar.py` | Sentetik manipülasyon senaryoları |
| `tekrar_oynat.py`, `toplu_oynat.py` | Doğrulama: motor işlemleri ile gerçek işlemlerin karşılaştırması |
| `enjeksiyon.py` | Enjeksiyon modu (komut satırından) |

Neden kayan nokta değil tamsayı: bilgisayarda 0,1 + 0,2 tam olarak 0,3 etmez (0,30000000000000004). Fiyat karşılaştırmalarında bu küçük hata "10,10 ≥ 10,10" sorusuna yanlış cevap verdirebilir. Milli-TL tamsayıyla bu sorun yoktur.

### 4.2 Emir defteri (`defter.py`)

Her taraf için `fiyat → {emir_no: Emir}` sözlüğü tutulur. Python sözlükleri ekleme sırasını korur; bu sıra zaman önceliğidir. Fiyatlar ayrıca sıralı bir listededir (`bisect` ile ikili arama): alışta en iyi fiyat listenin sonu, satışta başıdır. Önceliğini kaybeden emir seviyesinin sonuna taşınır (`sona_al`).

### 4.3 Sürekli işlem (`surekli_islem.py`), adım adım

Yeni bir emir geldiğinde (`_yerlestir` → `_eslestir`):
1. Karşı tarafın en iyi fiyatına bakılır. Karşı taraf boşsa durulur.
2. Gelen emir limitse ve karşı en iyi fiyat limitinden kötüyse durulur.
3. Devre kesici eşiği varsa ve karşı fiyat eşiğin ötesindeyse durulur, devre kesici tetiklenir (aşağıda).
4. Piyasadan limite emir, ilk işlemden sonra başka fiyat seviyesine geçmez.
5. O seviyenin ilk emriyle (zaman önceliği) eşleşilir: miktar = min(gelenin kalanı, pasifin görünen kısmı). **Fiyat pasif emrin fiyatıdır.**
6. Pasif emir bittiyse defterden çıkarılır. Görünen kısmı bittiyse yenilenir ve seviyenin sonuna alınır.
7. Gelen emrin kalanı varsa 1. adıma dönülür.

Sonra gelen emrin kalanına karar verilir:
- KİE ya da piyasa emriyse kalan iptal edilir;
- piyasadan limiteyse kalan, ilk işlem fiyatından limit emir olarak deftere yazılır;
- limit GÜN emriyse kalan, kendi fiyatından deftere yazılır.

Örnek (bölüm 1.1'deki defter): 150 lotluk piyasa alış emri gelir. 11,00'daki 80 lotu alır, sonra 11,05'ten 70 lot alır; 11,05 seviyesinde 20 lot kalır. Aynı emir piyasadan limite olsaydı yalnız 11,00'dan 80 lot alırdı, kalan 70 lot 11,00'dan alış emri olarak deftere yazılırdı.

**Değişiklik (`degistir`):**
- fiyat değişirse emir defterden çıkarılıp yeni emir gibi yeniden yerleştirilir (gerekirse hemen eşleşir);
- kalan artarsa ya da görünmeyen alan değişirse sona geçer;
- kalan azalırsa yerinde kalır.

Değişiklik "kalan farkı" olarak verilir. Böylece motorun kalanı bir sapma yüzünden gerçek kalandan farklıysa da değişiklik uygulanabilir.

**Devre kesici:** sürekli işlem bölümü başlarken eşik hesaplanır: son müzayede fiyatı × (1 − %5), içe yuvarlanır. Mart 2025'te yalnız alt eşik vardır. Gelen bir emir eşiğin altındaki bir seviyeyle eşleşecekse eşleşme orada durur, gelen emrin kalanı iptal edilir ve devre kesici tetiklenir. Bu davranışı veriden öğrendik (THYAO 19.03, KRGYO 03.03). Sonraki olaylar müzayede emir toplaması olarak işlenir.

### 4.4 Müzayede (`tek_fiyat.py`)

- Emir toplama sırasında eşleşme yapılmaz. Değişiklik ve iptaller yine öncelik kurallarıyla işlenir.
- Eşleştirme anında denge fiyatı hesaplanır (bölüm 1.7). Sınırlar günlük taban/tavandır; kapanış müzayedesinde ayrıca son işlem fiyatının ±%3'ü.
- Dağıtım iki listeyle yapılır (bölüm 1.7). Dengeleyici emirler önce karşı taraftaki karşılanmamış emirlerle, sonra birbirleriyle eşleşir.
- Kalanlar:
  - piyasa emri, KİE ve dengeleyici iptal edilir;
  - fiyatsız piyasadan limite emir denge fiyatından limit emre döner;
  - diğerleri öncelik sırasıyla sürekli işlemin başlangıç defterine geçer.

### 4.5 Bir günün akışı (`gun.py`)

`Gun` sınıfı bir pay-günü baştan sona oynatır:
1. Gün sonu dosyasından fiyat adımı tablosu, pazar ve baz fiyat okunur. Tarih parametrelerinden marj, devre kesici oranı ve yönü, açığa satış kapsamı ve Adım 4 referansı alınır.
2. Payın emir satırları zamana göre dizilir. Aynı bölümdeki ardışık satırlar **koşu**lara ayrılır (`kosular`): açılış toplama → eşleştirme → sürekli işlem → kapanış toplama → eşleştirme → kapanış fiyatından işlemler → gün sonu. **Bölüm geçişleri ve müzayede anları veriden alınır.** Rastlantısal eşleştirme saniyesini taklit etmeyiz; gerçekte ne olduysa onu kullanırız.
3. Her koşunun türüne göre:
   - toplama: olaylar `TekFiyat`'a verilir;
   - eşleştirme: toplanan defter eşleştirilir, işlemler bu anın zamanıyla yazılır; kapanış müzayedesinin anı `kapanis_ani` olarak saklanır;
   - sürekli işlem: `SurekliIslem` çalışır. Defter 1 saniyede bir örneklenir: en iyi 5 seviyedeki alış ve satış miktarı ile en iyi fiyatlar (`defter_ornekleri`). Bunlar hem derinlik göstergelerinde hem senaryo fiyatlarında kullanılır;
   - kapanış fiyatından işlemler: bütün işlemler kapanış fiyatından yapılır;
   - gün sonu: eşleşmemiş toplama defteri kaldıysa eşleştirilir, kalan sentetik olaylar reddedilir.
4. Sentetik olaylar zamanlarına göre ilgili koşuya yerleşir ve o anki bölüm ve defter durumuyla `Dogrulayici`dan geçer. Reddedilenler sebebiyle `reddedilen` listesine yazılır.

### 4.6 Sentetik emir doğrulama (`dogrulama.py`)

Gerçek emirleri doğrulamayız, çünkü borsa onları zaten kabul etmiştir. Sentetik emirleri ise borsanın yapacağı gibi kontrol ederiz:
- **Ek-19 matrisi:** her bölümde hangi emir türü girilebilir, hangi değişiklik yapılabilir. Ör. EBDKS durdurmasında emir girilemez; açılışın son 5 dakikasında iptal yapılamaz.
- Fiyat adımı, taban/tavan, kapanış toplamada ±%3, kapanış fiyatından işlemlerde yalnız kapanış fiyatı.
- Açığa satış kapsamı (tarihe göre).
- Emir bilgisi (MPF-AFK-Hesap No) değişikliği reddedilir.

Gerçek bir örnek: değerlendirmede VAKBN 21.03.2025 11:32'ye yanıltıcı emir konmak istendi. O anda EBDKS durdurması vardı ve doğrulayıcı 7 sentetik olayın hepsini reddetti: emirler `emir_tipi_A`, `emir_tipi_C`, iptaller `iptal` sebebiyle. Motor kurala aykırı manipülasyonun piyasaya girmesine izin vermiyor.

### 4.7 Motor ne kadar doğru

Ölçüt sıkıdır: bir işlem ancak **alış emri numarası, satış emri numarası, fiyat ve adedi** gerçek bir işlemle birebir aynıysa doğru sayılır.

| Sıra-gün | Müzayedeler | Sürekli işlem | Kapanış fiyatından | Bütün gün |
|---|---|---|---|---|
| THYAO.E 03.03 | 2.588 / %100 | 74.046 / %99,81 | 178 / %100 | %99,82 |
| KRGYO.E 03.03 (devre kesici) | 286 / %100 | 21.217 / %99,92 | 22 / %100 | %99,92 |
| THYAO.E 19.03 (2 EBDKS + devre kesici) | 6.807 / %100; EBDKS 3.227 / %71,4 | 176.028 / %99,82 | 276 / %100 | %99,34 |

Bütün paylarda: 03.03.2025'te 586 sıranın 4.915.057 işleminin %99,85'i, 19.03.2025'te 580 sıranın 6.825.508 işleminin %99,91'i birebir aynıdır.

Kalan farkların nedenleri:
- Kısmi görünme emirlerinin tepe büyüklüğü bazen belirsizdir. EBDKS müzayedelerindeki %71,4'ün nedeni budur: fiyat ve emir bazında gerçekleşen miktarlar yine aynıdır (3.213/3.213), farklı olan karşı emir eşleşmeleridir.
- Aynı µs'deki olayların sırası veride yoktur.
- Bir sapma olursa defter birkaç işlem boyunca farklı kalır (zincirleme etki).
- Özsermaye günlerinde (bedelsiz, temettü) gün sonu dosyasındaki baz fiyat düzeltilmemiştir; bu günler hariç tutulur.

---

## 5. Sentetik manipülasyon (`motor/senaryolar.py`)

### 5.1 Fikir

Aynı pay-gün iki kez oynatılır:
1. **Taban çizgisi:** yalnız gerçek emirlerle.
2. **Enjeksiyonlu:** gerçek emirler + sentetik aktörün emirleri.

İkisi arasındaki fark manipülasyonun piyasadaki izidir. Sentetik emirlerin numarası `SENT-<senaryo>-<n>` biçimindedir; bu yüzden aktörün her işlemini biliriz.

**Temel varsayım ("gerçek akış dışsaldır"):** gerçek katılımcılar sentetik emirlere tepki vermez. Gerçekte bir yanıltıcı emir başkalarını da etkileyebilirdi; bizim oynatmamızda etkilemez. Bu yöntemin bilinen sınırıdır. Tespit için bir "zor durum"dur: aktörün izi yalnız kendi emirlerinden ve bunların doğrudan sonuçlarından oluşur, piyasanın tepkisiyle büyümez.

### 5.2 Senaryolar

Büyüklükler, payın o günkü işlem miktarına (H, lot) göre ölçeklenir. Böylece büyük ve küçük paylarda manipülasyon aynı göreli büyüklükte olur. THYAO'da 1.000 lot devede kulaktır, küçük bir payda günün yarısı olabilir.

| Senaryo | Ne yapar | Değerlendirmedeki büyüklük | Bent |
|---|---|---|---|
| Kapanış etkileme | Kapanış emir toplamanın sonunda, eşleşmeden 10 sn önce, ±%3 bandın ucundan büyük bir emir | H × %3 | d |
| Yanıltıcı emir | Bir tarafta, o tarafın en iyi fiyatının 4, 5, 6 adım gerisinde 3 büyük emir (katman); 15 sn sonra karşı tarafta küçük agresif emir; 30 sn sonra katmanların iptali | Katman H × %2, karşı emir H × %0,2 | a, b |
| Fiyat yükseltme | 20 sn arayla 10 agresif alış (piyasadan limite + KİE); her biri en iyi satışı tüketip fiyatı yukarı iter | Her biri H × %0,5 | f |
| Karşılıklı işlem | 60 sn arayla 10 kez aynı aktörün aynı fiyattan satışı ve hemen ardından alışı | Her biri H × %0,5 | ç |

Ayrıntılar:
- **Yanıltıcı emir:** katmanlar defterin derinindedir, işlem görmesi beklenmez. En iyi fiyat, taban oynatmasının defter örneğinden (1 sn önceki durum) alınır. **Temiz vaka ölçütü:** katmanlardan, katman toplamının %1'inden fazlası işlem görürse senaryo artık "yanıltıcı emir" değil, "büyük agresif işlem"dir. Bu vaka değerlendirmeye alınmaz.
- **Karşılıklı işlem:** gerçek bir karşılıklı işlemde aktörün alışı kendi satışıyla eşleşmelidir. Bu yüzden emir makasın içinden girilir (en iyi alışın bir adım üstü): satış o fiyatta tek başına en iyi satış olur, ardından gelen alış onu karşılar. Makas tek adımsa içine fiyat girilemez; o zaman aktör kendi 60 saniyelik aralığında makasın en az iki adım açıldığı ilk anı bekler. Ölçüm (20 vaka): senaryo miktarının ortalama %89'u aktörün kendi emirleri arasında işlem görüyor. **Temiz vaka ölçütü:** satışın yarısından azı kendi alışıyla eşleşirse vaka değerlendirmeye alınmaz.
- **Kapanış etkileme:** emir bandın ucundan girilir (alışta son işlem fiyatı + %3, satışta − %3) ve kapanış müzayedesinin denge fiyatını o yöne iter. Örnek: ASELS 19.03.2025'te 200.000 lotluk alış emri kapanışı 112,30'dan 113,00'e çıkarır.

### 5.3 Enjeksiyon nasıl çalıştırılır

- Komut satırı: `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]`. Çıktıda sentetik işlemler, reddedilen olaylar, taban ve enjeksiyonlu kapanış fiyatları ve "gerçek işlemlerin kaçı değişmedi" bilgisi yer alır.
- Arayüz: bölüm 9.

---

## 6. Tespit için temel kavramlar: istatistik ve makine öğrenmesi

Bu bölüm projedeki bütün tespit yöntemlerinin altındaki fikirleri sıfırdan anlatır. Bölüm 7, bunların projede tam olarak nasıl kullanıldığını anlatır.

### 6.1 "Tespit" burada ne demek: puan ve sıralama

Bir yöntem her pay-güne (ya da her 5 dakikalık pencereye) bir **şüphe puanı** verir. Yüksek puan daha şüphelidir. "Manipülasyon var / yok" diye kesin karar vermeyiz. Bunun iki nedeni var:
- Gerçek hayatta bu işi gözetim uzmanları yapar. Sistemin görevi, binlerce pay-gün içinden bakılması gereken birkaçını öne çıkarmaktır. Bu yüzden asıl soru şudur: "Manipülasyonlu olanlar listenin başında mı?"
- Kesin karar için bir eşik seçmek gerekir. Eşik, kaç yanlış alarma katlanılacağına bağlıdır; bu da bir politika kararıdır. Sıralama ölçütleri (bölüm 6.13) eşikten bağımsızdır.

### 6.2 Özellik (gösterge) nedir

Ham veri milyonlarca emir satırıdır; hiçbir yöntem bunu doğrudan "anlayamaz". Bu yüzden her pay-gün ya da pencere için birkaç **sayısal özet** hesaplarız; bunlara **özellik** (feature) denir. Örnek: "bugün girilen emirlerin yüzde kaçı iptal edildi" (iptal oranı). Her özellik bir manipülasyon türünün izini taşıyacak şekilde seçilir. Ör. yanıltıcı emir çok sayıda kısa ömürlü emir bıraktığı için iptal oranını ve kısa ömürlü uzak emir payını yükseltir.

Özellik seçimi tespitin en önemli adımıdır. Kötü özellikle en iyi model bile bir şey bulamaz.

### 6.3 Ortalama ve standart sapma

- **Ortalama:** değerlerin toplamı / sayısı.
- **Standart sapma:** değerlerin ortalamadan tipik uzaklığı, yani "ne kadar dağınık oldukları".

Örnek: bir payın son 10 günündeki iptal oranları (%): 18, 20, 22, 19, 21, 20, 18, 22, 20, 20.
- Ortalama = 200 / 10 = **20**.
- Ortalamadan farklar: −2, 0, 2, −1, 1, 0, −2, 2, 0, 0. Kareleri toplamı 18'dir. (Örnek) varyans = 18 / 9 = 2, standart sapma = √2 ≈ **1,41**.

Yorum: bu payın iptal oranı genellikle %20 civarındadır ve günden güne tipik olarak 1,4 puan oynar.

### 6.4 Z-skor

**Nedir:** bir değerin ortalamadan kaç standart sapma uzak olduğu.

z = (değer − ortalama) / standart sapma

**Örnek:** yukarıdaki pay bugün %26 iptal oranı gösterdi. z = (26 − 20) / 1,41 ≈ **4,2**. Yani bugün olağan dalgalanmanın 4 katından fazla saptı.

**Nasıl yorumlanır:** değerler kabaca normal (çan eğrisi) dağılıyorsa:
- |z| ≥ 2 olasılığı ≈ %4,6 (yaklaşık 22 günde bir);
- |z| ≥ 3 olasılığı ≈ %0,27 (yaklaşık 370 günde bir).

Bu yüzden |z| ≥ 3 geleneksel olarak "olağan dışı" sayılır. Bizim kural eşiklerimiz de buradan gelir: ana koşul 3, yardımcı koşul 2.

**Bu projede neden kullanıldı:**
- **Her payın "normali" farklıdır.** THYAO'da günde 75.000 işlem olağandır, küçük bir payda 300 işlem bile yoğundur. Ham değerleri karşılaştırmak anlamsızdır. Z-skor her payı **kendi geçmişiyle** karşılaştırır ve bütün payları aynı ölçeğe getirir: "bu pay için ne kadar olağan dışı?"
- **Birimden bağımsızdır.** İptal oranı (%), hacim (TL) ve getiri (%) farklı birimlerdedir; z'leri ise doğrudan karşılaştırılabilir. Bu yüzden "özelliklerin en büyük |z|'si" tek bir puan olabilir.
- **Basit ve açıklanabilirdir.** "Bugün iptal oranı bu pay için 4,2 sapma yüksek" cümlesi bir gözetim uzmanına doğrudan anlam ifade eder.
- **Temel çizgidir.** Daha karmaşık bir yöntemin (Isolation Forest, model) işe yarayıp yaramadığını anlamak için önce basit yöntemle karşılaştırırız. Öneri formundaki "klasik yöntem karşılaştırması" budur.

**Projedeki ayrıntılar** (`tespit/yontemler.py`, `z_skorlari`):
- Ortalama ve standart sapma yalnız **önceki günlerden** hesaplanır; bugünün kendisi katılmaz. Yoksa bugünkü uç değer ortalamayı çekip kendi z'sini küçültürdü. Ayrıca bu, gerçek hayatta olduğu gibi "o gün elde olan bilgi" ile hesaplamaktır; geleceği kullanmayız. Bunu bir birim testi sınar (`test_zskor_yalniz_gecmis`).
- En az 5 günlük geçmiş gerekir. Mart'ın ilk 5 günü (3–7 Mart) için z yoktur.
- Pay-gün puanı (`puan_zskor`) = 24 özelliğin |z| değerlerinin en büyüğü.

**Neyi yapamaz:**
- **Geçmiş de kirliyse göremez.** Manipülasyon haftalarca sürüyorsa, payın "normali" zaten manipülasyonlu günlerdir ve z küçük çıkar. Gerçek bir örnek bölüm 6.7'de.
- Tek bir uç değer ortalamayı ve standart sapmayı bozar (bölüm 6.6).
- Çarpık dağılımlarda (hacim gibi) yanıltıcıdır (bölüm 6.5).

### 6.5 Log dönüşümü

Hacim, işlem sayısı gibi büyüklükler "çarpık" dağılır: çoğu gün normaldir, ama arada bir 5–10 katına çıkan günler olur. Bu durumda standart sapma büyük günlerin etkisiyle şişer. Logaritma büyük değerleri sıkıştırır: 10 kat artış, log ölçeğinde sabit bir artıştır (ln 10 ≈ 2,3). Bu yüzden hacim, fiyat kademesi sayısı ve emir/işlem oranı z'den önce log ile dönüştürülür (`log1p(x) = ln(1 + x)`; 0 değerinde de çalışır). Pencere düzeyinde işlem sayısı, hacim, yeni emir, iptal, fiyat kademesi ve derinlik için aynısı yapılır.

### 6.6 Sağlam Z-skor: ortanca ve MAD

**Sorun:** bir günün 6 penceresinin hacimleri 100, 120, 90, 110, 100, 2000 olsun. Son pencere açıkça uç değerdir.
- Ortalama = 420, standart sapma ≈ 774. Uç pencerenin z'si = (2000 − 420) / 774 ≈ **2,0**. Yani uç değer kendi varlığıyla ortalamayı ve sapmayı şişirmiş, kendini "normal" göstermiştir.

**Çözüm:**
- ortalama yerine **ortanca** (sıralayınca ortadaki değer),
- standart sapma yerine **MAD** (ortancadan mutlak farkların ortancası).

Aynı örnekte:
- ortanca = (100 + 110) / 2 = 105;
- mutlak farklar 5, 15, 15, 5, 5, 1895; bunların ortancası 10, yani MAD = 10;
- sağlam z = (2000 − 105) / (1,4826 × 10) ≈ **128**. Uç değer artık açıkça görünür.

1,4826 çarpanı, normal dağılımda MAD'ı standart sapmayla aynı ölçeğe getirir (1 / 0,6745). Böylece "3" eşiği aynı anlamı taşır.

**Bu projede neden:** 5 dakikalık pencere puanlamasında her pencere **aynı günün diğer pencereleriyle** karşılaştırılır. Bir günde yaklaşık 100 pencere vardır; manipülasyonlu pencere tam da uç değer olandır. Ortalama kullansaydık manipülasyon kendini gizlerdi. (`tespit/pencere.py`, `puanla`.)

### 6.7 Yüzdelik sıra ve kesitsel karşılaştırma

**Nedir:** bir değerin bir grup içindeki sırası. Ör. 100 pay içinde 95. sıradaki pay 0,95 yüzdelik sıradadır, yani payların %95'inden yüksektir.

**Kesitsel karşılaştırma:** payı kendi geçmişiyle değil, **aynı gün aynı pazardaki diğer paylarla** karşılaştırmak (`yontemler.kesitsel`). Her özellik için yüzdelik sıra (`k_*`) hesaplanır. Puan iki şekilde çıkar:
- uç sıra: |2 × sıra − 1| ortalaması (en alt ya da en üst uçta olmak 1, ortada olmak 0);
- yüzdelik sıralar üzerinde Isolation Forest (bölüm 6.10).

Ayrıca 5 günlük birikimli getiri ve hacim artışı eklenir; böylece birkaç güne yayılan hareketler de görünür.

**Neden gerekli: gerçek bir örnek (ALKLC, SPK A vakası).** SPK'ya göre ALKLC'de manipülasyon 04.02.2025'te başladı ve Mart ortasına kadar sürdü. "Kısa ömürlü uzak emir payı" (yanıltıcı emir izi) Mart'ın bütün piyasası için ortanca %1,2'dir.

| Tarih | ALKLC kısa ömürlü uzak emir payı | Kendi geçmişine göre z | Aynı gün paylar içindeki sırası |
|---|---|---|---|
| 11.03 | %7,4 | 1,6 | %94 |
| 12.03 | %8,0 | 1,7 | %95 |
| 13.03 | %7,0 | 0,6 | %96 |
| 14.03 | %5,5 | −0,7 | %92 |

ALKLC'nin değeri piyasa ortancasının 4–7 katıdır. Ama payın kendi geçmişi de (Şubat'tan beri) bu düzeydedir; bu yüzden **Z-skor "normal" der** (z ≈ 1). Kesitsel karşılaştırma ise payı her gün ilk %4–8'e koyar. Sonuç (bölüm 8.1): ALKLC için Z-skor ROC-AUC 0,65, kesitsel Isolation Forest 0,90.

**Neyi yapamaz:** bütün piyasayı etkileyen bir günde (ör. 19 Mart'taki sert düşüş) herkes uç değerde olabilir. Ayrıca doğası gereği farklı olan paylar (ör. çok sığ paylar) hep uçta görünür.

### 6.8 Kural tabanlı tespit (iktisadi kurallar)

**Nedir:** "eğer şu ve şu olursa uyar" biçiminde, insan tarafından yazılmış kurallar. Her kural Tebliğ'deki bir bende bağlanır.

**Örnek kural (bent f, fiyat yükseltme):** |z(getiri)| ≥ 3 **ve** |z(aktif taraf dengesizliği)| ≥ 2 **ve** ikisi aynı yönde. Neden "ve": fiyatın tek başına sert yükselmesi bir haberden (bilanço, ihale) olabilir. Ama fiyat yükselirken işlemlerin çoğunu agresif alıcılar başlatıyorsa, yani biri karşı tarafın satışlarını süpürerek fiyatı itiyorsa, bu "fiyat yükseltici işlem" tarifine uyar. İki koşulu birlikte istemek yanlış alarmı azaltır.

**Neden kullandık:**
- **Açıklanabilirlik:** bir uyarı "bent f: getiri z = 4,1, aktif alış dengesizliği z = 2,7" diye gerekçesiyle gelir. Hukuki bir süreçte "model öyle dedi" kabul edilmez; gerekçe gerekir.
- **Etiket gerektirmez:** kurallar alan bilgisinden yazılır, eğitilmez.
- **Hedefli:** genel "olağan dışılık" yerine belirli bir manipülasyon imzasını arar.

**Eşikler (3 ve 2):** bunlar bölüm 6.4'teki "olağan dışı" anlamından gelen tasarım parametreleridir; Prosedür'de ya da Tebliğ'de sayı yoktur. Yüksek eşik daha az alarm ve daha az isabet verir; düşük eşik tersini yapar. Puan, tetiklenen bent sayısıdır; eşitlikte Z-skor puanı belirler.

**Neyi yapamaz:** yazılmamış bir manipülasyon biçimini göremez. Birkaç zayıf işaretin birleşimini (hiçbiri tek başına eşiği aşmıyorsa) yakalayamaz. Bunu makine öğrenmesi yapar.

### 6.9 Makine öğrenmesi nedir

**Model:** girdi (özellikler) alıp çıktı (puan) veren bir hesap kuralı. Kural tabanlı yöntemden farkı, kuralın insan tarafından değil **veriden öğrenilmesidir**.

**Eğitim:** modelin içindeki ayarların (parametrelerin), örnekler üzerinde hatayı en aza indirecek biçimde ayarlanması.

İki tür öğrenme var:
- **Denetimli öğrenme:** örneklerin doğru cevabı (etiketi) bilinir. Model "bu özellikler → manipülasyon" eşleşmesini öğrenir. Benzetme: çözümlü soru bankasıyla çalışmak.
- **Denetimsiz öğrenme:** etiket yoktur. Model verinin yapısını öğrenir, ör. "normal" neye benziyor; ona benzemeyeni işaretler. Benzetme: hiç cevap anahtarı görmeden "bu soru ötekilere benzemiyor" demek.

**Bu projede ikisi neden birlikte:**
- Gerçek veride etiket yoktur (SPK etiketleri az ve kabadır). Bu yüzden etiket istemeyen **denetimsiz** bir yöntem gerekir: Isolation Forest.
- Sentetik enjeksiyon bize kesin etiket verir. Bununla **denetimli** bir model eğitebiliriz: hangi pencerede manipülasyon olduğunu biliyoruz.
- Kurallar ve Z-skor bunların karşılaştırılacağı temel çizgidir. Bir model basit kuralı geçemiyorsa karmaşıklığına değmez.

### 6.10 Isolation Forest (denetimsiz)

**Sezgi:** "20 soruda bul" oyununu düşün. Bir kalabalığın içinden birini rastgele sorularla ayırmaya çalışıyorsun ("boyu 1,90'dan uzun mu?"). Kalabalığın ortasındaki sıradan biri pek çok soru sonra ayrılır. 2,10 boyunda biri ise ilk bir iki soruda ayrılır. **Az soruda yalnız kalan, aykırıdır.**

**Nasıl çalışır:**
1. Rastgele bir özellik ve o özellikte rastgele bir eşik seçilir; veri ikiye bölünür.
2. Her parça, içinde tek nokta kalana kadar aynı şekilde bölünür. Bu bir ağaçtır.
3. Bu işlem çok kez tekrarlanır: bizde 300 ağaç ("orman").
4. Her noktanın ağaçlarda yalnız kalana kadar geçtiği ortalama bölme sayısı (derinlik) hesaplanır. **Kısa derinlik = aykırı = yüksek puan.**

Örnek: iki özellik düşün, iptal oranının z'si ve hacmin z'si. Pencerelerin çoğu (0, 0) civarında bir bulut oluşturur. (8, 0,5) noktasındaki bir pencere, "iptal z'si 5'ten büyük mü?" gibi ilk birkaç rastgele bölmede yalnız kalır. Bulutun ortasındaki bir pencere için ise onlarca bölme gerekir.

**Bu projede neden:**
- Etiket gerektirmez.
- Çok boyutludur: 24 özelliğe birlikte bakar. "Hiçbir özellik tek başına uç değil ama birleşimi garip" durumunu da görebilir.
- Öneri formunda vardı ve standart bir aykırılık tespiti yöntemidir.

**Projedeki ayrıntılar:** pay-gün düzeyinde z-skorlar üzerinde (`yontemler.isolation_forest`; uçlar ±10 ile kırpılır), kesitsel düzeyde yüzdelik sıralar üzerinde, pencere düzeyinde sürekli işlem pencerelerinin z'leri üzerinde çalışır. `random_state` sabittir: aynı veriyle her çalıştırmada aynı sonuç çıkar.

**Neyi yapamaz (ve bizde neden zayıf kaldı):** aykırı olmak manipülasyon olmak demek değildir. Borsada olağan dışı pencere çoktur: haber, büyük bir kurumsal alım, açılış sonrası oynaklık. Isolation Forest bunların hepsini işaretler; manipülasyon ise belirli bir olağan dışılık türüdür. Örneğin yanıltıcı emirde kurallar enjekte edilen pencereyi 19 vakanın 17'sinde günün ilk 3'üne koyarken Isolation Forest yalnız 1'inde koyuyor. Kural doğrudan imzaya (kısa ömürlü uzak emir) bakıyor; Isolation Forest bu imzayı 24 boyutun içinde "bir başka garipliğe" karıştırıyor.

### 6.11 Karar ağacı ve gradyan artırma (denetimli model)

**Karar ağacı:** evet/hayır sorularından oluşan bir akış şeması. Örnek (öğretim amaçlı, gerçek modelin bir parçası değildir):

```
kısa ömürlü uzak emir payı > %30 mu?
├─ evet → iptal sayısı z'si > 2 mi?
│        ├─ evet → manipülasyon olasılığı %85
│        └─ hayır → %40
└─ hayır → hacim z'si > 2 mi?
         ├─ evet → %15
         └─ hayır → %1
```

Eğitim, soruları ve eşikleri öyle seçer ki yapraklardaki örnekler olabildiğince "saf" olsun (hep manipülasyon ya da hep normal).

**Tek ağacın sorunu:** derin bir ağaç eğitim verisini ezberler (bölüm 6.12), sığ bir ağaç ise kaba kalır.

**Gradyan artırma (gradient boosting):** çok sayıda küçük ağaç **sırayla** kurulur:
1. Başlangıç tahmini taban orandır (pencerelerin %1,9'u manipülasyonlu).
2. İlk ağaç, bu tahminin en çok yanıldığı yerleri düzeltecek soruları öğrenir. Ör. "uzak emir payı yüksekse olasılığı artır".
3. İkinci ağaç, ilk iki adımın toplamının **kalan hatasını** düzeltir. Ör. ilk ağaç karşılıklı işlem pencerelerini kaçırdıysa, ikinci ağaç "hacim yüksekse artır" sorusunu öğrenir.
4. Bu 300 kez tekrarlanır. Her ağacın katkısı 0,05 ile çarpılır (öğrenme oranı). Küçük adımlarla öğrenmek ezberi azaltır.

Benzetme: bir öğrenci deneme sınavını çözer, yanlışlarına bakar ve sadece onlara çalışır. Sonra yeni denemede kalan yanlışlarına çalışır, ve böyle devam eder.

**Neden bu model:**
- Tablo biçimindeki verilerde (her satır bir pencere, her sütun bir özellik) en güçlü ve en yaygın yöntemlerden biridir.
- Ölçekleme gerektirmez; ağaçlar yalnız "büyük mü küçük mü" diye sorar.
- Eksik değeri (ör. o pencerede yeni emir yoksa uzak emir payı tanımsızdır) kendisi işler.
- Özellikleri **birleştirebilir**: tek başına eşiği aşmayan iki zayıf işaret birlikte güçlü bir işaret olabilir. Kuralların yapamadığı budur.
- Az veriyle çalışır. Derin öğrenme binlerce pozitif örnek ister; bizde 111 pozitif pencere vardır.

Kodda: `sklearn.ensemble.HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0)`. "Hist" (histogram) sürümü sayısal değerleri kutulara ayırarak hızlı çalışır. Eğitim birkaç saniye sürer.

### 6.12 Ezber (aşırı öğrenme) ve çapraz doğrulama

**Ezber (overfitting):** model eğitim örneklerini ezberler ama yeni örneklerde başarısız olur. Sınav sorularını cevaplarıyla ezberleyen öğrenci gibi: aynı sorular gelince 100 alır, farklı sorular gelince çakar. Bu yüzden bir modelin başarısı **eğitimde görmediği** örneklerde ölçülmelidir.

**Çapraz doğrulama (k katlı):** veri 5 parçaya bölünür. Model 4 parçayla eğitilir, 5. parçada sınanır. Bu, her parça bir kez sınav olacak şekilde 5 kez tekrarlanır. Böylece her örnek tam olarak bir kez, onu görmemiş bir modelce puanlanır.

**Gruplu çapraz doğrulama (bizim kullandığımız, `GroupKFold`):** aynı pay-günün pencereleri birbirine çok benzer (aynı pay, aynı gün, aynı haber ortamı). Aynı günün bazı pencereleri eğitimde, bazıları testte olursa model "bu güne" alışır ve test sonucu şişer. Bu yüzden bölme **pay-gün bazında** yapılır: bir pay-günün bütün pencereleri ya eğitimde ya testtedir. Test her zaman modelin hiç görmediği günlerde yapılır.

### 6.13 Değerlendirme ölçütleri

**Karışıklık matrisi.** Bir eşikle alarm verildiğini düşünelim. Örnek: 1.000 pencerenin 20'si manipülasyonlu; yöntem 30 pencereye alarm verdi, bunların 15'i gerçekten manipülasyonlu.

| | Gerçekte manipülasyon | Gerçekte normal |
|---|---|---|
| Alarm verildi | 15 (doğru pozitif) | 15 (yanlış pozitif) |
| Alarm verilmedi | 5 (kaçırılan) | 965 (doğru negatif) |

- **Kesinlik (precision):** alarmların ne kadarı doğru? 15 / 30 = %50.
- **Duyarlılık (recall):** manipülasyonların ne kadarı yakalandı? 15 / 20 = %75.
- **F1:** ikisinin uyumlu ortalaması: 2 × 0,5 × 0,75 / (0,5 + 0,75) = 0,6.
- **Neden "doğruluk" (accuracy) kullanmıyoruz:** bu yöntemin doğruluğu (15 + 965) / 1000 = %98'dir. Ama "hiçbir zaman alarm verme" diyen aptal bir yöntemin doğruluğu da 980 / 1000 = %98'dir. Pozitifler çok azken doğruluk anlamsızdır. Bizde pencerelerin yalnız %1–2'si pozitiftir.

**ROC-AUC (sıralama ölçütü, eşikten bağımsız).** Tanım: rastgele seçilen bir pozitifin, rastgele seçilen bir negatiften daha yüksek puan alma olasılığı.
- 0,5 = yazı-tura (yöntem bir şey bilmiyor);
- 1,0 = mükemmel (bütün pozitifler bütün negatiflerin üstünde);
- 0,5'in altı = ters (yöntem pozitiflere daha düşük puan veriyor).

Elle örnek: pozitiflerin puanları 0,9, 0,6, 0,4; negatiflerinki 0,8, 0,5, 0,3, 0,2, 0,1. 3 × 5 = 15 (pozitif, negatif) çifti var:
- 0,9 beş negatifin hepsinden büyüktür: 5 çift;
- 0,6 dört negatiften büyüktür (0,8 hariç): 4 çift;
- 0,4 üç negatiften büyüktür: 3 çift.

ROC-AUC = 12 / 15 = **0,80**.

**Ortalama kesinlik (AP):** pozitifler çok azken ROC-AUC iyimser kalabilir; AP "listenin başı ne kadar temiz" sorusuna daha duyarlıdır. Taban değeri pozitif oranıdır (bizde ≈ 0,02); 0,02'nin ne kadar üstündeyse o kadar iyidir.

**İlk 3 isabeti (pencere düzeyi, bizim pratik ölçütümüz):** bir günde yaklaşık 100 pencere vardır. Enjekte edilen pencerelerden biri günün en yüksek puanlı 3 penceresine giriyor mu? Bu, "analist her gün her payın en şüpheli 3 penceresine bakarsa manipülasyonu görür mü" sorusudur. Rastgele bir yöntem için bu olasılık ≈ %3–5'tir.

**Kontrol (yanlış alarm tabanı), en önemli ölçüt:** aynı pay-gün **enjeksiyonsuz** oynatıldığında, aynı pencereler yine ilk 3'e giriyor mu? Bir yöntem kontrolde de yüksek puan veriyorsa ayırt ettiği şey manipülasyon değil, o pencerenin kendisidir (ör. kapanış penceresi her gün uçtadır). Bu kontrolü yapmasaydık bölüm 11'deki iki önemli hatayı göremezdik.

### 6.14 Etiketsiz gün negatif değildir

SPK yalnız yakaladığı ve karar verdiği vakaları yayımlar. Etiketsiz bir pay-günde manipülasyon olmadığını bilmiyoruz; yalnız "SPK bu günü işaretlemedi" diyebiliriz. Bu yüzden SPK değerlendirmesinde etiketsiz günleri negatif saymak, yöntemi olduğundan kötü gösterebilir (gerçek ama yakalanmamış manipülasyonu "yanlış alarm" sayarız). Sonuçlar bu yüzden **alt sınır** olarak okunur.

### 6.15 Özellik önemi: model neye bakıyor

**Permütasyon önemi:** bir özelliğin değerleri satırlar arasında rastgele karıştırılır; böylece o özellik anlamsız hâle gelir. Modelin başarısı (ortalama kesinlik) ne kadar düşerse, model o özelliğe o kadar dayanıyordur. `denetimli.py` bunu hesaplar (`denetimli_ozellik_onemi.csv`). ×1 koşusunda en önemli üç özellik:

| Özellik | Önem (AP düşüşü) | Yorum |
|---|---|---|
| Hacim z'si | 0,25 | Karşılıklı işlem ve fiyat yükseltme hacim üretir |
| Kısa ömürlü uzak emir payı | 0,08 | Yanıltıcı emrin doğrudan izi |
| Aktif taraf dengesizliği | 0,02 | Agresif alımlar (yükseltme, karşılıklı işlemdeki alış) |

Defter derinliği göstergelerinin önemi sıfıra yakındır: bu aşamada katkıları yoktur.

---

## 7. Projedeki tespit sistemi (`tespit/`)

### 7.1 Birim: pay-gün ve 5 dakikalık pencere

Veride kimin emir verdiği yoktur. Bu yüzden birim **pay-zaman dilimi**dir:
- **pay-gün:** "THYAO 19 Mart'ta şüpheli mi?";
- **5 dakikalık pencere:** "THYAO 19 Mart 14:05–14:10 arasında şüpheli mi?".

Neden ikisi birden: uzun süren manipülasyon (haftalarca) gün düzeyinde görünür. Kısa bir epizot (30 saniyelik yanıltıcı emir) ise bütün günün toplamında kaybolur, ancak pencere düzeyinde görünür.

### 7.2 Pay-gün özellikleri (`ozellikler.py`)

Her pay-gün için 24 özellik hesaplanır; her biri bir bentle ilişkilidir:

| Grup | Özellik | Ne ölçer |
|---|---|---|
| Fiyat | `getiri` | Kapanış / baz − 1 |
| Fiyat | `aralik` | (Gün içi en yüksek − en düşük) / baz |
| Fiyat | `kapanis_oncesi_getiri` | 17:45 sonrası sürekli işlemdeki getiri |
| Hacim | `hacim_tl` | İşlem hacmi (TL) |
| Kapanış | `kapanis_aof_sapma` | Kapanış fiyatının gün içi ağırlıklı ortalama fiyattan (AOF) sapması |
| Kapanış | `kapanis_seansi_payi`, `kfi_payi` | Kapanış müzayedesinin ve kapanış fiyatından işlemlerin hacim payı |
| Kapanış | `kapanis_muzayede_sapma` | Kapanış müzayedesi fiyatı / son sürekli işlem fiyatı − 1 |
| Kapanış | `kapanis_toplama_dengesizlik` | Kapanış toplamadaki yeni emirlerde (alış − satış) / (alış + satış) |
| Kapanış | `kapanis_son_dakika_payi` | Kapanış toplama olaylarının son 60 sn'ye düşen payı |
| Kapanış | `kapanis_degisiklik_yogunlugu` | Kapanış toplamada (değişiklik + iptal) / yeni emir |
| Açılış | `acilis_sapma` | Açılış müzayedesi fiyatının bazdan sapması |
| Açılış | `acilis_iptal_orani` | 09:40–09:50 iptalleri / yeni emirler |
| Emir akışı | `iptal_orani`, `degisiklik_orani` | İptal ve değişiklik / yeni emir |
| Emir akışı | `emir_islem_orani` | Yeni emir / işlem sayısı |
| Emir akışı | `piyasa_payi`, `kie_payi`, `afk_payi` | Yeni emirler içindeki paylar |
| Emir akışı | `fiyat_kademesi` | Yeni limit emirlerdeki farklı fiyat sayısı |
| Emir akışı | `kisa_omurlu_uzak_pay` | Aynı tarafın en iyi fiyatından en az 3 adım uzakta girilip 60 sn içinde işlem görmeden iptal edilen emirlerin miktar payı |
| İşlem | `aktif_dengesizlik` | (Agresif alış − agresif satış) / toplam |
| İşlem | `kucuk_islem_payi` | 1.000 TL altı işlemlerin payı |
| Defter | `makas` | Göreli makasın ortancası |

"Kısa ömürlü uzak emir payı" bu projenin en etkili göstergesidir. Neden bu tanım: yanıltıcı emrin amacı işlem görmemektir. Bu yüzden en iyi fiyattan uzağa konur (yakın olsa işlem görebilirdi) ve kısa sürede çekilir. Normal bir yatırımcının uzak emri ise genellikle saatlerce bekler. Mart 2025'te piyasa ortancası %1,2'dir; ALKLC'nin manipülasyon günlerinde %5–8'dir.

Referans alanlar (pazar, BIST 100 üyeliği, piyasa yapıcı, brüt takas, özsermaye) modele girmez, yalnız açıklama içindir. Brüt takas bir SPK/Borsa tedbiridir; modele girseydi model "tedbirli pay = manipülasyon" diye ezberlerdi (etiket sızıntısı).

`motor_ozellikleri.py` aynı tanımlarla aynı özellikleri **motor çıktısından** hesaplar; enjeksiyonlu bir günün özellikleri ancak böyle hesaplanabilir. Kontrol: enjeksiyonsuz motor özellikleri veriden hesaplananlarla birebir aynıdır (fark ortancası 0).

### 7.3 Pay-gün yöntemleri (`yontemler.py`)

| Puan | Ne yapar | Bölüm |
|---|---|---|
| `puan_zskor` | 24 özelliğin, payın kendi geçmişine göre \|z\| değerlerinin en büyüğü | 6.4 |
| `puan_kural` | Tetiklenen bent sayısı (a, b, d, f); eşitlikte Z-skor | 6.8 |
| `puan_iforest` | Z-skorlar üzerinde Isolation Forest | 6.10 |
| `puan_kesit_uc` | Aynı gün aynı pazardaki yüzdelik sıraların uçluğu | 6.7 |
| `puan_kesit_iforest` | Yüzdelik sıralar üzerinde Isolation Forest | 6.7, 6.10 |

Pay-gün kuralları (eşikler 3 ve 2):
- **a:** z(iptal oranı) ≥ 3 ya da z(emir/işlem oranı) ≥ 3;
- **b:** z(fiyat kademesi) ≥ 3 ya da z(kısa ömürlü uzak emir payı) ≥ 3;
- **d:** kapanış AOF'den |z| ≥ 3 sapmış ve kapanış seansı hacim payı z ≥ 2; ya da kapanış müzayedesi sapması |z| ≥ 3 ve kapanış toplama dengesizliği |z| ≥ 2, ikisi aynı yönde; ya da açılış iptal oranı z ≥ 3 ve açılış sapması |z| ≥ 2;
- **f:** |z(getiri)| ≥ 3 ve |z(aktif dengesizlik)| ≥ 2, aynı yönde; ya da z(küçük işlem payı) ≥ 3 ve |z(getiri)| ≥ 2.

### 7.4 SPK etiketleri

SPK bültenlerinden (197 PDF) manipülasyon kararları çıkarıldı (`veri/araclar/spk_bulten_etiket.py`; kurallar `veri/etiketler/etiket-cikarim-kurallari.md`; elle doğrulama `dogrulama-kaydi.md`). Seviyeler:
- **A:** manipülasyon dönemi bültende gün düzeyinde yazılıdır. O dönemin işlem günleri pozitiftir. Mart 2025'te ALKLC (12 pay-gün).
- **B:** yalnız işlem yasağı (tedbir) tarihi bilinir. Varsayım: manipülasyon yasaktan önceki **20 işlem günüdür** ve pencere yasaktan 3 iş günü önce biter. Gerekçe: dönemi ve yasağı birlikte bilinen 4 vakanın dördünde de dönem, yasaktan 3 iş günü önce bitiyor. Yasaktan önceki 2 iş günü **belirsiz**dir, değerlendirmeye alınmaz. Mart 2025'te 8 pay, 64 pay-gün.
- Resmî tatiller iş günü sayılmaz (`TATILLER`, 2024–2026).
- Etiketsiz gün negatif değildir (bölüm 6.14).

### 7.5 5 dakikalık pencere (`pencere.py`)

Pencere özellikleri motor çıktısından hesaplanır:

| Özellik | Ne ölçer |
|---|---|
| `islem_sayisi`, `hacim` | İşlem sayısı ve lot |
| `getiri` | Pencere son fiyatı / önceki pencere son fiyatı (log) |
| `aktif_dengesizlik` | Agresif alış − satış dengesizliği |
| `yeni`, `iptal`, `iptal_orani` | Emir olayları |
| `uzak_kisa_pay` | Kısa ömürlü uzak emir miktar payı |
| `fiyat_kademesi` | Farklı limit fiyat sayısı |
| `net_adim` | Ardışık sürekli işlemlerde fiyatı yukarı iten agresif alış sayısı − aşağı iten agresif satış sayısı (fiyat yükseltme izi) |
| `derinlik_dengesizlik`, `derinlik` | Defter örneklerinden en iyi 5 seviyede alış/satış dengesizliği ve toplam derinlik |

Puanlama: her özellik **aynı pay-günün diğer pencerelerine göre** sağlam z ile ölçülür (bölüm 6.6). Kurallar:
- **a/b:** z(iptal oranı) ≥ 3 ya da z(kısa ömürlü uzak emir payı) ≥ 3;
- **f:** |z(getiri)| ≥ 3 ve |z(aktif dengesizlik)| ≥ 2 aynı yönde, ya da |z(net adım)| ≥ 3;
- **d:** kapanış müzayedesi penceresinde, geçmiş kapanışlara göre (aşağıda).

**Gerçek bir örnek (yanıltıcı emir, MNDTR 13.03.2025, 16:20 penceresi):** o pencerede girilen sürekli işlem limit emirlerinin miktarca %71'i kısa ömürlü uzak emirdi (bunlar sentetik katmanlardır). Günün pencerelerinde bu değerin ortancası 0'dır. Sağlam z 9,8 çıktı, a/b kuralı tetiklendi ve pencere günün 102 penceresi içinde 1. sırada yer aldı.

**Kapanış penceresi özel durumu:** kapanış müzayedesi penceresi her gün aynı günün diğer pencerelerinden farklıdır: hacim çok yüksektir, fiyat sıçrar. Aynı günle kıyaslanırsa her gün "şüpheli" görünür. Bu yüzden kapanış penceresi **payın önceki günlerdeki kapanışlarına göre** puanlanır (`kapanis_gecmisi`). Kullanılan göstergeler: kapanışın AOF'den sapması, kapanış seansı payı, kapanış öncesi getiri, kapanış müzayedesi sapması, toplama dengesizliği ve son dakika payı. Isolation Forest ve denetimli model bu pencereyi puanlamaz. Kapanış penceresi, motorun kaydettiği kapanış eşleşme anından (`kapanis_ani`) bulunur.

### 7.6 Denetimli modelin eğitimi, adım adım (`pencere_degerlendir.py` + `denetimli.py`)

1. **Pay-gün seçimi:** 10 Mart sonrası (Z-skor için 5 gün geçmiş gerekir), sürekli işlemde en az 300 işlem, SPK etiketsiz, özsermaye günü olmayan pay-günlerden rastgele 80 tane (tohum 11). Tohum rastgele seçimi sabitler; aynı tohumla herkes aynı 80 pay-günü alır.
2. **Senaryo atama:** sırayla kapanış, yanıltıcı emir, yükseltme, karşılıklı işlem; her senaryoya 20 pay-gün. Saat 10:30–17:00 arasında rastgele seçilir (kapanış hariç).
3. **İki oynatma:** her pay-gün enjeksiyonsuz ve enjeksiyonlu oynatılır. Her ikisinden pencereler çıkar; bir günde yaklaşık 100 pencere.
4. **Etiket:** enjeksiyonlu koşuda ilk ve son sentetik olay arasında kalan pencereler 1, diğerleri 0 olur.
5. **Ayıklama:** temiz olmayan vakalar, bütün olayları reddedilen vakalar, kapanış senaryosu ve kapanış pencereleri çıkarılır. Kalan: 59 pay-gün, 5.912 pencere, bunların 111'i pozitif (%1,9).
6. **Girdi:** 12 pencere özelliği (log dönüşümlü) ve 12 sağlam z, toplam 24 sütun.
7. **Gruplu 5 katlı çapraz doğrulama:** her katta yaklaşık 47 pay-günle eğitilir, kalan yaklaşık 12 pay-günle sınanır. Sınanan pay-günlerin enjeksiyonsuz pencereleri de aynı modelle puanlanır; bu, yanlış alarm kontrolüdür.
8. **Ölçüm:** ROC-AUC, ortalama kesinlik, ilk 3 isabeti ve kontrol ilk 3; senaryo bazında.

Model bir dosyaya kaydedilmez; her çalıştırmada yeniden eğitilir (birkaç saniye). Arayüz bu modeli kullanmaz; arayüzdeki uyarılar kural tabanlıdır.

**Modelin kuralların göremediğini görmesine bir örnek (karşılıklı işlem, BURCE 19.03.2025):** enjekte edilen pencerelerden birinde hacim 141.642 lottu; günün pencere ortancası 15.476 lot, yani yaklaşık 9 kat. Ama günün pencereleri zaten çok oynak olduğu için log ölçeğinde sağlam z yalnız 1,7'dir; hiçbir kuralın eşiği (3) aşılmaz. Model ise hacim artışını öteki zayıf işaretlerle birleştirerek bu pencereleri ayırt etmeyi öğreniyor (karşılıklı işlemde ROC-AUC 0,90, kurallarda 0,48).

### 7.7 SPK günlerinde pencere düzeyi (`spk_pencere.py`)

SPK etiketli 76 pay-gün, aynı payların etiketsiz 100 günü ve rastgele 300 pay-gün motorla oynatıldı. Her günün pencere uyarı sayıları gün puanına çevrildi ve etiketlerle karşılaştırıldı.

---

## 8. Sonuçlar

### 8.1 SPK vakaları, pay-gün (Mart 2025)

| Puan | ROC-AUC (A) | ROC-AUC (B) | ROC-AUC (A+B) |
|---|---|---|---|
| Z-skor (kendi geçmişi) | 0,65 | 0,52 | 0,53 |
| İktisadi kurallar | 0,47 | 0,59 | 0,57 |
| Isolation Forest | 0,53 | 0,53 | 0,53 |
| Kesitsel uç sıra | 0,89 | 0,50 | 0,56 |
| Kesitsel Isolation Forest | 0,90 | 0,53 | 0,59 |

- A vakasında (ALKLC) kesitsel karşılaştırma iyi çalışıyor. Kendi geçmişine bakan yöntemler zayıf kalıyor, çünkü manipülasyon Şubat'ta başladı ve geçmiş de kirli (bölüm 6.7).
- B'de sonuç rastgeleye yakındır. B penceresi bir varsayımdır ve B tedbirleri çoğunlukla "işlem bazlı" şüpheye dayanır.
- Pozitif sayısı azdır (12 ve 64 pay-gün). Sonuçlar 12 aylık veriyle tekrarlanmalıdır.

### 8.2 Sentetik enjeksiyon, 5 dakikalık pencere (×1, 80 enjeksiyon)

Hücreler: ROC-AUC / ilk 3 isabeti / kontrol ilk 3 (yanlış alarm).

| Senaryo | Z-skor | Kurallar | Isolation Forest | Denetimli |
|---|---|---|---|---|
| Yanıltıcı emir | 0,94 / %74 / %0 | 0,95 / %89 / %5 | 0,82 / %5 / %0 | 0,95 / %95 / %0 |
| Karşılıklı işlem | 0,48 / %0 / %0 | 0,48 / %5 / %5 | 0,49 / %5 / %5 | 0,90 / %80 / %10 |
| Fiyat yükseltme | 0,58 / %0 / %0 | 0,60 / %10 / %5 | 0,59 / %5 / %5 | 0,71 / %30 / %5 |
| Kapanış | 0,78 / %15 / %0 | 0,77 / %20 / %5 | — | — |

Büyüklüğe duyarlılık (aynı pay-günler, senaryolar ×0,3 ve ×3; hücreler ROC-AUC / ilk 3):

| Senaryo | ×0,3 | ×1 | ×3 | Hangi yöntemle |
|---|---|---|---|---|
| Yanıltıcı emir | 0,95 / %89 | 0,95 / %89 | 0,95 / %89 | Kurallar |
| Karşılıklı işlem | 0,79 / %35 | 0,90 / %80 | 0,95 / %95 | Denetimli |
| Fiyat yükseltme | 0,56 / %5 | 0,60 / %10 | 0,62 / %10 | Kurallar |
| Kapanış | 0,58 / %5 | 0,77 / %20 | 0,87 / %45 | Kurallar |

Kontrol (yanlış alarm) her ölçekte %0–15'tir. 15 dakikalık pencere fiyat yükseltmeyi iyileştirmedi (kurallar 0,51).

Ne anlama geliyor:
- **Yanıltıcı emir** kurallarla iyi yakalanıyor ve büyüklükten bağımsızdır. Kısa ömürlü uzak emir payı bir orandır; küçük katmanlar da iz bırakır. Kural büyüklüğe değil davranış biçimine bakıyor.
- **Karşılıklı işlem** yalnız denetimli modelle, hacim artışından yakalanıyor (aktör kimliği yok) ve büyüklükle güçleniyor.
- **Kapanış etkilemesi** büyüklükle ölçekleniyor. Günlük hacmin %1'i görünmüyor, %3'ü sınırda, %9'u açıkça görünüyor.
- **Fiyat yükseltme** bu büyüklükte (200 saniyede 10 agresif alış) likit paylarda olağan fiyat hareketinden ayrışmıyor. Bu bir bulgudur: göstergenin değil senaryonun özelliğidir; daha büyük ve uzun yükseltmelerle sınanmalıdır.
- **Isolation Forest** her senaryoda kuralların gerisindedir (bölüm 6.10'daki neden).

### 8.3 Sentetik enjeksiyon, pay-gün düzeyi

Aynı senaryolar bütün günün özelliklerine bakılarak ölçüldü: 76 temiz vaka; 4 vaka temizlik ölçütüyle dışarıda. Kurallar kapanışta 0,81, fiyat yükseltmede 0,72, karşılıklı işlemde 0,70, yanıltıcı emirde 0,68 alıyor. Ama enjeksiyonsuz kontrol kümesi de 0,64 alıyor, çünkü seçilen likit pay-günler zaten yüksek puan alıyor. Enjeksiyonun gerçek katkısı ≈ 0,09'dur.

Sonuç: 30 saniyelik bir yanıltıcı emir ya da 200 saniyelik bir yükseltme günün toplamında kaybolur. Pencere düzeyine geçmenin gerekçesi budur. Bu örnek kontrol kümesinin neden şart olduğunu da gösteriyor: yalnız 0,73'e baksaydık yöntemi olduğundan iyi sanırdık.

### 8.4 SPK günlerinde pencere düzeyi

Gün başına kural uyarısı sayısı A'yı (ALKLC) ayırt etmiyor (ROC-AUC 0,44). B'de zayıf bir sinyal var (0,61; iptal / yanıltıcı emir uyarıları 0,57).

| Grup | Uyarı penceresi (gün başına ortalama) | a/b | f | d |
|---|---|---|---|---|
| A (ALKLC) | 11,9 | 3,4 | 8,6 | 0,00 |
| B | 19,6 | 12,4 | 8,4 | 0,02 |
| Aynı payların etiketsiz günleri | 13,6 | 5,9 | 8,3 | 0,04 |
| Rastgele pay-günler | 16,3 | 10,8 | 7,0 | 0,03 |

Neden A'da çalışmıyor: pencere puanı aynı günün diğer pencerelerine göredir. Bütün güne ve haftalara yayılan bir manipülasyonda, gün içinde öne çıkan pencere olmaz; ALKLC'nin her penceresi "aynı derecede manipülasyonlu"dur. Bu vakalarda doğru araç gün düzeyindeki kesitsel karşılaştırmadır (0,90).

**İki düzey birbirini tamamlar:** gün düzeyi uzun süreli manipülasyonu, pencere düzeyi kısa epizotları yakalar.

---

## 9. Görselleştirme arayüzü (`arayuz/`)

Çalıştırma: `streamlit run arayuz/uygulama.py`. Tarayıcıda bir sayfa açılır.

Ekranda:
- **Sol menü:** gün, pay, senaryo ve senaryo parametreleri (saat, miktar, katman sayısı, süre…) ve **Oynat** düğmesi.
- **SPK etiketi kutusu:** seçilen pay-gün SPK etiketliyse seviye ve bülten numarası görünür (ör. ALKLC 11.03: A, bülten 2025-17).
- **Dört gösterge:** taban kapanış; enjeksiyonlu kapanış ve farkı; sentetik işlem sayısı / adedi; 5 dk pencere kural uyarısı sayısı.
- **Fiyat grafiği:**
  - gerçek akışın motorla üretilen fiyatı mavi, enjeksiyonlu fiyat turuncu çizgiyle gösterilir; turuncu yalnız ayrıştığı yerde görünür;
  - sentetik aktörün işlemleri nokta, kural uyarıları üçgen ile işaretlenir;
  - müzayede, devre kesici ve EBDKS bölümleri gri bantlarla gösterilir.
- **Dakikalık hacim grafiği** (ayrı eksen).
- **Sekmeler:** uyarı tablosu (hangi bent, hangi z), sentetik işlemler, reddedilen sentetik olaylar (sebebiyle), dakikalık tablo.

**Sunum için önerilen gösterim:**
1. ALKLC.E 11.03.2025, senaryo yok: SPK etiketi A görünür; gerçek bir manipülasyon gününün fiyatı ve uyarıları.
2. Likit bir pay (THYAO.E ya da ASELS.E), "Yanıltıcı emir", saat 14:00:00: turuncu çizgi, sentetik işlem (karşı emir) ve o pencerede a/b uyarısı.
3. "Kapanış fiyatını etkileme", alış, büyük miktar: enjeksiyonlu kapanış fiyatı yukarı kayar (ASELS 19.03, 200.000 lot: 112,30 → 113,00).
4. Bir sentetik emri kurala aykırı girmek (ör. kapanış bandı dışı): "Reddedilen sentetik olaylar" sekmesinde sebebi görülür. Motor kuralları uyguluyor.

---

## 10. Sınırlar ve dürüst notlar

- **Gerçek akış dışsaldır:** gerçek katılımcılar sentetik emirlere tepki vermez (bölüm 5.1).
- **Aktör kimliği yok:** bent c (yön değiştiren emir) ve gerçek veride bent ç (karşılıklı işlem) doğrudan ölçülemez.
- **Tek ay:** bütün sonuçlar Mart 2025'tendir. Pozitif sayısı azdır (A 12, B 64 pay-gün). 12 aylık veriyle tekrarlanmalıdır.
- **B etiketi varsayımdır** (20 işlem günü).
- **Senaryo büyüklükleri varsayımdır;** bu yüzden ×0,3, ×1 ve ×3 duyarlılık analizi yapıldı.
- **Eşikler (3 ve 2) tasarım parametresidir,** Prosedür kuralı değildir.
- **Denetimli model sentetik etiketle eğitildi:** öğrendiği, bizim senaryolarımızın imzasıdır. Gerçek manipülatör farklı davranırsa model bunu tanımayabilir. SPK etiketleriyle eğitim 12 aylık veriyle yapılacak.
- **Kapsam dışı:** kotasyonlar (piyasa yapıcı), orta nokta emirleri, özel işlem bildirimleri.
- **Özsermaye günleri:** düzeltilmiş baz fiyat kaynağı yok; bu günler dışarıda.
- **Bilinmeyenler:** değişiklik sebebi 116/117'nin anlamı; `guncelleme_no` atlamaları (%0,9); aynı µs içindeki olayların sırası (ITCH ile çözülebilir).
- **Bölüm sınırları payın kendi satırlarından okunur.** Çok seyrek işlem gören bir payda sentetik emir, payın o bölümdeki ilk satırına kadar bir önceki bölüme yerleşebilir. Değerlendirmede en az 300 işlemli paylar kullanıldığı için etkisizdir.

---

## 11. 24.10.2026 taramasında bulunan ve düzeltilen hatalar

Bütün kod ve belgeler satır satır okundu; şüpheli noktalar gerçek veriyle sınandı. Bulunanlar etki sırasıyla:

1. **Kapanış penceresi yanlış işaretleniyordu.** Pencere tespiti kapanış müzayedesi penceresini `P_ESLESTIRME` bölüm adından buluyordu. Açılış müzayedesi (09:55) ve bazı devre kesici müzayedeleri de bu adı taşıdığı için onlar da "kapanış penceresi" sayılıyordu. Sonuçları:
   - kapanış senaryosunda açılış penceresi de pozitif sayıldı (20 vakanın 19'unda);
   - açılış penceresine geçmiş kapanışlara göre puan ve bent d verildi;
   - denetimli model açılış penceresini hiç görmedi;
   - bir pay-günde motorun kapanış seansı payı yanlış hesaplandı (veriden 0,093 farklıydı; şimdi en büyük fark 0,00018).

   Düzeltme: motor kapanış müzayedesinin eşleşme anını kaydeder (`Gun.kapanis_ani`). Kapanış penceresi ve motor tarafındaki kapanış göstergeleri bu andan bulunur.
2. **Isolation Forest kapanış penceresini aynı günle kıyaslıyordu.** Bu pencere her gün uç değer olduğundan, kapanış senaryosunda enjeksiyonsuz kontrol de ROC-AUC 0,83 alıyordu (enjeksiyonlu 0,84). Yani yöntem bir şey ayırt etmiyordu. Düzeltme: Isolation Forest yalnız sürekli işlem pencerelerinde çalışır; kapanış penceresini yalnız geçmiş kapanışlara dayanan Z-skor ve kural puanlar.
3. **Karşılıklı işlem senaryosu çoğu zaman karşılıklı işlem değildi.** Fiyat "son işlem + 1 adım" idi; o fiyatta ya da altında gerçek satıcılar varsa aktörün alışı önce onlarla eşleşiyordu. Ölçüm (20 vaka): miktarın ortalama %75'i aktörün kendi emirleri arasındaydı; 3 vakada yalnız %10–35. Düzeltme: makasın içinden fiyat ve makasın açılmasını bekleme; temizlik ölçütü eklendi. Sonuç: ortalama %89; 13/20 vakada %90'ın üstü (önce 5/20).
4. **Ölçüm kontrolü devre kesici ve açığa satışta yutuluyordu.** `gun.py`'deki `except KeyError` blokları `OlcumEksik`'i de yakalıyordu (`OlcumEksik`, `KeyError`'ın alt sınıfıdır). Devre kesicisi ölçülmemiş bir ayda devre kesici sessizce kapanırdı. Düzeltme: `parametreler.varsa`; ölçüm kontrolü artık pazara göre yapılır.
5. **Kapanış müzayedesi gün sonunda eşleştirilmeyebiliyordu.** Veride kapanış eşleştirme ve kapanış fiyatından işlemler satırı olmayan pay-günlerde toplanan defter eşleştirilmeden kalıyordu. Enjeksiyonla kapanışta işlem doğabileceği için artık gün sonu bölümünde eşleştirilir.
6. **Defter örnekleme aralığı 10 sn'den 1 sn'ye indi.** Senaryoların kullandığı en iyi fiyat 10 saniyeye kadar eskiyebiliyordu. Önceki pay-gün koşusunda katmanları dolduğu için dışarıda kalan vaka (AVHOL 12.03) artık temizdir.
7. **SPK etiketlerinde tatil listesi eksikti.** 2024'ün ilk yarısı, 2025 Kurban Bayramı ve 2025 sonu ile 2026 tatilleri yoktu. 1.588 etiket satırının 102'si değişti. Veri döneminde değişen 2 satır var (SONME 28–29.05.2025); Mart 2025'te değişen yok.
8. **Sessiz atlamalar.** Bütün sentetik olayları reddedilen vaka (VAKBN 21.03, EBDKS durdurması) pencere değerlendirmesinde sessizce atlanıyordu. Pay-gün değerlendirmesinde ise manipülasyon hiç girmediği hâlde "enjekte edilmiş" sayılıyordu. Artık iki değerlendirme de vakayı sebebiyle yazıp dışarıda bırakır.
9. **Açıklama hataları:**
   - bent b tanımında kısa ömürlü uzak emir payı eksikti;
   - karşılıklı işlem bendi "c" yazılmıştı (doğrusu ç);
   - `TASARIM.md` ve `rapor.md`'de birkaç eski ifade vardı.
10. **Arayüz:**
    - SPK etiketi kutusu eklendi;
    - uyarı fiyatı pencere uzunluğuna bağlandı;
    - enjeksiyon özetindeki kapanış müzayedesi fiyatı artık kapanış anından alınır;
    - arayüz bütün senaryolarla uçtan uca sınandı.

Doğrulama: 35 birim testi geçer. Motorun tekrar oynatma doğruluğu değişmedi (THYAO 19.03: müzayedeler %100, sürekli işlem %99,82, bütün gün %99,34).

---

## 12. Sunumda sorulabilecek sorular

**"Motorunuzun doğru olduğunu nereden biliyorsunuz?"** Gerçek emirleri verip gerçek işlemleri birebir karşılaştırıyoruz: iki tarafın emir numarası, fiyat ve adet. Bütün paylarda %99,85 ve %99,91 aynı, müzayedelerde %100. Ayrıca 35 birim testi var; testler Prosedür'ün kendi örneklerini (Ek-16, Ek-18) içeriyor.

**"Prosedür'de yazan kuralı mı uyguladınız, verideki kuralı mı?"** Kural dosyaları yürürlükteki Prosedür'ü yazar. Veri tarihinde farklı uygulanan kurallar (marj ±%10, devre kesici yalnız düşüşte %5, EBDKS eski eşikleri) veriden ölçüldü ve tarih parametresi olarak tutuldu. Fark "Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayıtlıdır.

**"Neden ajan tabanlı simülasyon yapmadınız?"** Gerçek emir akışı ajanlardan daha gerçekçidir ve motorun doğruluğu ölçülebilir. Ajan simülasyonunun kalibrasyonu (GA/PSO) doğrulanamayan bir varsayımlar zinciri olurdu.

**"Z-skor nedir, neden kullandınız?"** Bir değerin, payın kendi geçmişindeki ortalamadan kaç standart sapma uzak olduğu. Her payın normali farklı olduğu için ham değer yerine "bu pay için ne kadar olağan dışı" sorusunu sorar ve farklı birimlerdeki özellikleri aynı ölçeğe getirir. Basit ve açıklanabilir bir temel çizgidir. Zayıf yanı: geçmiş de manipülasyonluysa olağan dışılığı göremez. Bunu ALKLC örneğinde gösteriyoruz ve kesitsel karşılaştırmayla çözüyoruz.

**"Neden sağlam Z-skor (ortanca, MAD)?"** Pencere düzeyinde manipülasyonlu pencere uç değerdir. Ortalama ve standart sapma uç değerden etkilenir ve onu gizler; ortanca ve MAD etkilenmez (bölüm 6.6'daki örnek: z 2'ye karşı 128).

**"Isolation Forest neden zayıf?"** Olağan dışı olanı bulur, manipülasyonu değil. Borsada olağan dışı pencere çoktur (haber, büyük alım). Kurallar manipülasyonun belirli imzasına bakar. Bu bir bulgudur: genel aykırılık tespiti, hedefli göstergelerin yerini tutmuyor.

**"Model neye bakıyor?"** Permütasyon önemine göre en çok hacim z'sine (0,25), kısa ömürlü uzak emir payına (0,08) ve aktif taraf dengesizliğine bakıyor. Bunlar senaryoların iktisadi izleriyle uyumlu; model anlamsız bir şeyi ezberlemiş görünmüyor.

**"Ezber (overfitting) var mı?"** Model hep görmediği pay-günlerde ölçülüyor (gruplu çapraz doğrulama). Ayrıca aynı günlerin enjeksiyonsuz hâlinde yanlış alarm oranı ölçülüyor: yanıltıcı emirde %0, karşılıklı işlemde %10.

**"Neden derin öğrenme yok?"** Veri tablo biçiminde ve etiketli pozitif az (111 pencere). Bu koşullarda gradyan artırmalı ağaçlar hem daha başarılı hem daha açıklanabilirdir. Derin öğrenme binlerce pozitif örnek ister.

**"Sentetik manipülasyon gerçekçi mi?"** Senaryolar Tebliğ bentlerine bağlı. Motor sentetik emirleri borsa kurallarıyla doğruluyor ve aykırıları reddediyor. Temizlik ölçütleri var: yanıltıcı emir katmanları işlem görmemeli, karşılıklı işlem aktörün kendi emirleri arasında olmalı. Büyüklükler varsayım olduğu için üç ölçekte sınandı. Sınır: gerçek katılımcılar tepki vermiyor.

**"Neden bazı senaryoları yakalayamıyorsunuz?"** Fiyat yükseltme (200 saniyede 10 agresif alış) likit paylarda olağan fiyat hareketinden ayrışmıyor. Bu bir bulgudur: bu büyüklükte bir yükseltme bu göstergelerle görünmez. Karşılıklı işlem aktör kimliği olmadan ancak hacim artışıyla görülebiliyor; bunu yalnız denetimli model yakalıyor.

**"SPK vakalarında neden sonuç zayıf?"** Etiketler kaba: B için tarih penceresi bir varsayım, etiketsiz gün negatif değil ve pozitif sayısı az. A vakasında (ALKLC) kesitsel karşılaştırma ROC-AUC 0,90 veriyor.

**"ROC-AUC 0,95 ne demek?"** Rastgele seçilen bir manipülasyonlu pencerenin, rastgele seçilen normal bir pencereden daha yüksek puan alma olasılığı %95. Pratikte bundan daha anlaşılır ölçütümüz "ilk 3": yanıltıcı emirde enjekte edilen pencere 19 günün 17'sinde günün en şüpheli 3 penceresinden biri; enjeksiyonsuz günde aynı pencere yalnız 1 günde ilk 3'e giriyor.

**"Veri sızıntısı (leakage) var mı?"** Z-skor yalnız geçmiş günleri kullanır (testle sınanıyor). Denetimli model pay-güne göre gruplu çapraz doğrulamayla ölçülür. Kapanış penceresi geçmiş kapanışlara göre puanlanır. Brüt takas gibi tedbir alanları modele girmez.

---

## 13. Dosya haritası, komutlar, sözlük

| Ne | Komut |
|---|---|
| Testler | `python -m pytest motor/testler tespit/testler` |
| Bir pay-günü oynat ve karşılaştır | `python -I motor/tekrar_oynat.py veri/gun-ici-emir/gunluk veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet 2025-03-19 THYAO.E --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet` |
| Bir günün bütün payları | `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv` |
| Enjeksiyon | `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]` |
| Pay-gün özellikleri | `python -I tespit/ozellikler.py GUNLUK ISLEM GUNSONU CIKTI.parquet` |
| SPK değerlendirmesi | `python -I tespit/degerlendir.py OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI` |
| Pencere değerlendirmesi | `python -I tespit/pencere_degerlendir.py OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI 80 11` (`OLCEK`, `PENCERE_DK` ortam değişkenleri) |
| Denetimli model | `python -I tespit/denetimli.py CIKTI/pencereler.parquet CIKTI` |
| SPK günlerinde pencere | `python -I tespit/spk_pencere.py OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI` (sonra `--degerlendir`) |
| Arayüz | `streamlit run arayuz/uygulama.py` |

Sözlük:

| Terim | Anlamı |
|---|---|
| Aktif / pasif | Gelen (eşleşmeyi başlatan) emir / defterde bekleyen emir |
| AOF | Ağırlıklı ortalama fiyat (hacim / miktar) |
| AP (ortalama kesinlik) | Listenin başının ne kadar temiz olduğunu ölçen sıralama ölçütü |
| Baz fiyat | Günün referans fiyatı (önceki kapanış) |
| Çapraz doğrulama | Veriyi parçalara bölüp her parçayı onu görmemiş bir modelle sınama |
| Denetimli / denetimsiz | Etiketle öğrenen / etiketsiz öğrenen yöntem |
| Denge fiyatı | Müzayedede bütün işlemlerin yapıldığı tek fiyat |
| Duyarlılık (recall) | Manipülasyonların yakalanan oranı |
| EBDKS | Endekse bağlı devre kesici |
| Etiket | Bir örneğin doğru cevabı (manipülasyon var / yok) |
| Ezber (overfitting) | Modelin eğitim örneklerini ezberleyip yenilerde başarısız olması |
| Gradyan artırma | Hataları sırayla düzelten küçük karar ağaçlarının toplamı |
| Isolation Forest | Az rastgele bölmeyle yalnız kalan noktaları aykırı sayan yöntem |
| Kesinlik (precision) | Alarmların doğru çıkan oranı |
| Kesitsel | Aynı gün diğer paylarla karşılaştırma |
| KİE | Kalanı iptal et |
| MAD | Ortancadan mutlak sapmaların ortancası |
| Özellik | Bir pay-gün ya da pencere için hesaplanan sayısal gösterge |
| Pay-gün | Bir payın bir işlem günü |
| Pencere | 5 dakikalık zaman dilimi |
| ROC-AUC | Rastgele bir pozitifin rastgele bir negatiften yüksek puan alma olasılığı |
| Tepe | Kısmi görünme emrinde görünen kısım |
| Tohum (seed) | Rastgele seçimleri tekrar edilebilir kılan başlangıç sayısı |
| Z-skor | Değerin ortalamadan kaç standart sapma uzak olduğu |
