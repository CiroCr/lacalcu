# PLAN — La calcu del fútbol argentino (Clausura 2026)

Estado al 20/10/2026 noche (2). HANDOFF.md = reglas base. Este archivo = estado + pendientes. Abajo, reglas de data vigentes.

## BUG PENDIENTE (diagnosticado, NO arreglar sin pedir) — asimetria del header del partido
El usuario ve el header del partido asimetrico y tiene razon (medido en 1428px):
- Equipos OK: 432px de aire a cada lado.
- PERO minuto (mmin) y marcador (mscore) quedan **22px a la izquierda** del centro real
  (score.cx=691 vs mhead.cx=713). Causa: .mteam tiene min-width:120px pero el nombre derecho
  ("Atlético Tucumán") mide 164px vs 120px del izquierdo; flex centra el GRUPO entero,
  no el marcador. Fix sugerido: .mteam{flex:1} en los dos lados con max-width, o
  posicionar .mscorewrap absoluto al centro, o grids `grid-template-columns:1fr auto 1fr`.
- Revisar tambien si pasa en partidos con nombres de distinto largo en general (caso tipico).

## TAREA SIGUIENTE: adaptación de resoluciones
**Que se vea bien en cualquier dispositivo.**
- Probar: móvil 360-414px, tablet 768-834px, laptop 1280-1440px, monitor 1920px+, pantallas de poca altura (1366x768).
- Base existente: `@media(max-width:760px)` (una columna, tabs scrolleables) y `@media(min-width:761px)` (app fija, dos columnas). Fixture y tablas de zonas ya usan flex nativo.
- Puntos sospechosos: (1) app fija en pantallas horizontales cortas (1366x768); (2) las 8 tablas del panel de partido en móvil (grid 1 col, larguísimas); (3) gráfico "¿Cuánto necesita?" + panel lateral en pantallas angostas; (4) inputs de goles táctiles (touch target mínimo 44px); (5) matchview (partido como página) en vertical.
- ui.py ya prueba 390px sin desborde + 3 viewports desktop; agregar tablet si se toca algo.

## ESTADO DEL PROYECTO (19/10 noche)
- Nombre: **La calcu del fútbol argentino** — title, og, JSON-LD, favicon, logo "LA CALCU" verde con ARGENTINO SVG calibrado (franjas 6/6/5px, sol centrado, glow celeste, gap 11px).
- Resultados: fechas 1-13 completas (NOB-CCO 1-0, SAR-BAR 1-1 y DRI-UNI entraron solos vía LIVE al terminar, lunes 19/10 21:15).
- **Módulo EN VIVO v2** (commit 5d477f6): ESPN cada 60s; LIVEIN guarda {gh,ga,min}; celda = solo "ET" (uso argentino); inputs readOnly; badges .lv en zonas/anual/promedios (verde/amarillo/rojo estilo promiedos); resetAll restaura el vivo desde LIVEIN; auto-carga al 'post' solo si venía en vivo. Tests 16+16 OK.
- Partidos de fechas viejas: bloqueo LIVEF-2 (al terminar la 13, la 11 queda fuera sola).
- Layout desktop: app fija sin page-scroll; tablas de zonas estiradas al alto exacto de la columna de partidos (dif 0, flex nativo); anual/prom/prob/elo scrollean su panel; fixture con filas flex (nada cortado).
- Teclado: gol -> foco al rival (solo si vacío; 700ms tras escribir "1"); Enter -> siguiente; flechas -> navegar.
- Accesibilidad: 180 alt de escudos, roles ARIA tabs/tabpanels, aria-label en inputs, contraste verificado.
- Legal/seguridad: Términos y Legal completos (modales); CSP estricta; 0 secretos (verificado git history); 0 recursos externos salvo el fetch ESPN.
- Git: todo commiteado (último 5d477f6). Repo LOCAL, sin push.

## PENDIENTES DE DATA
- EST-FLA vuelta semifinal Libertadores: **jueves 22/10 Maracaná** -> investigacion/conmebol-2026.json + python datos/build.py --write + contador en tests/verificar.js (hoy 1107).
- Copa Argentina 2026: semis ATU-PLA 28/10 y BAN-BOC 14/11, final 2/12 -> ídem.
- Supercopa Argentina 2025: EST-IRI 11/11/2026 -> otros-torneos.json.
- Fecha 16: horarios sin confirmar (cruces sí).

## IDEAS FUTURAS (charlado, sin prioridad)
- Publicar en GitHub Pages (repo listo; el LIVE completo solo funciona servido).
- API oficial (api-sports.io free, 100 req/día) + cron nocturno Hermes para históricos; GitHub Actions como evolución.

---

# REGLAS DE LA DATA (vigentes)

## Reglas de la data (todos los JSON)
- gl/gv = marcador al final de los 90 o 120 minutos. NUNCA plegar penales al marcador. penL/penV van aparte.
- Tokens: equipo de Primera 2026 o GOD/SMA -> su código de 3 letras; brasileño -> BR; extranjero no brasileño -> EXT; argentino de divisiones inferiores -> LOW. nombreL/nombreV siempre con el nombre real.
- Solo partidos con >=1 equipo argentino (de los 30 actuales, GOD o SMA). Sin amistosos.
- Mínimo 1 fuente seria por partido (ideal 2) + coherencia con el cuadro; URLs en "fuentes".
- Definiciones por penales cuentan como EMPATE en el Elo (estándar ClubElo); marcador de 120' es el que se carga.

## Elo: pipeline para agregar partidos
1. Agregar el partido al JSON de investigacion/ (fecha, torneo, ronda, local, visitante, gl, gv, penL/penV, nombreL/nombreV, fuentes, dudas).
2. Actualizar el contador esperado en datos/knockouts.py (FILES).
3. python datos/knockouts.py (anclas) -> python datos/build.py -> python datos/build.py --write (reinyecta ELO_EXTRA en el HTML).
4. Actualizar número en tests/verificar.js (ELO_EXTRA.length===1107).
5. node tests/verificar.js + python tests/ui.py -> verde -> commit.

## Códigos de equipo
Zona A: VEL Vélez Sarsfield · DYJ Defensa y Justicia · GEM Gimnasia y Esgrima (M) · INS Instituto · BOC Boca Juniors · UNI Unión · NOB Newell's Old Boys · IND Independiente · EST Estudiantes (LP) · LAN Lanús · SLO San Lorenzo · DRI Deportivo Riestra · PLA Platense · TAL Talleres (C) · CCO Central Córdoba (SdE)
Zona B: ARG Argentinos Juniors · ROS Rosario Central · GLP Gimnasia y Esgrima (LP) · BEL Belgrano · HUR Huracán · SAR Sarmiento (J) · IRI Independiente Rivadavia · ATU Atlético Tucumán · RIV River Plate · BAR Barracas Central · BAN Banfield · RAC Racing · ERC Estudiantes (RC) · ALD Aldosivi · TIG Tigre
Extras 2025: GOD Godoy Cruz · SMA San Martín (SJ)
ESPN ids (LIVE, ver ESPN2COD en el HTML): 9739 ALD, 3 ARG, 9785 ATU, 235 BAN, 10060 BAR, 4 BEL, 5 BOC, 11989 CCO, 8950 DYJ, 17702 DRI, 8 EST, 19685 ERC, 11972 GEM, 9 GLP, 10 HUR, 11 IND, 9744 IRI, 2975 INS, 12 LAN, 14 NOB, 7764 PLA, 15 RAC, 16 RIV, 17 ROS, 18 SLO, 10158 SAR, 19 TAL, 7767 TIG, 20 UNI, 21 VEL.

## Escudos (30/30 embebidos base64)
Manifests con URL/licencia en investigacion/escudos/. ALD.svg fair use de en.wiki; BAN.png CC BY-SA 3.0; INS.png CC BY-SA 4.0; resto dominio público salvo lo que digan los manifests. Verificación visual al cambiarlos (renderizar SVG y confirmar club por colores/monograma).

## Anclas de finales (para validar data)
- Apertura 2025: HUR 0-1 PLA (campeón Platense).
- Clausura 2025: RAC 1-1 EST (Estudiantes campeón 5-4 pen.).
- Copa Argentina 2025: IRI-ARG (IRI campeón 5-3 pen.).
- Apertura 2026: RIV 2-3 BEL (campeón Belgrano).
