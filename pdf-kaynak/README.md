# PDF kaynakları

Proje kökündeki dört PDF'in kaynakları ve üretim betiği.

| PDF | Kaynak | Not |
|---|---|---|
| `ANLATIM.pdf` | `../ANLATIM.md` + `ANLATIM-on-bilgi.md` (kapak bilgisi) | `ANLATIM.md`'nin doğrudan baskısıdır |
| `DURUM.pdf` | `DURUM-anlatim.md` | `DURUM.md`'nin baskısı değildir: ayrıca yazılmış sade anlatımıdır. `DURUM.md` değişince elle güncellenir |
| `TASARIM.pdf` | `TASARIM-anlatim.md` | `TASARIM.md`'nin sade anlatımıdır; `TASARIM.md` değişince elle güncellenir |
| `VERI.pdf` | `VERI.html` | `../VERI.md`'nin biçimli hâli; `VERI.md` değişince elle güncellenir (iki sayfaya sığacak biçimde) |

Diğer dosyalar:
- `md2html.py`: md → yazdırmaya hazır HTML (kapak, "Bu belge hakkında" kutusu, içindekiler, tablolar, kod blokları, `>` ile başlayan satırlardan sarı kutular). Kaynağın başındaki ön bilgi (`kisa`, `alt`, `tarih`) kapağa yazılır.
- `stil.css`: HTML'in stili (A4, sayfa başlığı `kisa` değeridir).
- `uret.py`: PDF'leri Microsoft Edge (headless) ile basar.

Üretim (proje klasöründe):

```
python -I pdf-kaynak/uret.py                    # dördü de, proje köküne
python -I pdf-kaynak/uret.py DURUM VERI         # yalnız seçilenler
python -I pdf-kaynak/uret.py --cikti KLASOR     # başka klasöre (deneme için)
```

Bir anlatımı güncellerken ön bilgideki `tarih`'i ve "Bu belge hakkında" bölümündeki tarihleri de güncelle. Tabloların GFM uyumlu olmasına dikkat et (başlık hücre sayısı = ayraç hücre sayısı); bozuk tablo PDF'te paragraf olarak çıkar.
