"""Arma la lista ELO_EXTRA (partidos para el Elo) y, con --write, la inyecta en calculadora-clausura-2026.html.

Fuentes (todas ya validadas contra tablas oficiales):
  - Apertura 2025: datos/ar2025.txt (openfootball/south-america, archivo argentina/2025_ar1.txt)
  - Clausura 2025 y Apertura 2026: matrices de resultados de en.wikipedia.org (datos/mats.py)
  - Libertadores/Sudamericana 2025 y 2026, fase de grupos, equipos argentinos (datos/cups.py)
Uso:  python datos/build.py          -> valida e imprime un resumen
      python datos/build.py --write  -> ademas reescribe ELO_EXTRA dentro del HTML
"""
import re,json,sys,datetime as dt
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
HTML=ROOT/'calculadora-clausura-2026.html'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mats import *
import cups
import knockouts
NAME={"Boca Juniors":"BOC","Central Córdoba (SdE)":"CCO","Defensa y Justicia":"DYJ","Deportivo Riestra":"DRI","Estudiantes (LP)":"EST","Gimnasia y Esgrima (M)":"GEM","Independiente":"IND","Instituto":"INS","Lanús":"LAN","Newell's Old Boys":"NOB","Platense":"PLA","San Lorenzo":"SLO","Talleres (C)":"TAL","Unión":"UNI","Vélez Sarsfield":"VEL","Aldosivi":"ALD","Argentinos Juniors":"ARG","Atlético Tucumán":"ATU","Banfield":"BAN","Barracas Central":"BAR","Belgrano":"BEL","Estudiantes (RC)":"ERC","Gimnasia y Esgrima (LP)":"GLP","Huracán":"HUR","Independiente Rivadavia":"IRI","Racing":"RAC","River Plate":"RIV","Rosario Central":"ROS","Sarmiento (J)":"SAR","Tigre":"TIG","Godoy Cruz":"GOD","San Martín (SJ)":"SMA"}
OF={"Tigre":"TIG","Vélez Sarsfield":"VEL","Godoy Cruz":"GOD","Rosario Central":"ROS","Newell's Old Boys":"NOB","Independiente Rivadavia":"IRI","Defensa y Justicia":"DYJ","Banfield":"BAN","Lanús":"LAN","Deportivo Riestra":"DRI","Barracas Central":"BAR","Racing Club":"RAC","Independiente":"IND","Sarmiento de Junín":"SAR","Belgrano de Córdoba":"BEL","Huracán":"HUR","San Martín de San Juan":"SMA","Atlético Tucumán":"ATU","San Lorenzo":"SLO","Talleres de Córdoba":"TAL","Estudiantes":"EST","Unión de Santa Fe":"UNI","Instituto de Córdoba":"INS","Gimnasia de La Plata":"GLP","Platense":"PLA","River Plate":"RIV","Boca Juniors":"BOC","Argentinos Juniors":"ARG","Central Córdoba SdE":"CCO","Aldosivi":"ALD"}
def score(s):a,b=re.split('[–-]',s.strip());return int(a),int(b)
def matrix(txt):
    L=[l for l in txt.strip().split('\n') if l.startswith('|')]
    hd=[c.strip() for c in L[0].strip().strip('|').split('|')][1:];hd=['GEM' if c=='GME' else c for c in hd]
    out=[]
    for l in L[1:]:
        cells=l.strip()[1:-1].split('|');name=cells[0].strip();assert len(cells)==16,(name,len(cells))
        for c,col in zip(cells[1:],hd):
            c=c.strip()
            if c:gh,ga=score(c);out.append((NAME[name],col,gh,ga))
    return out
def inter(txt):
    out=[]
    for l in txt.strip().split('\n'):
        a,s,b=[c.strip() for c in l.strip()[1:-1].split('|')];gh,ga=score(s);out.append((NAME[a],NAME[b],gh,ga))
    return out
def totals(ms):
    t={}
    for h,a,gh,ga in ms:
        for c,f,g in((h,gh,ga),(a,ga,gh)):
            d=t.setdefault(c,[0,0,0,0]);d[0]+=3 if f>g else 1 if f==g else 0;d[1]+=f;d[2]+=g;d[3]+=1
    return t
def check(name,ms,stand):
    t=totals(ms);bad=[]
    for x in stand.split(';'):
        c,p,gf,ga=x.split();p,gf,ga=int(p),int(gf),int(ga)
        if c not in t or t[c][:3]!=[p,gf,ga] or t[c][3]!=16:bad.append((c,t.get(c),[p,gf,ga]))
    print(name,'partidos:',len(ms),'| equipos:',len(t),'| desajustes:',bad if bad else 'ninguno')
    return not bad
txt=(ROOT/'datos'/'ar2025.txt').read_text(encoding='utf-8').replace('\r','')
ap25=[];md=0;cur=None
for l in txt.split('\n'):
    m=re.match(r'▪ 1° Semestre, Matchday (\d+)',l)
    if m:md=int(m.group(1));continue
    m=re.match(r'\s+(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d+)',l)
    if m:cur=dt.datetime.strptime(f'{m.group(1)} {m.group(2)} 2025','%b %d %Y').date();continue
    m=re.match(r'\s+(?:\d\d:\d\d)?\s*(.+?)\s+v\s+(.+?)\s+(\d+)-(\d+)',l)
    if m and cur:
        h,a=m.group(1).strip(),m.group(2).strip();ap25.append((OF[h],OF[a],int(m.group(3)),int(m.group(4)),md,cur))
ok1=check('Apertura 2025',[(h,a,x,y) for h,a,x,y,_,_ in ap25],ST_AP25)
md25={(h,a):m for h,a,_,_,m,_ in ap25}
cl25=matrix(CL25_A)+matrix(CL25_B)+inter(CL25_I)
ok2=check('Clausura 2025',cl25,ST_CL25)
miss=[(h,a) for h,a,_,_ in cl25 if (a,h) not in md25]
html=HTML.read_text(encoding='utf-8')
Z=json.loads(re.search(r'const ZA=(\[\[.*?\]\]);',html,re.S).group(1))+json.loads(re.search(r'const ZB=(\[\[.*?\]\]);',html,re.S).group(1))
ST_AP26=';'.join(f'{r[0]} {r[2]} {r[3]} {r[4]}' for r in Z)
ap26=matrix(AP26_A)+matrix(AP26_B)+inter(AP26_I)
ok3=check('Apertura 2026',ap26,ST_AP26)
past=re.search(r'const PAST_RAW=\{(.*?)\};',html,re.S).group(1)
fx=re.search(r'const RAW=\{(.*?)\};',html,re.S).group(1)
rd={}
for f,s in re.findall(r'(\d+):"([^"]*)"',past+','+fx):
    for x in s.split(','):
        h,a=x.split(' ')[0].split('-');rd[(h,a)]=int(f)
miss26=[(h,a) for h,a,_,_ in ap26 if (a,h) not in rd]
cr,cbad=cups.rows()
print('Copas (grupos Libertadores/Sudamericana 2025-2026):',len(cr),'partidos | desajustes:',cbad if cbad else 'ninguno')
kr,kbad=knockouts.rows()
print('Knockouts (playoffs liga, Copa Argentina 25/26, eliminatorias CONMEBOL 25/26, Recopas, Mundial, trofeos):',len(kr),'partidos | desajustes:',kbad if kbad else 'ninguno')
if not(ok1 and ok2 and ok3 and not miss and not miss26 and not cbad and not kbad):sys.exit('HAY DESAJUSTES: no se escribe nada')
D=dt.date;rows=[]
for h,a,gh,ga,m,d in ap25:rows.append((d,0,h,a,gh,ga))
for h,a,gh,ga in cl25:rows.append((D(2025,7,11)+dt.timedelta(days=7*(md25[(a,h)]-1)),1,h,a,gh,ga))
for h,a,gh,ga in ap26:
    r=rd[(a,h)];d=D(2026,5,2) if r==9 else D(2026,1,22)+dt.timedelta(days=4*(r-1));rows.append((d,2,h,a,gh,ga))
rows+=cr
rows+=kr
rows.sort(key=lambda x:(x[0],x[1]))
s=','.join(f'{h}-{a} {gh}-{ga}' for d,_,h,a,gh,ga in rows)
print('ELO_EXTRA:',len(rows),'partidos |',len(s),'caracteres | desde',rows[0][0],'hasta',rows[-1][0])
cur_s=re.search(r'const ELO_EXTRA="([^"]*)"\.split',html).group(1)
print('coincide con lo que ya tiene el HTML:',cur_s==s)
if '--write' in sys.argv:
    html=html.replace('const ELO_EXTRA="'+cur_s+'".split','const ELO_EXTRA="'+s+'".split')
    HTML.write_text(html,encoding='utf-8',newline='\n');print('HTML actualizado')
