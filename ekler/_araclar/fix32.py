import re
def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]
def fix32(md):
    lines=md.split('\n')
    out=[];i=0
    while i<len(lines):
        l=lines[i]
        if l.startswith('|') and len(_cells(l))==32 and i+3<len(lines):
            # collect block of consecutive table lines
            j=i
            blk=[]
            while j<len(lines) and lines[j].startswith('|'):
                blk.append(lines[j]); j+=1
            rows=[_cells(b) for b in blk if not re.match(r'^\|(---\|)+$',b)]
            idx=[k for k,r in enumerate(rows) if [re.sub(r'<br>','',c) for c in r]==[str(n) for n in range(1,33)]]
            if idx and idx[0]>=1 and len(rows)>idx[0]+1:
                k=idx[0]
                hdr=rows[0]
                data=[c.replace('<br>','') for c in rows[k+1]]
                starts=[(p,c.replace('<br>',' ')) for p,c in enumerate(hdr) if c.strip()]
                groups=[]
                for gi,(p,c) in enumerate(starts):
                    end=(starts[gi+1][0] if gi+1<len(starts) else 32)
                    label=c
                    if label.upper().startswith('CAL'): label='CALL / PUT'
                    groups.append((label,p+1,end))
                out.append('| '+' | '.join(['Alan grubu']+[g[0] for g in groups])+' |')
                out.append('|'+'---|'*(len(groups)+1))
                out.append('| '+' | '.join(['Başlık hücresinin kapsadığı sütunlar']+[(str(a) if a==b else f'{a}–{b}') for _,a,b in groups])+' |')
                out.append('')
                out.append('| Konum | '+' | '.join(str(n) for n in range(1,33))+' |')
                out.append('|'+'---|'*33)
                out.append('| Örnek karakter | '+' | '.join(data)+' |')
                i=j
                continue
        out.append(l); i+=1
    return '\n'.join(out)
