"""Incrusta los escudos reales (investigacion/escudos/*) en el HTML único como data-URI.

- SVG y PNG -> base64 (data:image/svg+xml;base64 o data:image/png;base64).
- Reemplaza la insignia dibujada (.bdg con colores) por <img> con el escudo real.
- Verifica: 30 escudos presentes, firma de archivo, HTML resultante parsea el
  <script> igual que tests/verificar.js espera, y tamaño final razonable.
Uso: python investigacion/embed_escudos.py [--check]  (--check solo muestra el estado)
"""
import base64, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESC = ROOT / 'investigacion' / 'escudos'
HTML = ROOT / 'calculadora-clausura-2026.html'
TEAMS = "VEL DYJ GEM INS BOC UNI NOB IND EST LAN SLO DRI PLA TAL CCO ARG ROS GLP BEL HUR SAR IRI ATU RIV BAR BAN RAC ERC ALD TIG".split()

def load_crests():
    out, missing, bad = {}, [], []
    for c in TEAMS:
        p = ESC / f'{c}.svg'
        mime = 'image/svg+xml'
        if not p.exists():
            p = ESC / f'{c}.png'
            mime = 'image/png'
        if not p.exists():
            missing.append(c); continue
        data = p.read_bytes()
        if mime == 'image/png':
            if not data.startswith(b'\x89PNG'):
                bad.append((c, 'sin firma PNG')); continue
        else:
            if b'<svg' not in data[:2000]:
                bad.append((c, 'sin marca <svg>')); continue
        out[c] = f'data:{mime};base64,' + base64.b64encode(data).decode()
    return out, missing, bad

def main(check_only=False):
    crests, missing, bad = load_crests()
    print('escudos listos:', len(crests), '/ 30')
    if missing: print('FALTAN:', ', '.join(missing))
    if bad: print('CON PROBLEMAS:', bad)
    total = sum(len(v) for v in crests.values())
    print('bytes base64 totales:', total, f'({total/1024:.0f} KB)')
    if check_only or missing or bad:
        return not (missing or bad)

    html = HTML.read_text(encoding='utf-8')

    # 1) inyectar el mapa de escudos antes de COL
    entries = ','.join(f'{c}:"{u}"' for c, u in crests.items())
    block = f'const CREST={{{entries}}};\n'
    if 'const CREST={' in html:
        html = re.sub(r'const CREST=\{[^}]*\};\n', block, html, count=1)
    else:
        html = html.replace('const COL={', block + 'const COL={', 1)

    # 2) badge: <img> con el escudo real (fallback a la insignia vieja si faltara uno)
    old_bdg = 'const bdg=c=>`<span class="bdg" style="--c1:${COL[c][0]};--c2:${COL[c][1]}">${c}</span>`;'
    new_bdg = ('const bdg=c=>CREST[c]?`<img class="bdg2" src="${CREST[c]}" alt="" loading="lazy">`'
               ':`<span class="bdg" style="--c1:${COL[c][0]};--c2:${COL[c][1]}">${c}</span>`;')
    assert old_bdg in html, 'no encontre la funcion bdg'
    html = html.replace(old_bdg, new_bdg, 1)

    # 3) CSS del img-escudo (mismas medidas que la insignia vieja)
    css_old = '.bdg{display:inline-flex;'
    css_new = ('.bdg2{display:inline-flex;flex:none;width:24px;height:24px;object-fit:contain;'
               'filter:drop-shadow(0 0 1px rgba(0,0,0,.5));border-radius:3px;vertical-align:-4px}\n'
               '.bdg{display:inline-flex;')
    assert css_old in html, 'no encontre el CSS .bdg'
    html = html.replace(css_old, css_new, 1)
    # en pantallas chicas, 22px igual que la insignia vieja
    html = html.replace('.bdg{width:22px;height:22px}}',
                        '.bdg{width:22px;height:22px}.bdg2{width:22px;height:22px}}', 1)

    HTML.write_text(html, encoding='utf-8', newline='\n')
    print('HTML actualizado:', HTML.stat().st_size, 'bytes',
          f'(+{(HTML.stat().st_size-55300)//1024} KB aprox)')
    # sanity: el script sigue extrayendose como en verificar.js
    m = re.search(r'<script>\n(// \[codigo[\s\S]*?)</script>', HTML.read_text(encoding='utf-8'))
    print('regex verificar.js sobre el <script>:', 'OK' if m and m.group(1) else 'FALLA')
    return True

if __name__ == '__main__':
    ok = main('--check' in sys.argv)
    sys.exit(0 if ok else 1)
