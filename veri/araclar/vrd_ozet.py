import struct, sys, io, collections, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08"


def parse(path):
    data = open(path, 'rb').read()
    pos = 0
    n = 0
    cnt = collections.Counter()
    lens = collections.defaultdict(collections.Counter)
    msgs = []
    while pos < len(data):
        if pos + 2 > len(data):
            print('  KESIK: dosya sonunda', len(data) - pos, 'bayt artik')
            break
        L = struct.unpack('>H', data[pos:pos + 2])[0]
        m = data[pos + 2:pos + 2 + L]
        if len(m) < L:
            print('  KESIK mesaj ofset', pos)
            break
        t = chr(m[0])
        cnt[t] += 1
        lens[t][L] += 1
        msgs.append(m)
        pos += 2 + L
    return data, pos, cnt, lens, msgs


for name in ['TM-1', 'TM-2', 'TR-1', 'TR-2']:
    p = D + r"\vrd\rewinder-files\%s.VRD" % name
    data, pos, cnt, lens, msgs = parse(p)
    print(name, 'bayt', len(data), 'tuketilen', pos, 'mesaj', len(msgs))
    print('  sayim', dict(cnt))
    print('  uzunluk (bayt, mesaj govdesi; uzunluk oneki haric)', {k: dict(v) for k, v in lens.items()})
