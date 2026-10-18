"""Partidos de playoffs, Copa Argentina, copas CONMEBOL y otros torneos 2025-2026 para el Elo.

Fuente: investigacion/*.json — recolección verificada por subagentes contra ESPN,
CONMEBOL, Wikipedia, TyC, La Nación, Infobae, etc. (el campo "fuentes" de cada
partido tiene las URLs; el campo "dudas" documenta alargues, penales y discrepancias
resueltas). Este módulo valida la estructura y las anclas, y devuelve las filas
en el formato que espera build.py: (fecha, 3, tokenLocal, tokenVisitante, gl, gv).

Reglas (HANDOFF §4.A):
  - gl/gv = marcador al final de los 90 o 120 minutos; los penales NUNCA se pliegan:
    una definición por penales cuenta como empate (estándar ClubElo).
  - Se excluye el partido suspendido Independiente-U. de Chile (Sudamericana 2025,
    descalificación de Independiente; marcador parcial 1-1 sin valor deportivo).
  - Se excluye el Trofeo de Campeones 2024 (21/12/2024): fuera de la ventana del
    Elo, que arranca en enero de 2025 junto con el Apertura 2025.
"""
import json, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INV = ROOT / 'investigacion'
D = dt.date

# archivo: cantidad esperada de partidos en 'partidos'
FILES = {
    'playoffs-apertura-2025.json': 15,
    'playoffs-clausura-2025.json': 15,
    'playoffs-apertura-2026.json': 15,
    'copa-argentina-2025.json': 62,
    'copa-argentina-2026.json': 59,
    'conmebol-2025.json': 33,
    'conmebol-2026.json': 30,
    'otros-torneos.json': 16,
}

# Finales ya verificadas contra múltiples fuentes (fecha, local, visitante, gl, gv)
ANCLAS = [
    ('2025-06-01', 'HUR', 'PLA', 0, 1),   # final Apertura 2025: Platense campeón
    ('2025-11-05', 'IRI', 'ARG', 2, 2),   # final Copa Argentina 2025: IRI campeón 5-3 pen.
    ('2025-12-13', 'RAC', 'EST', 1, 1),   # final Clausura 2025: EST campeón 5-4 pen.
    ('2026-05-24', 'RIV', 'BEL', 2, 3),   # final Apertura 2026: Belgrano campeón
]

def rows():
    out, bad = [], []
    for fn, expected in FILES.items():
        path = INV / fn
        if not path.exists():
            bad.append(('falta archivo', fn)); continue
        data = json.loads(path.read_text(encoding='utf-8'))
        ps = data.get('partidos')
        if not isinstance(ps, list):
            bad.append(('sin array partidos', fn)); continue
        if len(ps) != expected:
            bad.append(('conteo', fn, len(ps), expected))
        for p in ps:
            if 'suspend' in (p.get('dudas') or '').lower():
                continue  # partido no completado: sin valor deportivo
            d = D.fromisoformat(p['fecha'])
            if d < D(2025, 1, 1):
                continue  # fuera de la ventana del Elo
            out.append((d, 3, p['local'], p['visitante'], p['gl'], p['gv']))
    keys = {(r[0].isoformat(), r[2], r[3], r[4], r[5]) for r in out}
    for a in ANCLAS:
        if a not in keys:
            bad.append(('ancla', a))
    return out, bad

if __name__ == '__main__':
    r, bad = rows()
    print('knockouts:', len(r), 'partidos |', min(x[0] for x in r), 'a', max(x[0] for x in r),
          '| desajustes:', bad if bad else 'ninguno (anclas verificadas: 4 finales)')
