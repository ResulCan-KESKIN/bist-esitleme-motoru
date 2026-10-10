import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack; MIN=-2147483648
tot=collections.Counter(); ex=collections.defaultdict(list)
Acount=collections.Counter()
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0; state={}; lastZ={}; zn=collections.Counter(); 
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        if t=='Z':
            b=u('>I',m[5:9])[0]
            zz=(u('>Q',m[9:17])[0],u('>Q',m[17:25])[0],u('>i',m[25:29])[0],u('>i',m[29:33])[0],u('>i',m[33:37])[0],u('>Q',m[37:45])[0],u('>Q',m[45:53])[0])
            if zz[2]!=MIN: lastZ[b]=zz
            zn[b]+=1
        elif t=='O':
            b=u('>I',m[5:9])[0]; st=m[9:29].decode().strip()
            if st in('P_ESLESTIRME','P_ESLESTIRMETEKFIYAT'):
                z=lastZ.get(b); old=state.get(b)
                key=(old,)
                if z is None or z[2]==MIN: tot[(old,'Z yok/fiyat yok')]+=1
                else:
                    av,aa,eq,bb,ba,bbq,baq=z
                    sur='alis fazlasi' if av>aa else ('satis fazlasi' if aa>av else 'esit')
                    if eq==ba and eq==bb: pos_='eq=ba=bb'
                    elif eq==ba: pos_='eq=en iyi satis'
                    elif eq==bb: pos_='eq=en iyi alis'
                    elif ba<eq<bb: pos_='arada (ba<eq<bb)'
                    else: pos_='diger (bb<eq veya eq<ba veya MKT)'
                    tot[(old,sur,pos_)]+=1
                    if len(ex[(sur,pos_)])<3: ex[(sur,pos_)].append((part,b,old,sec,z))
            lastZ.pop(b,None) if st not in('P_ESLESTIRME','P_ESLESTIRMETEKFIYAT') else None
            state[b]=st
        elif t=='A':
            b=u('>I',m[13:17])[0]; Acount[state.get(b)]+=1
for k,v in sorted(tot.items(),key=lambda x:-x[1]): print(v,k)
print(Acount)
for k,v in ex.items(): print(k,v)
