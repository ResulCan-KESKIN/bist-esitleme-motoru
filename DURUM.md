# Proje durumu ve devam notu (yeni oturum için)

Son güncelleme: 10.10.2026. Bu dosya sohbet geçmişi olmadan çalışmaya devam etmek içindir. Görev tanımı: `gorev-kural-yazimi.md` (kurallar: kaynakta olmayanı ekleme, madde no sona, belirsizlik → "Açık sorular" [DOĞRULA], örnekler → "Test örnekleri", dosya adlarında Türkçe karakter yok, her oturumda tek kural dosyası, bitince [DOĞRULA] listesini göster).

## Klasör düzeni
- `kaynaklar/` ham PDF'ler (+ `README.md`, `_kullanilmayan/` kullanılmayacak belgeler).
- `ekler/` Prosedür Ek-1…Ek-21 (kullanıcı doğrulamalı, `README.md` var).
- `kurallar/` kural dosyaları. `veri/` çeviriler, DataStore md, ITCH örnek verisi (`veri/itch/`, git dışı), doğrulama sonuçları ve betikler (`veri/araclar/`).

## Kural dosyaları
| Dosya | Durum |
|---|---|
| 01-seanslar | Yazıldı; P_SI_KAP ve P_ISL_YOK ve öğle tek fiyat farkı DOĞRULANDI; gün sonu saatleri (18:11/18:13/18:14 ↔ Ek-10 18:13/18:15/18:19) ve `2`/EIY/PY/APY durumlarının tarihi AÇIK. |
| 02-fiyat | Yazıldı (7 [DOĞRULA]; fiyat adımı sınırları ITCH `L` ile, marj ve ISKUR Tablo-4/s. 27 ile kapatıldı). |
| 03-tek-fiyat | Yazıldı (en kritik dosya; 16 [DOĞRULA]). Adım 3–5, referans fiyat kaynağı ve eşit uzaklık/yuvarlama kararları gün içi emir verisi bekliyor. |
| 04-surekli-islem | Yazıldı (5.2.1, 5.6.1, Ek-18 §1.2; SMP ve FIX/OUCH kaynaklı madde 34–48; 5 [DOĞRULA]). Marj dışı iptal/duraklatma kararı verildi; öncelik kuralları ITCH 2018 ile doğrulandı. |
| 05-emirler | Yazıldı (143 madde, 24 [DOĞRULA]); kullanıcı doğrulaması bekliyor. Ek-19 matrisi betikle üretildi. Belgeler arası çelişkiler karara bağlandı (G sütunu→Ek-19, askıya alma→iptal+yeni emir, marj dışı→tarihli iptal/gün içi duraklatma, açılışta piyasa emri→Tablo-4, emir bilgisi değişimi reddedilir). Açık: Ek-18 5.4 Örnek 2 ve 6.3 Örnek 1 tablo/metin tutarsızlıkları vb. |
| 06-devre-kesici | Yazıldı (53 madde, 18 [DOĞRULA]); kullanıcı doğrulaması bekliyor. Ek-3 hareketli limit 02-fiyat'ta. Karar: pay bazında emir toplama 10 dk (5.3.4 güncel; Tablo-4 5/15/15 dk eski, süre tarihe bağlı parametre); DK eşleştirmesi sabit saatte, EBDKS rastlantısal. Açık: marj mı tetikleme oranı mı (güncel Tablo-4 için). Tablo-4 sayfa görüntüsüyle doğrulandı. |
| 08-pazarlar-tedbirler | Yazıldı (55 madde, 12 [DOĞRULA]); kullanıcı doğrulaması bekliyor. Tablo-3 ve Tablo-4 sayfa görüntüleriyle doğrulandı (hata yok). Açık: pazar eşikleri/oranlar 2018 verisinden önceki pazar yapısına ait değil, güncel metindir. |
| 07-itch | Yazıldı; örnek veriyle doğrulama sonuçları işlendi. |
8 kural dosyası yazıldı. Proje kökündeki `CLAUDE.md` yazıldı (dizin tablosu: | Dosya | İçerik | Ne zaman okunur |, çalışma kuralları, kodlamayı etkileyen kullanıcı kararları). Kural dosyalarına yeni karar işlenince CLAUDE.md'deki "kullanıcı kararları" listesi de güncellenmeli.

## Çeviriler ve doğrulamalar (`veri/`)
ITCH 2112, MoldUDP64, SoupBinTCP, OUCH, FIX Reference Data, FIX Order Entry (kapsamı sınırlı), SMP çevirileri; DataStore md. Hepsinde "Kullanıcı doğrulaması: bekliyor". `itch-ornek-veri-dogrulama.md`: 08.10.2018 verisi (TXT=VRD, 5.6M mesaj fark 0; VRD = 2 bayt uzunluk + mesaj, MoldUDP64 başlığı yok; zamanlar UTC; 2018'de `R` 129, `A` 37 bayt; seans durumu adları, tek fiyat, fiyat adımı, öncelik kontrolleri).

## Bilinen açık noktalar
Order Attributes = 2 ve Lot Type = 0 anlamı; `TM`/`TR`/`GP` ön ekleri; ITCH `Y` flush güncel davranışı; ek3/ek4'te girintili düzyazı satırları (GitHub'da kod bloğu riski, kullanıcı karar vermedi); `.gitignore` yalnızca `veri/itch/`; klasör şu an git deposu değil.

## Çalışma notları
Tablolar GFM uyumlu (başlık hücre sayısı = ayraç hücre sayısı, dikdörtgen). Betiklerdeki dosya yolları oturuma özgüdür. Büyük dosya yazımlarında Python heredoc yerine dosya yazıp çalıştır. `find /` çalıştırma.
