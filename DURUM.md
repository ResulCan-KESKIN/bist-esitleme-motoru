# Proje durumu ve devam notu (yeni oturum için)

Son güncelleme: 25.10.2026. Bu dosya sohbet geçmişi olmadan çalışmaya devam etmek içindir. Görev tanımı: `gorev-kural-yazimi.md` (kurallar: kaynakta olmayanı ekleme, madde no sona, belirsizlik → "Açık sorular" [DOĞRULA], örnekler → "Test örnekleri", dosya adlarında Türkçe karakter yok, her oturumda tek kural dosyası, bitince [DOĞRULA] listesini göster).

## Kaldığımız yer ve yapılacaklar (24.10.2026)

**25.10.2026 eki.**
- **Öneri formu:** doğru form kökteki `Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.pdf` (eski .docx yanlıştı; ajan simülasyonu, GA/PSO ve Monte Carlo formda yok). `ANLATIM.md` 2.3–2.4 ve `ANLATIM.pdf` doğru forma göre yazıldı. `CLAUDE.md` ("Sistem kapsamı" kararı ve .docx yolu), `TASARIM.md` 1/6.3/6.5, `rapor.md` 3.2–3.3 ve bu dosyadaki öneri formu notları hâlâ eski forma dayanıyor; vize raporundan önce düzeltilecek.
- **Pencere uzunluğu karşılaştırması** (1, 5, 10, 15 dk): 5 dk en dengeli (`rapor.md` 7).
- **Literatür:** `Literatür Araştırması/` klasöründe:
  - `eklenebilecekler.md`: incelenen 5 makale, sisteme eklenebilecekler (E1–E8, hiçbiri uygulanmadı), vize raporuna girecekler (bölüm 6);
  - `makale.md`: okunacak 10 makale, öncelik sırasıyla.
  - Makale PDF'leri git dışı.

**Kaldığımız yer (24.10.2026).**
- 22.10.2026 sonundaki listeden yapılanlar:
  - fiyat yükseltme göstergesi (net agresif adım) ve 15 dakikalık pencere denemesi: senaryo bu büyüklükte ayırt edilemiyor (4.1, 4.3);
  - kapanış etkilemesi göstergeleri: ×1'de ROC-AUC 0,80, ×3'te 0,87 (4.2);
  - SPK etiketli günlerde pencere düzeyi: A'da sinyal yok, B'de zayıf (4.4);
  - defter göstergeleri: şimdilik katkı yok (4.5).
- 24.10.2026 inceleme düzeltmeleri (`rapor.md` 5): veri döneminde ölçümü olmayan parametrede motor `OlcumEksik` ile durur; yanıltıcı emir katmanları en iyi fiyata göre, karşı emir agresif, katmanı dolan vakalar değerlendirme dışı (yanıltıcı emir pencere ROC-AUC 0,95).
- 24.10.2026 sistem taraması (`rapor.md` 6): kapanış penceresi açılış müzayedesinden ayrıldı (`Gun.kapanis_ani`), Isolation Forest ve denetimli model kapanış penceresini puanlamaz, karşılıklı işlem makasın içinden (kendi emirleri arası işlem %75 → %89), ölçüm kontrolü devre kesicide yutulmuyor ve pazara göre, defter örneği 1 sn, tatil listesi 2024–2026, reddedilen vakalar değerlendirme dışı, arayüzde SPK etiketi. Bütün sentetik değerlendirmeler ve SPK pencere değerlendirmesi yeniden koşuldu.
- Sistemin sıfırdan anlatımı: `ANLATIM.md`.
- Motor, arayüz ve tespit kodları, 35 test ve belgeler güncel; commit edildi.

**Yapılacaklar (öncelik sırasıyla).**
1. **Veri indirme (kullanıcı):** yeni ayların parametreleri ölçülmeden motor çalışmaz (`OlcumEksik`). 2024-06…2025-02 (DataStore gün içi emir, gün içi işlem, gün sonu; ITCH yalnız 2025-01 ve 2025-02). Ardından her ay için parquet dönüşümü, günlük bölümleme, kayıpsızlık kontrolü (`rapor.md` 2.10). Aralık dışı dosyaların (2025-06…09) silinmesi kullanıcıdadır.
2. **Yeni aylar için tarih parametreleri:** marj, devre kesici yönü/oranı/süreleri, açığa satış kapsamı veriden yeniden ölçülür; Mart doğrulama betikleri yeni aylarda çalıştırılır.
3. **12 ay ölçeğinde çalıştırma:** toplu oynatma ve özellik hesabı; SPK değerlendirmesinin (gün ve pencere düzeyi) 12 ayla tekrarı; denetimli modelin SPK etiketleriyle sınanması. Uzun işler parça parça çalıştırılmalı.
4. **Vize raporu:** literatür bölümü (`Literatür Araştırması/eklenebilecekler.md` bölüm 6 ve `makale.md`); öneri formu farkları doğru forma göre (`ANLATIM.md` 2.4); bölüm 3 ve 4'ün vize metnine dönüştürülmesi.
5. **Kural dosyalarının kullanıcı onayı** (veriyle birlikte).
6. **Tespit iyileştirmeleri (isteğe bağlı):** fiyat yükseltme senaryosunun daha büyük ve uzun hâliyle sınanması; defter göstergelerinin daha derin seviyelerle ve olay anında örneklenmesi.
7. **Özsermaye günleri:** düzeltilmiş baz fiyat kaynağı.


**Çalıştırma notları.**
- Tek sıra-gün: `python -I motor/tekrar_oynat.py veri/gun-ici-emir/gunluk veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet GUN KOD --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet`.
- Bütün gün: `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv`.
- Özellikler: `python -I tespit/ozellikler.py GUNLUK ISLEM GUNSONU CIKTI.parquet [GUN ...]` (parça parça çalıştırılabilir); yalnız kapanış göstergelerini eklemek için `python -I tespit/kapanis_ozellikleri.py GUNLUK ISLEM OZELLIKLER.parquet`.
- Değerlendirme: `tespit/degerlendir.py`, `tespit/pencere_degerlendir.py` (`OLCEK` ortam değişkeniyle büyüklük, `PENCERE_DK` ile pencere uzunluğu), `tespit/denetimli.py`, `tespit/spk_pencere.py` (kaldığı yerden devam eder; `--degerlendir`).
- Arayüz: `streamlit run arayuz/uygulama.py`.
- Testler: `python -m pytest motor/testler tespit/testler`.

## Klasör düzeni
- `kaynaklar/` ham PDF'ler (+ `README.md`, `_kullanilmayan/` kullanılmayacak belgeler).
- `ekler/` Prosedür Ek-1…Ek-21 (kullanıcı doğrulamalı, `README.md` var).
- `kurallar/` kural dosyaları. `veri/` çeviriler, DataStore md, DataStore gün içi verisi (`veri/gun-ici-emir/`, `veri/gun-ici-islem/`, `veri/gun-sonu-fiyat-hacim/`, git dışı), ITCH örnek verisi (`veri/itch/`, git dışı), doğrulama sonuçları (`veri/gunici-dogrulama/`) ve betikler (`veri/araclar/`).
- `TASARIM.md` sistem tasarımı (sürüm 2, 21.10.2026). `rapor.md` çalışma raporu (vize raporunun kaynağı).

## Kural dosyaları
| Dosya | Durum |
|---|---|
| 01-seanslar | Yazıldı; P_SI_KAP ve P_ISL_YOK ve öğle tek fiyat farkı DOĞRULANDI. Mart 2025 verisi: bölüm adları ve saatler Ek-10 ile uyumlu, `P_GUNSONU` 18:19 (gün sonu saati kısmen kapandı), müzayede başlangıcı aşama başına ortak rastlantısal an, varant `P_SALTKOTASYON` 07.03.2025 değişikliği görüldü. `2`/EIY/PY/APY durumlarının tarihi AÇIK. |
| 02-fiyat | Yazıldı. Mart 2025: marj tüm pazarlarda ±%10 (Tablo-4 %20/%15 değil; yeni [DOĞRULA], tarih parametresi), içe yuvarlama doğrulandı, AOF kapsamı kısmen kapandı, fiyat adımı Tablo-7/8 ile sınandı. |
| 03-tek-fiyat | Yazıldı (en kritik dosya). Mart 2025 müzayedeleri yeniden kuruldu: 29.633 müzayedenin %99,96'sında fiyat tutar; Adım 4 referansı = baz fiyat, kapanışta son işlem ±%3 sınırı, dengeleyici eşleşmesi, `_EIY` kısıtı, Ek-16 3-B açıklaması kapandı. AÇIK: karışık yön (4 vaka), eşit uzaklık ve Adım 5 (veride yok), kotasyonların müzayedeye katılımı. |
| 04-surekli-islem | Yazıldı (5.2.1, 5.6.1, Ek-18 §1.2; SMP ve FIX/OUCH kaynaklı madde 34–48). Marj dışı iptal/duraklatma kararı verildi; öncelik kuralları ITCH 2018 ve Mart 2025 ile doğrulandı (fiyat %99,998; zaman %99,76: öncelik kalan miktar artışı ve kısmi görünme yenilemesinde de kaybolur; `emir_giris_zamani` öncelik zamanı değil). |
| 05-emirler | Yazıldı (143 madde); kullanıcı doğrulaması bekliyor. Ek-19 matrisi betikle üretildi. Belgeler arası çelişkiler karara bağlandı (G sütunu→Ek-19, askıya alma→iptal+yeni emir, marj dışı→tarihli iptal/gün içi duraklatma, açılışta piyasa emri→Tablo-4, emir bilgisi değişimi reddedilir). Açık: Ek-18 5.4 Örnek 2 ve 6.3 Örnek 1 tablo/metin tutarsızlıkları vb. Mart 2025: Ek-19'a aykırı yeni emir 0; piyasa emri fiilen yalnız KİE; değişiklik sebepleri (8, 9, 13, 34) anlamlandırıldı, 116/117 tabloda yok. |
| 06-devre-kesici | Yazıldı (53 madde); kullanıcı doğrulaması bekliyor. Ek-3 hareketli limit 02-fiyat'ta. Karar: pay bazında emir toplama 10 dk (5.3.4 güncel; Tablo-4 5/15/15 dk eski, süre tarihe bağlı parametre); DK eşleştirmesi sabit saatte, EBDKS rastlantısal. Açık: marj mı tetikleme oranı mı (güncel Tablo-4 için). Tablo-4 sayfa görüntüsüyle doğrulandı. Mart 2025: pay bazında DK yalnız düşüşte %5, 15 dk + 2 dk, eşleştirme rastlantısal (sabit saat kararıyla çelişir, yeni [DOĞRULA]); EBDKS 19 ve 21 Mart'ta ikişer kez, eski 20/30 dk kuralı. |
| 08-pazarlar-tedbirler | Yazıldı (55 madde); kullanıcı doğrulaması bekliyor. Tablo-3 ve Tablo-4 sayfa görüntüleriyle doğrulandı (hata yok). Açık: pazar eşikleri/oranlar 2018 verisinden önceki pazar yapısına ait değil, güncel metindir. Mart 2025: pazar kodları eşlendi (T = Alt Pazar), Tablo-4 marj ve DK satırları veriye uymaz. |
| 07-itch | Yazıldı; örnek veriyle doğrulama sonuçları işlendi. |

Açık soru sayısı (21.10.2026; `- [DOĞRULA` ile başlayan satırlar): 01: 13, 02: 12, 03: 21, 04: 13, 05: 27, 06: 22, 07: 4, 08: 15.
8 kural dosyası yazıldı.

## DataStore gün içi verisi ve sistem tasarımı (21.10.2026)
- **Veri kararı (kullanıcı):** ITCH yalnız 2 aylık örnek; ana veri DataStore gün içi emir, gün içi işlem ve gün sonu fiyat-hacim (aylık parquet).
- **Eldeki veri:**
  - emir parquet 2025-03…07 (Mayıs 947.232.947 satır; Haziran ve Temmuz satır sayısı kayda geçmedi), 2025-08 yalnız zip (dönüştürülmedi); 06 ve 07 zip'leri de duruyor (22.10.2026),
  - işlem 2025-03…09,
  - gün sonu 2025-03…08.
- **Bölümleme:** emir dosyaları `veri/gun-ici-emir/gunluk/` altına bölümlendi: 2025-03 (kayıpsız, 1.128.466.831 satır), 2025-04, 2025-05 ve 2025-06 (24.10.2026; satır sayıları `veri/README.md`). Doğrulamalar yalnız Mart ile yapıldı.
- **Doğrulamalar:** Mart 2025 verisiyle yapıldı. Rapor `veri/gunici-veri-dogrulama.md` (13 bölüm). Betikler `veri/araclar/gunici_*.py`, `tek_fiyat_algoritma.py`. Çıktılar `veri/gunici-dogrulama/2025-03/`.
- **Tasarım:** `TASARIM.md` yazıldı:
  - veri katmanı,
  - tarih parametreleri (Mart 2025: marj ±%10, DK yalnız düşüş %5 / 15 dk, EBDKS eski 20/30 dk ve iki eşik, açığa satış 24.03'ten yasak),
  - motor modları (tekrar oynatma / enjeksiyon),
  - tespit birimi pay-pencere (veride üye/hesap kimliği yok).
- **Kullanıcı kararları (21.10.2026):**
  1. Pay bazında DK eşleştirmesi: sabit emir toplama + tarihe bağlı rastlantısal pencere (Mart 2025: 30 sn, 2018: 0 sn).
  2. Tablo-4 ile veri farkı: verideki fiili eşikler kullanılır; fark "Prosedür Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayıtlıdır. Değerler `motor/tarih_parametreleri.csv` dosyasındadır (motorun okuyacağı ilk dosya).
  3. Karışık yönlü tek fiyat: referansa / son işlem fiyatına en yakın aday, eşitlikte orta nokta. Mart 2025'te 2 vaka kurala uyar, 2 vaka istisnadır (`yon_karisik_istisna = 1`; ZPBDL.F, ZRE20.F).
  4. Emir verisi 2025-04 ve 2025-05 başı onaylandı. ITCH örneği önce 2025-03/04 olarak onaylandı, sonra **2025-01 ve 2025-02** olarak değiştirildi (A seviyesi vakalar KRGYO, TDGYO, ALKLC). Bu iki ay için DataStore emir ve işlem dosyaları da indirilecek. "2025-07 alınmaz" yalnız ITCH içindir.
  5. **Veri kapsamı (22.10.2026):** DataStore gün içi emir, işlem ve gün sonu verisi 2024-06…2025-05 arası alınır (12 ay; gerekirse genişletilir). Bu aralık 12.10.2026 planından gelir (o gün ITCH + gün sonu için seçilmişti); DataStore ana veri olunca bu dosyalara aktarıldı. 2025-01/02 (ITCH ayları) aralığın içindedir. 2025-06 ve sonrası indirilen dosyalar aralık dışıdır. Baz fiyat, pazar ve işlem yöntemi için aynı ayların gün sonu dosyası gerekir.
- **Bekleyen:**
  - 2025-01/02: ITCH, emir ve işlem dosyalarının indirilmesi; gün sonu dosyası da gerekir. Tablo: `veri/etiketler/ay_etiket_ortusmesi.csv`. Dikkat edilecekler (disk, biçim kontrolü, tarih parametrelerinin yeniden ölçülmesi, ITCH eşlemesi): `rapor.md` 2.10.
  - Aralıkta eksik: emir, işlem ve gün sonu 2024-06…2025-02 (9 ay). Aralık dışı indirilenler: emir 2025-06, 07 (parquet + zip), 08 (zip); işlem 2025-06…09; gün sonu 2025-06…08. 2025-04…06 emir günlük bölümlendi ama doğrulanmadı.
  - Disk: tüm kapsam aylık parquet + günlük bölümleme olarak D:'ye sığmaz (ay başına emir ≈ 17–21 GB parquet + ≈ 14 GB günlük). Saklamayı kullanıcı yönetir.

## Eşleştirme motoru, arayüz ve tespit (22.10.2026)
- Motor `motor/` (`TASARIM.md` 4.5): sürekli işlem, açılış/kapanış/devre kesici/EBDKS müzayedeleri, kapanış fiyatından işlemler, pay bazında devre kesici eşiği; sentetik emir doğrulama (Ek-19, fiyat adımı, marj, kapanış kuralları) ve enjeksiyon (`senaryolar.py`, `enjeksiyon.py`). Testler `motor/testler/` (23 test, hepsi geçer). 22.10.2026'da commit edildi.
- Tek sıra-gün: `python -I motor/tekrar_oynat.py veri/gun-ici-emir/gunluk veri/gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet GUN KOD --gunsonu veri/gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet [--cikti KLASOR]`.
- Bütün gün (tüm `.E`): `python -I motor/toplu_oynat.py GUNLUK ISLEM GUNSONU GUN CIKTI.csv` (yaklaşık 17 dk). 03.03.2025: 588 sıra, 4.915.057 işlemin %99,85'i birebir. Sonuçlar `veri/gunici-dogrulama/2025-03/motor/`.
- Enjeksiyon: `python -I motor/enjeksiyon.py GUNLUK GUNSONU GUN KOD SENARYO SAAT [ad=deger ...]`.
- Arayüz: `streamlit run arayuz/uygulama.py` (`TASARIM.md` 6.5).
- Tespit ilk sürüm `tespit/` (`TASARIM.md` 6.6): pay-gün özellikleri, Z-skor, VI-104.1 bent kuralları, Isolation Forest, kesitsel karşılaştırma; Mart 2025'te A (ALKLC) için kesitsel ROC-AUC 0,85, B için 0,55.
- Sentetik değerlendirme: pay-gün düzeyinde ROC-AUC 0,40–0,74. 5 dk pencere (`tespit/pencere.py`) ve denetimli model (`tespit/denetimli.py`): yanıltıcı emir kurallarla 0,85 (yanlış alarm yok), denetimli model genel 0,85; kapanış senaryosu şişkin (kapanış penceresi her gün uç). Ayrıntı `TASARIM.md` 6.6.
- Yeni özellikler: kısa ömürlü uzak emir payı, makas (veri ve motor tarafında). Arayüz uyarıları 5 dk pencere kurallarıdır.
- `ozellikler.parquet` yeni özelliklerle yeniden hesaplandı (gün başına ara dosyalar `ozellikler_gunluk/`, kaldığı yerden devam eder). SPK: A (ALKLC) kesitsel ROC-AUC 0,90, B 0,53. Pencere: yanıltıcı emir kurallarla 0,90 (ilk 3 %84); kapanış penceresi geçmiş kapanışlara göre puanlanınca yanlış alarm 0, ama H × %3 kapanış emri yakalanmıyor. Ayrıntı `TASARIM.md` 6.6.
- Motor: seans durum makinesi ajan tabanlı simülasyon çıkarıldığı için gereksiz; kotasyon ve orta nokta öncelikli değil.
- Kapsam dışı: kotasyon, orta nokta, özel işlem bildirimi.
- Karar (22.10.2026): madde 24 sentetik emirlerde geçerli (MPF-AFK-Hesap No değişikliği reddedilir); tekrar oynatmada AFK dolu emirdeki öncelik kaybı uygulanır.

## Öneri formu ve veri talebi (proje klasörü, 22.10.2026'da eklendi)
- **Öneri formu** (`Bitirme_Projesi_Oneri_Formu_Resul_Can_KESKIN.docx`, danışman Doç. Dr. Ersin Kaya): başlık "Ajan Tabanlı Yapay Borsa Simülasyonu ile Borsa İstanbul Pay Piyasasında Kural Dışı Fiyat Hareketlerinin (Anomalilerin) Tespiti". `CLAUDE.md` başlığından farklıdır.
- Formda olup `TASARIM.md`'de olmayanlar:
  - yatırımcı ajanları (küçük, büyük, yabancı),
  - GA/PSO ile kalibrasyon,
  - Monte Carlo "kurallara uygun piyasa" olasılık bandı,
  - anomalilerin piyasa geneli / paya özgü sınıflandırılması,
  - sanal-reel paralel çalışma (replay + gecikmeli canlı veri, gün sonu eşitleme),
  - Z-skor / Isolation Forest karşılaştırması,
  - görselleştirme arayüzü.
- Formda kapsam BIST 30'dan 5–10 paydır.
- Birinci yarıyıl (Ocak'a kadar) hedefleri: motor çalışır hâlde, ajanların ilk sürümü, tek gün simülasyonu, reel veriyle ön istatistik karşılaştırması.
- Çizelge: motor Kasım–Aralık, ajanlar Aralık–Ocak.
- **Veri talep dilekçesi** (`Başvuru Dilekçesi.pdf`, 13.10.2026):
  - gün içi emir defteri ve gün içi işlem defteri: 01.03.2025–31.03.2025,
  - aylık ITCH log ve gün sonu fiyat ve işlem hacmi: 01.06.2024–31.05.2025.
- Diskteki dosyalar bu talepten farklıdır: emir 2025-04…08, işlem 2025-04…09, gün sonu 2025-06…08 talepte yok; ITCH 2024-06…2025-05 talepte var ama indirilmedi.
- **Kullanıcı kararları (22.10.2026):**
  - Sistem öneri formundaki ajan tabanlı simülasyon değildir; `TASARIM.md`'deki sistemdir: eşleştirme motoru, veriye dayalı (denetimsiz) makine öğrenmesi, etiketli verilerle (denetimli) makine öğrenmesi ve iktisadi kurallara uygunluk ile manipülasyon tespiti. Formla farklar ve değişikliğin gerekçesi vize raporunda açıklanır (`rapor.md` bölüm 3).
  - Veri: dilekçede ITCH için istenen 01.06.2024–31.05.2025 aralığında DataStore gün içi emir, gün içi işlem ve gün sonu verisi çekilir. ITCH yalnız 2025-01 ve 2025-02 çekilir.
  - İki belge `.gitignore`'a eklendi (kişisel bilgi içerir).
  - Formdan basit ve yararlı olanlar eklenir: Z-skor temel çizgisi, görselleştirme (zorunlu; `TASARIM.md` 6.5), eklenebilirse Isolation Forest.
  - Saklama biçimini kullanıcı yönetir; aralık dışı dosyalar silinecek. Kural dosyalarının onayı veriyle birlikte yapılacak.
  - B seviyesi N = 20 işlem günü (gerekçe `veri/etiketler/etiket-cikarim-kurallari.md`). Pencere yasaktan 3 iş günü önce biter; yasaktan önceki 2 iş günü belirsiz, değerlendirme dışı (karar 22.10.2026; 4/4 A vakasında dönem yasaktan 3 iş günü önce biter).

## SPK bülten etiketleme (bölüm 3 için, 12.10.2026)
`kaynaklar/spk_bultenleri/{2024,2025,2026}` (197 PDF, eksikler eklendi; `2024 15.pdf` → `2024-15.pdf` yapıldı). 35 bülten gözle okundu; kurallar `veri/etiketler/etiket-cikarim-kurallari.md` (v1, 22 kural, 4 etiket seviyesi, 6 [DOĞRULA]). Betik `veri/araclar/spk_bulten_etiket.py` 197 bültende çalıştırıldı; çıktılar `veri/etiketler/` (`vaka.csv` 340 kod satırı, `olay.csv` 19 kayıt, `vaka_pencere_dogrulama.csv` 47 satır / 43 kod satırı / 28 benzersiz kaynak vaka / 27 pay: A 6, B 22). CSV'ler virgül ayırıcılı UTF-8 (BOM'lu); Excel'de CSV'yi kaydetmeyin (`6/1`→`6.Oca` bozulması, 19.10.2026'da betikle yeniden üretildi); inceleme için `vaka_inceleme.xlsx` (tüm sütunlar metin). Kodsuz şirketler `sirket_unvani` sütununda. **Elle doğrulama yapıldı** (47 pencere kaydı + 19 olay PDF metniyle karşılaştırıldı, 10 sınıflandırma/bağlama hatası düzeltildi): `veri/etiketler/dogrulama-kaydi.md`. Bağlantı kuralları 21–22 uygulandı (arşiv dışı atıfta bağ kopar; 6 kayıt C kaldı); kalan: 1 belirsiz bağlantı (ENSRI 2026-6); VI-104.1 Tebliği metni eklendi (`veri/etiketler/kaynak-vi-104-1-piyasa-bozucu-eylemler-tebligi.md`, 2014 yayımı; 18.02.2017 RG 29983 değişikliği işlendi: md 6/1-2 ve md 8 güncel; 2017 sonrası başka değişiklik kontrol edilmedi), bentler `manipulasyon_tipi` olarak çıkarıldı (kural 18, 188 İPC kaydı tam); kod↔unvan sözlüğü (ITCH `R` / DataStore) kurulmadı, pay kodları ITCH ile doğrulanmadı; N (B seviyesi başlangıç varsayımı) kararı bekliyor. Not: açığa satış yasağı 06.02.2023'ten beri vardı, BIST 50 için 02.01.2025'te kalktı, 24.03.2025'te tüm paylarda yeniden getirildi (29.08.2025'e kadar uzatmalı); 2026'da 02.03–26.06.2026 ayrı bir zincir var.

## Çeviriler ve doğrulamalar (`veri/`)
ITCH 2112, MoldUDP64, SoupBinTCP, OUCH, FIX Reference Data, FIX Order Entry (kapsamı sınırlı), SMP çevirileri; DataStore md. Hepsinde "Kullanıcı doğrulaması: bekliyor". `itch-ornek-veri-dogrulama.md`: 08.10.2018 verisi (TXT=VRD, 5.6M mesaj fark 0; VRD = 2 bayt uzunluk + mesaj, MoldUDP64 başlığı yok; zamanlar UTC; 2018'de `R` 129, `A` 37 bayt; seans durumu adları, tek fiyat, fiyat adımı, öncelik kontrolleri).

## Bilinen açık noktalar
Order Attributes = 2 ve Lot Type = 0 anlamı; `TM`/`TR`/`GP` ön ekleri; ITCH `Y` flush güncel davranışı. DataStore: değişiklik sebebi 116/117 anlamı, `guncelleme_no` atlamaları (%0,9), kotasyon zincirinin geçersizleşme anı, aynı µs'deki olayların sırası, özsermaye günlerinde baz fiyat (teorik fiyat kaynağı yok).

## Çalışma notları
Tablolar GFM uyumlu (başlık hücre sayısı = ayraç hücre sayısı, dikdörtgen). Eski ITCH betiklerindeki dosya yolları oturuma özgüdür; `gunici_*` betikleri argüman alır. Aylık emir dosyası tarihe göre sıralı değildir; gün bazlı işler `gun-ici-emir/gunluk/` üzerinden yapılmalı. 16 GB RAM: büyük işleri en fazla ikişer paralel çalıştır. Büyük dosya yazımlarında Python heredoc yerine dosya yazıp çalıştır. `find /` çalıştırma.
