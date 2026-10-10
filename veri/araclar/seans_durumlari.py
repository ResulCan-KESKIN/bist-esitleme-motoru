import re, sys, io, glob, collections, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje"
seq = collections.defaultdict(list)
names = {}
for f in sorted(glob.glob(D + r"\veri\itch\2018-10-08\txt\*.txt")):
    for l in open(f, encoding='latin-1'):
        if not l.startswith('O,'):
            continue
        p = l.rstrip('\n').split(',')
        ts = re.match(r'(\S+?)\(', p[1]).group(1)
        m = re.match(r'(.+)\((\d+)\)', p[2])
        sym, oid = m.group(1), m.group(2)
        t = datetime.datetime.strptime(ts[:26], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=3)
        seq[oid].append((t.strftime('%H:%M'), p[3]))
        names[oid] = sym
sig = collections.defaultdict(list)
for oid, s in seq.items():
    sig[tuple(s)].append(names[oid])
print('emir defteri', len(seq), 'farkli akis', len(sig))
for s, lst in sorted(sig.items(), key=lambda x: -len(x[1])):
    print('\n#', len(lst), 'ornek:', lst[:6])
    for a, b in s:
        print('   ', a, b)
allst = collections.Counter()
for s in seq.values():
    for a, b in s:
        allst[b] += 1
print(sorted(allst))
