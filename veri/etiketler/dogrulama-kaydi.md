# SPK bülten etiketleri: elle doğrulama kaydı (12.10.2026)

Kapsam: `vaka_pencere_dogrulama.csv` (pencere 01.06.2024–31.05.2025 ile kesişen 47 benzersiz kayıt) ve `olay.csv` (20 kayıt). Her kayıt `spk_bulten_etiket.py` çıktısı ile bülten PDF metninin birimi (paragraf + tablo) yan yana okunarak karşılaştırıldı. Ayrıca 197 bültenin tümünde "dayanak ifadesi geçip de vaka çıkmayan bülten" ve "işaretçi sayısı ↔ çıkan kayıt sayısı" geri-çağırma kontrolü yapıldı.
Durum: pay kodları ve bağlantılar bu kayıtta doğrulandı; kod↔unvan sözlüğü (ITCH `R`) ile eşleme yapılmadı.

## Sonuç

Alan düzeyinde (pay kodu, karar türü, dönem, yasak başlangıcı, süre, kişi sayısı) 47 kaydın hiçbirinde hata bulunmadı. Hatalar sınıflandırma ve bağlama tarafındaydı; bulunup betikte düzeltildi:

| # | Bulgu | Etkilenen | Düzeltme |
|---|---|---|---|
| 1 | "Lisans ve Yetki Belgesi İptalleri" (V-101.1 md 17/1) suç duyurusu sanılıyordu | 2025-66 ve 17 kayıt daha | Yeni tür `lisans_iptali`, seviye D |
| 2 | Mevcut yasağın 6 ay uzatılması yeni tedbir sanılıyordu | 2025-14 NTHOL (+1) | Yeni tür `tedbir_uzatma`; başlangıç tarihi yok, A/B donörü olamaz |
| 3 | Etkin pişmanlık dipnotu (107/1, 107/3) 109 izinsiz faaliyet kayıtlarına 107 dayanağı olarak bulaşıyordu | 2026-6 | Dipnot metni dayanak aramadan önce çıkarılır |
| 4 | 22–26 paylık sosyal medya İPC listeleri tek tek paya bağlanıyor, başka vakalara yanlış bağlantı üretiyordu | 2025-15, 2025-38, 2025-49, 2024-50 (7 pay) | Kod sayısı > 5 ise seviye D (`muhtelif=1`), bağlanmaz |
| 5 | Bağlama yönü iki taraflıydı (İPC'yi sonraki tedbire bağlıyordu) | TUREX 2024-19, DZGYO, HATEK | Yalnızca önceden yayımlanmış A/B kaydı |
| 6 | Aynı payın iki tedbirinden yanlış olanına bağlanıyordu | KRGYO 2025-45 (27.02.2025 kararına atıf) | Metindeki "gg.aa.yyyy tarihli kararı ile" atfı, donörün bülten/başlangıç tarihiyle eşleşirse öncelikli |
| 7 | Olay: yeniden değerleme tablosu ve fiili dolaşımdaki pay ilke kararı olay sanılıyordu | 2024-60, 2025-68, 2026-57 | Konu ilk ~1100 karakterde ve açığa satış/geri alım dayanağıyla geçmeli |
| 8 | Olay: ilk duyuru "uzatma" sayılıyordu; başlıkta "A DUYURU" noktasız olan bülten atlanıyordu | 2025-16, 2026-11, 2026-13 | `uzatma` yalnızca "devam edilmesine"; başlık noktası isteğe bağlı |
| 9 | Karar tarihi referans verilen eski karardan alınıyordu | 2026-19, 2026-63 | Önce "… Kararı Uyarınca Yapılan Duyuru" ve "i-SPK … (gg.aa.yyyy … s.k.)" kalıpları |
| 10 | Alıntıda büyük harfli kişi adı kalıyordu | 2025-11 (TDGYO/KRGYO) | Maskeli TCKN'den önceki sözcükler maskelenir |

## Bağlantı güncellemesi (19.10.2026, kural 21–22)

Atıf edilen ilk karar arşiv (2024–2026) dışındaysa bağlantı kurulmaz; kayıt kendi bülten tarihindeki seviyesinde (C) kalır, donörden dönem devralınmaz. Aynı bültende aynı paya ait suç duyurusu, kesin tedbir kaydının donörüne bağlanır.

| Bülten | Pay | Tür | Önce | Sonra | Neden |
|---|---|---|---|---|---|
| 2025-55 | AVHOL | tedbir_kesin | 2024-52 (B), belirsiz | bağ yok, C | Yasak 05.06.2023 ve 18.08.2023 kararlarındaki yasakları düşüyor; bunlar arşiv dışı |
| 2025-55 | AVHOL | suç duyurusu | 2024-52 (B) | bağ yok, C | Aynı bültende kesin tedbir kardeşi bağsız (kural 22) |
| 2026-4 | CEOEM | tedbir_kesin | 2024-36 (B), belirsiz | bağ yok, C | 03.11.2023 tarihli ilk yasak arşiv dışı |
| 2026-4 | CEOEM | suç duyurusu | 2024-36 (B) | bağ yok, C | Kural 22 kardeş |
| 2025-32 | BJKAS | tedbir_kesin | 2024-20 (B), belirsiz | bağ yok, C | Atıf tarihleri donörle eşleşmiyor |
| 2025-32 | BJKAS | suç duyurusu | 2024-20 (B) | bağ yok, C | Kural 22 kardeş |
| 2025-45 | KRGYO | suç duyurusu | 2025-28 (B), belirsiz | 2025-11 (A) | Suç duyurusu 2025-11'deki yasaklı (27.02.2025 kararı) ile aynı kişi; 2025-28'deki yasaklı başka kişi |

Not: BJKAS donörü 2024-20 (22.04.2024) zaten pencere öncesidir; BJKAS 2024-38 ve 2026-4 İPC'leri 2024-20'ye bağlı kalmıştır (atıf yok, tek aday). AVHOL (2024-52) ve CEOEM (2024-36) donör kayıtlarının kendisi pencerededir ve etiketlidir; yalnızca sonradan gelen C kayıtların bağı koptuğu için pencere kod satırı 47 → 43 oldu, pay sayısı 27 kaldı.

Kalan belirsiz bağlantı (`baglanti_belirsiz=1`): 1 kayıt.

| Bülten | Pay | Tür | Bağlanan | Neden belirsiz |
|---|---|---|---|---|
| 2026-6 | ENSRI | ipc | 2025-22 | Aynı payda 2024-40 ve 2025-22 olmak üzere iki tedbir var; atıf yok, en yakın önceki seçildi |

Not: önceki "30 benzersiz vaka (A 5, B 25)" sayısı mevcut betik çıktısından aynı tanımla yeniden üretilemedi. Donör anahtarıyla (bağlı kayıtlar donörüne sayılır) hem öncesi hem sonrası 28 vaka (A 6, B 22) çıkıyor.

## Pencere sonucu (düzeltmelerden sonra)

28 benzersiz kaynak vaka (donör anahtarı), 27 pay: A 6, B 22 (19.10.2026 güncellemesi sonrası; bkz. yukarıdaki not). Paylar: ALKLC, AVHOL, BAKAB, BEGYO, CEOEM, CVKMD, DZGYO, EKSUN, ENSRI, EUREN, HATEK, HEDEF, IPEKE, KRGYO, KUYAS, NTHOL, OZATD, PEHOL, SEGMN, SMRTG, SONME, TATEN, TDGYO, TMSN, TUCLK, TUREX, VKFYO.

A seviyesi (açık dönem): ALKLC 04.02–18.03.2025 (suç duyurusu) ve 07.03–18.03.2025 (tedbir), KRGYO 10.01–25.02.2025, TDGYO 24.01–25.02.2025, EUREN 14–21.04.2025. Tümünde dönem bitişi yasak başlangıcından 1–3 gün öncedir.

## Olay tablosu

19 kayıt, hepsi kaynakla karşılaştırıldı. Öne çıkanlar:

- Açığa satış yasağı kökeni 06.02.2023'tür (Kurul kararı 6/155); 05.12.2024 kararıyla BIST 50 payları için 02.01.2025'ten itibaren kaldırıldı (2024-55). Yani pencerenin ilk yedi ayında (Haz–Ara 2024) tüm pay piyasalarında yasak vardı.
- 23.03.2025 kararıyla (2025-18) yasak tüm pay piyasalarında 24.03.2025–25.04.2025 arası yeniden getirildi, zincir: 25.04 → 30.05 → 04.07 → 29.08.2025 (son uzatma 2025-36).
- 19.03.2025'te pay geri alımını kolaylaştıran ilke kararı (i-SPK.22.9, 2025-16).
- 01.08.2024'te depremle ilgili geri alım ilke kararı (i-SPK.22.7) yürürlükten kaldırıldı (2024-37).
- 2026'da yeni zincir: 02.03.2026 başlangıç, 06.03 → 13.03 → 27.03 → 10.04 → 24.04 → 08.05 → 26.05 → 12.06 → 26.06.2026; sonrasında bültenlerde açığa satış yasağı anılmıyor (2026-60'ta yalnızca öz kaynak oranı esnetmesi, 2026-68'de 30.10.2026'ya kadar uzatma).

## Gözlemler

- Birkaç kişinin MKK sicil numarası birden fazla payda ve yıl içinde tekrar ediyor (örn. 2025-12 ve 2026-50 yasaklarında aynı numara). Bu, pay düzeyinde etiketin yanında kişi/hesap düzeyinde tekrar eden aktör bilgisi olduğunu gösterir; ITCH verisinde hesap kimliği yoksa kullanılamaz.
- Suç duyurusu ve kesin yasak bültenleri, ilk geçici yasaktan 1–2 yıl sonra gelir; pencerenin son aylarına ait kararlar Ekim 2026 itibarıyla eksiktir.
