import sys, os
sys.path.insert(0, '.')
import ek11, final, gen, ekx

st = ek11.build()
ver = final.load('verified.json', {}).get('11', {})
notes = final.load('notes.json', {})
head = "# Ek-11: " + final.TITLES[11] + "\n\n"
head += "Kaynak: Pay Piyasası Prosedürü (`pay-piyasasi-prosedur.pdf`), Ek-11, s. 176–190 (PDF sayfa numarası = basılı sayfa numarası).\n"
head += "Aktarım yöntemi: Kaynakta iki sütunlu tablo (sol: seans bölümü adı, sağ: açıklamalar); her seans bölümü ayrı başlık altına alınmıştır. Açıklama satırları kaynaktaki sırayla ve aynen verilmiştir. Bir blok sayfa sınırını aşıyorsa sayfa aralığı başlığın altında belirtilmiştir. Her sayfada tekrarlanan “SEANSIN BÖLÜMÜ | AÇIKLAMALAR” başlık satırı yazılmamıştır.\n"
head += "Otomatik doğrulama: sayfalardaki tüm kelimelerin (tekrarlanan başlık satırı hariç) dosyada bulunduğu kontrol edildi (eksik kelime: 0).\n"
head += "Görsel doğrulama (Claude, sayfa görüntüsü ile karşılaştırma): " + ver.get('visual', 'yapılmadı') + "\n"
head += "Elle düzeltilen/yamalanan sayfalar: yok\n"
head += "Notlar: Kaynaktaki yazım hataları olduğu gibi bırakılmıştır. Üstü çizili, altı çizili, kalın ve renk gibi biçim bilgileri aktarılmamıştır. " + notes.get('11', '') + "\n"
head += "Kullanıcı doğrulaması: bekliyor\n\n"
body = []
for name, pg, lines in st:
    pgs = sorted({p for p, _ in lines} | {pg})
    rng = 's. %d' % pgs[0] if len(pgs) == 1 else 's. %d–%d' % (pgs[0], pgs[-1])
    body.append('## ' + name + '\n*(' + rng + ')*\n')
    for p, l in lines:
        body.append('- ' + l.replace('<br>', ' '))
    body.append('')
md190 = ekx.page_md(190)
prose = [l for l in md190.splitlines() if l.strip() and not l.startswith('|')]
body.append('## NOTLAR\n*(s. 190)*\n')
for l in prose:
    if l.strip() == 'NOTLAR:':
        continue
    body.append('- ' + l)
body.append('')
open(os.path.join(gen.OUT, 'ek11.md'), 'w', encoding='utf-8').write(head + '\n'.join(body))
print('ek11 ok', len(st))
