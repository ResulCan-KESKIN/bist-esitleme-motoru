import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
tot=collections.Counter(); ex=[]
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0; state={}
    live={}      # (bid,side,oid) -> [price, qty, ts]
    last={}      # key -> (how removed, price, qty_added_total, time)
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        ts=sec*10**9+u('>I',m[1:5])[0]
        if t=='O': state[u('>I',m[5:9])[0]]=m[9:29].decode().strip()
        elif t=='A':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); q=u('>Q',m[22:30])[0]; pr=u('>i',m[30:34])[0]
            k=(bid,side,oid)
            if k in last:
                how,ppr,pts,pq=last[k]
                samepx = (pr==ppr)
                gap = ts-pts
                tot[(how,'ayni fiyat' if samepx else 'farkli fiyat','ayni ns' if gap==0 else ('<1s' if gap<10**9 else '>=1s'))]+=1
                if how=='E-tukendi' and samepx and len(ex)<3: ex.append((part,k,state.get(bid),ppr,pq,q,gap))
            live[k]=[pr,q,ts]
        elif t=='E':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); q=u('>Q',m[18:26])[0]
            k=(bid,side,oid)
            if k in live:
                live[k][1]-=q
                if live[k][1]<=0:
                    last[k]=('E-tukendi',live[k][0],ts,q); live.pop(k)
        elif t=='D':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); k=(bid,side,oid)
            if k in live:
                last[k]=('D',live[k][0],ts,live[k][1]); live.pop(k)
for k,v in sorted(tot.items(),key=lambda x:-x[1]): print(v,k)
print(ex)
