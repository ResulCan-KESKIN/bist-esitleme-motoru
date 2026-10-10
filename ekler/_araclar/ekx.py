import pdfplumber, re, pypdfium2 as pdfium
P=r"E:\DERSLER\7. DÖNEM\Bitirme Projesi 1\proje\pay-piyasasi-prosedur.pdf"
_pdf=pdfplumber.open(P)
_doc=pdfium.PdfDocument(P)
HDR=re.compile(r'^(Pay Piyasası Direktörlüğü|Prosedür|TANIMLAR ve KISALTMALAR LİSTESİ)')
FTR=re.compile(r'^(Sayfa\s*\d+\s*/\s*380|\(\s*\d+\s*\))$')
def words(n):
    pg=_pdf.pages[n-1]
    return pg.extract_words(x_tolerance=1.5,y_tolerance=2,keep_blank_chars=False,extra_attrs=['size'])
def rows(n,tol=3.0,gap=14.0,sep=' | '):
    ws=words(n)
    ws.sort(key=lambda w:(round(w['top']),w['x0']))
    out=[];cur=[]
    for w in sorted(ws,key=lambda w:(w['top'],w['x0'])):
        if cur and abs(w['top']-cur[0]['top'])>tol:
            out.append(cur);cur=[]
        cur.append(w)
    if cur: out.append(cur)
    res=[]
    for r in out:
        r.sort(key=lambda w:w['x0'])
        s=r[0]['text'];prev=r[0]
        for w in r[1:]:
            g=w['x0']-prev['x1']
            s+= (sep if g>gap else ' ')+w['text']
            prev=w
        res.append((round(r[0]['top']),round(r[0]['x0']),s,round(max(w['x1'] for w in r)),round(r[0]['x1']-r[0]['x0'])))
    return res
def clean(n,**kw):
    out=[]
    for top,x,s,x1,fw in rows(n,**kw):
        t=s.replace(' | ',' ').strip()
        if HDR.match(t) and top<80: continue
        if FTR.match(t): continue
        out.append((top,x,s,x1,fw))
    return out
def render(n,scale=1.2):
    import os
    f=f'img/p{n}.png'
    _doc[n-1].render(scale=scale).to_pil().save(f)
    return f

# ---- grid table detection from thin filled rects ----
def _black(c):
    return c in (0.0,(0,0,0),[0.0],(0.0,),None,0,(0,),[0],[0,0,0],(0.0,0.0,0.0))
def _white(c):
    return c in (1.0,(1,1,1),[1.0],(1.0,),1,(1,),[1],[1,1,1],(1.0,1.0,1.0))
def edges(n,thick=3.2,minlen=6):
    pg=_pdf.pages[n-1]
    H=[];V=[]
    fills=[]
    for r in pg.rects:
        w=r['x1']-r['x0'];h=r['bottom']-r['top']
        c=r.get('non_stroking_color')
        if h<=thick and w>=minlen and not _white(c):
            H.append(((r['top']+r['bottom'])/2,r['x0'],r['x1']))
        elif w<=thick and h>=minlen and not _white(c):
            V.append(((r['x0']+r['x1'])/2,r['top'],r['bottom']))
        elif w>15 and h>thick and not _white(c) and not _black(c):
            fills.append((r['x0'],r['x1'],r['top'],r['bottom']))
    # outermost filled rects only
    outer=[f for f in fills if not any(g is not f and g[0]<=f[0]+0.5 and g[1]>=f[1]-0.5 and g[2]<=f[2]+0.5 and g[3]>=f[3]-0.5 and (g[1]-g[0])*(g[3]-g[2])>(f[1]-f[0])*(f[3]-f[2])+1 for g in fills)]
    for x0,x1,t,b in outer:
        H.append((t,x0,x1));H.append((b,x0,x1));V.append((x0,t,b));V.append((x1,t,b))
    for l in pg.lines:
        if abs(l['top']-l['bottom'])<1: H.append((l['top'],l['x0'],l['x1']))
        elif abs(l['x0']-l['x1'])<1: V.append((l['x0'],l['top'],l['bottom']))
    H=[h for h in H if 52<h[0]<785]
    V=[v for v in V if v[2]>52 and v[1]<785]
    return H,V
def cluster(vals,tol=2.0):
    vals=sorted(vals);out=[]
    for v in vals:
        if out and v-out[-1][-1]<=tol: out[-1].append(v)
        else: out.append([v])
    return [sum(c)/len(c) for c in out]
def _xs_for(b,H,V):
    y0,y1=b[0]-2,b[-1]+2
    Hs=[h for h in H if y0<=h[0]<=y1]
    Vs=[v for v in V if v[1]<=y1+2 and v[2]>=y0-2]
    xs=cluster([v[0] for v in Vs],tol=2.5)
    x_min=min(h[1] for h in Hs);x_max=max(h[2] for h in Hs)
    if xs[0]-x_min>6: xs=[x_min]+xs
    if x_max-xs[-1]>6: xs=xs+[x_max]
    return xs,Vs
def _join_lines(cw,xb,tol=3.0,wrap_margin=None):
    cw=sorted(cw,key=lambda w:(w['top'],w['x0']))
    lines=[]
    for w in cw:
        if lines and abs(w['top']-lines[-1][0]['top'])<=tol: lines[-1].append(w)
        else: lines.append([w])
    out='';prev_x1=None
    for ln in lines:
        ln.sort(key=lambda w:w['x0'])
        t=' '.join(w['text'] for w in ln)
        if prev_x1 is None: out=t
        else: out+=(' ' if (wrap_margin is not None and prev_x1>=xb-wrap_margin) else '<br>')+t
        prev_x1=max(w['x1'] for w in ln)
    return out
def tables(n,mergegap=45,merge_blank=True):
    H,V=edges(n)
    if not H or not V: return []
    ys=cluster([h[0] for h in H])
    ws=words(n)
    def covered(ya,yb):
        mid=(ya+yb)/2
        return any(v[1]-1<=mid<=v[2]+1 and v[1]-2<=ya+(yb-ya)*0.4 and v[2]+2>=yb-(yb-ya)*0.4 for v in V)
    blocks=[];cur=[ys[0]]
    for ya,yb in zip(ys,ys[1:]):
        if yb-ya>=3 and covered(ya,yb): cur.append(yb)
        elif yb-ya<3: cur[-1]=yb
        else:
            if len(cur)>=2: blocks.append(cur)
            cur=[yb]
    if len(cur)>=2: blocks.append(cur)
    info=[(b,)+_xs_for(b,H,V) for b in blocks]
    # merge neighbouring blocks with same columns when the gap holds table-like text (unshaded rows)
    if merge_blank:
        merged=[info[0]+(set(),)] if info else []
        for b,xs,Vs in info[1:]:
            pb,pxs,pVs=merged[-1][:3]
            gap=b[0]-pb[-1]
            same=len(xs)==len(pxs) and all(abs(p-q)<3 for p,q in zip(xs,pxs))
            def _mh(bb):
                hs=sorted(bb[i+1]-bb[i] for i in range(len(bb)-1) if bb[i+1]-bb[i]>6)
                return hs[len(hs)//2] if hs else 14
            lim=1.35*max(_mh(pb),_mh(b))
            if same and 3<gap<=min(mergegap,lim):
                gw=[w for w in ws if pb[-1]<(w['top']+w['bottom'])/2<b[0]]
                gw.sort(key=lambda w:w['x0'])
                _ng=0;_pv=None
                for w in gw:
                    if _pv is None or w['x0']-_pv>8: _ng+=1
                    _pv=w['x1']
                if len(gw)>=2 and _ng>=max(2,(len(xs)-1)//2):
                    pbl=merged[-1][3] if len(merged[-1])>3 else set()
                    nbl=set(pbl)|{len(pb)-1}
                    merged[-1]=(pb+b,pxs,pVs+Vs,nbl)
                    continue
            merged.append((b,xs,Vs,set()))
        info=merged
    res=[]
    for b,xs,Vs,blank_bands in [(i[0],i[1],i[2],i[3]) if len(i)>3 else (i[0],i[1],i[2],set()) for i in info]:
        Hs=[h for h in H if b[0]-2<=h[0]<=b[-1]+2]
        nb=len(b)-1; nc=len(xs)-1
        # union-find over cells
        par={}
        def f(c):
            while par.setdefault(c,c)!=c:
                par[c]=par[par[c]]; c=par[c]
            return c
        def u(c1,c2): par[f(c1)]=f(c2)
        for i in range(nb):
            ya,yb=b[i],b[i+1]
            if yb-ya<3: continue
            mid=(ya+yb)/2
            # band without any interior vertical edge: data row if its words form >=3 groups
            interior=[any(abs(v[0]-xs[j2])<=3.0 and v[1]-1<=mid<=v[2]+1 for v in Vs) for j2 in range(1,nc)]
            nogrid=False
            if not any(interior):
                bw=sorted([w for w in ws if ya<=(w['top']+w['bottom'])/2<=yb and xs[0]-2<=w['x0'] and w['x1']<=xs[-1]+2],key=lambda w:w['x0'])
                ng=0;pv=None
                for w in bw:
                    if pv is None or w['x0']-pv>8: ng+=1
                    pv=w['x1']
                nogrid = ng>=2
            for j in range(nc):
                f((i,j))
                if i in blank_bands or nogrid: continue
                if j+1<nc:
                    x=xs[j+1]
                    has=any(abs(v[0]-x)<=3.0 and v[1]-1<=mid<=v[2]+1 for v in Vs)
                    if not has: u((i,j),(i,j+1))
                if i+1<nb and (i+1) not in blank_bands and i not in blank_bands:
                    xm=(xs[j]+xs[j+1])/2
                    has=any(abs(h[0]-yb)<=3.0 and h[1]-1<=xm<=h[2]+1 for h in Hs)
                    if not has: u((i,j),(i+1,j))
        comps={}
        for i in range(nb):
            if b[i+1]-b[i]<3: continue
            for j in range(nc): comps.setdefault(f((i,j)),[]).append((i,j))
        texts={};boxes=[];assigned=set()
        for root,cells_ in comps.items():
            ya=min(b[i] for i,j in cells_); yb=max(b[i+1] for i,j in cells_)
            xa=min(xs[j] for i,j in cells_); xb=max(xs[j+1] for i,j in cells_)
            cw=[w for w in ws if ya<=(w['top']+w['bottom'])/2<=yb and xa<=(w['x0']+w['x1'])/2<=xb]
            for w in cw: assigned.add(id(w))
            tl=min(cells_)
            texts[tl]=cw; boxes.append((tl,ya,yb,xa,xb))
        # fallback: words inside table bbox not assigned to any cell -> nearest cell
        for w in ws:
            if id(w) in assigned: continue
            cx=(w['x0']+w['x1'])/2; cy=(w['top']+w['bottom'])/2
            if not (xs[0]-1<=cx<=xs[-1]+1 and b[0]-2<=cy<=b[-1]+2): continue
            best=min(boxes,key=lambda bx:(max(bx[1]-cy,0,cy-bx[2])*3+max(bx[3]-cx,0,cx-bx[4])))
            texts[best[0]].append(w); assigned.add(id(w))
        boxmap={bx[0]:bx for bx in boxes}
        for k in texts:
            xb_=boxmap[k][4]
            texts[k]=_join_lines(texts[k],xb_)
        rows=[]
        for i in range(nb):
            ya,yb=b[i],b[i+1]
            if yb-ya<3: continue
            cells=[(xs[j],xs[j+1],texts.get((i,j),'')) for j in range(nc)]
            rows.append((ya,yb,cells))
        res.append(dict(y0=b[0]-2,y1=b[-1]+2,xs=xs,rows=rows))
    # extend by unshaded first/last rows
    for tb in res:
        hs=[yb-ya for ya,yb,_ in tb['rows'] if yb-ya>6]
        if not hs: continue
        H_=sorted(hs)[len(hs)//2]
        xs=tb['xs']
        for direction in ('down','up'):
            for _ in range(2):
                if direction=='down': ya,yb=tb['rows'][-1][1],tb['rows'][-1][1]+H_+2
                else: ya,yb=tb['rows'][0][0]-H_-2,tb['rows'][0][0]
                gw=[w for w in ws if ya<(w['top']+w['bottom'])/2<yb and xs[0]-3<=w['x0'] and w['x1']<=xs[-1]+3]
                # group count
                gw.sort(key=lambda w:w['x0'])
                ng=0;prev=None
                for w in gw:
                    if prev is None or w['x0']-prev>14: ng+=1
                    prev=w['x1']
                other=[w for w in ws if ya<(w['top']+w['bottom'])/2<yb and not(xs[0]-3<=w['x0'] and w['x1']<=xs[-1]+3)]
                if ng>=3 and not other:
                    cells=[]
                    for j in range(len(xs)-1):
                        cw=[w for w in gw if xs[j]<=(w['x0']+w['x1'])/2<=xs[j+1]]
                        cells.append((xs[j],xs[j+1],' '.join(w['text'] for w in cw)))
                    row=(ya,yb,cells)
                    if direction=='down': tb['rows'].append(row); tb['y1']=yb
                    else: tb['rows'].insert(0,row); tb['y0']=ya
                else: break
    return res
def table_md(tb,drop_empty_rows=True):
    xs=tb['xs'];lines=[]
    ncol=len(xs)-1
    for ya,yb,cells in tb['rows']:
        out=['']*ncol
        for (xa,xb,t) in cells:
            i=min(range(ncol),key=lambda k:abs(xs[k]-xa))
            if out[i]: out[i]+=' '+t
            else: out[i]=t.replace('|','\|')
        if drop_empty_rows and not any(out): continue
        lines.append(out)
    if lines:
        keep=[j for j in range(ncol) if any(l[j] for l in lines)]
        lines=[[l[j] for j in keep] for l in lines]
    return lines
def _split_fullwidth(tbs):
    out=[]
    for tb in tbs:
        def full(r):
            c=r[2]
            return bool(c) and c[0][2].strip()!='' and all(not x[2].strip() for x in c[1:])
        groups=[];g=[]
        for r in tb['rows']:
            if full(r) and g and not full(g[-1]):
                groups.append(g);g=[]
            g.append(r)
        if g: groups.append(g)
        for g in groups:
            out.append(dict(y0=g[0][0]-2,y1=g[-1][1]+2,xs=tb['xs'],rows=g))
    return out
# ---- page assembly ----
BUL=re.compile(r'^(\(?[a-zçğıöşüA-Z0-9]{1,3}\)|•|[–\-]\s|\d+[\.\)]\s|\d+\.\d+|[•●■·]\s|[ivxIVX]+\))')
LBL=re.compile(r'^[A-ZÇĞİÖŞÜ][^:]{2,45} : ')
def prose_rows(n,tbs,gap=30.0):
    out=[]
    for top,x,s,x1,fw in clean(n,gap=gap):
        inside=any(tb['y0']-1<=top<=tb['y1']+1 and tb['xs'][0]-4<=x and x1<=tb['xs'][-1]+4 for tb in tbs)
        if not inside: out.append((top,x,s,x1,fw))
    return out
def page_md(n,para_gap=1.6,split_fullwidth=False):
    tbs=tables(n)
    if split_fullwidth: tbs=_split_fullwidth(tbs)
    pr=prose_rows(n,tbs)
    items=[(tb['y0'],'T',tb) for tb in tbs]+[(t,'P',(x,s,x1,fw)) for t,x,s,x1,fw in pr]
    items.sort(key=lambda a:(a[0],0 if a[1]=='T' else 1))
    gaps=[b[0]-a[0] for a,b in zip(pr,pr[1:]) if 8<b[0]-a[0]<30]
    med=sorted(gaps)[len(gaps)//2] if gaps else 13
    maxx1=max([r[3] for r in pr],default=540)
    md=[];para=[];prev=None
    def flush():
        nonlocal para
        if para:
            md.append(' '.join(para)); para=[]
    for top,k,v in items:
        if k=='T':
            flush()
            lines=table_md(v)
            if not lines: continue
            nc=max(len(l) for l in lines)
            if md and ' | ' in md[-1] and len(md[-1].split(' | '))==nc and prev is not None and v['y0']-prev[0]<40:
                hdr=md.pop().split(' | '); lines=[hdr]+lines
            md.append('')
            md.append('| '+' | '.join(lines[0])+' |')
            md.append('|'+'---|'*nc)
            for l in lines[1:]: md.append('| '+' | '.join(l)+' |')
            md.append('')
            prev=(v['y1'],0,999)
        else:
            x,s,x1,fw=v
            wrapped = prev is not None and (maxx1-prev[2]) <= fw+10
            newp = (prev is None or (top-prev[0])>med*para_gap or BUL.match(s) is not None or LBL.match(s) is not None or not wrapped)
            if s.count(' | ')>=2: newp=True
            elif ' | ' in s: s=s.replace(' | ',' ')
            if newp: flush()
            para.append(s)
            if s.count(' | ')>=2: flush()
            prev=(top,x,x1)
    flush()
    return '\n'.join(md)
