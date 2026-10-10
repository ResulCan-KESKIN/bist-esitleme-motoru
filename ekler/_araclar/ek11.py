import sys,re
sys.path.insert(0,'.')
import ekx
def build():
    out=[];cur=None;curpage=None
    states=[]  # (name, page_started, [ (page,line) ])
    for n in range(176,191):
        for tb in ekx.tables(n):
            for ya,yb,cells in tb['rows']:
                # cells: per column; collapse: col0 text, col1 text
                texts=[c[2] for c in cells]
                if len(texts)<2: continue
                a,b=texts[0].strip(),texts[-1].strip()
                if a.startswith('SEANSIN BÖLÜMÜ') and b.startswith('AÇIKLAMALAR'): continue
                if a:
                    states.append([a,n,[]])
                if b:
                    if not states: states.append(['(ad belirtilmemiş)',n,[]])
                    states[-1][2].append((n,b))
    return states
if __name__=='__main__':
    st=build()
    print(len(st))
    for name,pg,lines in st[:8]:
        print('###',name,'p',pg)
        for p,l in lines: print('  ',p,l[:100])
