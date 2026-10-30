# Literatürden eklenebilecekler

İncelenen makalelerden sisteme eklenebilecek fikirler ve makalelerin kaynak olarak kullanılacağı yerler. **Buradakiler henüz uygulanmadı** (25.10.2026: şimdilik projeye uygulanmayacak, not olarak tutuluyor; 26.10.2026'da yinelendi: önce sistem hâkimiyeti, eklemeler sonra).

| No | Makale | Değerlendirme |
|---|---|---|
| M1 | Cao vd. (2015), IEEE TNNLS | Çekirdek kaynak; konuya doğrudan uygun, hakemli dergi |
| M2 | Ahsan vd. (2025), ICDICI | Kaynak olarak önerilmez (bölüm 2) |
| M3 | Gündüz vd. (2017), IEEE (Türkçe bildiri) | Yalnız bağlam kaynağı: literatürdeki eksikliği göstermek için anılır (bölüm 3) |
| M4 | Uslu ve Akal (2022), Computational Economics | Çekirdek kaynak: Borsa İstanbul ve SPK vakalarıyla en yakın hakemli öncül; bulgusu iyimser (bölüm 4) |
| M5 | Zaman vd. (2026), IEEE QPAIN | Zayıf; karşı örnek olarak anılır, birleşik uyarı fikri alınabilir (bölüm 5) |
| M6 | Do ve Putniņš (2023), SSRN ön baskısı / doktora tezi bölümü | Çekirdek kaynak: kovuşturulmuş gerçek vakalarla sınanmış yanıltıcı emir göstergeleri; hakemsiz (bölüm 6) |

Vize raporuna girecekler bütün makalelerden toplanarak bölüm 7'dedir.

## Özet: sisteme eklenebilecekler

Ayrıntı ilgili makalenin bölümünde. Hiçbiri uygulanmadı; kullanıcıyla yeniden değerlendirilecek.

| No | Ne | Neden | Ne zaman yapılabilir | Öncelik | Makale |
|---|---|---|---|---|---|
| E1 | Hızlı yanıltıcı emir senaryosu ve "en iyi fiyatı iyileştirip hızla iptal edilen emir payı" göstergesi | Gerçek vakası olan bir tür sistemde yok | Şimdi (Mart verisi) | Yüksek | M1 |
| E2 | En iyi fiyatın sıçrayıp geri dönmesi göstergesi | E1'i fiyat tarafından da görmek | E1 ile birlikte | Orta | M1 |
| E3 | Smarts kapanış kuralı, temel çizgi olarak | Kapanış göstergelerini endüstri kuralıyla karşılaştırmak | 12 aylık veriyle | Düşük | M1 |
| E4 | SPK değerlendirmesinde ikinci negatif küme: aynı payın dönem dışı günleri | Uslu ve Akal ile karşılaştırılabilirlik | Kısmen şimdi (ALKLC), asıl 12 aylık veriyle | Yüksek | M4 |
| E5 | Vaka zaman çizelgesi grafiği: puanlar ve SPK dönemi | Sunum; dönemde yükselip sonra düşme | ALKLC şimdi; KRGYO, TDGYO 2025-01/02 hazırlanınca | Yüksek | M4 |
| E6 | Fiyat yönüne göre işlem payı (artıran, azaltan, değiştirmeyen) | Bent f (fiyat yükseltme), en zayıf senaryomuz | Şimdi | Düşük | M4 |
| E7 | Birleşik uyarı seviyesi: kural ve model birlikte, seviyeler eşiğe bağlı | Öneri formu adım 11, henüz yapılmadı | Şimdi tasarlanabilir | Yüksek | M5 |
| E8 | Pay düzeyinde şüphe puanı (sıklık + şiddet) ve en şüpheli paylar listesi | Uzun süreli (B) vakalar; arayüz | 12 aylık veriyle | Orta | M5 |
| E9 | Do-Putniņš yanıltıcı emir göstergeleri, olay düzeyinde: derinlik ve iptal dengesizliği, dengesizliğin ters tarafında işlem, döngü sayısı | En iyi fiyattaki sahte emirde mevcut yöntemler rastgeleye iniyor (ölçüldü, `rapor.md` 8); göstergeler gerçek vakalarla sınanmış | Şimdi (Mart verisi) | Yüksek | M6 |
| E10 | Döngüsel yanıltıcı emir senaryosu: iki taraflı, en iyi fiyata yakın, gerçekleşme yaklaşınca iptal edip yeniden giren, tekrarlı | Gerçek vakaların tipik kalıbı; en iyi fiyattaki katmanlar bugün vakaların yarısında doluyor | E9 ile birlikte | Orta | M6 |
| E11 | Yanıltıcı emir senaryosunda karışık katman uzaklığı; sonuçların uzaklığa göre ayrı raporlanması (kullanıcı önerisi) | Sabit 4–6 adım sonucu şişiriyor; SPK vakalarında sahte emir yeri tek yönlü değil (`rapor.md` 9) | Şimdi | Yüksek | M6, kullanıcı |

## 1. Cao vd. (2015): aykırı durumlu uyarlamalı gizli Markov modeli

**Künye:** Cao, Y., Li, Y., Coleman, S., Belatreche, A., McGinnity, T. M. (2015). Adaptive Hidden Markov Model With Anomaly States for Price Manipulation Detection. *IEEE Transactions on Neural Networks and Learning Systems*, 26(2), 318–330. DOI: 10.1109/TNNLS.2014.2315042

**Kısaca:** Yazarların elinde yalnız en iyi alış/satış fiyatı serisi var, emirleri göremiyorlar. Sahte emirlerin fiyat çizgisinde bıraktığı kısa süreli şekilleri (testere dişi, kare dalga, darbe) dalgacık dönüşümü ve gizli Markov modeliyle arıyorlar. Etiketli veri olmadığı için bu şekilleri gerçek veriye yapay olarak ekleyip ölçüyorlar.

**Bizden farkı:** biz her emri (giriş, değişiklik, iptal) görüyoruz. Manipülasyonu fiyatın şeklinden tahmin etmek yerine emirlerin kendisine bakabiliyoruz. Bu yüzden makalenin modeli değil, içindeki birkaç fikir işe yarar.

### 1.1 Sisteme eklenebilecekler

#### E1. Hızlı yanıltıcı emir senaryosu ve göstergesi (öncelik 1)

**Makaledeki vaka (FINRA 2012, Hold Brothers; makale II-A ve II-C, Şekil 2a):**
- Manipülatör önce gerçek bir satış emri koyuyor.
- Sonra en iyi alışın üstüne, giderek yükselen sahte alışlar giriyor. En iyi alış 6,9 bp yükseliyor, makas %87,5 daralıyor.
- Kandırılan alıcı geliyor; 1.000 lotun 845'i satılıyor.
- Sahte alışlar 767 ms içinde iptal ediliyor ve fiyat eski yerine dönüyor.
- İşlemin tamamı 819 ms sürüyor.

**Borsa İstanbul'a uyarlanmış örnek** (fiyat 100 TL, fiyat adımı 0,10 TL):
1. Başta en iyi alış 100,00, en iyi satış 100,30.
2. Manipülatör 100,20'den gerçek satış emri koyar.
3. Ardından 100,10'a büyük bir sahte alış girer; en iyi alış 100,10'a çıkar ve "alıcı var" görüntüsü oluşur.
4. Biri 100,20'den alır ve manipülatörün satışı gerçekleşir.
5. Sahte alış birkaç saniye içinde iptal edilir.

**Bizde neden yok:**
- Bizim yanıltıcı emir senaryomuz sahte emirleri en iyi fiyatın 4–6 adım gerisine koyup 30 sn bekletiyor (`tespit/sentetik_degerlendir.py` `YANILTICI_ADIM`, `motor/senaryolar.py` `yaniltici_emir`).
- Göstergemiz `kisa_omurlu_uzak_pay` ise yalnız en iyi fiyattan en az 3 adım uzakta duran ve 60 sn içinde işlem görmeden iptal edilen emirleri sayıyor (`tespit/ozellikler.py` `UZAK_ADIM`, `KISA_SN`).
- Hızlı türdeki sahte emir en iyi fiyatın önüne geçtiği için bu göstergeye hiç girmiyor.
- Tersine, makalenin fiyat şekli yöntemi de bizim derin katman senaryomuzu göremez, çünkü orada en iyi fiyat oynamıyor.

**Eklenecekler:**
- **Senaryo:** `motor/senaryolar.py`'ye `hizli_yaniltici`. Önce gerçek emir, sonra kendi tarafının en iyi fiyatını iyileştiren sahte emir, birkaç saniye sonra iptal.
  - Ayrıca `tespit/sentetik_degerlendir.py` `SENARYO_SIRASI`'na beşinci senaryo olarak eklenir ve arayüzde `SENARYOLAR`'a girer.
- **Gösterge:** "en iyi fiyatı iyileştirip K sn içinde işlem görmeden iptal edilen emir payı".
  - Pay-gün düzeyi `tespit/ozellikler.py`'de, mevcut `uzak_kisa_omurlu` fonksiyonunun yanına yazılır.
  - Sentetik emirler için `tespit/motor_ozellikleri.py`, 5 dk pencere için `tespit/pencere.py` düzeyinde de hesaplanır.
- **Kural:** VI-104.1 bent b'ye (yanıltıcı emir) ek koşul olarak girer; yeni bir bent uydurulmaz (`tespit/yontemler.py`, `tespit/pencere.py`).
- **Test:** `tespit/testler/` altına gösterge testi, `motor/testler/` altına senaryo testi.

**Uygularken karar verilecek ya da doğrulanacaklar:**
- **Makas tek adımsa sahte emir en iyi fiyatı iyileştiremez,** çünkü karşı taraftaki emirle eşleşir. Likit paylarda makas çoğu zaman tek adımdır. Senaryo yalnız makasın en az 2 adım olduğu anlarda kurulur, ya da o anlarda sahte emir en iyi fiyata (iyileştirmeden) büyük miktar olarak girilir.
- **Gösterge için "girişten önceki en iyi fiyat" gerekli.** DataStore emir dosyasındaki en iyi alış/satış alanı "emir girildikten sonraki" en iyi fiyattır (`veri/datastore-dosya-formatlari.md` satır 586). En iyi fiyatı iyileştiren emirde bu alan emrin kendi fiyatına eşit çıkar. Önceki en iyi fiyat, aynı paydaki bir önceki olay satırından alınmalıdır. [DOĞRULA: veride örnek emirlerle kontrol]
- **Süre eşiği K:** makaledeki vakada 767 ms. Veri zamanı mikro saniye çözünürlüklü; K birkaç saniye seçilip duyarlılığa bakılır.
- **Temizlik ölçütü:** sahte emir işlem görürse vaka dışarıda kalır (yanıltıcı emirdeki `katman_dolan` gibi).

#### E2. En iyi fiyatın sıçrayıp geri dönmesi göstergesi (öncelik 2)

**Kaynak:** makalenin testere dişi ve kare dalga fikrinin (II-C ve III, Şekil 2) dalgacık ve HMM kullanmayan, basit sayım hali.

**Tanım:** pencerede, en iyi alışın (satışın) en az 1 adım iyileşip K sn içinde eski düzeyine döndüğü olay sayısı.

**Veri:**
- Gerçek veride DataStore emir satırlarındaki en iyi alış/satış alanı kullanılır; motor gerekmez.
- Enjeksiyonlu oynatmada motorun defter örnekleri kullanılır (`motor/gun.py` `defter_ornekleri`). Bunlar 1 sn aralıklı olduğundan saniye altı olayları kaçırabilir; gerekirse olay düzeyinde hesaplanır.

**Uyarı:** normal yüksek frekanslı işlem de aynı şekli bırakır (makale V-C, Şekil 13). Bu yüzden tek başına kural olmaz; E1 göstergesiyle birlikte ya da modellere özellik olarak kullanılır.

#### E3. Smarts kapanış kuralı, temel çizgi olarak (öncelik 3)

**Kural** (Aitken, Harris, Ji 2009; NASDAQ OMX'te gözetimde kullanılan, makale II-B): kapanış fiyatı ile 15 dakika önceki fiyat arasındaki değişim, payın geçmiş değişimlerinin %99'luk diliminin üstündeyse alarm verilir.

**Bizdeki karşılığı:**
- `kapanis_oncesi_getiri`: son sürekli işlem fiyatı / 17:45 öncesi son işlem fiyatı (`tespit/ozellikler.py`). Kapanış müzayedesini içermez; müzayede ayrıca `kapanis_muzayede_sapma` ile ölçülür.
- Eşik %99 dilimi yerine z-skor.

**Eklenebilecek:** kuralın birebir hali (kapanış müzayedesi fiyatı / 17:45 öncesi fiyat, payın kendi geçmişinde %99 dilim) ayrı bir temel çizgi olur. Kapanış etkilemesi senaryosunda bizim kapanış göstergelerimizle karşılaştırılır. Payın kendi geçmişi gerektiğinden 12 aylık veri hazır olunca yapılabilir.

### 1.2 Eklenmeyecekler ve nedeni

- **Dalgacık dönüşümü, DPGMM, 32 durumlu gizli Markov modeli, uyarlamalı yeniden eğitim:**
  - Bu araçlar yalnız fiyat verisi olduğu için gerekmiş; bizde emir verisi var.
  - Borsa İstanbul'da fiyat adımı büyük. Örneğin 300 TL'lik payda adım 0,25 TL, yani ≈ 8,3 bp. Makaledeki 6,9 bp'lik hareket burada tek adımdan küçük kalır ve fiyat çizgisinde görünmez.
  - Sonuçlar yalnız fiyat çizgisine yapay olarak çizilen üç sabit şekille ölçülmüş; emir defteri ve eşleştirme yok.
  - Öneri formunda yok; takvimde ayrılacak zaman yok.

### 1.3 Kaynak olarak kullanılacağı yerler

| Konu | Makaledeki yer | Kullanılacağı yer |
|---|---|---|
| Manipülasyon türleri: ramping, quote stuffing, pump & dump, kapanış; FINRA Hold Brothers vakası | II-A, Şekil 1, Tablo I | ANLATIM 1.9; vize raporu literatür bölümü |
| Etiketli veri yokken gerçek veriye sentetik kalıp ekleyerek değerlendirme (endüstride kabul gören yol) | V-A | ANLATIM 5.1; vize raporu yöntem. Bizim farkımız: emirler kurallarla doğrulanıyor ve motorda gerçek emirlerle eşleşiyor |
| Günlük getiri/hacim sapmasına dayalı yöntemlerin eleştirisi (meşru olaylar da sapma yaratır) | II-B | ANLATIM 2.4 (KAP ayıklaması adımının gerekçesi), 6.7 (kesitsel karşılaştırma) |
| Smarts kapanış kuralı (kapanış − 15 dk, %99 dilim) | II-B | ANLATIM 6.8 ve 7.2 (bent d, kapanış göstergeleri) |
| Aykırı bölge eşiği: uçlardaki %0,5 + %0,5 | IV | ANLATIM 6.4 (\|z\| ≥ 3 eşiğinin gerekçesi) |
| Bir limit emrin fiyat etkisi: en iyi alışın 5 bp üstüne konan emir en iyi alışı ortalama 5,95 bp daha yükseltiyor (Hautsch & Huang 2012) | II-C | ANLATIM 5.1 ve 10 ("gerçek akış dışsaldır" sınırının büyüklüğü) |
| "Temiz" sayılan test verisinde gerçek şüpheli salınım (Microsoft, Şekil 13) | V-C | ANLATIM 6.14 (etiketsiz gün negatif değildir) |
| Gelecek iş: fiyat serisini emir bilgisiyle birlikte modellemek | VI | Vize raporunda katkı cümlesi; ANLATIM 12 ("Literatürde benzeri var mı?") |
| Türkiye'de (İMKB) manipülasyon tespiti çalışması (Öğüt vd. 2009) | II-B | Vize raporu literatür bölümü |

### 1.4 Makalenin kaynakçasından okunacaklar

Bu çalışmalara atıf yapmadan önce asıllarının okunması gerekir; aşağıdaki özetler Cao vd.'nin anlatımından alınmıştır (ikincil).

| Künye | Neden önemli |
|---|---|
| Öğüt, H., Doğanay, M. M., Aktaş, R. (2009). Detecting stock-price manipulation in an emerging market: The case of Turkey. *Expert Systems with Applications*, 36(9), 11944–11949. | İMKB verisiyle; günlük getiri, hacim ve oynaklıktan YSA, lojistik regresyon ve SVM. Türkiye'deki en yakın öncül |
| Diaz, D., Theodoulidis, B., Sampaio, P. (2011). Analysis of stock market manipulations using knowledge discovery techniques applied to intraday trade prices. *Expert Systems with Applications*, 38(10), 12757–12771. | SEC vakalarında gün içi işlem fiyatlarıyla tespit |
| Aitken, M. J., Harris, F. H., Ji, S. (2009). Trade-based manipulation and market efficiency: A cross-market comparison. *Proc. 22nd Australasian Finance and Banking Conference*. | Smarts kapanış rampası kuralı (E3) |
| Lee, E. J., Eom, K. S., Park, K. S. (2013). Microstructure-based manipulation: Strategic behavior and performance of spoofing traders. *Journal of Financial Markets*, 16(2), 227–252. | Yanıltıcı emir (spoofing) yapanların davranışı; E1 senaryosunun tasarımı için |
| Hautsch, N., Huang, R. (2012). The market impact of a limit order. *Journal of Economic Dynamics and Control*, 36(4), 501–522. | Limit emrin fiyat etkisi; "gerçek akış dışsaldır" sınırı |
| Allen, F., Gale, D. (1992). Stock-price manipulation. *Review of Financial Studies*, 5(3), 503–529. | Bilgiye, eyleme ve işleme dayalı manipülasyon ayrımı (temel tanım kaynağı) |
| Mongkolnavin, J., Tirapat, S. (2009). Marking the close analysis in Thai Bond Market surveillance using association rules. *Expert Systems with Applications*, 36(4), 8523–8527. | Kapanışı etkileme tespiti (kural tabanlı) |
| Cumming, D. J., Zhan, F., Aitken, M. J. (2013). High frequency trading and end-of-day manipulation. York University, teknik rapor. | Yüksek frekanslı işlem ve kapanış manipülasyonu |
| FINRA (2012). FINRA Joins Exchanges and the SEC in Fining Hold Brothers More Than $5.9 Million for Manipulative Trading, Anti-Money Laundering, and Other Violations. Basın bülteni. | E1'deki vakanın birincil kaynağı |

## 2. Ahsan vd. (2025): LSTM/GRU ile fiyat tahmini ve anomali tespiti

**Künye:** Ahsan, M. N., Moniruzzaman, M., Jahan, S. (2025). Deep Learning-based Stock Price Forecasting and Anomaly Detection: A Data-Driven Approach. *Proc. 6th International Conference on Data Intelligence and Cognitive Informatics (ICDICI-2025)*, IEEE, 1645–1651. DOI: 10.1109/ICDICI66477.2025.11135369

**Sisteme eklenebilecek:** yok. Günlük fiyat tahmini yapıyor; manipülasyon, emir verisi ve borsa kuralı içermiyor.

**Kaynak olarak önerilmez:**
- Kaynakça metinle uyuşmuyor (CO2 ve enerji makaleleri).
- "Anomali" ölçüsü tanımlanmamış ve değerlendirilmemiş.
- Anomaliler gerçek veride değil, tahminler üzerinde aranmış.
- Basit bir karşılaştırma (naif tahmin) yok.
- Eğitim ve test aynı grafikte çizilmiş.
- Metinde iç tutarsızlıklar var (14/10 yıl, "BP shares").

Gerekirse yalnız "derin öğrenmeyle fiyat tahmini manipülasyon tespiti değildir" ayrımını göstermek için anılabilir.

## 3. Gündüz vd. (2017): derin sinir ağlarıyla Borsa İstanbul yön tahmini

**Künye:** Gündüz, H., Çataltepe, Z., Yaslan, Y. (2017). Derin Sinir Ağları ile Borsa Yönü Tahmini (Stock Market Direction Prediction Using Deep Neural Networks). IEEE, 25. Sinyal İşleme ve İletişim Uygulamaları Kurultayı (SIU 2017). [DOĞRULA: kurultay adı, sayfa ve DOI IEEE Xplore kaydından]

**Kısaca:**
- GARAN, THYAO ve ISCTR'nin günlük kapanış yönünü (yükseliş/düşüş) evrişimsel sinir ağıyla tahmin ediyor.
- Veri 2011–2015, 931 gün: ilk 663 gün eğitim, son 268 gün test.
- Girdi: fiyattan 58, dolar ve altından 29'ar teknik gösterge.
- Doğruluk 0,574–0,61. Dolar-altın göstergeleri eklenince 1–4 puan artış bildiriliyor.

**Sisteme eklenebilecek:** yok. Manipülasyon, emir verisi ve borsa kuralı içermiyor.

**Kaynak olarak kullanımı (25.10.2026 kararı):** vize raporunun literatür bölümünde, Borsa İstanbul literatüründeki eksikliği göstermek için anılır. Kullanılacağı yerler: vize raporu literatür bölümü ve ANLATIM 12 ("Literatürde benzeri var mı?").

Örnek cümle:

> Borsa İstanbul verisiyle yapılan makine öğrenmesi çalışmalarının büyük kısmı fiyat ya da yön tahminine yöneliktir (Kara vd. 2011; Gündüz vd. 2017). Manipülasyon tespiti az çalışılmıştır ve mevcut çalışmalar günlük veriyle sınırlıdır (Öğüt vd. 2009; Uslu ve Akal 2022). Emir düzeyinde veriyle, borsa kurallarına uygun bir eşleştirme motorunda sentetik manipülasyonla değerlendirme yapan bir çalışmaya rastlanmamıştır.

**Atıf yaparken dikkat:** makale yalnız "bu konuda çalışma var" bağlamında anılır; bulgusu bir sonuç olarak aktarılmaz. Nedenleri:
- Dolar-altın katkısı (1–4 puan), 268 günlük testte doğruluğun ±0,06'lık %95 güven aralığı içinde kalıyor; anlamlılık testi yok.
- Basit tahmin (hep "yükselir") temel çizgisi verilmemiş; etikette eşit günler yükseliş sayılıyor.
- Özelliklerin etiketle hangi günde hizalandığı açık değil; özelliklerde o günün kapanışı var.
- Ayar seçimindeki 5 katlı çapraz doğrulamanın zaman sırasını koruyup korumadığı yazılmamış.

**Yöntem açısından not:** test kümesini zamana göre ayırmışlar (ilk günler eğitim, son günler test). Bizde denetimli model pay-gün bazında gruplu çapraz doğrulama kullanıyor (ANLATIM 6.12). 12 aylık veriyle buna zamana göre bir sınama da eklenebilir: ilk aylarla eğitip son aylarda sınamak.

**Bu bağlam cümlesi için okunacak kaynaklar** (künyeler bu makalenin kaynakçasından ve Google Scholar'dan; atıf yapmadan önce asıllarına bakılmalı):

| Künye | Kullanım |
|---|---|
| Kara, Y., Boyacıoğlu, M. A., Baykan, Ö. K. (2011). Predicting direction of stock price index movement using artificial neural networks and support vector machines: The sample of the Istanbul Stock Exchange. *Expert Systems with Applications*, 38(5), 5311–5319. | BIST'te yön tahmini (bağlam) |
| Gündüz, H., Çataltepe, Z. (2015). Borsa Istanbul (BIST) daily prediction using financial news and balanced feature selection. *Expert Systems with Applications*, 42(22), 9001–9011. | BIST'te haberle günlük tahmin (bağlam) |
| Uslu, N. C., Akal, F. (2022). A machine learning approach to detection of trade-based manipulations in Borsa Istanbul. *Computational Economics*, 60, 25–45. DOI: 10.1007/s10614-021-10131-8 | BIST'te manipülasyon tespiti: 22 SPK vakası (2010–2015), günlük veri, denetimli model; eksikliğin karşı tarafı (bölüm 4) |
| Öğüt, H., Doğanay, M. M., Aktaş, R. (2009). Bölüm 1.4'te. | BIST'te manipülasyon tespiti, günlük veri |

## 4. Uslu ve Akal (2022): Borsa İstanbul'da işlem bazlı manipülasyon tespiti

**Künye:** Uslu, N. C., Akal, F. (2022). A Machine Learning Approach to Detection of Trade-Based Manipulations in Borsa Istanbul. *Computational Economics*, 60, 25–45. DOI: 10.1007/s10614-021-10131-8

Uslu'nun Hacettepe'deki doktorasından; Uslu SPK Strateji Geliştirme Dairesi'nde çalışıyor.

**Kısaca:**
- SPK haftalık bültenleri 2010–2015 için taranmış: 75 pay, 256 vaka; ortalama manipülasyon süresi 66 gün.
- En çok manipüle edilen 20 pay (22 vaka) seçilmiş.
- SPK'nın işlem verisi (yatırımcı kimliğiyle, yaklaşık 1 milyar satır) günlük özetlere çevrilmiş; yaklaşık 20 özellik var (Tablo 1).
- Etiket: SPK'nın verdiği dönem 1; aynı payın dönemden önceki ve sonraki, eşit uzunlukta günleri 0.
- 6 sınıflandırıcı × 2 ölçekleme = 12 model. Her payda test kümesinde en iyi F1'i veren seçilmiş: F1 0,91. Tek algoritmalarda en iyisi naive Bayes ve SVM: F1 0,85.
- En önemli özellikler fiyat düzeyi: ağırlıklı ortalama, en düşük ve en yüksek fiyat (Şekil 3).

**Bizden farkı:**

| Konu | Uslu ve Akal | Bizim sistem |
|---|---|---|
| Veri | Gün sonu işlem özetleri (SPK iç verisi, yatırımcı kimliğiyle) | Gün içi emir verisi (DataStore): emir, değişiklik, iptal, müzayede |
| Etiket | SPK haftalık bültenleri | Aynı kaynak (A ve B seviyeleri, `veri/etiketler/`) |
| Negatif örnek | Aynı payın dönem öncesi ve sonrası | Bütün diğer pay-günler; etiketsiz gün negatif sayılmaz (ANLATIM 6.14) |
| Değerlendirme | Pay başına; model test kümesinde seçiliyor | Gruplu çapraz doğrulama; SPK vakaları ve motorda sentetik enjeksiyon |
| Özellikler | Fiyat düzeyi ağırlıklı | Oranlar ve z-skorlar; fiyat düzeyinden bağımsız |

### 4.1 Sisteme eklenebilecekler

#### E4. SPK değerlendirmesinde ikinci negatif küme (öncelik: yüksek)

- **Ne:** SPK etiketli günler bugün bütün diğer pay-günlerle karşılaştırılıyor (`tespit/degerlendir.py`). Buna ikinci bir karşılaştırma eklenir: aynı payın dönem dışındaki günleri. Bu, Uslu ve Akal'ın kurgusudur. İki sonuç yan yana raporlanır.
- **Neden:**
  - Sonuçlarımız Borsa İstanbul'daki hakemli öncülle karşılaştırılabilir olur.
  - "Aynı payın kendi öncesi ve sonrasıyla karşılaştırmak işi kolaylaştırır; gözetimde asıl soru bütün paylar arasındadır" argümanı sayıyla gösterilir.
  - Sunumdaki "Onlar %91 aldı, siz neden daha düşük?" sorusunun cevabı olur.
- **Şimdi yapılabilir mi:** kısmen.
  - Mart 2025'te A vakası yalnız ALKLC: dönem 18.03'te bitiyor, 19–31.03 sonrası. B'de 5 pay var.
  - Asıl sonuç 12 aylık veriyle çıkar; o zaman KRGYO, TDGYO ve EUREN de girer.
- **İş:** `tespit/degerlendir.py`'de ikinci negatif küme ve sonuç tablosuna bir sütun.
- **Dikkat:** aynı payın dönem dışındaki günleri de "temiz" sayılamaz (ANLATIM 6.14). B'de pencere dışında kalan günler gerçekte dönemin içinde olabilir. Bu karşılaştırma yalnız onların kurgusunu yeniden üretmek içindir; asıl ölçüt bütün paylarla karşılaştırma olarak kalır.

#### E5. Vaka zaman çizelgesi grafiği (öncelik: yüksek)

- **Ne:** A seviyesi vakalarda günlük puanları (z-skor, kural, Isolation Forest, kesitsel) zamana göre çizip SPK dönemini gölgelemek.
- **Neden:**
  - Bu bulgu bizim puanlarımızla gösterilir: manipülasyon döneminde hacim, getiri ve likidite artar, sonra düşer (Aktaş ve Doğanay 2006; Aggarwal ve Wu 2006).
  - ALKLC'de kesitsel puanın iyi (AUC 0,90), z-skorun zayıf (0,63) çıkmasını görsel olarak açıklar. Dönem 04.02'de başladığı için z-skorun dayandığı geçmiş de kirlidir (ANLATIM 6.4).
  - Sunum için anlaşılır bir şekil olur.
- **Şimdi yapılabilir mi:** ALKLC için Mart verisiyle evet. KRGYO ve TDGYO için 2025-01/02 verisinin hazırlanması gerekir.
- **İş:** puanlar `veri/gunici-dogrulama/2025-03/tespit/puanlar.parquet`'te hazır; bir çizim betiği ya da arayüzde bir sekme.

#### E6. Fiyat yönüne göre işlem payı (öncelik: düşük)

- **Ne:** pay-gün ve pencere için fiyatı önceki işleme göre artıran, azaltan ve değiştirmeyen işlemlerin sayı ve hacim payı. Makalede fiyat düzeyinden sonraki önemli grup bu (Şekil 3).
- **Neden:** bent f (fiyat yükseltme); bu senaryo bizde en zayıf olanı.
- **Çekince:** pencerede benzeri olan "net agresif adım" belirgin katkı vermedi; büyük bir kazanç beklenmiyor.
- **İş:** gün içi işlem verisinden hesaplanır. Etkilenen dosyalar `tespit/ozellikler.py`, `tespit/motor_ozellikleri.py` (sentetik) ve `tespit/pencere.py`; ardından test ve yeniden hesap.

### 4.2 Alınmayacaklar

- **Alıcı ve satıcı sayısı:** yatırımcı kimliği gerektirir; DataStore'da yok. `PP_UYESIRA` üye bazında toplamdır, pay bazında değil.
- **Fiyat düzeyi özellikleri** (ortalama, en yüksek, en düşük fiyat): makaledeki hatanın kaynağı.
- **Test kümesinde model seçimi** ve doğrulama F1'i bir eşiği geçene kadar özellik çıkarma.

### 4.3 Kaynak olarak kullanılacağı yerler

| Konu | Makalede | Kullanılacağı yer |
|---|---|---|
| Borsa İstanbul ve SPK vakalarıyla en yakın öncül | Bütünü | Vize raporu literatür bölümü; ANLATIM 12 |
| SPK haftalık bültenlerinden etiket çıkarma (aynı yöntem) | Bölüm 3, 4.1 | ANLATIM 7.4; `veri/etiketler/etiket-cikarim-kurallari.md` |
| 2010–2015'te 75 pay, 256 vaka; ortalama süre 66 gün | Bölüm 3 | B penceresi tartışması: bizim 2024–2026 bültenlerinde dönem ortancası 23,5 işlem günü (n = 12); N = 40 duyarlılık analizinin gerekçesi |
| Negatif örnek kurgusu ve test kümesinde model seçimi | Bölüm 4 | ANLATIM 6.13–6.14: neden bütün paylarla karşılaştırıyoruz ve test kümesinde seçim yapmıyoruz |
| Gelecek iş: davranış modelleriyle daha hızlı tespit, Borsa İstanbul'un çevrim içi gözetimini geliştirmek | Bölüm 5 | Katkı cümlesi: biz gün içi emir düzeyine iniyoruz |

### 4.4 Atıf yaparken dikkat

- **0,91 F1 başarı olarak aktarılmaz.** Her payda 12 modelden test sonucu en iyi olan seçilmiş. Aktarılacaksa tek algoritmanınki (0,85) kurgunun sınırıyla birlikte verilir.
- **Piyasa geneli ölçülmemiş.** Negatif örnekler aynı payın öncesi ve sonrası; piyasa genelinde yanlış alarm oranına bakılmamış.
- **Sayılar tutarsız.** Metinde en uzun dönem 103 gün; Tablo 2'de tek vakalık dönemler 71–209 gün (8. pay 01.06.2010–01.03.2011).
- **Yöntem ayrıntıları eksik.** Bölmenin rastgele mi zaman sırasıyla mı yapıldığı ve ölçeklemenin hangi veriden öğrenildiği yazmıyor.

### 4.5 Kaynakçasından okunacaklar

| Künye | Kullanım |
|---|---|
| Kim, Y., Sohn, Y. S. (2012). Stock fraud detection using peer group analysis. *Expert Systems with Applications*, 39(10), 8986–8992. | Payı benzer paylarla karşılaştırarak sapma arama: kesitsel karşılaştırmamızın kaynağı (ANLATIM 6.7) |
| Aktaş, R., Doğanay, M. (2006). Stock-price manipulation in the Istanbul Stock Exchange. *Eurasian Review of Economics and Finance*, 2, 21–28. | Borsa İstanbul'da manipülasyon döneminde hacim, getiri ve likidite artıyor, sonra düşüyor; özellik seçimi ve E5 |
| Aggarwal, R. K., Wu, G. (2006). Stock market manipulations. *The Journal of Business*, 79(4), 1915–1953. | 142 SEC vakası; düşük likiditeli paylar daha çok manipüle ediliyor; fiyat dönem sonrasında geri dönüyor |
| Leangarun, T., Tangamchit, P., Thajchayapong, S. (2016). Stock price manipulation detection using a computational neural network model. *ICACI 2016*, 337–341. | Uslu ve Akal'ın aktarımına göre emir iptali bilgisi olmadan spoofing modellenemiyor: emir verisi kullanmamızın gerekçesi |
| Li, A., Wu, J., Liu, Z. (2017). Market manipulation detection based on classification methods. *Procedia Computer Science*, 122, 788–795. | Aktarıma göre günlük veriyle iyi, tick verisiyle zayıf; örneklem dışı sınama yok |
| Wang, Q., Xu, W., Huang, X., Yang, K. (2019). Enhancing intraday stock price manipulation detection by leveraging recurrent neural networks with ensemble learning. *Neurocomputing*, 347, 46–58. | Gün içi tespit (Çin, CSRC vakaları) |

## 5. Zaman vd. (2026): kümeleme ile şüpheli işlem örüntüleri

**Künye:** Zaman, A., Sarkar, R. M., Ohi, S. K., Mobin, I. (2026). A Clustering-Based Framework for Identifying Suspicious Trading Patterns in Capital Market. *2026 IEEE 2nd International Conference on Quantum Photonics, Artificial Intelligence, and Networking (QPAIN)*, Chittagong. DOI: 10.1109/QPAIN69676.2026.11546622

**Kısaca:**
- Dakka borsasının 2012–2024 günlük verisi (yaklaşık 1 milyon pay-gün) K-Means (k = 5) ile kümeleniyor.
- Kümesinden uzak olan ve hacmi ya da fiyatı sıçrayan pay-günler şüpheli sayılıyor (%2,02).
- Türler eşiklerle adlandırılıyor; şüphelilerin %51'i "spoofing".
- Doğrulama yalnız siluet skoru.

**Kaynak olarak:** zayıf; yalnız karşı örnek olarak anılır.
- Günlük veriyle spoofing iddia ediliyor; bu emir verisi kullanmamızın gerekçesini destekler.
- Bölünme ve bedelsiz düzeltmesi ile hisse dışı araç ayıklaması yapılmadığında yanlış alarm çıkıyor:
  - Şekil 4: SBIN'de 2014 bölünmesinden sonra sürekli alarm.
  - Şekil 5: en şüpheli 20 menkulün 11'i fon ya da tahvil.
- Bizde ikisi de var: özsermaye günleri dışarıda (`tespit/degerlendir.py`), yalnız pay pazarlarının `.E` serileri alınıyor (`tespit/ozellikler.py`).

**Sisteme eklenebilecekler:**
- **E7. Birleşik uyarı seviyesi (öneri formu adım 11).**
  - Makaledeki fikir: yapısal aykırı (model) + en az bir davranış koşulu (kural).
  - Öneri: kural ve model (Isolation Forest ya da kesitsel puan) ikisi de işaretlediyse "yüksek", yalnız biri işaretlediyse "orta".
  - Seviyeler eşiğe bağlı olmalı. Makaledeki gibi salt yüzdelik dilim, hiçbir şey olmayan günde de payların %10'unu "kritik" yapar.
  - Solak vd. (2026) da katmanlı eşik politikaları öneriyor; okunduktan sonra tasarım netleşir.
- **E8. Pay düzeyinde şüphe puanı.**
  - Sıklık (işaretlenen gün oranı) ve şiddet birleştirilir.
  - Ay ya da dönem için en şüpheli paylar listesi çıkar; uzun süreli (B) vakalar ve arayüz için.

**Kaynakçasından okunacaklar** (künyeler bu makalenin kaynakçasından; doğrulanacak):
- Rizvi, B., Belatreche, A., Bouridane, A., Watson, I. (2020). Detection of stock price manipulation using kernel-based principal component analysis and multivariate density estimation. *IEEE Access*, 8, 135989–136003.
- Fabre, T., Toke, I. M. (2025). High-frequency market manipulation detection with a Markov-modulated Hawkes process. arXiv:2502.04027.

## 6. Do ve Putniņš (2023): yanıltıcı emir ve katmanlı emir tespiti

**Künye:** Do, B. L., Putniņš, T. J. (2023). Detecting Layering and Spoofing in Markets. SSRN 4525036. DOI: 10.2139/ssrn.4525036

**Okunan metin:** Do, B. L. (2023). *Machines in markets: The impacts of technology on stock valuation and trading*. Doktora tezi, University of Technology Sydney, 4. bölüm (s. 93–147). Tezin önsözüne göre bölüm, makalenin kendisidir. Klasördeki dosya: `Do_Putnins_2023_Detecting_Layering_and_Spoofing_in_Markets_tez_s118-146.pdf` (tez s. 118–146). Aşağıdaki sayfa numaraları tezin sayfalarıdır.

**Kısaca:**
- 2010–2020 arasında kovuşturulmuş 25 yanıltıcı emir vakası: ABD, İngiltere, Kanada, Japonya; çoğu vadeli işlem (Tablo 4.1).
- Vakalardan 14 ortak özellik çıkarılmış (s. 118–123). Bunların 8'i hesap kimliği olmadan, yalnız piyasa verisiyle hesaplanabiliyor; bu 8'i gösterge yapılmış (s. 126–130).
- Göstergeler defterin ilk 5 seviyesinden **her defter olayında** hesaplanıyor. Ardından 1 sn ya da 1 gün içindeki **en büyük** değer alınıyor.
- Etiket: vakalardan elle çıkarılmış 151 manipüle pay-gün ve 1.282 manipüle pay-saniye (s. 126).
- Negatif örnekler:
  - gün içinde: manipülasyon günlerindeki manipülasyonsuz saniyeler;
  - günlükte: aynı borsadaki diğer menkuller, manipülasyon günlerinde.
- Sonuçlar (örneklem dışı ROC-AUC; Tablo 4.6–4.8, Şekil 4.7–4.11):

| Düzey | Lojistik regresyon | Rastgele orman | Boosted tree | Özellik önemi (rastgele orman) |
|---|---|---|---|---|
| Gün içi (1 sn) | 0,77 | 0,81 | 0,82 | HQ 0,33, UQ 0,32, AC 0,31; diğerleri ≤ 0,015 |
| Günlük | 0,93 | 0,96 | 0,97 | TOCQ 0,42, CPDC 0,25, UQ 0,14, AC 0,13, HQ 0,06 |
| Da Vinci vakası, eğitimde yok (gün içi) | 0,85 | 0,92 | 0,92 | 0,5 eşiğinde duyarlılık 0,08 / 0,07 / 0,45 |

**Göstergeler.** Hepsi bir olay anında hesaplanıyor. A ve S, o andaki ilk 5 satış ve ilk 5 alış seviyesindeki toplam miktar. Giriş, A'nın ya da S'nin artışı; iptal, azalışı.

| Kısaltma | Ad | Tanım (aralıktaki en büyük değer) | Bizdeki karşılığı |
|---|---|---|---|
| UQ | Dengesiz kotasyon | \|A − S\| / (A + S) | `derinlik_dengesizlik`: 1 sn'lik defter örneklerinde (A − S)/(A + S) ortalaması (`tespit/pencere.py`) |
| HQ | Yoğun kotasyon | \|giriş_A − giriş_S\| / (A + S) | Yok. `yeni` emir sayısı var; taraf ayrımı ve derinliğe oran yok |
| AC | Olağan dışı iptal | \|iptal_A − iptal_S\| / (A + S) | `iptal_orani` = iptal sayısı / yeni emir sayısı; taraf ayrımı yok |
| LE | Düşük gerçekleşme olasılığı | 2–5. seviyelerde \|A − S\| / (A + S) | Yok. UQ ile korelasyonu 0,95; makalede de modelden çıkarılmış |
| TOQ | İşlem, kotasyonun tersinde | Önceki saniyede (A − S)/(A + S) > %10 ve bu saniyede "alış tarafında" işlem; ya da tersi | Yok |
| COT | İptal, işlemin tersinde | Önceki saniyede (iptal_A − iptal_S)/(A + S) > %10 ve bu saniyede "alış tarafında" işlem; ya da tersi | Yok |
| CPD | Derinlikte döngü | (A − S)/(A + S)'nin +%10'un üstünden −%10'un altına (ya da tersi) geçme sayısı | Yok |
| CPC | İptalde döngü | Aynısı, iptal dengesizliği için | Yok |

Günlük modelde iki çift toplanıyor: CPDC = CPD + CPC (korelasyon 0,80) ve TOCQ = TOQ + COT (korelasyon 0,95).

**Bizden farkı:**
- **Etiket:** onlarınki kovuşturulmuş gerçek vakalar. Bizimki motorda sentetik enjeksiyon ve SPK bültenleri.
- **Ortak yanı:** göstergeler piyasa düzeyinde, hesap kimliği yok. Bizim DataStore verimizde de yatırımcı kimliği yok (bölüm 4.2), bu yüzden kurgu doğrudan aktarılabilir.

### 6.1 Sisteme eklenebilecekler

#### E9. Do ve Putniņš göstergeleri, olay düzeyinde (öncelik: yüksek)

- **Ne:** LE dışındaki 7 gösterge iki düzeyde hesaplanır:
  - 5 dk pencere: `tespit/pencere.py`;
  - pay-gün: `tespit/ozellikler.py`, sentetik emirler için `tespit/motor_ozellikleri.py`. Pay-günde makaledeki birleşik hâller (CPDC, TOCQ) de eklenir.
- **Neden:**
  - **Kör nokta ölçüldü (26.10.2026, `rapor.md` 8).** Senaryodaki katmanlar en iyi fiyata konunca (adım 0) bütün yöntemler rastgeleye iniyor. Aynı 9 pay-günde kurallar 0,98 / %100'den 0,55 / %11'e düşüyor. Nedeni, `uzak_kisa_pay`'ın en az 3 adım uzaktaki emirleri sayması; en iyi fiyata yakın yanıltıcı emri gören bir göstergemiz yok.
  - Kovuşturulmuş gerçek vakalarla sınanmış bir gösterge setidir; günlük AUC 0,93–0,97.
  - Bizim defter göstergelerimiz katkı vermemişti (`rapor.md` 4.5). Makale aynı büyüklüğü (ilk 5 seviyede dengesizlik) farklı ölçüyor: olay anında ve aralıktaki en büyük değer. Ortalama almak, 30 sn süren bir yanıltıcı emri 5 dk'lık pencerede sulandırır.
  - Günlük düzeyde en önemli iki gösterge (TOCQ, CPDC) bizde hiç yok.
- **Veri:**
  - Enjeksiyonlu oynatmada motorun defteri her olayda elimizde (`motor/gun.py`, `Defter.derinlik(…, 5)`). Şu an yalnız 1 sn'de bir örnekleniyor (`DEFTER_ORNEK_US`).
  - Makale giriş ve iptali derinliğin artışından ve azalışından çıkarıyor; işlemle azalan derinliği de "iptal" sayıyor. Bizde olay türü belli olduğu için gerçek iptal miktarı kullanılabilir. Bu, makaleden bilinçli bir sapma olarak yazılır.
- **Uygularken karar verilecek ya da doğrulanacaklar:**
  - **"Alış tarafında işlem" makalede tanımlanmamış.** İki okuma var: pasif alış emri doluyor (işlemi satıcı başlatıyor) ya da işlemi alıcı başlatıyor. Da Vinci anlatımında manipülatörün gerçek alışları "bid tarafında" gerçekleşiyor (s. 113). Bizim senaryoda karşı emir agresif (piyasadan limite, KIE; `motor/senaryolar.py` `yaniltici_emir`, `karsi_agresif`). İki tanım da hesaplanıp denenir. [DOĞRULA]
  - **COT'ta sıra ters görünüyor.** 7. özellikte iptal işlemden sonra geliyor (s. 121). Formülde (44) ise iptal önceki saniyede, işlem bu saniyede. İki sıra da denenebilir.
  - **İlk 5 seviye yetmeyebilir.** Senaryomuzun katmanları en iyi fiyatın 4–6 adım gerisinde (`tespit/sentetik_degerlendir.py` `YANILTICI_ADIM`). Dolu bir defterde 6. adım 5. seviyenin dışında kalabilir. Seviye sayısı parametre olmalı.
  - **Maliyet.** Her olayda ilk 5 seviyeyi toplamak motoru yavaşlatabilir; bir gün zaten 17–30 dk sürüyor (`rapor.md` 3.13). Toplamlar artımlı tutulabilir.
  - **%10 eşikleri** makaleden alınır; duyarlılığa bakılır.
- **Gerçek veride yanlış alarm riski (26.10.2026 notu):**
  - E9 gerçek verideki tespiti değiştirir; normal işlemi işaretleme riski gerçektir.
  - "En iyi fiyata yakın girilip hızla iptal edilen emir" tek başına ölçüt olamaz. 10.03.2025'te piyasada hızlı iptal edilen emir miktarının %76'sı en iyi fiyattaydı. En iyi fiyata girilen miktarın %14'ü 60 sn içinde işlem görmeden iptal ediliyordu (`rapor.md` 9). Bu yüzden `uzak_kisa_pay` sınırı (3 adım) 0'a indirilmez.
  - E9 tek bir işarete değil sıraya dayanır: bir taraf şişer, karşı tarafta işlem olur, şişen taraf söner. Bu sıra payın kendi normaline göre (z-skor) ölçülür.
  - **Kabul ölçütü:** "kontrol ilk 3", yani sahte emir eklenmemiş gerçek pay-günlerin pencerelerinin günün ilk 3'üne girme oranı. Gerçek veride yanlış alarm ölçüsü budur. Bugün kurallarda ve denetimli modelde ~%5. Yakalama artsa bile bu oran belirgin yükselirse E9 alınmaz; "belirgin" eşiği kullanıcıyla belirlenecek.
  - Katmanları en iyi fiyata konmuş senaryoyla eğitilen denetimli modelde bu oran değişmedi (59'da 3, 58'de 4, 49'da 3 pay-gün; `rapor.md` 8). Bunun nedeni, bugünkü özelliklerin bu türü hiç görmemesi; E9 özellikleri eklenince yeniden ölçülür.
  - Gerçek verideki ikinci sınama: SPK etiketli günlerin üst sıralara çıkıp çıkmadığı (`tespit/spk_pencere.py`, 12 aylık veriyle).

#### E10. Döngüsel yanıltıcı emir senaryosu, Da Vinci kalıbı (öncelik: orta)

- **Makaledeki vaka:** FCA v. Da Vinci Invest; Admiral Group, LSE, 18.03.2011, 14:35–15:08 (s. 108–117; klasördeki PDF'te bu sayfalar yok).
  - **Alış aşaması:** en iyi satışta 79 lot varken o fiyata 14.520 lot sahte satış giriliyor, 3 sn sonra 17.500 lot daha. Başkaları önüne geçtikçe sahte emirler 2. seviyeye itiliyor.
  - Fiyat düşüyor. Manipülatörün gerçek alışı 21 sn sonra gerçekleşiyor. Sahte emirlerin bir kısmı iptal edilip yeniden giriliyor. Aşama yaklaşık 80 sn sürüyor.
  - **Satış aşaması:** birkaç dakika sonra (metne göre ~5 dk) aynı kalıp alış tarafında kuruluyor ve biriken pay satılıyor.
  - Döngü gün içinde birçok kez tekrarlanıyor ("testere dişi"); bazı vakalarda bir dakikadan kısa sürüyor (s. 105).
- **Bizde neden yok:**
  - Yanıltıcı emir senaryomuz tek taraflı ve tek seferlik: en iyi fiyatın 4–6 adım gerisinde 3 katman, 30 sn, arada küçük agresif karşı emir (`motor/senaryolar.py` `yaniltici_emir`, `tespit/sentetik_degerlendir.py`).
  - Makaleye göre sahte emirler çoğunlukla en iyi fiyatta ya da hemen gerisinde, sıranın arkasında duruyor ve gerçekleşme yaklaşınca iptal edilip yeniden giriliyor (s. 100).
  - Günlük düzeyde en güçlü iki gösterge (TOCQ, CPDC) döngüye dayanıyor. E9'u adil sınamak için bu senaryo gerekir.
  - Ölçümde (`rapor.md` 8) katmanlar en iyi fiyata konunca 20 vakanın 10'unda katmanlar doldu ve vaka dışarıda kaldı. Gerçekleşme yaklaşınca iptal edip yeniden girme olmadan en iyi fiyattaki sahte emir sınanamıyor.
- **Eklenecek:**
  - `motor/senaryolar.py`'ye `dongusel_yaniltici`: K döngü, her döngüde yön değişir.
  - Her aşamada en iyi fiyata ya da bir adım gerisine büyük sahte emir; karşı tarafta pasif gerçek emir. Gerçek emir dolunca ya da süre bitince sahte emirler iptal edilir.
  - Parametreler: döngü sayısı, aşama süresi, aşamalar arası bekleme, sahte miktarın en iyi seviyedeki miktara oranı.
- **E1 ile ilişkisi:** E1 tek seferlik ve hızlı, E10 tekrarlı. E1'in "en iyi fiyata büyük miktar" çeşidi E10'un tek bir aşamasıdır; ikisi aynı fonksiyonla kurulabilir.

#### E11. Karışık katman uzaklığı (öncelik: yüksek; kullanıcı önerisi, 26.10.2026)

- **Ne:** yanıltıcı emir senaryosunda katman uzaklığı (`YANILTICI_ADIM`) sabit 4 yerine her vakada rastgele seçilir, örneğin 0–6 adım. Sonuçlar tek sayı olarak değil, uzaklık bandına göre ayrı raporlanır (0–2 ve 3+).
- **Neden:**
  - Sabit 4–6 adım, senaryoyu göstergenin (`uzak_kisa_pay`, 3+ adım) tam baktığı yere koyuyor ve başarıyı şişiriyor (`rapor.md` 8).
  - Kullanıcının gözlemi: Borsa İstanbul'da tahtacılar sahte emri genelde ilk kademelere koymaz. Yabancı vakalarda ise en iyi fiyatta ya da hemen gerisinde (M6).
  - SPK vakalarında ölçüldü (`rapor.md` 9); veri tek yönü desteklemiyor. ENSRI'de büyük kısa ömürlü emirlerde uzak kademede zayıf artış var; VKFYO'da hem yakın hem uzak kademede artış var. İki vaka da B seviyesinde.
- **Uzaklık dağılımı:** veriden kesin bir dağılım çıkmadı. Başlangıç için 0–6 arasında eşit dağılım alınıp kararı kullanıcı verir. KRGYO ve TDGYO (A) verisi gelince yeniden ölçülür.
- **Gerçek veride tespiti değiştirmez.** Yalnız sentetik değerlendirmedeki sahte emrin yerini değiştirir; tespit kuralları ve model girdileri aynı kalır. Etkisi ölçümün dürüstleşmesidir: yakın bandın başarısı düşük çıkacaktır (`rapor.md` 8: en iyi fiyatta ROC-AUC 0,52–0,57). Bu yüzden riski yoktur. Yakın bandı yakalamak E9'a bağlıdır; yanlış alarm riski oradadır.
- **Dikkat:** en iyi fiyata yakın katmanlar sık doluyor (adım 0'da 20 vakanın 10'u). E10'daki "iptal edip yeniden girme" olmadan yakın bant az vakayla ölçülür.
- **İş:** `tespit/sentetik_degerlendir.py` `senaryo_olaylari` (uzaklığın vaka başına seçimi), değerlendirme çıktısına uzaklık sütunu; `pencere_degerlendir.py` ve `denetimli.py` sonuçlarında bant kırılımı.

### 6.2 Eklenmeyecekler ve nedeni

- **Hesap kimliği gerektiren özellikler:** envanter dönüşü (5), gizli ve görünür emir dengesizliği (8), envanter ve işlem niyeti (9, 10), envanterde döngü (13). DataStore'da yatırımcı ya da hesap kimliği yok (bölüm 4.2). Makale de bunları hesaplayamamış (s. 126).
- **Orta fiyatta döngü (14):** makale de gösterge yapmamış. Fiyat tarafındaki karşılığı E2'dir.

### 6.3 Kaynak olarak kullanılacağı yerler

| Konu | Tezdeki yer | Kullanılacağı yer |
|---|---|---|
| Yanıltıcı emir ve katmanlı emir tanımı; Dodd-Frank 747, AB MAR md. 12 | 4.2 (s. 98–100) | ANLATIM 1.9; vize raporu literatür (manipülasyon türleri) |
| Sahte emirler en iyi fiyatta ya da hemen gerisinde, sıranın arkasında durur; gerçekleşme yaklaşınca iptal edilir ya da yeniden girilir | s. 100 | Yanıltıcı emir senaryosunun gerekçesi; E10 |
| Kovuşturulmuş 25 vaka ve 14 ortak özellik | Tablo 4.1, 4.2 (s. 102–103, 124–125) | Vize raporu literatür; VI-104.1 bent b göstergelerinin gerekçesi |
| Yalnız piyasa verisiyle 8 gösterge; günlük AUC 0,93–0,97 | 4.4–4.5 (s. 126–146) | Vize raporu literatür (emir düzeyinde tespit); E9 |
| Yüksek frekanslı işlemcilerin iptal oranı meşru nedenlerle de yüksektir; günlük iptal göstergesi diğerlerinin üstüne katkı vermiyor | s. 137 (Khomyn ve Putniņš 2021'e atıfla) | İptal oranı kuralının (bent a/b) yanlış alarm kaynağı; sınırlar |

### 6.4 Atıf yaparken dikkat

- **Hakemsiz.** SSRN ön baskısı ve doktora tezi bölümü; dergide yayımlanmış bir sürümü bulunamadı (26.10.2026).
- **Gün içi kanıt vadeli işlem ağırlıklı.** Gün içi örneklemde yalnız CBOE, COMEX, IOM ve NYMEX var (Tablo 4.4). Pay piyasası (LSE) yalnız günlük örneklemde.
- **Doğruluk yanıltıcı.** Da Vinci sınamasında doğruluk %97–98, ama 0,5 eşiğinde manipüle saniyelerin yalnız %7–45'i yakalanıyor (Tablo 4.8). Bunun nedeni sınıf dengesizliği. Aktarılacaksa AUC ve duyarlılık birlikte verilir.
- **Sayılar tutarsız.**
  - Metinde 151 pay-gün ve 1.282 pay-saniye var. Tablo 4.3'te 167, Tablo 4.4'te 1.959 manipüle gözlem.
  - Metin gün içi ağaç modellerinin AUC'sini ters sırayla veriyor. Şekil 4.7'de rastgele orman 0,81, boosted tree 0,82.
- **Doğrulama yöntemleri farklı.** Metne göre lojistik regresyon birini dışarıda bırakarak, ağaç modelleri 3 katlı çapraz doğrulamayla ölçülmüş. Şekiller ise üçü için de k katlı diyor.

### 6.5 Kaynakçasından okunacaklar

| Künye | Kullanım |
|---|---|
| Khomyn, M., Putniņš, T. J. (2021). Algos gone wild: What drives the extreme order cancellation rates in modern markets? *Journal of Banking and Finance*, 129. | İptal oranının meşru nedenleri; iptal oranı göstergemizin yanlış alarmları |
| Cartea, Á., Jaimungal, S., Wang, Y. (2020). Spoofing and price manipulation in order-driven markets. *Applied Mathematical Finance*, 27, 67–98. | Yanıltıcı emrin kuramsal modeli; senaryo parametreleri |
| Williams, B., Skrzypacz, A. (2021). Spoofing in equilibrium. SSRN 3742327. | Yanıltıcı emir en çok orta likiditeli piyasalarda; pay seçimi |
| Wang, Y.-Y. (2019). Strategic spoofing order trading by different types of investors in the futures markets. *Journal of Financial Studies*, 27, 65–103. | Tayvan vadeli işlem piyasasında yanıltıcı emrin etkileri |
| Lee, E. J., Eom, K. S., Park, K. S. (2013). Bölüm 1.4'te. | Kore borsasında yanıltıcı emir |

## 7. Rapora eklenecekler (vize raporu)

İncelenen makalelerden vize raporuna girecekler. Rapor henüz yazılmadı; sıra ve metin kullanıcıyla yeniden değerlendirilecek. "Okunacak" işaretli kaynaklar, asılları okunmadan rapora girmez.

### 7.1 Literatür bölümünün yapısı

| Alt başlık | Söylenecek | Kaynaklar | Durum |
|---|---|---|---|
| Manipülasyonun tanımı ve türleri | Bilgiye, eyleme ve işleme dayalı manipülasyon; işleme dayalı türler: yanıltıcı emir (spoofing, layering), fiyat yükseltme (ramping), kapanışı etkileme, karşılıklı işlem | Allen ve Gale 1992; Putniņš 2012; Cao vd. 2015 | Cao okundu; diğerleri okunacak |
| Günlük veriyle tespit | Getiri, hacim ve oynaklık sapmalarından tespit. Sınırı: meşru olaylar da sapma yaratır; emir düzeyindeki manipülasyon görünmez | Öğüt vd. 2009; Diaz vd. 2011; Uslu ve Akal 2022; Zaman vd. 2026 (karşı örnek) | Uslu-Akal, Zaman okundu; Öğüt, Diaz okunacak |
| Fiyat ve emir düzeyinde tespit | Fiyat serisindeki kısa süreli şekiller; emir defteri verisiyle denetimsiz ve derin öğrenme | Cao vd. 2015; Leangarun vd. 2021; Do ve Putniņš 2023 | Cao, Do-Putniņš okundu; Leangarun okunacak |
| Etiket sorunu ve sentetik enjeksiyon | Gerçek etiket az; değerlendirme yapay kalıp ekleyerek yapılıyor | Cao vd. 2015; Golmohammadi ve Zaiane 2015; Solak vd. 2026 | Cao okundu; diğerleri okunacak |
| Kapanış manipülasyonu | Kapanış fiyatlarının yaklaşık %1'i manipüle, çok azı yakalanıyor (özetten); gözetim kuralı: kapanış − 15 dk, %99 dilim | Comerton-Forde ve Putniņš 2014; Aitken vd. 2009 (Cao vd. 2015 üzerinden) | Okunacak |
| Borsa İstanbul | Makine öğrenmesi çalışmalarının çoğu fiyat ya da yön tahmini; manipülasyon tespiti az ve günlük veriyle | Kara vd. 2011; Gündüz vd. 2017; Öğüt vd. 2009; Aktaş ve Doğanay 2006; Uslu ve Akal 2022 | Gündüz, Uslu-Akal okundu; diğerleri okunacak |
| Tekrar oynatma ve simülasyon | Tekrar oynatmada piyasa sentetik emirlere tepki vermez; limit emrin fiyat etkisi | Balch vd. 2019; Hautsch ve Huang 2012 | Okunacak |

### 7.2 Taslak paragraf: literatürdeki boşluk ve katkı

> Borsa İstanbul verisiyle yapılan makine öğrenmesi çalışmalarının büyük kısmı fiyat ya da yön tahminine yöneliktir (Kara vd., 2011; Gündüz vd., 2017). Manipülasyon tespitine yönelik çalışmalar ise SPK'nın tespit ettiği vakaları gün sonu verisiyle incelemektedir (Öğüt vd., 2009; Uslu ve Akal, 2022). Gerçek etiketlerin az olması nedeniyle uluslararası çalışmalarda değerlendirme çoğunlukla fiyat serisine eklenen yapay kalıplarla yapılmaktadır (Cao vd., 2015; Golmohammadi ve Zaiane, 2015). Cao vd. (2015), gelecek çalışma olarak fiyat serisinin emir bilgisiyle birlikte modellenmesini önermektedir. Bu çalışma, Borsa İstanbul gün içi emir verisini Pay Piyasası kurallarına uygun bir eşleştirme motorunda tekrar oynatmakta, sentetik manipülasyonu emir düzeyinde enjekte etmekte ve tespiti hem bu sentetik vakalarla hem SPK vakalarıyla değerlendirmektedir. İncelenen çalışmalar arasında bu yaklaşımı izleyen bir çalışmaya rastlanmamıştır.

### 7.3 Yöntem bölümüne eklenecek gerekçeler

| Kararımız | Gerekçe | Kaynak |
|---|---|---|
| Sentetik enjeksiyonla değerlendirme | Gerçek etiket az; endüstride kabul gören yol | Cao vd. 2015 (V-A); Golmohammadi ve Zaiane 2015 (okunacak) |
| Enjeksiyonun emir düzeyinde ve motorda yapılması | Fiyat serisine kalıp çizmek emir defterini ve eşleştirmeyi yok sayar | Cao vd. 2015 ile karşıtlık (bölüm 1.2) |
| Emir verisi kullanımı | Yanıltıcı emir iptal edilen emirle yapılır; günlük veride görünmez | Cao vd. 2015 (gelecek iş); Do ve Putniņš 2023 (gerçek vakalarda bütün göstergeler emir defterinden); Leangarun vd. 2016 (okunacak); Zaman vd. 2026 (karşı örnek) |
| Kesitsel karşılaştırma | Meşru olaylar (haber, endeks hareketi) da günlük sapma yaratır; pay benzerleriyle karşılaştırılmalı | Cao vd. 2015 (II-B); Kim ve Sohn 2012 (okunacak) |
| \|z\| ≥ 3 eşiği | Endüstride uçtaki %1 aykırı sayılıyor | Cao vd. 2015 (IV); Aitken vd. 2009 |
| Kapanış göstergesi (`kapanis_oncesi_getiri`) | Gözetimde kullanılan kapanış kuralıyla aynı fikir | Aitken vd. 2009 (Cao vd. 2015 üzerinden) |
| SPK bültenlerinden etiket | Aynı kaynağı kullanan hakemli öncül var | Uslu ve Akal 2022 |
| Negatif örnek: bütün diğer pay-günler | Aynı payın öncesi ve sonrasıyla karşılaştırmak işi kolaylaştırır, piyasa genelini ölçmez | Uslu ve Akal 2022 ile karşıtlık (bölüm 4.4) |
| Özsermaye günleri dışarıda; yalnız pay pazarları | Bölünme, bedelsiz ve hisse dışı araçlar yanlış alarm üretir | Zaman vd. 2026 (karşı örnek) |

### 7.4 Sınırlar bölümüne eklenecekler

- **Gerçek akış dışsaldır** (ANLATIM 5.1): sentetik emir başkalarını etkilemez. En iyi alışın 5 bp üstüne konan bir emir en iyi alışı ortalama 5,95 bp daha yükseltiyor (Hautsch ve Huang 2012, Cao vd. üzerinden). Tekrar oynatma ile etkileşimli simülasyon ayrımı için Balch vd. 2019 (okunacak).
- **Etiketsiz gün negatif değildir** (ANLATIM 6.14): Cao vd. 2015'in "temiz" test verisinde bile şüpheli salınım var (Şekil 13). Comerton-Forde ve Putniņš 2014'e göre kapanışların yaklaşık %1'i manipüle ve çok azı yakalanıyor (özetten; okunacak).
- **Hızlı yanıltıcı emir türü kapsanmıyor:** en iyi fiyatı iyileştirip milisaniyelerde iptal edilen emir. E1 yapılmazsa bu sınır olarak yazılır.
- **En iyi fiyata yakın yanıltıcı emir yakalanmıyor (ölçüldü):** sahte emirler en iyi fiyattayken yöntemler rastgeleye iniyor (ROC-AUC 0,52–0,57; `rapor.md` 8). Raporlanan 0,95 yalnız derin katmanlı tür içindir. E9 yapılmazsa bu sınır olarak yazılır.
- **Döngüsel yanıltıcı emir kapsanmıyor:** Do ve Putniņš 2023'ün Tablo 4.2'sindeki 25 vakanın 13'ünde kalıp gün içinde iki taraflı olarak tekrarlanıyor; kalanında bilgi yok. Senaryomuz tek seferlik; E10 yapılmazsa bu sınır olarak yazılır.
- **Hesap kimliği yok:** yanıltıcı emir özelliklerinin bir kısmı (envanter, işlem niyeti) hesap düzeyinde veri ister. Göstergelerimiz piyasa düzeyindedir. Do ve Putniņš 2023 de aynı sınırla çalışıyor (tez s. 126).

### 7.5 Sonuçlar bölümü için

- Uslu ve Akal'ın %91 F1'i bizim AUC değerlerimizle doğrudan karşılaştırılmaz: kurguları aynı payın öncesi ve sonrasıyla karşılaştırmaya ve test kümesinde model seçimine dayanır. E4 yapılırsa iki kurgu yan yana verilir.
- E5 yapılırsa vaka zaman çizelgesi şekli sonuçlara girer.

### 7.6 Sunumda sorulabilecek sorular (ANLATIM 12'ye eklenebilir)

| Soru | Cevabın özü |
|---|---|
| Literatürde benzeri var mı? | Borsa İstanbul'da SPK vakalarıyla yapılan çalışmalar gün sonu verisi kullanıyor (Öğüt vd. 2009; Uslu ve Akal 2022). Yurt dışında fiyat ya da emir defteriyle çalışanlar fiyat serisine yapay kalıp ekliyor (Cao vd. 2015). Emir düzeyinde, kurallara uygun motorda enjeksiyon yapan çalışmaya rastlamadık |
| Uslu ve Akal %91 F1 almış; sizin SPK sonuçlarınız neden daha düşük? | Onlar SPK dönemini aynı payın hemen öncesi ve sonrasıyla karşılaştırıyor ve en iyi modeli test sonucuna bakarak seçiyor. En önemli özellikleri fiyat düzeyi; yani model hangi dönemde olduğunu öğreniyor. Biz bütün paylar arasında sıralıyoruz; bu gözetimdeki gerçek soru ve çok daha zor |
| Neden günlük veri yetmez? | Yanıltıcı emir, girilip iptal edilen emirlerle yapılır; günlük özette iz bırakmaz. Günlük veriyle "spoofing" bulduğunu söyleyen çalışmalar aslında yalnız hacim artışını ölçüyor (Zaman vd. 2026) |
| Neden fiyat serisine kalıp eklemediniz? | Fiyat çizgisine çizilen kalıp emir defterini, eşleştirmeyi ve borsa kurallarını yok sayar. Bizde sentetik emirler kurallarla doğrulanıp gerçek emirlerle eşleşir; iz motorun çıktısından ölçülür |

### 7.7 Rapora girmeden önce yapılacaklar

1. **Okunacaklar (öncelik sırasıyla):**
   1. Solak vd. 2026 (E7 ve enjeksiyon);
   2. Comerton-Forde ve Putniņš 2014;
   3. Kim ve Sohn 2012;
   4. Öğüt vd. 2009;
   5. Golmohammadi ve Zaiane 2015;
   6. Balch vd. 2019;
   7. Aktaş ve Doğanay 2006.

   Do ve Putniņš 2023 okundu (bölüm 6).
2. **İkincil aktarılan sayılar asıllarından doğrulanacak:** Hautsch ve Huang 5,95 bp; Smarts %99 kuralı; Leangarun 2016 spoofing sonucu.
3. **Açık `[DOĞRULA]`:** Gündüz vd. 2017 kurultay adı, sayfa ve DOI (bölüm 3).
4. **Öneri formuyla ilgili:** `rapor.md` 3.2–3.3 hâlâ yanlış öneri formunu anlatıyor; vize raporu yazılmadan önce düzeltilmeli.
