import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
MIN = -2147483648


def run(path, label):
    data = open(path, 'rb').read()
    pos = 0
    sec = 0
    state = {}
    tick = collections.defaultdict(list)
    lastZ = {}
    cross_state = collections.Counter()
    # auction tracking: book -> dict(zlast, trades list) ; flush on state change out of ESLESTIRME
    cur = {}
    res = collections.Counter()
    examples = []
    tickbad = collections.Counter()
    tickok = collections.Counter()
    while pos < len(data):
        L = u('>H', data[pos:pos + 2])[0]
        m = data[pos + 2:pos + 2 + L]
        pos += 2 + L
        t = chr(m[0])
        if t == 'T':
            sec = u('>I', m[1:5])[0]
            continue
        if t == 'L':
            b = u('>I', m[5:9])[0]
            tick[b].append((u('>Q', m[9:17])[0], u('>i', m[17:21])[0], u('>i', m[21:25])[0]))
        elif t == 'A':
            b = u('>I', m[13:17])[0]
            pr = u('>i', m[30:34])[0]
            ok = None
            for tk, f, to in tick[b]:
                if f <= pr and (pr <= to or to == 0):
                    ok = (pr % tk == 0)
                    break
            if ok is None:
                tickbad['aralik yok'] += 1
            elif ok:
                tickok['ok'] += 1
            else:
                tickbad['tick disi'] += 1
        elif t == 'Z':
            b = u('>I', m[5:9])[0]
            z = (u('>Q', m[9:17])[0], u('>Q', m[17:25])[0], u('>i', m[25:29])[0], u('>i', m[29:33])[0],
                 u('>i', m[33:37])[0], u('>Q', m[37:45])[0], u('>Q', m[45:53])[0], state.get(b))
            if z[2] != MIN:
                lastZ[b] = z
        elif t == 'O':
            b = u('>I', m[5:9])[0]
            st = m[9:29].decode().strip()
            old = state.get(b)
            zsave = lastZ.get(b)
            if old in ('P_ESLESTIRME', 'P_ESLESTIRMETEKFIYAT') and b in cur:
                c = cur.pop(b)
                tr = c['trades']
                z = c['z']
                key = c['from']
                if z is None:
                    res[(key, 'Z yok', 'islem var' if tr else 'islem yok')] += 1
                else:
                    eq = z[2]
                    vol = sum(q for q, p in tr)
                    prices = set(p for q, p in tr)
                    if not tr:
                        res[(key, 'islem yok', 'Z eq fiyat var' if eq != MIN else 'Z eq yok')] += 1
                    else:
                        res[(key, 'tek fiyat' if len(prices) == 1 else 'COKLU FIYAT',
                             'fiyat==Z' if prices == {eq} else 'fiyat!=Z',
                             'hacim==min(bid,ask)' if vol == min(z[0], z[1]) else ('hacim>min' if vol > min(z[0], z[1]) else 'hacim<min'))] += 1
                        if (prices != {eq} or vol != min(z[0], z[1])) and len(examples) < 6:
                            examples.append((b, key, z, tr[:5], vol))
            if st != 'P_ESLESTIRME' and st != 'P_ESLESTIRMETEKFIYAT':
                lastZ.pop(b, None)
            state[b] = st
            if st in ('P_ESLESTIRME', 'P_ESLESTIRMETEKFIYAT'):
                cur[b] = {'trades': [], 'z': zsave, 'from': old}
        elif t == 'P':
            b = u('>I', m[26:30])[0]
            q = u('>Q', m[18:26])[0]
            p = u('>i', m[30:34])[0]
            cross_state[(state.get(b), chr(m[49]))] += 1
            if b in cur:
                cur[b]['trades'].append((q, p))
    print('==', label)
    print('P cross bayragi / durum:', dict(cross_state))
    print('tick uygunlugu A fiyatlari:', dict(tickok), dict(tickbad))
    for k, v in sorted(res.items(), key=lambda x: -x[1]):
        print('  ', v, k)
    for e in examples:
        print('  ornek', e)


run(D + r"\TM-1.VRD", 'partition-1')
run(D + r"\TM-2.VRD", 'partition-2')
