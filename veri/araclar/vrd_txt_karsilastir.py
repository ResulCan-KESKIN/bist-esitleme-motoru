import struct, sys, io, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\veri\itch\2018-10-08"


def a(b):
    return b.decode('latin-1').rstrip(' ')


def decode(m, sec):
    t = chr(m[0])
    u = struct.unpack
    if t == 'T':
        return t, [str(u('>I', m[1:5])[0])], u('>I', m[1:5])[0]
    ns = u('>I', m[1:5])[0]
    ts = str(sec * 10**9 + ns)
    if t == 'S':
        return t, [ts, chr(m[5])], sec
    if t == 'R':
        f = [ts, str(u('>I', m[5:9])[0]), a(m[9:41]), a(m[41:73]), a(m[73:85]), str(m[85]), a(m[86:89]),
             str(u('>H', m[89:91])[0]), str(u('>H', m[91:93])[0]), str(u('>I', m[93:97])[0]),
             str(u('>I', m[97:101])[0]), str(u('>I', m[101:105])[0]), str(u('>Q', m[105:113])[0]),
             str(m[113]), str(u('>I', m[114:118])[0]), str(u('>i', m[118:122])[0]), str(u('>I', m[122:126])[0]),
             str(u('>H', m[126:128])[0]), str(m[128])]
        return t, f, sec
    if t == 'L':
        return t, [ts, str(u('>I', m[5:9])[0]), str(u('>Q', m[9:17])[0]), str(u('>i', m[17:21])[0]),
                   str(u('>i', m[21:25])[0])], sec
    if t == 'O':
        return t, [ts, str(u('>I', m[5:9])[0]), a(m[9:29])], sec
    if t == 'A':
        return t, [ts, str(u('>Q', m[5:13])[0]), str(u('>I', m[13:17])[0]), chr(m[17]), str(u('>I', m[18:22])[0]),
                   str(u('>Q', m[22:30])[0]), str(u('>i', m[30:34])[0]), str(u('>H', m[34:36])[0]), str(m[36])], sec
    if t == 'E':
        return t, [ts, str(u('>Q', m[5:13])[0]), str(u('>I', m[13:17])[0]), chr(m[17]), str(u('>Q', m[18:26])[0]),
                   str(u('>Q', m[26:34])[0]), str(u('>I', m[34:38])[0]), a(m[38:45]), a(m[45:52])], sec
    if t == 'D':
        return t, [ts, str(u('>Q', m[5:13])[0]), str(u('>I', m[13:17])[0]), chr(m[17])], sec
    if t == 'P':
        return t, [ts, str(u('>Q', m[5:13])[0]), str(u('>I', m[13:17])[0]), chr(m[17]), str(u('>Q', m[18:26])[0]),
                   str(u('>I', m[26:30])[0]), str(u('>i', m[30:34])[0]), a(m[34:41]), a(m[41:48]), chr(m[48]),
                   chr(m[49])], sec
    if t == 'Z':
        return t, [ts, str(u('>I', m[5:9])[0]), str(u('>Q', m[9:17])[0]), str(u('>Q', m[17:25])[0]),
                   str(u('>i', m[25:29])[0]), str(u('>i', m[29:33])[0]), str(u('>i', m[33:37])[0]),
                   str(u('>Q', m[37:45])[0]), str(u('>Q', m[45:53])[0])], sec
    raise ValueError(t)


def vrd_msgs(path):
    data = open(path, 'rb').read()
    pos = 0
    sec = 0
    while pos < len(data):
        L = struct.unpack('>H', data[pos:pos + 2])[0]
        m = data[pos + 2:pos + 2 + L]
        t, f, sec = decode(m, sec)
        yield t, f
        pos += 2 + L


def norm_txt(line):
    p = line.rstrip('\n').split(',')
    t = p[0]
    if t == 'T':
        return t, [p[1]]
    # ts: 2018-...(epoch)
    ts = re.search(r'\((\d+)\)', p[1]).group(1)
    q = [ts] + p[2:]
    # SYM(id) -> id ; semboller icinde virgul olmadigi varsayilir (kontrol asagida)
    out = []
    for x in q:
        m = re.fullmatch(r'(.+)\((\d+)\)', x)
        out.append(m.group(2) if m and x is not q[0] else x)
    return t, out


def compare(vrd, txt, label):
    n = 0
    bad = 0
    typ = collections.Counter()
    typbad = collections.Counter()
    first = {}
    it = iter(vrd_msgs(vrd))
    started = False
    with open(txt, encoding='latin-1') as fh:
        for line in fh:
            if not started:
                if line.startswith('T,'):
                    started = True
                else:
                    continue
            if line.startswith('on') or line.startswith('connection'):
                continue
            t, f = norm_txt(line)
            try:
                vt, vf = next(it)
            except StopIteration:
                print(label, 'VRD bitti ama TXT devam ediyor, satir', n)
                break
            n += 1
            typ[t] += 1
            ok = (t == vt)
            if ok:
                # R: TXT'de symbol/longname/isin dahil; vf ayni sirada
                ok = (f == vf)
                if not ok and t == 'R':
                    ok = (f == [x.strip() for x in vf])
            if not ok:
                bad += 1
                typbad[t] += 1
                if t not in first:
                    first[t] = (line.rstrip()[:200], vt, vf)
    rest = sum(1 for _ in it)
    print(label, 'karsilastirilan', n, 'farkli', bad, 'VRD artik mesaj', rest)
    print('  tip basina:', dict(typ))
    print('  tip basina fark:', dict(typbad))
    for k, v in first.items():
        print('  ilk fark', k, '\n    TXT:', v[0], '\n    VRD:', v[1], v[2])


compare(D + r"\vrd\rewinder-files\TM-1.VRD", D + r"\txt\itch-partition-1-2018-10-08-0000.txt", 'partition-1 / TM-1')
compare(D + r"\vrd\rewinder-files\TM-2.VRD", D + r"\txt\itch-partition-2-2018-10-08-0000.txt", 'partition-2 / TM-2')
