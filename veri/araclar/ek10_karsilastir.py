import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje"
# ek10 tablolari: baslik satiri (P_XXX | SAAT) ardindan 1..n satirlari
L = open(D + r"\ekler\ek10.md", encoding='utf-8').read().split('\n')
tabs = []
cur = None
page = 0
for l in L:
    m = re.match(r'\*\*\[Sayfa (\d+)', l)
    if m:
        page = int(m.group(1))
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    if len(c) == 2 and c[1] == 'SAAT':
        cur = {'name': c[0].split('<br>')[0], 'page': page, 'rows': []}
        tabs.append(cur)
        continue
    if cur and len(c) == 3 and re.fullmatch(r'\d+', c[0]) and re.fullmatch(r'\d\d:\d\d:\d\d', c[2]):
        cur['rows'].append((c[2][:5], c[1]))
    elif cur and l.startswith('|') and len(c) >= 1 and not re.fullmatch(r'-+', c[0]) and len(c) != 3:
        pass
print('ek10 akis tablosu:', len(tabs))
# itch akislari (states.py ciktisi)
S = open(r"C:\Users\Resul\AppData\Local\Temp\claude\E--DERSLER-7--D-NEM-Bitirme-Projesi-1-proje\fa4bf77e-0881-4ab3-ad84-86bc27d8532d\scratchpad\states_out.txt", encoding='utf-8').read().split('\n')
flows = []
cf = None
for l in S:
    m = re.match(r'# (\d+) ornek: (.*)', l)
    if m:
        cf = {'n': int(m.group(1)), 'ex': m.group(2), 'rows': []}
        flows.append(cf)
        continue
    m = re.match(r'\s+(\d\d:\d\d) (\S+)$', l)
    if m and cf:
        cf['rows'].append((m.group(1), m.group(2)))
for f in flows:
    rows = [r for r in f['rows'] if r[0] >= '07:00']  # gun basi P_GUNSONU satirlari hari\u00e7
    best = None
    for t in tabs:
        a = set(rows)
        b = set(t['rows'])
        d = len(a ^ b)
        if best is None or d < best[0]:
            best = (d, t)
    d, t = best
    print('\nITCH akisi n=%d %s' % (f['n'], f['ex'][:60]))
    print('  en yakin Ek-10 tablosu: %s (s.%d), fark satiri=%d' % (t['name'], t['page'], d))
    only_i = [r for r in rows if r not in t['rows']]
    only_e = [r for r in t['rows'] if r not in rows]
    print('  sadece ITCH :', only_i)
    print('  sadece Ek-10:', only_e)
