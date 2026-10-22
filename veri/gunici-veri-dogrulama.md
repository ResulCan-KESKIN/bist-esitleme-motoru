# DataStore gün içi verisi (Mart 2025) ile yapılan doğrulamalar

Bu dosya, Mart 2025 DataStore verisiyle yapılan kontrolleri ve sonuçlarını kaydeder:

- `PP_GUNICIEMIR`, `PP_GUNICIISLEM`, `PP_GUNSONUFIYATHACIM`
- 20 işlem günü: 03.03.2025–28.03.2025

Ham veri (`veri/gun-ici-*`, `veri/gun-sonu-fiyat-hacim/`) git dışıdır. Betikler `veri/araclar/gunici_*.py`, özet çıktılar `veri/gunici-dogrulama/2025-03/` altındadır.

Kapsam yalnız bu aydır. Kurallar yürürlükteki Prosedürdür (rev. 21/09/2026); Mart 2025 verisi bazı konularda o tarihteki (eski ya da geçici) kurallara uyar (bkz. bölüm 13).

Hazırlayan: Claude. Kullanıcı doğrulaması: bekliyor.

## 1 Dosyalar

| Dosya | Satır | Sütun | Not |
|---|---|---|---|
| `gun-ici-emir/PP_GUNICIEMIR.M.202503.parquet` | 1.128.466.831 | 26 | 11.943 işlem sırası, 191.047 sıra-gün. Satır grupları 12 güne kadar yayılır (tarihe göre sıralı değildir) |
| `gun-ici-islem/PP_GUNICIISLEM.M.202503.parquet` | 234.387.516 | 21 | Tarihe göre sıralı |
| `gun-sonu-fiyat-hacim/PP_GUNSONUFIYATHACIM.M.202503.parquet` | 192.220 | 52 | DataStore belgesindeki 56 alandan gün ortası seansının 4 alanı yok; sütun adları İngilizce |

Günlük bölümleme (`gunici_emir_gunluk_bol.py`): aylık emir dosyası `gun-ici-emir/gunluk/YYYY-MM-DD/{pay,varant}-{0..7}.parquet` dosyalarına ayrıldı. Bu dosyalar `islem_kodu`, `emir_degistirilme_zamani`, `guncelleme_no` sırasındadır. Satır toplamı aylık dosyayla aynıdır: 1.128.466.831, fark 0.

## 2 Alan anlamları (veriden)

| Konu | Bulgu |
|---|---|
| Emir zamanları | `emir_giris_zamani` ve `emir_degistirilme_zamani` İstanbul saati, µs. `guncelleme_zamani` UTC, saniye: 1.128.466.831 satırın tamamında yerel − 3 saat |
| `emir_giris_zamani` | Emir ömrü boyunca değişmez, fiyat değişikliğinde bile (bkz. 9). Hiçbir satırda değiştirilme zamanından sonra değildir |
| Gün | Tüm satırlarda `tarih` = değiştirilme günü. Geçerlilik yalnız `DAY` (1.037.313.268) ve `IMMEDIATE` (91.153.563); İKG/tarihli emir yoktur |
| Gün sonu | Aktif kalan emirler `P_GUNSONU` bölümünde 18:19:00'da sebep 19 (Expired) ile kapanır: 11.871.378 satır |
| Kategori | 1 normal emir 669.520.670; 4 kotasyon 458.945.852; 32 özel işlem bildirimi 309 |
| Fiyat türü | 1 limit; 2 piyasa; 3 piyasadan limite; 66 dengeleyici (Imbalance 64 + Market 2). Piyasa emri yeni girişlerinde 4.712.232 + tüm müzayede bölümleri `IMMEDIATE`; `DAY` yalnız 2 |
| Emir türü | 0; 2 açığa satış (17.474.762 satır); 64 orta nokta (6.452 satır) |
| Değişiklik sebebi | 5: 571.577.395; 3: 233.970.398; 6: 230.819.084; 1: 79.698.360; 19: 11.871.378; 13: 332.841; 8: 75.709; 117: 42.144; 9: 29.756; 4: 18.613; 116: 16.581; 34: 14.572. 116 ve 117, DataStore referans tablosunda (3.1.4) yoktur. 117 yalnız `P_GECICI_DURDUR_EBDK` (EBDKS durdurması) ve `P_SUREKLI_ISLEM` bölümlerinde görülür |
| İşlem satırları | `islem_numarasi` dolu satırlar 234.387.566; işlem dosyasındaki taraf sayısı 234.387.516 (fark 50). Bu satırlar sebep 3 (233.970.398), 13 (332.841), 8 (74.890), 34 (6.931) ve 9 (2.506) satırlarıdır |
| Anahtar | `emir.islem_numarasi = int(islem.ortak_sozlesme_no, 16)`. İşlem dosyasında her işlem iki satırdır (A ve S, aynı `ortak_sozlesme_no`), her satırda o tarafın `emir_no`'su vardır |
| Aktif/pasif | Sürekli işlemde her işlemin bir aktif, bir pasif tarafı vardır (03.03: 2.566.507 AP + 2.363.544 PA). Müzayede işlemlerinde iki taraf pasiftir. Özel işlem bildiriminde iki taraf aynı emir numarasını taşır. Sürekli işlemde iki tarafı da pasif görünen az sayıda işlem vardır (03.03: 255). Bunlar orta nokta değildir: iki taraf da `DAY` limit emirdir. Birkaç payda birkaç dakikalık kümeler hâlinde görülür (ör. GARAN.E 11:44'te 55 işlem). Niteliği belirlenemedi |
| Görünen miktar | `gorunen_miktar` tüm satırlarda `emir_miktari`'na eşittir. Kısmi görünme koşullu emirler bu alandan ayırt edilemez, ancak sebep 13 satırlarından tanınır (bkz. 9) |
| Kotasyonlar | Pay grubunda yalnız `.F` sıralarında. Her güncelleme yeni bir emir numarasıyla gelir (`onceki_emir_no` zinciri), eski kotasyonun bitişi yazılmaz. Varant grubunda `guncelleme_no` ardışık değildir |
| `giveup_flag` | Tümü `H` |

Pazar kodları (`market_segment`): Z Yıldız, N Ana, T Alt Pazar, W YİP, S PÖİP, K KYÜP, Q GSP/NYİP, E Emtia.
- T, DataStore belgesindeki (2016) referans tablosunda yoktur. Alt Pazar olarak eşlendi; bu eşleme, Tablo-4'teki işlem yöntemi ve açılış emir türü özellikleriyle tutarlıdır (bkz. 6).
- `trading_method`: SI 12.026, TF 760, PY 179.434 sıra-gün.

## 3 İşlem defteri ↔ gün sonu bülteni (`gunici_islem_gunsonu_karsilastir.py`)

İşlem olan 74.979 sıra-günde her bülten alanı, işlemlerden yeniden hesaplanan değerle karşılaştırıldı:

| Bülten alanı | Tanım (veriden) | Uyan / 74.979 |
|---|---|---|
| Toplam sözleşme, miktar, hacim | Normal işlemler + özel işlem bildirimleri (`normal_islem` 3/5) | 74.979 |
| Özel işlem bildirimi sayı/miktar | `normal_islem` 3 ve 5 | 74.979 |
| En düşük, en yüksek fiyat | Normal işlemler | 74.979 |
| Açılış fiyatı | Günün ilk işlemi | 74.979 |
| Kapanış fiyatı | Günün son işlemi (kapanış fiyatından işlemler dâhil ya da hariç aynı) | 74.979 |
| Açılış seansı fiyat/sözleşme/miktar/hacim | 12:00 öncesi `P_ESLESTIRME` ve 10:00 öncesi `P_ESLESTIRMETEKFIYAT` işlemleri | 74.979 |
| Kapanış seansı fiyat/sözleşme/miktar | 18:00 sonrası eşleştirme işlemleri | 74.979 |
| Kapanış fiyatından işlemler | `P_KAPANIS_FIY_ISLEM` | 74.979 |
| AOF | Özel işlem bildirimi hariç tüm normal işlemler (açılış, sürekli, kapanış, kapanış fiyatından); hacim/miktar, 3 hane | 74.960 (kalan 19: düşük hacimli varantlarda 0,001'lik yuvarlama farkı) |
| Değişim % | (kapanış / önceki kapanış − 1) × 100, 3 hane, yarım yukarı (kesin ondalık) | 74.979 |

## 4 Fiyat marjı (`gunici_marj_kontrol.py`; marj adayları ±%10/±%15/±%20)

Baz fiyat = `previous_last_price`. Sınırlar içe yuvarlanır (alt sınır yukarı, üst sınır aşağı adım; `02-fiyat.md` madde 37).

- ±%10 ile işlem olan 12.335 pay/BYF/GMF/GSF/EMS/rüçhan sıra-gününde, sınır dışında işlem olan 20 sıra-gün vardır. Hepsi açıklanabilir:
  - 15'i özsermaye hâli (bedelsiz/temettü; baz düzeltilmemiş),
  - 4'ü rüçhan (`.R`, ±%50),
  - 1'i birincil piyasa (`.BE`).
- 495 sıra-günde en yüksek fiyat hesaplanan tavana, 786 sıra-günde en düşük fiyat hesaplanan tabana **tam olarak** eşittir.
- ±%15 ve ±%20 ile hiçbir sıra-gün sınıra ulaşmaz.

Sonuç: Mart 2025'te Yıldız, Ana, Alt, YİP, PÖİP, BYF (K) ve GSF (Q) için fiyat marjı **±%10**'dur; emtia sertifikası (E) ±%5 ile uyumludur (en yüksek sapma %4,99). Yürürlükteki Tablo-4 (Yıldız %20, Ana %15) bu veriye uymaz (bkz. 13).

## 5 Fiyat adımı ve emir fiyat sınırı (`gunici_fiyat_adimi_sinir_kontrol.py`, `gunici_emir_sinir_disi.py`)

Kontrol edilen fiyatlar:
- **Emir tarafı:** üyenin belirlediği fiyatlar, yani yeni emir (6) ve değişiklik (5) satırları, fiyat > 0.
- **İşlem tarafı:** her işlemin alış satırı.

Kullanılan adım tabloları:
- paylar ve rüçhan: Tablo-7 (`02-fiyat.md`; 06.11.2023 sonrası güncel tablo),
- BYF, GMF, GSF: Tablo-8,
- varant, sertifika, emtia sertifikası: 0,01.

| Kaynak | Grup | Fiyatlı satır | Adım dışı |
|---|---|---|---|
| Emir | Pay (EQT) | 335.383.280 | 0 |
| Emir | Varant (ECW + EPW) | 442.997.511 | 0 |
| Emir | BYF, GMF, GSF, EMS, XCR, RGT | 18.687.183 | 0 |
| İşlem | Pay (EQT) | 114.043.575 | 1 (özel işlem bildirimi, BVSAN.E 13.03, 106,56) |
| İşlem | Diğer | 3.150.183 | 0 |

Sonuç: Mart 2025'te fiyat adımı güncel Tablo-7 / Tablo-8 ile birebir uygulanır; özel işlem bildirimi adıma tabi değildir.

Emir fiyatının günlük sınır (baz ±%10, içe yuvarlanmış) dışına çıktığı pay sıra-günleri 27'dir:
- 26'sı özsermaye hâli günüdür (temettü 14, bedelsiz 12; gün sonu dosyasındaki önceki kapanış düzeltilmemiştir, emir aralığı düzeltilmiş baz fiyatın ±%10'una oturur);
- 1'i birincil piyasa sırasıdır (`BNTAS.BE`).

Diğer günlerde sınır dışında emir yoktur. Liste: `gunici-dogrulama/2025-03/fiyat/emir_sinir_disi.csv`.

## 6 Seans bölümleri ve saatler (profil: `gunici_emir_profil.py`; eşleştirme anı: `gunici_eslestirme_zamani.py`)

Görülen 22 bölüm adı:

`P_ACILIS_EMIR_TPL`, `P_ACS_EMR_TP2_PY`, `P_ACS_EMR_TP2_PY_EIY`, `P_ACS_EMR_TP_EIY`, `P_BP_SUREKLI_ISLEM`, `P_DK_TEKFIY_EMIR_TPL`, `P_DK_TEKFIY_EMR_TPL2`, `P_ESLESTIRME`, `P_ESLESTIRMETEKFIYAT`, `P_ESLESTIRME_EBDK`, `P_GECICI_DURDUR_EBDK`, `P_GECICI_DUR_EBDK_KT`, `P_GECICI_DUR_EBDK_SI`, `P_GUNSONU`, `P_KAPANIS_EMIR_TPL`, `P_KAPANIS_EMIR_TPL2`, `P_KAPANIS_FIY_ISLEM`, `P_SALTKOTASYON`, `P_SUREKLI_ISLEM`, `P_TEKFIYAT_EMIR_TPL2`, `P_TF_EMIR_TPL2_EBDK`, `P_TF_EMIR_TPL_EBDK`.

Hepsi Ek-11/Ek-19'da vardır. Emir satırları yalnız olay olan bölümlerde görüldüğünden `P_MARJ_YAYIN`, `P_ARA`, `P_GUNSONU_ISLEMLERI` vb. görünmez.

| Akış (Ek-10) | Veri |
|---|---|
| Açılış emir toplama 09:40, son 5 dk bölümü (`_EIY`) 09:50 | `.E` için ilk olay 09:40:00.157, `P_ACILIS_EMIR_TPL` son olayı 09:50:00.184, `P_ACS_EMR_TP_EIY` ilk olayı 09:50:00.163. Bütün `.E` sıraları `_EIY` bölümüne girer (son 5 dk kısıtı tüm paylarda; Tablo-4 "YOK") |
| Yıldız/Ana: `P_STNDRT_APY` (`P_ACILIS_EMIR_TPL` → `P_ACS_EMR_TP_EIY`); Alt/YİP/PÖİP: `P_ACS_EMR_TP2_PY` → `P_ACS_EMR_TP2_PY_EIY` (bilgi yayını kısıtlı) | Z ve N sıraları ilk akışta; T, W, S sıraları ikinci akışta (03.03 yeni emir dağılımı). Tablo-4 "bilgi yayınının kısıtlanması: Alt/YİP/PÖİP VAR" ile uyumlu |
| Açılış eşleştirmesi 09:55 (+30 sn rastlantısal) | Her gün tüm paylarda aynı an: gecikme 0,000–29,145 sn, paylar arası yayılım ≤ 0,833 sn |
| BYF açılış eşleştirmesi 09:56 | Gecikme 1,1–28,1 sn, yayılım ≤ 0,001 sn |
| Sürekli işlem 10:00–18:00 | İlk olay 10:00:00.048, son olay 18:00:00.241 |
| Kapanış emir toplama 18:01, eşleştirme 18:05 | 18:01:00.137'den; eşleştirme 18:05:00,144–18:05:28,144, yayılım ≤ 0,495 sn |
| Kapanış fiyatından işlemler 18:08–18:10 | 18:08:00.074–18:10:00.124 |
| 5 kez tek fiyat (`P_TEK_FIY2`): eşleştirmeler 09:55, 12:55, 13:55, 17:55, 18:05 | `P_ESLESTIRMETEKFIYAT` aynı dakikalarda; her aşamada ortak rastlantısal an (gecikme 0,1–29,2 sn, yayılım ≤ 0,7 sn). Emir toplama bölümü yalnız `P_TEKFIYAT_EMIR_TPL2` |
| `P_GUNSONU` 18:19:00 | Süre dolumu satırları 18:19:00.07–18:19:02.25. 2018 ITCH'teki 18:14 farkı bu tarihte yoktur; Ek-10 ile aynı |
| Varant/sertifika `P_SI_KOT`: `P_SALTKOTASYON` 10:00:10, sürekli 10:02:00 | 03–06.03: `P_SALTKOTASYON` ilk olay 10:00:00.6; 07.03'ten itibaren 10:00:10.1 sonrası (Ek-21: 07.03.2025, Duyuru 2025/33431). Sürekli işlem 10:02:00.18'den; bölüm adı veride `P_SUREKLI_ISLEM`, Ek-10'daki `P_SUREKLI_ISLEM_HFL` görülmez |
| Birincil piyasa `.BE` | `P_BP_SUREKLI_ISLEM` 10:30:00–12:56:18 (tek sıra-gün) |

Sonuç: Rastlantısal 30 saniyelik başlangıç pay bazında değil, aşama bazında tektir. O gün o aşamadaki bütün sıralar aynı anda eşleşir. Bu, 2018 verisindeki gözlemle aynıdır.

## 7 Ek-19: bölüm × emir tipi (`gunici_ek19_kontrol.py`)

Yeni emirler (sebep 6) bölüm × tip bazında sayıldı. Ek-19'da 0 olan hücrede yeni emir: **0**. Ayrıntı: `gunici-dogrulama/2025-03/profil/ek19_karsilastirma.csv`.
- Açılış bölümlerinde piyasa ve piyasadan limite emirleri yalnız `P_ACILIS_EMIR_TPL` ve `P_ACS_EMR_TP_EIY` bölümlerinde, yani Yıldız ve Ana pazarda görülür. `TP2_PY` bölümlerinde yoktur. Bu, `03-tek-fiyat.md` madde 24 kullanıcı kararıyla uyumludur.
- Açılış bölümlerinde açığa satış 0'dır. Kapanış (1.188), devre kesici (73) ve EBDKS tek fiyat (235) bölümlerinde açığa satış vardır.
- Orta nokta yalnız sürekli işlemde (3.226), dengeleyici yalnız tek fiyat bölümlerindedir.
- Kapanış fiyatından işlemler bölümünde piyasa emri yoktur. Kotasyon `P_SALTKOTASYON` ve `P_GECICI_DUR_EBDK_KT` bölümlerindedir.

## 8 Emir yaşam döngüsü ve bölüm kuralları (`gunici_emir_kural_kontrol.py`, `gunici_emir_kural_ozet.py`)

20 günün tamamı işlendi. Her emrin satırları `emir_no`, `guncelleme_no` sırasına dizilip bir önceki satırla karşılaştırıldı. Özet: `gunici-dogrulama/2025-03/emir-kural/ozet.txt`.

| Kontrol | Sonuç |
|---|---|
| `emir_giris_zamani` değişiklikte | Normal emirde 131.496.491 değişikliğin hiçbirinde değişmez (fiyat değişikliği dâhil). Kotasyonda (253.410.890) `emir_giris_zamani` = değiştirilme zamanıdır |
| İşlem satırı tutarlılığı (pay grubu) | 230.235.088 işlem satırının 230.234.867'sinde kalan = önceki kalan − eşleşen, emir miktarı ve giriş zamanı sabit; 221 istisna |
| İlk satır | Pay grubunda normal emirlerin ilk satırı sebep 6'dır (219.174.249; 238 kimliğin ilk satırı sebep 3 ya da 1, emir girişi aynı mikrosaniyede sıralanmış olabilir). Pay grubunda ilk satırı sebep 5 olan 3.718.063 kimlik kotasyondur (her güncelleme yeni kimlik, tek satır, kapanış satırı yok) |
| `guncelleme_no` | Pay grubunda ardışık satırların %0,9'unda (4.050.440) 1'den fazla artar; arada yazılmamış olay vardır (türü belirlenemedi). Varantta kotasyon güncellemeleri nedeniyle çoğunlukla ardışık değildir |
| KİE | `IMMEDIATE` emirlerin aktif satırları müzayede emir toplama bölümlerinde görülür (eşleştirmeye kadar defterde bekler). Sürekli işlemde aktif görünen KİE satırı 504'tür; ayrıca incelenmedi |
| Gün sonu | Pay grubunda emirlerin son satırı çoğunlukla işlem, iptal, süre dolumu (11.311.478, `P_GUNSONU`) veya müzayede sonrası sistem iptalidir (9/34). Son satırı aktif kalan kimlikler: sebep 5 ile 3.711.617 + 1.500 (kotasyon kimlikleri, ilk satırı da sebep 5 olan 3.718.063 kimlikle uyumlu) ve sebep 6 / 3 ile 2.737 + 119 (süre dolumu satırı olmayan kimlikler; incelenmedi) |

Bölüm bazında değişiklik yönü (normal emir, sebep 5; fiyat iyileştirme/kötüleştirme, miktar artış/azalış) ve kullanıcı iptali (sebep 1):

| Bölüm | Kötüleştirme | Miktar azaltma | İptal | Ek-19 (I / K / M) |
|---|---|---|---|---|
| `P_ACS_EMR_TP_EIY` (09:50–eşleştirme) | 0 | 0 | 0 | 0 / 0 / 0 |
| `P_ACS_EMR_TP2_PY_EIY` | 0 | 0 | 0 | 0 / 0 / 0 |
| `P_GECICI_DUR_EBDK_KT` (EBDKS, varant/BYF) | 111 | 22 | 103.413 | 1 / 1 / 1 (iyileştirme 0, artış 0; Ek-19 J = L = 0) |
| `P_ACILIS_EMIR_TPL`, `P_KAPANIS_EMIR_TPL`, `P_DK_*`, `P_TF_*`, `P_TEKFIYAT_EMIR_TPL2` | var | var | var | 1 / 1 / 1 |

Sonuç: Açılışın son 5 dakikası kuralı (`03-tek-fiyat.md` madde 22) ve EBDKS durdurmasındaki kısıt (`06-devre-kesici.md` madde 44) veride istisnasız uygulanmıştır.

Kapanış seansı (`P_KAPANIS_EMIR_TPL*`, yeni emir ve değişiklik, fiyatlı):
- Son sürekli işlem fiyatının ±%3'ü (içe yuvarlanmış) içinde 888.155, dışında 395 (%0,04; 326 değişiklik, 69 yeni emir).
- Son sürekli işlemi olmayan sıralarda 21.252 satırın tamamı günlük sınır içindedir (madde 74).

Kapanış fiyatından işlemler (`P_KAPANIS_FIY_ISLEM`):
- 183.942 yeni emrin tamamı kapanış fiyatındandır (madde 88).
- Değişikliklerde fiyat kötüleştirme 1 kez görülür. İyileştirme (kapanış fiyatına çekme) 37.501 kez görülür; bunun 312'si miktar artışıyla birliktedir.
- Kapanış fiyatından farklı fiyatla kalan değişiklik 1.783'tür (madde 91'e göre bunlar yalnız azaltma olabilir; miktar yönü bu alt kümede ayrıca ayrıştırılmadı).

Açılışta yeni emir, pazar × fiyat türü:

| Pazar | Limit | Piyasa | Piyasadan limite | Dengeleyici |
|---|---|---|---|---|
| Z | 4.524.962 | 89.956 | 9.378 | 401 |
| N | 2.074.231 | 29.970 | 5.041 | 190 |
| T | 231.964 | 0 | 0 | 11 |
| W | 53.297 | 0 | 0 | 19 |
| S | 54.010 | 0 | 0 | 13 |

Sistem kaynaklı sebeplerin veride görülen anlamı (önceki satırla fark):

| Sebep | Görülen anlam |
|---|---|
| 13 | Kısmi görünme koşullu emirde görünen kısmın işlem sonrası yenilenmesi; satır işlem taşır, kalan azalır. 330.039'u sürekli işlemde |
| 8 | Piyasadan limite emrin kalanının limit emre dönüşmesi; fiyat işlem fiyatı olur, fiyat türü 1 |
| 9, 34 | Müzayede eşleştirmesinden sonra kalan emrin sistemce iptali |
| 4 | Pasifleştirme (`emir_durumu` 4), sürekli işlemde 18.542 |
| 116 | Sürekli işlemde sistem iptali (15.750); anlamı referans tablosunda yok |
| 117 | EBDKS durdurmasında (`P_GECICI_DURDUR_EBDK`) iptal (38.051); sürekli işlemde 4.093; anlamı referans tablosunda yok |

## 9 Sürekli işlemde fiyat-zaman önceliği (`gunici_oncelik_kontrol.py`)

Kapsam: 03.03, 19.03 ve 27.03.2025; bütün `.E` sıraları.

Yöntem:
- Sürekli işlem defteri emir satırlarından yeniden kuruldu.
- İşlem defterinde pasif (`aktif_pasif = P`) olarak görünen her gerçekleşmede, o andan hemen önceki defter durumuna bakıldı.
- Denetlenen iki koşul:
  - **Fiyat önceliği:** gerçekleşen emirlerden daha iyi fiyattaki bütün emirler aynı anda gerçekleşmiş olmalıdır.
  - **Zaman önceliği:** fiyat seviyesinde gerçekleşen emirler, öncelik sırasının ilk emirleri olmalıdır.

| Kontrol / öncelik zamanı modeli | Tutan / 9.636.513 | Oran |
|---|---|---|
| Fiyat önceliği | 9.636.368 | %99,998 |
| M1: `emir_giris_zamani` | 7.427.444 | %77,08 |
| M2: yeni emir; fiyat değişikliği veya `emir_miktari` artışında sıfırlanır | 9.570.064 | %99,31 |
| M3: her değişiklikte sıfırlanır | 9.559.023 | %99,20 |
| M4: yeni emir; fiyat değişikliği veya **kalan** miktar artışında sıfırlanır | 9.577.033 | %99,38 |
| **M5: M4 + kısmi görünme yenilemesinde (sebep 13) sıfırlanır** | **9.613.155** | **%99,76** |

- M5 ihlallerinin 23.358'inin 22.941'inde (%98,2) seviyede sebep 13 yenilemesi görmüş bir emir vardır. Görünen kısım büyüklüğü veride yazılı olmadığından bu emirlerin önceliği tam modellenemez.
- Kalan 417 ihlal (%0,004) ve 145 fiyat önceliği istisnası, aynı mikrosaniyedeki olayların sırasının bilinmemesiyle uyumludur; ayrıca incelenmedi.

Sonuçlar (`04-surekli-islem.md` madde 15–16, 20–22, 30):
- Fiyat önceliği istisnasız geçerlidir.
- Zaman önceliği fiyat değişikliğinde ve kalan miktarın artmasında kaybolur; miktar azaltmada korunur.
- Kısmi görünme koşullu emirde görünen kısım yenilenince emir seviyenin sonuna gider.
- Örnek (AGROT.E, 03.03 14:30:23): emir miktarı 50.435'ten 10.905'e düşürülmüş, ancak işlemlerden sonra kalan 96 olduğundan kalan 10.905'e çıkmıştır. Bu değişiklik öncelik kaybettirmiştir; yani "miktar artışı" kalan miktara göre değerlendirilir.

## 10 Tek fiyat (müzayede) defterinin yeniden kurulması (`tek_fiyat_algoritma.py`, `gunici_tek_fiyat_kontrol.py`, `gunici_tek_fiyat_ozet.py`)

ITCH'te emir toplama aşamasındaki emirler yayımlanmadığından bu kontrol 2018 verisiyle yapılamamıştı. Gün içi emir verisinde bütün emir olayları vardır.

Yöntem:
- **Eşleştirme anı M:** her emir toplama koşusunu izleyen ilk eşleştirme satırının zamanı. Eşleştirme satırı yoksa son toplama satırı + 1 µs alınır.
- **Defter:** M'den önce her emrin son satırı alınır; `emir_durumu` = 1 ve kalan > 0 olanlar defterdedir.
  - Piyasa emri ve fiyatsız piyasadan limite emri piyasa emri sayılır.
  - Dengeleyici ve orta nokta emirleri hesaplamaya alınmaz.
- **Algoritma:** `tek_fiyat_algoritma.py`, `03-tek-fiyat.md` Bölüm D.
  - Adım 3: aday seviyelerde kalan miktarın yönü (kullanıcı kararı).
  - Adım 6: en düşük limit − 1 adım ile en yüksek limit + 1 adım arası.
  - Adım 7: sınırlar.
  - Ek-16'nın beş örneğinin hepsini doğru verir.
- **Gerçekleşen:** M − 1 sn … M + 300 sn içindeki eşleştirme işlemlerinin fiyatı (tek fiyat) ve toplam miktarı.
- **Dengeleyici emirler:** belirlenen fiyatta kalan tarafla, sonra birbirleriyle eşleşir (madde 52–55). Bu eşleşme miktara eklenir.

Varyantlar (fiyat uyan müzayede sayısı; tüm müzayedeler):

| Sınıf | Müzayede | Kotasyon dâhil, baz, sınırlı | Kotasyon hariç, baz, sınırsız | Kotasyon hariç, son işlem, sınırlı | **Kotasyon hariç, baz, sınırlı** |
|---|---|---|---|---|---|
| Açılış | 12.275 | 12.238 | 12.230 | 12.238 | **12.238** |
| Kapanış | 12.188 | 11.819 | 11.794 | 12.151 | **12.169** |
| Gün içi tek fiyat (5 kez tek fiyat) | 2.056 | 2.056 | 2.004 | 2.044 | **2.056** |
| EBDKS tek fiyatı | 2.214 | 2.203 | 2.195 | 2.203 | **2.204** |
| Pay bazında devre kesici | 1.122 | 997 | 1.003 | 998 | **998** |

"Sınırlı" şu demektir:
- günlük fiyat sınırları (±%10);
- kapanış seansında ayrıca son işlem fiyatının ±%3'ü, içe yuvarlanmış (madde 72).

Kapanış ±%3 bandı eklenmeden önce kapanışta 12.188'in 12.149'unda fiyat tutuyordu. Temiz kapanışlardaki 25 uyumsuz vakanın 20'sinde gerçek fiyat, son işlem fiyatının ±%3 sınırındaydı (sapma %2,6–%3,0).

Son sütun açıklanan dışlamalar ayrılarak:

| Sınıf | Müzayede | Özsermaye hâli | EBDKS ile kesilen | Kalan | Fiyat uyan | Miktar uyan |
|---|---|---|---|---|---|---|
| Açılış | 12.275 | 28 | 18 | 12.229 | 12.222 | 12.224 |
| Kapanış | 12.188 | 27 | 0 | 12.161 | 12.156 | 12.157 |
| Gün içi tek fiyat | 2.056 | 4 | 0 | 2.052 | 2.052 | 2.052 |
| EBDKS tek fiyatı | 2.214 | 10 | 0 | 2.204 | 2.204 | 2.203 |
| Pay bazında devre kesici | 1.122 | 10 | 125 | 987 | 987 | 987 |
| **Toplam** | **29.855** | 79 | 143 | **29.633** | **29.621 (%99,96)** | 29.623 |

Dışlama ölçütleri:
- **Özsermaye hâli:** bedelsiz/temettü günü. Gün sonu dosyasındaki önceki kapanış düzeltilmemiş olduğundan baz fiyat ve sınırlar yanlış çıkar.
- **EBDKS ile kesilen:** emir toplama koşusundan sonra EBDKS durdurması gelir; eşleştirme yapılmamıştır.

Bulgular:
1. **Algoritma Adım 1–4 veriyle uyumludur.** Karar adımına göre (temiz müzayedeler, fiyat uyan / toplam):

   | Karar adımı | Fiyat uyan / toplam |
   |---|---|
   | Adım 1 | 20.640 / 20.643 |
   | Adım 2 | 5.640 / 5.641 |
   | Adım 3 | 2.910 / 2.915 |
   | Adım 4, yön Eşit | 142 / 142 |
   | Adım 4, yön karışık | 2 / 4 |
   | Fiyat oluşmaz (en çok işlem 0) | 285 / 286 |
   | Aday aralık boş | 2 / 2 |
2. **Adım 4'teki referans fiyat baz fiyattır (önceki kapanış).** Adım 4'e düşen 146 müzayedede:
   - baz fiyatla 144'ü,
   - M öncesi son işlem fiyatıyla (kapanışta son sürekli işlem, gün içi tek fiyatta önceki tek fiyat) 113'ü tutar;
   - iki referansın farklı olduğu vaka sayısı 136'dır.

   Bu, açılış, kapanış, gün içi tek fiyat ve EBDKS tek fiyatı için aynıdır. Referansa eşit uzaklıkta iki seviye kalan vaka ve Adım 5'e (referans yok) düşen vaka bu ayda yoktur.
3. **Adım 7 uygulanır.** Sınırsız varyantta kapanış ve gün içi tek fiyatta uyum düşer. Kapanışta sınır, son işlem fiyatının ±%3'üdür (içe yuvarlanmış).
4. **Adım 3 (yön) kullanıcı kararıyla uyumludur.** 2.915 Adım 3 kararının 2.910'u tutar.
5. **Yönün karışık olduğu durumlar (aday seviyelerde alış ve satış fazlası birlikte; kaynakta tanımsız, `03-tek-fiyat.md` Açık sorular):** 4 vaka vardır (3 BYF açılışı, 1 ISBTR gün içi tek fiyat).
   - Dördünde de gerçek fiyat, kalan miktarın alış fazlasından satış fazlasına döndüğü iki komşu seviyeden biridir.
   - Kullanıcı kararıyla (21.10.2026) uygulanan kural: referansa (baz) / son işlem fiyatına en yakın aday; eşitlik sürerse orta nokta. Betik `gunici_tek_fiyat_karisik.py`, çıktı `gunici-dogrulama/2025-03/tek-fiyat/yon_karisik.csv`.
   - Kurala uyan: ISBTR.E 14.03 (baz referansla) ve Z30KP.F 17.03.
   - İstisna (`yon_karisik_istisna = 1`): ZPBDL.F 14.03 ve ZRE20.F 21.03. İkisi de öncesinde işlem olmayan BYF açılışıdır.
   - Eşitlik (orta nokta) hiçbir vakada oluşmadı.
6. **Dengeleyici emirler:** dengeleyici emir bulunan 1.272 müzayedede gerçekleşen miktar, denge miktarından büyüktür. Dengeleyicilerin kalan tarafla ve birbirleriyle eşleşmesi eklenince, fiyatı tutan müzayedelerde miktar uyumu 28.827'den 29.365'e çıkar (madde 52–55 doğrulanır).
7. **Kotasyonlar (kategori 4):**
   - Kotasyonlu müzayede sayısı 447'dir: kapanışta 400 BYF (`.F`), 19 emtia sertifikası (`.S1`) ve 20 pay; ayrıca 5 EBDKS ve 3 devre kesici müzayedesi.
   - Kotasyonlar dâhil edildiğinde kapanışta uyum 12.169'dan 11.819'a düşer.
   - Veride kotasyonun geçersizleşmesi ayrı bir satırla yazılmadığından, kotasyonlar dâhil edilince eski kotasyonlar da defterde kalır.
   - Kotasyonların kapanış müzayedesine katılıp katılmadığı bu veriden ayırt edilemez (Adım 8 "kotasyonlar dâhil" der).
8. **Açıklanmayan 12 vaka (%0,04):**
   - 5'i 19.03 BYF açılışıdır; EBDKS 09:55:25'te, BYF eşleştirmesinden (09:56) önce tetiklenmiştir ve ölçüt bunları ayıramamıştır.
   - 2'si karışık yön istisnasıdır (bulgu 5; `yon_karisik_istisna = 1`).
   - 2'si kotasyonlu BYF kapanışıdır (OPTGY.F).
   - 3'ü PÖİP/Alt Pazar kapanışında Adım 3 farkıdır (SODSN.E 06.03, OYAYO.E 19.03, AKSUE.E 27.03).
   - Liste: `gunici-dogrulama/2025-03/tek-fiyat/aciklanmayan_uyumsuz.csv`.

## 11 Pay bazında devre kesici (`gunici_seans_akis_kontrol.py`, `gunici_devre_kesici_kontrol.py`)

1.195 olay görüldü (Ana 610, Yıldız 423, Alt 162). Tetikleme anı T, devre kesici bölümüne geçişten önceki son sürekli işlem satırıdır.

| Ölçüm | Sonuç |
|---|---|
| Yön | 1.184 olayın (referansı bulunan) tamamı **düşüş** yönlü. Gün boyu sürekli işlemlerin son müzayede fiyatına göre en büyük düşüşü her pazarda tam −%5,00; yukarı yönde sapma %22'ye kadar çıkar (yukarı yönlü devre kesici çalışmaz) |
| Oran | T öncesi son sürekli işlem fiyatının referansa (son müzayede fiyatı) oranı: medyan −%4,9, en büyük −%5,00 (Z, N, T aynı) |
| Emir toplama süresi | T'den eşleştirmeye 899–929 sn: 15 dk + 0–29 sn (Z, N, T aynı) |
| Eşleştirme bölümü | Eşleştirme anı T + 15:00 + rastlantısal 0–30 sn. Sürekli işleme dönüş her olayda T + 17:00 (eşleştirme + dönüş = 119,5–119,9 sn). Yani 2 dk'lık eşleştirme bölümü içinde ilk 30 sn'de rastlantısal kesim (5.3.4 metniyle aynı) |
| Kapanışa taşma | T ≥ 17:40 olan 29 olayda ayrı eşleştirme yoktur; emir toplama kapanış seansına aktarılır. En geç ayrı eşleştirmeli tetikleme 17:39, en erken taşan 17:40:59 (Z dâhil) |
| EBDKS ile kesişme | 138 olay EBDKS durdurmasıyla kesilir (bkz. 12) |

Mart 2025 düzeni yürürlükteki metinden (`06-devre-kesici.md`) farklıdır: oran %5 yalnız düşüşte (Tablo-4: %10 / %7,5 / %5), emir toplama 15 dk (yürürlükteki 10 dk; eski metin Yıldız 5, Ana/Alt 15), rastlantısal eşleştirme. Kullanıcı kararı (21.10.2026): fiili eşikler kullanılır; eşleştirme sabit emir toplama + tarihe bağlı rastlantısal pencere ile modellenir (`../motor/tarih_parametreleri.csv`). Bkz. 13.

## 12 Endekse bağlı devre kesici (EBDKS)

19.03.2025 ve 21.03.2025'te ikişer kez çalışmıştır. Bölüm koşularından çıkarılan zamanlar:

| Olay | Tetikleme T (yaklaşık) | `.E` tek fiyat emir toplama (`P_TF_EMIR_TPL_EBDK`) | Eşleştirme (`P_ESLESTIRME_EBDK`) | `.E` sürekliye dönüş | `.V/.C/.F` sürekliye dönüş |
|---|---|---|---|---|---|
| 19.03 – 1 | 09:55:25 (açılış eşleştirmesi sırasında) | 10:20:00 | 10:25:08 | 10:30:00 | 10:30:00 |
| 19.03 – 2 | ≈14:08 | ≈14:28 | 14:33:20 | ≈14:38 | 14:38:10 |
| 21.03 – 1 | 10:52:12 | 11:12:12 | 11:17:22 | 11:22:12 | 11:22:12 |
| 21.03 – 2 | ≈11:27:12 | ≈11:47:12 | 11:52:24 | ≈11:57:2 | 11:57:14 |

- `.E` sıraları T + 20 dk durdurulur (`P_GECICI_DURDUR_EBDK`), sonra 5 dk tek fiyat emir toplama yapılır. Eşleştirme sonraki 5 dk'nın başında 8–24 sn rastlantısal gecikmeyle başlar. Sürekli işleme dönüş T + 30 dk'dır.
- `.V/.C/.F` sıraları T + 30 dk durdurulur (`P_GECICI_DUR_EBDK_KT`). Bu sırada kotasyon ve fiyat kötüleştirme/miktar azaltma vardır.
- `.R` sırası `P_GECICI_DUR_EBDK_SI` bölümüne girer.
- 19.03'teki ilk olay açılış eşleştirmesi sırasında tetiklenmiştir. `.E` açılışları eşleşip (madde 31) 10:00 + 20 dk = 10:20'de tek fiyata geçmiştir. BYF açılışı (09:56) ise eşleşmeden durdurulmuştur.
- Aynı gün ikinci kez çalışma, eski metindeki iki eşikli düzene (%5 ve %7) uyar; yürürlükteki metinde tek eşik (%6) vardır ve ikinci kez çalışmaz (madde 28).
- Süreler Ek-21 Rev. 51 eski metniyle aynıdır (`.E` 20 dk, `.V/.C/.F/.R` 30 dk); yürürlükteki metin 10 dk / 20 dk'dır.
- Eşik hesabı (BIST 100 değeri) veride yoktur, sınanmadı.

## 13 Tarihe bağlı parametreler (Mart 2025 ↔ yürürlükteki metin)

Kullanıcı kararı (21.10.2026): veride gözlenen fiili değerler esas alınır. Fark "Borsa İstanbul Pay Piyasası Prosedürü Tablo-4 dipnotundaki geçici duyuru/uygulama farkı" olarak kayda geçer. Makine okunur tablo: `../motor/tarih_parametreleri.csv`.

| Parametre | Mart 2025 (veri) | Yürürlükteki Prosedür | Kaynak notu |
|---|---|---|---|
| Fiyat marjı (paylar, tüm pazarlar; BYF, GSF) | ±%10 | Tablo-4: Yıldız %20, Ana %15, Alt/YİP/PÖİP %10; BYF %20 | Tablo-4 dipnot (9), "ikinci bir duyuruya kadar geçerli" duyurulara (2020/20, 2020/21, 2020/50 ...) atıf yapar; duyuru metinleri elde yok |
| Pay bazında DK yönü ve oranı | Yalnız düşüş, %5 (tüm pazarlar) | İki yönlü; %10 / %7,5 / %5 | Aynı |
| Pay bazında DK emir toplama | 15 dk (tüm pazarlar) + 2 dk eşleştirme (rastlantısal 30 sn) | 10 dk + 2 dk | Ek-21 eski metin Yıldız 5, Ana/Alt 15 dk; veri 15 dk |
| DK'nın kapanışa taşması | T ≥ 17:40 | 17:45–18:00 (uzatma 15 dk) | Eski metin: Ana/Alt 17:40, Yıldız 17:50 |
| EBDKS | İki eşik, `.E` 20 dk, `.V/.C/.F/.R` 30 dk | Tek eşik %6, 10 dk / 20 dk | Ek-21 Rev. 51 (2025/38860, 01.09.2025) eski metin |
| Açığa satış | 03–21.03: yalnız 50 payda (hepsi BIST 100 içinde; gün başına 358 bin–1,01 milyon yeni açığa satış emri); 24.03'ten itibaren yeni açığa satış emri ve işlemi 0 | Ayrı düzenleme (SPK) | `DURUM.md` notu: BIST 50 için 02.01.2025'te serbest, 24.03.2025'te tüm paylarda yasak; veri birebir uyar |
| Varant `P_SALTKOTASYON` başlangıcı | 07.03.2025'ten itibaren 10:00:10 | 10:00:10 | Ek-21 (2025/33431) |
| Fiyat adımı | Tablo-7 / Tablo-8 (güncel) birebir | Tablo-7 / Tablo-8 | 06.11.2023 değişikliği (Ek-21); 2018 ITCH eski tabloya uyar |
