# Veri klasörü: notlar ve dikkat edilecek noktalar

Bu klasör ham veriyi (`itch/`) ve veri dokümanının markdown hâlini (`datastore-dosya-formatlari.md`) içerir. Aşağıdaki notlar veriyi kullanırken (özellikle farklı tarihli dosyaları birleştirirken) göz önünde bulundurulmalıdır.

## 1. Endeks değerlerinde 27.07.2020 ölçek değişikliği (ÖNEMLİ)

Kaynak: Borsa İstanbul DataStore sayfasındaki uyarı (kullanıcı tarafından aktarılmıştır; sayfa adresi ve erişim tarihi bu klasörde kayıtlı değildir):

> 27.07.2020 tarihinden itibaren (ve bu tarih dahil olmak üzere) TL cinsi BIST Pay Endekslerinden ve Müşteri Endekslerinden iki sıfır atılmıştır. Bu tarihten önceki dosyalardaki endeks değerlerinin 100'e bölünerek ve bölen değerlerinin 100'le çarpılarak kullanılması gerekmektedir. Ayrıca endekslerden sıfır atılması sonucu VİOP'ta işlem gören endeks vadeli işlem ve opsiyon sözleşmelerinde de değişiklikler yapılmıştır. 27.07.2020 tarihinden önceki VİOP dosyaları kullanılırken bu hususun dikkate alınması gerekmektedir. Bahsi geçen hususlarda Borsa İstanbul'un herhangi bir sorumluluğu bulunmamaktadır.

Projede ne zaman gerekir:
- **Endeks değeri içeren her dosya**, özellikle `datastore-dosya-formatlari.md` bölüm 2.1.1–2.1.4 ve 2.1.12 civarındaki endeks dosyaları (fiyat endeksleri, getiri endeksleri, risk kontrol endeksleri, tarihsel volatilite, kapanış/en düşük/en yüksek değerler). 27.07.2020 öncesi ve sonrası tarihli dosyalar aynı ölçekte değildir.
- **Endeksi karşılaştırma ölçütü olarak kullanan modeller** (manipülasyon tespiti: hisse getirisi ile endeks getirisi, piyasa geneli hareket). Farklı tarihlerden endeks verisi birleştirilecekse 27.07.2020 öncesi değerler ölçeklenmeli (aşağıdaki kurala göre), aksi hâlde sıçrama yapay olur.
- **Endekse bağlı devre kesici (EBDKS)** hesabı yüzdesel değişime dayandığı için ölçek değişikliğinden doğrudan etkilenmez; ancak mutlak endeks değeri kullanan her hesap etkilenir.
- **Hisse bazında ITCH verisi** (emir/işlem, fiyat) bu ölçek değişikliğinden etkilenmez. Şu anki örnek veri 08.10.2018 tarihli ITCH verisidir; endeks dosyası kullanılırsa 27.07.2020 öncesi olduğu için ölçeklenmesi gerekir.

Uygulanacak kural (kaynak metne göre): 27.07.2020 öncesi tarihli dosyalardaki endeks değerleri 100'e bölünür; bölen değerleri 100 ile çarpılır. VİOP dosyaları için sözleşme tanımlarındaki değişiklik ayrıca dikkate alınmalıdır (ayrıntı kaynak metinde yok).

## 2. Veri tarihi ile Prosedür sürümü farkı

Örnek ITCH verisi 08.10.2018 tarihlidir; `kurallar/` ve `ekler/` altındaki Prosedür güncel sürümdür. Aradaki kural değişiklikleri (fiyat adımı, seans saatleri, ücretler vb.) `ekler/ek21.md` içindeki tarihsel gelişim tablosunda ve eski/yeni metin karşılaştırma cetvellerinde izlenebilir. Örnek: 2018 verisindeki `L` (fiyat adımı) mesajlarında 100 TL ve üzeri için tek adım (0,10) görünür; güncel Tablo-7'de bu aralık kademelidir (06.11.2023 tarihli değişiklik).

## 3. Klasör düzeni

| Yol | İçerik |
|---|---|
| `itch/<tarih>/itch-TXT-...tar.bz2` | Metin hâlinde çözülmüş ITCH mesajları (iki parça: `itch-partition-1-...txt`, `itch-partition-2-...txt`). |
| `itch/<tarih>/itch-VRD-...tar.bz2` | İkili "rewinder" dosyaları (`TM-*.VRD`, `TR-*.VRD`, boş `GP-*.VRD`). |
| `itch/<tarih>/txt/`, `itch/<tarih>/vrd/rewinder-files/` | Yukarıdaki arşivlerin çıkarılmış hâli (≈ 570 MB + 380 MB). `veri/itch/` `.gitignore` ile git dışındadır. |
| `datastore-dosya-formatlari.md` | DataStore rapor dosyaları (endeks, işlem hacmi, emir defteri raporları vb.) için alan tanımları; ITCH akışını anlatmaz. |
| `bistech-itch-protokol-spesifikasyonu.md` | ITCH protokol spesifikasyonunun (sürüm 2112) Türkçe çevirisi. |
| `moldudp64-protokol-spesifikasyonu.md`, `soupbintcp-protokol-spesifikasyonu.md` | Taşıma katmanı belgelerinin Türkçe çevirisi. |
| `ouch-protokol-spesifikasyonu.md`, `fix-referans-veri-protokol-spesifikasyonu.md`, `fix-emir-iletimi-protokol-spesifikasyonu.md`, `emrimle-eslesmesin-teknik-calisma-esaslari.md` | Emir iletimi (OUCH, FIX Order Entry), FIX Reference Data ve SMP belgelerinin Türkçe karşılıkları (FIX Order Entry kapsamı sınırlıdır; dosya başlığında yazılı). |
| `itch-ornek-veri-dogrulama.md` | 08.10.2018 örnek verisiyle yapılan doğrulamaların sonuçları (VRD biçimi, TXT–ikili eşleşmesi, seans durumları, tek fiyat, fiyat adımı). |
| `araclar/` | Doğrulama betikleri (Python; dosya yolları oturuma özgüdür) ve seans durumu çıktısı. |

Notlar:
- Klasör adı `itch/2018-10-08` (8 Ekim 2018 tarihli veri).
- TXT dosyalarındaki zaman UTC'dir (İstanbul = UTC + 3). `TM-n.VRD` ile `TR-n.VRD` bayt bayt aynıdır; `partition-1` ↔ `TM-1`, `partition-2` ↔ `TM-2`.
- `.VRD` dosyası MoldUDP64 paketi değil, `[2 bayt uzunluk][mesaj]` dizisidir (ayrıntı: `itch-ornek-veri-dogrulama.md`).
