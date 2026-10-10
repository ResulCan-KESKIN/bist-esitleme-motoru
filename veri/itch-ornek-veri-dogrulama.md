# Örnek ITCH verisi (08.10.2018) ile yapılan doğrulamalar

Bu dosya, `veri/itch/2018-10-08/` altındaki örnek veriyle yapılan kontrolleri ve sonuçlarını kaydeder. Ham veri (`veri/itch/`) `.gitignore` ile git dışındadır; kontrol betikleri `veri/araclar/` altındadır (dosya yolları bu oturuma özgüdür, çalıştırmadan önce yolları düzeltin).
Kapsam: yalnızca bu tek günün (Pazartesi, 08.10.2018) verisi. Aşağıdaki "gözlem"ler başka günler için genellenemez.
Hazırlayan: Claude. Kullanıcı doğrulaması: bekliyor.

## 1 Dosyaların yapısı

| Dosya | Boyut (bayt) | Bulgu |
|---|---|---|
| `txt/itch-partition-1-2018-10-08-0000.txt` | 277.053.968 | Çözülmüş metin (satır başına bir mesaj), bölüm (partition) 1 |
| `txt/itch-partition-2-2018-10-08-0000.txt` | 292.098.523 | Aynısı, bölüm 2 |
| `vrd/rewinder-files/TM-1.VRD` | 93.068.014 | İkili; bölüm 1 ile birebir eşleşti (bkz. 2) |
| `vrd/rewinder-files/TM-2.VRD` | 97.625.915 | İkili; bölüm 2 ile birebir eşleşti |
| `vrd/rewinder-files/TR-1.VRD`, `TR-2.VRD` | TM-1 / TM-2 ile aynı boyut | `cmp` ile TM-1 = TR-1 ve TM-2 = TR-2 (bayt bayt aynı) |
| `vrd/rewinder-files/GP-1.VRD`, `GP-2.VRD` | 0 | Boş dosya |

TXT dosyalarında mesaj satırlarının dışında şu satırlar vardır: `connectionOpened`, `onStartOfSession`, `onEndOfSession`, `connectionLost` (her dosyada birer tane).
TXT zaman biçimi: `2018-10-07T21:37:14.841792820(1538948234841792820)`; parantez içi, Unix epoch nanosaniyesidir ve zaman **UTC**'dir (İstanbul saati = UTC + 3). `T,<saniye>` satırı Unix saniyesidir. Ham hâliyle dosya, 07.10.2018 21:37 UTC (08.10.2018 00:37 İstanbul) ile 08.10.2018 20:47 UTC arasındadır.

## 2 İkili (`.VRD`) dosya biçimi ve çözümleyici doğrulaması

- `.VRD` dosyasında **MoldUDP64 paket başlığı yoktur** (Session/Sequence Number/Message Count alanları yok). Dosya baştan sona şu yapıdadır: `[2 bayt big-endian uzunluk][mesaj]` tekrarlanır; uzunluk, kendisini içermeyen mesaj baytı sayısıdır (MoldUDP64'ün Message Block yapısıyla aynı: `Message Length` + `Message Data`). İlk baytlar: `00 05 54 5B BA 7C 8A` = uzunluk 5, tip `T`, saniye 0x5BBA7C8A = 1538948234.
- Bu yapıyla dosyalar baştan sona tam tüketildi (artık bayt 0).
- Mesaj sayıları TXT ile birebir aynı: bölüm 1 → 2.731.600 mesaj, bölüm 2 → 2.884.165 mesaj.
- Her mesaj alan alan çözüldü ve TXT'deki karşılığıyla karşılaştırıldı (zaman damgası epoch ns, kimlikler, yön, miktar, fiyat, durum adı vb.): **5.615.765 mesajın tamamında fark 0**.

### 2.1 2018 mesaj uzunlukları (uzunluk öneki hariç, bayt)

| Tip | 2018'de gözlenen | Spesifikasyon 2112'ye göre hesaplanan (07-itch.md) | Fark |
|---|---|---|---|
| `T` | 5 | 5 | yok |
| `S` | 6 | 6 | yok |
| `R` | 129 | 130 | 2018'de `Ranking Type` (1 bayt) yok |
| `L` | 25 | 25 | yok |
| `O` | 29 | 29 | yok |
| `A` | 37 | 45 | 2018'de `Order Book Position` (4 bayt, offset 18) var; `Ranking Time` (8 bayt) yok. 2112'de offset 18'deki alan `Ranking Sequence Number` |
| `E` | 52 | 52 | yok |
| `D` | 18 | 18 | yok |
| `P` | 50 | 50 | yok |
| `Z` | 53 | 53 | yok |

2018 `A` mesajı alanları (çözümleme doğrulandı): Order ID @5 (8), Order Book ID @13 (4), Side @17 (1), Order Book Position @18 (4), Quantity @22 (8), Price @30 (4), Order Attributes @34 (2), Lot Type @36 (1).
Bu günün verisinde **hiç** `C`, `F`, `M`, `U`, `V`, `Y` mesajı yoktur.

## 3 Emir defteri yeniden kurma testi

Her bölüm için, Order Book ID + taraf + Order ID anahtarıyla emirler `A` ile eklenip `E` ile miktarı azaltılıp `D` ile silinerek izlendi:

| Kontrol | Bölüm 1 | Bölüm 2 |
|---|---|---|
| Zaman damgasının geri gitmesi | 0 | 0 |
| Aynı anahtarla tekrar `A` | 0 | 0 |
| Bilinmeyen emre `E` / `D` | 0 / 0 | 0 / 0 |
| `E` sonrası kalan miktar < 0 | 0 | 0 |
| Tamamen gerçekleşip silinen emir | 201.266 | 188.474 |
| Gün sonunda defterde kalan emir | 0 | 0 |

Sonuç: Prosedür 5.7.4/spesifikasyon Appendix A'daki "kalan miktar 0 olunca emri çıkar" kuralı (07-itch.md madde 38–39) veriyle tutarlıdır; tamamen gerçekleşen emir için `D` gelmez.
`A` fiyatlarının tamamı (bölüm 1: 1.219.236; bölüm 2: 1.284.821), ilgili emir defterinin `L` mesajlarındaki fiyat adımının katıdır (0 uyumsuzluk).

### 3.1 Fiyat adımı tabloları (`L` mesajı) ve Ek-21

1.628 emir defterinin fiyat adımı tabloları (3 ondalıklı fiyat; değerler TL):

| Grup | Emir defteri | Tablo (Price From – Price To → Tick Size) |
|---|---|---|
| `.E`, `.R`, `.G` (pay ve benzeri) | 411 | 0,010–19,999 → 0,010; 20,000–49,999 → 0,020; 50,000–99,999 → 0,050; 100,000 ve üzeri → 0,100 |
| `.F`, `.F1` (BYF) | 13 | 0,010–49,999 → 0,010; 50,000–99,999 → 0,020; 100,000–249,999 → 0,050; 250,000 ve üzeri → 0,100 |
| `.V` (varant/sertifika) | 1.204 | Tek satır: tüm fiyatlar → 0,010 |

Bu iki tablo, `../ekler/ek21.md` içinde 5.1.9 Tablo-7 ve BYF Tablo-5 için "ESKİ METİN" olarak yazan tablolarla (ek21.md, s. 320) birebir aynıdır (eski Tablo-7: 100,000 – üzeri → 0,100; eski Tablo-5: 250,000 – üzeri → 0,100). Yani 08.10.2018 verisi güncel Tablo-7 / Tablo-5 değil, eski (değişiklik öncesi) tablolara uyar; `../kurallar/02-fiyat.md` güncel tabloları içerir. Varant/sertifika için 0,010 tek adımı bu çalışmada Prosedürle karşılaştırılmadı.
Tablolar 04:00'teki yeniden gönderimde (bkz. bölüm 7) aynen tekrarlanır.

## 4 Seans durumu adları (Order Book State `O` mesajı)

Bu gün 16 farklı `State Name` gözlendi. Hepsi `../ekler/ek11.md` ve `../ekler/ek19.md` içinde geçer; Ek-10'da `P_DK_TEKFIY_EMIR_TPL` ve `P_GECICI_DURDURMA` geçmez (bu durumlar akışta sabit saatli değildir):

`P_ACILIS_EMIR_TPL`, `P_ARA`, `P_DK_TEKFIY_EMIR_TPL`, `P_ESLESTIRME`, `P_ESLESTIRMETEKFIYAT`, `P_GECICI_DURDURMA`, `P_GUNSONU`, `P_GUNSONU_ISLEMLERI`, `P_GUNSONU_ISTATISTIK`, `P_KAPANIS_EMIR_TPL`, `P_KAPANIS_FIY_ISLEM`, `P_MARJ_YAYIN`, `P_MARJ_YAYIN_KAPANIS`, `P_MARJ_YAYIN_KAP_TF`, `P_SUREKLI_ISLEM`, `P_TEKFIYAT_EMIR_TPL`.

Bu günde **görülmeyen** ama Ek-10/Ek-11'de olan adlar (2 sonekli, `_EIY`, `_PY`, `_APY` vb.; ör. `P_ACILIS_EMIR_TPL2`, `P_ACS_EMR_TP_EIY`, `P_KAPANIS_EMIR_TPL2`) 2018 verisinde yoktur.

### 4.1 Akış saatleri (İstanbul saati) ve Ek-10 karşılaştırması

`O` mesajlarından her emir defteri için durum–saat dizisi çıkarıldı: 1.628 emir defteri, 18 farklı dizi. Sınıflar (saatler dakika duyarlığındadır):

| Sınıf | Emir defteri | Akış (özet) |
|---|---|---|
| Standart pay akışı (çoğu `.E`) | 346 | 07:00 `P_MARJ_YAYIN`, 07:30 `P_ARA`, 09:40 `P_ACILIS_EMIR_TPL`, 09:55 `P_ESLESTIRME`, 10:00 `P_SUREKLI_ISLEM`, **13:00 `P_TEKFIYAT_EMIR_TPL`, 13:55 `P_ESLESTIRME`, 14:00 `P_SUREKLI_ISLEM`**, 18:00 `P_MARJ_YAYIN_KAPANIS`, 18:01 `P_KAPANIS_EMIR_TPL`, 18:05 `P_ESLESTIRME`, 18:07 `P_MARJ_YAYIN`, 18:08 `P_KAPANIS_FIY_ISLEM`, 18:10 `P_GUNSONU_ISLEMLERI`, 18:11 `P_GUNSONU_ISTATISTIK`, 18:13 `P_MARJ_YAYIN`, 18:14 `P_GUNSONU` |
| 5 kez tek fiyat (49 `.E` + 4 `.F1`; ör. `ALBTS.F1`, `ANELT.E`) | 53 | Açılış 09:40–09:55 (`P_ESLESTIRMETEKFIYAT`), sonra 10:00, 13:00, 14:00 `P_TEKFIYAT_EMIR_TPL` ve eşleştirmeler 12:55, 13:55, 17:55; kapanış standartla aynı |
| Varant/sertifika (`.V`, 1.204) | 1.204 | 07:00 `P_MARJ_YAYIN`, 07:30 `P_ARA`, 10:00 `P_SUREKLI_ISLEM`, **13:00 `P_ARA`, 14:00 `P_SUREKLI_ISLEM`**, 18:00 `P_ARA`, 18:10 `P_GUNSONU_ISLEMLERI`, 18:11, 18:13, 18:14 |
| BYF (`.F`, 9 emir defteri) ve hak (`.R`, 1) | 10 | Varantla aynı akış (açılış seansı yok) |
| Gün içinde `P_DK_TEKFIY_EMIR_TPL` girenler | 14 | Standart akış + gün içi (dinamik) tek fiyat; durum girişi sabit saatli değil (ör. 10:10, 10:48, 11:05, 11:09, 11:31, 14:29, 14:32, 15:10, 15:53, 17:16, 17:58); eşleştirme genelde girişten 5–15 dakika sonra, sürekli işleme dönüş eşleştirmeden 2 dakika sonra |
| `P_GECICI_DURDURMA` (1; `ATPET.E`) | 1 | 07:30'dan 18:00'e kadar `P_GECICI_DURDURMA`; 18:00 `P_MARJ_YAYIN_KAPANIS`, 18:01 ve 18:08 yine `P_GECICI_DURDURMA`, 18:10 `P_GUNSONU_ISLEMLERI` |

`veri/araclar/ek10_karsilastir.py` ile bu diziler Ek-10'daki 37 akış tablosuyla karşılaştırıldı. Sonuç:
- Gün başı ve kapanış akışı (07:00 → 18:10) Ek-10 `P_STANDART`/`P_TEK_FIY`/`P_IKI_SI` ile **aynıdır**: 5 kez tek fiyat akışı (`P_TEK_FIY`, s. 158) için eşleştirme ve emir toplama saatlerinin tamamı (09:55, 10:00, 12:55, 13:00, 13:55, 14:00, 17:55, 18:00, 18:01, 18:05, 18:07, 18:08, 18:10) birebir tutuyor.
- **Fark 1 (gün sonu saatleri):** 2018 verisinde `P_GUNSONU_ISTATISTIK` 18:11, ikinci `P_MARJ_YAYIN` 18:13, `P_GUNSONU` 18:14; Ek-10'da (güncel metin) 18:13, 18:15, 18:19. Ek-21'de `P_GUNSONU_ISTATISTIK` 18:11:00 yazan eski çizelgeler de bulunur (ek21.md Revizyon No:27, Sürüm 3.7 bölümü); hangi Prosedür sürümünün 08.10.2018'de yürürlükte olduğu bu çalışmada belirlenmedi.
- **Fark 2 (öğle):** 2018 verisinde standart pay akışında 13:00–14:00 arası gün ortası tek fiyat vardır (`P_TEKFIYAT_EMIR_TPL` 13:00, `P_ESLESTIRME` 13:55, sürekli 14:00); varant ve BYF'lerde bu arada `P_ARA`. Ek-10 `P_STANDART` ve `P_IKI_SI` akışlarında bu 13:00–14:00 aralığı yoktur. Ek-21'de (Revizyon 39, Sürüm 3.19 eski metni, s. 325) "tek fiyat yöntemi ile işlem gören kıymetlerde 13:00-14:00 arasında yapılmakta olan gün ortası tek fiyat bölümü devam etmektedir" notu geçer; bu not yalnızca tek fiyat yöntemiyle işlem görenlerden söz eder, oysa 2018 verisinde standart (sürekli) paylar da 13:00'te tek fiyata girmiştir.
- Gün başında BYF akışı: Ek-9/Ek-10 BYF için `P_SI_KAP` akışında açılış eşleştirmesi 09:56 (Ek-9: 09:40–09:56 (+)). 2018 verisindeki `.F` BYF'lerde (9 emir defteri) açılış seansı hiç yok (varant akışı); `.F1` olanlar 5 kez tek fiyat akışındadır. Bu nedenle 09:56 sorusu **bu günün verisiyle kapanmadı**.
- Temerrüt/resmî müzayede (P_ISL_YOK), yarım gün akışları ve EBDKS durumları bu günün verisinde yoktur; ilgili sorular **kapanmadı**.

## 5 Tek fiyat (müzayede) kontrolleri

`veri/araclar/tek_fiyat_kontrol.py`, her `P_ESLESTIRME`/`P_ESLESTIRMETEKFIYAT` girişinden önceki son anlamlı `Z` mesajı (denge fiyatı mevcutken) ile o eşleştirmedeki `P` işlemlerini karşılaştırır:

| Sonuç | Bölüm 1 | Bölüm 2 |
|---|---|---|
| İşlem olan eşleştirmelerin hepsinde tek fiyat (çoklu fiyat) | tümü tek fiyat | tümü tek fiyat |
| İşlem fiyatı = son `Z` denge fiyatı | tümü eşit | tümü eşit |
| İşlem hacmi = min(alış, satış miktarı @ denge fiyatı) | 539 (açılış 154, gün ortası 190, kapanış 189, gün içi tek fiyat 6) | 507 (açılış 147, gün ortası 178, kapanış 175, gün içi tek fiyat 7) |
| İşlem hacmi > son `Z`'deki min miktar (hiçbirinde küçük değil) | 48 | 58 |
| Son `Z` yok, işlem yok | 106 | 83 |
| İşlem yok ama `Z`'de denge fiyatı var | 8 | 9 |

Yorum (kanıtlı kısım): Denge fiyatı ve tek fiyat kuralı verideki tüm işlemlerde tutarlıdır. Hacim farkı olan eşleştirmelerde işlem hacmi `Z` mesajındaki en küçük miktardan **hiçbir zaman küçük değildir**; fark yalnızca büyüktür (örnek: ACSEL.E 2018 açılışı, `Z`: alış 3500 / satış 2123 / denge fiyatı 2,640 TL, gerçekleşen toplam 2124). Nedeni (son `Z`'nin son emirden önce yayımlanmış olması) bu çalışmada **doğrulanmadı**.
Bu kontrol, 03-tek-fiyat.md'deki denge fiyatı seçim kurallarının (azami eşleşme, artık miktar, baz fiyata yakınlık vb.) kendisini sınamaz; çünkü emir toplama sırasında emirler ITCH'ten yayımlanmaz (bkz. 6).

## 6 Müzayede sırasında emir yayını

- Hiçbir emir defterinde `P_ACILIS_EMIR_TPL`, `P_KAPANIS_EMIR_TPL`, `P_TEKFIYAT_EMIR_TPL`, `P_DK_TEKFIY_EMIR_TPL` durumunda `A` (emir ekleme) mesajı gelmez: `A` mesajları yalnızca `P_SUREKLI_ISLEM`, `P_ESLESTIRME`, `P_KAPANIS_FIY_ISLEM` ve `P_ESLESTIRMETEKFIYAT` durumlarında görülür (bölüm 1: 951.464 / 184.506 / 78.631 / 4.635).
- Müzayede girişlerinde emir defterleri `Y` (flush) ile değil, **tek tek `D` mesajlarıyla** boşaltılır (2018'de `Y` mesajı hiç yok): `D` mesajları ağırlıkla `P_SUREKLI_ISLEM`, `P_GUNSONU_ISLEMLERI`, `P_MARJ_YAYIN`, `P_MARJ_YAYIN_KAPANIS`, `P_TEKFIYAT_EMIR_TPL` durumlarında gelir.
- Eşleştirme durumunda gelen `A` mesajlarının (eşleşmeden artan emirlerin yeniden yayımı olduğu varsayımı) anlamı bu çalışmada ayrıca sınanmadı.

## 7 Diğer alan gözlemleri

| Alan | Gözlem (bu gün) |
|---|---|
| Fiyat ondalığı (`R`) | Bütün emir defterlerinde 3 (örn. 2640 = 2,640 TL) |
| `R` Trading Currency | Hepsi `TRY` |
| `R` Financial Product | 5 (Cash; `.E`, `.F`, `.F1` vb.) ve 14 (Equity Warrant; `.V`) |
| `R` Odd/Round/Block Lot | Hepsi 0 / 1 / 0 |
| `R` Number of Legs | Hepsi 0 (kombinasyon yok) |
| `R` Put or Call | 0, 1, 2 gözlendi (`.V` varantlarda 1 = Call ve 2 = Put) |
| `R` Nominal Value | 0 veya 1 |
| `L` Tick Size | Her emir defteri için 4 satır: 10 (0,010), 20 (0,020), 50 (0,050), 100 (0,100) — varantlarda yalnızca 10 |
| `A` Order Attributes | 0 ve **2** (2: bölüm 1'de 18.184, bölüm 2'de 17.401; spesifikasyonda tanımlı değil — yalnızca 0 ve 8192 tanımlı) |
| `A` Lot Type | 2 (tam lot) ve **0** (bölüm 1'de 50, bölüm 2'de 23; spesifikasyonda tanımlı değil) |
| `A` piyasa emri (MIN_INT) / miktar 0 | Hiç yok |
| `E` Combo Group ID | Hep 0 |
| `E` ve `P` Reserved alanları | Hep boşluk baytı (7 + 7) |
| `P` Side | Hep boşluk (anonim piyasa) |
| `P` Printable | Hep `Y` (`N` hiç yok) |
| `P` Occurred at Cross | `Y`: `P_ESLESTIRME` (9.138 + 10.597) ve `P_ESLESTIRMETEKFIYAT` (851 + 687). `N`: `P_SUREKLI_ISLEM` (1.384 + 1.329), `P_DK_TEKFIY_EMIR_TPL` (142 + 16), `P_KAPANIS_FIY_ISLEM` (0 + 3), ayrıca az sayıda `P_ESLESTIRME` (0 + 26) ve `P_ESLESTIRMETEKFIYAT` (2 + 0) |
| `E` mesajı hangi durumda | Hemen hepsi `P_SUREKLI_ISLEM` (421.084 + 423.287); kalanı `P_KAPANIS_FIY_ISLEM` (923 + 1.092) |
| `S` olayı | Dosya başına bir `O` ve bir `C` |
| Bölüm 1 / 2 ayrımı | Emir defterleri bölümlere ayrılmıştır, kesişim yok: bölüm 1'de 750, bölüm 2'de 878 farklı Order Book ID (toplam 1.628); `O` mesajı alan emir defteri sayısı da 1.628 |
| `R` mesajının tekrarı | Bölüm 1'de 972 `R` satırı, 750 farklı emir defteri: 222 emir defteri için `R` (ve `L`) ikinci kez, 04:00 İstanbul saatinde (01:00 UTC) yeniden gönderilmiştir; bu emir defterlerinin akışında 00:37 ve 04:00'te iki kez `P_GUNSONU` görülür. Varant emir defterleri (`.V`) için tekrar yok. (Bölüm 2: 1.080 satır, 878 farklı emir defteri.) |

## 8 Zaman damgası

- `T` mesajlarının saniye değeri hiç geri gitmedi; mesaj `Timestamp – Nanoseconds` alanı `1.000.000.000`'dan küçüktür (hata 0).
- Birleşik zaman = `T` saniyesi × 10⁹ + nanosaniye, TXT'deki parantez içi epoch değerine birebir eşittir.
- `T` mesajı, en az bir yük mesajı üretilen saniyelerde gönderilir: bölüm 1'de 28.022, bölüm 2'de 28.279 adet; dosya süresi yaklaşık 83.000 saniye olduğundan her saniye değil. (İfade 07-itch.md madde 16 ile uyumlu.)

## 9 Fiyat-zaman önceliği kontrolü (sürekli işlem)

`veri/araclar/oncelik_kontrol.py`: Her (emir defteri, taraf) için emirler `A` mesajındaki `Order Book Position` konumuna eklenip `E` ile miktarı azaltılarak ve `D` ile silinerek tutuldu.

| Kontrol | Bölüm 1 | Bölüm 2 |
|---|---|---|
| `A` yerleştirme sayısı | 1.219.236 | 1.284.821 |
| Komşu emirlere göre **fiyat** sırası ihlali (alış azalan, satış artan) | 0 | 0 |
| Aynı fiyatta **zaman** sırası ihlali (yerleştirilen emrin zamanı komşusundan daha önce/sonra) | 2.815 (`P_SUREKLI_ISLEM` 2.808; `P_KAPANIS_FIY_ISLEM` 7) | 2.905 (`P_SUREKLI_ISLEM` 2.887; `P_KAPANIS_FIY_ISLEM` 18) |
| `E` mesajıyla gerçekleşen emrin tarafın en önündeki (konum 1) emir olması | 422.007 / 422.007 (`P_SUREKLI_ISLEM` 421.084, `P_KAPANIS_FIY_ISLEM` 923) | 424.379 / 424.379 (423.287 + 1.092) |

- Zaman sırası ihlallerinin tamamı (5.720 yerleştirme), daha önce `D` ile silinmiş aynı Order ID ile gelen `A` mesajlarıdır. Aynı Order ID'yi yeniden ekleyen `A` mesajlarının toplamı 635.111'dir; bunların yalnızca %0,9'unda zaman sırası bozulur. Bu, "miktar azaltıldığında öncelik korunur" kuralının (04-surekli-islem.md madde 20) uygulaması **olabilir**; bu çalışmada doğrulanmadı.
- `A` zaman damgası mesajın yayın zamanıdır; 2018 verisinde `Ranking Time` alanı yoktur, bu yüzden zaman önceliği yalnızca `A`'nın konum alanıyla izlenebilir.

## 10 Yapılamayanlar / sınırlar

- `GP-*.VRD` dosyaları boş olduğundan GLIMPSE biçimi (SoupBinTCP) bu veriyle sınanamadı.
- Ağ üzerindeki gerçek MoldUDP64 paketleri bu veride yok; yalnızca mesaj akışı var. MoldUDP64 ve SoupBinTCP dokümanları (`moldudp64-protokol-spesifikasyonu.md`, `soupbintcp-protokol-spesifikasyonu.md`) ağ katmanı içindir.
- 2025 sürümündeki `Ranking Type`, `Ranking Time`, `Ranking Sequence Number` alanlarını, `Y` ve `V` mesajlarını içeren veri elde edilmemiştir.
- Bu verideki fiyat adımları (L mesajları) 2018 kurallarına aittir; güncel Tablo-7 (06.11.2023 sonrası) ile karşılaştırma için `../kurallar/02-fiyat.md` ve `../ekler/ek21.md` kullanılmalıdır; bu doküman karşılaştırmayı yapmaz.
