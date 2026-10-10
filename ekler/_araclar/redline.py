import sys, re
sys.path.insert(0, '.')
import ekx

HDR_L = ('ESKİ', 'Yürürlükteki')
HDR_NOISE = ('Pay', 'Piyasası', 'Direktörlüğü', 'Prosedür', 'TANIMLAR', 've', 'KISALTMALAR', 'LİSTESİ')


def rows_words(n):
    ws = ekx.words(n)
    foot = ekx._pdf.pages[n - 1].height - 65
    ws = [w for w in ws if not (w['top'] < 56 and w['text'] in HDR_NOISE)]
    ws = [w for w in ws if not (w['text'] == 'Sayfa' and w['top'] > foot)]
    ws = [w for w in ws if not (w['top'] > foot and re.match(r'^(\d+|/|380)$', w['text']))]
    ws.sort(key=lambda w: (w['top'], w['x0']))
    rows = []
    cur = []
    for w in ws:
        if cur and abs(w['top'] - cur[0]['top']) > 3:
            rows.append(cur)
            cur = []
        cur.append(w)
    if cur:
        rows.append(cur)
    for r in rows:
        r.sort(key=lambda w: w['x0'])
    return rows


def txt(ws, gap=14):
    if not ws:
        return ''
    s = ws[0]['text']
    p = ws[0]
    for w in ws[1:]:
        s += (' | ' if w['x0'] - p['x1'] > gap else ' ') + w['text']
        p = w
    return s


def page_md(n):
    pg = ekx._pdf.pages[n - 1]
    mid = pg.width / 2
    rows = rows_words(n)
    out = []
    L = []
    R = []
    state = {'mode': 'intro'}

    def flush():
        if L or R:
            out.append('**ESKİ METİN / Yürürlükteki metin (sol sütun)**')
            out.append('\n'.join(L) if L else '*(boş)*')
            out.append('')
            out.append('**YENİ METİN / Değişiklik (sağ sütun)**')
            out.append('\n'.join(R) if R else '*(boş)*')
            out.append('')
        del L[:]
        del R[:]

    for r in rows:
        left = [w for w in r if (w['x0'] + w['x1']) / 2 < mid]
        right = [w for w in r if (w['x0'] + w['x1']) / 2 >= mid]
        crossing = any(w['x0'] < mid - 4 and w['x1'] > mid + 4 for w in r)
        small_gap = bool(left and right and (right[0]['x0'] - left[-1]['x1']) < 14)
        t_all = txt(r)
        if left and left[0]['text'] in HDR_L and right and right[0]['text'] in ('YENİ', 'Yürürlükteki') and len(left) <= 4:
            flush()
            out.append('*(Sütun başlıkları: ' + txt(left) + ' | ' + txt(right) + ')*')
            out.append('')
            state['mode'] = 'table'
            continue
        full = crossing or small_gap or state['mode'] == 'intro' or t_all.startswith('Revizyon No')
        if full:
            flush()
            out.append(t_all)
            out.append('')
            if re.search(r'karşılaştırma cetvel', t_all) or re.search(r'yer almaktadır', t_all):
                state['mode'] = 'intro'
        else:
            if left:
                L.append(txt(left))
            if right:
                R.append(txt(right))
    flush()
    return '\n'.join(out)
