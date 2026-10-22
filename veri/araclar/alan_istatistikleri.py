import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack


def run(path, label):
    data = open(path, 'rb').read()
    pos = 0
    sec = 0
    C = collections.defaultdict(collections.Counter)
    books = {}          # book id -> {'sym','decp'}
    orders = {}         # (book, side, oid) -> [price, remaining, pos]
    nseq = 0
    lastts = 0
    nonmono = 0
    err = collections.Counter()
    ex_overflow = 0
    dup_add = 0
    del_unknown = 0
    exec_unknown = 0
    fully = 0
    state = {}
    while pos < len(data):
        L = u('>H', data[pos:pos + 2])[0]
        m = data[pos + 2:pos + 2 + L]
        pos += 2 + L
        t = chr(m[0])
        if t == 'T':
            s = u('>I', m[1:5])[0]
            if s < sec:
                err['T geri gitti'] += 1
            sec = s
            continue
        ns = u('>I', m[1:5])[0]
        ts = sec * 10**9 + ns
        if ts < lastts:
            nonmono += 1
        lastts = ts
        if ns >= 10**9:
            err['ns>=1e9'] += 1
        if t == 'R':
            bid = u('>I', m[5:9])[0]
            books[bid] = (m[9:41].decode('latin-1').strip(), u('>H', m[89:91])[0])
            C['R fin.product'][m[85]] += 1
            C['R cur'][m[86:89].decode()] += 1
            C['R decp'][u('>H', m[89:91])[0]] += 1
            C['R odd/round/block'][(u('>I', m[93:97])[0], u('>I', m[97:101])[0], u('>I', m[101:105])[0])] += 1
            C['R nominal'][u('>Q', m[105:113])[0]] += 1
            C['R legs'][m[113]] += 1
            C['R putcall'][m[128]] += 1
            C['R symbol sonek'][m[9:41].decode('latin-1').strip().rsplit('.', 1)[-1]] += 1
        elif t == 'L':
            C['L tick'][u('>Q', m[9:17])[0]] += 1
        elif t == 'O':
            bid = u('>I', m[5:9])[0]
            state[bid] = m[9:29].decode().strip()
            C['O state'][state[bid]] += 1
        elif t == 'A':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            rp = u('>I', m[18:22])[0]
            q = u('>Q', m[22:30])[0]
            pr = u('>i', m[30:34])[0]
            at = u('>H', m[34:36])[0]
            lt = m[36]
            C['A attr'][at] += 1
            C['A lot'][lt] += 1
            C['A side'][side] += 1
            C['A market(MIN_INT)'][pr == -2147483648] += 1
            C['A qty==0'][q == 0] += 1
            C['A durum'][state.get(bid, '?')] += 1
            k = (bid, side, oid)
            if k in orders:
                dup_add += 1
            orders[k] = [pr, q, rp]
        elif t == 'E':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            q = u('>Q', m[18:26])[0]
            mid = u('>Q', m[26:34])[0]
            cg = u('>I', m[34:38])[0]
            C['E combo'][cg] += 1
            C['E reserved'][(m[38:45], m[45:52])] += 1
            C['E durum'][state.get(bid, '?')] += 1
            k = (bid, side, oid)
            o = orders.get(k)
            if o is None:
                exec_unknown += 1
            else:
                o[1] -= q
                if o[1] < 0:
                    ex_overflow += 1
                if o[1] == 0:
                    fully += 1
                    del orders[k]
        elif t == 'D':
            oid = u('>Q', m[5:13])[0]
            bid = u('>I', m[13:17])[0]
            side = chr(m[17])
            k = (bid, side, oid)
            C['D durum'][state.get(bid, '?')] += 1
            if k in orders:
                del orders[k]
            else:
                del_unknown += 1
        elif t == 'P':
            C['P side'][chr(m[17])] += 1
            C['P combo'][u('>I', m[13:17])[0] != 0] += 1
            C['P reserved'][(m[34:41], m[41:48])] += 1
            C['P printable/cross'][(chr(m[48]), chr(m[49]))] += 1
            bid = u('>I', m[26:30])[0]
            C['P durum'][state.get(bid, '?')] += 1
        elif t == 'Z':
            bid = u('>I', m[5:9])[0]
            C['Z durum'][state.get(bid, '?')] += 1
        elif t == 'S':
            C['S event'][chr(m[5])] += 1
    print('==', label)
    print('zaman damgasi geri gitme:', nonmono, ' diger hata:', dict(err))
    print('A: ayni anahtarla tekrar ekleme', dup_add, '| E: bilinmeyen emir', exec_unknown, '| E: kalan<0', ex_overflow,
          '| D: bilinmeyen emir', del_unknown, '| tam gerceklesen', fully, '| gun sonunda defterde kalan', len(orders))
    for k, v in C.items():
        items = v.most_common(12)
        print(' ', k, items)


run(D + r"\TM-1.VRD", 'partition-1')
run(D + r"\TM-2.VRD", 'partition-2')
