# Okunacak makaleler

Öncelik sırasına göre (25.10.2026). Seçim ölçütü: gerçek borsa verisinde (kovuşturulmuş vakalar ya da sağlam enjeksiyon, örneklem dışı sınama) manipülasyon tespitini başarıyla yapmış olmak **ve** sistemimize alınabilecek somut bir şey (gösterge, model, senaryo) vermek.

Başarı bilgileri makalelerin özetlerinden alındı; tam metin indirilince ayrıca incelenir. İncelenenlerin sisteme eklenebilecekleri `eklenebilecekler.md`'de tutulur.

**Durum:** indirilmedi → indirildi → incelendi (incelenince `eklenebilecekler.md`'ye işlenir).

## Özet

| Öncelik | Makale | Ne için | Erişim | Durum |
|---|---|---|---|---|
| 1 | Do ve Putniņš (2023), SSRN | Yeni yanıltıcı emir göstergeleri; gerçek spoofing vakaları | Ücretsiz | indirilmedi |
| 2 | Leangarun vd. (2021), IEEE Access | Otokodlayıcı adımı (form adım 8); karar eşiği | Açık erişim | indirilmedi |
| 3 | Poutré vd. (2024), J. Finance and Data Science | Otokodlayıcı; gerçek vakalardan senaryo üretme | Açık erişim | indirilmedi |
| 4 | Wang vd. (2019), Neurocomputing | Şirket özellikleri model girdisi; gün içi dizi modeli | Okul erişimi | indirilmedi |
| 5 | Ye vd. (2026), SSRN | XGBoost adımı (form adım 10); gün içi değişkenler | Ücretsiz | indirilmedi |
| 6 | Comerton-Forde ve Putniņš (2011), JFI | Kapanış göstergeleri | SSRN sürümü ücretsiz | indirilmedi |
| 7 | Kadıoğlu vd. (2015), Borsa Istanbul Review | Borsa İstanbul'da kapanış manipülasyonu ölçümü | Açık erişim | indirilmedi |
| 8 | Martínez-Miranda vd. (2019), High Frequency | İptal tahmini; "beklenen iptale göre sapma" | Wiley | indirilmedi |
| 9 | Zhai vd. (2018), RQFA | Emir özelliklerini durağanlaştırma; HMM | Springer | indirilmedi |
| 10 | Tiwari vd. (2021), IEEE Access | Derleme: hangi yöntem neyle başarılı | Açık erişim | indirilmedi |

## Birinci sıra

### 1. Do ve Putniņš (2023): yanıltıcı emir ve katmanlı emir tespiti

- **Künye:** Do, B. L., Putniņš, T. J. (2023). Detecting Layering and Spoofing in Markets. SSRN 4525036. 58 sayfa.
- **Bağlantı:** https://ssrn.com/abstract=4525036
- **Neyi başarmış:** dünya genelinde kovuşturulmuş gerçek spoofing vakaları; örneklem dışı çapraz doğrulama. Göstergeler makine öğrenmesiyle birleştirilince yüksek tespit doğruluğu.
- **Özette en iyi göstergeler:**
  - alış ve satış derinliği arasındaki dengesizlik;
  - yüksek emir yoğunluğu;
  - olağan dışı iptaller;
  - derinlikte ve iptallerde döngüsel (tekrarlayan) örüntü.
- **Sistemimize ne ekler:**
  - **Yeni göstergeler:** iptal oranı bizde var; derinlik dengesizliği ve döngüsellik yok. Motorun saniyelik defter örneklerinden (`motor/gun.py` `defter_ornekleri`) hesaplanabilir.
  - Daha önce denediğimiz defter göstergeleri katkı vermemişti (`rapor.md` 4.5). Bu makale hangi biçimde ölçüldüğünde işe yaradığını gösterir.
  - E1 (hızlı yanıltıcı emir) için de kaynak.
- **Okurken bak:** göstergelerin tam tanımı ve pencere uzunluğu; hangi model; doğruluk ve yanlış alarm oranları; vaka listesi (hangi borsalar).

### 2. Leangarun, Tangamchit, Thajchayapong (2021): Tayland borsasında derin denetimsiz öğrenme

- **Künye:** Leangarun, T., Tangamchit, P., Thajchayapong, S. (2021). Stock price manipulation detection using deep unsupervised learning: The case of Thailand. *IEEE Access*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Stock+price+manipulation+detection+using+deep+unsupervised+learning%3A+The+case+of+Thailand%22
- **Neyi başarmış:** emir defteri verisiyle otokodlayıcı ve GAN. Model yalnız normal işlemle eğitiliyor; ondan sapan davranış manipülasyon sayılıyor. Tayland borsasında kovuşturulmuş 6 gerçek vakanın 5'ini düşük yanlış alarmla yakalıyor.
- **Sistemimize ne ekler:**
  - Öneri formundaki **otokodlayıcı adımı (8)** için doğrudan tarif. Bu adım henüz yapılmadı.
  - Karar eşiği seçme yöntemi ("MinManiMax"); birleşik uyarı seviyesi (E7) için.
- **Okurken bak:** girdi olarak defterin kaç seviyesi ve hangi pencere; otokodlayıcının yapısı; eşik yöntemi; 6 vakanın türleri.

### 3. Poutré, Chételat, Morales (2024): yüksek frekanslı piyasalarda derin denetimsiz aykırılık tespiti

- **Künye:** Poutré, C., Chételat, D., Morales, M. (2024). Deep unsupervised anomaly detection in high-frequency markets. *The Journal of Finance and Data Science*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Deep+unsupervised+anomaly+detection+in+high-frequency+markets%22
- **Neyi başarmış:**
  - Emir defteri için transformer tabanlı otokodlayıcı.
  - NASDAQ'ta 5 paya gerçek vakalardan türetilmiş quote stuffing, layering ve pump & dump senaryoları ekleniyor.
  - Model paydan bağımsız; manipülasyon kalıbı bilmeden alanında en iyi sonuç.
- **Sistemimize ne ekler:**
  - Otokodlayıcı adımı için ikinci tarif.
  - **Gerçek vakalardan senaryo üretme yöntemi:** bizim enjeksiyon senaryolarımızla karşılaştırma ve eksik olan "quote stuffing" senaryosu için.
- **Okurken bak:** senaryoların parametreleri (büyüklük, süre); bizim `motor/senaryolar.py` ile farkı; modelin girdi penceresi; karşılaştırılan yöntemler.

## İkinci sıra: denetimli model

### 4. Wang, Xu, Huang, Yang (2019): RNN topluluğuyla gün içi manipülasyon tespiti

- **Künye:** Wang, Q., Xu, W., Huang, X., Yang, K. (2019). Enhancing intraday stock price manipulation detection by leveraging recurrent neural networks with ensemble learning. *Neurocomputing*, 347, 46–58.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Enhancing+intraday+stock+price+manipulation+detection+by+leveraging+recurrent+neural+networks%22
- **Neyi başarmış:** Çin'de kovuşturulmuş gerçek vakalar (CSRC). Gün içi işlem özellikleri ile şirket özellikleri birlikte kullanılıyor. Önceki yöntemlere göre AUC'de ortalama %29,8 iyileşme. 111 atıf.
- **Sistemimize ne ekler:**
  - **Şirket özelliklerini modele girdi yapmak:** pazar, BIST 100 üyeliği, piyasa yapıcı, büyüklük. Bunlar bizde var ama şu an "model girdisi değil" (`tespit/ozellikler.py` başındaki açıklama).
  - Gün içi dizilerden öğrenen bir model (RNN/GRU): denetimli adıma alternatif ya da ek.
- **Okurken bak:** hangi şirket özellikleri; negatif örnekler nasıl seçilmiş (başka paylar mı, aynı payın başka günleri mi); örneklem dışı sınama.

### 5. Ye, Ge, Yang (2026): makine öğrenmesiyle günlük manipülasyon ölçüsü

- **Künye:** Ye, W., Ge, Y., Yang, J. (2026). Measuring Daily Stock Manipulation: A Machine Learning Perspective. SSRN 6805806. 59 sayfa. Hakemsiz ön baskı.
- **Bağlantı:** https://ssrn.com/abstract=6805806
- **Neyi başarmış:** Çin'de kovuşturulmuş 159 gerçek vaka (2010–2023). Yüksek frekanslı işlem değişkenlerinden XGBoost ile günlük bir "manipülasyon yoğunluğu" puanı. Puan sürü davranışı ve momentumdan ayrışıyor; pump & dump örüntüsünü gösteriyor.
- **Sistemimize ne ekler:**
  - Formdaki **XGBoost adımının (10)** gerçek vakalarla yapılmış en yakın örneği.
  - Hangi gün içi değişkenlerin önemli çıktığını özellik listemizle karşılaştırırız.
  - Günlük puan tasarımı, pay düzeyinde şüphe puanı (E8) için.
- **Okurken bak:** değişken listesi ve önem sıralaması; etiket kurgusu; örneklem dışı sınama.

## Üçüncü sıra: kapanış manipülasyonu

### 6. Comerton-Forde ve Putniņš (2011): kapanış fiyatı manipülasyonunu ölçmek

- **Künye:** Comerton-Forde, C., Putniņš, T. J. (2011). Measuring closing price manipulation. *Journal of Financial Intermediation*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Measuring+closing+price+manipulation%22
- **Neyi başarmış:** kovuşturulmuş gerçek kapanış manipülasyonu vakalarıyla bir kapanış manipülasyonu ölçüsü kuruyor. 259 atıf.
- **Sistemimize ne ekler:** kapanış etkilemesi en zayıf senaryomuz (×1'de AUC 0,80). Makaledeki göstergeler kapanış göstergelerimize (`tespit/kapanis_ozellikleri.py`) eklenebilir.
- **Okurken bak:** ölçünün bileşenleri (kapanış getirisi, ertesi gün geri dönüş, kapanış öncesi işlem yoğunluğu gibi); ağırlıklar; vakalardaki başarı.

### 7. Kadıoğlu, Küçükkocaoğlu, Kılıç (2015): Borsa İstanbul'da kapanış manipülasyonu

- **Künye:** Kadıoğlu, E., Küçükkocaoğlu, G., Kılıç, S. (2015). Closing price manipulation in Borsa Istanbul and the impact of call auction sessions. *Borsa Istanbul Review*, 15(3), 213–221.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Closing+price+manipulation+in+Borsa+Istanbul+and+the+impact+of+call+auction+sessions%22
- **Neyi başarmış:** Borsa İstanbul'da 102 pay, 2006–2012. Kapanış müzayedesi (02.03.2012) gelmeden önce yukarı yönlü kapanış manipülasyonu bulunuyor. Makine öğrenmesi değil, ölçüm yöntemi.
- **Sistemimize ne ekler:** Borsa İstanbul'a özgü kapanış manipülasyonu ölçümü; bent d ve kapanış senaryomuz için.
- **Okurken bak:** kullanılan ölçü; kapanış müzayedesinden sonra ne değişmiş (bizim veri dönemi müzayedeli).

## Dördüncü sıra: gerekirse

### 8. Martínez-Miranda, Phelps, Howard (2019): emir iptalini tahmin etmek

- **Künye:** Martínez-Miranda, E., Phelps, S., Howard, M. J. (2019). Order flow dynamics for prediction of order cancelation and applications to detect market manipulation. *High Frequency*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Order+flow+dynamics+for+prediction+of+order+cancelation%22
- **Sistemimize ne ekler:** iptal oranı göstergemizi "beklenen iptale göre sapma" biçimine çevirmek için fikir. Olağan iptali model tahmin eder, fazlası şüpheli sayılır.

### 9. Zhai, Cao, Ding (2018): borsada manipülasyon tespitine veri analitiği yaklaşımı

- **Künye:** Zhai, J., Cao, Y., Ding, X. (2018). Data analytic approach for manipulation detection in stock market. *Review of Quantitative Finance and Accounting*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Data+analytic+approach+for+manipulation+detection+in+stock+market%22
- **Sistemimize ne ekler:** limit emirlerini durağanlığı azaltan bir dönüşümden geçirip kullanıyor; statik model ve HMM ile gerçek işlem verisinde sınanmış. Emir özelliklerimizi günler ve paylar arasında karşılaştırılabilir yapmak için fikir.

### 10. Tiwari, Ramampiaro, Langseth (2021): finansal piyasa gözetiminde makine öğrenmesi derlemesi

- **Künye:** Tiwari, S., Ramampiaro, H., Langseth, H. (2021). Machine learning in financial market surveillance: A survey. *IEEE Access*.
- **Bağlantı:** https://scholar.google.com/scholar?q=%22Machine+learning+in+financial+market+surveillance%3A+A+survey%22
- **Sistemimize ne ekler:** hangi yöntemin hangi veriyle başarılı olduğunu toplayan yol haritası; yeni makale bulmak için.

## Bilerek dışarıda bırakılanlar

- **Kripto para çalışmaları:** pump & dump, wash trading, NFT. Veri ve piyasa yapısı farklı.
- **Pekiştirmeli öğrenmeyle "spoofer nasıl davranır" modelleri ve yalnız teorik çalışmalar:** gerçek veride tespit yapmıyorlar.
- **Fiyat ya da yön tahmini çalışmaları:** manipülasyon tespiti değiller.
