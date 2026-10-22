import struct, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r"D:\Bitirme\proje\veri\itch\2018-10-08\vrd\rewinder-files"
u = struct.unpack
tot=collections.Counter(); ex=collections.defaultdict(list)
for part in ("TM-1","TM-2"):
    data=open(D+"\\"+part+".VRD",'rb').read(); pos=0; sec=0; state={}
    book=collections.defaultdict(list)   # (bid,side)-> [[oid,price,ts,qty]]
    dele={}   # key -> (ts, price, qty_rem, behind, state)
    while pos<len(data):
        L=u('>H',data[pos:pos+2])[0]; m=data[pos+2:pos+2+L]; pos+=2+L; t=chr(m[0])
        if t=='T': sec=u('>I',m[1:5])[0]; continue
        ts=sec*10**9+u('>I',m[1:5])[0]
        if t=='O': state[u('>I',m[5:9])[0]]=m[9:29].decode().strip()
        elif t=='A':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); rp=u('>I',m[18:22])[0]
            q=u('>Q',m[22:30])[0]; pr=u('>i',m[30:34])[0]
            lst=book[(bid,side)]; idx=min(max(rp-1,0),len(lst))
            lst.insert(idx,[oid,pr,ts,q])
            k=(bid,side,oid)
            if k in dele and dele[k][0]==ts and state.get(bid)=='P_SUREKLI_ISLEM':
                _,ppr,pq,pbehind,st=dele.pop(k)
                behind=sum(1 for x in lst[idx+1:] if x[1]==pr)
                same_px = (pr==ppr)
                rel='miktar azaldi' if q<pq else ('miktar artti' if q>pq else 'miktar ayni')
                if not same_px: rel2='fiyat degisti'
                else: rel2='ayni fiyat'
                pos_= 'seviye sonunda' if behind==0 else 'seviyede arkada emir var'
                kept = (behind==pbehind) 
                tot[(rel2, rel if same_px else '-', pos_, 'onceki konumla ayni' if kept else 'onceki konumdan farkli')]+=1
                key=(rel2,rel if same_px else '-')
                if len(ex[key])<2: ex[key].append((part,bid,side,oid,ppr,pr,pq,q,pbehind,behind))
        elif t=='E':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17]); q=u('>Q',m[18:26])[0]
            lst=book[(bid,side)]; i=next((j for j,x in enumerate(lst) if x[0]==oid),None)
            if i is not None:
                lst[i][3]-=q
                if lst[i][3]<=0: lst.pop(i)
        elif t=='D':
            oid=u('>Q',m[5:13])[0]; bid=u('>I',m[13:17])[0]; side=chr(m[17])
            lst=book[(bid,side)]; i=next((j for j,x in enumerate(lst) if x[0]==oid),None)
            if i is not None:
                x=lst.pop(i)
                behind=sum(1 for y in lst[i:] if y[1]==x[1])
                dele[(bid,side,oid)]=(ts,x[1],x[3],behind,state.get(bid))
for k,v in sorted(tot.items(),key=lambda x:-x[1]): print(v,k)
for k,v in ex.items(): print(k,v)
