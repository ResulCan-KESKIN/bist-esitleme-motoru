# Veri klasörü: notlar ve dikkat edilecek noktalar

Bu klasör ham veriyi ve veri belgelerinin markdown hâllerini içerir. Ana veri DataStore gün içi verisidir: `gun-ici-emir/`, `gun-ici-islem/`, `gun-sonu-fiyat-hacim/`. ITCH (`itch/`) yalnız örnektir. Ham veri git dışıdır; tasarım `../TASARIM.md`'dedir. Aşağıdaki notlar veriyi kullanırken (özellikle farklı tarihli dosyaları birleştirirken) göz önünde bulundurulmalıdır.

## 1. Endeks değerlerinde 27.07.2020 ölçek değişikliği (ÖNEMLİ)

Kaynak: Borsa İstanbul DataStore sayfasındaki uyarı (kullanıcı tarafından aktarılmıştır; sayfa adresi ve erişim tarihi bu klasörde kayıtlı değildir):

> 27.07.2020 tarihinden itibaren (ve bu tarih dahil olmak üzere) TL cinsi BIST Pay Endekslerinden ve Müşteri Endekslerinden iki sıfır atılmıştır. Bu tarihten önceki dosyalardaki endeks değerlerinin 100'e bölünerek ve bölen değerlerinin 100'le çarpılarak kullanılması gerekmektedir. Ayrıca endekslerden sıfır atılması sonucu VİOP'ta işlem gören endeks vadeli işlem ve opsiyon sözleşmelerinde de değişiklikler yapılmıştır. 27.07.2020 tarihinden önceki VİOP dosyaları kullanılırken bu hususun dikkate alınması gerekmektedir. Bahsi geçen hususlarda Borsa İstanbul'un herhangi bir sorumluluğu bulunmamaktadır.

Projede ne zaman gerekir:
- **Endeks değeri içeren her dosya**, özellikle `datastore-dosya-formatlari.md` bölüm 2.1.1–2.1.4 ve 2.1.12 civarındaki endeks dosyaları (fiyat endeksleri, getiri endeksleri, risk kontrol endeksleri, tarihsel volatilite, kapanış/en düşük/en yüksek değerler). 27.07.2020 öncesi ve sonrası tarihli dosyalar aynı ölçekte değildir.
- **Endeksi karşılaştırma ölçütü olarak kullanan modeller** (manipülasyon tespiti: hisse getirisi ile endeks getirisi, piyasa geneli hareket). Farklı tarihlerden endeks verisi birleştirilecekse 27.07.2020 öncesi değerler ölçeklenmeli (aşağıdaki kurala göre), aksi hâlde sıçrama yapay olur.
- **Endekse bağlı devre kesici (EBDKS)** hesabı yüzdesel değişime dayandığı için ölçek değişikliğinden doğrudan etkilenmez; ancak mutlak endeks değeri kullanan her hesap etkilenir.
- **Hisse bazında emir/işlem verisi** (DataStore gün içi dosyaları ve ITCH; fiyat) bu ölçek değişikliğinden etkilenmez. Ana veri Mart 2025 (sonrası) olduğundan ölçekleme gerekmez; 08.10.2018 ITCH örneğiyle birlikte endeks dosyası kullanılırsa 27.07.2020 öncesi değerler ölçeklenmelidir.

Uygulanacak kural (kaynak metne göre): 27.07.2020 öncesi tarihli dosyalardaki endeks değerleri 100'e bölünür; bölen değerleri 100 ile çarpılır. VİOP dosyaları için sözleşme tanımlarındaki değişiklik ayrıca dikkate alınmalıdır (ayrıntı kaynak metinde yok).

## 2. Veri tarihi ile Prosedür sürümü farkı

Ana veri Mart 2025'tir; bu tarihte bazı kurallar yürürlükteki metinden farklıdır (fiyat marjı, devre kesiciler, EBDKS). Mart 2025 değerleri `gunici-veri-dogrulama.md` bölüm 13 ve `../TASARIM.md` 3.6'dadır.

Örnek ITCH verisi 08.10.2018 tarihlidir; `kurallar/` ve `ekler/` altındaki Prosedür güncel sürümdür. Aradaki kural değişiklikleri (fiyat adımı, seans saatleri, ücretler vb.) `ekler/ek21.md` içindeki tarihsel gelişim tablosunda ve eski/yeni metin karşılaştırma cetvellerinde izlenebilir. Örnek: 2018 verisindeki `L` (fiyat adımı) mesajlarında 100 TL ve üzeri için tek adım (0,10) görünür; güncel Tablo-7'de bu aralık kademelidir (06.11.2023 tarihli değişiklik).

## 3. Klasör düzeni

| Yol | İçerik |
|---|---|
| `gun-ici-emir/PP_GUNICIEMIR.M.YYYYAA.parquet` | Aylık gün içi emir olayları (her satır, bir olay sonrası emrin tam durumu). CSV'den `araclar/gunici_emir_csv2parquet.py` ile. |
| `gun-ici-emir/gunluk/YYYY-MM-DD/{pay,varant}-{0..7}.parquet` | Aynı veri gün ve sıra kovasına bölünmüş, `islem_kodu`, `emir_degistirilme_zamani`, `guncelleme_no` sıralı (`araclar/gunici_emir_gunluk_bol.py`; kayıpsız). Motor ve doğrulamaların girdisi. |
| `gun-ici-islem/PP_GUNICIISLEM.M.YYYYAA.parquet` | Aylık gün içi işlemler (her işlem A ve S olmak üzere iki satır). CSV'den `araclar/gunici_islem_csv2parquet.py` ile. |
| `gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.YYYYAA.parquet` | Sıra-gün gün sonu bülteni (baz fiyat, pazar, işlem yöntemi, fiyat/hacim özetleri). CSV'den `araclar/gunsonu_fiyat_hacim_csv2parquet.py` ile. |
| `gun-ici-endeks/PP_GUNICITUMENDEKS.M.YYYYAA.{zip,parquet}` | Gün içi endeks değerleri, bütün fiyat endeksleri, saniyelik (`datastore-dosya-formatlari.md` 2.1.19). 2024-01…2025-06. Parquet `araclar/gunici_endeks_csv2parquet.py` ile: `tarih`, `zaman` (time32 ms), `endeks_kodu`, `endeks_adi`, `deger`; satırlar kaynak sırasında, kayıpsız. İçerik kontrolü aşağıda, notlarda. |
| `degerleme-orani/degoran_M_YYYYAA.{zip,parquet}` | Değerleme Oranları (Aylık; `datastore-dosya-formatlari.md` 2.1.23): ay sonu itibarıyla pay bazında piyasa değeri, son 4 çeyrek net kâr, nakit net temettü, özsermaye (bin TL), F/K, TV, PD/DD; paylar sektörlere göre. 2024-01…2025-06. Parquet `araclar/degerleme_oranlari_xlsx2parquet.py` ile: satır başına bir kayıt (`tur`: ozet / ana_sektor_toplam / sektor_toplam / pay), `ana_sektor`, `sektor`; sayı olmayan hücreler (`VY` veri yok, `---` negatif kârda F/K) `<alan>_metin` sütununda. |
| `gunici-veri-dogrulama.md` | Mart 2025 gün içi verisiyle yapılan doğrulamaların sonuçları. |
| `gunici-dogrulama/YYYY-MM/` | Doğrulama betiklerinin çıktıları (özet CSV/TXT git'te; ara parquet dosyaları git dışı, yeniden üretilebilir). |
| `itch/<tarih>/itch-TXT-...tar.bz2` | Metin hâlinde çözülmüş ITCH mesajları (iki parça: `itch-partition-1-...txt`, `itch-partition-2-...txt`). |
| `itch/<tarih>/itch-VRD-...tar.bz2` | İkili "rewinder" dosyaları (`TM-*.VRD`, `TR-*.VRD`, boş `GP-*.VRD`). |
| `itch/<tarih>/txt/`, `itch/<tarih>/vrd/rewinder-files/` | Yukarıdaki arşivlerin çıkarılmış hâli (≈ 570 MB + 380 MB). `veri/itch/` `.gitignore` ile git dışındadır. |
| `datastore-dosya-formatlari.md` | DataStore rapor dosyaları (endeks, işlem hacmi, emir defteri raporları vb.) için alan tanımları; ITCH akışını anlatmaz. |
| `bistech-itch-protokol-spesifikasyonu.md` | ITCH protokol spesifikasyonunun (sürüm 2112) Türkçe çevirisi. |
| `moldudp64-protokol-spesifikasyonu.md`, `soupbintcp-protokol-spesifikasyonu.md` | Taşıma katmanı belgelerinin Türkçe çevirisi. |
| `ouch-protokol-spesifikasyonu.md`, `fix-referans-veri-protokol-spesifikasyonu.md`, `fix-emir-iletimi-protokol-spesifikasyonu.md`, `emrimle-eslesmesin-teknik-calisma-esaslari.md` | Emir iletimi (OUCH, FIX Order Entry), FIX Reference Data ve SMP belgelerinin Türkçe karşılıkları (FIX Order Entry kapsamı sınırlıdır; dosya başlığında yazılı). |
| `itch-ornek-veri-dogrulama.md` | 08.10.2018 örnek verisiyle yapılan doğrulamaların sonuçları (VRD biçimi, TXT–ikili eşleşmesi, seans durumları, tek fiyat, fiyat adımı). |
| `araclar/` | Hazırlama ve doğrulama betikleri (Python). `gunici_*` betikleri komut satırı argümanı alır (kullanım her dosyanın başında); eski ITCH betiklerinde dosya yolları oturuma özgüdür. |

Notlar:
- Gün içi endeks (`PP_GUNICITUMENDEKS`, 2024-05…2025-06, 14 zip; içerik kontrolü 28.10.2026):
  - **Biçim:** iki başlık satırı (TR/EN), `;` ayraçlı: `TARIH` (GG/AA/YYYY; belgede GG.AA.YYYY yazar), `ZAMAN` (SS:DD:ss), `ENDEKS KODU`, `ENDEKSLER` (Türkçe ad), `FIYAT ENDEKSI DEGERI`.
  - **Izgara:** her endeks için 09:55:00–18:09:59 arasında her saniye bir satır, artı 18:10:11'de kapanış değeri (günde 29.701 satır). Değer değişmese de yazılır. Yarım günlerde (28.10.2024, 05.06.2025) 12:40:11'e kadardır (9.901 satır).
  - **Endeksler:** 2024-05…08'de 75 endeks var. 2024-09'dan sonra 77'dir; `XGYOS` (GYO ağırlık sınırlamalı) ve `XSINS` (sınai ağırlık sınırlamalı) eklenir. XU100, XU030, XU050, XUTUM, XYLDZ, sektör endeksleri (XBANK, XGMYO, XHOLD, XUSIN, XUMAL, XUHIZ, XUTEK vb.), katılım, temettü ve şehir endeksleri her aydadır. Her kodun tek adı vardır.
  - **Doğrulama:**
    - Okunan satır sayısı her ayda CSV veri satırı sayısıyla birebirdir.
    - Hatalı tarih, zaman ya da değer, boş değer ve sıfır ya da altı değer yoktur.
    - Ay dışı tarih yoktur.
    - Gün kümesi her ayda gün sonu dosyasıyla aynıdır.
  - **Tek kusur:**
    - 19.07.2024'te açılışta (09:55:21–09:55:51) 14 endekste 30 saniye eksiktir. Ardından 09:55:52–54'te tekrarlı satırlar gelir (154 satır; 14 (zaman, kod) çiftinde değerler farklıdır).
    - 28.08.2024'te aynı biçimde 8 saniye eksiktir (09:55:29–36). Ardından 09:55:37–38'de 98 tekrarlı satır gelir (değerler aynı).
    - Etki yalnız açılış eşleşmesinin ilk dakikasındadır, sürekli işlemden öncedir. Kullanırken (tarih, zaman, kod) başına son satır alınır; parquet'e çevirirken satırlar olduğu gibi tutulur.
  - Kontrol betiği ve çıktıları: oturum dışı (`endeks_kontrol.py`; özet: aylık satır, gün, endeks sayısı; günlük satır, ilk ve son zaman).
  - Klasör 28.10.2026'da `gun-ici-tum-endeks-bilgieri/` adından `gun-ici-endeks/` olarak değiştirildi (kullanıcı).
- Değerleme oranları (`degoran_M_YYYYAA`, 2024-05…2025-06, 14 ay; kontrol 28.10.2026):
  - **Biçim:** zip içinde tek xlsx (`oranYYYYAA.xlsx`). İlk sayfa ("sınıf"):
    - Önce endeks ve pazar toplamları gelir (BIST 100/50/30/TÜM, Yıldız, Ana, Alt, Yakın İzleme, PÖİP, PP Genel).
    - Sonra sektör başlıkları altında paylar ve "TOPLAM / ORTALAMA" satırları gelir.
    - Başlığının hemen altında TOPLAM gelen sektör ana sektördür. Alt sektörleri, toplamları ana sektör toplamını tutana kadar onu izler; sınır tabloda yazmaz.
    - En sonda Piyasa Öncesi İşlem Platformu (PÖİP) bölümü vardır.
    - İkinci sayfa sektör kod tablosudur. Başlıktaki tarih takvim ay sonudur (ör. 30.06.2024 pazar); değerler ayın son iş gününe aittir.
  - **Biçim farkı:** 2024-05'te 4 sektör başlığının kod sütunu boştur; çevirici başlığı ad sütunundan tanır. 2024-06'da 4 sektör adı değişir:
    - "MADENCİLİK" → "MADENCİLİK VE TAŞ OCAKÇILIĞI",
    - "METAL ANA SANAYİ" → "ANA METAL SANAYİ",
    - "TAŞ VE TOPRAĞA DAYALI SANAYİ" → "TAŞ VE TOPRAĞA DAYALI",
    - "SPOR VE EĞLENCE HİZMETLERİ" → "SPOR EGLENCE BOS ZAMANLARI DEGERLENDIRME HIZMETLERI".
  - **Doğrulama:**
    - Her ayda bütün hücreler geri okunup Excel ile birebir karşılaştırıldı (fark 0).
    - Her sektörde payların piyasa değeri toplamı sektör toplamını, alt sektörlerinki ana sektör toplamını, bütün paylarınki "PP GENEL" toplamını tutar.
    - Ayda 560…589 pay, 44 sektör, 16 ana sektör vardır. Ay içinde tekrarlı kod yoktur. Piyasa değeri hiç boş değildir.
    - `VY`: net kâr 628, temettü 317, özsermaye 13 hücre. `---`: F/K 2.699 hücre.
  - **Gün sonu ile kapsam:** ayın son işlem günündeki `EQT` / `.E` payların hepsi vardır, yalnız ISKUR (İş Bankası kurucu payı) yoktur.
  - **Piyasa değeri ile kapanış fiyatı tutarlı:** piyasa değeri / kapanış fiyatından çıkan pay sayısı aylar arasında 157 geçişte %1'den çok değişir.
    - Oranlar çoğunlukla tam sayıdır (2, 3, 4, 5 kat; bedelsiz sermaye artırımı).
    - Bu değişimlerin %99,3'ü sonraki ay da kalır, yani gerçek pay sayısı değişimidir.
  - **Sektör değişimi:** ad değişiklikleri dışında 14 ayda yalnız 6 pay sektör değiştirir (BORLS, EMNIS, GRTRK, KNFRT, RGYAS; TBORG PÖİP'ten Gıda'ya).
  - **SPK etiketli paylar** (`etiketler/vaka.csv`, etiket_nihai = 1; 61 kod):
    - 60'ı vardır. Olmayan TRALT'tır; kararları 2026'dadır, bu dönemde pay KOZAL koduyla işlem görür.
    - En çok GYO (8), holding (7), gıda (6), tekstil (4) ve kimya (4) sektörlerindedir.
    - Mart 2025 piyasa değeri dağılımında A seviyesi payların yüzdelik sırası 0,10…0,66'dır, yani yalnız en küçük paylar değildir.
- DataStore zamanları: emir giriş/değiştirilme ve işlem zamanı İstanbul saatidir; `guncelleme_zamani` ve işlem değiştirilme zamanı UTC'dir (ayrıntı `gunici-veri-dogrulama.md` bölüm 2).
- Eldeki parquet dosyaları (22.10.2026): emir 2025-03…07 (2025-08 yalnız zip); işlem 2025-03…09; gün sonu 2025-03…08. 26.10.2026: emir ve işlem 2025-02 eklendi (zip'ler harici diskte; emir 796.921.021, işlem 20 gün 173.886.550 satır; ikisi de zip içindeki CSV'nin veri satırı sayısıyla birebir); emir ve işlem 2025-01 eklendi (emir 824.226.427, işlem 22 gün 194.373.786 satır; CSV ile birebir); işlem 2024-12 eklendi (22 gün, 209.861.208 satır; CSV ile birebir); 27.10.2026: emir 2024-12 (828.267.318 satır), 2024-11 (790.210.572), 2024-10 (845.482.082), 2024-09 (844.331.279) ve işlem 2024-11 (21 gün, 199.469.570 satır), 2024-10 (22 gün, 201.418.356 satır) eklendi; hepsi CSV ile birebir (2024-09 işlem zip'i yok); gün sonu 2024-09…2025-02 eklendi (hücre hücre CSV ile birebir; gün kümesi emir günlük klasörleriyle aynı), 2024-06…08 gün sonu henüz yok; 2025-07/08 gün sonu kullanılmayacağı için silindi (27.10.2026; eldeki gün sonu 2024-09…2025-06). 28.10.2026: emir 2024-07 (820.493.297 satır, 2024-07-01…31) ve 2024-08 (914.468.353 satır, 2024-08-01…29) eklendi, ikisi de CSV ile birebir (zip'ler `Downloads`'ta); 28.10.2026: emir ve işlem 2024-06 eklendi (emir 703.468.955 satır, işlem 17 gün 200.100.560 satır; ikisi de CSV ile birebir); işlem 2024-07 (22 gün, 245.973.362 satır), 2024-08 (21 gün, 239.387.574 satır), 2024-09 (21 gün, 218.040.362 satır) eklendi; üçü de CSV ile birebir, gün kümeleri emir günlük klasörleri ve gün sonuyla aynı. 28.10.2026: gün sonu 2024-05…08 eklendi (satır 149.164 / 110.860 / 135.997 / 141.786, gün 22 / 17 / 22 / 21; sabit şemaya kayıpsız, CSV veri satırı sayısıyla birebir; 2024-07/08 gün kümesi emir günlük klasörleriyle aynı; CSV'ler silindi). Eldeki gün sonu 2024-05…2025-06; 2024-05 hedef aralığın bir ay öncesidir. Gün sonu dosyalarının hepsi aynı sabit şemadadır (şema `araclar/gunsonu_fiyat_hacim_csv2parquet.py` içinde; 27.10.2026'da 2024-09…2025-08 bu şemayla yeniden yazıldı, eski dosyalarla değer farkı 0): `corporate_action` metindir (iki haneli kodlar "03", "06", birleşik "01&03"; boş = null), `reference_price` ve açığa satış fiyat/tutar sütunları ondalıktır. Bir ayın değeri şemaya kayıpsız uymazsa çevirici durur; şema genişletilir ve tüm aylar yeniden yazılır. Hedef kapsam emir, işlem ve gün sonu için 2024-06…2025-05'tir; 2025-06 ve sonrası aralık dışıdır (`TASARIM.md` 6.4). Günlük bölümleme 2024-06…2025-06 için yapıldı (24.10.2026, 2025-01/02: 26.10.2026, 2024-09…12: 27.10.2026, 2024-06…08: 28.10.2026; aylık dosyayla satır sayısı tutar: 2024-06 17 gün 703.468.955 satır, 2024-07 22 gün 820.493.297 satır, 2024-08 21 gün 914.468.353 satır, 2024-09 21 gün 844.331.279 satır, 2024-10 22 gün 845.482.082 satır, 2024-11 21 gün 790.210.572 satır, 2024-12 22 gün 828.267.318 satır, 2025-01 22 gün 824.226.427 satır, 2025-02 20 gün 796.921.021 satır, 2025-04 20 gün 1.026.868.890 satır, 2025-05 20 gün 947.232.947 satır, 2025-06 19 gün 894.030.467 satır). Doğrulamalar yalnız Mart 2025 ile yapıldı.
- **29.10.2026: 2024-01…05 eklendi** (kullanıcı isteği; dönüşüm hattı, her adım doğrulandı, hata 0, silinen zip yok):
  - gün sonu 2024-01…04 (satır 95.678 / 96.703 / 106.669 / 107.892), gün içi endeks 2024-01…04 (13.134.990 / 12.537.356 / 12.537.945 / 10.348.830), değerleme 2024-01…04 (606 / 610 / 614 / 616 satır); üçü de dönüştürücülerin kayıpsızlık kontrolüyle ("SONUC: GECTI"). Endeks her gün 597.045 satırdır (gün sayısı aynı olan aylarda satır sayısı aynı çıkar). Gün sonu CSV'leri klasörde duruyor.
  - işlem 2024-01…05: 276.026.604 / 354.376.090 / 330.241.292 / 248.470.228 / 333.846.636 satır, gün 22 / 21 / 21 / 18 / 22; satır sayısı zip içindeki CSV'nin veri satırı sayısıyla birebir, gün kümesi gün sonuyla aynı.
  - emir 2024-01…05: 821.518.791 / 965.257.677 / 970.495.341 / 809.651.490 / 1.036.717.486 satır, CSV ile birebir; günlük bölümleme 22 / 21 / 21 / 18 / 22 gün, gün klasörleri gün sonu günleriyle aynı, satır toplamı aylık dosyayla aynı.
  - Günlük bölümler 2024-01…2025-06'yı kesintisiz kapsar (18 ay). Emir zip'leri 2024-03…05 ve aylık emir parquet'leri kullanıcı tarafından harici diske (F:) taşındı; emir ve işlem 2024-01/02 ile işlem 2024-03…05 zip'leri `Downloads`'ta. Bölme sırasında en yüksek ek disk kullanımı aylık parquet boyutunun 1,9 katı ölçüldü (2024-03: 28,4 GB / 15,0 GB); günlük bölümler aylık dosyanın 0,82 katı yer tutar.
  - Tarih parametreleri 2024-01…05 için ölçüldü ve `VERI_DONEMI` 2024-01-01'e genişletildi (30.10.2026, `../rapor.md` 15); ölçüm çıktıları `gunici-dogrulama/2024-0N/` (`gunsonu/`, `seans-akisi/`, `devre-kesici/`, `tek-fiyat/`).
- Klasör adı `itch/2018-10-08` (8 Ekim 2018 tarihli veri).
- TXT dosyalarındaki zaman UTC'dir (İstanbul = UTC + 3). `TM-n.VRD` ile `TR-n.VRD` bayt bayt aynıdır; `partition-1` ↔ `TM-1`, `partition-2` ↔ `TM-2`.
- `.VRD` dosyası MoldUDP64 paketi değil, `[2 bayt uzunluk][mesaj]` dizisidir (ayrıntı: `itch-ornek-veri-dogrulama.md`).
