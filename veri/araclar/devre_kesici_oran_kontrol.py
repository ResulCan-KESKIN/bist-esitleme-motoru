import struct, sys, io, collections, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
rows=[]; allmax=[]
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0; state={}
    ref={}; lasttr={}; maxdev=collections.defaultdict(float); px={}
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        if t=='P':
            b=u('>I',m[26:30])[0]; p=u('>i',m[30:34])[0]; st=state.get(b)
            if st in('P_ESLESTIRME','P_ESLESTIRMETEKFIYAT') or (st=='P_DK_TEKFIY_EMIR_TPL'): pass
            if st in('P_ESLESTIRME','P_ESLESTIRMETEKFIYAT'): ref[b]=p
        elif t=='A':
            px[(u('>I',m[13:17])[0],u('>Q',m[5:13])[0])]=u('>i',m[30:34])[0]
        elif t=='E':
            b=u('>I',m[13:17])[0]; o=u('>Q',m[5:13])[0]; p=px.get((b,o))
            if p is not None and state.get(b)=='P_SUREKLI_ISLEM':
                lasttr[b]=p
                if b in ref and ref[b]>0: maxdev[b]=max(maxdev[b],abs(p-ref[b])/ref[b])
        elif t=='O':
            b=u('>I',m[5:9])[0]; st=m[9:29].decode().strip(); old=state.get(b)
            if st=='P_DK_TEKFIY_EMIR_TPL' and old=='P_SUREKLI_ISLEM':
                r=ref.get(b); l=lasttr.get(b)
                tt=datetime.datetime.utcfromtimestamp(sec)+datetime.timedelta(hours=3)
                rows.append((part,b,tt.strftime('%H:%M:%S'),r,l,(abs(l-r)/r if r and l else None)))
            state[b]=st
    allmax+= [(part,b,v) for b,v in maxdev.items()]
for r in rows: print(r)
import statistics
vals=[v for _,_,v in allmax]
print('books with continuous trades & ref:',len(vals))
for th in (0.04,0.05,0.06,0.07,0.075,0.09,0.10,0.11):
    print('max sapma >=',th, sum(1 for v in vals if v>=th))
