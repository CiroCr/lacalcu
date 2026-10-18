"""Prueba de humo en un navegador real (Playwright). Uso: python tests/ui.py
Requiere: pip install playwright  y  python -m playwright install chromium"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parent.parent/'calculadora-clausura-2026.html').as_uri()
FIT="()=>{const p=document.querySelector('#fixtureList .panel');return p.scrollHeight-p.clientHeight}"
fallas=[];errs=[]
def ok(c,m):
    print(('OK     ' if c else 'FALLA  ')+m)
    if not c:fallas.append(m)
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1184,'height':909})
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto(URL);pg.wait_for_timeout(1500)
    ok(pg.input_value('#fSel')=='13','fecha por defecto = proxima fecha con partidos sin jugar (13)')
    ok(pg.evaluate("document.querySelectorAll('input:not([aria-label])').length")==0,'todas las cajas de goles tienen etiqueta accesible')
    ins=pg.locator('#fixtureList input:not([readonly])')
    ins.nth(0).fill('99');ok(ins.nth(0).input_value()=='15','99 se corrige a 15')
    ins.nth(0).fill('-3');ok(ins.nth(0).input_value()=='3','el signo menos se descarta')
    ins.nth(0).fill('abc');ok(ins.nth(0).input_value()=='','las letras se descartan')
    ins.nth(0).fill('2');ins.nth(1).fill('1');pg.wait_for_timeout(300)
    pg.reload();pg.wait_for_timeout(900)
    ins=pg.locator('#fixtureList input:not([readonly])')
    ok([ins.nth(0).input_value(),ins.nth(1).input_value()]==['2','1'],'lo simulado se guarda al recargar (localStorage)')
    pg.click('text=Borrar resultados');pg.reload();pg.wait_for_timeout(700)
    ok(pg.locator('#fixtureList input:not([readonly])').nth(0).input_value()=='','Borrar resultados limpia lo guardado')
    pg.select_option('#fSel','6');pg.wait_for_timeout(150)
    ok(pg.evaluate("document.querySelectorAll('#fixtureList .match.inter').length")==0 and pg.evaluate("!!document.querySelector('#fixtureList .dh')"),'fecha 6: aviso de fecha interzonal y sin bordes dorados')
    pg.wait_for_timeout(2200)
    ok('Elo' in pg.evaluate("document.querySelector('#PROB .ph').textContent") and pg.evaluate("document.querySelectorAll('#ELO tbody tr').length")>=30,'modelo Elo unico: probabilidades y ranking Elo (30 filas)')
    pg.evaluate("showPane('NEED',document.querySelectorAll('.tab')[5])");pg.wait_for_timeout(200)
    ok(pg.evaluate("document.getElementById('pane-NEED').classList.contains('on')"),'pestañas: abrir ¿Cuánto necesita? muestra su panel')
    pg.evaluate("showPane('PROB',document.querySelectorAll('.tab')[3])");pg.wait_for_timeout(200)
    pg.evaluate("showPane('NEED',document.querySelectorAll('.tab')[5])");pg.wait_for_timeout(200)
    pg.select_option('#selEq',label='Estudiantes (RC)');pg.wait_for_timeout(6000)
    ok(pg.evaluate("document.querySelectorAll('#needSvg .sline').length")>0 and pg.evaluate("document.getElementById('needOut').textContent.includes('Puntos a conseguir')"),'gráfico de puntos necesarios: SVG con líneas y ejes')
    for w,h in [(1184,909),(1366,768),(1920,1080)]:
        q=b.new_page(viewport={'width':w,'height':h});q.goto(URL);q.wait_for_timeout(700)
        ok(all((q.select_option('#fSel',f),q.wait_for_timeout(100),q.evaluate(FIT))[2]<=1 for f in ('11','12')),f'{w}x{h}: la fecha entra sin scroll en la columna de partidos')
    m=b.new_page(viewport={'width':390,'height':800});m.goto(URL);m.wait_for_timeout(900)
    ok(not m.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"),'celular (390px): sin desborde horizontal')
    ok(not errs,'sin errores en consola '+str(errs[:3]))
    b.close()
sys.exit(1 if fallas else 0)
