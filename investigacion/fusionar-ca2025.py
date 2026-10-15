"""Fusiona la Copa Argentina 2025 completa en un solo JSON.

Lee los parciales del subagent (32avos: -a; cuartos/semis/final: -b) y agrega
16avos y octavos tomados de los anexos de Wikipedia ES, verificados contra
La Nación (02/07/2025), TyC, TheSportsDB y Playmakerstats (cruce hecho a mano).
Los parciales se mueven a _src/ para que el validador no los duplique.
"""
import json, shutil
from pathlib import Path

INV = Path(__file__).resolve().parent
SRC = INV / '_src'
SRC.mkdir(exist_ok=True)

ANX16 = "https://es.wikipedia.org/wiki/Anexo:Dieciseisavos_de_final_de_la_Copa_Argentina_2025"
ANX8 = "https://es.wikipedia.org/wiki/Anexo:Octavos_de_final_de_la_Copa_Argentina_2025"
W = "https://es.wikipedia.org/wiki/Copa_Argentina_2025"
TSDB = "https://www.thesportsdb.com/season/4500-copa-argentina/2025"
LN = "https://www.lanacion.com.ar/deportes/futbol/asi-quedo-el-cuadro-de-la-copa-argentina-2025-tras-el-triunfo-de-racing-nid02072025/"
PM = "https://www.playmakerstats.com/competition/copa-argentina"

# 16avos (11/5 - 2/8/2025) — anexo Wikipedia ES + cruces verificados
d16 = [
 # fecha, local, visitante, gl, gv, penL, penV, nombreL, nombreV, fuentes extra, dudas
 ("2025-05-11","LOW","GLP",1,1,5,4,"Central Córdoba de Rosario","Gimnasia y Esgrima (LP)",[ANX16,PM],"Cancha neutral San Nicolás; Primera C vs Primera. Penales 5-4."),
 ("2025-05-21","LAN","VEL",2,0,None,None,"Lanús","Vélez Sarsfield",[ANX16,TSDB],""),
 ("2025-05-22","DYJ","NOB",0,2,None,None,"Defensa y Justicia","Newell's Old Boys",[ANX16,TSDB],""),
 ("2025-05-24","DRI","LOW",2,2,4,3,"Deportivo Riestra","Deportivo Armenio",[ANX16,LN],""),
 ("2025-05-28","LOW","ARG",0,3,None,None,"Excursionistas","Argentinos Juniors",[ANX16],""),
 ("2025-06-01","EST","ALD",1,1,2,4,"Estudiantes (LP)","Aldosivi",[ANX16,PM],""),
 ("2025-06-26","TIG","BAN",2,0,None,None,"Tigre","Banfield",[ANX16,TSDB],""),
 ("2025-06-27","BEL","LOW",3,2,None,None,"Belgrano","Defensores de Belgrano",[ANX16,LN],""),
 ("2025-06-28","ROS","UNI",0,0,1,3,"Rosario Central","Unión",[ANX16,PM],""),
 ("2025-06-29","GEM","IND",1,2,None,None,"Gimnasia y Esgrima (M)","Independiente",[ANX16,"https://www.copaargentina.org/es/pwa/match/3629_Gimnasia-de-Mendoza-vs-Independiente.html"],""),
 ("2025-07-02","RAC","SMA",3,1,None,None,"Racing Club","San Martín (SJ)",[ANX16,LN],"Ambos de Primera en 2025 (SMA descendió a fin de año)."),
 ("2025-07-02","PLA","IRI",2,2,1,3,"Platense","Independiente Rivadavia",[ANX16,LN],""),
 ("2025-07-03","INS","HUR",0,0,2,3,"Instituto","Huracán",[ANX16,LN],""),
 ("2025-07-05","SLO","LOW",0,0,4,3,"San Lorenzo","Quilmes",[ANX16,LN],""),
 ("2025-07-23","BOC","ATU",1,2,None,None,"Boca Juniors","Atlético Tucumán",[ANX16,TSDB],""),
 ("2025-08-02","LOW","RIV",0,3,None,None,"San Martín (T)","River Plate",[ANX16,TSDB],"SMT de Primera Nacional = LOW."),
]
# Octavos (30/7 - 28/8/2025)
d8 = [
 ("2025-07-30","IRI","LOW",2,1,None,None,"Independiente Rivadavia","Central Córdoba de Rosario",[ANX8,LN],""),
 ("2025-07-31","ALD","ARG",1,2,None,None,"Aldosivi","Argentinos Juniors",[ANX8,PM],""),
 ("2025-08-01","BEL","IND",2,0,None,None,"Belgrano","Independiente",[ANX8,"https://tn.com.ar/deportes/futbol/2025/08/01/belgrano-vs-independiente-en-vivo-por-los-octavos-de-final-de-la-copa-argentina-hora-donde-ver-y-formaciones/"],""),
 ("2025-08-01","LAN","HUR",2,0,None,None,"Lanús","Huracán",[ANX8,W],""),
 ("2025-08-02","SLO","TIG",0,1,None,None,"San Lorenzo","Tigre",[ANX8,W],""),
 ("2025-08-03","RAC","DRI",3,0,None,None,"Racing Club","Deportivo Riestra",[ANX8,"https://www.newsdigitales.com/nota/308469/racing-goleo-a-riestra-y-se-metio-en-cuartos-de-final-de-la-copa-argentina/"],""),
 ("2025-08-13","ATU","NOB",2,3,None,None,"Atlético Tucumán","Newell's Old Boys",[ANX8,TSDB],""),
 ("2025-08-28","UNI","RIV",0,0,3,4,"Unión","River Plate",[ANX8,W],""),
]

def mk(fila, ronda):
    f,l,v,gl,gv,pl,pv,nl,nv,extra,dudas = fila
    return {"fecha":f,"torneo":"Copa Argentina 2025","ronda":ronda,"local":l,"visitante":v,
            "gl":gl,"gv":gv,"penL":pl,"penV":pv,"nombreL":nl,"nombreV":nv,
            "fuentes":extra,"dudas":dudas}

partidos = []
for fn in ("copa-argentina-2025-a.json","copa-argentina-2025-b.json"):
    data = json.loads((INV/fn).read_text(encoding='utf-8'))
    partidos += data["partidos"]
    shutil.move(str(INV/fn), str(SRC/fn))
partidos += [mk(x,"16avos") for x in d16]
partidos += [mk(x,"octavos") for x in d8]
partidos.sort(key=lambda p:p["fecha"])

# sanity: cada ronda con lo esperado
from collections import Counter
c = Counter(p["ronda"] for p in partidos)
assert c["32avos"]==31 and c["16avos"]==16 and c["octavos"]==8 and c["cuartos"]==4 and c["semifinal"]==2 and c["final"]==1, c

out = {"partidos": partidos}
(INV/"copa-argentina-2025.json").write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
print("copa-argentina-2025.json:", len(partidos), "partidos |", dict(c))
print("rango:", partidos[0]["fecha"], "a", partidos[-1]["fecha"])
