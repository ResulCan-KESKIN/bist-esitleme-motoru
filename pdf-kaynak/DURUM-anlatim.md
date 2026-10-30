---
kisa: Proje durumunun sade anlatımı
alt: `DURUM.md` bölüm bölüm, hiç bilmeyen birine anlatır gibi: nerede kaldık, ne bitti, ne bekliyor, hangi karar neden verildi
tarih: 30.10.2026
---

# Proje durumunun sade anlatımı

Bu belge `DURUM.md` dosyasının (son kaydı 30.10.2026) sade dille, ayrıntılı anlatımıdır. `DURUM.md` projenin "kaldığımız yer" sayfasıdır: sohbet geçmişi olmadan, yeni bir çalışma oturumunda işe kaldığı yerden devam edebilmek için tutulur. Bu yüzden çok kısa, kısaltmalı notlarla yazılmıştır. Burada her not açılır: ne yapıldı, neden yapıldı, sonuç ne, sırada ne var.

Belgenin ilk sürümü 25.10.2026 tarihliydi (o günkü durum: yalnız Mart 2025 verisi). Bu sürüm 30.10.2026 durumunu anlatır: 18 aylık veri, 18 ayla ölçülen sonuçlar, hisseye göre ayarlı senaryo ve SPK etiketleriyle eğitilen model.

`DURUM.md`'nin bazı bölümleri tarihli kayıtlardır (21.10.2026, 22.10.2026, 24.10.2026). O günlerde yazılan bazı sayılar sonraki koşularda güncellendi. Bu belgede her yerde **güncel** değer kullanıldı; `DURUM.md`'de eski kalan sayılar ve bilgiler bölüm 14'te tek tabloda listelendi. Sayıların ayrıntılı kaydı `rapor.md`'dedir; bölüm numaraları yanlarında yazılıdır.

Sarı kutular benzetme, örnek ya da "akılda kalsın" özetidir. Sistemin kendisinin anlatımı `ANLATIM.pdf`'de, tasarımın sade anlatımı `TASARIM.pdf`'de, verinin kısa özeti `VERI.pdf`'dedir.

## 0. DURUM.md nedir, nasıl okunur?

### 0.1 Neden böyle bir dosya var?

Proje uzun süren, çok oturumlu bir çalışmadır. Her oturumda yapılan işler, verilen kararlar ve yarım kalan noktalar bir yere yazılmazsa, bir sonraki oturumda "nerede kalmıştık?" sorusu saatler alır. `DURUM.md` bu soruyu tek sayfada cevaplar.

> **Benzetme:** Bir inşaatın şantiye defteri. Mimari proje (`TASARIM.md`) binanın nasıl olacağını söyler; şantiye defteri (`DURUM.md`) bugün hangi katın döküldüğünü, hangi malzemenin beklendiğini, hangi kararın kimden çıktığını söyler. Çalışma raporu (`rapor.md`) ise bütün günlerin ayrıntılı kaydıdır.

### 0.2 Dosyanın bölümleri

| `DURUM.md` bölümü | Ne anlatır | Bu belgede |
|---|---|---|
| Kaldığımız yer ve yapılacaklar (24.10 kaydı ve 25, 26, 29.10 ekleri) | Son oturumlarda yapılanlar ve sıradaki işler | Bölüm 2, 3 |
| Çalıştırma notları | Hangi komutla ne çalıştırılır | Bölüm 4 |
| Klasör düzeni | Hangi klasörde ne var | Bölüm 5 |
| Kural dosyaları | 8 kural dosyasının durumu | Bölüm 6 |
| DataStore gün içi verisi ve sistem tasarımı (21.10.2026) | Veri kararı, eldeki veri, kullanıcı kararları | Bölüm 7 |
| Eşleştirme motoru, arayüz ve tespit (22.10.2026) | Motor ve tespitin ilk sürüm kaydı | Bölüm 8 |
| Öneri formu ve veri talebi | Bölüme verilen formla ve veri dilekçesiyle farklar | Bölüm 9 |
| SPK bülten etiketleme | Gerçek manipülasyon etiketlerinin nasıl çıkarıldığı | Bölüm 10 |
| Çeviriler ve doğrulamalar | Protokol çevirileri, ITCH 2018 doğrulaması | Bölüm 11 |
| Bilinen açık noktalar | Henüz anlamı bilinmeyenler | Bölüm 12 |
| Çalışma notları | Uyulacak teknik kurallar | Bölüm 13 |

### 0.3 Görev tanımı ve işaretler

`DURUM.md`'nin ilk satırı kural dosyalarının nasıl yazılacağını hatırlatır (`gorev-kural-yazimi.md`). Kuralların sade anlamı ve gerekçesi:

| Kural | Sade anlamı | Neden |
|---|---|---|
| Kaynakta olmayanı ekleme | Prosedür'de yazmayan bir kuralı "mantıklı geldi" diye ekleme | Motor borsanın kurallarını taklit ediyor; uydurulan kural taklidi bozar |
| Madde numarası sona | Her kuralın kaynaktaki madde numarası cümlenin sonuna yazılır | Her kuralın nereden geldiği izlenebilsin |
| Belirsizlik → "Açık sorular" `[DOĞRULA]` | Metin iki türlü okunabiliyorsa yorum yapma, soru olarak yaz | Yanlış yorum sessizce koda geçmesin |
| Örnekler → "Test örnekleri" | Kaynaktaki sayısal örnekler ayrı bölüme | Birim testlerinin verisi buradan gelir |
| Dosya adlarında Türkçe karakter yok | `gorev-kural-yazimi.md` yazılır, `görev-kural-yazımı.md` değil | Farklı işletim sistemlerinde ve araçlarda dosya adı bozulmasın |
| Her oturumda tek kural dosyası | Bir oturumda yalnız bir dosya yazılır | Dikkat dağılmasın, her dosya bütün olarak gözden geçirilsin |
| Bitince `[DOĞRULA]` listesini göster | Oturum sonunda açık sorular kullanıcıya gösterilir | Kararı kullanıcı versin |

Kural dosyalarındaki işaretler:
- **`[DOĞRULA]`:** açık soru; henüz karar yok.
- **`[DOĞRULANDI …]`, `[KISMEN DOĞRULANDI …]`:** kapanmış ya da kısmen kapanmış soru; nasıl kapandığı yanında yazılı.
- **`[BİLGİ …]`:** veriden gelen ölçüm notu ("Mart 2025'te şu kadar vaka gördük").
- **Uygulama kararı (kullanıcı):** kaynak belirsizken kullanıcının verdiği karar; açıkça kullanıcıya ait olduğu yazılır.

> **Akılda kalsın:** Projede üç tür bilgi birbirinden ayrı tutulur: **metin** (Prosedür ne diyor), **veri** (borsada gerçekte ne oldu), **karar** (ikisi uyuşmadığında ya da metin sustuğunda ne yapıyoruz). Her cümlenin hangisi olduğu işaretlidir.

## 1. Tek bakışta: proje nerede?

| Parça | Durum | Kanıt |
|---|---|---|
| Kural dosyaları (8 adet) | Hepsi yazıldı; 3'ü (05, 06, 08) kullanıcı doğrulaması bekliyor | 128 açık soru (`[DOĞRULA]`) |
| Veri | 18 ay (2024-01…2025-06): gün içi emir, gün içi işlem, gün sonu, gün içi endeks, değerleme oranları. Hepsi parquet'e çevrildi ve kayıpsızlık kontrolünden geçti; emirler gün gün bölümlendi | 371 işlem günü; ayda 0,7–1,1 milyar emir satırı. Alanların ayrıntılı doğrulaması Mart 2025 ile yapıldı |
| Tarih parametreleri | 18 ayın hepsinde veriden ölçüldü; bütün aylarda aynı çıktı | Motor 2024-01-02…2025-06-30 arasında çalışır |
| Eşleştirme motoru | Çalışıyor | Mart 2025, bütün paylar: işlemlerin %99,85'i birebir; 2024 sınamaları: ISYAT 05.02.2024 %100, THYAO 15.03.2024 %99,89 |
| Sentetik manipülasyon | 4 senaryo, iki sürüm: sabit kalıplı (eski) ve hisseye göre ayarlı (yeni) | Ayarlı senaryo 18 ayda 1.548 vaka |
| Tespit, gerçek vakalar | 18 ayla ölçüldü | SPK etiketleriyle eğitilen model, pay-gün ROC-AUC: A+B 0,71 (A 0,84, B 0,69) |
| Tespit, sentetik vakalar | 18 ayla ölçüldü; kör noktalar belirlendi | Ayarlı senaryoda yanıltıcı emir: kurallar 0,57, denetimli 0,68; fiyat yükseltme: denetimli 0,89 |
| Arayüz | Çalışıyor | `streamlit run arayuz/uygulama.py` |
| Testler | 41 test, hepsi geçer | `python -m pytest motor/testler tespit/testler` |
| Belgeler | `rapor.md` (bölüm 16'ya kadar), `ANLATIM.md`, `VERI.md` güncel; `TASARIM.md`'deki sonuç sayıları hâlâ Mart 2025'ten | Hepsi commit edildi (30.10.2026) |
| Vize raporu | Kaynağı (`rapor.md`) hazır; literatür çalışması başladı | Yapılacaklar 3.3 |

> **Benzetme:** Ev inşaatı düşün. 25.10'da temel atılmış, kaba inşaat bitmiş, elektrik tek bir odada denenmişti (motor ve tespit yalnız Mart 2025'te). Bugün bütün katların malzemesi geldi ve 18 katın hepsinde ışıklar yakıldı (motor ve tespit 18 ayda çalıştı). Şimdiki iş, hangi odaların karanlık kaldığını bulmak: **kör noktalar**. Sıradaki adım bu odalardan birine lamba takmak, ama önce lambaya gerçekten gerek olup olmadığını veriyle ölçmek.

## 2. Kaldığımız yer (24–30.10.2026)

### 2.1 Kısa takvim

| Tarih | Ne oldu | Bu belgede |
|---|---|---|
| 24.10 | 22.10 listesindeki dört iş bitti; inceleme düzeltmeleri; sistem taraması | 2.2–2.4 |
| 25.10 | Öneri formu düzeltmesi; pencere uzunluğu karşılaştırması; literatür çalışması | 2.5 |
| 26.10 | Yanıltıcı emirde kör nokta; SPK vakalarında sahte emirlerin yeri | 2.6 |
| 26–28.10 | Veri 2024-06…2025-06 tamamlandı; tarih parametreleri ölçüldü; EBDKS eşiği sınandı; Mart → 5 ay → 9 ay | 2.7 |
| 29.10 | 13 ay; hisseye göre ayarlı senaryo; 2024-01…05 eklendi; 18 ay ve SPK denetimli model | 2.8, 2.9 |
| 30.10 | 2024-01…05 tarih parametreleri; 18 ay motorlu değerlendirmeler; `VERI.md`; commit | 2.10 |

### 2.2 24.10.2026: 22.10 listesinden bitenler

22.10.2026 sonunda dört iş sıradaydı. Dördü de yapıldı (sayılar Mart 2025 iledir; 18 aylık hâlleri 2.7–2.10'da):

1. **Fiyat yükseltme için yeni gösterge ve 15 dakikalık pencere.**
   - *Ne yapıldı:* "Net agresif adım" göstergesi eklendi: bir pencerede, ardışık işlemlerde fiyatı yukarı iten agresif alış sayısından aşağı iten agresif satış sayısı çıkarılır. Ayrıca 5 dakika yerine 15 dakikalık pencere denendi.
   - *Sonuç:* Fiyat yükseltme senaryosu bu büyüklükte (200 saniyede 10 agresif alış) ayırt edilemedi. Kurallar ROC-AUC 0,56–0,62; 15 dakikalık pencerede 0,51.
   - *Sonradan anlaşıldı (29.10, 2.8):* sorun göstergede değil senaryodaydı. Eski senaryo fiyatı neredeyse hiç itmiyordu; fiyatı gerçekten iten ayarlı senaryoda kurallar 0,78'e çıkıyor.
2. **Kapanış etkilemesi göstergeleri.**
   - *Ne yapıldı:* Üç gösterge: kapanış fiyatının son sürekli işlem fiyatından sapması, kapanış emir toplamadaki alış−satış dengesizliği, emirlerin son 60 saniyedeki payı.
   - *Sonuç (Mart):* temel büyüklükte (×1) ROC-AUC 0,77, üç kat büyüklükte (×3) 0,87. Yanlış alarm her ölçekte %5.
3. **SPK etiketli günlerde pencere düzeyi.**
   - *Ne yapıldı:* Gerçek manipülasyon günlerinde, gün başına kaç pencerenin uyarı verdiğine bakıldı.
   - *Sonuç (Mart):* A vakasında (ALKLC) sinyal yok (ROC-AUC 0,44), B vakalarında zayıf (0,61).
   - *Anlamı:* Pencere puanı aynı günün diğer pencerelerine göredir; bütün güne yayılan manipülasyon gün içinde öne çıkmaz. Bu vakalarda gün düzeyindeki araçlar doğrudur (18 ayda en iyisi SPK denetimli model, 2.9).
4. **Defter göstergeleri.**
   - *Ne yapıldı:* Motorun sürekli işlemde çektiği defter fotoğraflarından derinlik dengesizliği ve toplam derinlik hesaplandı.
   - *Sonuç:* Katkı yok (denetimli modelde önem ≈ 0). En iyi 5 seviye, en iyi fiyattan 4–6 adım uzaktaki yanıltıcı katmanları ancak kısmen görüyor.

### 2.3 24.10.2026: inceleme düzeltmeleri

İki önemli düzeltme (`rapor.md` 5):

- **Ölçüm kontrolü (`OlcumEksik`).** Motor, oynatılan gün için tarih parametresinin veriden ölçülmüş bir değeri yoksa durur. Önceden, ölçüm yoksa yürürlükteki metnin değerine (ör. marj %20) sessizce düşebilirdi.

  > **Neden önemli?** Yeni bir ayın verisi geldiğinde o ayın marjını ölçmeyi unutup motoru çalıştırdığını düşün. Eski hâliyle motor yanlış marjla çalışır, sonuçlar sessizce bozulurdu ve kimse fark etmezdi. Yeni hâliyle motor ilk çalıştırmada "bu günün ölçümü yok" diye durur. 27–30.10 arasında 17 yeni ay eklendi; her ayda önce parametreler ölçüldü, motor ancak ondan sonra çalıştırıldı.

- **Yanıltıcı emir senaryosunun düzeltilmesi.**
  - Önce: katmanlar son işlem fiyatına göre yerleşiyordu; karşı emir makas genişse pasif kalıyordu (işlem görmüyordu).
  - Sonra: katmanlar aynı tarafın **en iyi fiyatına** göre yerleşir (4–6 adım geride); karşı emir agresiftir (hemen işlem görür); katmanları işlem gören vakalar "temiz değil" sayılıp değerlendirmeden çıkarılır.
  - Sonuç (Mart): yanıltıcı emir pencere düzeyinde ROC-AUC 0,95 (önce 0,89). Bu yüksek değerin yalnız "derin katmanlı" türde geçerli olduğu 26.10'da anlaşıldı (2.6).

### 2.4 24.10.2026: sistem taraması

Bütün kod ve belgeler satır satır okundu, şüpheli noktalar gerçek veriyle sınandı (`rapor.md` 6). Bulunanlar ve düzeltmeler:

| Ne bozuktu | Sonucu neydi | Nasıl düzeltildi |
|---|---|---|
| Kapanış penceresi `P_ESLESTIRME` bölüm adından bulunuyordu; açılış müzayedesi de aynı adı taşır | Açılış penceresi de "kapanış" sayıldı; kapanış senaryosunda 20 vakanın 19'unda açılış penceresi de pozitif işaretlendi | Motor kapanış eşleşme anını ayrıca kaydeder (`Gun.kapanis_ani`) |
| Isolation Forest kapanış penceresini aynı günün diğer pencereleriyle kıyaslıyordu | Kapanış penceresi her gün uç değer olduğu için enjeksiyonsuz günde de alarm veriyordu (kontrol ROC-AUC 0,83, enjeksiyonlu 0,84: ayırt edicilik yok) | Isolation Forest da denetimli model gibi yalnız sürekli işlem pencerelerinde çalışır; kapanışı geçmiş kapanışlara dayanan Z-skor ve kurallar puanlar |
| Karşılıklı işlem senaryosu "son işlem + 1 adım" fiyatından emir veriyordu | Aktörün alışı çoğu zaman gerçek satıcılarla eşleşiyordu; kendi emirleri arası işlem ortalama %75, bazı vakalarda %10–35 | Fiyat makasın içinden; makas tek adımsa açılması beklenir. Kendi emirleri arası işlem ortalama %89 |
| Ölçüm kontrolü devre kesici ve açığa satış kodunda yanlışlıkla yakalanıp yutuluyordu | Devre kesicisi ölçülmemiş bir ayda devre kesici sessizce kapanırdı | Ayrı bir kontrol (`parametreler.varsa`); kontrol artık pazara göre |
| Defter fotoğrafı 10 saniyede bir çekiliyordu | Senaryoların kullandığı "en iyi fiyat" 10 saniyeye kadar eski olabiliyordu | 1 saniyede bir |
| SPK etiketlerindeki tatil listesi eksikti | İş günü sayımı bazı tarihlerde kayıyordu; 1.588 etiket satırının 102'si değişti (Mart 2025'te değişen yok) | Tatil listesi 2024–2026 tamamlandı |
| Bütün sentetik olayları reddedilen vaka (ör. EBDKS durdurması sırasında) sessizce atlanıyor ya da "enjekte edilmiş" sayılıyordu | Değerlendirmede hiç manipülasyon içermeyen vaka pozitif sayılabiliyordu | Vaka sebebiyle yazılıp dışarıda bırakılır |
| Arayüzde SPK etiketi görünmüyordu | Gerçek vaka gününde kullanıcı bunu bilemiyordu | Seviye ve bülten bir uyarı kutusunda gösteriliyor |

> **Akılda kalsın:** Taramanın en önemli dersi, "iyi görünen" bir sonucun kontrol kümesine bakınca boş çıkabilmesidir. Kapanış penceresinde ROC-AUC 0,84 iyi görünüyordu; enjeksiyonsuz günde de 0,83 çıkınca, yöntemin aslında hiçbir şey ayırt etmediği anlaşıldı. Sonraki günlerin bütün ölçümlerinde bu yüzden her sonuç kontrolüyle birlikte verildi.

### 2.5 25.10.2026: öneri formu, pencere uzunluğu, literatür

- **Öneri formu düzeltmesi.** Kullanıcı, daha önce verdiği öneri formunun (`.docx`) yanlış olduğunu söyledi; doğrusu proje kökündeki `Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.pdf`'tir. Doğru formun başlığı projenin başlığıyla aynıdır; ajan tabanlı simülasyon, GA/PSO ve Monte Carlo bu formda **yoktur**. `ANLATIM.md` 2.3–2.4 doğru forma göre yeniden yazıldı. Eski forma dayanan yerler hâlâ duruyor: `CLAUDE.md` ("Sistem kapsamı" kararı), `TASARIM.md` 1 / 6.3 / 6.5, `rapor.md` 3.2–3.3 ve `DURUM.md`'nin "Öneri formu" bölümü. Vize raporundan önce düzeltilecek (bölüm 9 ve 14).
- **Pencere uzunluğu karşılaştırması** (`rapor.md` 7). 5 dakikalık pencere 22.10'da gerekçesi yazılmadan seçilmişti; 1, 5, 10 ve 15 dakika aynı vakalarla denendi:
  - 1 dakika çok kısa: manipülasyon birkaç pencereye bölünüyor; yanıltıcı emirde kuralların ilk 3 isabeti %89'dan %63'e düşüyor.
  - 10 ve 15 dakika yanlış alarmı artırıyor: günde daha az pencere olduğu için "ilk 3"e şansla girmek kolaylaşıyor (denetimli modelde 15 dakikada kontrol %17).
  - **5 dakika en dengeli:** her satırda birinci değil, ama isabeti yüksek, yanlış alarmı düşük (%5).

  > **Benzetme:** Bir maçı özetlemek için videoyu parçalara bölüyorsun. 1 dakikalık parçalarda tek bir atak üç parçaya bölünür, hiçbirinde tam görünmez. 15 dakikalık parçalarda ise her parçada bir şeyler olur, "en heyecanlı 3 parça" seçmek anlamını yitirir. 5 dakika, bir atağın tek parçada kaldığı ve parçaların hâlâ birbirinden ayrılabildiği uzunluktur.

- **Literatür çalışması başladı.** `Literatür Araştırması/eklenebilecekler.md`: incelenen makaleler ve sisteme eklenebilecek fikirler (E1–E11); `makale.md`: okunacak 10 makale, öncelik sırasıyla. Makale PDF'leri git dışıdır (yayıncı lisanslı).

### 2.6 26.10.2026: yanıltıcı emirde kör nokta

- **Do ve Putniņš (2023) incelendi.** Kovuşturulmuş 25 vakayı inceleyen çalışma; tam metin birinci yazarın açık erişimli doktora tezinin 4. bölümü. Bulgusu: gerçek vakalarda sahte emirler en iyi fiyatta ya da hemen gerisinde durur. Bizim senaryomuz ise katmanları 4–6 adım geriye koyuyordu.
- **Kör nokta ölçüldü** (`rapor.md` 8). Aynı senaryo, katmanlar en iyi fiyata konarak yeniden koşuldu: bütün yöntemler rastgeleye iniyor (ROC-AUC 0,52–0,57). Aynı 9 pay-günde kurallar 0,98'den 0,55'e düşüyor. Raporlanan 0,95 yalnız derin katmanlı tür için geçerli. Kod değişikliği yapılmadı.
- **SPK vakalarında sahte emirlerin yeri ölçüldü** (`rapor.md` 9): veri tek bir yönü desteklemiyor.
  - ALKLC işlem bazlı bir vaka; emir izi yok.
  - ALKLC'deki yüksek "kısa ömürlü uzak emir payı" paya özgü: dönem sonrasında da aynı düzeyde (günlük ortanca dönemde 6,9, 19.03–30.06 arasında 7,6). Yani bu yükseklik manipülasyon dönemini ayırt etmiyor.
  - Kademe emri nitelemeli ENSRI ve VKFYO'da (B) sonuç karışık.
- Kullanıcı önerisi: senaryoda karışık katman uzaklığı ve uzaklık bandına göre raporlama. Bu öneri 29.10'daki hisseye göre ayarlı senaryonun çekirdeği oldu (2.8).

> **Akılda kalsın:** Bir yöntemin başarısı, sınandığı senaryo kadar geçerlidir. Senaryo, dedektörün aradığı izi bırakacak biçimde kurulursa sonuç parlak çıkar; gerçek manipülatör o izi bırakmayabilir.

### 2.7 26–28.10.2026: veri, tarih parametreleri ve 9 ay

**Veri.** 2024-06…2025-06 arasında gün içi emir, gün içi işlem ve gün sonu verisi eksiksiz hâle geldi. Her ay için:
1. zip'ten parquet'e dönüştürme;
2. kayıpsızlık kontrolü: parquet satır sayısı = zip içindeki CSV'nin veri satırı sayısı;
3. emirlerin günlük bölümlenmesi; gün dosyalarının toplamı = aylık dosya;
4. gün kümesinin emir, işlem ve gün sonu dosyalarında aynı olduğunun kontrolü.

İki yeni veri türü de eklendi: **gün içi endeks** (75–77 endeksin saniyelik değeri) ve **değerleme oranları** (ay sonu piyasa değeri, özsermaye, F/K, PD/DD, sektör). Kullanıcı kararı (27.10): 2025-06 da analize alınır.

**Tarih parametreleri** (`rapor.md` 10.5, 10.10, 12.2). Her yeni ay için Mart betikleri yeniden çalıştırıldı (ay başına yaklaşık 50–60 dakika). Bütün aylarda değerler Mart 2025 ile aynı çıktı:
- fiyat marjı ±%10;
- pay bazında devre kesici yalnız düşüşte, %5; tetiklemeden eşleştirmeye 899–929 saniye (yaklaşık 15 dakika);
- tek fiyat Adım 4 referansı baz fiyat; temiz müzayedelerde fiyat uyumu her ayda %99,9 ya da üstü;
- açığa satış yasak çizelgesiyle uyumlu: 2024 aylarında hiç yok; 02.01–21.03.2025 arasında yalnız aynı 50 payda; 24.03.2025'ten sonra yok.

**EBDKS eşiği** (`rapor.md` 12.3). Endekse bağlı devre kesicinin süreleri ölçülmüştü, eşiği ise endeks verisi olmadığından sınanamamıştı. Saniyelik BIST 100 değerleriyle bakıldı: 18 ayın üç gününde (05.08.2024, 19.03.2025, 21.03.2025) toplam altı tetikleme var ve altısı da endeksin önceki kapanışa göre **−%5 ve −%7**'yi ilk aştığı saniyede. Bu, eski metindeki iki eşiktir. 21.03.2025'te endeks −%6'yı aştı ama tetikleme olmadı: yürürlükteki tek %6 eşiği o tarihte geçerli değildi.

**Mart → 5 ay → 9 ay** (`rapor.md` 11). Yöntemler aynı kaldı, yalnız veri büyüdü:

| Ölçüm | Mart | 5 ay | 9 ay |
|---|---|---|---|
| SPK A, kesitsel karşılaştırma | 0,90 | 0,75 | 0,76 |
| SPK B, kesitsel karşılaştırma | 0,52 | 0,61 | 0,63 |
| Yanıltıcı emir (eski senaryo), kurallar, pencere | 0,95 | 0,91 | 0,91 |
| Denetimli model (eski senaryo, kapanış hariç), pencere | 0,85 | 0,88 | 0,92 |
| Kapanış etkileme, Z-skor, pencere | 0,78 | 0,69 | 0,65 |

- Tek ayın sonuçları iki yönde de sapmıştı. A'daki 0,90 tek bir vakadan (ALKLC) geliyordu; dört vakayla 0,75'e indi. B ise etiket sayısı arttıkça yükseldi.
- Veri büyüdükçe sürekli iyileşen tek yöntem **denetimli model**: her ayla daha çok örnek görüyor. Kurallar ve Z-skor öğrenmez; onlarda daha çok veri yalnız ölçümü daha güvenilir yapar.

> **Benzetme:** Bir öğrencinin tek sınavdaki notu şanslı ya da şanssız bir güne denk gelebilir. Beş sınavın ortalaması daha güvenilirdir, dokuz sınavınki daha da. Mart'ın 0,90'ı "şanslı sınav"dı: o ay A vakası olarak yalnız ALKLC vardı ve kesitsel karşılaştırma bu vakada çok iyi çalışıyordu.

### 2.8 29.10.2026: 13 ay ve hisseye göre ayarlı senaryo

**13 ay.** 2024-06…09'un pay-gün göstergeleri hesaplandı ve 13 ay birleştirildi (154.490 pay-gün). Pay-gün SPK değerlendirmesi: kesitsel A 0,76, B 0,64 (`rapor.md` 13.1–13.2).

**Senaryo tasarımı** (`senaryo-tasarimi.md`). Eski senaryolar sabit kalıplıydı: ör. yanıltıcı emirde her vakada katmanlar 4–6 adım geride, boy günlük işlemin belli bir oranı. Yeni tasarımda:
- senaryonun parametreleri **payın kendi önceki 5 gününden** çekilir (ör. katman boyu payın olağan büyük emirleri boyunda);
- aralıklar dedektörün eşiklerinden bağımsız seçilir (dedektörün "görebileceği" vakalar seçilmez);
- vakalar uzaklık, ömür, katman sayısı gibi eksenlerde bantlara eşit dağıtılır ve sonuç bant bant raporlanır (**kör nokta haritası**);
- sahte katman işlem görmeye başlarsa, işlem görmeden hemen önce iptal edilip yeniden girilir (**planlı iptal**).

Öğrenen bir üretici model (SPK vakalarından "manipülasyon üretmeyi öğrenen" model) değerlendirildi ve reddedildi: etiketli pay sayısı az, emir düzeyinde etiket yok ve üretici, dedektörün gördüğünü öğrenir. Kullanıcı kararı (29.10): ayarlı senaryo uygulanır; eskisi silinmez, iki sürüm yan yana koşulur.

**Sonuç: 13 ayda eski ve ayarlı senaryo yan yana** (`rapor.md` 13.5; pencere düzeyi ROC-AUC):

| Senaryo | Kurallar, eski | Kurallar, ayarlı | Denetimli, eski | Denetimli, ayarlı |
|---|---|---|---|---|
| Yanıltıcı emir | 0,90 | 0,59 | 0,94 | 0,68 |
| Fiyat yükseltme | 0,55 | 0,77 | 0,81 | 0,90 |
| Karşılıklı işlem | 0,48 | 0,44 | 0,95 | 0,74 |
| Kapanış etkileme (Z-skor) | 0,66 | 0,71 | — | — |

- **Yanıltıcı emirde eski başarı iyimserdi.** Kayıp, dedektörün eşiklerinin dışına düşen vakalardan geliyor:
  - ömrü 60 saniyeyi aşan sahte emirler: kurallar 0,46–0,50, yani rastgele;
  - tek katman: 0,49;
  - en iyi fiyata yakın katmanlar: 0,53–0,57.
- **Fiyat yükseltmede ilişki ters.** Eski senaryo fiyatı neredeyse hiç itmiyordu; fiyatı gerçekten iten ayarlı senaryo daha iyi yakalanıyor (kurallar 0,55 → 0,77). Eski "fiyat yükseltme zayıf yakalanıyor" sonucu senaryonun etkisizliğinden geliyordu.
- **Karşılıklı işlemin eski başarısı boyun göze batmasından geliyordu.** Payın olağan işlem boyunda yapılan karşılıklı işlem bu veride görülemez: üye ya da hesap bilgisi yok.
- **Okuma notu:** ayarlı senaryoda olaylar birçok pencereye yayılır; "ilk 3 isabeti" şans eseri de tutar. Bu yüzden ayarlıda ilk 3, kontrol ilk 3 ile birlikte okunur; senaryolar arası karşılaştırmada ROC-AUC esas alınır.

> **Benzetme:** Bir hırsız alarmını, her seferinde aynı kapıdan, aynı saatte, aynı ayakkabıyla giren bir deneme hırsızıyla sınarsan alarm "kusursuz" görünür. Gerçek hırsız pencereden girer. Ayarlı senaryo deneme hırsızını her seferinde başka yerden sokar ve hangi girişlerin alarmı çaldırmadığını tek tek yazar: kör nokta haritası budur.

### 2.9 29.10.2026 akşamı: 18 ay ve SPK etiketleriyle denetimli model

**Veri 2024-01…05 eklendi** (kullanıcı isteği). Gün sonu, gün içi endeks ve değerleme 2024-01…04; işlem ve emir 2024-01…05. 27 adımın hepsi doğrulandı (kayıpsızlık, CSV satır sayısı birebir, gün kümesi gün sonuyla aynı); hata 0. 18 ay birleştirildi: **211.698 pay-gün, 371 işlem günü** (2024-01-02…2025-06-30).

**SPK etiketleri 18 ayda:** A 93 pay-gün (4 pay: KRGYO, TDGYO, ALKLC, EUREN), B 582 pay-gün (31 pay); toplam 34 pay (KRGYO iki seviyede de var). 2024-01…05, 9 B payı ekledi; 7'si yalnız bu aylarda.

**SPK denetimli model** (`tespit/spk_denetimli.py`, `rapor.md` 14.3). Şimdiye kadarki denetimli model sentetik vakalarla eğitiliyordu. Bu model doğrudan SPK etiketleriyle eğitilir:
- **Örnek:** pay-gün. **Hedef:** o pay-gün SPK A ya da B etiketli mi?
- **Girdiler (80):** göstergelerin ham değerleri, payın kendi geçmişine göre z'leri, aynı gün aynı pazardaki paylar içindeki sıraları, 5 günlük getiri ve hacim artışı, endeks göstergeleri.
- **Bilerek verilmeyenler:** pazar, sektör, piyasa değeri, fiyat ve hacim düzeyi, brüt takas (tedbir etiketle birlikte gelir, sızıntı olur).
- **Doğrulama:** paya göre gruplu 5 katlı çapraz doğrulama. Her pay-günün puanı, **o payı hiç görmemiş** bir modelden gelir.

| Puan | A+B | A | B |
|---|---|---|---|
| SPK denetimli model | **0,71** | **0,84** | **0,69** |
| Kesitsel karşılaştırma (Isolation Forest) | 0,67 | 0,74 | 0,65 |
| Isolation Forest (payın geçmişine göre) | 0,59 | 0,50 | 0,61 |
| Z-skor | 0,58 | 0,47 | 0,60 |
| İktisadi kurallar | 0,57 | 0,48 | 0,58 |

- **En iyi pay-gün yöntemi bu model.** En üstteki %1'de etiketli pay-gün oranı %1,7; taban oran %0,32, yani beş katı. Mutlak düzey yine düşük: en şüpheli 2.111 pay-günün 36'sı etiketli.
- **A'da 13 aydan 18 aya büyük artış (0,68 → 0,84).** A pozitifleri aynı; değişen, modelin öğrendiği B paylarının 24'ten 31'e çıkması. Az etiketle çalışan modelde her yeni vakanın değeri büyük.
- **Endeks göstergeleri katkı vermedi** (fazla getiri: payın getirisi eksi piyasa ya da sektör endeksi getirisi). Kesitsel sıralar aynı gün aynı pazardaki paylarla kıyasladığı için piyasa hareketini zaten büyük ölçüde gideriyor.
- **Sınırlar:** 34 pozitif pay; B etiketi "tedbirden önceki 20 iş günü" varsayımıdır; etiketsiz günlerin bir kısmı yakalanmamış manipülasyon olabilir. Model aynı dönemin **başka paylarına** genellemeyi ölçüyor; **zamanda ileriye** genelleme sınanmadı (3.2).

> **Örnek: neden paya göre gruplu doğrulama?** ALKLC'nin 12 manipülasyon gününden 6'sıyla eğitip diğer 6'sıyla sınadığını düşün. Model "manipülasyon nedir"i değil "ALKLC neye benzer"i öğrenir ve sınavı ezberle geçer. Paya göre gruplamada ALKLC'nin bütün günleri ya eğitimde ya sınavdadır; model ALKLC'yi hiç görmeden puanlamak zorundadır. Gerçek hayatta da yeni vaka, modelin hiç görmediği bir payda olacaktır.

### 2.10 30.10.2026: 2024 başı parametreleri ve 18 ay motorlu değerlendirmeler

**Tarih parametreleri 2024-01…05** (`rapor.md` 15). İki pencerede, yaklaşık 2 saatte ölçüldü. Bütün değerler sonraki aylarla aynı. `motor/parametreler.py`'deki veri dönemi (`VERI_DONEMI`) 2024-01-01…2025-06-30 oldu; motor artık 18 ayın her gününde çalışır. Motorla sınama:
- ISYAT.E 05.02.2024 (bir SPK B vakasının dönemi): 5.727 işlemin tamamı birebir;
- THYAO.E 15.03.2024: 103.540 işlemin %99,89'u birebir (fark, görünen kısmı veride yazılmayan kısmi görünmeli emirlerden; Mart 2025'te de aynı).

**18 ay motorlu değerlendirmeler** (`rapor.md` 16). Ayarlı senaryo 1.660 seçim (ay başına 13 aydaki kadar; kullanıcı kararı), eski senaryo 720 seçim, SPK pencere 1.275 pay-gün; yaklaşık 3,5 saat, hata yok.

| Senaryo (ayarlı, pencere düzeyi) | Kurallar 13 ay | Kurallar 18 ay | Denetimli 13 ay | Denetimli 18 ay |
|---|---|---|---|---|
| Yanıltıcı emir | 0,59 | 0,57 | 0,68 | 0,68 |
| Fiyat yükseltme | 0,77 | 0,78 | 0,90 | 0,89 |
| Karşılıklı işlem | 0,44 | 0,45 | 0,74 | 0,73 |
| Kapanış etkileme (Z-skor) | 0,71 | 0,67 | — | — |

- **18 ay, 13 ayı doğruluyor.** Bant başına vaka 130–147'den 190–203'e çıktı; değerler 0,01–0,02 içinde kaldı.
- **Yanıltıcı emir kör noktaları kesinleşti:** ömrü 60 saniyeyi aşan emirlerde kurallar 0,46; en iyi fiyattaki katmanlarda 0,51; tek katmanda 0,50. Denetimli model aynı bantlarda 0,59–0,63.
- **Eski senaryo, pay-gün düzeyi:** enjeksiyonsuz kontrol 0,49–0,50. Yani motorla yeniden üretilen gün ile gerçek gün arasındaki küçük fark yapay bir ayrım üretmiyor.
- **Gerçek SPK vakalarında 5 dakikalık uyarılar zayıf** (A 0,61–0,65, B 0,54). Gerçek vakalar için en iyi araç pay-gün düzeyindeki SPK denetimli modeldir.

**Belgeler ve kayıt.** Verinin kısa özeti `VERI.md` yazıldı. 26–30.10 arasındaki bütün kod, belge ve ölçüm çıktıları git'e kaydedildi (commit). `ANLATIM.pdf`, `TASARIM.pdf`, `DURUM.pdf` ve `VERI.pdf` de kaynaklarıyla (`pdf-kaynak/`) birlikte eklendi.

## 3. Yapılacaklar (öncelik sırasıyla)

25.10'daki listenin ilk üç işi bir zincirdi ve üçü de bitti:

```
Biten zincir:
[1] Veri indir ve hazırla            tamam: 18 ay (2024-01…2025-06)
[2] Tarih parametrelerini ölç        tamam: 18 ay, hepsi aynı
[3] Çok ay ölçeğinde çalıştır        tamam: 18 ay (rapor.md 13–16)

Sıradaki işler:
[1] 60 sn eşiğini veriye göre gözden geçir   (önce ömür dağılımı ölçümü)
[2] Zamanda ileriye genelleme
[3] Vize raporu (ve eski öneri formuna dayanan yerlerin düzeltilmesi)
[4] Kural dosyalarının onayı (veriyle birlikte)
[5] Tespit eklemeleri (isteğe bağlı; şimdilik yapılmıyor)
[6] Özsermaye günleri için düzeltilmiş baz fiyat
```

### 3.1 60 saniye eşiğinin veriye göre gözden geçirilmesi

- **Ne:** Yanıltıcı emrin ana göstergesi "kısa ömürlü uzak emir payı"dır: en iyi fiyattan en az 3 adım uzakta girilip **60 saniye içinde** işlem görmeden iptal edilen emirlerin payı. Ayarlı senaryoda ömrü 60 saniyeyi aşan sahte emirler bu tanıma girmiyor ve hiç yakalanmıyor (kurallar 0,46).
- **Neden dikkatli olunmalı:** Eşiği senaryoya bakarak büyütmek kolaydır ama hiledir: senaryo zaten bizim seçtiğimiz aralıklardan gelir. Eşik veriye göre seçilmelidir.
- **Sıra (kullanıcıyla konuşuldu, 29.10):**
  1. gerçek veride büyük, uzak, işlem görmeden iptal edilen emirlerin ömür dağılımının ölçülmesi (normal piyasada ve emir bazlı SPK vakalarında);
  2. ardından kademeli bir gösterge;
  3. kabul ölçütü: yanlış alarm ve SPK vakalarındaki başarı.

> **Benzetme:** Hız radarının eşiği. Eşiği yalnız yakalamak istediğin araca göre ayarlarsan normal sürücüleri de cezalandırırsın. Önce yoldaki olağan hız dağılımına bakılır, sonra eşik "olağanın dışı"na konur.

### 3.2 Zamanda ileriye genelleme

- **Ne:** SPK denetimli model şu an "aynı dönemin başka paylarına" genellemeyi ölçüyor. Geçmişte eğitilip gelecekteki vakalarda sınanması yapılmadı.
- **Neden:** Gerçek kullanımda model geçmiş vakalarla eğitilir ve sonraki aylarda çalışır. Manipülasyon biçimleri ve piyasa koşulları zamanla değişebilir; aynı dönemde ölçülen başarı geleceğe taşınmayabilir.

### 3.3 Vize raporu

- **Ne:**
  - literatür bölümü (`Literatür Araştırması/eklenebilecekler.md` ve `makale.md`);
  - öneri formu ile sistem arasındaki farklar, **doğru forma göre** (`ANLATIM.md` 2.4);
  - `rapor.md` bölümlerinin vize metnine dönüştürülmesi.
- **Önce:** eski (yanlış) forma dayanan yerlerin düzeltilmesi: `CLAUDE.md` "Sistem kapsamı" kararı, `TASARIM.md` 1 / 6.3 / 6.5, `rapor.md` 3.2–3.3, `DURUM.md` "Öneri formu" bölümü (bölüm 9).

### 3.4 Kural dosyalarının kullanıcı onayı

05 (emirler), 06 (devre kesici) ve 08 (pazarlar, tedbirler) kullanıcı doğrulaması bekliyor. Onay veriyle birlikte yapılacak: kuralın veride gerçekten öyle işlediği görülerek.

### 3.5 Tespit eklemeleri (isteğe bağlı)

- Literatürden çıkan fikirler `eklenebilecekler.md`'de E1–E11 olarak not edildi. E10 (iptal edip yeniden giren, döngüsel yanıltıcı emir) ve E11'in (karışık katman uzaklığı, bant bazında raporlama) fikri ayarlı senaryoyla uygulandı; diğerleri yalnız not.
- Kullanıcı kararı (25–26.10): eklemeler şimdilik uygulanmıyor; önce sistemin bütünüyle anlaşılması.
- Ayrıca: defter göstergelerinin daha derin seviyelerle ve olay anında örneklenmesi.

### 3.6 Özsermaye günleri

Bedelsiz ve temettü günlerinde baz fiyat "teorik fiyat"a düzeltilir. Gün sonu dosyasındaki önceki kapanış düzeltilmemiş olduğundan motor bu günlerde doğru taban/tavanı bilemez. Düzeltilmiş baz fiyat için bir kaynak gerekiyor; o zamana kadar bu günler dışarıda.

## 4. Çalıştırma notları: komutlar tek tek

Bütün komutlar proje klasöründe (`D:\Bitirme\proje`) çalıştırılır. `python -I`, Python'u "yalıtılmış modda" çalıştırır: çalışma klasöründeki rastgele bir dosyanın modül diye yüklenmesini ve ortam değişkenlerinin etkisini önler.

**Tek bir pay-günü oynatmak (doğrulama):**

```
python -I motor/tekrar_oynat.py  veri/gun-ici-emir/gunluk
                                 veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet
                                 GUN  KOD
                                 --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet
                                 [--cikti KLASOR]
```

| Argüman | Anlamı | Örnek |
|---|---|---|
| `veri/gun-ici-emir/gunluk` | Günlük bölümlenmiş emir dosyaları | — |
| `PP_GUNICIISLEM…parquet` | O ayın işlem dosyası (karşılaştırma için) | Mart 2025 |
| `GUN` | Oynatılacak gün | `2025-03-03` |
| `KOD` | İşlem sırası | `THYAO.E` |
| `--gunsonu` | O ayın gün sonu dosyası (baz fiyat, pazar) | — |
| `--cikti` | İsteğe bağlı: sonuçların yazılacağı klasör | — |

Çıktı: bölüm bölüm ve bütün gün için "gerçek işlemlerin yüzde kaçı birebir üretildi".

**Bir günün bütün payları:** `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv` (yaklaşık 17 dakika). `GUNLUK`, `ISLEM`, `GUNSONU` yukarıdaki üç veri yoludur; `CIKTI.csv` her sıranın sonucunu yazar.

**Enjeksiyon:** `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]`. Örneğin bir payda saat 14:00:00'da yanıltıcı emir senaryosu; `ad=deger` ile senaryo parametreleri (miktar, katman sayısı, süre…) değiştirilir.

**Pay-gün göstergeleri:**
- Bir ay: `python -I tespit/ozellikler.py GUNLUK ISLEM GUNSONU CIKTI.parquet [GUN ...]`. Gün verilmezse gün sonu dosyasının ayı hesaplanır; gün listesiyle parça parça da çalıştırılabilir. Yalnız kapanış göstergelerini eklemek için `tespit/kapanis_ozellikleri.py`.
- Çok ay: her ay ayrı hesaplanır, sonra `python -I tespit/ozellik_birlestir.py BIRLESIK.parquet AY1.parquet AY2.parquet ...` ile birleştirilir. Değerlendirmeler birleşik dosyayla yapılır.
- Endeks göstergeleri: `python -I tespit/endeks_ozellikleri.py OZELLIKLER.parquet` (sütun ekler).

**Değerlendirmeler:**

| Betik | Ne ölçer | Ayar |
|---|---|---|
| `tespit/degerlendir.py` | SPK etiketleriyle eğitimsiz yöntemlerin pay-gün ölçütleri | — |
| `tespit/spk_denetimli.py` | SPK etiketleriyle eğitilen pay-gün modeli | `OZELLIKLER.parquet veri/etiketler/vaka.csv CIKTI` |
| `tespit/pencere_degerlendir.py` | Sentetik enjeksiyonla 5 dk pencere ölçütleri | `SENARYO_SURUM=yeni`: ayarlı senaryo; `SENARYOLAR`: senaryo listesi; `OLCEK`: büyüklük; `PENCERE_DK`: pencere uzunluğu |
| `tespit/denetimli.py` | Sentetik etiketlerle denetimli model | `GRUP=pay`: paya göre gruplu doğrulama |
| `tespit/kor_nokta.py` | Ayarlı senaryonun bant bant raporu | `PENCERE_KLASORU` |
| `tespit/spk_pencere.py` | SPK günlerinde pencere düzeyi | Kaldığı yerden devam eder; `--degerlendir` ile ölçüm |

**Tarih parametresi ölçümü:** `veri/araclar/gunici_*` betikleri ay ile çalışır (ör. `gunici_seans_akis_kontrol.py ... AY`). Enjeksiyon adayları verinin 6. işlem gününden başlar (Z-skor için 5 günlük geçmiş gerekir).

**Arayüz:** `streamlit run arayuz/uygulama.py` (tarayıcıda sayfa açılır).

**Testler:** `python -m pytest motor/testler tespit/testler` (41 test).

## 5. Klasör düzeni

| Klasör / dosya | İçinde ne var | Git'te mi? |
|---|---|---|
| `kaynaklar/` | Ham PDF'ler (Prosedür, SPK bültenleri); `_kullanilmayan/` kullanılmayacak belgeler | Hayır |
| `ekler/` | Prosedür Ek-1…Ek-21 (kullanıcı doğrulamalı) | Evet |
| `kurallar/` | 8 kural dosyası | Evet |
| `veri/` | Çeviriler, DataStore biçim belgesi, doğrulama ve ölçüm çıktıları (`gunici-dogrulama/`), betikler (`araclar/`), etiketler | Evet |
| `veri/gun-ici-emir/`, `gun-ici-islem/`, `gun-sonu-fiyat-hacim/`, `gun-ici-endeks/`, `degerleme-orani/`, `itch/` | Büyük veri | Hayır |
| `motor/`, `tespit/`, `arayuz/` | Kod | Evet |
| `TASARIM.md` | Sistem tasarımı (sürüm 2) | Evet |
| `rapor.md` | Çalışma raporu (vize raporunun kaynağı) | Evet |
| `ANLATIM.md`, `VERI.md`, `senaryo-tasarimi.md` | Sistemin anlatımı, verinin özeti, ayarlı senaryo tasarımı | Evet |
| `Literatür Araştırması/` | Literatür notları (`eklenebilecekler.md`, `makale.md`); makale PDF'leri | Notlar evet, PDF'ler hayır |
| `pdf-kaynak/` | PDF'lerin kaynakları ve üretim betiği | Evet |

Aylık emir parquet dosyaları ve indirilen zip'ler harici diskte (F:) durur; D: üzerinde emirlerin yalnız günlük bölümleri vardır.

> **Neden büyük veri git dışında?** Git, kodun ve belgelerin sürümlerini tutar. Yüzlerce GB'lık veri git'e konamaz; ayrıca lisanslı veridir, paylaşılmamalıdır.

## 6. Kural dosyalarının durumu

Kural dosyaları, Borsa İstanbul Pay Piyasası Prosedürü'nden çıkarılmış, madde numaralı kurallardır. Motor bunlara göre yazılır. Sekizinin de ilk sürümü yazıldı.

| Dosya | Konusu (sade) | Ne yapıldı | Ne açık |
|---|---|---|---|
| `01-seanslar` | Günün saat çizelgesi, bölümler, geçici durdurma | Mart 2025'te bölüm adları ve saatleri Ek-10 ile uyumlu; gün sonu 18:19; müzayede başlangıcı her aşamada ortak rastlantısal bir saniye; varant akışındaki 07.03.2025 değişikliği görüldü | Bazı durum adlarının (`2`, EIY, PY, APY) hangi tarihten beri geçerli olduğu |
| `02-fiyat` | Lot, fiyat adımı, baz fiyat, taban/tavan, AOF | Marj 18 ayın hepsinde bütün pazarlarda ±%10 (tarih parametresi); içe yuvarlama doğrulandı; fiyat adımı Tablo-7/8 ile sınandı | Marjın yazılı dayanağı (duyuru metni yok) |
| `03-tek-fiyat` | Müzayede (açılış, kapanış) denge fiyatı algoritması — **en kritik dosya** | Mart 2025'te 29.633 müzayedenin %99,96'sında fiyat tutuyor (diğer aylarda temiz müzayedelerde %99,9 ya da üstü); Adım 4 referansı = baz fiyat; kapanışta son işlem ±%3; dengeleyici emir eşleşmesi | Karışık yön, Adım 4 eşit uzaklık ve Adım 5 (veride hiç oluşmadı), kotasyonların müzayedeye katılımı |
| `04-surekli-islem` | Sürekli işlemde fiyat-zaman önceliği, değişiklikte öncelik | Fiyat önceliği %99,998, zaman önceliği %99,76 uyum (ITCH 2018 ve Mart 2025); `emir_giris_zamani` öncelik zamanı değil; marj dışı iptal/duraklatma kararı verildi | 14 açık soru (ayrıntı dosyada) |
| `05-emirler` | Emir tipleri, değiştirme/iptal, hangi bölümde hangi emre izin var (Ek-19) | 143 madde; Ek-19 matrisi betikle üretildi; belgeler arası çelişkiler karara bağlandı; Mart 2025'te Ek-19'a aykırı yeni emir 0; piyasa emri fiilen yalnız KİE | **Kullanıcı doğrulaması**; Ek-18 bazı örneklerinde tablo/metin tutarsızlığı |
| `06-devre-kesici` | Pay bazında devre kesici ve EBDKS | 53 madde; Tablo-4 sayfa görüntüsüyle doğrulandı; 18 ayın hepsinde DK yalnız düşüşte %5, yaklaşık 15 dk; EBDKS eşiği gün içi endeksle doğrulandı (eski metin: −%5 ve −%7; 28.10.2026) | **Kullanıcı doğrulaması**; marj mı tetikleme oranı mı |
| `07-itch` | ITCH mesaj kuralları | 2018 örnek veriyle doğrulama sonuçları işlendi | 4 açık soru (ayrıntı dosyada) |
| `08-pazarlar-tedbirler` | Pazarlar, piyasa yapıcılık, brüt takas, bülten | 55 madde; Tablo-3 ve Tablo-4 sayfa görüntüleriyle doğrulandı; pazar kodları eşlendi (T = Alt Pazar) | **Kullanıcı doğrulaması**; Tablo-4 marj ve DK satırları veriye uymuyor |

**Açık soru sayıları** (30.10.2026 sayımı; `[DOĞRULA]` ile başlayan satırlar; `DURUM.md`'deki 21.10.2026 sayımından tek fark 04'te bir soru fazlası):

| 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | Toplam |
|---|---|---|---|---|---|---|---|---|
| 13 | 12 | 21 | 14 | 27 | 22 | 4 | 15 | 128 |

> **Bir kararın evrimi: devre kesicide eşleştirme anı.** `DURUM.md`'deki `06-devre-kesici` satırında "DK eşleştirmesi sabit saatte" kararı ve "Mart 2025'te eşleştirme rastlantısal (sabit saat kararıyla çelişir, yeni `[DOĞRULA]`)" notu birlikte durur. Sıra şöyledir: önce metne bakılarak "sabit saat" kararı verildi; sonra Mart 2025 verisinde eşleşmenin bölümün ilk 30 saniyesinde rastlantısal olduğu görüldü; 21.10.2026'da kullanıcı kararıyla kural "sabit emir toplama süresi + tarihe bağlı rastlantısal pencere" oldu (Mart 2025: 30 sn, 2018: 0 sn). Geçerli olan sonuncusudur.

**"Kullanıcı doğrulaması bekliyor" ne demek?** Dosyayı Claude kaynaktan çıkardı, ama kullanıcı henüz satır satır okuyup "doğru" demedi. Onay veriyle birlikte yapılacak: bir kural okunurken verideki karşılığına da bakılacak.

## 7. DataStore verisi ve sistem tasarımı

### 7.1 Veri kararı (21.10.2026)

**Karar (kullanıcı):** ITCH yalnız örnektir; ana veri DataStore gün içi emir, gün içi işlem ve gün sonu fiyat-hacim dosyalarıdır (aylık parquet).

**Neden?** ITCH, müzayede sırasında gelen emirleri tek tek yayımlamaz. Açılış ve kapanış müzayedelerinin defteri yalnız DataStore verisiyle kurulabilir. Kapanış manipülasyonu tam da orada olduğu için bu belirleyicidir. (Ayrıntı: `TASARIM.pdf` bölüm 2.)

### 7.2 Elimizde ne var (30.10.2026)

| Veri | Dönem | Biçim | Not |
|---|---|---|---|
| Gün içi emir | 2024-01…2025-06 | Günlük bölümler (D:); aylık parquet ve zip'ler harici diskte (F:) | 371 gün; ayda 0,7–1,1 milyar satır |
| Gün içi işlem | 2024-01…2025-06 | Aylık parquet | Ayda 0,17–0,35 milyar satır (her işlem alış ve satış için iki satır); aralık dışı 2025-07…09 da diskte |
| Gün sonu fiyat-hacim | 2024-01…2025-06 | Aylık parquet, bütün aylar tek sabit şemada | Baz fiyat, pazar, işlem yöntemi, günlük özetler |
| Gün içi endeks | 2024-01…2025-06 | Aylık parquet | 75–77 endeks, saniyelik |
| Değerleme oranları | 2024-01…2025-06 | Aylık parquet | Ay sonu, pay bazında; sektör bilgisi |
| ITCH | Yalnız 08.10.2018 | Metin ve ikili dosya | 2025-01/02 örneği henüz indirilmedi |

**Doğrulamalar:**
- Alanların anlamına kadar inen ayrıntılı doğrulama yalnız Mart 2025 ile yapıldı: rapor `veri/gunici-veri-dogrulama.md` (13 bölüm), çıktılar `veri/gunici-dogrulama/2025-03/`.
- Diğer bütün aylarda: kayıpsızlık kontrolü (satır sayıları CSV ile birebir, gün kümeleri dosyalar arasında aynı) ve tarih parametresi ölçümü (`veri/gunici-dogrulama/YYYY-MM/`). Ayrıntı `veri/README.md` ve `VERI.md`.

### 7.3 Tasarımın özü (21.10.2026)

`TASARIM.md` bu tarihte sürüm 2 olarak yazıldı:
- veri katmanı;
- tarih parametreleri (marj ±%10; DK yalnız düşüşte %5 / 15 dk; EBDKS eski kurallarla 20/30 dk ve iki eşik; açığa satış 24.03.2025'ten itibaren yasak). 28.10'da EBDKS eşiği de endeks verisiyle doğrulandı; 30.10'da bütün değerlerin 18 ayın hepsinde geçerli olduğu ölçüldü;
- motorun iki modu (tekrar oynatma ve enjeksiyon);
- tespit birimi pay-pencere (veride üye/hesap kimliği yok).

### 7.4 Kullanıcı kararları, tek tek

1. **Devre kesicide eşleştirme anı (21.10).**
   - *Karar:* Sabit emir toplama süresi + tarihe bağlı rastlantısal pencere (Mart 2025: 30 sn, 2018: 0 sn).
   - *Neden:* Veride eşleşme sabit saatte değil, bölümün ilk 30 saniyesinde rastlantısal. 2018 ITCH verisinde ise sabit. Yani kural zamanla değişmiş; tarih parametresi olarak tutulmalı.
2. **Tablo-4 ile veri farkı (21.10).**
   - *Karar:* Verideki fiili eşikler kullanılır. Fark, "Prosedür Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayıtlıdır. Değerler `motor/tarih_parametreleri.csv`'dedir.
   - *Neden:* Motorun amacı o günkü piyasayı taklit etmektir. Metin ±%20 dese de o gün ±%10 uygulandıysa, ±%10 kullanılmalıdır.
3. **Karışık yönlü tek fiyat (21.10).**
   - *Durum:* Müzayede algoritmasının 3. adımı "kalan miktar alış yönündeyse en yüksek adayı, satış yönündeyse en düşüğü seç" der. Ama aday fiyatların bir kısmında kalan alış, bir kısmında satış yönündeyse ne olacağı yazılı değil.
   - *Karar:* Referansa (baz fiyat) / son işlem fiyatına en yakın aday; eşitlikte orta nokta.
   - *Veri:* Mart 2025'te 4 vaka var; 2'si kurala uyar, 2'si (ZPBDL.F, ZRE20.F) istisnadır ve `yon_karisik_istisna = 1` ile işaretlidir. Diğer aylarda da ayda 0–5 vaka, uyan ve istisna karışık.
4. **ITCH ayları (21.10).** ITCH örneği önce 2025-03/04 seçildi, aynı gün **2025-01/02** ile değiştirildi (A vakaları KRGYO, TDGYO, ALKLC bu aylarda). "2025-07 alınmaz" yalnız ITCH içindir.
5. **Veri kapsamı (22.10).** DataStore gün içi emir, işlem ve gün sonu verisi 2024-06…2025-05 arası alınır (12 ay; gerekirse genişletilir). Bu aralık 12.10.2026 planından gelir (o gün ITCH ve gün sonu için seçilmişti); DataStore ana veri olunca bu dosyalara aktarıldı.
6. **2025-06 analize alınır (27.10).** Veri dönemi 2025-06-30'a uzatıldı.
7. **2024-01…05 eklenir (29.10).** Veri dönemi 2024-01-01…2025-06-30 oldu (18 ay).
8. **Hisseye göre ayarlı senaryo uygulanır (29.10).** Eski senaryo silinmez; iki sürüm yan yana koşulur. 18 ayda ayarlı senaryonun seçim sayısı ay başına 13 aydaki kadar tutuldu (30.10).

> **Akılda kalsın:** Veri kapsamı iki kez genişledi: önce sona doğru (2025-06), sonra başa doğru (2024-01…05). Her genişlemede aynı sıra izlendi: dönüştür, kayıpsızlığı kontrol et, tarih parametrelerini ölç, ancak ondan sonra motoru çalıştır.

### 7.5 Bekleyenler ve disk

- ITCH 2025-01/02 (çapraz doğrulama için) henüz indirilmedi.
- Aralık dışı indirilen dosyaların (ör. işlem 2025-07…09) silinmesi kullanıcıya bırakıldı.
- Disk: aylık emir dosyaları ve zip'ler harici diske (F:) taşındı. Günlük bölümleme bittikten sonra aylık emir dosyası artık gerekli değildir; motor ve doğrulamalar günlük bölümleri okur.

> **Örnek: bir ay ne kadar yer tutar?** Emir dosyası zip olarak ≈ 20 GB, açılmış CSV olarak ≈ 209 GB, parquet olarak 15–21 GB; günlük bölümler aylık dosyanın ≈ 0,82 katı yer tutar. Bölme sırasında en yüksek ek disk kullanımı aylık dosyanın 1,9 katı ölçüldü. 18 ayın hem aylık hem günlük hâli D:'ye sığmazdı; bu yüzden aylık dosyalar dışarı taşındı.

## 8. Motor, arayüz ve tespit (22.10.2026 kaydı)

Bu bölüm `DURUM.md`'de 22.10.2026'nın kaydıdır; sistemin ilk sürümünün ne olduğunu anlatır. Buradaki sayılar Mart 2025 iledir; 18 aylık sonuçlar bölüm 2.7–2.10'dadır.

**Motor (`motor/`):**
- sürekli işlem; açılış, kapanış, devre kesici ve EBDKS müzayedeleri; kapanış fiyatından işlemler; pay bazında devre kesici eşiği;
- sentetik emir doğrulama (Ek-19, fiyat adımı, marj, kapanış kuralları) ve enjeksiyon (`senaryolar.py`, `enjeksiyon.py`);
- bütün paylar, bir gün: 03.03.2025'te 4.915.057 işlemin %99,85'i birebir; bir gün ≈ 17 dakika. Sonuçlar `veri/gunici-dogrulama/2025-03/motor/`.

**Motorla ilgili iki tasarım notu:**
- **Seans durum makinesi gerekmedi.** Tekrar oynatmada bölüm geçiş saatleri veriden okunduğu için ayrı bir "saat makinesi"ne gerek kalmadı. (`DURUM.md` bunu "ajan tabanlı simülasyon çıkarıldığı için" diye yazar; ajan simülasyonu doğru öneri formunda zaten yoktur, bölüm 9.)
- **Kotasyon ve orta nokta emirleri öncelikli değil;** kapsam dışı (özel işlem bildirimi de).

**Emir bilgisi kararı (madde 24, 22.10.2026).** Emrin bilgi alanları (MPF, AFK, hesap no) Prosedür'e göre değiştirilemez.
- *Sentetik emirlerde:* bu alanları değiştiren bir değişiklik reddedilir.
- *Tekrar oynatmada:* veride AFK alanı dolu bir emirde, fiyatı ve kalanı değişmeyen bir değişiklik bile önceliği kaybettiriyor; motor bunu böyle uygular.

**Arayüz:** `streamlit run arayuz/uygulama.py`. Uyarılar 5 dakikalık pencere kurallarıdır; SPK etiketli günlerde seviye ve bülten gösterilir.

**Tespit (`tespit/`), Mart 2025 ile:**
- pay-gün göstergeleri, Z-skor, VI-104.1 bent kuralları, Isolation Forest, kesitsel karşılaştırma;
- yeni göstergeler: kısa ömürlü uzak emir payı ve makas (veriden ve motordan);
- SPK, Mart 2025: A (ALKLC) kesitsel ROC-AUC 0,90, B 0,53 (18 ayda 0,74 ve 0,65; 2.9);
- sentetik, 5 dk pencere (eski senaryo): yanıltıcı emir kurallarla 0,95; karşılıklı işlem denetimli modelle 0,90; kapanış ×1'de 0,77;
- `ozellikler.parquet` gün başına ara dosyalarla tutulur (`ozellikler_gunluk/`), iş yarıda kalırsa kaldığı yerden devam eder.

## 9. Öneri formu ve veri talebi

> **Dikkat: `DURUM.md`'nin bu bölümü yanlış formu anlatır.** `DURUM.md`'deki "Öneri formu" bölümü 22.10'da `.docx` dosyasından yazıldı; o form yanlıştı (başlığı "Ajan Tabanlı Yapay Borsa Simülasyonu…"). Doğru form proje kökündeki PDF'tir (25.10.2026). Aşağıda doğru form anlatılır. Eski formdaki yatırımcı ajanları, GA/PSO kalibrasyonu, Monte Carlo bandı ve sanal-reel paralel çalışma doğru formda **yoktur**; bunlar için yazılan "yapılmaz" kararları ve farklar artık geçersizdir.

### 9.1 Doğru öneri formu ve sistemdeki karşılığı

Bölüme verilen öneri formunun (danışman Doç. Dr. Ersin Kaya) başlığı projenin başlığıyla aynıdır: "Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi". Form 12 adım, iki yarıyılın hedefleri ve Eylül–Mayıs iş-zaman çizelgesi verir. Sistem bu planın uygulamasıdır.

| Formdaki adım | Durum (30.10.2026) |
|---|---|
| 1. Literatür taraması ve gereksinim analizi | Kısmen: Prosedür kuralları `kurallar/`'da; literatür çalışması başladı (2.5) |
| 2. Veri temini: DataStore'dan ITCH ve gün sonu; KAP bildirim zamanları; SPK etiketleri | Ana veri DataStore gün içi verisi (18 ay); SPK etiketleri hazır; KAP bildirimleri derlenmedi |
| 3. ITCH çözümleyici ve defter, örnek veriyle doğrulama | Yapıldı (08.10.2018 örneği); defterin ana kaynağı DataStore emir olayları |
| 4. Eşleştirme motoru, Prosedür örnekleriyle test | Yapıldı; devre kesici, EBDKS ve tarih parametreleri de var |
| 5. Tekrar oynatma ve motorun gerçek veriyle doğrulanması | Yapıldı: işlem işlem karşılaştırma, %99,85 (Mart 2025), 2024 sınamaları |
| 6. Özellik çıkarımı | Yapıldı (pay-gün ve 5 dk pencere); KAP özelliği yok |
| 7. İktisadi kural tabanlı tespit | Yapıldı (VI-104.1 bentleri) |
| 8. Denetimsiz öğrenme (Isolation Forest, otokodlayıcı vb.) | Isolation Forest yapıldı; otokodlayıcı yok |
| 9. Enjeksiyonla etiketli veri | Yapıldı; iki senaryo sürümü (eski ve ayarlı) |
| 10. Denetimli öğrenme (XGBoost vb.) | Yapıldı: sentetik etiketlerle (pencere) ve SPK etiketleriyle (pay-gün, A+B 0,71) |
| 11. Birleştirme ve değerlendirme (uyarı seviyeleri, KAP ayıklaması, SPK ve vaka olmayan dönemler, uyuşmazlıklar) | Kısmen: yöntemler ayrı ayrı ölçüldü; birleşik uyarı seviyesi, KAP ayıklaması ve uyuşmazlık incelemesi yok |
| 12. Arayüz ve raporlama | Kısmen: arayüz var; emir defteri görünümü yok; vize raporu hazırlanıyor |

### 9.2 Formdan farklar

- **Ana veri ITCH yerine DataStore gün içi verisi.** ITCH müzayede defterini vermez ve işlem mesajında yalnız pasif emri gösterir; motor ancak gün içi verisiyle işlem işlem doğrulanabilir. ITCH'in rolü çapraz doğrulamadır.
- **Formda olup sistemde henüz olmayanlar:** KAP bildirimleri (bildirim zamanları, "son bildirimden geçen süre" özelliği, haberle açıklanan alarmların ayıklanması), birleşik uyarı sistemi, otokodlayıcı, arayüzde emir defteri görünümü, literatür bölümü.
- **Sistemde olup formda olmayanlar:** Z-skor temel çizgisi; devre kesici ve EBDKS müzayedeleri, tarih parametreleri ve ölçüm kontrolü; enjeksiyonsuz kontrol (yanlış alarm tabanı) ve büyüklük duyarlılığı; hisseye göre ayarlı senaryo ve kör nokta haritası; SPK etiketleriyle eğitilen pay-gün modeli.

**22.10 kararlarından geçerli kalanlar:** Z-skor temel çizgisi ve görselleştirme (zorunlu); Isolation Forest (eklendi); B seviyesi etiket penceresi N = 20 işlem günü, yasaktan 3 iş günü önce biter, yasaktan önceki 2 iş günü belirsizdir; öneri formu ve dilekçe kişisel bilgi içerdiği için git dışıdır; kural dosyalarının onayı veriyle birlikte yapılır.

### 9.3 Veri talep dilekçesi

Dilekçede (13.10.2026) istenenler:
- gün içi emir defteri ve gün içi işlem defteri: 01.03.2025–31.03.2025;
- aylık ITCH ve gün sonu fiyat-hacim: 01.06.2024–31.05.2025.

Karar (22.10): dilekçede ITCH için istenen aralıkta DataStore gün içi emir, gün içi işlem ve gün sonu verisi çekilir; ITCH yalnız 2025-01 ve 2025-02. Sonra aralık iki kez genişletildi (2025-06 ve 2024-01…05; 7.4). Bugün elde 18 ay vardır.

> **Akılda kalsın:** Dilekçedeki tarih aralığı çekirdek olarak korundu, yalnız o aralıkta hangi dosya türünün çekileceği değişti (ITCH yerine DataStore gün içi verisi) ve aralık iki yana uzatıldı.

## 10. SPK bülten etiketleme

### 10.1 Ne yapıldı, adım adım

SPK, manipülasyon kararlarını (işlem yasakları, idari para cezaları, suç duyuruları) haftalık bültenlerde yayımlar. Bu kararlar projenin "gerçek manipülasyon etiketleri"dir.

1. **Bültenler toplandı:** 2024–2026 arası 197 PDF (`kaynaklar/spk_bultenleri/`).
2. **Elle okundu:** 35 bülten gözle okunup çıkarım kuralları yazıldı (`veri/etiketler/etiket-cikarim-kurallari.md`; 22 kural, 4 etiket seviyesi).
3. **Betikle çıkarıldı:** `veri/araclar/spk_bulten_etiket.py` 197 bültende çalıştırıldı:
   - `vaka.csv`: 340 kod satırı (her pay kodu × karar),
   - `olay.csv`: 19 kayıt,
   - `vaka_pencere_dogrulama.csv`: 47 satır / 43 kod satırı / 28 kaynak vaka / 27 pay (A 6, B 22).
4. **Elle doğrulandı:** 47 pencere kaydı ve 19 olay PDF metniyle karşılaştırıldı; 10 sınıflandırma/bağlama hatası düzeltildi (`veri/etiketler/dogrulama-kaydi.md`).

### 10.2 Etiket seviyeleri

| Seviye | Ne zaman | Pay-gün etiketi |
|---|---|---|
| A | Pay kodu + manipülasyon dönemi açıkça yazılı | Dönemin işlem günleri "şüpheli" |
| B | Pay kodu + yalnız yasak başlangıcı belli, dönem yok | Yasaktan önceki 20 işlem günü (yasaktan önceki 2 iş günü belirsiz) |
| C | Pay kodu var ama dönem yok (ceza, suç duyurusu) | Etiket yok; aynı vakaya bağlanan A/B kaydı varsa onun seviyesini devralır |
| D | Kodsuz, "muhtelif paylar", varant | Etiket yok |

> **Örnek: aynı vaka birden çok bültende.** ALKLC önce 2025-17 bülteninde işlem yasağıyla (dönem 07–18.03.2025), sonra 2025-57 bülteninde suç duyurusuyla (dönem 04.02–18.03.2025) geçer. İki kayıt aynı vakaya bağlanır. Etiketsiz gün negatif değildir: SPK'nın henüz karar vermediği bir günde manipülasyon olmadığını bilemeyiz.

### 10.3 18 ayda değerlendirmeye giren etiketler

| Seviye | Pay | Pay-gün | Paylar |
|---|---|---|---|
| A | 4 | 93 | KRGYO, TDGYO, ALKLC, EUREN |
| B | 31 | 582 | (ayrıntı `rapor.md` 14.1) |
| Toplam | 34 | 675 | KRGYO hem A hem B |

Değerleme verisiyle bakıldığında SPK etiketli paylar küçük paylarda belirgin yoğunlaşmıyor (piyasa değeri yüzdeliği ortancası 0,46). Bu yüzden piyasa değeri modele girdi yapılmadı; yalnız raporlamada kullanılır.

### 10.4 Önemli teknik uyarı: Excel

CSV'ler virgül ayırıcılı, BOM'lu UTF-8'dir. **Excel'de açıp kaydetme.** Excel "6/1" gibi değerleri tarihe çevirip "6.Oca" yapar; bu yüzden 19.10.2026'da dosyalar betikle yeniden üretilmek zorunda kalındı. İnceleme için bütün sütunları metin olan `vaka_inceleme.xlsx` var.

### 10.5 Diğer notlar

- **Bağlantı kuralları (21–22):** bir karar, bülten arşivinin dışında kalan eski bir karara atıf yapıyorsa bağ kurulmaz (6 kayıt C seviyesinde kaldı). Bir belirsiz bağlantı kaldı (ENSRI, 2026-6).
- **VI-104.1 Tebliği** metni eklendi (2014 yayımı, 18.02.2017 değişikliği işlendi; 2017 sonrası değişiklik kontrol edilmedi). Kararlardaki bentler `manipulasyon_tipi` olarak çıkarıldı (188 idari para cezası kaydının hepsinde).
- **Eksik:** pay kodu ↔ şirket unvanı sözlüğü kurulmadı; pay kodları ITCH ile doğrulanmadı.
- **Açığa satış zaman çizelgesi:**

| Tarih | Olay |
|---|---|
| 06.02.2023 | Açığa satış yasağı başladı |
| 02.01.2025 | BIST 50 payları için kalktı |
| 24.03.2025 | Bütün paylarda yeniden getirildi (29.08.2025'e kadar uzatmalı) |
| 02.03–26.06.2026 | Ayrı bir yasak zinciri |

Veri bu çizelgeyle birebir uyumlu: 2024 aylarında açığa satış işlemi yok; 02.01–21.03.2025 arasında her gün aynı 50 payda var; 24.03.2025'ten itibaren yok.

## 11. Çeviriler ve ITCH doğrulaması

### 11.1 Protokol çevirileri (`veri/`)

| Çeviri | Ne işe yarar (sade) |
|---|---|
| ITCH 2112 | Borsanın kamuya yayımladığı piyasa verisinin mesaj biçimi |
| MoldUDP64 | ITCH mesajlarının ağda paketlenme biçimi |
| SoupBinTCP | TCP üzerinde oturum (bağlantı) katmanı |
| OUCH | Emir girişi protokolü |
| FIX Reference Data, FIX Order Entry (kapsamı sınırlı) | Referans verisi ve emir girişinin FIX biçimi |
| SMP ("emrimle eşleşmesin") | Bir üyenin kendi emirlerinin birbiriyle eşleşmesini önleme işlevi |
| DataStore dosya biçimleri | Emir, işlem ve gün sonu dosyalarının alan tanımları |

Hepsinde "Kullanıcı doğrulaması: bekliyor" yazılıdır.

### 11.2 ITCH 2018 örneği

08.10.2018 tarihli ITCH örneği doğrulandı (`veri/itch-ornek-veri-dogrulama.md`):
- TXT ve VRD dosyaları aynı içeriktedir; 5,6 milyon mesajda fark sıfır.
- VRD dosyası "2 bayt uzunluk + mesaj" dizisidir; MoldUDP64 başlığı yoktur.
- Zamanlar UTC'dir.
- 2018'de `R` (sıra tanımı) mesajı 129, `A` (emir ekleme) mesajı 37 bayttı.
- Seans durumu adları, tek fiyat, fiyat adımı ve öncelik kontrolleri yapıldı.

2025 örneği gelince mesaj uzunlukları ve dosya biçimi ITCH 2112 çevirisiyle yeniden sınanacak.

## 12. Bilinen açık noktalar

| Açık nokta | Sade anlamı | Etkisi |
|---|---|---|
| ITCH: Order Attributes = 2 ve Lot Type = 0 | İki alan değerinin anlamı belgede yok | ITCH çapraz doğrulamasında |
| ITCH: `TM`/`TR`/`GP` ön ekleri | Dosya adı ön eklerinin anlamı | Dosya eşlemesinde |
| ITCH: `Y` mesajının güncel davranışı | Defteri boşaltma (flush) mesajı | 2025 örneğiyle bakılacak |
| DataStore: sebep 116/117 | Sistem iptallerinin anlamı referans tablosunda yok | Motor bunları dışarıdan verilen olay olarak işliyor |
| DataStore: `guncelleme_no` atlamaları (%0,9) | Bir emrin fotoğraf albümünde kopuk sayfalar | Arada ne olduğu bilinmiyor |
| DataStore: kotasyon zincirinin geçersizleşme anı | Eski kotasyonun ne zaman bittiği ayrıca yazılmıyor | Kotasyonlar kapsam dışı |
| DataStore: aynı µs'deki olayların sırası | Genel sıra numarası yok | Çok nadir sapma; ITCH ile çözülebilir |
| Özsermaye günlerinde baz fiyat | Teorik fiyat kaynağı yok | Bu günler dışarıda |

## 13. Çalışma notları

| Not | Sade anlamı | Neden |
|---|---|---|
| Tablolar GFM uyumlu | Başlık satırındaki hücre sayısı = ayraç satırındaki hücre sayısı; tablo dikdörtgen | Aksi hâlde tablo GitHub'da ve PDF'te bozuk görünür |
| Eski ITCH betiklerindeki dosya yolları oturuma özgü | O betikler başka bir oturumun geçici klasörlerine bakar | Doğrudan çalıştırılamaz; `gunici_*` betikleri ise argüman alır |
| Aylık emir dosyası tarihe göre sıralı değil | Gün bazlı işler günlük bölümlemeden yapılır | Aylık dosyada bir günü okumak bütün ayı taramak demek |
| 16 GB RAM: büyük işler en çok ikişer paralel | Aynı anda en çok iki ağır iş | Bellek dolarsa bilgisayar kilitlenir ya da iş çöker |
| Büyük dosya yazımında heredoc yerine dosya yazıp çalıştır | Uzun Python kodu komut satırına gömülmez, dosyaya yazılıp çalıştırılır | Kabuk tırnak/karakter sorunları önlenir |
| `find /` çalıştırma | Bütün diski dosya aramakla tarama | Saatler sürer, sistemi yorar |

## 14. DURUM.md'de eskimiş kalan bilgiler

`DURUM.md`'nin tarihli bölümlerinde, sonradan güncellenmiş bazı sayılar ve bilgiler eski hâliyle duruyor. Bu belgede güncel değerler kullanıldı:

| `DURUM.md`'deki yer | Orada yazan | Güncel | Güncel kaynak |
|---|---|---|---|
| İlk satır | Son güncelleme: 25.10.2026 | Ekler 30.10.2026'ya kadar | `DURUM.md` 29.10 eki |
| Yapılacaklar 1–3 | Veri indirme, parametre ölçümü, 12 ay çalıştırma yapılacak işler olarak duruyor (içlerine ilerleme notları eklenmiş) | Üçü de bitti (18 ay) | `rapor.md` 13–16 |
| Kaldığımız yer (24.10) | 35 test | 41 test | `rapor.md` 14.4, 15 |
| Motor (22.10) | 23 test | 41 test | `rapor.md` 15 |
| Motor (22.10) | 03.03.2025: 588 sıra | 586 sıra (özsermaye günleri hariç; işlem sayısı ve oran aynı) | `TASARIM.md` 4.5 |
| Tespit ilk sürüm (22.10) | A kesitsel 0,85, B 0,55 | Mart: A 0,90, B 0,53; 18 ay: A 0,74, B 0,65; SPK denetimli A 0,84, B 0,69 | `rapor.md` 14.3 |
| Sentetik değerlendirme (22.10) | Yanıltıcı emir kurallarla 0,85, sonra 0,90 | Eski senaryo 18 ayda 0,90; ayarlı senaryo 0,57 | `rapor.md` 16 |
| Kaldığımız yer, kapanış göstergeleri | ×1'de ROC-AUC 0,80 | Mart: 0,77; ayarlı senaryo 18 ay (Z-skor): 0,67 | `TASARIM.md` 6.6, `rapor.md` 16 |
| Veri kapsamı kararı (22.10) | 2024-06…2025-05; 2025-06 ve sonrası aralık dışı | 2024-01…2025-06 (27.10 ve 29.10 kararları) | `CLAUDE.md`, `veri/README.md` |
| Eldeki veri | Bazı aylar "bölümlendi ama doğrulanmadı" | Hepsinde kayıpsızlık kontrolü ve parametre ölçümü yapıldı; alan doğrulaması yalnız Mart | `veri/README.md` |
| Bekleyen, disk | Kapsam D:'ye sığmaz, saklamayı kullanıcı yönetir | Aylık emir dosyaları ve zip'ler F:'ye taşındı | `veri/README.md` |
| Öneri formu bölümü | `.docx` form, ajan simülasyonu ve farkları | Doğru form kökteki PDF; ajan simülasyonu formda yok | `ANLATIM.md` 2.3–2.4 |
| `06-devre-kesici` satırı | DK eşleştirmesi sabit saatte | Sabit emir toplama + tarihe bağlı rastlantısal pencere (21.10.2026 kararı) | `CLAUDE.md`, `06-devre-kesici.md` |

Bu farklar `DURUM.md`'nin tarihli kayıt bölümlerinden gelir; o günkü durumu doğru anlatırlar, ama bugünkü sonuç değildirler.

## 15. Akılda kalsın: durumun on cümlelik özeti

1. Sekiz kural dosyası yazıldı; üçü kullanıcı onayı bekliyor; 128 açık soru var.
2. 18 aylık veri (2024-01…2025-06) hazır: dönüştürüldü, kayıpsızlığı kontrol edildi, tarih parametreleri her ayda ölçüldü ve hepsi aynı çıktı.
3. Motor gerçek işlemlerin %99,85'ini birebir üretiyor; 2024 başından seçilen günlerde de aynı düzeyde.
4. EBDKS eşiği endeks verisiyle doğrulandı: o dönemde eski metnin −%5 ve −%7 eşikleri geçerliydi.
5. Tek ayın sonuçları yanıltıcıydı; ay eklendikçe değerler oturdu ve 18 ay 13 ayı doğruladı.
6. Gerçek vakalar için en iyi araç SPK etiketleriyle eğitilen pay-gün modeli: A+B 0,71, A 0,84, B 0,69.
7. Sabit kalıplı senaryolar iyimserdi; hisseye göre ayarlı senaryoda yanıltıcı emir kurallarla 0,57, denetimli modelle 0,68.
8. Kör noktalar kesin: 60 saniyeden uzun ömürlü, tek katmanlı ya da en iyi fiyattaki sahte emirler ve olağan boyda karşılıklı işlem.
9. Sıradaki iş 60 saniye eşiğini veriye göre gözden geçirmek (önce ömür dağılımı ölçümü), ardından zamanda ileriye genelleme.
10. Vize raporundan önce eski öneri formuna dayanan yerler düzeltilmeli; doğru formda ajan simülasyonu yoktur.
