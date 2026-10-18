"""Integra investigacion/dias-fechas-1a10.json al mapa SCH del HTML.

Agrega entradas 'LOCAL-VISITA': ['Dia DD/MM'] (sin hora) para las fechas 1-10.
Claves que ya existan en SCH (fechas 11-16) NO se pisan; se reportan.
Al final valida contra PAST_RAW: cada cruce de las fechas 1-10 debe tener día.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(r'C:\Users\Usuario\proyectos\calculadora-clausura-2026')
HTML = ROOT / 'calculadora-clausura-2026.html'
J = ROOT / 'investigacion' / 'dias-fechas-1a10.json'

d = json.loads(J.read_text(encoding='utf-8'))
dudas = d.pop('dudas', [])
h = HTML.read_text(encoding='utf-8')

# 1) pares ya presentes en SCH (fechas 11-16)
sch_re = re.search(r'const SCH=\{(.*?)\};', h, re.S); assert sch_re, 'SCH no encontrado'
sch_block = sch_re.group(1)
existing = set(re.findall(r'"([A-Z]{3}-[A-Z]{3})":\[', sch_block))

# 2) canon PAST_RAW: cruces de fechas 1-10
past = {}
m = re.search(r'const PAST_RAW=\{(.*?)\};', h, re.S); assert m, 'PAST_RAW no encontrado'
for f, body in re.findall(r'(\d+):"([^"]*)"', m.group(1)):
    if int(f) > 10:
        continue
    for p in body.split(','):
        past.setdefault(int(f), set()).add(p.split(' ')[0])

# 3) construir el bloque nuevo
adds, colisiones, faltantes = [], [], []
for f in range(1, 11):
    data = d.get(str(f)) or d.get(f) or {}
    for par, dia in data.items():
        if dia is None:
            continue
        if par in existing:
            colisiones.append((f, par, 'ya en SCH'))
            continue
        if par not in past.get(f, set()):
            colisiones.append((f, par, 'no coincide con PAST_RAW'))
            continue
        adds.append((f, par, dia))
for f in range(1, 11):
    data = d.get(str(f)) or d.get(f) or {}
    for par in past.get(f, set()):
        if data.get(par) is None:
            faltantes.append((f, par))

if faltantes or colisiones:
    print('COLISIONES:', colisiones[:10])
    print('SIN DIA:', faltantes[:10], '| total:', len(faltantes))
    if not adds:
        sys.exit('nada para agregar')

# 4) validar formato de dia: 'Vie 18/09'
bad_fmt = [a for a in adds if not re.match(r'^(Lun|Mar|Mié|Jue|Vie|Sáb|Dom) \d{1,2}/\d{2}$', a[2])]
if bad_fmt:
    print('FORMATO RARO:', bad_fmt[:5]); sys.exit(1)

# 5) insertar: Object.assign(SCH, {...}) justo despues del cierre de SCH
new_entries = ','.join(f'"{p}":["{dia}"]' for _, p, dia in sorted(adds))
assign = f'\nObject.assign(SCH,{{{new_entries}}});'
h = h.replace(sch_block + '};', sch_block + '};' + assign, 1)
HTML.write_text(h, encoding='utf-8', newline='\n')
print(f'OK: {len(adds)} dias agregados a SCH | sin dia: {len(faltantes)} | colisiones: {len(colisiones)}')
print('dudas del recolector:', dudas if dudas else 'ninguna')
