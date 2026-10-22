import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
tot=collections.Counter()
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0
    book=collections.defaultdict(list)
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        ts=sec*10**9+u('>I',m[1:5])[0]
        if t=='A':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); rp=u('>I',m[18:22])[0]; q=u('>Q',m[22:30])[0]; pr=u('>i',m[30:34])[0]
            lst=book[(bid,side)]; idx=min(max(rp-1,0),len(lst))
            # same ts and same price immediately before?
            if idx>0 and lst[idx-1][1]==pr and lst[idx-1][2]==ts:
                tot['ayni fiyat+ayni ns: onceki emir (mesaj sirasiyla) onde']+=1
                tot['  ...onceki emir Order ID daha kucuk' if lst[idx-1][0]<oid else '  ...onceki emir Order ID daha buyuk']+=1
            if idx<len(lst) and lst[idx][1]==pr and lst[idx][2]==ts:
                tot['ayni fiyat+ayni ns: sonraki emir arkada (SIRA TERS)']+=1
            lst.insert(idx,[oid,pr,ts,q]); tot['A toplam']+=1
        elif t=='E':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); q=u('>Q',m[18:26])[0]
            lst=book[(bid,side)]; i=next((j for j,x in enumerate(lst) if x[0]==oid),None)
            if i is not None:
                lst[i][3]-=q
                if lst[i][3]<=0: lst.pop(i)
        elif t=='D':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17])
            lst=book[(bid,side)]; i=next((j for j,x in enumerate(lst) if x[0]==oid),None)
            if i is not None: lst.pop(i)
for k,v in sorted(tot.items()): print(k,v)
