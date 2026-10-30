# Hisseye göre ayarlı sentetik manipülasyon: tasarım

Durum: **uygulandı (29.10.2026), deneme aşamasında.** Uygulama kararı (kullanıcı, 29.10.2026): önerilen aralıklarla uygulanır; önce Mart'ta 40 seçimlik yanıltıcı emir denemesi, sonra 13 ayda eski senaryoyla yan yana. Aralıklardaki `[DOĞRULA]` işaretleri sonuçlar görüldükten sonra yeniden değerlendirilir. Kod: `tespit/pay_profili.py`, `tespit/ayarli_senaryo.py`, `motor/senaryolar.py` (ayarlı üreticiler), `tespit/pencere_degerlendir.py` (`SENARYO_SURUM=yeni`), `tespit/kor_nokta.py`, `tespit/denetimli.py` (`GRUP=pay`). İlgili: `Literatür Araştırması/eklenebilecekler.md` E10 ve E11, `rapor.md` 8–9, `TASARIM.md` 5. Onaylanırsa `TASARIM.md` 5 bu dosyaya göre güncellenir.

## 1. Sorun ve amaç

Bugünkü senaryolar sabit kalıptır (`motor/senaryolar.py`, `tespit/sentetik_degerlendir.py`):

| Senaryo | Bugünkü kalıp |
|---|---|
| Yanıltıcı emir | 3 katman, en iyi fiyatın 4, 5, 6 adım gerisi, her biri H × %2; 15. sn'de karşı tarafta H × %0,2 piyasadan limite KİE; 30. sn'de üç katman birlikte iptal |
| Fiyat yükseltme | 10 agresif alış (piyasadan limite KİE), 20 sn arayla, her biri H × %0,5 |
| Karşılıklı işlem | 10 tekrar, 60 sn arayla, her biri H × %0,5, makasın içinden |
| Kapanış etkileme | Kapanış eşleştirmesinden 10 sn önce, H × %3, son işlem fiyatının ±%3 bant ucundan |

H: payın o günkü toplam işlem miktarı (lot).

Sorun: sabit değerler dedektörün eşiklerinin içine düşüyor. Katmanlar 4. adımdan başlıyor, `uzak_kisa_pay` ise 3 adım ve ötesini sayıyor. Ölçüldü: katmanlar en iyi fiyata konunca yanıltıcı emir başarısı 0,95'ten 0,55'e iniyor (`rapor.md` 8). Gerçek vakalarda ise sahte emrin yeri tek bir değer değil (`rapor.md` 9).

Amaç:

1. Sahte emir, o hissede olağan görünen yere ve boya konur. Gerçek manipülatör de böyle yapar.
2. Parametreler dedektörden bağımsız aralıklardan çekilir; aralıklar dedektörün eşiklerinin iki yanını da kapsar.
3. Sonuç tek bir sayı değil, parametre bandına göre bir kör nokta haritasıdır.

## 2. Neden öğrenen bir üretici model değil

SPK etiketlerinden manipülasyon türlerini öğrenip sahte manipülasyon üreten bir model bu veriyle kurulamaz:

- **Örnek çok az.** 13 aylık veri döneminde etiketli 27 pay var: 4'ü A seviyesinde (ALKLC, EUREN, KRGYO, TDGYO), 24'ü B seviyesinde (KRGYO ikisinde de). B'de türü belli olan yalnız 5 pay var (BAKAB, EKSUN, ENSRI, KUYAS, VKFYO) ve her biri birkaç türü birden içeriyor. 15 B payında yalnız "işlem bazlı piyasa dolandırıcılığı" yazıyor, 4'ü bilgi bazlı (`veri/etiketler/vaka.csv`). Bir türü öğrenmek için yüzlerce örnek gerekir. Model bu birkaç hisseyi ezberler.
- **Etiket gün düzeyinde, emir düzeyinde değil.** SPK hangi emirlerin sahte olduğunu söylemez. DataStore'da üye ya da hesap bilgisi yok, manipülatörün emirleri ayrılamıyor. Model manipülasyonu değil, o hissenin o dönemdeki bütün gününü öğrenir. B'de 20 günlük pencere de bir varsayımdır.
- **Döngüsellik.** Üretici, gerçekçiliği bizim göstergelerimize bakarak öğrenir. Ürettiği şey dedektörün zaten gördüğüne benzer; 4-5-6 sorununun otomatikleşmiş hâli olur. Üretilenin gerçekçiliğini sınamak için kenara ayrılmış gerçek vaka da yok.

Normal piyasayı üretmek zaten gerekmiyor: gerçek emir akışı tekrar oynatılıyor. Üretilecek olan yalnız manipülatörün birkaç emri; bunun için hisseye göre ayarlanan birkaç parametre yeter.

## 3. İlkeler

1. **Zemin gerçek emir akışıdır.** Motor değişmez; yalnız sentetik olay listesi değişir.
2. **Hisseye göre ayar, yalnız geçmişten.** Boy, uzaklık, makas ve derinlik payın kendi verisinden alınır: önceki 5 işlem günü (Z-skorun `GECMIS_EN_AZ = 5` kuralıyla aynı) ya da aynı günün enjeksiyon anından önceki kısmı. Tek istisna 5.1'deki iptal planıdır (gerekçesi orada).
3. **Dedektörden bağımsızlık.** Aralıklar dedektör eşiklerinin (3 adım, 60 sn, z ≥ 3) iki yanını kapsar. Parametre seçilirken dedektör çıktısına bakılmaz.
4. **Tabakalı örnekleme.** Her bantta yeterli vaka olsun diye bantlar eşit sayıda çekilir. Genel sonuç iki biçimde verilir: eşit ağırlıklı ve gerçekçi ağırlıklı.
5. **SPK etiketleri parametre seçmek için kullanılmaz.** Yalnız bant ağırlıklarının kaba kontrolünde kullanılır. SPK günleri dedektörün ayrı sınavıdır.
6. **Her parametre kayda yazılır** (`sentetik_kayit.csv` ve pencere kaydı). Sonuçlar sonradan parametreye göre ayrılabilir.

## 4. Pay profili

Her seçilen pay-gün için enjeksiyondan önce hesaplanır:

| Ölçü | Kaynak | Zaman aralığı | Kullanıldığı senaryo |
|---|---|---|---|
| Yeni limit emir boyu yüzdelikleri (%50, %90, %99, en büyük) | Emir dosyası (`veri.pay_gun_emirleri`), sürekli işlem | Önceki 5 işlem günü | Yanıltıcı (katman, karşı emir) |
| Büyük emirlerin (≥ %90 yüzdelik) en iyi fiyata uzaklık dağılımı, adım cinsinden | Emir dosyası; satırdaki en iyi fiyat (`rapor.md` 9 tanımı, `veri/araclar/yaniltici_yerlesim.py`) | Önceki 5 işlem günü | Yanıltıcı (bant içi uzaklık) |
| İşlem boyu yüzdelikleri | İşlem dosyası | Önceki 5 işlem günü | Karşılıklı işlem |
| Kapanış emir toplamadaki günlük yeni emir miktarı | Emir dosyası | Önceki 5 işlem günü | Kapanış etkileme |
| Makas (adım), ilk 5 kademe derinliği | Taban oynatmanın defter örnekleri (`Gun.defter_ornekleri`, 1 sn) | Aynı gün, enjeksiyondan önceki 30 dk | Yükseltme, karşılıklı, yanıltıcı |
| Fiyat adımı, fiyat marjı | Motor (`tablo`, `parametreler`) | Enjeksiyon anı | Hepsi |
| Piyasa değeri çeyreği, sektör | Değerleme oranları (`veri/degerleme-orani/`) | Önceki ay sonu | Raporlama |
| Piyasa ve sektör hareketi (5 dk getiri, oynaklık) | Gün içi endeks (`veri/gun-ici-endeks/`) | Enjeksiyon pencereleri | Raporlama, yükseltme etkisi |

- **Yedek:** Önceki 5 günde 50'den az yeni limit emir varsa aynı günün senaryo başlangıcından önceki satırları eklenir (`profil_yedek = 1`). O da yetmezse eski H tabanlı boylar kullanılır (`profil_yedek = 2`). Uygulamada "aynı pazarın ortancası" yerine bu yol seçildi; pazar ortancası için bütün payların profili gerekirdi.
- **Maliyet:** Tek pay okuma filtreli ve hızlıdır. Seçim başına birkaç saniye eklenir.

## 5. Senaryolar: bugün ve yeni

Dayanak etiketleri:

- **[veri]**: payın kendi verisi;
- **[literatür]**: Do ve Putniņš (2023);
- **[SPK]**: `rapor.md` 9 ölçümü;
- **[varsayım]**: kaynak yok, kullanıcı onayı gerekir.

### 5.1 Yanıltıcı emir (E11 + E10)

| Parametre | Bugün | Yeni | Dayanak |
|---|---|---|---|
| İlk katmanın uzaklığı | 4 adım | Bant {0, 1–2, 3–6, 7–10}, eşit sayıda; bant içinde payın büyük emir uzaklık dağılımından (bantta gözlem yoksa düzgün) | [SPK], [literatür]; üst sınır 10 [varsayım] |
| Katman sayısı | 3 | 1–5, ardışık kademeler | [varsayım]; SPK "farklı fiyat kademeleri" diyor, sayı vermiyor |
| Katman boyu | H × %2 | Her katman ayrı çekilir: payın %90 yüzdeliği ile en büyük emri arası | [veri] |
| Ömür (döngü başına) | 30 sn | Log-düzgün 5–300 sn | [varsayım]; 60 sn eşiğinin iki yanı |
| Yaklaşınca iptal | Yok | Aynı tarafın en iyi fiyatı katmana 1 adım kalınca iptal; yeni en iyi fiyata göre aynı uzaklıktan yeniden giriş | [literatür] s. 100 |
| Döngü | 1 | 1–5 döngü; aralar 1–10 dk; her döngüde %50 olasılıkla yön değişir | [literatür] (25 vakanın 13'ünde iki taraflı tekrar); olasılıklar [varsayım] |
| Karşı emir | H × %0,2, 15. sn | Boy payın %50–%90 yüzdelik aralığından; döngü ömrünün ortasında; piyasadan limite KİE | [veri] |
| Saat | 10:30–17:00 | Aynı | — |

**Yaklaşınca iptalin planlanması.** Motor sahte emre tepki vermez; gerçek emir akışı aynen oynatılır. Bu yüzden bir katmanın hangi anda işlem göreceği enjeksiyonlu koşunun kendisinden kesin olarak bilinir (uygulamada 1 sn'lik defter örneği yerine bu yol seçildi, 29.10.2026). Plan şöyle kurulur, motor değişmez (`calistir(olaylar)`):

1. Katmanlar girilir, enjeksiyonlu koşu çalıştırılır.
2. İşlem gören her katman parçası, ilk işlem anından `TEPKI_SN` (1 sn, [varsayım]) önce iptal edilecek şekilde kısaltılır.
3. Parça, `BEKLEME_SN` (1–5 sn, [varsayım]) sonra o anki en iyi fiyata göre aynı uzaklıktan yeniden girilir (`motor/senaryolar.py` `bolum_bol`).
4. Koşu tekrarlanır; en çok `PLAN_TUR` (5) kez.

Bu, hızlı tepki veren manipülatörün yaklaşığıdır.

Planın sınırları:

- Plan bir sonraki dolumu ancak bir sonraki turda görür; 5 turdan sonra kalan dolum olabilir.
- Bu yüzden `katman_dolan` ölçülmeye ve %1 temizlik ölçütü uygulanmaya devam eder.
- Dışarıda kalan vaka sayısı bant bazında raporlanır. Bu önemli, çünkü `rapor.md` 8'de yakın bantta dışarıda kalanlar sonucu durgun paylara kaydırmıştı.

### 5.2 Fiyat yükseltme

| Parametre | Bugün | Yeni | Dayanak |
|---|---|---|---|
| Emir sayısı | 10 | 5–30 | [varsayım] |
| Aralık | 20 sn sabit | Üstel dağılım, ortalaması 10–60 sn | [varsayım] |
| Emir türü | Piyasadan limite KİE | Piyasa emri KİE (kademeleri miktarı bitene kadar süpürür) | Duman testi: piyasadan limite emir yalnız en iyi kademede işlem görür, k > 1 boşa çıkıyordu |
| Emir boyu | H × %0,5 | Karşı tarafın ilk 5 kademe miktarı ortancasının k/5'i, yani yaklaşık k kademe; k = 1–3 | [veri] |
| Rapor ekseni | — | Gerçekleşen fiyat etkisi: senaryo sonunda enjeksiyonlu ve enjeksiyonsuz koşunun son işlem fiyatı farkı; bantlar <%1, %1–3, %3–5, >%5 | [veri] |

Tekrar oynatma tepki vermediği için iki koşunun fiyat farkı yalnız senaryonun etkisidir; piyasa ya da sektör hareketi bu farka girmez. Bu yüzden etki için endeks gerekmez (uygulamada değişti, 29.10.2026).

### 5.3 Karşılıklı işlem

| Parametre | Bugün | Yeni | Dayanak |
|---|---|---|---|
| Tekrar | 10 | 3–30 | [varsayım] |
| Aralık | 60 sn | Üstel dağılım, ortalaması 30–300 sn | [varsayım] |
| Boy | H × %0,5 | Yarı yarıya iki tür: "karışan" (payın işlem boyu %50–%90 yüzdelik aralığı) ve "göze batan" (%99 yüzdeliğin üstü) | [veri] |
| Fiyat | Makasın içi | Aynı | — |

Aktör bilgisi olmadığı için dedektör yalnız işlem kalıbını görebilir. "Karışan" türde düşük başarı beklenir; bu bir bulgudur.

### 5.4 Kapanış etkileme

| Parametre | Bugün | Yeni | Dayanak |
|---|---|---|---|
| Boy | H × %3 | Payın önceki 5 gündeki kapanış emir toplama miktarı ortancasının 0,5–3 katı (log-düzgün) | [veri] |
| Giriş anı | Eşleştirmeden 10 sn önce | Toplamanın son 0–5 dk'sında düzgün | [varsayım] |
| Fiyat | Son işlem ±%3 bant ucu | Aynı (kapanışta aday fiyatlar son işlemin ±%3'üyle sınırlı, `03-tek-fiyat.md`) | — |

## 6. Yeni veriler: nerede işe yarar, nerede yaramaz

### Gün içi endeks

- **Senaryo raporlaması:** Enjeksiyon penceresinde XUTUM'un ve sektör endeksinin 5 dk getirisi ve oynaklığı hesaplanır. Bunlarla "sakin / hareketli piyasa" bandı kurulur. Sorulan soru: dedektör, bütün piyasa hareket ederken mi zorlanıyor?
- **Tespit tarafı (ayrı karar, öneri E12):** Pencere getirisi sektör ya da piyasa endeksine göre düzeltilir. 19.03.2025 gibi bütün piyasanın düştüğü günlerde z(getiri) bütün paylarda yükselir ve bent f yanlış alarm üretir. Bu değişiklik gerçek veride tespiti değiştirir. Bu yüzden senaryo işinden ayrı yapılır; kabul ölçütü E9'daki gibidir (kontrol ilk 3, SPK pencere ROC-AUC).
- **Sektör–endeks eşlemesi gerekir:**
  - Değerleme dosyasında 44 sektör var; gün içi endekste ana sektör endeksleri dahil yaklaşık 25 sektör endeksi var.
  - Eşleme tablosu elle kurulur (`tespit/sektor_endeks.csv`); her satır gerekçeli yazılır, belirsiz satırlar `[DOĞRULA]` ile işaretlenir.
  - Karşılığı olmayan sektör XUTUM'a düşer. XU100'e düşmez, çünkü küçük payların çoğu XU100'de değil.

### Değerleme oranları

- **Raporlama:** Sonuçlar piyasa değeri çeyreğine göre ayrılır (önceki ay sonu).
- **Aday seçimi değişmez:** SPK etiketli 27 pay küçük paylarda belirgin biçimde yoğunlaşmıyor. Payların aylık piyasa değeri yüzdeliklerinin ortancası 0,46; %56'sı ortanın altında, %22'si alt çeyrekte (ölçüm 29.10.2026, 2024-05…2025-06 değerleme dosyaları). Seçimi küçük paylara kaydırmanın veride dayanağı yok.
- **Model girdisi olmaz:** Sektör ve piyasa değeri denetimli modele ham özellik olarak verilmez. Etiketler pay bazında olduğundan model payı ezberler (`DURUM.md`, değerleme notu).
- **F/K, PD/DD kullanılmaz:** Manipülasyonla ilişkilerine dair ne veri ne kaynak var.

## 7. Değerlendirme

- **Örneklem ve süre:**
  - Pencere değerlendirmesi seçim başına yaklaşık 4,5 sn sürüyor (200 seçim 15 dk, `rapor.md` 10.8); profil okuma birkaç saniye ekler.
  - Hedef, bant başına en az 100 temiz vaka. Yanıltıcıda 4 bant × 100 = 400 vaka, dışarıda kalanlarla yaklaşık 500 seçim; diğer üç senaryoda 200'er.
  - Toplam yaklaşık 1.100 seçim, 2–3 saat (tahmin).
- **Pozitif pencere tanımı:**
  - Bugün ilk ve son sentetik olay arasındaki bütün pencereler pozitif sayılıyor. Döngülü senaryoda aradaki boş pencereler de pozitif sayılır.
  - Yeni tanım: en az bir sentetik olay içeren pencere.
  - Pozitif pencere sayısı arttıkça "ilk 3 isabeti" kolaylaşır; bu yüzden sonuç döngü sayısına göre ayrı raporlanır.
- **Kör nokta haritası:**
  - Her senaryo ve her parametre ekseni için bant bant ROC-AUC, ilk 3 isabeti ve kontrol ilk 3.
  - Yanıltıcıda ayrıca uzaklık × boy iki boyutlu tablo.
- **Genel sayı** iki biçimde verilir:
  - eşit ağırlıklı;
  - gerçekçi ağırlıklı: yanıltıcı uzaklık ağırlıkları SPK vakalarındaki kısa ömürlü büyük emir dağılımından alınır (`rapor.md` 9.2; 3 vaka, kaba, [varsayım]).
- **Denetimli model:**
  - Çapraz doğrulamada gruplama pay-gün yerine **pay** olur. Profil paya özgü olduğundan aynı payın günleri eğitimde ve testte bir arada olmamalı.
  - Genelleme sınaması (bir bandı dışarıda bırak): model örneğin 3–6 ve 7+ bantlarıyla eğitilir, 0 ve 1–2'de sınanır. Sorulan soru: model görmediği yerleşimi yakalıyor mu?
- **Eskiyle karşılaştırma:** Senaryo değiştiği için sonuçlar Mart → 5 ay → 9 ay serisiyle doğrudan karşılaştırılamaz. Eski sabit senaryo 13 ayda aynı tohumla bir kez daha koşulur ve iki sonuç yan yana verilir.

## 8. Kod değişiklikleri (onaylanırsa)

| Dosya | Değişiklik |
|---|---|
| `tespit/pay_profili.py` (yeni) | Profil hesabı: önceki 5 günün emir ve işlemleri, enjeksiyon öncesi defter; uzaklık tanımı `yaniltici_yerlesim.py` ile aynı |
| `motor/senaryolar.py` | `yaniltici_emir`: katman sayısı ve boy listesi, döngü, taban oynatmadan iptal planı; `fiyat_yukseltme` ve `karsilikli_islem`: değişken aralık ve boy; `kapanis_etkileme`: giriş anı |
| `tespit/sentetik_degerlendir.py`, `tespit/pencere_degerlendir.py` | Tabakalı parametre çekimi, kayda yazım, yeni pozitif pencere tanımı, bant raporu, eski senaryo seçeneği |
| `tespit/denetimli.py` | Pay bazında gruplama, bant dışarıda bırakma |
| `tespit/sektor_endeks.csv` (yeni) ve endeks okuyucu | Yalnız raporlama ve yükseltme etkisi için |
| `motor/testler/test_senaryolar.py` | Plan iptali taban işlemden önce mi; parametreler aralıkta mı; aynı tohumla aynı olaylar; profil yedeği |

Motorun eşleştirme kodu değişmez.

## 9. Riskler ve sınırlar

- **Gerçek veride tespit değişmez.** Bu iş yalnız ölçümü dürüstleştirir. Yakın bantta ve "karışan" boyda başarı düşük çıkacaktır (`rapor.md` 8: en iyi fiyatta 0,52–0,57). Bu bir bulgudur: vize raporunda sınır olarak yazılır ve E9 tartışmasının girdisi olur.
- **Aralıkların çoğu varsayımdır** (tabloda işaretli). Genel sayı bu aralıklara bağlıdır; bu yüzden birincil sonuç haritadır.
- **Plan gelecek bilgisini kullanır.** Taban oynatmadan planlama, manipülatörün hızlı tepkisinin yaklaşığıdır. Tekrar oynatmanın genel sınırı burada da geçerli: diğer katılımcılar sahte emre tepki vermez. Ajan simülasyonu kapsam dışıdır (22.10.2026).

## 10. Sıra

1. 13 ayın özellikleri ve birleştirme (29.10.2026'da sürüyor).
2. Pay profili ve yanıltıcı emir (E11 + E10). Önce küçük deneme: Mart, 40 seçim. Planlı iptalin çalıştığı ve doluma düşen vaka oranı görülür.
3. Diğer üç senaryo.
4. 13 ayda eski ve yeni senaryo; kör nokta haritası; `rapor.md`'de yeni bölüm.
5. Ayrı kararlar: E9 (olay anında dengesizlik), E12 (endeksle düzeltilmiş getiri).
6. SPK etiketleriyle denetimli model. Sentetik işten bağımsızdır; pay bazında gruplama kararı ikisinde ortaktır.

## Açık sorular

- [DOĞRULA] Uzaklık bantları (0 / 1–2 / 3–6 / 7–10) ve gerçekçi ağırlıklar.
- [DOĞRULA] Katman sayısı 1–5, ömür 5–300 sn, döngü 1–5, döngü arası 1–10 dk.
- [DOĞRULA] "Yaklaşınca iptal" eşiği: 1 adım.
- [DOĞRULA] Yükseltme ve karşılıklı işlem aralıkları (emir sayısı, aralık ortalaması).
- [DOĞRULA] Sektör–endeks eşlemesinin belirsiz satırları (eşleme kurulunca).
- [DOĞRULA] E12 (endeks düzeltmesi) bu işe mi dahil, ayrı mı.
