import sys,re,collections
sys.path.insert(0,'.')
import ekx
OUT=r"D:\Bitirme\proje\ekler"
EKS={1:(105,110),2:(111,112),3:(113,134),4:(135,142),5:(143,144),6:(145,147),7:(148,150),8:(151,153),9:(154,155),10:(156,175),11:(176,190),12:(191,191),13:(192,192),14:(193,193),15:(194,195),16:(196,200),17:(201,202),18:(203,225),19:(226,229),20:(230,233),21:(234,380)}
def toks(s):
    s=s.replace('|',' ').replace('<br>',' ')
    s=re.sub(r'\s+',' ',s)
    return s.split()
def page_tokens(n):
    out=[]
    for top,x,s,x1,fw in ekx.clean(n):
        out+=toks(s)
    return out
def coverage(n,md):
    a=collections.Counter(page_tokens(n))
    b=collections.Counter(toks(md))
    miss=a-b; extra=b-a
    return miss,extra
def build(num,pages=None,status='Otomatik çıkarım; doğrulama bekliyor',extra_note=''):
    a,b=EKS[num]
    parts=[];report=[]
    for n in range(a,b+1):
        md=ekx.page_md(n)
        miss,extra=coverage(n,md)
        # '|' separators and header cells produce minor diffs; report
        mc=sum(miss.values())
        report.append((n,mc,sum(extra.values())))
        parts.append(f'<!-- sayfa {n} -->\n**[Sayfa {n}]**\n\n{md}\n')
    return parts,report
if __name__=='__main__':
    num=int(sys.argv[1])
    parts,rep=build(num)
    print([r for r in rep if r[1] or r[2]])
    open(f'draft_ek{num}.md','w',encoding='utf-8').write('\n'.join(parts))
