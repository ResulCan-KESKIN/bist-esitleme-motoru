import struct, sys, io, collections, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
def fmt(ns):
    s=ns/1e9+3*3600
    return datetime.datetime.utcfromtimestamp(s).strftime('%H:%M:%S.%f')[:-3]
dk=[]; reg=collections.defaultdict(list)
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0; state={}; ent={}
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        if t!='O': continue
        ts=sec*10**9+u('>I',m[1:5])[0]; b=u('>I',m[5:9])[0]; st=m[9:29].decode().strip(); old=state.get(b)
        if st=='P_DK_TEKFIY_EMIR_TPL' and old=='P_SUREKLI_ISLEM': ent[b]={'dk':ts}
        elif b in ent and st=='P_ESLESTIRME' and old=='P_DK_TEKFIY_EMIR_TPL': ent[b]['es']=ts
        elif b in ent and st=='P_SUREKLI_ISLEM' and old=='P_ESLESTIRME' and 'es' in ent[b]:
            e=ent.pop(b); dk.append((part,b,fmt(e['dk']),(e['es']-e['dk'])/1e9,(ts-e['es'])/1e9))
        # regular auctions: offset of start of eslestirme from scheduled second
        if st in('P_ESLESTIRME','P_ESLESTIRMETEKFIYAT') and old in('P_ACILIS_EMIR_TPL','P_TEKFIYAT_EMIR_TPL','P_KAPANIS_EMIR_TPL'):
            reg[old].append(fmt(ts))
        state[b]=st
print("DK: (bolum, defter, giris saati, giris->eslestirme sn, eslestirme->surekli sn)")
for r in dk: print(r)
import collections
for k,v in reg.items():
    c=collections.Counter(x[:8] for x in v)
    print(k,len(v),'en sık başlangıç saniyeleri:',c.most_common(6))
