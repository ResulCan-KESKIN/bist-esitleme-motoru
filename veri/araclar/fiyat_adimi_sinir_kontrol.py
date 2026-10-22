import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
tot=collections.Counter()
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; tabs=collections.defaultdict(list)
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='L':
            b=u('>I',m[5:9])[0]; tabs[b].append((u('>Q',m[9:17])[0],u('>i',m[17:21])[0],u('>i',m[21:25])[0]))
        elif t=='A':
            b=u('>I',m[13:17])[0]; p=u('>i',m[30:34])[0]
            tb=tabs.get(b)
            if not tb or p<=0: continue
            band=None
            for tk,f,to in tb:
                if f<=p and (p<=to or to==0): band=(tk,f,to); break
            if band is None: tot['band yok']+=1; continue
            tot[('fiyat adimina uygun' if p%band[0]==0 else 'UYGUN DEGIL')]+=1
            if band[1]==20000 and band[0]==20:
                if p==20000: tot['tam 20,000 fiyatli emir (0,02 bandi)']+=1
                if p%20!=0: tot['0,02 bandinda 0,01 katı emir']+=1
            if p in (19990,19999,20010,20020,20000): tot[('fiyat',p)]+=1
for k,v in sorted(tot.items(),key=lambda x:str(x[0])): print(k,v)
