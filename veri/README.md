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
- DataStore zamanları: emir giriş/değiştirilme ve işlem zamanı İstanbul saatidir; `guncelleme_zamani` ve işlem değiştirilme zamanı UTC'dir (ayrıntı `gunici-veri-dogrulama.md` bölüm 2).
- Eldeki parquet dosyaları (22.10.2026): emir 2025-03…07 (2025-08 yalnız zip); işlem 2025-03…09; gün sonu 2025-03…08. Hedef kapsam emir, işlem ve gün sonu için 2024-06…2025-05'tir; 2025-06 ve sonrası aralık dışıdır (`TASARIM.md` 6.4). Günlük bölümleme yalnız 2025-03 için yapıldı. Doğrulamalar yalnız Mart 2025 ile yapıldı.
- Klasör adı `itch/2018-10-08` (8 Ekim 2018 tarihli veri).
- TXT dosyalarındaki zaman UTC'dir (İstanbul = UTC + 3). `TM-n.VRD` ile `TR-n.VRD` bayt bayt aynıdır; `partition-1` ↔ `TM-1`, `partition-2` ↔ `TM-2`.
- `.VRD` dosyası MoldUDP64 paketi değil, `[2 bayt uzunluk][mesaj]` dizisidir (ayrıntı: `itch-ornek-veri-dogrulama.md`).
