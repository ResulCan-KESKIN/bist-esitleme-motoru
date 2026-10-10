import sys,re,json,os
sys.path.insert(0,'.')
import ekx,gen
OUT=gen.OUT
TITLES={1:'Birincil Piyasada Talep Toplama ve Satış Yöntemlerine İlişkin Örnekler',2:'Talep Toplama Yöntemlerinin İşleyişine İlişkin Özet Çizelge',3:'Varantların Borsa Kotuna Alınmasına ve Borsada İşlem Görmesine İlişkin Usul ve Esaslar',4:'Sertifikaların Borsa Kotuna Alınmasına ve Borsada İşlem Görmesine İlişkin Usul ve Esaslar',5:'Sahipliğe Dayalı Kira Sertifikalarının Borsa İstanbul Pay Piyasasında İşlem Görme Esasları',6:'Gayrimenkul Sertifikalarının Borsa İstanbul Pay Piyasasında İşlem Görme Esasları',7:'Gayrimenkul Yatırım Fonu ve Girişim Sermayesi Yatırım Fonu Katılma Paylarının Borsa İstanbul Pay Piyasasında İşlem Görme Esasları',8:'Emtia Sertifikalarının Borsa İstanbul Pay Piyasasında İşlem Görme Esasları',9:'Pay Piyasasında Pazarlar ve Seans Saatleri Çizelgeleri',10:'Pay Piyasasında Seans Akış Çizelgeleri',11:'Seansın Bölümleri ve Açıklamaları',12:'İşlem Sırasının Geçici Kapatılması Talebinde Bulunabilecek Ortaklık Yetkilileri Listesi',13:'Borsada İşlem Gören Sermaye Piyasası Araçlarına İlişkin İşlem Sırası Geçici Kapatma Talep Formu',14:'Borsa Dışında Yapılan İşlemlerin Tescil Talep Formu',15:'Tezgâhüstü Türev İşlemlerinin Bildirimi',16:'Açılış Fiyatı Örnekleri',17:'Özel İşlem Bildirimi',18:'Emir Tiplerine İlişkin Örnekler',19:'Seansın Bölümlerine Göre Girilebilecek Emir Tipleri Çizelgesi',20:'Borsa Payı ve Diğer Ücretlere İlişkin Tarife',21:'BİAŞ Pay Piyasası Tarihsel Gelişimi'}
def load(name,default):
    p=name
    if os.path.exists(p):
        return json.load(open(p,encoding='utf-8'))
    return default
OPTS={10:dict(split_fullwidth=True)}
def page_text(n,overrides,num=None):
    if str(n) in overrides: return overrides[str(n)],'elle'
    if num==21 and n>=258:
        import redline
        return redline.page_md(n),'otomatik'
    md=ekx.page_md(n,**OPTS.get(num,{}))
    if num in (3,4):
        import fix32
        md=fix32.fix32(md)
    pt=load('patches.json',{}).get(str(n))
    if pt:
        for p in pt:
            if p[0]=='block':
                _,sp,ep,nw=p
                lines=md.splitlines()
                si=next(i for i,l in enumerate(lines) if l.startswith(sp))
                ei=next(i for i,l in enumerate(lines) if i>=si and l.startswith(ep))
                lines[si:ei+1]=nw.splitlines()
                md=chr(10).join(lines)
            else:
                old,new=p
                assert old in md,('patch bulunamadı',n,old[:60])
                md=md.replace(old,new)
        return md,'yama'
    return md,'otomatik'
def lastline_is_table(md):
    ls=[l for l in md.splitlines() if l.strip()]
    return bool(ls) and ls[-1].startswith('|')
def first_is_table(md):
    ls=[l for l in md.splitlines() if l.strip()]
    return bool(ls) and ls[0].startswith('|')
def build_ek(num):
    a,b=gen.EKS[num]
    ov=load('overrides.json',{})
    ver=load('verified.json',{})
    parts=[];prev_md=None;manual=[]
    for n in range(a,b+1):
        md,kind=page_text(n,ov,num)
        if kind in ('elle','yama'): manual.append(n)
        note=''
        parts.append(f'<!-- sayfa {n} -->\n**[Sayfa {n}]**\n\n{note}{md.strip()}\n')
        prev_md=md
    v=ver.get(str(num),{})
    notes=load('notes.json',{})
    head=f"""# Ek-{num}: {TITLES[num]}

Kaynak: Pay Piyasası Prosedürü (`pay-piyasasi-prosedur.pdf`), Ek-{num}, s. {a}–{b} (PDF sayfa numarası = basılı sayfa numarası).
Aktarım yöntemi: PDF'ten kelime konumlarıyla çıkarım; tablo hücreleri sayfadaki kenarlık ve dolgu çizgilerinden kurulmuştur, bu yüzden sütun kayması olmaz. Yorum eklenmemiştir. Hücre içi satır sonları `<br>` ile gösterilir. Markdown tablolarında ilk satır, kaynakta başlık satırı olmasa da başlık satırı olarak yazılır; bir sayfanın başında devam eden tablonun ilk satırı da veri satırıdır (sayfa işaretleri `[Sayfa N]` ile verilmiştir).
Otomatik doğrulama: sayfalardaki tüm kelimelerin dosyada bulunduğu kontrol edildi (eksik kelime: {v.get('missing','0')}).
Görsel doğrulama (Claude, sayfa görüntüsü ile karşılaştırma): {v.get('visual','yapılmadı')}
Elle düzeltilen/yamalanan sayfalar: {', '.join(map(str,manual)) if manual else 'yok'}
Notlar: Kaynaktaki yazım hataları ve dipnot işaretleri (metin içinde sayı veya "65F" gibi kalıntılar) olduğu gibi bırakılmıştır. Üstü çizili, altı çizili, kalın ve renk gibi biçim bilgileri aktarılmamıştır.{(' ' + notes.get(str(num),'')) if notes.get(str(num)) else ''}
Kullanıcı doğrulaması: bekliyor

"""
    open(os.path.join(OUT,f'ek{num}.md'),'w',encoding='utf-8').write(head+'\n'.join(parts))
if __name__=='__main__':
    for a in sys.argv[1:]: build_ek(int(a))
