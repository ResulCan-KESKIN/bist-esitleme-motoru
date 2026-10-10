# Görev: Borsa İstanbul Pay Piyasası Prosedürü'nden kural dosyaları oluşturmak

## Proje bağlamı (kısa)
Bilgisayar mühendisliği bitirme projesi, tek kişilik. Başlık: "Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi".

Sistemin parçaları:
- Borsa İstanbul DataStore'dan alınan tarihsel ITCH verisi (emir ve işlem akışı) için çözümleyici ve emir defteri yeniden kurucu
- BIST kurallarına uygun eşleştirme motoru (sürekli işlem + açılış/kapanış seanslarında tek fiyat). Gerçek ITCH emir akışını tekrar oynatmak ve araya enjekte edilen sentetik manipülatif emirlerin gerçek emirlerle etkileşimini hesaplamak için kullanılacak.
- Manipülasyon tespiti: iktisadi kurallar + denetimsiz model + denetimli model, SPK vakalarıyla değerlendirme

Bu görevin çıktısı olan kural dosyaları sonraki kod yazma oturumlarında kullanılacak; her oturumda sadece gereken dosya açılıp okunacak. Bu yüzden dosyalar kısa, net ve birbirinden bağımsız okunabilir olmalı.

## Kaynak
Bütün dosyalar bu klasörde:
- Pay Piyasası Prosedürü: pay-piyasasi-prosedur.pdf
- ITCH protokolü: bistech-itch-protocol.pdf (s. 7–32, Appendix C hariç; sadece 07-itch.md için)
Her dosya için yalnızca o dosyanın madde listesindeki sayfaları oku. PDF'in tamamını okuma.
Sayfa numaraları prosedürün içindekiler tablosundaki numaralardır; PDF'in sayfa numarasıyla kayma olabilir, önce doğru sayfayı bul.

## Dosya yapısı (8 dosya)
- 01-seanslar.md: 4.2.11 Seans Saatleri, 4.3.2 Seansın Geçici Durdurulması, 4.3.3 Seansların Uzama ve İptal Esasları
- 02-fiyat.md: 5.1.1 Lot, 5.1.4 Fiyat Gösterimi, 5.1.6 AOF, 5.1.7–5.1.9 Baz Fiyat Aralıkları / Baz Fiyat / Fiyat Adımları, 5.1.10 Referans Fiyat, 5.1.11 + 5.6.2 Fiyat Değişme Sınırları, 5.1.15 Maddi Hata Nedeniyle İşlem İptali
- 03-tek-fiyat.md: 5.2.2 Tek Fiyat Yöntemi (işleyiş, açılış seansı, kapanış seansı, kapanış fiyatından işlemler)
- 04-surekli-islem.md: 5.2.1 Sürekli İşlem Yöntemi, 5.6.1 Öncelik Kuralları
- 05-emirler.md: 5.4.1–5.4.3 Limit / Piyasa / Piyasadan Limite emirler, 5.4.4–5.4.9 diğer emir tipleri (sadece tanım), 5.5 Değiştirme ve İptal, 5.6.3–5.6.4 Maksimum Kotasyon ve Değer Sınırları, 5.6.5 Geçerlilik Süresi (Günlük, KİE, İKG, Tarihli, Askıya Alma)
- 06-devre-kesici.md: 5.3.4 Devre Kesiciler (pay bazında + endekse bağlı)
- 07-itch.md: Prosedür 5.7.4 + ITCH protokolündeki veri tipleri, tüm mesaj formatları, Appendix A (order book view), B (trade ticker), D (reserve order matching), E (protocol flow). Order Book State (O) mesajındaki durum adları belgede listelenmiyor; uydurma, "Açık sorular"a yaz (örnek ITCH gününden doldurulacak).
- 08-pazarlar-tedbirler.md: 4.2.1–4.2.3 ve 4.2.6 Pazarlar, 6.1.1 Brüt Takas, 5.3.1 Piyasa Yapıcılık (sadece genel kurallar, kotasyon fiyatı ve miktarı), 5.3.2 Likidite Sağlayıcılık (sadece kriter), 5.3.6 Gruplama, 5.10–5.11 Bülten ve Raporlar. Bu dosya bağlam amaçlı, kısa özet yeterli.

Dosya adlarında Türkçe karakter kullanma.

## Her dosyanın formatı
# <Başlık>
Kaynak: <belge> <madde no> (s. <sayfa>)
İlgili kod: <ör. motor, parser>

## Kurallar
1. <tek cümlelik, kodlanabilir kural> [madde no]
2. ...

## Açık sorular
- [DOĞRULA] <belirsiz, eksik veya çelişkili nokta>

## Test örnekleri
- <prosedürde veya Ekler'de geçen sayısal örnekler, birebir>

## Çalışma kuralları (çok önemli)
1. Kaynakta olmayan hiçbir kuralı ekleme. Prosedürü bildiğini düşünsen bile.
2. Her kuralın sonuna madde numarasını yaz.
3. Belirsiz, eksik ya da kendi içinde çelişkili gördüğün yerleri düzeltme veya yorumlama; "Açık sorular" altına [DOĞRULA] ile yaz.
4. Kuralları prompt diliyle değil, şartname diliyle yaz. Kısa, kesin, kodlanabilir cümleler.
5. Aynı kural iki maddede geçiyorsa (ör. fiyat limitleri 5.1.11 ve 5.6.2) tek yerde birleştir, iki madde numarasını da yaz.
6. Sayısal değerleri (saatler, yüzdeler, tablolar) birebir aktar, yuvarlama.
7. Prosedürdeki örnek hesaplamaları "Test örnekleri" bölümüne eksiksiz koy; bunlar eşleştirme motorunun birim testleri olacak.
8. 03-tek-fiyat.md projenin en kritik dosyası. Algoritmayı adım adım, sıralı yaz; eşitlik durumlarında hangi kuralın uygulandığını prosedürde nasıl geçiyorsa öyle yaz ve atlama.
9. İlgili bir Ek varsa (prosedürün içindekiler tablosundaki EKLER listesinden) onu da kaynak olarak kullan. Ek'lerdeki tablolar için sütun kayması riskini belirt.

## Akış
- Her oturumda sadece istenen tek dosyayı oluştur ve bu klasöre kaydet.
- Kod yazma, başka dosya oluşturma, sadece istenen md dosyasını yaz.
- Tablolardan aktarılan sayısal değerlerin yanına (tablodan) yaz; bunları ben PDF'le ayrıca kontrol edeceğim.
- Bir madde PDF'te bulunamazsa uydurma, dosyada eksik olduğunu belirt.
- Dosya bitince bana eklediğin [DOĞRULA] maddelerini liste halinde göster.
- 8 dosya bittikten sonra ayrı bir oturumda CLAUDE.md için dizin tablosunu iste: | Dosya | İçerik | Ne zaman okunur |