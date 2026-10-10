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
| 02-fiyat | Yazıldı (12 [DOĞRULA]). |
| 03-tek-fiyat | Yazıldı (en kritik dosya). |
| 04-surekli-islem | Yazıldı (5.2.1, 5.6.1, Ek-18 §1.2; SMP ve FIX/OUCH kaynaklı madde 34–48). Açık: Prosedür 5.6.5 "marj dışı emir iptal" ↔ FIX 6.5.6 "duraklatılır". |
| 05-emirler | **YAZILMADI — sıradaki.** Kaynak: Prosedür 5.4.1–5.4.9, 5.5, 5.6.3–5.6.5; Ek-18, Ek-19, Ek-11; OUCH/FIX çevirileri. |
| 06-devre-kesici | Yazılmadı (5.3.4; Ek-3'te hareketli limit, Ek-10 EBDKS akışları). |
| 08-pazarlar-tedbirler | Yazılmadı (kısa özet). |
| 07-itch | Yazıldı; örnek veriyle doğrulama sonuçları işlendi. |
8 dosya bitince ayrı oturumda CLAUDE.md dizin tablosu istenecek: | Dosya | İçerik | Ne zaman okunur |.

## Çeviriler ve doğrulamalar (`veri/`)
ITCH 2112, MoldUDP64, SoupBinTCP, OUCH, FIX Reference Data, FIX Order Entry (kapsamı sınırlı), SMP çevirileri; DataStore md. Hepsinde "Kullanıcı doğrulaması: bekliyor". `itch-ornek-veri-dogrulama.md`: 08.10.2018 verisi (TXT=VRD, 5.6M mesaj fark 0; VRD = 2 bayt uzunluk + mesaj, MoldUDP64 başlığı yok; zamanlar UTC; 2018'de `R` 129, `A` 37 bayt; seans durumu adları, tek fiyat, fiyat adımı, öncelik kontrolleri).

## Bilinen açık noktalar
Order Attributes = 2 ve Lot Type = 0 anlamı; `TM`/`TR`/`GP` ön ekleri; ITCH `Y` flush güncel davranışı; ek3/ek4'te girintili düzyazı satırları (GitHub'da kod bloğu riski, kullanıcı karar vermedi); `.gitignore` yalnızca `veri/itch/`; klasör şu an git deposu değil.

## Çalışma notları
Tablolar GFM uyumlu (başlık hücre sayısı = ayraç hücre sayısı, dikdörtgen). Betiklerdeki dosya yolları oturuma özgüdür. Büyük dosya yazımlarında Python heredoc yerine dosya yazıp çalıştır. `find /` çalıştırma.
