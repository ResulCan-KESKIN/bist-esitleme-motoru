# Ekler (Pay Piyasası Prosedürü Ek-1 … Ek-21)

Kaynak: `pay-piyasasi-prosedur.pdf`, s. 104–380. Her Ek ayrı dosyada (`ek1.md` … `ek21.md`) aktarılmıştır. Kural dosyalarını yazarken Ek içeriği tekrar PDF'ten çıkarılmaz, bu dosyalardan okunur.

## Aktarım yöntemi

- PDF'ten kelime konumlarıyla çıkarım yapılmıştır; tablo hücreleri sayfadaki kenarlık ve dolgu çizgilerinden kurulmuştur. Bu yüzden önceki metin çıkarımındaki sütun kayması sorunu yoktur.
- Yorum eklenmemiştir. Kaynaktaki yazım hataları ve dipnot işaretleri olduğu gibi bırakılmıştır. Üstü çizili, altı çizili, kalın ve renk bilgisi aktarılmamıştır.
- Hücre içi satır sonları tabloda `<br>` ile gösterilir. Markdown tablolarında ilk satır başlık satırı olarak yazılır.
- Her dosyanın başında kaynak sayfa aralığı, otomatik doğrulama, görsel doğrulama durumu, elle düzeltilen sayfalar ve notlar yazılıdır. Sayfa sınırları `**[Sayfa N]**` ile işaretlidir.

## Doğrulama düzeyleri

1. **Otomatik kelime kapsamı:** Her sayfadaki her kelimenin dosyada bulunduğu kontrol edilmiştir (kayıp: 0).
2. **Sayısal tutarlılık:** Ek-1 toplamları; Ek-16 ve Ek-18 emir defteri tablolarında kümülatif toplam, işlem = min(alış, satış) ve kalan = |alış − satış|; Ek-10 akış tablolarında satır numarası ve saat sırası otomatik kontrol edilmiştir.
3. **Görsel karşılaştırma (Claude):** Sayfa görüntüsüyle karşılaştırılan sayfalar her dosyanın başında listelidir. Görüntüsü incelenmeyen sayfalar yalnızca 1. ve 2. düzeyle doğrulanmıştır.
4. **Kullanıcı doğrulaması:** Tüm Ek dosyaları kullanıcı tarafından doğrulanmıştır (her dosyanın başında "Kullanıcı doğrulaması: doğrulandı" yazar).

## Dosya listesi

| Dosya     | Ek    | İçerik                                                                                                                    | Sayfa   | Ne zaman okunur                                         | Görsel doğrulama         |
| --------- | ----- | ------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------- | ------------------------ |
| `ek1.md`  | Ek-1  | Birincil piyasada talep toplama ve satış yöntemi örnekleri (sabit/değişken fiyat dağıtımı)                                | 105–110 | Birincil piyasa gerekirse                               | yok; sayısal kontrol var |
| `ek2.md`  | Ek-2  | Talep toplama yöntemleri özet çizelgesi                                                                                   | 111–112 | Birincil piyasa gerekirse                               | s. 111                   |
| `ek3.md`  | Ek-3  | Varantlar: usul ve esaslar, kodlama şemaları, ihraç başvuru formu                                                         | 113–134 | Varant bağlamı (08-pazarlar-tedbirler.md)               | s. 116, 124, 134         |
| `ek4.md`  | Ek-4  | Sertifikalar: usul ve esaslar, kodlama şemaları                                                                           | 135–142 | Sertifika bağlamı                                       | s. 140                   |
| `ek5.md`  | Ek-5  | Sahipliğe dayalı kira sertifikaları; fiyat adımı ve özellik kodu tabloları                                                | 143–144 | 02-fiyat.md (fiyat adımı), bağlam                       | yok                      |
| `ek6.md`  | Ek-6  | Gayrimenkul sertifikaları; fiyat adımı ve özellik kodu tabloları                                                          | 145–147 | 02-fiyat.md (fiyat adımı), bağlam                       | yok                      |
| `ek7.md`  | Ek-7  | Gayrimenkul yatırım fonu ve girişim sermayesi yatırım fonu katılma payları; fiyat adımı tablosu                           | 148–150 | 02-fiyat.md (fiyat adımı), bağlam                       | s. 149                   |
| `ek8.md`  | Ek-8  | Emtia sertifikaları                                                                                                       | 151–153 | Bağlam                                                  | yok                      |
| `ek9.md`  | Ek-9  | Pazarlar ve seans saatleri çizelgeleri (tam gün, yarım gün)                                                               | 154–155 | 01-seanslar.md                                          | s. 154–155               |
| `ek10.md` | Ek-10 | Seans akış çizelgeleri (seans durumu ve başlangıç saati)                                                                  | 156–175 | 01-seanslar.md, 03-tek-fiyat.md, 06-devre-kesici.md     | s. 172–174               |
| `ek11.md` | Ek-11 | Seans bölümleri (seans durumları) ve açıklamaları; seans durumu bazlı bölümler                                            | 176–190 | 01-seanslar.md, 03-tek-fiyat.md, 05-emirler.md          | s. 177, 181              |
| `ek12.md` | Ek-12 | Ortaklık yetkilileri listesi formu                                                                                        | 191     | Gerekmez (form)                                         | s. 191                   |
| `ek13.md` | Ek-13 | İşlem sırası geçici kapatma talep formu                                                                                   | 192     | Gerekmez (form)                                         | yok                      |
| `ek14.md` | Ek-14 | Borsa dışı işlemlerin tescil talep formu                                                                                  | 193     | Gerekmez (form)                                         | yok                      |
| `ek15.md` | Ek-15 | Tezgâhüstü türev işlemlerinin bildirimi                                                                                   | 194–195 | Gerekmez                                                | yok                      |
| `ek16.md` | Ek-16 | Açılış fiyatı algoritması ve örnekleri                                                                                    | 196–200 | **03-tek-fiyat.md** (birim testleri)                    | tümü (ekran görüntüleri) |
| `ek17.md` | Ek-17 | Özel işlem bildirimi esasları ve örnekleri                                                                                | 201–202 | 04-surekli-islem.md / 05-emirler.md bağlamı             | yok                      |
| `ek18.md` | Ek-18 | Emir tiplerine ilişkin örnekler (öncelik, piyasa, piyasadan limite, dengeleyici, koşullu, kısmi görünme, orta nokta, AOF) | 203–225 | **05-emirler.md**, 03-tek-fiyat.md, 04-surekli-islem.md | s. 206, 210, 224         |
| `ek19.md` | Ek-19 | Seansın bölümlerine göre girilebilecek emir tipleri matrisi                                                               | 226–229 | **05-emirler.md**, 01-seanslar.md                       | s. 228                   |
| `ek20.md` | Ek-20 | Borsa payı ve diğer ücret tarifesi                                                                                        | 230–233 | Gerekmez (ücret)                                        | s. 230–231               |
| `ek21.md` | Ek-21 | Tarihsel gelişim, revizyon özeti ve eski/yeni metin karşılaştırma cetvelleri                                              | 234–380 | Yalnızca değişiklik geçmişi gerekirse                   | s. 236, 361              |

## Dosyaları üreten araçlar

`_araclar/` klasöründe, dosyaların üretiminde kullanılan Python betikleri ve elle düzeltme kayıtları (`overrides.json` elle yazılan sayfalar, `patches.json` yamalar, `verified.json` doğrulama notları) referans için saklanmıştır. Betikler `pdfplumber` ve `pypdfium2` kütüphanelerini kullanır; yollar Claude oturumuna özeldir.
