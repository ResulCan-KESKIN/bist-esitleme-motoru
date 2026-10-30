"""Anlatim md -> yazdirmaya hazir HTML (kapak, icindekiler, ic ice listeler, tablolar, kod bloklari, kutular).

Kullanim: md2html.py KAYNAK.md CIKTI.html stil.css
KAYNAK basinda on bilgi: ---\nkisa: ...\nalt: ...\ntarih: ...\n---
"> " ile baslayan satirlar kutu (benzetme / ornek / akilda kalsin) olur.
"""
import html, re, sys

KAYNAK, CIKTI, STIL = sys.argv[1], sys.argv[2], sys.argv[3]

LISTE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
AYRAC = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")


def satir_ici(s):
    kodlar = []

    def kod(m):
        kodlar.append(html.escape(m.group(1)))
        return f"\x00{len(kodlar) - 1}\x00"

    s = re.sub(r"`([^`]+)`", kod, s)
    s = html.escape(s, quote=False)
    s = s.replace("\\|", "|")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{kodlar[int(m.group(1))]}</code>", s)


def girinti(s):
    return len(s) - len(s.lstrip(" "))


def hucreler(s):
    return [c.strip() for c in re.split(r"(?<!\\)\|", s.strip().strip("|"))]


basliklar = []


def bloklar(L):
    out, i = [], 0
    while i < len(L):
        s = L[i]
        if not s.strip():
            i += 1
            continue
        if s.strip().startswith("```"):
            j = i + 1
            while j < len(L) and not L[j].strip().startswith("```"):
                j += 1
            ic = min((girinti(x) for x in L[i + 1:j] if x.strip()), default=0)
            out.append("<pre>" + html.escape("\n".join(x[ic:] for x in L[i + 1:j])) + "</pre>")
            i = j + 1
            continue
        if s.lstrip().startswith(">"):
            j, ic = i, []
            while j < len(L) and L[j].lstrip().startswith(">"):
                ic.append(re.sub(r"^\s*>\s?", "", L[j]))
                j += 1
            out.append('<div class="kutu">' + "".join(bloklar(ic)) + "</div>")
            i = j
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            n, metin = len(m.group(1)), m.group(2)
            kimlik = f"b{len(basliklar)}"
            basliklar.append((n, metin, kimlik))
            out.append(f'<h{n} id="{kimlik}">{satir_ici(metin)}</h{n}>')
            i += 1
            continue
        if s.strip() == "---":
            out.append('<hr>')
            i += 1
            continue
        if s.strip().startswith("|") and i + 1 < len(L) and AYRAC.match(L[i + 1].strip()):
            bas = hucreler(s)
            j, govde = i + 2, []
            while j < len(L) and L[j].strip().startswith("|"):
                govde.append(hucreler(L[j]))
                j += 1
            t = ["<table><thead><tr>" + "".join(f"<th>{satir_ici(c)}</th>" for c in bas) + "</tr></thead><tbody>"]
            t += ["<tr>" + "".join(f"<td>{satir_ici(c)}</td>" for c in r) + "</tr>" for r in govde]
            out.append("".join(t) + "</tbody></table>")
            i = j
            continue
        m = LISTE.match(s)
        if m:
            ic, sirali = len(m.group(1)), m.group(2)[0].isdigit()
            ogeler, j = [], i
            while j < len(L):
                m2 = LISTE.match(L[j])
                if not m2 or len(m2.group(1)) != ic or m2.group(2)[0].isdigit() != sirali:
                    break
                icerik_col = ic + len(m2.group(2)) + 1
                parca = [m2.group(3)]
                k = j + 1
                while k < len(L):
                    x = L[k]
                    if not x.strip():
                        # bos satirdan sonra girintili devam varsa ogeye aittir
                        n_ = k + 1
                        while n_ < len(L) and not L[n_].strip():
                            n_ += 1
                        if n_ < len(L) and girinti(L[n_]) > ic:
                            parca += [""] * (n_ - k)
                            k = n_
                            continue
                        break
                    if girinti(x) <= ic:
                        break
                    parca.append(x[min(icerik_col, girinti(x)):])
                    k += 1
                ogeler.append(parca)
                j = k
                # ayni listenin ogeleri arasinda bos satir olabilir
                while j < len(L) and not L[j].strip():
                    n_ = j + 1
                    if n_ < len(L) and LISTE.match(L[n_]) and len(LISTE.match(L[n_]).group(1)) == ic:
                        j = n_
                    break
            etiket = "ol" if sirali else "ul"
            bas_no = int(m.group(2)[:-1]) if sirali else 1
            ek = f' start="{bas_no}"' if sirali and bas_no != 1 else ""
            li = []
            for parca in ogeler:
                ilk, kalan = parca[0], parca[1:]
                # ilk satira bitisik devam satirlari (liste/tablo/kod degilse) ayni paragraftir
                devam = []
                while kalan and kalan[0].strip() and not LISTE.match(kalan[0]) and not kalan[0].strip().startswith(("|", "```", ">")):
                    devam.append(kalan.pop(0).strip())
                metin = satir_ici(" ".join([ilk] + devam))
                ic_html = "".join(bloklar(kalan)) if any(x.strip() for x in kalan) else ""
                li.append(f"<li>{metin}{ic_html}</li>")
            out.append(f"<{etiket}{ek}>" + "".join(li) + f"</{etiket}>")
            i = j
            continue
        # paragraf
        p = [s.strip()]
        j = i + 1
        while j < len(L) and L[j].strip() and not LISTE.match(L[j]) and not L[j].strip().startswith(("|", "```", "#", ">")) \
                and L[j].strip() != "---":
            p.append(L[j].strip())
            j += 1
        out.append(f"<p>{satir_ici(' '.join(p))}</p>")
        i = j
    return out


L = open(KAYNAK, encoding="utf-8").read().split("\n")
on = {}
if L[0].strip() == "---":
    k = L.index("---", 1)
    for x in L[1:k]:
        a, _, d = x.partition(":")
        on[a.strip()] = d.strip()
    L = L[k + 1:]
govde = bloklar(L)

# ilk h1 kapakta; belgedeki h1 kaldirilir, ilk h2'ye kadar olan kisim "Bu belge hakkinda" kutusuna gider
govde = [b for b in govde if not b.startswith("<h1")]
k = next(i for i, b in enumerate(govde) if b.startswith('<h2'))
giris, govde = govde[:k], govde[k:]
icindekiler = []
for n, metin, kimlik in basliklar:
    if n == 2:
        icindekiler.append(f'<li class="t2"><a href="#{kimlik}">{satir_ici(metin)}</a></li>')
    elif n == 3:
        icindekiler.append(f'<li class="t3"><a href="#{kimlik}">{satir_ici(metin)}</a></li>')

kisa = on.get("kisa", "Anlatım")
CSS = open(STIL, encoding="utf-8").read().replace('content: "Sistemin anlatımı"', f'content: "{kisa}"')
sayfa = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>{html.escape(kisa)}</title><style>{CSS}</style></head>
<body>
<section class="kapak">
  <div class="ust">Bilgisayar Mühendisliği Bitirme Projesi</div>
  <h1 class="baslik">Borsa İstanbul Pay Piyasası Kurallarına Uygun Eşleştirme Motoru ve Makine Öğrenmesi Destekli Piyasa Manipülasyonu Tespit Sistemi</h1>
  <div class="belge">{html.escape(kisa)}</div>
  <div class="alt">{satir_ici(on.get("alt", ""))}</div>
  <div class="yazar">Resul Can KESKİN</div>
  <div class="tarih">{html.escape(on.get("tarih", ""))}</div>
</section>
<section class="onsoz"><h3>Bu belge hakkında</h3>{''.join(giris)}</section>
<section class="icindekiler"><h2 class="ic-baslik">İçindekiler</h2><ul>{''.join(icindekiler)}</ul></section>
<main>{''.join(govde)}</main>
</body></html>"""
open(CIKTI, "w", encoding="utf-8").write(sayfa)
print("basliklar:", len(basliklar), "blok:", len(govde))
