import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack


def run(path, label):
    data = open(path, 'rb').read()
    pos = 0
    sec = 0
    state = {}
    book = collections.defaultdict(list)   # (bid, side) -> list of [oid, price, ts, qty]
    C = collections.Counter()
    ex = []
    deleted = set()
    readd = collections.Counter()
    while pos < len(data):
        L = u('>H', data[pos:pos + 2])[0]
        m = data[pos + 2:pos + 2 + L]
        pos += 2 + L
        t = chr(m[0])
        if t == 'T':
            sec = u('>I', m[1:5])[0]
            continue
        ts = sec * 10**9 + u('>I', m[1:5])[0]
        if t == 'O':
            state[u('>I', m[5:9])[0]] = m[9:29].decode().strip()
        elif t == 'A':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            rp = u('>I', m[18:22])[0]
            q = u('>Q', m[22:30])[0]
            pr = u('>i', m[30:34])[0]
            lst = book[(bid, side)]
            idx = rp - 1
            if idx < 0 or idx > len(lst):
                C['A konum aralik disi'] += 1
                idx = min(max(idx, 0), len(lst))
            lst.insert(idx, [oid, pr, ts, q])
            pf = True
            tf = True
            if idx > 0:
                p0 = lst[idx - 1]
                pf &= (p0[1] >= pr) if side == 'B' else (p0[1] <= pr)
                if p0[1] == pr:
                    tf &= p0[2] <= ts
            if idx < len(lst) - 1:
                n0 = lst[idx + 1]
                pf &= (n0[1] <= pr) if side == 'B' else (n0[1] >= pr)
                if n0[1] == pr:
                    tf &= n0[2] >= ts
            st = state.get(bid)
            if not tf:
                readd[('ihlal', (bid, side, oid) in deleted)] += 1
            readd[('tum A', (bid, side, oid) in deleted)] += 1
            C['A fiyat sirasi ihlali'] += (not pf)
            C[('A zaman sirasi ihlali', st)] += (not tf)
            C[('A toplam', st)] += 1
        elif t == 'E':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            q = u('>Q', m[18:26])[0]
            lst = book[(bid, side)]
            i = next((k for k, x in enumerate(lst) if x[0] == oid), None)
            if i is None:
                C['E emir yok'] += 1
                continue
            st = state.get(bid)
            C[('E sirasi', 'en onde (konum 1)' if i == 0 else 'onde baska emir var', st)] += 1
            lst[i][3] -= q
            if lst[i][3] <= 0:
                lst.pop(i)
        elif t == 'D':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            lst = book[(bid, side)]
            i = next((k for k, x in enumerate(lst) if x[0] == oid), None)
            if i is not None:
                lst.pop(i)
            deleted.add((bid, side, oid))
    print('==', label)
    for k, v in sorted(C.items(), key=lambda x: str(x[0])):
        print('  ', k, v)
    print('  daha once D ile silinmis ayni Order ID ile A:', dict(readd))
    for e in ex:
        print('  ornek uygunsuz', e)


run(D + r"\TM-1.VRD", 'partition-1')
run(D + r"\TM-2.VRD", 'partition-2')
