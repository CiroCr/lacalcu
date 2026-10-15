# HANDOFF — Simulador Clausura 2026 (calculadora de la Liga Profesional argentina)

- **Fecha del traspaso:** 12/10/2026
- **Origen:** Claude (chat de claude.ai). **Destino:** Hermes Agent (Nous Research) sobre Windows.
- **Carpeta destino (convención del usuario):** `C:\Users\Usuario\proyectos\calculadora-clausura-2026\`
- **Idioma del usuario y de la interfaz:** español rioplatense (Argentina). Todo texto visible en la app va en español.

## 0. Cómo usar este documento

1. La sección 1 trae **todos los archivos con su código íntegro** (copias exactas, con tamaño y SHA-256 para comprobar que no se alteró nada al pegarlos). Si también recibiste el `.zip`, es la misma estructura lista para descomprimir dentro de `C:\Users\Usuario\proyectos\`.
2. Antes de tocar nada: hacé una **copia de seguridad de la carpeta** y corré los dos controles de la sección 2 (`node tests\verificar.js` y `python tests\ui.py`). Deben dar todo OK. Repetilos después de cada cambio.
3. Lo primero que conviene hacer es **actualizar los resultados que se jugaron desde el 11/10** (receta en la sección 2.5).
4. Regla de oro del proyecto: **los datos se verifican contra tablas publicadas** antes de darlos por buenos. No inventar resultados ni completar de memoria.

---

## 1. INVENTARIO COMPLETO

### 1.1 Estructura de carpetas

```
C:\Users\Usuario\proyectos\calculadora-clausura-2026\
├── calculadora-clausura-2026.html      <- la app (se abre con doble clic; no necesita servidor)
├── HANDOFF.md                          <- este documento
├── datos\
│   ├── build.py                        <- valida fuentes y regenera ELO_EXTRA
│   ├── mats.py                         <- matrices de resultados (Wikipedia)
│   ├── cups.py                         <- grupos de Libertadores/Sudamericana
│   └── ar2025.txt                      <- Apertura 2025 (openfootball)
└── tests\
    ├── verificar.js                    <- datos + motor + Elo (Node)
    └── ui.py                           <- prueba en navegador (Playwright)
```

### 1.2 Archivos (tamaño y huella SHA-256)

| Ruta | Rol | Tamaño | SHA-256 |
|---|---|---|---|
| `calculadora-clausura-2026.html` | La aplicación completa (HTML + CSS + JS en un solo archivo). | 48,602 bytes | `b46628e03682eadfd35b5483f90336ff5907d013547aea4f9ca5a88cd144f92f` |
| `datos\\build.py` | Valida las fuentes de datos y regenera la lista ELO_EXTRA dentro del HTML (--write). | 6,143 bytes | `3a2bb29e2984f0a3266acfcbae9f28c4be608b4e6c21e6e548a3ea87bd085c5e` |
| `datos\\mats.py` | Matrices de resultados y tablas finales copiadas de Wikipedia (Clausura 2025, Apertura 2026) usadas por build.py. | 9,769 bytes | `4bd7a6e6417daa28eb50be13eda433509a9c9f09939841501aa2265e522fef05` |
| `datos\\cups.py` | Fase de grupos de Libertadores y Sudamericana 2025-2026 de los equipos argentinos, con validación contra las tablas de grupo. | 5,602 bytes | `0f50612fce5338a8e13fae2291eb56cad743874a0b1de395f0f39a39807b37a0` |
| `datos\\ar2025.txt` | Apertura 2025 completo (openfootball/south-america, argentina/2025_ar1.txt), tal cual se descargó. | 19,136 bytes | `e087b6827b229bfd797da1293f735ba1958d54c294a27bc7eb863bca5bf71289` |
| `tests\\verificar.js` | Verificación de datos, motor, simulación, Elo y comparación de modelos (Node). | 6,235 bytes | `f54dc02944f6bbdbe61ddc1bd3f30251bc42af75d9644aa0d2a93dc8a99e2dd2` |
| `tests\\ui.py` | Prueba de humo en navegador real (Playwright). | 3,407 bytes | `d7c230091480b746cf7dfb68168f83dddbf68952a3d5e1e9e7b7ce0b11ef7703` |

### 1.3 Código íntegro de cada archivo

#### `calculadora-clausura-2026.html`

La aplicación completa (HTML + CSS + JS en un solo archivo).

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Calculadora Clausura 2026: simulá la tabla, la anual y los promedios</title>
<meta name="description" content="Simulador del Torneo Clausura 2026 de la Liga Profesional: cargá los resultados de las fechas 11 a 16 y mirá cómo cambian la tabla de cada zona, la tabla anual y la tabla de promedios (descenso).">
<meta name="keywords" content="calculadora clausura 2026, simulador liga profesional, tabla de promedios 2026, tabla anual 2026, descenso 2026, simulador fecha 11">
<link rel="canonical" href="https://TU-DOMINIO.com/">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR">
<meta property="og:title" content="Calculadora Clausura 2026: tabla, anual y promedios">
<meta property="og:description" content="Cargá los resultados que faltan y mirá quién clasifica, quién va a copas y quién desciende.">
<meta property="og:url" content="https://TU-DOMINIO.com/">
<meta name="theme-color" content="#0b2a14">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"Calculadora Clausura 2026","applicationCategory":"SportsApplication","operatingSystem":"Web","inLanguage":"es-AR","offers":{"@type":"Offer","price":"0","priceCurrency":"ARS"}}</script>
<!-- Google AdSense: pegá acá tu código cuando te aprueben la cuenta -->
<style>
:root{--bg:#1b4a2a;--bg2:#0b2a14;--panel:#0e3a1d;--head:#0a2d16;--line:#1c5a2e;--text:#fff;--muted:#8fb99a;--acc:#4caf50;--inp:#082411;--pl:rgba(76,175,80,.18);--lib:rgba(242,194,0,.2);--sud:rgba(90,178,230,.2);--rel:rgba(215,25,32,.32);font-family:Roboto,-apple-system,"Segoe UI",Arial,sans-serif}
*{box-sizing:border-box}
html{scroll-padding-top:calc(64px + env(safe-area-inset-top,0px))}
body{margin:0;color:var(--text);background:radial-gradient(circle at 20% 0,var(--bg),var(--bg2) 70%) fixed;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}
.top{display:flex;align-items:baseline;gap:14px;max-width:1100px;margin:0 auto;padding:14px 14px 4px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.logo{margin:0;font-size:1.6rem;font-weight:900;letter-spacing:.02em}.logo b{color:var(--acc)}
.top span{color:var(--muted);font-size:.85rem}
.shell{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:18px;padding:0 14px 30px;align-items:start}
.jump{position:sticky;top:calc(6px + env(safe-area-inset-top,0px));z-index:5;width:calc(100% - 28px);max-width:1172px;margin:6px auto 12px;display:flex;gap:2px;overflow-x:auto;background:var(--head);border-radius:8px;padding:4px}
.jump a{color:#d7e9dc;text-decoration:none;font-size:.82rem;font-weight:600;padding:7px 11px;white-space:nowrap;border-radius:6px}.jump a:hover{background:rgba(255,255,255,.1);color:var(--acc)}
.col-p{border-radius:8px}
.pad{padding:12px 14px}
select{width:100%;padding:9px;border-radius:6px;border:1px solid var(--line);background:var(--inp);color:#fff;font-size:.9rem}
.panel{background:var(--panel);border-radius:8px;margin-bottom:12px;overflow:hidden}
.ph{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--head);font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.bar{display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:12px 14px;margin-bottom:12px;background:var(--panel);border-radius:8px}
.note{font-size:.8rem;color:var(--muted);line-height:1.6}
.btn{background:var(--acc);color:#04210d;border:none;padding:8px 16px;border-radius:6px;font-size:.8rem;font-weight:700;cursor:pointer}
.fnav{display:flex;align-items:center;gap:6px;background:var(--head);border-radius:8px;padding:6px;margin-bottom:12px}
.fnav select{flex:1;width:auto;text-align:center;text-align-last:center;font-weight:800;font-size:.95rem;text-transform:uppercase;background:transparent;border:0;cursor:pointer}
option{background:#0a2d16;color:#fff}
.arr{background:none;border:0;color:#fff;font-size:1.7rem;line-height:1;padding:2px 16px 6px;cursor:pointer;border-radius:6px}.arr:hover:not(:disabled){background:rgba(255,255,255,.1)}.arr:disabled{opacity:.25;cursor:default}
.dh{padding:7px 14px;font-size:.78rem;color:var(--muted);text-align:center;background:rgba(0,0,0,.18);border-bottom:1px solid var(--line)}
.match input[readonly]{background:transparent;border-color:transparent;color:#fff;pointer-events:none}
.match{display:grid;grid-template-columns:56px 1fr 36px 10px 36px 1fr;align-items:center;gap:6px;padding:0 10px 0 0;min-height:46px;border-bottom:1px solid var(--line);font-size:.85rem}
.match.inter{box-shadow:inset 3px 0 0 #f2c200}
.st{align-self:stretch;display:flex;align-items:center;justify-content:center;border-right:1px solid var(--line);font-size:.66rem;font-weight:700;color:var(--muted);background:rgba(0,0,0,.12)}
.st.fin{color:#fff}
.side{display:flex;align-items:center;gap:8px;min-width:0;font-weight:600}.side .t{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.side.h{justify-content:flex-end;flex-direction:row-reverse;text-align:right}
.match input{width:36px;padding:7px 0;border-radius:6px;border:1px solid var(--line);background:var(--inp);color:#fff;text-align:center;font-size:.95rem;font-weight:700}
.match input:focus{outline:2px solid var(--acc)}.vs{color:var(--muted);text-align:center}
.tblwrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.85rem}
th,td{padding:9px 6px;text-align:center;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-size:.68rem;font-weight:700;text-transform:uppercase}
td.eq{text-align:left;font-weight:600}.nm{display:inline-flex;align-items:center;gap:9px}
tr.playoff td{background:var(--pl)}tr.playoff td:first-child{box-shadow:inset 3px 0 0 var(--acc)}
tr.lib td,tr.camp td{background:var(--lib)}tr.camp td:first-child{box-shadow:inset 3px 0 0 #f2c200}.tag{font-size:.6rem;font-weight:700;color:#f2c200;border:1px solid #f2c200;border-radius:4px;padding:1px 5px;margin-left:8px;white-space:nowrap}tr.sud td{background:var(--sud)}tr.releg td{background:var(--rel)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:.72rem;color:var(--muted);padding:10px 14px}
.dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.bdg{display:inline-flex;flex:none;width:24px;height:24px;border-radius:50%;align-items:center;justify-content:center;font-size:.46rem;font-weight:800;color:#fff;text-shadow:0 0 2px #000,0 0 2px #000;border:1px solid rgba(255,255,255,.35);background:linear-gradient(90deg,var(--c1) 50%,var(--c2) 50%)}
.txt{padding:14px;background:var(--panel);border-radius:8px;margin-bottom:12px}
.txt h2{font-size:1rem;margin:14px 0 6px}.txt h2:first-child{margin-top:0}
.foot{max-width:1100px;margin:0 auto;padding:0 14px 30px;text-align:center}
@media(max-width:760px){
.shell{grid-template-columns:minmax(0,1fr);gap:10px}.col-p{position:static;max-height:none;overflow:visible}
.match{grid-template-columns:44px 1fr 32px 6px 32px 1fr;gap:4px;font-size:.78rem}
.match input{width:32px}.side{gap:5px}.bdg{width:22px;height:22px}}
@media(min-width:761px){
#PART{position:sticky;top:60px;height:calc(100vh - 122px);min-height:420px;display:flex;flex-direction:column}
#PART .bar,#PART .fnav{flex:none;margin-bottom:8px}
#PART .bar{padding:8px 12px}#PART .bar .note{font-size:.72rem;line-height:1.35}#PART .btn{padding:6px 12px}
#PART .fnav{padding:3px 6px}
#fixtureList{flex:1;min-height:0;display:flex}
#fixtureList .panel{flex:1;display:flex;flex-direction:column;min-height:0;overflow-y:hidden;margin:0}
#fixtureList .ph{flex:none;padding:7px 14px}#fixtureList .dh{flex:none;padding:2px 14px;font-size:.72rem}
#fixtureList .match{flex:1 1 0;min-height:22px;max-height:46px}
#fixtureList .match input{padding:3px 0;font-size:.85rem}
}
@media(min-width:761px) and (max-height:759px){#fixtureList .panel{overflow-y:auto}}
</style>
</head>
<body>
<div class="top"><h1 class="logo">SIMULA<b>DOR</b><span class="sr"> Calculadora del Clausura 2026 de la Liga Profesional</span></h1><span>Clausura 2026, Liga Profesional</span></div>
<nav class="jump"><a href="#PART">Partidos</a><a href="#A">Zona A</a><a href="#B">Zona B</a><a href="#ANUAL">Anual</a><a href="#PROM">Promedios</a><a href="#PROB">Probabilidades</a><a href="#NEED">Necesita ganar</a></nav>
<div class="shell">
  <section id="PART" class="col-p">
    <div class="bar"><span class="note">Oficiales bloqueados. Cargá goles en los pendientes para simular (se guardan en tu navegador). Dorado = interzonal (fecha 6: todos).</span>
    <button class="btn" onclick="resetAll()">Borrar resultados</button></div>
    <div class="fnav"><button class="arr" id="fPrev" onclick="goF(-1)" aria-label="Fecha anterior">&#8249;</button><select id="fSel" onchange="setF(+this.value)" aria-label="Elegir fecha"></select><button class="arr" id="fNext" onclick="goF(1)" aria-label="Fecha siguiente">&#8250;</button></div>
    <div id="fixtureList"></div>
  </section>
  <main>
    <div id="A"></div><div id="B"></div><div id="ANUAL"></div><div id="PROM"></div><div class="bar"><span class="note">Modelo de fuerza para simular:</span><select id="selModel" aria-label="Modelo de fuerza" onchange="setModel(this.value)" style="width:auto"><option value="goles">Goles (ataque y defensa)</option><option value="elo">Elo (en prueba)</option></select></div>
    <div id="PROB"></div><div id="ELO"></div>
    <div id="NEED" class="panel"><div class="ph">¿Cuántas victorias necesita tu equipo?</div><div class="pad"><select id="selEq" onchange="renderNeed()" aria-label="Elegir equipo"></select></div><div id="needOut"></div></div>
    <div class="txt note"><h2>Fuentes y datos</h2>
      <p><b>Fixture:</b> Liga Profesional de Fútbol de AFA, "Agenda para la temporada 2026" (ligaprofesional.ar), fechas 11 a 16 del Clausura. Las fechas/horarios pueden moverse, los cruces no.</p>
      <p><b>Base:</b> tablas de la Zona A y B con la fecha 10 completa (los 30 equipos con 10 PJ), según futbolargentino.com y Mendoza Post (21/09/2026). El Apertura (cerrado) y los puntos de 2024 y 2025 para los promedios salen de Wikipedia / AFA. Tabla Anual y Promedios se calculan sumando esos datos fijos a lo que cargues en las fechas 11 a 16. Verificá contra ligaprofesional.ar antes de usarlo para algo importante.</p>
      <p><b>Formato:</b> 2 zonas de 15, 16 fechas (14 de zona + 2 interzonales), clasifican los 8 primeros de cada zona. Anual = Apertura (campeón Belgrano) + Clausura: Libertadores los 3 mejores sin cupo previo, Sudamericana los 6 siguientes, desciende el último (sin contar al que baje por promedios). Promedios = puntos 2024+2025+2026 sobre partidos jugados; desciende el peor.</p>
      <p><b>Resultados:</b> fechas 1 a 12 (parcial) según futbolargentino.com, ligaprofesional.ar y medios, con los partidos jugados hasta el 11/10/2026. Se controlaron contra las tablas: cada equipo suma exactamente los PJ, puntos y goles de la base. 23 resultados de las fechas 1 a 3 que no figuraban en esa fuente se calcularon cruzando esos totales (la solución es única). Los resultados de la fecha 11 y siguientes se cargan a mano a medida que se juegan.</p>
      <p><b>Escudos:</b> son insignias dibujadas con los colores de cada club, no los logos oficiales.</p></div>
    <div class="txt note">
      <h2>Cómo funciona la calculadora del Clausura 2026</h2>
      <p>En la columna <b>Partidos</b> (a la izquierda; arriba en el celular) se ven las 16 fechas: las flechas cambian de fecha y arranca en la próxima. En las fechas 11 a 16 escribí los goles de los partidos pendientes y se actualizan al instante las dos zonas, la Tabla Anual y la Tabla de Promedios. Los 8 primeros de cada zona clasifican a los octavos de final. Más abajo, <b>Probabilidades</b> muestra qué tan probable es cada resultado y <b>Necesita ganar</b> te dice cuántas victorias le hacen falta a tu equipo.</p>
      <h2>Preguntas frecuentes</h2>
      <p><b>¿Cómo se define el descenso en 2026?</b> Descienden dos equipos: el último de la Tabla Anual (puntos del Apertura más el Clausura) y el de peor promedio (puntos de 2024, 2025 y 2026 divididos por los partidos jugados en Primera). Si el mismo equipo es último en las dos tablas, desciende por promedios y el segundo descenso es para el anteúltimo de la anual.</p>
      <p><b>¿Quién clasifica a la Copa Libertadores y a la Sudamericana?</b> Son seis plazas a la Libertadores: los campeones del Apertura (Belgrano), del Clausura y de la Copa Argentina, más los tres mejores de la Tabla Anual que no clasificaron por título. A la Sudamericana van los seis siguientes de la anual, también sin contar a quienes ya tienen lugar. El 1° de la anual es el Campeón de Liga.</p>
      <p><b>¿Cómo se desempata?</b> Puntos, diferencia de gol y goles a favor. En esta herramienta no se aplican los criterios siguientes (resultado entre sí, fair play).</p>
      <p><b>¿Los datos son oficiales?</b> Es una herramienta independiente, sin relación con la AFA ni la Liga Profesional. Resultados cargados hasta el 11/10/2026; verificá en ligaprofesional.ar.</p>
    </div>
  </main>
</div>
<div class="foot note">Herramienta independiente, no afiliada a la AFA ni a la Liga Profesional. Los escudos son insignias ilustrativas.</div>
<script>
// [codigo, nombre, apPts, apGF, apGC, clPJ, clPts, clGF, clGC, h24, h25, pjHist]
const ZA=[["VEL","Vélez Sarsfield",28,18,12,10,20,15,9,76,40,73],["DYJ","Defensa y Justicia",19,18,21,10,18,13,11,58,38,73],["GEM","Gimnasia y Esgrima (M)",19,14,22,10,17,14,9,0,0,0],["INS","Instituto",21,17,17,10,22,13,7,53,34,73],["BOC","Boca Juniors",30,22,9,10,17,14,11,67,62,73],["UNI","Unión",21,24,20,10,13,17,16,60,39,73],["NOB","Newell's Old Boys",15,15,27,10,16,11,8,49,33,73],["IND","Independiente",24,24,20,10,17,10,8,63,47,73],["EST","Estudiantes (LP)",31,19,7,10,10,10,11,63,42,73],["LAN","Lanús",24,18,15,10,16,13,9,59,50,73],["SLO","San Lorenzo",22,14,14,10,11,4,8,45,51,73],["DRI","Deportivo Riestra",11,5,12,10,10,8,10,48,52,73],["PLA","Platense",16,10,15,10,9,9,15,57,35,73],["TAL","Talleres (C)",26,17,13,10,8,11,17,72,34,73],["CCO","Central Córdoba (SdE)",16,11,21,10,8,7,13,42,42,73]];
const ZB=[["ARG","Argentinos Juniors",29,17,13,10,18,13,9,56,57,73],["ROS","Rosario Central",28,20,16,10,18,11,8,47,66,73],["GLP","Gimnasia y Esgrima (LP)",26,19,19,10,17,15,15,48,38,73],["BEL","Belgrano",26,17,13,10,16,11,7,49,37,73],["HUR","Huracán",22,17,13,10,16,10,8,62,47,73],["SAR","Sarmiento (J)",19,13,20,10,16,17,16,35,35,73],["IRI","Independiente Rivadavia",34,29,15,10,17,14,13,46,43,73],["ATU","Atlético Tucumán",14,15,20,10,13,7,6,50,34,73],["RIV","River Plate",29,22,12,10,13,13,12,70,53,73],["BAR","Barracas Central",21,15,15,10,12,5,7,49,49,73],["BAN","Banfield",18,17,19,10,9,11,16,41,35,73],["RAC","Racing",21,17,15,10,8,11,16,70,53,73],["ERC","Estudiantes (RC)",5,5,24,10,6,5,13,0,0,0],["ALD","Aldosivi",8,6,19,10,8,12,16,0,33,32],["TIG","Tigre",20,18,15,10,12,9,9,39,49,73]];
const mk=a=>({c:a[0],n:a[1],apPts:a[2],apGF:a[3],apGC:a[4],clPJ:a[5],clPts:a[6],clGF:a[7],clGC:a[8],h24:a[9],h25:a[10],pj:a[11]});
const TA=ZA.map(mk),TB=ZB.map(mk),ALL=TA.concat(TB),T={};ALL.forEach(t=>T[t.c]=t);
// colores de camiseta [c1,c2]
const COL={VEL:["#fff","#0b3d91"],DYJ:["#f2c200","#0a6b2e"],GEM:["#111","#fff"],INS:["#d71920","#fff"],BOC:["#0b3d91","#f2c200"],UNI:["#d71920","#fff"],NOB:["#d71920","#111"],IND:["#d71920","#fff"],EST:["#d71920","#fff"],LAN:["#7a1f2b","#fff"],SLO:["#0b3d91","#d71920"],DRI:["#111","#fff"],PLA:["#6b3a1e","#fff"],TAL:["#0b3d91","#fff"],CCO:["#111","#fff"],ARG:["#d71920","#fff"],ROS:["#0b3d91","#f2c200"],GLP:["#0b3d91","#fff"],BEL:["#5ab2e6","#fff"],HUR:["#fff","#d71920"],SAR:["#0a6b2e","#fff"],IRI:["#0b3d91","#fff"],ATU:["#5ab2e6","#fff"],RIV:["#fff","#d71920"],BAR:["#d71920","#111"],BAN:["#0a6b2e","#fff"],RAC:["#5ab2e6","#fff"],ERC:["#d71920","#fff"],ALD:["#0a6b2e","#f2c200"],TIG:["#0b3d91","#d71920"]};
const bdg=c=>`<span class="bdg" style="--c1:${COL[c][0]};--c2:${COL[c][1]}">${c}</span>`;
// Fixture oficial LPF fechas 11-16 (* = interzonal)
const RAW={11:"TAL-BEL 0-1,IND-INS 1-4,BOC-UNI 3-0,DYJ-SLO 3-0,DRI-CCO 1-1,EST-GEM 3-0,NOB-LAN 0-0,VEL-PLA 2-2,ERC-RAC 1-2,SAR-RIV,HUR-ALD 1-0,ATU-BAR 2-3,IRI-GLP 1-1,BAN-ROS 1-1,ARG-TIG 2-1",
12:"PLA-ARG,LAN-VEL,GEM-NOB,CCO-EST 2-2,SLO-DRI,UNI-DYJ 0-2,INS-BOC 2-2,TAL-IND,TIG-BAN 1-2,ROS-IRI,GLP-ATU 1-1,BAR-HUR 2-0,ALD-SAR 1-3,RIV-ERC 1-0,RAC-BEL",
13:"RAC-IND,BOC-TAL,DYJ-INS,DRI-UNI,EST-SLO,NOB-CCO,VEL-GEM,PLA-LAN,BEL-RIV,ERC-ALD,SAR-BAR,HUR-GLP,ATU-ROS,IRI-TIG,BAN-ARG",
14:"BAN-LAN,GEM-PLA,CCO-VEL,SLO-NOB,UNI-EST,INS-DRI,TAL-DYJ,IND-BOC,ARG-IRI,TIG-ATU,ROS-HUR,GLP-SAR,BAR-ERC,ALD-BEL,RIV-RAC",
15:"BOC-RIV,DYJ-IND,DRI-TAL,EST-INS,NOB-UNI,VEL-SLO,PLA-CCO,LAN-GEM,RAC-ALD,BEL-BAR,ERC-GLP,SAR-ROS,HUR-TIG,ATU-ARG,IRI-BAN",
16:"GEM-IRI,CCO-LAN,SLO-PLA,UNI-VEL,INS-NOB,TAL-EST,IND-DRI,BOC-DYJ,BAN-ATU,ARG-HUR,TIG-SAR,ROS-ERC,GLP-BEL,BAR-RAC,ALD-RIV"};
const zi=c=>TA.some(t=>t.c===c)?0:1;
const FX=[];Object.keys(RAW).forEach(f=>RAW[f].split(",").forEach(x=>{const[p,sc]=x.split(" "),[h,a]=p.split("-");FX.push([+f,h,a,zi(h)!==zi(a),sc?sc.split("-").map(Number):null]);}));
const res=FX.map(()=>null),part=FX.map(()=>null);
function initRes(){FX.forEach((m,i)=>{res[i]=m[4]?{gh:m[4][0],ga:m[4][1]}:null;part[i]=m[4]?{gh:String(m[4][0]),ga:String(m[4][1])}:null})}initRes();
function proj(t){let pj=0,gf=0,gc=0,pts=0;FX.forEach((f,i)=>{const r=res[i];if(!r)return;
 if(f[1]===t.c){pj++;gf+=r.gh;gc+=r.ga;pts+=r.gh>r.ga?3:r.gh===r.ga?1:0}
 else if(f[2]===t.c){pj++;gf+=r.ga;gc+=r.gh;pts+=r.ga>r.gh?3:r.gh===r.ga?1:0}});
 return{PJ:t.clPJ+pj,GF:t.clGF+gf,GC:t.clGC+gc,DG:t.clGF+gf-t.clGC-gc,Pts:t.clPts+pts}}
const dg=n=>(n>0?"+":"")+n,nm=t=>`<span class="nm">${bdg(t.c)}${t.n}</span>`;
const panel=(title,body,leg)=>`<div class="panel"><div class="ph">${title}</div><div class="tblwrap">${body}</div>${leg?`<div class="legend">${leg}</div>`:''}</div>`;
function zone(id,teams,title){const r=teams.map(t=>({t,p:proj(t)})).sort((a,b)=>b.p.Pts-a.p.Pts||b.p.DG-a.p.DG||b.p.GF-a.p.GF);
 let h='<table><tr><th>#</th><th style="text-align:left">Equipo</th><th>Pts</th><th>PJ</th><th>F:C</th><th>DG</th></tr>';
 r.forEach((x,i)=>h+=`<tr class="${i<8?'playoff':''}"><td>${i+1}</td><td class="eq">${nm(x.t)}</td><td><b>${x.p.Pts}</b></td><td>${x.p.PJ}</td><td>${x.p.GF}:${x.p.GC}</td><td>${dg(x.p.DG)}</td></tr>`);
 document.getElementById(id).innerHTML=panel(title,h+'</table>','<span><span class="dot" style="background:var(--acc)"></span>Clasifica a playoffs (top 8)</span>')}
const worstProm=()=>ALL.map(t=>{const p=proj(t);return{c:t.c,a:(t.h24+t.h25+t.apPts+p.Pts)/(t.pj+16+p.PJ)}}).sort((x,y)=>x.a-y.a)[0];
function anual(){const r=ALL.map(t=>{const p=proj(t);return{t,pts:t.apPts+p.Pts,d:t.apGF-t.apGC+p.DG,pj:16+p.PJ,gf:t.apGF+p.GF,gc:t.apGC+p.GC}}).sort((a,b)=>b.pts-a.pts||b.d-a.d);
 const w=worstProm(),di=r[29].t.c===w.c?28:29;
 let h='<table><tr><th>#</th><th style="text-align:left">Equipo</th><th>Pts</th><th>PJ</th><th>F:C</th><th>DG</th></tr>';
 let c3=0;const cls=r.map(x=>{if(x.t.c==='BEL')return 'camp';c3++;return c3<=3?'lib':c3<=9?'sud':''});
 r.forEach((x,i)=>{const c=i===di?'releg':cls[i];
 h+=`<tr class="${c}"><td>${i+1}</td><td class="eq">${nm(x.t)}${x.t.c==='BEL'?'<span class="tag">Campeón Apertura</span>':''}</td><td><b>${x.pts}</b></td><td>${x.pj}</td><td>${x.gf}:${x.gc}</td><td>${dg(x.d)}</td></tr>`});
 document.getElementById('ANUAL').innerHTML=panel('Tabla anual',h+'</table>','<span><span class="dot" style="background:#f2c200"></span>Libertadores (3 mejores sin título)</span><span><span class="dot" style="background:#5ab2e6"></span>Sudamericana (6 siguientes)</span><span><span class="dot" style="background:#d71920"></span>Descenso por tabla anual</span><span style="flex-basis:100%">Belgrano ya tiene su lugar en la Libertadores como campeón del Apertura y no ocupa un cupo de la anual. Los campeones del Clausura y de la Copa Argentina también clasifican y liberarían su lugar si terminan arriba: eso todavía no está modelado.</span>'+(di===28?`<span style="flex-basis:100%">${r[29].t.n} es último en la anual y en los promedios: desciende por promedios, y el descenso de la anual pasa a ${r[28].t.n}.</span>`:''))}
function prom(){const r=ALL.map(t=>{const p=proj(t),pt=t.h24+t.h25+t.apPts+p.Pts,pj=t.pj+16+p.PJ;return{t,pt,pj,a:pt/pj}}).sort((a,b)=>b.a-a.a);
 let h='<table><tr><th>#</th><th style="text-align:left">Equipo</th><th>Prom.</th><th>Pts</th><th>PJ</th></tr>';
 r.forEach((x,i)=>h+=`<tr class="${i===29?'releg':''}"><td>${i+1}</td><td class="eq">${nm(x.t)}</td><td><b>${x.a.toFixed(3)}</b></td><td>${x.pt}</td><td>${x.pj}</td></tr>`);
 document.getElementById('PROM').innerHTML=panel('Promedios',h+'</table>','<span><span class="dot" style="background:#d71920"></span>Peor promedio = desciende</span>')}
// Resultados reales de las fechas 1 a 10 (ya incluidos en la base de las tablas, solo se muestran)
const PAST_RAW={1:"BEL-ROS 2-1,SAR-ARG 2-3,DYJ-ALD 1-1,GEM-CCO 1-0,RAC-GLP 2-1,VEL-INS 1-0,HUR-BAN 1-0,PLA-UNI 2-2,ERC-TIG 1-0,NOB-TAL 1-0,RIV-BAR 0-1,LAN-SLO 1-0,ATU-IRI 0-0,EST-IND 0-2,DRI-BOC 3-0",
2:"SLO-GEM 1-0,BAN-SAR 3-2,ARG-ERC 3-0,ROS-RAC 0-0,BAR-ALD 1-0,DYJ-DRI 2-1,GLP-RIV 1-0,INS-PLA 2-1,IRI-HUR 2-1,TAL-VEL 1-3,IND-NOB 1-0,CCO-ATU 0-2,BOC-EST 1-0,TIG-BEL 0-0,UNI-LAN 2-1",
3:"GEM-UNI 2-0,ERC-BAN 0-0,BEL-ARG 0-1,EST-DYJ 3-0,RAC-TIG 1-3,DRI-BAR 0-1,ALD-GLP 1-2,NOB-BOC 2-2,RIV-ROS 0-1,LAN-INS 0-1,SAR-IRI 2-1,PLA-TAL 0-4,VEL-IND 1-0,CCO-SLO 1-0,HUR-ATU 0-0",
4:"UNI-CCO 1-2,ROS-ALD 2-1,ARG-RAC 2-1,TIG-RIV 1-0,DYJ-NOB 2-1,BAN-BEL 0-2,IND-PLA 0-1,ATU-SAR 1-2,SLO-HUR 0-2,INS-GEM 1-0,BOC-VEL 1-1,GLP-BAR 2-0,DRI-EST 2-0,TAL-LAN 0-3,IRI-ERC 2-1",
5:"ALD-TIG 0-0,RIV-ARG 2-0,LAN-IND 1-3,SLO-UNI 1-0,VEL-DYJ 1-1,RAC-BAN 0-1,GEM-TAL 3-1,SAR-HUR 2-0,ERC-ATU 0-1,BEL-IRI 2-0,EST-GLP 4-0,PLA-BOC 1-1,BAR-ROS 0-1,CCO-INS 0-1,NOB-DRI 2-0",
6:"BEL-DYJ 1-2,SAR-EST 2-0,RAC-BOC 1-1,ATU-INS 0-0,GLP-GEM 2-3,TAL-ROS 2-2,BAR-PLA 1-2,IND-IRI 0-0,NOB-BAN 2-1,HUR-DRI 0-0,TIG-CCO 2-1,ERC-SLO 0-0,RIV-VEL 2-2,ALD-UNI 1-3,LAN-ARG 1-1",
7:"DYJ-PLA 1-0,INS-SLO 1-0,ATU-BEL 0-0,TAL-CCO 0-0,IND-GEM 0-3,TIG-BAR 0-0,ROS-GLP 1-2,DRI-VEL 1-1,EST-NOB 0-0,UNI-SAR 4-1,IRI-RAC 3-1,HUR-ERC 1-1,BAN-RIV 2-3,BOC-LAN 1-0,ARG-ALD 2-1",
8:"GEM-BOC 2-2,CCO-IND 0-1,SLO-TAL 1-0,ROS-NOB 1-1,BAR-ARG 0-0,UNI-INS 3-2,LAN-DYJ 1-0,GLP-TIG 2-1,ALD-BAN 3-1,PLA-DRI 1-1,VEL-EST 1-0,RIV-IRI 3-1,BEL-HUR 1-1,ERC-SAR 0-2,RAC-ATU 1-2",
9:"BAN-BAR 1-1,DRI-LAN 0-3,BOC-CCO 3-1,IND-SLO 1-1,TAL-UNI 2-1,EST-PLA 2-1,IRI-ALD 4-3,TIG-ROS 0-1,HUR-RAC 2-1,ARG-GLP 1-1,SAR-BEL 1-1,ATU-RIV 1-2,DYJ-GEM 2-0,NOB-VEL 1-1,INS-ERC 2-1",
10:"VEL-TIG 3-2,UNI-IND 1-2,PLA-NOB 0-1,RAC-SAR 3-1,GLP-BAN 2-2,ROS-ARG 1-0,SLO-BOC 0-2,BAR-IRI 0-1,ALD-ATU 1-0,GEM-DRI 0-0,CCO-DYJ 2-2,INS-TAL 3-1,BEL-ERC 2-1,RIV-HUR 1-2,LAN-EST 2-1"};
const PAST=[];Object.keys(PAST_RAW).forEach(f=>PAST_RAW[f].split(",").forEach(x=>{const[p,sc]=x.split(" "),[h,a]=p.split("-");PAST.push([+f,h,a,zi(h)!==zi(a),sc.split("-").map(Number)])}));
// Dia y hora de los partidos (ligaprofesional.ar y medios, al 11/10/2026). Solo se usa la hora de los pendientes.
const SCH={"IND-INS":["Vie 02/10"],"IRI-GLP":["Vie 02/10"],"BOC-UNI":["Vie 02/10"],"DYJ-SLO":["Sáb 03/10"],"ATU-BAR":["Sáb 03/10"],"NOB-LAN":["Sáb 03/10"],"HUR-ALD":["Dom 04/10"],"TAL-BEL":["Dom 04/10"],"ARG-TIG":["Dom 04/10"],"ERC-RAC":["Dom 04/10"],"DRI-CCO":["Lun 05/10"],"VEL-PLA":["Lun 05/10"],"EST-GEM":["Lun 05/10"],"BAN-ROS":["Lun 05/10"],"SAR-RIV":["Mié 14/10","19:00"],
"ALD-SAR":["Vie 09/10"],"GLP-ATU":["Vie 09/10","18:00"],"INS-BOC":["Vie 09/10","19:30"],"UNI-DYJ":["Vie 09/10","21:45"],
"BAR-HUR":["Sáb 10/10","15:45"],"CCO-EST":["Sáb 10/10","17:00"],"TIG-BAN":["Sáb 10/10","19:15"],"RIV-ERC":["Sáb 10/10","21:30"],
"SLO-DRI":["Dom 11/10","14:45"],"PLA-ARG":["Dom 11/10","17:00"],"ROS-IRI":["Dom 11/10","17:00"],"RAC-BEL":["Dom 11/10","19:15"],"TAL-IND":["Dom 11/10","21:30"],
"LAN-VEL":["Lun 12/10","16:00"],"GEM-NOB":["Lun 12/10","18:30"]};
const POSTP={"SAR-RIV":1}; // postergado: no cuenta para elegir la "proxima fecha"
const tk=m=>{const t=(SCH[pk(m)]||[])[1];return t&&t.includes(':')?+t.slice(0,2)*60+ +t.slice(3,5):-1},pk=m=>m[1]+"-"+m[2],dnum=l=>{const[d,m]=l.split(' ')[1].split('/');return +m*100+ +d};
const pend=i=>(SCH[pk(FX[i])]||[])[1]||"Pend.";
// Lo que simulas se guarda en el navegador (solo partidos sin resultado oficial)
const LSK='simulador-clausura-2026-v1';
function save(){try{const o={};FX.forEach((m,i)=>{if(!m[4]&&part[i]&&(part[i].gh!==''||part[i].ga!==''))o[pk(m)]=[part[i].gh,part[i].ga]});if(Object.keys(o).length)localStorage.setItem(LSK,JSON.stringify(o));else localStorage.removeItem(LSK)}catch(e){}}
function load(){try{const o=JSON.parse(localStorage.getItem(LSK)||'{}');FX.forEach((m,i)=>{const v=o[pk(m)];if(!m[4]&&Array.isArray(v)){const g=[v[0],v[1]].map(x=>/^\d{1,2}$/.test(x)?String(Math.min(15,+x)):'');part[i]={gh:g[0],ga:g[1]};res[i]=(g[0]===''||g[1]==='')?null:{gh:+g[0],ga:+g[1]}}})}catch(e){}}
load();
let ALLI=false;
let curF=(()=>{for(let f=11;f<=16;f++)if(FX.some(m=>m[0]===f&&!m[4]&&!POSTP[pk(m)]))return f;return 16})();
function setF(f){curF=Math.max(1,Math.min(16,f));fixture()}
function goF(d){setF(curF+d)}
function mrow(m,i){const lock=!!m[4],r=i<0?{gh:m[4][0],ga:m[4][1]}:(part[i]||{gh:'',ga:''}),fin=lock||res[i]!==null;
 const lab=k=>`Goles de ${T[k==='gh'?m[1]:m[2]].n}`,inp=k=>lock?`<input type="text" value="${r[k]}" readonly tabindex="-1" aria-label="${lab(k)}">`:`<input type="text" inputmode="numeric" pattern="[0-9]*" maxlength="2" autocomplete="off" value="${r[k]}" aria-label="${lab(k)}" oninput="sc(${i},'${k}',this)">`;
 return `<div class="match${m[3]&&!ALLI?' inter':''}"><div class="st${fin?' fin':''}"${i>=0?` id="st${i}"`:''}>${fin?'Final':pend(i)}</div><div class="side h">${bdg(m[1])}<span class="t">${T[m[1]].n}</span></div>${inp('gh')}<div class="vs">-</div>${inp('ga')}<div class="side">${bdg(m[2])}<span class="t">${T[m[2]].n}</span></div></div>`}
function fixture(){
 const list=curF<=10?PAST.filter(m=>m[0]===curF).map(m=>[m,-1]):FX.map((m,i)=>[m,i]).filter(x=>x[0][0]===curF);
 ALLI=list.every(([m])=>m[3]);
 let h=`<div class="panel"><div class="ph">Fecha ${curF}</div>`+(ALLI?'<div class="dh">Fecha interzonal: todos los partidos son entre equipos de distintas zonas</div>':'');
 const days=[...new Set(list.map(([m])=>(SCH[pk(m)]||[])[0]).filter(Boolean))].sort((x,y)=>dnum(x)-dnum(y));
 if(days.length){days.forEach(d=>{h+=`<div class="dh">${d}</div>`+list.filter(([m])=>(SCH[pk(m)]||[])[0]===d).sort(([x],[y])=>tk(x)-tk(y)).map(([m,i])=>mrow(m,i)).join('')});h+=list.filter(([m])=>!SCH[pk(m)]).map(([m,i])=>mrow(m,i)).join('')}
 else h+=list.map(([m,i])=>mrow(m,i)).join('');
 document.getElementById('fixtureList').innerHTML=h+'</div>';
 document.getElementById('fSel').value=curF;document.getElementById('fPrev').disabled=curF<=1;document.getElementById('fNext').disabled=curF>=16}
function sc(i,k,el){let v=el.value.replace(/\D/g,'').slice(0,2);if(v!==''&&+v>15)v='15';if(el.value!==v)el.value=v;const c=part[i]||(part[i]={gh:'',ga:''});c[k]=v;save();res[i]=(c.gh===''||c.ga==='')?null:{gh:+c.gh,ga:+c.ga};
 const s=document.getElementById('st'+i);s.textContent=res[i]?'Final':pend(i);s.classList.toggle('fin',!!res[i]);tables()}
// Probabilidades: simulaciones con goles de Poisson y fuerza de ataque/defensa por equipo
const NS=10000,NF=2500,KEYS=['ca','po','lib','sud','da','dp'],CL={ca:'242,194,0',po:'76,175,80',lib:'242,194,0',sud:'90,178,230',da:'215,25,32',dp:'215,25,32'};let simTimer=null,LAST=null,NEEDC={};const BI=ALL.findIndex(t=>t.c==='BEL');
const pois=l=>{const L=Math.exp(-l);let k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1};
const pmf=(x,l)=>{let p=Math.exp(-l);for(let i=1;i<=x;i++)p*=l/i;return p};
const pwin=(lt,lo)=>{let s=0;for(let a=1;a<=12;a++)for(let b=0;b<a;b++)s+=pmf(a,lt)*pmf(b,lo);return s};
// ===== Elo (en prueba) =====
// K = cuanto se mueve el puntaje por partido; HFA = ventaja de local.
// EXT y BR = puesto de la tabla Elo (de los 30 equipos actuales) que se usa como rival fijo: extranjero (no brasileño) = puesto 22, brasileño = puesto 3.
// LOW = division inferior: el ultimo de la tabla menos LOWGAP (ganar suma lo minimo, perder resta lo maximo).
const EL={K:20,HFA:70,EXT:22,BR:3,LOWGAP:150};
// Fase de grupos de la liga 2025 (Apertura y Clausura) y Apertura 2026, mas la fase de grupos de Libertadores y Sudamericana 2025 y 2026 de los equipos argentinos, en orden cronologico: "local-visitante golesLocal-golesVisitante".
// Para sumar mas partidos (playoffs, Copa Argentina, copas internacionales) se agregan aca: codigo de equipo, o EXT (extranjero no brasileño), BR (brasileño), LOW (division inferior). Sin amistosos.
const ELO_EXTRA="TIG-VEL 3-0,GOD-ROS 0-3,NOB-IRI 0-1,DYJ-BAN 0-1,LAN-DRI 0-2,BAR-RAC 1-3,IND-SAR 2-1,BEL-HUR 1-1,SMA-ATU 0-1,SLO-TAL 1-0,EST-UNI 3-1,INS-GLP 3-0,PLA-RIV 1-1,BOC-ARG 0-0,CCO-ALD 1-0,BAN-NOB 3-0,DRI-SMA 0-0,ROS-LAN 2-1,SAR-GOD 0-0,IRI-BAR 0-0,VEL-PLA 0-1,TAL-IND 2-3,GLP-SLO 0-2,HUR-EST 0-0,UNI-BOC 1-1,RIV-INS 1-0,ALD-DYJ 0-5,RAC-BEL 4-0,ARG-TIG 1-0,CCO-ATU 2-0,BAR-BAN 1-0,SMA-ROS 0-0,LAN-SAR 2-0,SLO-RIV 0-0,BOC-HUR 2-1,NOB-ALD 1-0,INS-VEL 2-0,IND-GLP 2-0,DYJ-CCO 2-1,TIG-UNI 1-0,EST-RAC 2-0,BEL-IRI 0-3,ARG-PLA 1-0,ATU-DRI 0-3,ALD-BAR 1-3,SAR-SMA 1-1,BAN-BEL 1-1,CCO-NOB 2-0,HUR-TIG 2-0,IRI-EST 2-2,UNI-ARG 0-1,VEL-SLO 0-0,ROS-ATU 3-1,RIV-IND 2-0,RAC-BOC 2-0,PLA-INS 1-0,DRI-DYJ 1-1,GLP-GOD 3-0,TAL-LAN 0-1,BAR-CCO 3-3,BOC-IRI 2-0,EST-BAN 1-0,TIG-RAC 1-0,BEL-ALD 2-0,DRI-ROS 0-0,NOB-DYJ 0-1,ARG-HUR 1-1,IND-VEL 3-0,GOD-RIV 0-0,LAN-GLP 0-0,SLO-PLA 2-1,SMA-TAL 0-1,ATU-SAR 5-0,UNI-INS 0-0,BAN-BOC 0-1,DYJ-BAR 1-1,ALD-EST 2-2,CCO-BEL 4-0,IRI-TIG 1-4,RAC-ARG 2-3,NOB-ROS 1-2,RIV-LAN 1-0,HUR-UNI 1-0,TAL-ATU 1-1,SAR-DRI 2-1,GLP-SMA 1-0,PLA-IND 1-1,VEL-GOD 0-2,INS-SLO 0-1,DRI-TAL 0-0,EST-CCO 3-2,GOD-PLA 1-1,LAN-VEL 0-0,IND-INS 2-0,BOC-ALD 2-1,SMA-RIV 0-2,ROS-SAR 1-0,HUR-SLO 2-0,BEL-DYJ 2-0,ATU-GLP 0-1,BAR-NOB 2-0,ARG-IRI 0-0,TIG-BAN 1-0,BOC-ROS 1-0,CCO-DRI 0-0,SMA-BEL 3-1,ALD-SAR 2-2,RIV-EST 0-2,UNI-GLP 1-0,TAL-TIG 1-2,IRI-LAN 1-1,ARG-INS 2-0,VEL-HUR 0-2,BAR-GOD 1-2,SLO-RAC 3-2,ATU-NOB 1-2,BAN-IND 0-0,PLA-DYJ 0-1,BAN-ARG 1-2,VEL-SMA 1-0,CCO-BOC 0-3,SLO-IND 1-2,RAC-HUR 0-1,PLA-LAN 0-0,SAR-BAR 1-1,DYJ-EST 1-0,ALD-TIG 0-2,RIV-ATU 1-0,NOB-BEL 0-0,INS-GOD 1-1,GLP-DRI 1-1,IRI-UNI 2-0,TAL-ROS 0-0,ARG-ALD 0-2,GOD-SLO 0-0,DRI-RIV 0-0,EST-NOB 1-1,ROS-GLP 2-1,HUR-IRI 2-0,SAR-TAL 0-0,IND-RAC 1-1,BOC-DYJ 4-0,BEL-BAR 1-1,LAN-INS 4-1,UNI-BAN 3-1,TIG-CCO 1-2,SMA-PLA 0-2,ATU-VEL 1-2,UNI-RAC 0-1,GOD-TAL 0-0,ALD-UNI 2-1,BAR-EST 2-1,IRI-RAC 2-1,DYJ-TIG 1-2,BAN-HUR 0-0,SLO-LAN 1-1,VEL-DRI 0-1,PLA-ATU 2-1,INS-SMA 1-0,CCO-ARG 1-1,IND-GOD 4-0,RIV-ROS 2-2,BEL-TAL 1-1,GLP-SAR 0-0,NOB-BOC 2-0,EXT-EST 0-2,EXT-RIV 0-1,CCO-EXT 0-0,TAL-BR 0-1,BR-RAC 0-3,VEL-EXT 2-1,EXT-IND 2-0,EXT-DYJ 0-0,BR-HUR 1-2,EXT-GOD 0-2,UNI-BR 1-0,EXT-LAN 2-2,EST-BEL 0-1,SMA-SLO 0-1,ROS-VEL 2-1,GOD-IRI 1-1,HUR-ALD 3-3,TAL-GLP 2-0,SAR-RIV 1-1,UNI-CCO 1-0,LAN-IND 1-1,BOC-BAR 1-0,RAC-BAN 4-1,ARG-DYJ 4-1,DRI-PLA 1-0,TIG-NOB 0-2,ATU-INS 3-2,EST-EXT 1-2,RIV-EXT 0-0,BR-CCO 1-2,EXT-TAL 2-0,RAC-EXT 1-2,EXT-VEL 0-4,IND-EXT 2-1,DYJ-BR 0-0,HUR-EXT 5-0,GOD-EXT 2-0,EXT-UNI 2-0,LAN-EXT 3-0,BAN-IRI 1-1,NOB-ARG 0-0,SLO-ATU 1-0,BAR-TIG 1-0,BEL-BOC 1-3,INS-DRI 3-0,GLP-EST 1-1,IND-SMA 2-0,RIV-TAL 1-1,ALD-RAC 0-2,CCO-HUR 1-2,DYJ-UNI 0-0,VEL-SAR 0-1,GOD-LAN 0-0,PLA-ROS 0-0,GLP-RIV 0-3,RAC-CCO 1-0,TAL-VEL 0-1,UNI-NOB 1-1,LAN-BAN 1-1,HUR-DYJ 1-1,BOC-EST 2-0,DRI-SLO 0-0,SMA-GOD 1-0,SAR-PLA 0-1,ROS-INS 3-0,ARG-BAR 3-0,TIG-BEL 0-0,IRI-ALD 1-0,EST-BR 1-0,EXT-RIV 2-2,CCO-EXT 2-1,EXT-TAL 3-2,EXT-RAC 1-1,EXT-VEL 2-1,EXT-IND 2-1,EXT-DYJ 3-1,HUR-EXT 0-0,GOD-BR 2-2,EXT-UNI 3-0,BR-LAN 0-0,ALD-BAN 2-1,SLO-ROS 0-1,BEL-ARG 1-1,RIV-BOC 2-1,INS-SAR 1-1,LAN-SMA 1-0,IND-DRI 0-0,BAR-UNI 2-1,GOD-ATU 1-0,EST-TIG 0-0,DYJ-RAC 1-2,CCO-IRI 1-2,VEL-GLP 1-0,NOB-HUR 2-0,PLA-TAL 2-1,ATU-IND 2-0,BAN-CCO 3-1,IRI-DYJ 3-2,RAC-NOB 1-0,ARG-EST 4-0,UNI-BEL 1-1,DRI-GOD 3-0,SAR-SLO 1-1,TAL-INS 1-2,ROS-IND 1-0,HUR-BAR 0-1,ATU-LAN 1-0,GLP-PLA 1-0,SMA-ALD 0-3,TIG-BOC 1-1,RIV-VEL 4-1,EXT-EST 0-3,EXT-RIV 2-3,CCO-BR 1-1,TAL-EXT 0-0,EXT-RAC 0-4,VEL-EXT 1-1,EXT-IND 1-5,BR-DYJ 1-1,EXT-HUR 1-3,EXT-GOD 0-1,UNI-EXT 1-2,EXT-LAN 0-1,BR-EST 3-2,RIV-EXT 6-2,EXT-CCO 1-2,TAL-EXT 2-0,RAC-EXT 4-0,VEL-EXT 3-0,IND-EXT 1-0,DYJ-EXT 1-1,EXT-HUR 0-0,BR-GOD 1-1,UNI-EXT 0-1,LAN-BR 1-0,EST-EXT 2-0,RIV-EXT 1-1,EXT-CCO 3-0,BR-TAL 2-1,RAC-BR 1-0,EXT-VEL 0-0,IND-EXT 7-0,DYJ-EXT 1-2,HUR-BR 1-0,GOD-EXT 2-2,BR-UNI 0-0,LAN-EXT 2-2,ALD-CCO 0-0,ARG-BOC 0-0,BAN-DYJ 0-0,HUR-BEL 0-3,IRI-NOB 1-2,RAC-BAR 0-1,UNI-EST 1-0,ATU-SMA 2-1,DRI-LAN 1-0,GLP-INS 0-1,RIV-PLA 3-1,ROS-GOD 1-1,SAR-IND 2-2,TAL-SLO 1-2,VEL-TIG 2-1,BAR-IRI 0-3,BEL-RAC 0-1,BOC-UNI 1-1,DYJ-ALD 2-0,EST-HUR 2-1,NOB-BAN 1-2,TIG-ARG 2-1,GOD-SAR 0-0,IND-TAL 1-2,INS-RIV 0-4,LAN-ROS 0-1,PLA-VEL 0-0,SLO-GLP 0-0,SMA-DRI 3-2,ATU-CCO 1-1,ALD-NOB 0-0,BAN-BAR 1-3,CCO-DYJ 2-1,HUR-BOC 1-0,IRI-BEL 0-0,RAC-EST 0-1,UNI-TIG 0-0,DRI-ATU 1-0,GLP-IND 1-0,RIV-SLO 0-0,ROS-SMA 0-0,SAR-LAN 0-2,TAL-GOD 0-0,VEL-INS 0-0,PLA-ARG 0-0,ARG-UNI 1-0,BAR-ALD 3-1,BEL-BAN 2-1,BOC-RAC 1-1,EST-IRI 2-1,NOB-CCO 1-1,TIG-HUR 0-1,ATU-ROS 0-0,GOD-GLP 1-2,IND-RIV 0-0,INS-PLA 1-1,LAN-TAL 1-0,SLO-VEL 1-0,SMA-SAR 0-1,DYJ-DRI 1-0,ALD-BEL 0-0,BAN-EST 3-2,CCO-BAR 1-1,DYJ-NOB 1-1,HUR-ARG 1-0,IRI-BOC 0-3,RAC-TIG 1-2,GLP-LAN 1-2,PLA-SLO 2-1,RIV-GOD 4-2,ROS-DRI 1-1,SAR-ATU 2-2,TAL-SMA 0-0,VEL-IND 2-1,INS-UNI 0-4,ARG-RAC 4-1,BAR-DYJ 1-1,BEL-CCO 0-3,BOC-BAN 2-0,EST-ALD 1-0,TIG-IRI 1-1,UNI-HUR 1-1,ATU-TAL 3-0,DRI-SAR 3-0,GOD-VEL 0-2,IND-PLA 3-0,LAN-RIV 1-1,SLO-INS 1-0,SMA-GLP 1-0,ROS-NOB 1-0,ALD-BOC 0-2,BAN-TIG 1-0,CCO-EST 2-0,DYJ-BEL 2-1,IRI-ARG 2-1,NOB-BAR 1-2,RAC-UNI 2-3,GLP-ATU 1-0,INS-IND 0-0,PLA-GOD 1-3,RIV-SMA 2-0,SAR-ROS 0-1,TAL-DRI 0-1,VEL-LAN 3-0,SLO-HUR 0-0,BEL-SMA 0-0,DRI-CCO 2-0,HUR-VEL 0-0,RAC-SLO 2-0,LAN-IRI 1-0,NOB-ATU 2-0,GOD-BAR 0-0,IND-BAN 0-1,EST-RIV 1-2,SAR-ALD 2-0,GLP-UNI 1-3,INS-ARG 2-0,ROS-BOC 1-1,DYJ-PLA 1-2,TIG-TAL 0-0,ARG-BAN 3-0,BEL-NOB 3-0,BOC-CCO 2-2,EST-DYJ 1-0,HUR-RAC 0-2,TIG-ALD 2-0,UNI-IRI 2-2,ATU-RIV 2-0,DRI-GLP 1-0,GOD-INS 1-1,IND-SLO 1-1,LAN-PLA 2-1,ROS-TAL 1-1,SMA-VEL 1-2,BAR-SAR 0-1,ALD-ARG 0-2,BAN-UNI 0-0,BAR-BEL 1-1,CCO-TIG 0-1,DYJ-BOC 2-1,IRI-HUR 0-0,NOB-EST 1-1,GLP-ROS 0-3,INS-LAN 0-0,PLA-SMA 2-2,RIV-DRI 1-2,SLO-GOD 2-0,TAL-SAR 1-0,VEL-ATU 3-1,RAC-IND 0-0,ARG-CCO 0-0,BOC-NOB 5-0,EST-BAR 1-1,HUR-BAN 1-0,RAC-IRI 0-0,TIG-DYJ 1-1,UNI-ALD 0-2,ATU-PLA 2-0,DRI-VEL 2-2,GOD-IND 1-1,LAN-SLO 2-1,ROS-RIV 2-1,SMA-INS 0-0,SAR-GLP 0-1,TAL-BEL 0-0,ALD-HUR 2-0,BAN-RAC 1-3,BAR-BOC 1-3,BEL-EST 1-1,CCO-UNI 3-1,DYJ-ARG 1-0,NOB-TIG 1-1,GLP-TAL 1-2,IND-LAN 0-2,INS-ATU 2-0,PLA-DRI 1-1,RIV-SAR 0-1,SLO-SMA 0-1,VEL-ROS 1-2,IRI-GOD 0-0,ARG-NOB 3-1,BOC-BEL 1-2,HUR-CCO 0-1,IRI-BAN 1-2,RAC-ALD 1-0,TIG-BAR 2-2,UNI-DYJ 3-0,ATU-SLO 1-2,DRI-INS 1-0,LAN-GOD 2-0,ROS-PLA 1-0,SMA-IND 1-0,SAR-VEL 0-2,TAL-RIV 0-2,EST-GLP 2-0,ALD-IRI 3-1,BAR-ARG 2-0,BEL-TIG 0-0,CCO-RAC 0-0,DYJ-HUR 1-3,EST-BOC 1-2,NOB-UNI 0-1,GOD-SMA 0-0,IND-ATU 3-0,INS-ROS 1-3,PLA-SAR 1-1,RIV-GLP 0-1,SLO-DRI 1-0,VEL-TAL 0-1,BAN-LAN 2-1,ARG-BEL 1-0,BAN-ALD 0-1,HUR-NOB 0-2,IRI-CCO 0-0,RAC-DYJ 1-0,TIG-EST 1-0,UNI-BAR 0-0,ATU-GOD 2-1,DRI-IND 0-1,GLP-VEL 2-0,ROS-SLO 0-0,SMA-LAN 1-1,SAR-INS 2-1,TAL-PLA 1-0,BOC-RIV 2-0,BAR-HUR 1-1,BEL-UNI 0-0,BOC-TIG 2-0,CCO-BAN 1-1,DYJ-IRI 0-2,EST-ARG 1-2,NOB-RAC 0-1,GOD-DRI 1-1,IND-ROS 1-0,INS-TAL 0-0,LAN-ATU 3-1,PLA-GLP 0-3,SLO-SAR 1-1,VEL-RIV 0-0,ALD-SMA 4-2,BOC-DRI 1-0,CCO-GEM 0-1,IND-EST 1-1,INS-VEL 0-1,SLO-LAN 2-3,TAL-NOB 2-1,UNI-PLA 0-0,ARG-SAR 1-0,BAN-HUR 1-1,BAR-RIV 0-1,GLP-RAC 2-1,IRI-ATU 2-1,ROS-BEL 1-2,TIG-ERC 2-0,ALD-DYJ 0-0,DRI-DYJ 0-1,EST-BOC 2-1,GEM-SLO 0-1,LAN-UNI 2-1,NOB-IND 1-1,PLA-INS 2-1,VEL-TAL 2-1,ALD-BAR 0-0,BEL-TIG 1-1,ERC-ARG 0-0,HUR-IRI 1-2,RAC-ROS 1-2,RIV-GLP 2-0,SAR-BAN 1-0,ATU-CCO 0-0,BOC-NOB 2-0,DYJ-EST 0-0,IND-VEL 1-1,INS-LAN 2-2,SLO-CCO 1-0,TAL-PLA 1-2,UNI-GEM 4-0,ARG-BEL 0-0,ATU-HUR 1-1,BAN-ERC 2-1,GLP-ALD 3-1,IRI-SAR 2-1,ROS-RIV 0-0,TIG-RAC 3-1,BAR-DRI 1-1,CCO-UNI 1-0,EST-DRI 1-0,GEM-INS 1-0,LAN-TAL 1-1,NOB-DYJ 2-3,PLA-IND 0-1,VEL-BOC 2-1,ALD-ROS 1-1,BAR-GLP 2-0,BEL-BAN 1-0,ERC-IRI 0-1,RAC-ARG 2-1,RIV-TIG 1-4,SAR-ATU 2-1,HUR-SLO 1-0,BOC-PLA 0-0,DYJ-VEL 1-1,DRI-NOB 1-1,IND-LAN 2-0,INS-CCO 2-0,TAL-GEM 2-1,UNI-SLO 0-0,ARG-RIV 1-0,ATU-ERC 4-0,BAN-RAC 0-2,HUR-SAR 1-0,IRI-BEL 0-1,ROS-BAR 2-0,TIG-ALD 1-0,GLP-EST 0-0,DYJ-BEL 1-1,EST-SAR 1-0,BOC-RAC 0-0,INS-ATU 2-1,GEM-GLP 0-1,ROS-TAL 0-1,IRI-IND 3-2,PLA-BAR 1-0,BAN-NOB 3-0,DRI-HUR 0-0,CCO-TIG 0-0,SLO-ERC 2-0,VEL-RIV 1-0,UNI-ALD 1-0,ARG-LAN 2-1,CCO-TAL 2-0,GEM-IND 1-1,LAN-BOC 0-3,NOB-EST 0-2,PLA-DYJ 0-0,SLO-INS 1-1,VEL-DRI 0-0,ALD-ARG 0-2,BAR-TIG 2-1,BEL-ATU 3-1,ERC-HUR 2-0,GLP-ROS 1-2,RAC-IRI 1-1,RIV-BAN 3-1,SAR-UNI 1-3,BOC-GEM 1-1,DYJ-LAN 1-1,DRI-PLA 0-0,EST-VEL 0-1,IND-CCO 2-0,INS-UNI 1-2,TAL-SLO 0-0,ARG-BAR 1-1,ATU-RAC 0-3,BAN-ALD 2-0,HUR-BEL 3-1,IRI-RIV 1-1,SAR-ERC 1-0,TIG-GLP 2-2,NOB-ROS 0-2,BOC-SLO 1-1,DYJ-CCO 1-1,DRI-GEM 0-0,EST-LAN 0-1,IND-UNI 4-4,NOB-PLA 1-1,TAL-INS 2-0,ARG-ROS 0-0,ATU-ALD 1-1,BAN-GLP 1-2,ERC-BEL 0-1,HUR-RIV 1-2,IRI-BAR 1-2,SAR-RAC 0-0,TIG-VEL 1-1,CCO-DRI 1-0,GEM-EST 1-2,INS-IND 2-1,LAN-NOB 5-0,PLA-VEL 0-2,SLO-DYJ 2-5,UNI-BOC 1-1,ALD-HUR 0-0,BAR-ATU 2-1,GLP-IRI 2-3,RAC-ERC 2-0,RIV-SAR 2-0,ROS-BAN 2-1,TIG-ARG 1-1,BEL-TAL 0-0,BOC-INS 2-0,DYJ-UNI 2-0,DRI-SLO 1-1,EST-CCO 5-0,IND-TAL 1-2,NOB-GEM 1-0,VEL-LAN 0-1,ATU-GLP 1-0,BAN-TIG 1-0,BEL-RAC 1-2,ERC-RIV 0-2,HUR-BAR 0-0,IRI-ROS 2-0,SAR-ALD 2-0,ARG-PLA 1-0,CCO-NOB 1-3,GEM-VEL 3-2,INS-DYJ 2-0,LAN-PLA 0-0,SLO-EST 1-0,TAL-BOC 0-1,UNI-DRI 2-0,ALD-ERC 0-0,ARG-BAN 3-2,BAR-SAR 1-2,GLP-HUR 0-3,RIV-BEL 3-0,ROS-ATU 2-1,TIG-IRI 0-2,IND-RAC 1-0,BOC-IND 1-1,DYJ-TAL 1-2,DRI-INS 0-1,EST-UNI 2-1,NOB-SLO 0-0,PLA-GEM 1-1,VEL-CCO 1-0,ATU-TIG 0-0,BEL-ALD 1-0,ERC-BAR 1-2,HUR-ROS 3-1,IRI-ARG 3-1,RAC-RIV 0-2,SAR-GLP 1-2,LAN-BAN 1-0,CCO-PLA 4-3,GEM-LAN 1-0,IND-DYJ 3-1,INS-EST 0-1,SLO-VEL 0-0,TAL-DRI 2-0,UNI-NOB 2-3,ALD-RAC 1-1,ARG-ATU 1-0,BAN-IRI 0-0,BAR-BEL 0-0,GLP-ERC 1-0,ROS-SAR 2-1,TIG-HUR 1-1,RIV-BOC 0-1,DYJ-BOC 0-4,DRI-IND 2-0,EST-TAL 0-0,LAN-CCO 0-0,NOB-INS 1-1,PLA-SLO 0-1,VEL-UNI 2-2,ATU-BAN 1-1,BEL-GLP 0-1,ERC-ROS 1-2,HUR-ARG 1-2,RAC-BAR 1-1,RIV-ALD 3-1,SAR-TIG 1-0,IRI-GEM 5-1,EXT-EST 1-1,IRI-EXT 1-0,EXT-BOC 1-2,PLA-BR 0-2,BR-LAN 1-0,ROS-EXT 0-0,EXT-TIG 1-1,EXT-SLO 1-1,EXT-RAC 1-3,DRI-EXT 0-0,BAR-BR 0-0,EXT-RIV 1-1,EST-EXT 2-1,BR-IRI 1-2,BOC-EXT 3-0,EXT-PLA 1-2,LAN-EXT 1-0,EXT-ROS 0-1,TIG-EXT 0-1,SLO-EXT 2-0,RAC-BR 2-3,BR-DRI 1-0,EXT-BAR 0-0,RIV-EXT 1-0,EST-BR 1-1,IRI-EXT 4-1,BR-BOC 1-0,PLA-EXT 2-1,LAN-EXT 1-0,EXT-ROS 0-3,TIG-EXT 2-0,SLO-BR 1-1,EXT-RAC 1-1,DRI-EXT 2-1,BAR-EXT 1-1,BR-RIV 0-1,CCO-BOC 1-2,GEM-DYJ 2-1,LAN-DRI 0-0,PLA-EST 0-2,SLO-IND 1-2,UNI-TAL 1-1,VEL-NOB 1-1,ALD-IRI 1-1,BAR-BAN 1-2,BEL-SAR 4-0,GLP-ARG 2-0,RAC-HUR 0-0,RIV-ATU 0-1,ROS-TIG 1-1,ERC-INS 0-2,EXT-EST 1-1,IRI-BR 1-1,EXT-BOC 1-0,PLA-EXT 1-1,EXT-LAN 4-0,ROS-EXT 1-0,EXT-TIG 2-2,EXT-SLO 0-0,BR-RAC 2-1,DRI-BR 0-3,BAR-EXT 1-2,EXT-RIV 1-2,BR-EST 1-0,EXT-IRI 2-4,BOC-BR 1-1,EXT-PLA 2-1,EXT-LAN 2-0,ROS-EXT 4-0,EXT-TIG 1-1,BR-SLO 2-2,RAC-EXT 2-2,EXT-DRI 4-1,EXT-BAR 2-0,RIV-BR 1-1,EST-EXT 1-0,EXT-IRI 1-3,BOC-EXT 0-1,BR-PLA 0-2,LAN-BR 1-0,EXT-ROS 1-0,TIG-EXT 2-0,SLO-EXT 0-1,RAC-EXT 2-0,EXT-DRI 1-1,BR-BAR 3-0,RIV-EXT 3-0".split(',').map(x=>{const[p,sc]=x.split(' '),[h,a]=p.split('-'),[g,k]=sc.split('-');return[h,a,+g,+k]});
const CUR=new Set(ALL.map(t=>t.c));
let MODEL='goles';
function eloRun(upto){
 const R={},ref=k=>{const v=Object.keys(R).filter(c=>CUR.has(c)).map(c=>R[c]).sort((x,y)=>y-x);if(v.length<8)return 1500;return k==='BR'?v[Math.min(EL.BR,v.length)-1]:k==='EXT'?v[Math.min(EL.EXT,v.length)-1]:v[v.length-1]-EL.LOWGAP};
 const upd=(h,a,gh,ga)=>{for(const c of[h,a])if(!(c in R)&&c!=='EXT'&&c!=='BR'&&c!=='LOW')R[c]=ref('EXT');
  const rh=h in R?R[h]:ref(h),ra=a in R?R[a]:ref(a),e=1/(1+Math.pow(10,-(rh+EL.HFA-ra)/400)),sc=gh>ga?1:gh===ga?.5:0,d=Math.abs(gh-ga),g=d<=1?1:d===2?1.5:(11+d)/8,dl=EL.K*g*(sc-e);
  if(h in R)R[h]+=dl;if(a in R)R[a]-=dl};
 ELO_EXTRA.forEach(m=>upd(m[0],m[1],m[2],m[3]));
 const base=Object.assign({},R);
 PAST.map(m=>[m[0],m[1],m[2],m[4][0],m[4][1]]).concat(FX.map((m,i)=>res[i]?[m[0],m[1],m[2],res[i].gh,res[i].ga]:null).filter(Boolean)).filter(m=>upto===undefined||m[0]<upto).sort((x,y)=>x[0]-y[0]).forEach(m=>upd(m[1],m[2],m[3],m[4]));
 return{R,seed:base,ref:{EXT:ref('EXT'),BR:ref('BR'),LOW:ref('LOW')}}}
const pdraw=(a,b)=>{let t=0;for(let k=0;k<=12;k++)t+=pmf(k,a)*pmf(k,b);return t};
// Convierte la diferencia de Elo en goles esperados de cada equipo (mantiene la probabilidad de ganar/empatar del Elo)
function lamElo(dR,mu){const E=1/(1+Math.pow(10,-dR/400));let lo=-3,hi=3;
 for(let i=0;i<28;i++){const x=(lo+hi)/2,lh=Math.max(.15,(mu+x)/2),la=Math.max(.15,(mu-x)/2);if(pwin(lh,la)+.5*pdraw(lh,la)<E)lo=x;else hi=x}
 const x=(lo+hi)/2;return[Math.max(.15,(mu+x)/2),Math.max(.15,(mu-x)/2)]}
function setModel(v){MODEL=v;NEEDC={};probs()}
function eloPanel(){const x=eloRun(),r=ALL.slice().sort((a,b)=>x.R[b.c]-x.R[a.c]);
 let h='<table><tr><th>#</th><th style="text-align:left">Equipo</th><th>Elo</th><th>Cambio</th></tr>';
 r.forEach((t,i)=>{const d=Math.round(x.R[t.c]-x.seed[t.c]);h+=`<tr><td>${i+1}</td><td class="eq">${nm(t)}</td><td><b>${Math.round(x.R[t.c])}</b></td><td>${d>=0?'+':''}${d}</td></tr>`});
 document.getElementById('ELO').innerHTML=panel('Ranking Elo (en prueba)',h+'</table>',`<span style="flex-basis:100%">Elo con K=${EL.K}, ventaja de local +${EL.HFA} y más puntos por goleada, calculado con ${ELO_EXTRA.length} partidos: fase de grupos de la liga 2025 (Apertura y Clausura) y del Apertura 2026, y fase de grupos de Libertadores y Sudamericana 2025 y 2026, más los del Clausura 2026. Todavía no incluye playoffs de la liga, Copa Argentina, eliminatorias de las copas internacionales ni Recopa. "Cambio" = diferencia con el Elo antes del Clausura 2026. Rivales fijos: extranjero ${Math.round(x.ref.EXT)}, brasileño ${Math.round(x.ref.BR)}, división inferior ${Math.round(x.ref.LOW)}.</span>`)}
function setup(){const P=ALL.map(t=>proj(t));let G=0,N=0;ALL.forEach((t,i)=>{G+=t.apGF+P[i].GF;N+=16+P[i].PJ});const avg=G/N,K=12,S={},ix={},rem=[],E=MODEL==='elo'?eloRun().R:null;
 ALL.forEach((t,i)=>{ix[t.c]=i;const n=16+P[i].PJ+K;S[t.c]={a:(t.apGF+P[i].GF+K*avg)/n/avg,d:(t.apGC+P[i].GC+K*avg)/n/avg}});
 FX.forEach((m,i)=>{if(!res[i]){const[lh,la]=E?lamElo(E[m[1]]+EL.HFA-E[m[2]],2*avg):[avg*1.1*S[m[1]].a*S[m[2]].d,avg*.9*S[m[2]].a*S[m[1]].d];rem.push([ix[m[1]],ix[m[2]],lh,la])}});return rem}
const tp=(r,t)=>r[0]===t?pwin(r[2],r[3]):pwin(r[3],r[2]);
function winDist(t){let d=[1];setup().forEach(r=>{if(r[0]!==t&&r[1]!==t)return;const p=tp(r,t),n=new Array(d.length+1).fill(0);d.forEach((v,w)=>{n[w]+=v*(1-p);n[w+1]+=v*p});d=n});return d}
// M simulaciones del resto del torneo. Con team y k, el equipo gana exactamente k de sus partidos pendientes.
function simulate(M,team,k){
 const rem=setup(),B=ALL.map(t=>proj(t)),o={};KEYS.forEach(q=>o[q]=new Array(30).fill(0));
 const tm=[],subs=[];let force=null;
 if(team!==undefined){rem.forEach((r,j)=>{if(r[0]===team||r[1]===team)tm.push(j)});
  const pw=tm.map(j=>tp(rem[j],team));let tot=0;
  for(let m=0;m<(1<<tm.length);m++){let c=0,w=1;for(let b=0;b<tm.length;b++){if(m>>b&1){c++;w*=pw[b]}else w*=1-pw[b]}if(c===k){tot+=w;subs.push([m,tot])}}
  force=new Array(rem.length)}
 const i0=[...Array(15).keys()],i1=i0.map(i=>i+15),all0=[...Array(30).keys()];
 const AP=ALL.map(t=>t.apPts),AD=ALL.map(t=>t.apGF-t.apGC),H0=ALL.map(t=>t.h24+t.h25+t.apPts),J0=ALL.map(t=>t.pj+16);
 for(let s=0;s<M;s++){
  if(force){const u=Math.random()*subs[subs.length-1][1];let m=subs[subs.length-1][0];for(const x of subs){if(u<=x[1]){m=x[0];break}}tm.forEach((j,b)=>force[j]=(m>>b&1)?1:2)}
  const P=B.map(b=>b.Pts),F=B.map(b=>b.GF),C=B.map(b=>b.GC),J=B.map(b=>b.PJ);
  for(let j=0;j<rem.length;j++){const[h,a,lh,la]=rem[j],f=force&&force[j];let gh,ga,c=0;
   if(f){const th=h===team;do{gh=pois(lh);ga=pois(la);c++}while(c<400&&(f===1)!==(th?gh>ga:ga>gh))}else{gh=pois(lh);ga=pois(la)}
   F[h]+=gh;C[h]+=ga;F[a]+=ga;C[a]+=gh;J[h]++;J[a]++;
   if(gh>ga)P[h]+=3;else if(gh<ga)P[a]+=3;else{P[h]++;P[a]++}}
  [i0.slice(),i1.slice()].forEach(ids=>{ids.sort((x,y)=>P[y]-P[x]||(F[y]-C[y])-(F[x]-C[x])||F[y]-F[x]||Math.random()-.5);for(let q=0;q<8;q++)o.po[ids[q]]++});
  const an=all0.slice().sort((x,y)=>(AP[y]+P[y])-(AP[x]+P[x])||(AD[y]+F[y]-C[y])-(AD[x]+F[x]-C[x])||Math.random()-.5);
  o.ca[an[0]]++;o.lib[BI]++;let cq=0;for(const t of an){if(t===BI)continue;cq++;if(cq<=3)o.lib[t]++;else if(cq<=9)o.sud[t]++;else break}
  let w=0,wa=99;for(let i=0;i<30;i++){const v=(H0[i]+P[i])/(J0[i]+J[i]);if(v<wa){wa=v;w=i}}o.da[an[29]===w?an[28]:an[29]]++;o.dp[w]++}
 return o}
const pc=(x,c)=>`<td style="background:rgba(${c},${(x*.6).toFixed(2)})">${(x*100).toFixed(1)}%</td>`;
function probs(){const o=LAST=simulate(NS);NEEDC={};eloPanel();
 const r=ALL.map((t,i)=>i).sort((x,y)=>o.po[y]-o.po[x]||o.ca[y]-o.ca[x]);
 let h='<table><tr><th style="text-align:left">Equipo</th><th>Zona</th><th>Campeón anual</th><th>Playoffs</th><th>Libert.</th><th>Sudam.</th><th>Desc. anual</th><th>Desc. prom.</th></tr>';
 r.forEach(i=>h+=`<tr><td class="eq">${nm(ALL[i])}</td><td>${i<15?'A':'B'}</td>${KEYS.map(k=>pc(o[k][i]/NS,CL[k])).join('')}</tr>`);
 document.getElementById('PROB').innerHTML=panel('Probabilidades (modelo '+(MODEL==='elo'?'Elo':'Goles')+')',h+'</table>','<span style="flex-basis:100%">Resultado de 10.000 simulaciones de los partidos que no tienen resultado cargado. Campeón anual = 1° de la tabla anual (Campeón de Liga). Libert. = los 3 mejores de la anual sin contar a Belgrano (ya clasificado como campeón del Apertura, 100%) y Sudam. = los 6 siguientes. Todavía no se descuentan los campeones del Clausura y de la Copa Argentina, que liberarían su lugar si terminan arriba. Desc. prom. = peor promedio; Desc. anual = último de la anual sin contar al que baja por promedios (regla de la AFA). Los goles se simulan con distribución de Poisson, usando el ataque y la defensa de cada equipo en el Apertura y el Clausura, más ventaja de local. Es un modelo simple: no sabe de lesiones, refuerzos ni de los playoffs, por eso no calcula el % de campeón del Clausura.</span>');
 renderNeed()}
function renderNeed(){if(!LAST)return;const sel=document.getElementById('selEq'),i=+sel.value;
 if(NEEDC[i]){drawNeed(NEEDC[i]);return}
 document.getElementById('needOut').innerHTML='<div class="pad note">Calculando...</div>';
 setTimeout(()=>{if(+sel.value!==i)return;const d=winDist(i);
  NEEDC[i]=d.map((pe,k)=>{const o=d.length===1?LAST:simulate(NF,i,k),M=d.length===1?NS:NF;return{pe,v:KEYS.map(q=>o[q][i]/M)}});drawNeed(NEEDC[i])},30)}
function drawNeed(rows){const N=rows.length-1,a=rows.findIndex(r=>r.v[1]>=.5),b=rows.findIndex(r=>r.v[4]+r.v[5]<.1);
 const m1=N===0?'No le quedan partidos sin resultado.':a<0?'Ni ganando todos llega al 50% de clasificar a playoffs.':a===0?'Ya tiene 50% o más de clasificar a playoffs sin ganar ninguno.':`Para llegar al 50% de clasificar a playoffs necesita ganar ${a} de sus ${N} partidos.`;
 const m2=N===0?'':b<0?'Ni ganando todos baja del 10% de riesgo de descenso.':b===0?'Ya está por debajo del 10% de riesgo de descenso (anual y promedios).':`Para bajar del 10% de riesgo de descenso (anual y promedios) necesita ganar ${b} de ${N}.`;
 let h='<table><tr><th>Gana</th><th>Escenario</th><th>Campeón anual</th><th>Playoffs</th><th>Libert.</th><th>Sudam.</th><th>Desc. anual</th><th>Desc. prom.</th></tr>';
 rows.forEach((r,k)=>h+=`<tr><td><b>${k} de ${N}</b></td><td>${(r.pe*100).toFixed(1)}%</td>${KEYS.map((q,j)=>pc(r.v[j],CL[q])).join('')}</tr>`);
 document.getElementById('needOut').innerHTML=`<div class="pad note">${m1}<br>${m2}</div><div class="tblwrap">${h}</table></div><div class="legend"><span style="flex-basis:100%">Cada fila es lo que pasa si el equipo gana exactamente esa cantidad de sus partidos pendientes; el resto de los resultados se simula. "Escenario" = qué tan probable es ganar esa cantidad. No incluye el % de campeón del Clausura.</span></div>`}
function sched(){clearTimeout(simTimer);simTimer=setTimeout(probs,350)}
function resetAll(){try{localStorage.removeItem(LSK)}catch(e){}initRes();fixture();tables()}
function tables(){zone('A',TA,'Zona A');zone('B',TB,'Zona B');anual();prom();sched()}
document.getElementById('fSel').innerHTML=Array.from({length:16},(_,i)=>`<option value="${i+1}">Fecha ${i+1}</option>`).join('');
document.getElementById('selEq').innerHTML=ALL.map((t,i)=>`<option value="${i}">${t.n}</option>`).join('');
fixture();tables();
</script>
</body>
</html>

```

#### `datos/build.py`

Valida las fuentes de datos y regenera la lista ELO_EXTRA dentro del HTML (--write).

```python
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
if not(ok1 and ok2 and ok3 and not miss and not miss26 and not cbad):sys.exit('HAY DESAJUSTES: no se escribe nada')
D=dt.date;rows=[]
for h,a,gh,ga,m,d in ap25:rows.append((d,0,h,a,gh,ga))
for h,a,gh,ga in cl25:rows.append((D(2025,7,11)+dt.timedelta(days=7*(md25[(a,h)]-1)),1,h,a,gh,ga))
for h,a,gh,ga in ap26:
    r=rd[(a,h)];d=D(2026,5,2) if r==9 else D(2026,1,22)+dt.timedelta(days=4*(r-1));rows.append((d,2,h,a,gh,ga))
rows+=cr
rows.sort(key=lambda x:(x[0],x[1]))
s=','.join(f'{h}-{a} {gh}-{ga}' for d,_,h,a,gh,ga in rows)
print('ELO_EXTRA:',len(rows),'partidos |',len(s),'caracteres | desde',rows[0][0],'hasta',rows[-1][0])
cur_s=re.search(r'const ELO_EXTRA="([^"]*)"\.split',html).group(1)
print('coincide con lo que ya tiene el HTML:',cur_s==s)
if '--write' in sys.argv:
    html=html.replace('const ELO_EXTRA="'+cur_s+'".split','const ELO_EXTRA="'+s+'".split')
    HTML.write_text(html,encoding='utf-8');print('HTML actualizado')

```

#### `datos/mats.py`

Matrices de resultados y tablas finales copiadas de Wikipedia (Clausura 2025, Apertura 2026) usadas por build.py.

```python
AP26_A="""| Home \\ Away | BOC | CCO | DYJ | DRI | EST | GME | IND | INS | LAN | NOB | PLA | SLO | TAL | UNI | VEL |
| Boca Juniors |  |  |  | 1–0 |  | 1–1 | 1–1 | 2–0 |  | 2–0 | 0–0 | 1–1 |  |  |  |
| Central Córdoba (SdE) | 1–2 |  |  | 1–0 |  | 0–1 |  |  |  | 1–3 | 4–3 |  | 2–0 | 1–0 |  |
| Defensa y Justicia | 0–4 | 1–1 |  |  | 0–0 |  |  |  | 1–1 |  |  |  | 1–2 | 2–0 | 1–1 |
| Deportivo Riestra |  |  | 0–1 |  |  | 0–0 | 2–0 | 0–1 |  | 1–1 | 0–0 | 1–1 |  |  |  |
| Estudiantes (LP) | 2–1 | 5–0 |  | 1–0 |  |  |  |  | 0–1 |  |  |  | 0–0 | 2–1 | 0–1 |
| Gimnasia y Esgrima (M) |  |  | 2–1 |  | 1–2 |  | 1–1 | 1–0 | 1–0 |  |  | 0–1 |  |  | 3–2 |
| Independiente |  | 2–0 | 3–1 |  | 1–1 |  |  |  | 2–0 |  |  |  | 1–2 | 4–4 | 1–1 |
| Instituto |  | 2–0 | 2–0 |  | 0–1 |  | 2–1 |  | 2–2 |  |  |  |  | 1–2 | 0–1 |
| Lanús | 0–3 | 0–0 |  | 0–0 |  |  |  |  |  | 5–0 | 0–0 |  | 1–1 | 2–1 |  |
| Newell's Old Boys |  |  | 2–3 |  | 0–2 | 1–0 | 1–1 | 1–1 |  |  | 1–1 | 0–0 |  |  |  |
| Platense |  |  | 0–0 |  | 0–2 | 1–1 | 0–1 | 2–1 |  |  |  | 0–1 |  |  | 0–2 |
| San Lorenzo |  | 1–0 | 2–5 |  | 1–0 |  | 1–2 | 1–1 | 2–3 |  |  |  |  |  | 0–0 |
| Talleres (C) | 0–1 |  |  | 2–0 |  | 2–1 |  | 2–0 |  | 2–1 | 1–2 | 0–0 |  |  |  |
| Unión | 1–1 |  |  | 2–0 |  | 4–0 |  |  |  | 2–3 | 0–0 | 0–0 | 1–1 |  |  |
| Vélez Sarsfield | 2–1 | 1–0 |  | 0–0 |  |  |  |  | 0–1 | 1–1 |  |  | 2–1 | 2–2 |  |"""
AP26_B="""| Home \\ Away | ALD | ARG | ATU | BAN | BAR | BEL | ERC | GLP | HUR | IRI | RAC | RIV | ROS | SAR | TIG |
| Aldosivi |  | 0–2 |  |  | 0–0 |  | 0–0 |  | 0–0 | 1–1 | 1–1 |  | 1–1 |  |  |
| Argentinos Juniors |  |  | 1–0 | 3–2 | 1–1 | 0–0 |  |  |  |  |  | 1–0 | 0–0 | 1–0 |  |
| Atlético Tucumán | 1–1 |  |  | 1–1 |  |  | 4–0 | 1–0 | 1–1 |  | 0–3 |  |  |  | 0–0 |
| Banfield | 2–0 |  |  |  |  |  | 2–1 | 1–2 | 1–1 | 0–0 | 0–2 |  |  |  | 1–0 |
| Barracas Central |  |  | 2–1 | 1–2 |  | 0–0 |  | 2–0 |  |  |  | 0–1 |  | 1–2 | 2–1 |
| Belgrano | 1–0 |  | 3–1 | 1–0 |  |  |  | 0–1 |  |  | 1–2 |  |  | 4–0 | 1–1 |
| Estudiantes (RC) |  | 0–0 |  |  | 1–2 | 0–1 |  |  | 2–0 | 0–1 |  | 0–2 | 1–2 |  |  |
| Gimnasia y Esgrima (LP) | 3–1 | 2–0 |  |  |  |  | 1–0 |  | 0–3 | 2–3 | 2–1 |  | 1–2 |  |  |
| Huracán |  | 1–2 |  |  | 0–0 | 3–1 |  |  |  | 1–2 |  | 1–2 | 3–1 | 1–0 |  |
| Independiente Rivadavia |  | 3–1 | 2–1 |  | 1–2 | 0–1 |  |  |  |  |  | 1–1 | 2–0 | 2–1 |  |
| Racing |  | 2–1 |  |  | 1–1 |  | 2–0 |  | 0–0 | 1–1 |  | 0–2 | 1–2 |  |  |
| River Plate | 3–1 |  | 0–1 | 3–1 |  | 3–0 |  | 2–0 |  |  |  |  |  | 2–0 | 1–4 |
| Rosario Central |  |  | 2–1 | 2–1 | 2–0 | 1–2 |  |  |  |  |  | 0–0 |  | 2–1 | 1–1 |
| Sarmiento (J) | 2–0 |  | 2–1 | 1–0 |  |  | 1–0 | 1–2 |  |  | 0–0 |  |  |  | 1–0 |
| Tigre | 1–0 | 1–1 |  |  |  |  | 2–0 | 2–2 | 1–1 | 0–2 | 3–1 |  |  |  |  |"""
AP26_I="""| Aldosivi | 0–0 | Defensa y Justicia |
| Atlético Tucumán | 0–0 | Central Córdoba (SdE) |
| Barracas Central | 1–1 | Deportivo Riestra |
| Huracán | 1–0 | San Lorenzo |
| Gimnasia y Esgrima (LP) | 0–0 | Estudiantes (LP) |
| Sarmiento (J) | 1–3 | Unión |
| Newell's Old Boys | 0–2 | Rosario Central |
| Tigre | 1–1 | Vélez Sarsfield |
| Belgrano | 0–0 | Talleres (C) |
| Argentinos Juniors | 1–0 | Platense |
| Independiente | 1–0 | Racing |
| Lanús | 1–0 | Banfield |
| River Plate | 0–1 | Boca Juniors |
| Independiente Rivadavia | 5–1 | Gimnasia y Esgrima (M) |
| Estudiantes (RC) | 0–2 | Instituto |
| Defensa y Justicia | 1–1 | Belgrano |
| Estudiantes (LP) | 1–0 | Sarmiento (J) |
| Boca Juniors | 0–0 | Racing |
| Instituto | 2–1 | Atlético Tucumán |
| Gimnasia y Esgrima (M) | 0–1 | Gimnasia y Esgrima (LP) |
| Rosario Central | 0–1 | Talleres (C) |
| Independiente Rivadavia | 3–2 | Independiente |
| Platense | 1–0 | Barracas Central |
| Banfield | 3–0 | Newell's Old Boys |
| Deportivo Riestra | 0–0 | Huracán |
| Central Córdoba (SdE) | 0–0 | Tigre |
| San Lorenzo | 2–0 | Estudiantes (RC) |
| Vélez Sarsfield | 1–0 | River Plate |
| Unión | 1–0 | Aldosivi |
| Argentinos Juniors | 2–1 | Lanús |"""
CL25_A="""| Home \\ Away | ALD | ARG | BAN | BAR | BEL | BOC | CCO | DYJ | EST | HUR | IRI | NOB | RAC | TIG | UNI |
| Aldosivi |  | 0–2 |  |  | 0–0 | 0–2 | 0–0 |  |  | 2–0 | 3–1 | 0–0 |  |  |  |
| Argentinos Juniors |  |  | 3–0 |  | 1–0 | 0–0 | 0–0 |  |  |  |  | 3–1 | 4–1 |  | 1–0 |
| Banfield | 0–1 |  |  | 1–3 |  |  |  | 0–0 | 3–2 |  |  |  | 1–3 | 1–0 | 0–0 |
| Barracas Central | 3–1 | 2–0 |  |  | 1–1 | 1–3 |  | 1–1 |  | 1–1 | 0–3 |  |  |  |  |
| Belgrano |  |  | 2–1 |  |  |  | 0–3 |  | 1–1 |  |  | 3–0 | 0–1 | 0–0 | 0–0 |
| Boca Juniors |  |  | 2–0 |  | 1–2 |  | 2–2 |  |  |  |  | 5–0 | 1–1 | 2–0 | 1–1 |
| Central Córdoba (SdE) |  |  | 1–1 | 1–1 |  |  |  | 2–1 | 2–0 |  |  |  | 0–0 | 0–1 | 3–1 |
| Defensa y Justicia | 2–0 | 1–0 |  |  | 2–1 | 2–1 |  |  |  | 1–3 | 0–2 | 1–1 |  |  |  |
| Estudiantes (LP) | 1–0 | 1–2 |  | 1–1 |  | 1–2 |  | 1–0 |  | 2–1 | 2–1 |  |  |  |  |
| Huracán |  | 1–0 | 1–0 |  | 0–3 | 1–0 | 0–1 |  |  |  |  | 0–2 | 0–2 |  |  |
| Independiente Rivadavia |  | 2–1 | 1–2 |  | 0–0 | 0–3 | 0–0 |  |  | 0–0 |  | 1–2 |  |  |  |
| Newell's Old Boys |  |  | 1–2 | 1–2 |  |  | 1–1 |  | 1–1 |  |  |  | 0–1 | 1–1 | 0–1 |
| Racing | 1–0 |  |  | 0–1 |  |  |  | 1–0 | 0–1 |  | 0–0 |  |  | 1–2 | 2–3 |
| Tigre | 2–0 | 2–1 |  | 2–2 |  |  |  | 1–1 | 1–0 | 0–1 | 1–1 |  |  |  |  |
| Unión | 0–2 |  |  | 0–0 |  |  |  | 3–0 | 1–0 | 1–1 | 2–2 |  |  | 0–0 |  |"""
CL25_B="""| Home \\ Away | ATU | DRI | GLP | GOD | IND | INS | LAN | PLA | RIV | ROS | SLO | SMA | SAR | TAL | VEL |
| Atlético Tucumán |  |  |  | 2–1 |  |  |  | 2–0 | 2–0 | 0–0 | 1–2 | 2–1 |  | 3–0 |  |
| Deportivo Riestra | 1–0 |  | 1–0 |  | 0–1 | 1–0 | 1–0 |  |  |  |  |  | 3–0 |  | 2–2 |
| Gimnasia y Esgrima (LP) | 1–0 |  |  |  | 1–0 | 0–1 | 1–2 |  |  | 0–3 |  |  |  | 1–2 | 2–0 |
| Godoy Cruz |  | 1–1 | 1–2 |  | 1–1 | 1–1 |  |  |  |  |  | 0–0 | 0–0 |  | 0–2 |
| Independiente | 3–0 |  |  |  |  |  | 0–2 | 3–0 | 0–0 | 1–0 | 1–1 |  |  | 1–2 |  |
| Instituto | 2–0 |  |  |  | 0–0 |  | 0–0 | 1–1 | 0–4 | 1–3 |  |  |  | 0–0 |  |
| Lanús | 3–1 |  |  | 2–0 |  |  |  | 2–1 | 1–1 | 0–1 | 2–1 |  |  | 1–0 |  |
| Platense |  | 1–1 | 0–3 | 1–3 |  |  |  |  |  |  | 2–1 | 2–2 | 1–1 |  | 0–0 |
| River Plate |  | 1–2 | 0–1 | 4–2 |  |  |  | 3–1 |  |  | 0–0 | 2–0 | 0–1 |  |  |
| Rosario Central |  | 1–1 |  | 1–1 |  |  |  | 1–0 | 2–1 |  | 0–0 | 0–0 |  | 1–1 |  |
| San Lorenzo |  | 1–0 | 0–0 | 2–0 |  | 1–0 |  |  |  |  |  | 0–1 | 1–1 |  | 1–0 |
| San Martín (SJ) |  | 3–2 | 1–0 |  | 1–0 | 0–0 | 1–1 |  |  |  |  |  | 0–1 |  | 1–2 |
| Sarmiento (J) | 2–2 |  | 0–1 |  | 2–2 | 2–1 | 0–2 |  |  | 0–1 |  |  |  |  | 0–2 |
| Talleres (C) |  | 0–1 |  | 0–0 |  |  |  | 1–0 | 0–2 |  | 1–2 | 0–0 | 1–0 |  |  |
| Vélez Sarsfield | 3–1 |  |  |  | 2–1 | 0–0 | 3–0 |  | 0–0 | 1–2 |  |  |  | 0–1 |  |"""
CL25_I="""| Atlético Tucumán | 1–1 | Central Córdoba (SdE) |
| Platense | 0–0 | Argentinos Juniors |
| Defensa y Justicia | 1–0 | Deportivo Riestra |
| Instituto | 0–4 | Unión |
| Rosario Central | 1–0 | Newell's Old Boys |
| San Lorenzo | 0–0 | Huracán |
| Barracas Central | 0–1 | Sarmiento (J) |
| Racing | 0–0 | Independiente |
| Talleres (C) | 0–0 | Belgrano |
| Independiente Rivadavia | 0–0 | Godoy Cruz |
| Estudiantes (LP) | 2–0 | Gimnasia y Esgrima (LP) |
| Banfield | 2–1 | Lanús |
| Boca Juniors | 2–0 | River Plate |
| Aldosivi | 4–2 | San Martín (SJ) |
| Vélez Sarsfield | 2–1 | Tigre |
| Belgrano | 0–0 | San Martín (SJ) |
| Deportivo Riestra | 2–0 | Central Córdoba (SdE) |
| Huracán | 0–0 | Vélez Sarsfield |
| Racing | 2–0 | San Lorenzo |
| Lanús | 1–0 | Independiente Rivadavia |
| Newell's Old Boys | 2–0 | Atlético Tucumán |
| Godoy Cruz | 0–0 | Barracas Central |
| Independiente | 0–1 | Banfield |
| Estudiantes (LP) | 1–2 | River Plate |
| Sarmiento (J) | 2–0 | Aldosivi |
| Gimnasia y Esgrima (LP) | 1–3 | Unión |
| Instituto | 2–0 | Argentinos Juniors |
| Rosario Central | 1–1 | Boca Juniors |
| Defensa y Justicia | 1–2 | Platense |
| Tigre | 0–0 | Talleres (C) |"""
# Pts GF GA finales (fase de grupos)
ST_CL25="""BOC 29 28 12;UNI 25 20 13;RAC 25 16 13;CCO 24 17 11;ARG 24 18 13;BAR 23 19 17;TIG 22 14 13;EST 21 17 18;BAN 21 15 21;BEL 20 13 11;HUR 20 10 15;DYJ 19 14 19;ALD 18 13 18;IRI 16 14 17;NOB 14 13 23;ROS 31 18 8;LAN 30 20 13;DRI 28 19 12;VEL 26 19 12;SLO 24 13 11;RIV 22 20 15;GLP 22 14 16;TAL 21 9 12;SAR 20 13 17;SMA 19 13 16;IND 18 14 13;ATU 18 17 22;INS 16 9 17;GOD 12 11 19;PLA 12 12 25"""
ST_AP25="""ARG 33 24 9;BOC 33 24 11;RAC 28 26 16;HUR 27 19 12;TIG 27 18 12;IRI 27 20 17;BAR 26 20 18;EST 21 18 19;NOB 19 12 15;DYJ 19 18 22;CCO 18 21 22;BEL 17 13 23;ALD 15 18 28;BAN 14 14 19;UNI 14 11 17;ROS 35 22 8;RIV 31 21 9;IND 29 23 12;SLO 27 14 10;DRI 24 13 7;PLA 23 13 11;LAN 20 13 11;INS 18 16 20;GOD 17 8 18;ATU 16 17 21;GLP 16 9 18;SAR 15 11 19;VEL 14 7 22;TAL 13 11 15;SMA 9 5 18"""

```

#### `datos/cups.py`

Fase de grupos de Libertadores y Sudamericana 2025-2026 de los equipos argentinos, con validación contra las tablas de grupo.

```python
import datetime as dt
D=dt.date
MD={(4,2):1,(3,1):1,(2,3):2,(1,4):2,(2,1):3,(4,3):3,(3,2):4,(4,1):4,(1,2):5,(3,4):5,(1,3):6,(2,4):6}
DATES={2025:{1:D(2025,4,2),2:D(2025,4,9),3:D(2025,4,23),4:D(2025,5,7),5:D(2025,5,14),6:D(2025,5,28)},
       2026:{1:D(2026,4,8),2:D(2026,4,15),3:D(2026,4,29),4:D(2026,5,6),5:D(2026,5,20),6:D(2026,5,27)}}
# (año, competencia, equipo argentino, codigos brasileños, potes, partidos [local,visitante,gl,gv], esperado [pts,gf,gc])
G=[
(2025,'LIB','EST',{'BOT'},{'EST':2,'BOT':1,'UCH':3,'CBO':4},[('EST','BOT',1,0),('EST','UCH',1,2),('EST','CBO',2,0),('BOT','EST',3,2),('UCH','EST',0,3),('CBO','EST',0,2)],(12,11,5)),
(2025,'LIB','RIV',set(),{'RIV':1,'UNI':3,'IDV':2,'BSC':4},[('RIV','UNI',1,1),('RIV','IDV',6,2),('RIV','BSC',0,0),('UNI','RIV',0,1),('IDV','RIV',2,2),('BSC','RIV',2,3)],(12,13,7)),
(2025,'LIB','CCO',{'FLA'},{'LDQ':2,'FLA':1,'CCO':4,'TAC':3},[('LDQ','CCO',3,0),('FLA','CCO',1,2),('CCO','LDQ',0,0),('CCO','FLA',1,1),('CCO','TAC',2,1),('TAC','CCO',1,2)],(11,7,7)),
(2025,'LIB','TAL',{'SPA'},{'SPA':1,'LIB':2,'ALI':4,'TAL':3},[('SPA','TAL',2,1),('LIB','TAL',2,0),('ALI','TAL',3,2),('TAL','SPA',0,1),('TAL','LIB',0,0),('TAL','ALI',2,0)],(4,5,8)),
(2025,'LIB','RAC',{'FOR'},{'RAC':1,'FOR':3,'BUC':4,'CLC':2},[('RAC','FOR',1,0),('RAC','BUC',1,2),('RAC','CLC',4,0),('FOR','RAC',0,3),('BUC','RAC',0,4),('CLC','RAC',1,1)],(13,14,3)),
(2025,'LIB','VEL',set(),{'VEL':3,'PEN':1,'SAB':4,'OLI':2},[('VEL','PEN',2,1),('VEL','SAB',3,0),('VEL','OLI',1,1),('PEN','VEL',0,0),('SAB','VEL',2,1),('OLI','VEL',0,4)],(11,11,4)),
(2025,'SUD','IND',set(),{'IND':1,'GUA':2,'BOS':4,'NAP':3},[('IND','GUA',1,0),('IND','BOS',2,1),('IND','NAP',7,0),('GUA','IND',2,1),('BOS','IND',1,5),('NAP','IND',2,0)],(12,16,6)),
(2025,'SUD','DYJ',{'VIT'},{'UCA':2,'CRL':3,'VIT':4,'DYJ':1},[('UCA','DYJ',3,1),('CRL','DYJ',0,0),('VIT','DYJ',1,1),('DYJ','UCA',1,1),('DYJ','CRL',1,2),('DYJ','VIT',0,0)],(4,4,7)),
(2025,'SUD','HUR',{'COR'},{'HUR':2,'AME':1,'COR':4,'RCM':3},[('HUR','AME',0,0),('HUR','COR',1,0),('HUR','RCM',5,0),('AME','HUR',0,0),('COR','HUR',1,2),('RCM','HUR',1,3)],(14,11,2)),
(2025,'SUD','GOD',{'GRE'},{'GOD':2,'GRE':1,'CAG':4,'SLU':3},[('GOD','GRE',2,2),('GOD','CAG',2,2),('GOD','SLU',2,0),('GRE','GOD',1,1),('CAG','GOD',0,2),('SLU','GOD',0,1)],(12,10,5)),
(2025,'SUD','UNI',{'CRU'},{'MUS':4,'PAL':2,'CRU':1,'UNI':3},[('UNI','MUS',0,1),('UNI','PAL',1,2),('UNI','CRU',1,0),('MUS','UNI',3,0),('PAL','UNI',2,0),('CRU','UNI',0,0)],(4,2,8)),
(2025,'SUD','LAN',{'VAS'},{'LAN':1,'VAS':2,'MEL':4,'APC':3},[('LAN','VAS',1,0),('LAN','MEL',3,0),('LAN','APC',2,2),('VAS','LAN',0,0),('MEL','LAN',0,1),('APC','LAN',2,2)],(12,9,4)),
(2026,'LIB','EST',{'FLA'},{'FLA':1,'EST':2,'DIM':4,'CUS':3},[('FLA','EST',1,0),('EST','FLA',1,1),('EST','DIM',1,0),('EST','CUS',2,1),('DIM','EST',1,1),('CUS','EST',1,1)],(9,6,5)),
(2026,'LIB','IRI',{'FLU'},{'IRI':4,'FLU':1,'BOL':2,'DLG':3},[('IRI','FLU',1,1),('IRI','BOL',1,0),('IRI','DLG',4,1),('FLU','IRI',1,2),('BOL','IRI',1,3),('DLG','IRI',2,4)],(16,15,6)),
(2026,'LIB','BOC',{'CRU'},{'UCA':3,'CRU':2,'BOC':1,'BSC':4},[('UCA','BOC',1,2),('CRU','BOC',1,0),('BOC','UCA',0,1),('BOC','CRU',1,1),('BOC','BSC',3,0),('BSC','BOC',1,0)],(7,6,5)),
(2026,'LIB','PLA',{'COR'},{'COR':2,'PLA':4,'SFE':3,'PEN':1},[('COR','PLA',0,2),('PLA','COR',0,2),('PLA','SFE',2,1),('PLA','PEN',1,1),('SFE','PLA',2,1),('PEN','PLA',1,2)],(10,8,7)),
(2026,'LIB','LAN',{'MIR'},{'LDQ':1,'MIR':4,'LAN':2,'CAR':3},[('LDQ','LAN',2,0),('MIR','LAN',1,0),('CAR','LAN',4,0),('LAN','LDQ',1,0),('LAN','MIR',1,0),('LAN','CAR',1,0)],(9,3,7)),
(2026,'LIB','ROS',set(),{'IDV':1,'ROS':3,'UCV':4,'LIB':2},[('IDV','ROS',1,0),('UCV','ROS',0,3),('LIB','ROS',0,1),('ROS','IDV',0,0),('ROS','UCV',4,0),('ROS','LIB',1,0)],(13,9,1)),
(2026,'SUD','TIG',set(),{'MAC':3,'TIG':2,'AME':1,'AAS':4},[('MAC','TIG',2,2),('TIG','MAC',0,1),('TIG','AME',2,0),('TIG','AAS',2,0),('AME','TIG',1,1),('AAS','TIG',1,1)],(9,8,5)),
(2026,'SUD','SLO',{'SAN'},{'REC':4,'SAN':1,'SLO':2,'CUE':3},[('REC','SLO',1,1),('SLO','REC',0,1),('SAN','SLO',2,2),('SLO','SAN',1,1),('SLO','CUE',2,0),('CUE','SLO',0,0)],(7,6,5)),
(2026,'SUD','RAC',{'BOT'},{'BOT':4,'CAR':2,'RAC':1,'IPE':3},[('BOT','RAC',2,1),('CAR','RAC',1,1),('IPE','RAC',1,3),('RAC','BOT',2,3),('RAC','CAR',2,2),('RAC','IPE',2,0)],(8,11,9)),
(2026,'SUD','DRI',{'GRE'},{'MCT':3,'GRE':1,'DRI':4,'PAL':2},[('MCT','DRI',4,1),('GRE','DRI',1,0),('PAL','DRI',1,1),('DRI','MCT',2,1),('DRI','GRE',0,3),('DRI','PAL',0,0)],(5,4,10)),
(2026,'SUD','BAR',{'VAS'},{'OLI':1,'VAS':2,'AUD':3,'BAR':4},[('OLI','BAR',0,0),('VAS','BAR',3,0),('AUD','BAR',2,0),('BAR','OLI',1,2),('BAR','VAS',0,0),('BAR','AUD',1,1)],(3,2,8)),
(2026,'SUD','RIV',{'RBB'},{'RIV':1,'RBB':2,'CBO':4,'BLO':3},[('RIV','RBB',1,1),('RIV','CBO',1,0),('RIV','BLO',3,0),('RBB','RIV',0,1),('CBO','RIV',1,2),('BLO','RIV',1,1)],(14,9,3)),
]
def rows():
    out=[];bad=[]
    for yr,comp,arg,br,pots,ms,exp in G:
        p=g=c=0;seen=set()
        for h,a,gh,ga in ms:
            mdn=MD[(pots[h],pots[a])]
            assert (mdn,arg) not in seen or True
            tok=lambda x:x if x==arg else ('BR' if x in br else 'EXT')
            out.append((DATES[yr][mdn],3,tok(h),tok(a),gh,ga))
            f,k=(gh,ga) if h==arg else (ga,gh)
            p+=3 if f>k else 1 if f==k else 0;g+=f;c+=k
            seen.add(mdn)
        if len(seen)!=6 or (p,g,c)!=exp:bad.append((yr,comp,arg,(p,g,c),exp,sorted(seen)))
    return out,bad
if __name__=='__main__':
    r,bad=rows();print('partidos de copa:',len(r),'| desajustes:',bad if bad else 'ninguno (los 24 equipos-grupo coinciden con Pts, GF y GC de la tabla; cada uno juega una vez por fecha)')

```

#### `datos/ar2025.txt`

Apertura 2025 completo (openfootball/south-america, argentina/2025_ar1.txt), tal cual se descargó.

```text
= Argentina Primera Division 2025

# Date       Thu Jan 23 - Sun May 4 2025 (101d)
# Teams      30
# Matches    240
# Stages     1° Semestre (240)



▪ 1° Semestre, Matchday 1
  Thu Jan 23 2025
    19:00  Tigre                   v Vélez Sarsfield          3-0 (2-0)
           Godoy Cruz              v Rosario Central          0-3 (0-2)
    21:30  Newell's Old Boys       v Independiente Rivadavia  0-1 (0-1)
           Defensa y Justicia      v Banfield                 0-1 (0-0)
           Lanús                   v Deportivo Riestra        0-2 (0-0)
  Fri Jan 24
    17:00  Barracas Central        v Racing Club              1-3 (1-1)
    19:15  Independiente           v Sarmiento de Junín       2-1 (1-0)
    21:00  Belgrano de Córdoba     v Huracán                  1-1 (1-1)
    21:30  San Martín de San Juan  v Atlético Tucumán         0-1 (0-1)
  Sat Jan 25
    17:00  San Lorenzo             v Talleres de Córdoba      1-0 (0-0)
    19:15  Estudiantes             v Unión de Santa Fe        3-1 (3-0)
           Instituto de Córdoba    v Gimnasia de La Plata     3-0 (1-0)
    21:30  Platense                v River Plate              1-1 (1-0)
  Sun Jan 26
    19:00  Boca Juniors            v Argentinos Juniors       0-0
    21:00  Central Córdoba SdE     v Aldosivi                 1-0 (0-0)


▪ 1° Semestre, Matchday 2
  Mon Jan 27
    20:00  Banfield                v Newell's Old Boys        3-0 (2-0)
  Tue Jan 28
    17:00  Deportivo Riestra       v San Martín de San Juan   0-0
    19:15  Rosario Central         v Lanús                    2-1 (2-0)
           Sarmiento de Junín      v Godoy Cruz               0-0
    21:30  Independiente Rivadavia v Barracas Central         0-0
           Vélez Sarsfield         v Platense                 0-1 (0-0)
  Wed Jan 29
    17:00  Talleres de Córdoba     v Independiente            2-3 (1-2)
           Gimnasia de La Plata    v San Lorenzo              0-2 (0-0)
    19:15  Huracán                 v Estudiantes              0-0
           Unión de Santa Fe       v Boca Juniors             1-1 (0-1)
    21:30  River Plate             v Instituto de Córdoba     1-0 (0-0)
  Thu Jan 30
    17:00  Aldosivi                v Defensa y Justicia       0-5 (0-2)
    19:15  Racing Club             v Belgrano de Córdoba      4-0 (1-0)
    21:30  Argentinos Juniors      v Tigre                    1-0 (1-0)
           Central Córdoba SdE     v Atlético Tucumán         2-0 (1-0)


▪ 1° Semestre, Matchday 3
  Sat Feb 1
    17:00  Barracas Central        v Banfield                 1-0 (1-0)
    19:00  San Martín de San Juan  v Rosario Central          0-0
    21:00  Lanús                   v Sarmiento de Junín       2-0 (2-0)
  Sun Feb 2
    17:00  San Lorenzo             v River Plate              0-0
    19:15  Boca Juniors            v Huracán                  2-1 (1-1)
           Newell's Old Boys       v Aldosivi                 1-0 (1-0)
    21:30  Instituto de Córdoba    v Vélez Sarsfield          2-0 (1-0)
           Independiente           v Gimnasia de La Plata     2-0 (1-0)
  Mon Feb 3
    17:00  Defensa y Justicia      v Central Córdoba SdE      2-1 (0-0)
    19:15  Tigre                   v Unión de Santa Fe        1-0 (1-0)
           Estudiantes             v Racing Club              2-0 (1-0)
    21:30  Belgrano de Córdoba     v Independiente Rivadavia  0-3 (0-3)
           Argentinos Juniors      v Platense                 1-0 (0-0)
  Tue Feb 4
    21:00  Atlético Tucumán        v Deportivo Riestra        0-3 (0-1)
  Sat Mar 22
    17:00  Godoy Cruz              v Talleres de Córdoba      0-0


▪ 1° Semestre, Matchday 4
  Thu Feb 6
    17:00  Aldosivi                v Barracas Central         1-3 (0-2)
    20:00  Sarmiento de Junín      v San Martín de San Juan   1-1 (0-1)
  Fri Feb 7
    17:45  Banfield                v Belgrano de Córdoba      1-1 (1-0)
    20:00  Central Córdoba SdE     v Newell's Old Boys        2-0 (1-0)
           Huracán                 v Tigre                    2-0 (1-0)
    22:15  Independiente Rivadavia v Estudiantes              2-2 (0-0)
           Unión de Santa Fe       v Argentinos Juniors       0-1 (0-1)
  Sat Feb 8
    18:00  Vélez Sarsfield         v San Lorenzo              0-0
    19:30  Rosario Central         v Atlético Tucumán         3-1 (1-0)
    20:15  River Plate             v Independiente            2-0 (0-0)
    22:15  Racing Club             v Boca Juniors             2-0 (1-0)
  Sun Feb 9
    17:00  Platense                v Instituto de Córdoba     1-0 (0-0)
           Deportivo Riestra       v Defensa y Justicia       1-1 (0-0)
    19:15  Gimnasia de La Plata    v Godoy Cruz               3-0 (1-0)
    21:30  Talleres de Córdoba     v Lanús                    0-1 (0-1)


▪ 1° Semestre, Matchday 5
  Tue Feb 11
    17:45  Barracas Central        v Central Córdoba SdE      3-3 (0-0)
    20:00  Boca Juniors            v Independiente Rivadavia  2-0 (0-0)
           Estudiantes             v Banfield                 1-0 (0-0)
    22:15  Tigre                   v Racing Club              1-0 (1-0)
           Belgrano de Córdoba     v Aldosivi                 2-0 (1-0)
  Wed Feb 12
    17:00  Deportivo Riestra       v Rosario Central          0-0
    17:45  Newell's Old Boys       v Defensa y Justicia       0-1 (0-0)
    20:00  Argentinos Juniors      v Huracán                  1-1 (1-0)
           Independiente           v Vélez Sarsfield          3-0 (2-0)
    22:15  Godoy Cruz              v River Plate              0-0
  Thu Feb 13
    17:45  Lanús                   v Gimnasia de La Plata     0-0
    20:00  San Lorenzo             v Platense                 2-1 (1-1)
           San Martín de San Juan  v Talleres de Córdoba      0-1 (0-0)
    22:15  Atlético Tucumán        v Sarmiento de Junín       5-0 (4-0)
           Unión de Santa Fe       v Instituto de Córdoba     0-0


▪ 1° Semestre, Matchday 6
  Fri Feb 14
    20:00  Banfield                v Boca Juniors             0-1 (0-0)
  Sat Feb 15
    17:00  Defensa y Justicia      v Barracas Central         1-1 (1-0)
           Aldosivi                v Estudiantes              2-2 (0-1)
    19:15  Central Córdoba SdE     v Belgrano de Córdoba      4-0 (2-0)
           Independiente Rivadavia v Tigre                    1-4 (0-2)
    21:30  Racing Club             v Argentinos Juniors       2-3 (0-2)
  Sun Feb 16
    17:00  Newell's Old Boys       v Rosario Central          1-2 (0-1)
    19:15  River Plate             v Lanús                    1-0 (0-0)
    21:30  Huracán                 v Unión de Santa Fe        1-0 (0-0)
           Talleres de Córdoba     v Atlético Tucumán         1-1 (0-0)
  Mon Feb 17
    17:00  Sarmiento de Junín      v Deportivo Riestra        2-1 (0-1)
           Gimnasia de La Plata    v San Martín de San Juan   1-0 (1-0)
    19:15  Platense                v Independiente            1-1 (0-0)
    21:30  Vélez Sarsfield         v Godoy Cruz               0-2 (0-2)
           Instituto de Córdoba    v San Lorenzo              0-1 (0-1)


▪ 1° Semestre, Matchday 7
  Fri Feb 21
    17:00  Deportivo Riestra       v Talleres de Córdoba      0-0
    19:15  Estudiantes             v Central Córdoba SdE      3-2 (0-1)
           Godoy Cruz              v Platense                 1-1 (0-1)
    21:30  Lanús                   v Vélez Sarsfield          0-0
  Sat Feb 22
    18:00  Independiente           v Instituto de Córdoba     2-0 (0-0)
    19:30  Boca Juniors            v Aldosivi                 2-1 (0-0)
    21:30  San Martín de San Juan  v River Plate              0-2 (0-0)
    21:45  Rosario Central         v Sarmiento de Junín       1-0 (1-0)
  Sun Feb 23
    18:00  Huracán                 v San Lorenzo              2-0 (1-0)
    21:00  Belgrano de Córdoba     v Defensa y Justicia       2-0 (1-0)
           Atlético Tucumán        v Gimnasia de La Plata     0-1 (0-1)
  Mon Feb 24
    17:00  Barracas Central        v Newell's Old Boys        2-0 (1-0)
    19:00  Argentinos Juniors      v Independiente Rivadavia  0-0
    21:00  Tigre                   v Banfield                 1-0 (0-0)
  Thu Mar 20
    21:00  Unión de Santa Fe       v Racing Club              0-1 (0-0)


▪ 1° Semestre, Matchday 8
  Fri Feb 28
    20:00  Boca Juniors            v Rosario Central          1-0 (1-0)
    22:15  Central Córdoba SdE     v Deportivo Riestra        0-0
           San Martín de San Juan  v Belgrano de Córdoba      3-1 (0-0)
  Sat Mar 1
    17:00  Aldosivi                v Sarmiento de Junín       2-2 (2-2)
    19:15  River Plate             v Estudiantes              0-2 (0-1)
    21:30  Unión de Santa Fe       v Gimnasia de La Plata     1-0 (0-0)
           Talleres de Córdoba     v Tigre                    1-2 (1-1)
  Sun Mar 2
    17:00  Independiente Rivadavia v Lanús                    1-1 (0-0)
           Argentinos Juniors      v Instituto de Córdoba     2-0 (0-0)
    19:15  Vélez Sarsfield         v Huracán                  0-2 (0-1)
  Mon Mar 3
    17:00  Barracas Central        v Godoy Cruz               1-2 (0-1)
    19:00  San Lorenzo             v Racing Club              3-2 (1-1)
    21:00  Atlético Tucumán        v Newell's Old Boys        1-2 (1-2)
  Tue Mar 4
    19:30  Banfield                v Independiente            0-0
    20:00  Platense                v Defensa y Justicia       0-1 (0-1)


▪ 1° Semestre, Matchday 9
  Fri Mar 7
    19:00  Banfield                v Argentinos Juniors       1-2 (1-0)
           Vélez Sarsfield         v San Martín de San Juan   1-0 (0-0)
    21:15  Central Córdoba SdE     v Boca Juniors             0-3 (0-2)
  Sat Mar 8
    17:00  San Lorenzo             v Independiente            1-2 (1-1)
    19:15  Racing Club             v Huracán                  0-1 (0-1)
    21:30  Platense                v Lanús                    0-0
           Sarmiento de Junín      v Barracas Central         1-1 (0-0)
  Sun Mar 9
    17:00  Defensa y Justicia      v Estudiantes              1-0 (0-0)
           Aldosivi                v Tigre                    0-2 (0-1)
    19:15  River Plate             v Atlético Tucumán         1-0 (0-0)
    21:30  Newell's Old Boys       v Belgrano de Córdoba      0-0
           Instituto de Córdoba    v Godoy Cruz               1-1 (1-1)
  Mon Mar 10
    19:00  Gimnasia de La Plata    v Deportivo Riestra        1-1 (0-1)
    21:15  Independiente Rivadavia v Unión de Santa Fe        2-0 (1-0)
           Talleres de Córdoba     v Rosario Central          0-0


▪ 1° Semestre, Matchday 10
  Fri Mar 14
    19:00  Argentinos Juniors      v Aldosivi                 0-2 (0-1)
    21:00  Godoy Cruz              v San Lorenzo              0-0
  Sat Mar 15
    16:00  Deportivo Riestra       v River Plate              0-0
    18:30  Estudiantes             v Newell's Old Boys        1-1 (1-1)
           Rosario Central         v Gimnasia de La Plata     2-1 (1-1)
    21:00  Huracán                 v Independiente Rivadavia  2-0 (0-0)
           Sarmiento de Junín      v Talleres de Córdoba      0-0
  Sun Mar 16
    16:00  Independiente           v Racing Club              1-1 (0-1)
    18:15  Boca Juniors            v Defensa y Justicia       4-0 (2-0)
    21:00  Belgrano de Córdoba     v Barracas Central         1-1 (1-1)
           Lanús                   v Instituto de Córdoba     4-1 (1-1)
  Mon Mar 17
    19:00  Unión de Santa Fe       v Banfield                 3-1 (1-0)
           Tigre                   v Central Córdoba SdE      1-2 (0-0)
    21:15  San Martín de San Juan  v Platense                 0-2 (0-2)
           Atlético Tucumán        v Vélez Sarsfield          1-2 (1-1)


▪ 1° Semestre, Matchday 11
  Thu Mar 27
    15:30  Aldosivi                v Unión de Santa Fe        2-1 (1-0)
    18:00  Barracas Central        v Estudiantes              2-1 (1-0)
    21:00  Independiente Rivadavia v Racing Club              2-1 (0-1)
  Fri Mar 28
    17:00  Defensa y Justicia      v Tigre                    1-2 (0-0)
    19:15  Banfield                v Huracán                  0-0
           San Lorenzo             v Lanús                    1-1 (0-0)
    21:30  Vélez Sarsfield         v Deportivo Riestra        0-1 (0-1)
           Platense                v Atlético Tucumán         2-1 (1-1)
  Sat Mar 29
    16:30  Instituto de Córdoba    v San Martín de San Juan   1-0 (0-0)
    18:30  Central Córdoba SdE     v Argentinos Juniors       1-1 (0-0)
    18:45  Independiente           v Godoy Cruz               4-0 (4-0)
    21:00  River Plate             v Rosario Central          2-2 (1-1)
  Sun Mar 30
    15:00  Belgrano de Córdoba     v Talleres de Córdoba      1-1 (0-1)
    16:00  Gimnasia de La Plata    v Sarmiento de Junín       0-0
    19:30  Newell's Old Boys       v Boca Juniors             2-0 (2-0)


▪ 1° Semestre, Matchday 12
  Fri Apr 4
    19:00  Estudiantes             v Belgrano de Córdoba      0-1 (0-1)
    22:00  San Martín de San Juan  v San Lorenzo              0-1 (0-0)
  Sat Apr 5
    15:30  Rosario Central         v Vélez Sarsfield          2-1 (0-1)
           Godoy Cruz              v Independiente Rivadavia  1-1 (1-0)
    18:00  Huracán                 v Aldosivi                 3-3 (1-1)
           Talleres de Córdoba     v Gimnasia de La Plata     2-0 (1-0)
    20:30  Sarmiento de Junín      v River Plate              1-1 (1-1)
  Sun Apr 6
    15:30  Unión de Santa Fe       v Central Córdoba SdE      1-0 (1-0)
           Lanús                   v Independiente            1-1 (0-1)
    18:00  Boca Juniors            v Barracas Central         1-0 (1-0)
    20:15  Racing Club             v Banfield                 4-1 (1-0)
           Argentinos Juniors      v Defensa y Justicia       4-1 (4-0)
  Mon Apr 7
    15:30  Deportivo Riestra       v Platense                 1-0 (0-0)
    21:00  Tigre                   v Newell's Old Boys        0-2 (0-1)
           Atlético Tucumán        v Instituto de Córdoba     3-2 (1-0)


▪ 1° Semestre, Matchday 13
  Fri Apr 11
    19:00  Banfield                v Independiente Rivadavia  1-1 (1-0)
    21:00  Newell's Old Boys       v Argentinos Juniors       0-0
  Sat Apr 12
    15:30  San Lorenzo             v Atlético Tucumán         1-0 (0-0)
    18:00  Barracas Central        v Tigre                    1-0 (1-0)
    20:30  Belgrano de Córdoba     v Boca Juniors             1-3 (0-1)
  Sun Apr 13
    15:30  Instituto de Córdoba    v Deportivo Riestra        3-0 (0-0)
           Gimnasia de La Plata    v Estudiantes              1-1 (1-0)
    18:00  Independiente           v San Martín de San Juan   2-0 (0-0)
    20:15  River Plate             v Talleres de Córdoba      1-1 (0-0)
  Mon Apr 14
    15:30  Aldosivi                v Racing Club              0-2 (0-2)
    18:00  Central Córdoba SdE     v Huracán                  1-2 (1-1)
    19:00  Defensa y Justicia      v Unión de Santa Fe        0-0
    21:15  Vélez Sarsfield         v Sarmiento de Junín       0-1 (0-0)
           Godoy Cruz              v Lanús                    0-0
  Tue Apr 15
    20:00  Platense                v Rosario Central          0-0


▪ 1° Semestre, Matchday 14
  Fri Apr 18
    17:00  Gimnasia de La Plata    v River Plate              0-3 (0-1)
    19:15  Racing Club             v Central Córdoba SdE      1-0 (1-0)
           Talleres de Córdoba     v Vélez Sarsfield          0-1 (0-0)
    21:30  Unión de Santa Fe       v Newell's Old Boys        1-1 (1-1)
  Sat Apr 19
    16:15  Lanús                   v Banfield                 1-1 (1-0)
    18:15  Huracán                 v Defensa y Justicia       1-1 (0-1)
    20:30  Boca Juniors            v Estudiantes              2-0 (0-0)
  Sun Apr 20
    15:30  Deportivo Riestra       v San Lorenzo              0-0
    16:30  San Martín de San Juan  v Godoy Cruz               1-0 (1-0)
    18:00  Sarmiento de Junín      v Platense                 0-1 (0-0)
    20:30  Rosario Central         v Instituto de Córdoba     3-0 (1-0)
  Tue Apr 22
    19:00  Argentinos Juniors      v Barracas Central         3-0 (2-0)
           Tigre                   v Belgrano de Córdoba      0-0
    21:15  Independiente Rivadavia v Aldosivi                 1-0 (1-0)
  Wed Apr 30
    21:00  Atlético Tucumán        v Independiente            2-0 (1-0)


▪ 1° Semestre, Matchday 15
  Sat Apr 26
    15:00  Aldosivi                v Banfield                 2-1 (1-0)
    17:00  San Lorenzo             v Rosario Central          0-1 (0-0)
    19:00  Belgrano de Córdoba     v Argentinos Juniors       1-1 (1-0)
  Sun Apr 27
    15:30  River Plate             v Boca Juniors             2-1 (2-1)
    19:00  Instituto de Córdoba    v Sarmiento de Junín       1-1 (0-0)
           Lanús                   v San Martín de San Juan   1-0 (0-0)
    21:15  Independiente           v Deportivo Riestra        0-0
  Mon Apr 28
    15:00  Barracas Central        v Unión de Santa Fe        2-1 (1-1)
    17:15  Godoy Cruz              v Atlético Tucumán         1-0 (1-0)
    19:30  Estudiantes             v Tigre                    0-0
           Defensa y Justicia      v Racing Club              1-2 (0-0)
    21:45  Central Córdoba SdE     v Independiente Rivadavia  1-2 (0-0)
           Vélez Sarsfield         v Gimnasia de La Plata     1-0 (0-0)
  Tue Apr 29
    19:00  Newell's Old Boys       v Huracán                  2-0 (1-0)
           Platense                v Talleres de Córdoba      2-1 (0-1)


▪ 1° Semestre, Matchday 16
  Fri May 2
    15:30  Banfield                v Central Córdoba SdE      3-1 (2-0)
           Independiente Rivadavia v Defensa y Justicia       3-2 (1-2)
           Racing Club             v Newell's Old Boys        1-0 (0-0)
           Argentinos Juniors      v Estudiantes              4-0 (2-0)
    18:00  Unión de Santa Fe       v Belgrano de Córdoba      1-1 (1-1)
  Sat May 3
    16:00  Deportivo Riestra       v Godoy Cruz               3-0 (1-0)
           Sarmiento de Junín      v San Lorenzo              1-1 (1-0)
           Talleres de Córdoba     v Instituto de Córdoba     1-2 (1-1)
    18:30  Rosario Central         v Independiente            1-0 (1-0)
    21:00  Huracán                 v Barracas Central         0-1 (0-0)
           Atlético Tucumán        v Lanús                    1-0 (0-0)
  Sun May 4
    15:30  Gimnasia de La Plata    v Platense                 1-0 (0-0)
           San Martín de San Juan  v Aldosivi                 0-3 (0-1)
    18:00  Tigre                   v Boca Juniors             1-1 (1-1)
    20:30  River Plate             v Vélez Sarsfield          4-1 (3-1)

```

#### `tests/verificar.js`

Verificación de datos, motor, simulación, Elo y comparación de modelos (Node).

```javascript
// Verificacion de datos y motor. Uso: node tests/verificar.js   (sale con codigo 1 si algo falla)
const fs=require('fs'),vm=require('vm'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','calculadora-clausura-2026.html'),'utf8');
const js=html.match(/<script>\n(\/\/ \[codigo[\s\S]*?)<\/script>/)[1];
const els={};
const ctx=vm.createContext({console,Math,JSON,Object,Array,Set,Date,
  document:{getElementById:id=>els[id]||(els[id]={value:id==='selEq'?'4':'',classList:{toggle(){}},set innerHTML(v){this._h=v},get innerHTML(){return this._h}}),querySelectorAll:()=>[]},
  setTimeout:f=>{f();return 0},clearTimeout:()=>0});
vm.runInContext(js,ctx);
const lines=vm.runInContext('('+function(){
  const out=[];const log=(ok,m)=>out.push((ok?'OK     ':'FALLA  ')+m);
  const all=PAST.concat(FX);
  // --- fixture
  let badF=[];for(let f=1;f<=16;f++){const m=all.filter(x=>x[0]===f),c={};m.forEach(x=>{c[x[1]]=(c[x[1]]||0)+1;c[x[2]]=(c[x[2]]||0)+1});if(m.length!==15||Object.keys(c).length!==30||Object.values(c).some(v=>v!==1))badF.push(f)}
  log(!badF.length,'16 fechas x 15 partidos, cada equipo juega una vez por fecha');
  const pair={},inter={};ALL.forEach(t=>inter[t.c]=0);
  all.forEach(x=>{const k=[x[1],x[2]].sort().join('-');pair[k]=(pair[k]||0)+1;if(zi(x[1])!==zi(x[2])){inter[x[1]]++;inter[x[2]]++}});
  let miss=[];for(const Z of [TA,TB])for(let i=0;i<15;i++)for(let j=i+1;j<15;j++){const k=[Z[i].c,Z[j].c].sort().join('-');if(pair[k]!==1)miss.push(k)}
  log(!miss.length,'210 cruces de la misma zona exactamente una vez');
  log(Object.values(inter).every(v=>v===2),'cada equipo juega exactamente 2 interzonales (la fecha 6 es toda interzonal)');
  // --- datos base
  log(ALL.reduce((a,t)=>a+t.apGF,0)===ALL.reduce((a,t)=>a+t.apGC,0),'Apertura: goles a favor = goles en contra');
  const tot={};ALL.forEach(t=>tot[t.c]={pj:0,pts:0,gf:0,gc:0});
  PAST.forEach(x=>{const[h,a]=[x[1],x[2]],[gh,ga]=x[4];for(const[t,f,c]of[[h,gh,ga],[a,ga,gh]]){const d=tot[t];d.pj++;d.gf+=f;d.gc+=c;d.pts+=f>c?3:f===c?1:0}});
  const bad=ALL.filter(t=>{const d=tot[t.c];return d.pj!==t.clPJ||d.pts!==t.clPts||d.gf!==t.clGF||d.gc!==t.clGC});
  log(!bad.length,'resultados de las fechas 1-10 reproducen PJ/Pts/GF/GC de las 30 filas base '+bad.map(t=>t.c));
  log(ALL.every(t=>COL[t.c])&&new Set(ALL.map(t=>t.c)).size===30,'30 equipos con codigo unico y colores de escudo');
  // --- tablas tras fecha 11 (sin fecha 12) vs bolavip (11/10/2026)
  const exp={INS:[25,11,17,8],VEL:[21,11,17,11],DYJ:[21,11,16,11],BOC:[20,11,17,11],LAN:[17,11,13,9],NOB:[17,11,11,8],GEM:[17,11,14,12],IND:[17,11,11,12],EST:[13,11,13,11],UNI:[13,11,17,19],DRI:[11,11,9,11],SLO:[11,11,4,11],PLA:[10,11,11,17],CCO:[9,11,8,14],TAL:[8,11,11,18],ARG:[21,11,15,10],BEL:[19,11,12,7],ROS:[19,11,12,9],HUR:[19,11,11,8],IRI:[18,11,15,14],GLP:[18,11,16,16],SAR:[16,10,17,16],BAR:[15,11,8,9],RIV:[13,10,13,12],ATU:[13,11,9,9],TIG:[12,11,10,11],RAC:[11,11,13,17],BAN:[10,11,12,17],ALD:[8,11,12,17],ERC:[6,11,6,15]};
  const keep=FX.map((m,i)=>res[i]);FX.forEach((m,i)=>{if(m[0]>=12)res[i]=null});
  const badT=[];for(const c in exp){const p=proj(T[c]);if([p.Pts,p.PJ,p.GF,p.GC].join()!==exp[c].join())badT.push(c)}
  keep.forEach((v,i)=>res[i]=v);
  log(!badT.length,'estado tras la fecha 11 (las fechas 12 en adelante se ignoran): 30 filas coinciden con la tabla publicada '+badT);
  log(true,'resultados oficiales cargados en fechas 11-16: '+FX.filter(m=>m[4]).length+' | pendientes: '+FX.filter(m=>!m[4]).length+' | fecha por defecto: '+curF);
  // --- Elo
  log(ELO_EXTRA.length===864,'ELO_EXTRA tiene '+ELO_EXTRA.length+' partidos (esperado 864)');
  const e=eloRun(),rk=ALL.slice().sort((a,b)=>e.R[b.c]-e.R[a.c]);
  log(rk.every(t=>isFinite(e.R[t.c])),'Elo: top5 '+rk.slice(0,5).map(t=>t.c+' '+Math.round(e.R[t.c])).join(', ')+' | ultimos '+rk.slice(-3).map(t=>t.c+' '+Math.round(e.R[t.c])).join(', '));
  log(true,'Elo: rivales fijos EXT='+Math.round(e.ref.EXT)+' BR='+Math.round(e.ref.BR)+' LOW='+Math.round(e.ref.LOW));
  // --- simulaciones: sumas esperadas
  const chk=m=>{MODEL=m;probs();const o=LAST,sm=a=>a.reduce((p,q)=>p+q,0)/NS,exp={ca:1,po:16,lib:4,sud:6,da:1,dp:1};
    return KEYS.every(k=>Math.abs(sm(o[k])-exp[k])<1e-9)};
  log(chk('goles'),'simulacion (modelo goles): sumas ca=1 po=16 lib=4 sud=6 da=1 dp=1');
  log(chk('elo'),'simulacion (modelo Elo): mismas sumas');
  MODEL='goles';probs();
  const o=LAST;log(o.lib[BI]===NS&&o.sud[BI]===0,'Belgrano (campeon Apertura) = 100% Libertadores y 0% Sudamericana por la anual');
  log(ALL.every((t,i)=>o.da[i]+o.dp[i]<=NS),'ningun equipo desciende dos veces (regla AFA)');
  // --- backtest fechas 7-12
  const M=PAST.map(m=>({f:m[0],h:m[1],a:m[2],gh:m[4][0],ga:m[4][1]})).concat(FX.filter(m=>m[4]).map(m=>({f:m[0],h:m[1],a:m[2],gh:m[4][0],ga:m[4][1]})));
  const oc=(a,b)=>a>b?0:a===b?1:2;
  const pG=(f,h,a)=>{let G=0,N=0;const st={};ALL.forEach(t=>st[t.c]={gf:t.apGF,gc:t.apGC,n:16});M.filter(m=>m.f<f).forEach(m=>{st[m.h].gf+=m.gh;st[m.h].gc+=m.ga;st[m.h].n++;st[m.a].gf+=m.ga;st[m.a].gc+=m.gh;st[m.a].n++});
    ALL.forEach(t=>{G+=st[t.c].gf;N+=st[t.c].n});const avg=G/N,K=12,A=c=>(st[c].gf+K*avg)/(st[c].n+K)/avg,D=c=>(st[c].gc+K*avg)/(st[c].n+K)/avg,lh=avg*1.1*A(h)*D(a),la=avg*.9*A(a)*D(h),pH=pwin(lh,la),pD=pdraw(lh,la);return[pH,pD,1-pH-pD]};
  const pE=(f,h,a)=>{const R=eloRun(f).R;let G=0,N=0;ALL.forEach(t=>{G+=t.apGF;N+=16});M.filter(m=>m.f<f).forEach(m=>{G+=m.gh+m.ga;N+=2});const[lh,la]=lamElo(R[h]+EL.HFA-R[a],2*G/N),pH=pwin(lh,la),pD=pdraw(lh,la);return[pH,pD,1-pH-pD]};
  const pB=f=>{const c=[1,1,1];M.filter(m=>m.f<f).forEach(m=>c[oc(m.gh,m.ga)]++);const s=c[0]+c[1]+c[2];return c.map(v=>v/s)};
  const R2={goles:[0,0],elo:[0,0],base:[0,0]};let n=0;
  for(const m of M.filter(m=>m.f>=7)){const y=oc(m.gh,m.ga);n++;for(const[k,p]of[['goles',pG(m.f,m.h,m.a)],['elo',pE(m.f,m.h,m.a)],['base',pB(m.f)]]){R2[k][0]+=-Math.log(Math.max(1e-6,p[y]));R2[k][1]+=p.indexOf(Math.max(...p))===y?1:0}}
  log(true,'backtest fechas 7-12 ('+n+' partidos): '+Object.keys(R2).map(k=>k+' log-loss '+(R2[k][0]/n).toFixed(4)+' aciertos '+R2[k][1]).join(' | '));
  return out}.toString()+')()',ctx);
console.log(lines.join('\n'));
if(lines.some(l=>l.startsWith('FALLA')))process.exit(1);

```

#### `tests/ui.py`

Prueba de humo en navegador real (Playwright).

```python
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
    ok(pg.input_value('#fSel')=='12','fecha por defecto = proxima fecha con partidos sin jugar (12)')
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
    pg.select_option('#selModel','elo');pg.wait_for_timeout(2200)
    ok('Elo' in pg.evaluate("document.querySelector('#PROB .ph').textContent") and pg.evaluate("document.querySelectorAll('#ELO tbody tr').length")>=30,'cambio a modelo Elo: probabilidades y ranking Elo (30 filas)')
    pg.select_option('#selModel','goles');pg.wait_for_timeout(1500)
    pg.select_option('#selEq',label='Estudiantes (RC)');pg.wait_for_timeout(2500)
    ok(pg.evaluate("document.querySelectorAll('#needOut td').length")>0 and '>-<' not in pg.evaluate("document.getElementById('needOut').innerHTML"),'cuadro de victorias necesarias sin guiones')
    for w,h in [(1184,909),(1366,768),(1920,1080)]:
        q=b.new_page(viewport={'width':w,'height':h});q.goto(URL);q.wait_for_timeout(700)
        ok(all((q.select_option('#fSel',f),q.wait_for_timeout(100),q.evaluate(FIT))[2]<=1 for f in ('11','12')),f'{w}x{h}: la fecha entra sin scroll en la columna de partidos')
    m=b.new_page(viewport={'width':390,'height':800});m.goto(URL);m.wait_for_timeout(900)
    ok(not m.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"),'celular (390px): sin desborde horizontal')
    ok(not errs,'sin errores en consola '+str(errs[:3]))
    b.close()
sys.exit(1 if fallas else 0)

```

---

## 2. STACK Y EJECUCIÓN

### 2.1 Stack

| Pieza | Detalle |
|---|---|
| App | **HTML + CSS + JavaScript vanilla en un solo archivo.** Sin frameworks, sin librerías, sin CDN, sin servidor, sin peticiones de red. Todos los datos están incrustados. |
| Datos / herramientas | **Python 3.10+** (solo `datos/build.py`, biblioteca estándar). |
| Verificación de datos y motor | **Node.js** (LTS) con el módulo `vm` incluido; sin dependencias npm. |
| Prueba en navegador | **Python + Playwright** (`pip install playwright`, `python -m playwright install chromium`). |
| Persistencia | `localStorage` del navegador, clave `simulador-clausura-2026-v1` (solo guarda los resultados que el usuario simula en partidos sin resultado oficial). |

### 2.2 Comandos (PowerShell, desde la carpeta del proyecto)

```powershell
cd C:\Users\Usuario\proyectos\calculadora-clausura-2026

# Abrir la app en el navegador (no hace falta instalar nada)
start .\calculadora-clausura-2026.html

# Instalaciones por única vez
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
pip install playwright
python -m playwright install chromium

# Controles (deben dar todo OK)
$env:PYTHONIOENCODING='utf-8'
node tests\verificar.js
python tests\ui.py

# Datos del Elo: validar fuentes / regenerar ELO_EXTRA dentro del HTML
python datos\build.py
python datos\build.py --write
```

### 2.3 Estado actual (12/10/2026)

**Funciona (verificado con los tests de abajo):**
- 16 fechas con el fixture oficial; una fecha por vez, flechas y selector; arranca en la próxima fecha con partidos sin resultado oficial (hoy la 12). Fecha 6 mostrada como "fecha interzonal".
- Resultados oficiales cargados al 11/10/2026: fechas 1-10 completas (150), fecha 11 (14 de 15), fecha 12 (8 de 15). Quedan 68 partidos sin resultado de las fechas 11-16.
- Tablas Zona A, Zona B, Anual (Pts, PJ, F:C, DG) y Promedios (Prom., Pts, PJ), todas recalculadas al cargar resultados simulados.
- Regla de descenso de la AFA (si un equipo es último en anual y en promedios, baja por promedios y el otro descenso es el anteúltimo de la anual) y cupos a copas con Belgrano ya clasificado por título.
- Probabilidades por Monte Carlo (10.000 simulaciones) con dos modelos de fuerza seleccionables: Goles (por defecto) y Elo (en prueba), más el ranking Elo.
- Cuadro "¿Cuántas victorias necesita tu equipo?" con escenarios forzados, sin celdas vacías.
- Goles validados (enteros 0-15), simulaciones guardadas en el navegador, etiquetas accesibles, diseño de escritorio que entra sin scroll y diseño de celular.

**A medio hacer:**
- **El Elo no tiene todos los partidos que pidió el usuario.** Cargados: fase de grupos de la liga 2025 (Apertura y Clausura) y Apertura 2026, fase de grupos de Libertadores y Sudamericana 2025 y 2026 de los equipos argentinos (864 partidos) y el Clausura 2026. Faltan los playoffs de la liga, Copa Argentina, eliminatorias de copas internacionales, Recopa, etc. (ver sección 4.A). Por eso el modelo por defecto sigue siendo Goles.
- **Resultados al día:** la app no se actualiza sola; hay partidos pendientes que ya pueden haberse jugado (ver 2.5).
- **Publicación:** no está publicada; faltan dominio y datos de publicación (sección 4.D).

**Resultado de los controles al armar este documento:**

`python datos\build.py`
```
Apertura 2025 partidos: 240 | equipos: 30 | desajustes: ninguno
Clausura 2025 partidos: 240 | equipos: 30 | desajustes: ninguno
Apertura 2026 partidos: 240 | equipos: 30 | desajustes: ninguno
Copas (grupos Libertadores/Sudamericana 2025-2026): 144 partidos | desajustes: ninguno
ELO_EXTRA: 864 partidos | 10329 caracteres | desde 2025-01-23 hasta 2026-05-27
coincide con lo que ya tiene el HTML: True
```

`node tests\verificar.js`
```
OK     16 fechas x 15 partidos, cada equipo juega una vez por fecha
OK     210 cruces de la misma zona exactamente una vez
OK     cada equipo juega exactamente 2 interzonales (la fecha 6 es toda interzonal)
OK     Apertura: goles a favor = goles en contra
OK     resultados de las fechas 1-10 reproducen PJ/Pts/GF/GC de las 30 filas base 
OK     30 equipos con codigo unico y colores de escudo
OK     estado tras la fecha 11 (las fechas 12 en adelante se ignoran): 30 filas coinciden con la tabla publicada 
OK     resultados oficiales cargados en fechas 11-16: 22 | pendientes: 68 | fecha por defecto: 12
OK     ELO_EXTRA tiene 864 partidos (esperado 864)
OK     Elo: top5 BOC 1595, ROS 1589, IRI 1578, RIV 1560, VEL 1553 | ultimos PLA 1387, ALD 1334, ERC 1300
OK     Elo: rivales fijos EXT=1427 BR=1578 LOW=1150
OK     simulacion (modelo goles): sumas ca=1 po=16 lib=4 sud=6 da=1 dp=1
OK     simulacion (modelo Elo): mismas sumas
OK     Belgrano (campeon Apertura) = 100% Libertadores y 0% Sudamericana por la anual
OK     ningun equipo desciende dos veces (regla AFA)
OK     backtest fechas 7-12 (82 partidos): goles log-loss 1.0185 aciertos 40 | elo log-loss 1.0144 aciertos 42 | base log-loss 1.0983 aciertos 34
```

`python tests\ui.py`
```
OK     fecha por defecto = proxima fecha con partidos sin jugar (12)
OK     todas las cajas de goles tienen etiqueta accesible
OK     99 se corrige a 15
OK     el signo menos se descarta
OK     las letras se descartan
OK     lo simulado se guarda al recargar (localStorage)
OK     Borrar resultados limpia lo guardado
OK     fecha 6: aviso de fecha interzonal y sin bordes dorados
OK     cambio a modelo Elo: probabilidades y ranking Elo (30 filas)
OK     cuadro de victorias necesarias sin guiones
OK     1184x909: la fecha entra sin scroll en la columna de partidos
OK     1366x768: la fecha entra sin scroll en la columna de partidos
OK     1920x1080: la fecha entra sin scroll en la columna de partidos
OK     celular (390px): sin desborde horizontal
OK     sin errores en consola []
```

### 2.4 Mapa del código de la app (`calculadora-clausura-2026.html`)

Un solo `<script>` al final. Contratos de datos (no cambiar el formato sin actualizar todo el código y los tests):

| Constante | Contenido |
|---|---|
| `ZA`, `ZB` | Zona A / Zona B. Cada fila: `[codigo, nombre, apPts, apGF, apGC, clPJ, clPts, clGF, clGC, h24, h25, pjHist]`. `ap*` = Apertura 2026 completo; `cl*` = Clausura 2026 **estado tras la fecha 10** (base fija); `h24`/`h25` = puntos de 2024 y 2025; `pjHist` = partidos de 2024+2025 en Primera. |
| `COL` | Colores de camiseta por equipo (para el escudo ilustrado). |
| `PAST_RAW` | Resultados de las fechas 1-10 del Clausura: `{fecha: "LOC-VIS gl-gv,..."}`. Solo se muestran: ya están sumados en `ZA`/`ZB`. |
| `RAW` | Fechas 11-16: `"LOC-VIS"` si falta jugar, `"LOC-VIS gl-gv"` si ya hay resultado oficial (se bloquea en la interfaz). |
| `SCH` | Día y hora de los partidos: `{"LOC-VIS": ["Vie 09/10","19:30"]}` (la hora solo se muestra mientras está pendiente). `POSTP` = partidos postergados (no cuentan para elegir la "próxima fecha"). |
| `ELO_EXTRA` | Cadena `"LOC-VIS gl-gv,..."` en orden cronológico con partidos anteriores al Clausura 2026. Los rivales extranjeros se escriben `EXT` (no brasileño), `BR` (brasileño) o `LOW` (división inferior). Se genera con `datos/build.py`. |
| `EL` | Parámetros del Elo (K, ventaja de local, puestos de referencia). |
| `KEYS`, `CL` | Columnas de probabilidades: `ca` campeón anual, `po` playoffs, `lib` Libertadores, `sud` Sudamericana, `da` descenso por anual, `dp` descenso por promedios. |

Funciones clave: `proj(t)` (tabla de un equipo con todos los resultados cargados), `zone/anual/prom` (tablas), `setup()` (fuerzas y partidos pendientes), `simulate(M, equipo, k)` (Monte Carlo; con `equipo` y `k` fuerza que gane exactamente `k`), `probs()`, `renderNeed()/drawNeed()`, `eloRun()`, `lamElo()`, `fixture()`, `sc()`, `save()/load()`.

### 2.5 Receta: cargar resultados nuevos

1. Conseguir el resultado en **una fuente confiable** (captura de Promiedos del usuario, futbolargentino.com, ligaprofesional.ar, La Nación) y, si se puede, **comprobarlo con la tabla publicada** (puntos, PJ, goles).
2. En `RAW`, agregar ` gl-gv` al partido (ejemplo: `SLO-DRI` pasa a `SLO-DRI 1-0`). El partido queda bloqueado y suma en las tablas.
3. Si cambió un día u horario, ajustar `SCH`. Si un partido se posterga, ponerlo en `POSTP`.
4. Actualizar la fecha de "al 11/10/2026" / "hasta el 11/10/2026" en los textos de la pestaña de datos y la pregunta frecuente (buscar `11/10/2026` en el HTML).
5. Correr `node tests\verificar.js` y `python tests\ui.py`. Ojo: `verificar.js` tiene una comparación contra la tabla del 11/10 (estado tras la fecha 11); sigue válida porque ignora las fechas 12 en adelante.
6. **Partidos pendientes conocidos al 11/10 00:08:** fecha 11: Sarmiento–River (miércoles 14/10, 19:00). Fecha 12: San Lorenzo–Riestra (dom 14:45), Platense–Argentinos (17:00), Rosario Central–Independiente Rivadavia (17:00), Racing–Belgrano (19:15), Talleres–Independiente (21:30), Lanús–Vélez (lun 16:00), Gimnasia (M)–Newell's (lun 18:30). Las fechas 13-16 no tienen día ni hora cargados.

---

## 3. DECISIONES TOMADAS (y por qué)

### 3.1 Producto y diseño
1. **Un solo archivo HTML sin dependencias.** Para abrirlo con doble clic, hospedarlo gratis en cualquier lado, incrustarlo (iframe) en otra web y mostrarlo como demo. No migrar a un framework ni agregar librerías o CDN sin una razón fuerte.
2. **Estética tipo Promiedos solo como estilo** (verde oscuro, paneles, fila con estado a la izquierda). No se usa ni se debe usar código, logo, escudos ni datos de Promiedos (derechos de autor y términos de uso). Los escudos son insignias dibujadas con los colores del club. El nombre "SIMULADOR" es provisorio.
3. **Una sola página, sin pestañas**: columna izquierda con una fecha por vez y columna derecha con las tablas apiladas; barra de accesos fija arriba. En escritorio la columna de partidos se ajusta al alto de la pantalla (sin scroll propio; con menos de 760 px de alto vuelve el scroll). En celular, una columna.
4. **Resultados oficiales bloqueados**, lo simulado se guarda en el navegador y "Borrar resultados" solo borra lo simulado. Goles: enteros de 0 a 15.
5. **Fecha 6**: es toda interzonal (15 de 15). No se marcan 15 bordes dorados; se muestra un aviso. En las demás fechas el borde dorado marca el único interzonal.
6. **Columnas pedidas por el usuario:** zonas y anual con Pts, PJ, F:C, DG; promedios solo Prom., Pts, PJ; todos los porcentajes con el símbolo `%`; en probabilidades "Copas" se renombró **Sudam.** y "1° zona" se reemplazó por **Campeón anual**.
7. **Cuadro de victorias necesarias:** nunca debe mostrar guiones. Por eso cada fila se calcula forzando esa cantidad de victorias y simulando el resto, en vez de filtrar simulaciones.
8. **"% de campeón del Clausura" NO se muestra** porque depende de los playoffs, que no están modelados. "Campeón anual" es otra cosa (1° de la tabla anual = Campeón de Liga).

### 3.2 Reglas de la liga implementadas (con la fuente que se usó)
- **Formato:** 2 zonas de 15; 16 fechas = 14 de zona + 2 interzonales (la fecha 6 completa y el clásico/interzonal de los equipos libres en cada fecha); clasifican los 8 primeros de cada zona. Fuente: ligaprofesional.ar y medios; comprobado por estructura (210 cruces de zona exactamente una vez, 2 interzonales por equipo).
- **Tabla anual** = Apertura + Clausura. **Promedios** = puntos 2024 + 2025 + 2026 sobre partidos jugados en Primera.
- **Descenso:** dos equipos, el peor promedio y el último de la anual. **Si es el mismo equipo, baja por promedios y el segundo descenso es el anteúltimo de la anual** (no el siguiente peor promedio). Hoy pasa con Estudiantes (RC) y Aldosivi. Fuentes: El Economista y El Intransigente; conviene confirmarlo con el reglamento oficial.
- **Copas 2027:** Libertadores = campeones del Apertura (Belgrano), del Clausura y de la Copa Argentina + los 3 mejores de la anual sin cupo por título; Sudamericana = los 6 siguientes de la anual sin contar a quienes ya tienen lugar. **Belgrano no ocupa cupo de la anual** (100% Libertadores). Las fuentes se contradicen porque el reglamento cambió durante 2026: confirmar con el reglamento oficial. **Los campeones del Clausura y de la Copa Argentina todavía no se descuentan.**
- **Desempates implementados:** puntos, diferencia de gol, goles a favor. El reglamento sigue con resultado entre sí y fair play (no implementados). En un empate por descenso el reglamento prevé partido desempate (no modelado).

### 3.3 Modelos de simulación
- **Monte Carlo de 10.000 simulaciones** de los partidos sin resultado; goles con distribución de Poisson; con debounce de 350 ms al cargar resultados.
- **Modelo Goles (por defecto):** ataque y defensa = goles por partido del Apertura y del Clausura (con **todos** los resultados cargados) con regresión a la media (K=12); local ×1,1 y visitante ×0,9.
- **Modelo Elo (en prueba):** K=20; ventaja de local +70; multiplicador por diferencia de goles (1 si ≤1; 1,5 si 2; (11+d)/8 si ≥3); todos arrancan en 1500 en enero de 2025 y se procesa cronológicamente. **Reglas pedidas por el usuario:** se cuentan todos los partidos de la temporada pasada y la actual de todos los torneos, **sin amistosos**; ganar a un equipo de otro país (menos Brasil) suma como ganar a uno de puestos bajos pero no muy bajos (puesto 22 de la tabla Elo de los 30 actuales); ganar a un brasileño suma como ganar a uno de puestos muy altos (puesto 3); ganar a una división inferior suma lo mínimo (último de la tabla − 150); perder resta al revés (poco contra fuertes, mucho contra débiles; lo da la fórmula de Elo). Los rivales virtuales (`EXT`, `BR`, `LOW`) no cambian de puntaje. Los equipos que aparecen por primera vez (descendidos, ascendidos) entran en el nivel del puesto 22.
- **Elo → goles:** por bisección se buscan los goles esperados que mantienen la probabilidad de ganar/empatar del Elo (total de goles = 2 × promedio de goles por equipo y partido).
- **Orden cronológico del Elo:** Apertura 2025 con fechas reales (openfootball); Clausura 2025 = espejo del Apertura 2025 con localía invertida; Apertura 2026 con 4 días por fecha (la fecha 9 el 2/5/2026) tomando la fecha de su espejo del Clausura 2026; copas con la fecha por jornada deducida de los potes (2025: 2/4, 9/4, 23/4, 7/5, 14/5, 28/5; 2026: 8/4, 15/4, 29/4, 6/5, 20/5, 27/5). Son aproximaciones y solo importan para el orden.
- **El modelo por defecto sigue siendo Goles** hasta que el Elo tenga todos los datos. Comparación en las fechas 7-12 (82 partidos, cada uno predicho solo con lo anterior): error (log-loss) Goles 1,0185 / Elo 1,0144 / frecuencias base 1,0983; aciertos 40 / 42 / 34. La diferencia es chica y ruidosa: no afirmar que uno es mejor.
- **Victorias necesarias:** el equipo gana exactamente `k` de sus partidos pendientes; el subconjunto de partidos ganados se sortea con las probabilidades reales de cada partido y los resultados se muestrean condicionados (ganó / no ganó). 2.500 simulaciones por fila. La columna "Escenario" es la probabilidad exacta de ganar `k`.

### 3.4 Datos y fuentes
- **Base:** `ZA`/`ZB` con el Clausura 2026 tras la fecha 10, tomado de futbolargentino.com y verificado luego contra bolavip (30 filas coinciden).
- **Fechas 1-10 del Clausura (150 partidos):** 127 de futbolargentino.com y ligaprofesional.ar; **23 de las fechas 1-3 se calcularon cruzando los totales de cada equipo (la solución es única)**. Todo el conjunto reproduce exactamente PJ, Pts, GF y GC de los 30 equipos.
- **Elo:** Apertura 2025 de openfootball (240 partidos); Clausura 2025 y Apertura 2026 de las matrices de resultados de en.wikipedia.org más las dos fechas interzonales de cada torneo; grupos de copas de las tablas de grupo de en.wikipedia.org. **Cada torneo se validó contra las tablas finales (puntos, goles a favor y en contra de los 30 equipos, 16 partidos cada uno)** y los puntos de 2025 contra la columna `h25`.
- **Fuentes poco confiables:** exclusiva.com.ar tuvo errores (por ejemplo, "Defensa 0-3 San Lorenzo" y "Huracán 3-2 Aldosivi"; los correctos son 3-0 y 1-0). Wikipedia en inglés **no sirve para resultados de partidos sueltos** de cuadros o copas porque el texto extraído pierde los marcadores (solo sirven las matrices y tablas).
- **Promedios:** `h24`, `h25` y `pjHist` se verificaron solo para Estudiantes (RC) y Aldosivi contra publicaciones y por coincidencia con las tablas; conviene contrastarlos con la tabla oficial de promedios.
- **Códigos de equipo (3 letras):** `BOC, CCO, DYJ, DRI, EST, GEM (Gimnasia Mendoza), IND, INS, LAN, NOB, PLA, SLO, TAL, UNI, VEL, ALD, ARG, ATU, BAN, BAR, BEL, ERC (Estudiantes Río Cuarto), GLP (Gimnasia La Plata), HUR, IRI, RAC, RIV, ROS, SAR, TIG`; en datos de 2025 también `GOD` (Godoy Cruz) y `SMA` (San Martín de San Juan). Wikipedia usa `GME` para Gimnasia (M): `build.py` lo convierte.

### 3.5 Cosas que el nuevo agente NO debería hacer
- No hacer scraping ni copiar código, logos o datos de Promiedos.
- No pasar la app a un framework, ni agregar CDN, ni sacar el archivo único sin acordarlo con el usuario.
- No cambiar los formatos de datos (sección 2.4) ni la clave de `localStorage` sin migrar.
- No modificar reglas de descenso o de copas sin una fuente oficial.
- No mostrar "% de campeón del Clausura" sin modelar los playoffs.
- No inventar resultados ni completar datos de memoria; verificar contra tablas.
- No poner claves de API en el HTML ni en archivos del proyecto.
- No enviar el código fuente a terceros al contactar a un medio; mostrar una demo publicada.

---

## 4. PENDIENTES

### A. Datos del Elo que faltan (pedido explícito del usuario: toda la temporada pasada y la actual, liga y copas)
- Playoffs de la liga: Apertura 2025, Clausura 2025 y Apertura 2026 (unos 45 partidos; solo se conocen las finales: Platense 1-0 Huracán, Estudiantes 1-1 Racing (5-4 por penales), Belgrano 3-2 River).
- Copa Argentina 2025 y 2026 (rivales de divisiones inferiores = token `LOW`).
- Eliminatorias previas y fases finales de Libertadores y Sudamericana 2025 y 2026 de los equipos argentinos (rivales brasileños = `BR`, otros = `EXT`).
- Recopa Sudamericana, Trofeo de Campeones / Supercopa, Mundial de Clubes 2025 (Boca y River).
- **Obstáculo:** el texto que se extrae de Wikipedia pierde los marcadores de los cuadros. Alternativas: abrir las páginas con el **navegador real** de Hermes (worldfootball.net, fbref.com, 365scores, sitios de cada torneo) o una API de fútbol. Validar siempre contra tablas o resúmenes por equipo. Agregar los partidos en `datos/cups.py`/`datos/mats.py` o como nuevos bloques de `build.py` y regenerar con `python datos\build.py --write`.
- Cuando estén completos: reevaluar el backtest y decidir si el Elo pasa a ser el modelo por defecto; ajustar parámetros (K, ventaja de local, puestos de referencia).

### B. Modelo y reglas
- Descontar los cupos de los campeones del Clausura y de la Copa Argentina (idea: selectores de "qué pasa si gana X" para ambos).
- Modelar playoffs para poder dar "% de campeón del Clausura".
- Confirmar con el reglamento oficial: cupos a copas 2027 y desempate por descenso (partido extra).
- Desempates oficiales completos (resultado entre sí, fair play).
- Ventaja de local fija para todos los equipos; efecto de equipos argentinos que ganen copas internacionales de este año.

### C. Actualización de resultados
- Cargar los partidos pendientes (sección 2.5, punto 6) y los horarios de las fechas 13-16.
- **Actualizador automático:** mover los datos a un `datos.json` y generar ese archivo con un script programado. Fuentes candidatas: API-Football (plan gratis de 100 pedidos por día; hay que comprobar que incluya la temporada actual de Argentina) o Highlightly (100 pedidos por día). Una sola consulta puede traer todos los partidos de la temporada. Hosting y tareas programadas gratuitas posibles con GitHub Pages y GitHub Actions. football-data.org no sirve (su plan gratuito no cubre Argentina). Siempre validar contra las tablas antes de publicar.

### D. Publicación
- Reemplazar `https://TU-DOMINIO.com/` en dos lugares del `<head>` (`canonical` y `og:url`); agregar favicon, imagen para compartir (`og:image`), política de privacidad, cookies y contacto.
- Hay un comentario "Google AdSense" en el `<head>` para pegar el código cuando aprueben la cuenta. AdSense y varios servicios piden mayoría de edad: el usuario es estudiante de secundaria, así que las cuentas y cobros deben abrirse con un adulto responsable.
- Analítica simple; revisar los términos de uso de cualquier API de datos antes de uso comercial.

### E. Bugs y límites conocidos
- La columna de partidos puede tener 1 px de diferencia por redondeo en algunas alturas de pantalla (se oculta el desborde); con menos de 760 px de alto aparece scroll.
- El cálculo tarda unos 0,15 s en una PC y unos 0,7 s con CPU 4 veces más lenta (celular medio), y bloquea la pantalla mientras corre: pasarlo a un Web Worker.
- No se probó en Safari/iOS, ni con lector de pantalla, ni a fondo con teclado.
- Los horarios de la fecha 12 están escritos a mano en `SCH`.
- `h24`/`h25`/`pjHist` sin contrastar para todos los equipos (ver 3.4).
- El orden cronológico del Elo usa fechas aproximadas (ver 3.3).

### F. Ideas a futuro
- **Multi-liga:** separar datos y reglas por liga en archivos JSON (zonas, cupos, descensos, desempates) para vender o mostrar la herramienta en otras ligas.
- **Propuesta comercial:** primero publicar una demo con fecha visible y algo de tráfico; después contactar a Promiedos y a otros medios. No mandar el código fuente; un NDA rara vez funciona en un primer contacto; tener un plan B (monetizar directamente).

---

## 5. SERVICIOS EXTERNOS

- **En ejecución la app no usa ningún servicio, API ni cuenta**: no hay variables de entorno ni claves en el código.
- **Cuentas creadas hasta ahora:** ninguna para este proyecto.
- **Fuentes consultadas a mano** (sin cuenta ni clave): futbolargentino.com, bolavip.com, ligaprofesional.ar, lanacion.com.ar, es/en.wikipedia.org, `openfootball/south-america` en GitHub (datos abiertos), medios deportivos, y capturas de Promiedos del propio usuario.
- **Variables que se podrían necesitar más adelante** (propuestas de nombre, todavía no existen): `API_FOOTBALL_KEY` o `HIGHLIGHTLY_API_KEY` (actualizador de resultados). Las claves de Hermes Agent (`NVIDIA_API_KEY`, `OPENROUTER_API_KEY`) son del agente, no del proyecto. Nunca escribir sus valores en archivos del proyecto ni en capturas.

---

## Resumen para el usuario

Tu simulador del Clausura 2026 quedó funcionando en un solo archivo que podés abrir con doble clic. Muestra los partidos de una fecha por vez con flechitas, las tablas de las dos zonas, la anual y los promedios, y calcula las probabilidades de clasificar, de ir a copas y de descender, con las reglas del descenso y de las copas que revisamos. También te dice cuántas victorias necesita cada equipo. Cargué todos los resultados hasta el 11/10 y los comprobé contra las tablas publicadas. El Elo funciona, pero todavía le faltan partidos que pediste: los playoffs, la Copa Argentina y las eliminatorias de las copas internacionales, así que por ahora el modelo principal sigue siendo el de goles. Lo primero que tiene que hacer el agente nuevo es cargar los resultados que se jugaron desde el 11/10 y correr los dos controles para ver que todo siga en verde. Después, lo más importante es conseguir los partidos que faltan para el Elo, y más adelante publicar la página con un adulto a cargo de las cuentas.
