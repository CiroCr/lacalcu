"""Valida los JSON de investigacion/*.json antes de integrarlos al Elo.

Uso: python investigacion/validar.py [archivo1.json archivo2.json ...]
Sin argumentos valida todos los .json de la carpeta.

Chequea por partido: campos obligatorios, tokens validos, marcador entero razonable,
penales solo si hubo empate, al menos un equipo argentino, al menos una fuente,
fechas validas, duplicados dentro y entre archivos, y solapamiento con lo ya
cargado en el HTML (ELO_EXTRA + fechas del Clausura via RAW/PAST_RAW).
Al final imprime un resumen listo para leer.
"""
import json, re, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INV = ROOT / 'investigacion'
HTML = ROOT / 'calculadora-clausura-2026.html'

TEAMS = set("VEL DYJ GEM INS BOC UNI NOB IND EST LAN SLO DRI PLA TAL CCO ARG ROS GLP BEL HUR SAR IRI ATU RIV BAR BAN RAC ERC ALD TIG GOD SMA".split())
VIRTUAL = {"BR", "EXT", "LOW"}
VALID = TEAMS | VIRTUAL

def html_pairs():
    """Pares ya cargados en el HTML: ELO_EXTRA + PAST_RAW + RAW (con y sin score)."""
    h = HTML.read_text(encoding='utf-8')
    out = set()
    m = re.search(r'const ELO_EXTRA="([^"]*)"', h)
    if m:
        for x in m.group(1).split(','):
            p = x.split(' ')[0]
            l, v = p.split('-')
            out.add((l, v))
    for pat in (r'const PAST_RAW=\{(.*?)\};', r'const RAW=\{(.*?)\};'):
        m = re.search(pat, h, re.S)
        if m:
            for f, s in re.findall(r'(\d+):"([^"]*)"', m.group(1)):
                for x in s.split(','):
                    l, v = x.split(' ')[0].split('-')
                    out.add((l, v))
    return out

def main(files):
    loaded = html_pairs()
    all_keys, problems, stats = {}, [], []
    for fp in files:
        name = Path(fp).name
        try:
            data = json.loads(Path(fp).read_text(encoding='utf-8'))
        except Exception as e:
            print(f"[{name}] ERROR: no se puede leer: {e}")
            continue
        partidos = data.get('partidos') if isinstance(data, dict) else None
        if not isinstance(partidos, list):
            print(f"[{name}] ERROR: no tiene array 'partidos'")
            continue
        err, warn, fechas = [], [], []
        for i, p in enumerate(partidos):
            tag = f"[{name} #{i} {p.get('local','?')}-{p.get('visitante','?')}]"
            for k in ('fecha', 'torneo', 'ronda', 'local', 'visitante', 'gl', 'gv', 'nombreL', 'nombreV', 'fuentes'):
                if k not in p or p[k] in (None, '', []):
                    err.append(f"{tag} falta {k}")
            for k in ('local', 'visitante'):
                if p.get(k) not in VALID:
                    err.append(f"{tag} token invalido: {p.get(k)!r}")
            if p.get('local') not in TEAMS and p.get('visitante') not in TEAMS:
                err.append(f"{tag} ningun equipo argentino de la lista")
            if not isinstance(p.get('gl'), int) or not isinstance(p.get('gv'), int) or not (0 <= p['gl'] <= 20 and 0 <= p['gv'] <= 20):
                err.append(f"{tag} marcador invalido: {p.get('gl')}-{p.get('gv')}")
            pl, pv = p.get('penL'), p.get('penV')
            if (pl is None) != (pv is None):
                err.append(f"{tag} penales incompletos: {pl}/{pv}")
            if (pl is not None) and p['gl'] != p['gv']:
                warn.append(f"{tag} penales con marcador no empatado ({p['gl']}-{p['gv']}) — revisar (¿carga de 120'?)")
            try:
                d = dt.date.fromisoformat(p['fecha'])
                if not (dt.date(2025, 1, 1) <= d <= dt.date(2026, 12, 31)):
                    warn.append(f"{tag} fecha fuera de rango: {p['fecha']}")
                fechas.append(d)
            except Exception:
                err.append(f"{tag} fecha invalida: {p.get('fecha')!r}")
            if p.get('local') == p.get('visitante'):
                err.append(f"{tag} local == visitante")
            key = (p['fecha'], p['local'], p['visitante'])
            if key in all_keys:
                err.append(f"{tag} DUPLICADO de {all_keys[key]}")
            else:
                all_keys[key] = name
            # mismo cruce, misma fecha, localia invertida = probable doble carga del mismo partido
            inv = (p['fecha'], p.get('visitante'), p.get('local'))
            if inv in all_keys:
                warn.append(f"{tag} espejo de otro partido mismo dia (ida/vuelta ok, pero verificar)")
            if p.get('local') in TEAMS and p.get('visitante') in TEAMS:
                pk = (p['local'], p['visitante'])
                if pk in loaded and 'Copa Argentina' not in p.get('torneo', '') and 'playoff' not in p.get('torneo', '').lower():
                    # en liga regular cada cruce se juega 1 vez por semestre; ELO_EXTRA ya tiene 2025-2026 regulares
                    warn.append(f"{tag} cruce {pk[0]}-{pk[1]} ya existe en el HTML (¿seguro que es otro torneo/semestre?)")
            if p.get('dudas'):
                warn.append(f"{tag} DUDA reportada: {p['dudas']}")
        stats.append((name, len(partidos), min(fechas) if fechas else None, max(fechas) if fechas else None))
        print(f"\n=== {name}: {len(partidos)} partidos ===")
        for e in err: print("  ERROR:", e)
        for w in warn: print("  AVISO:", w)
        if not err and not warn: print("  todo OK")
    print("\n=== RESUMEN ===")
    tot = 0
    for name, n, d0, d1 in stats:
        print(f"  {name}: {n} partidos ({d0} a {d1})")
        tot += n
    print(f"  TOTAL: {tot} partidos en {len(stats)} archivos")

if __name__ == '__main__':
    args = sys.argv[1:]
    files = [Path(a) for a in args] if args else sorted(INV.glob('*.json'))
    if not files:
        print("No hay JSON para validar en", INV)
        sys.exit(1)
    main(files)
