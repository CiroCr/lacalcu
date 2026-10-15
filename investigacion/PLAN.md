# PLAN — Completar los partidos que faltan para el Elo (HANDOFF §4.A)

Fecha: 12/10/2026. Este archivo es la guía de integración para cuando vuelva la data de los subagentes.

## Ya está cargado en ELO_EXTRA (864 partidos) — NO duplicar
- Fase regular: Apertura 2025, Clausura 2025, Apertura 2026, Clausura 2026 (hasta fecha 12).
- Fase de GRUPOS de Libertadores y Sudamericana 2025 y 2026 (equipos argentinos), en `datos/cups.py`.

## Falta recolectar (olas de subagentes → investigacion/*.json)
| Archivo | Contenido | Estado |
|---|---|---|
| `playoffs-apertura-2025.json` | Playoffs Apertura 2025 | ✅ LISTO 12/10 noche: 15 partidos, validado OK. Final HUR 0-1 PLA (1-0, cancha neutral) |
| `playoffs-clausura-2025.json` | Playoffs Clausura 2025 | ✅ LISTO 12/10 noche: 15 partidos, validado OK. Final RAC 1-1 EST (5-4 pen.) |
| `playoffs-apertura-2026.json` | Playoffs Apertura 2026 | ✅ LISTO 12/10 noche: 15 partidos, validado OK. Final RIV 2-3 BEL. OJO: semifinal ARG-BEL penales 4-3 según LPF/ESPN (Transfermarkt dice 4-5, confirmar) |
| `copa-argentina-2025.json` | CA 2025 completa | 🔄 RELANZADO 14/10 ~18:45 EN 2 MITADES (deleg_106048a0): copa-argentina-2025-a.json (32avos/16avos/octavos) + copa-argentina-2025-b.json (cuartos/semis/final). El intento de archivo único falló por límite de tokens de razonamiento. ANCLA: final ganó IRI ante ARG (~abril-mayo 2026) |
| `copa-argentina-2026.json` | CA 2026 en curso | ✅ LISTO 14/10: 59 partidos (32avos 32, 16avos 15, octavos 8, cuartos 4). Semis (ATU-PLA 28/10, BAN-BOC 14/11) y final (2/12) pendientes. Discrepancias resueltas: UNI-Agropecuario 2-0; GEM-GyT penales 3-4; BAN-San Martín (T) 5-4 pen. IRI-ATU: ganó ATU 3-2 pen (ancla corregida) |
| `conmebol-2025.json` | Lib+Sud 2025 eliminatorias | ✅ LISTO 14/10: 33 partidos (Lib 18: fase previa, octavos, cuartos, semifinal RAC-FLA; Sud 15: repechaje CCO, octavos, cuartos, semifinal, final LAN 0-0 AMI **campeón LAN 5-4 pen**). ANCLA CORREGIDA: Lib 2025 la ganó Flamengo 1-0 a Palmeiras (no Botafogo, eso fue 2024). ⚠️ IND-U. de Chile octavos: SUSPENDIDO 1-1 al inicio del 2T, Conmebol descalificó a IND — NO cargarlo al Elo (marcador parcial) |
| `conmebol-2026.json` | Lib+Sud 2026 eliminatorias | ✅ LISTO 14/10: 29 partidos (fase previa 2, repechaje Sud 6, octavos 14, cuartos 6, semifinal BOC 0-1 Vasco 13/10). Semis EST-FLA 15/10 aún no jugada. Discrepancia resuelta: ARG-Barcelona penales 4-5 (ESPN tenía 5-4 invertido) |
| `otros-torneos.json` | Mundial Clubes, Recopas, Trofeo/Supercopa | ✅ LISTO 14/10: 16 partidos. Mundial: BOC 2-2 Benfica, 1-2 Bayern, 1-1 Auckland; RIV 3-1 Urawa, 0-0 Monterrey, 0-2 Inter. Recopa 2025: RAC campeón 4-0 global a Botafogo; Recopa 2026: LAN campeón 4-2 global a Flamengo (confirma Sud 2025 = LAN). Trofeos: TdC 2024 (21/12/2024 — FUERA de ventana Elo), Supercopas Int. 2023/2024/2025, Supercopa Arg 2024, TdC 2025. ⚠️ VEL-EST 21/12/2024 fuera de ventana; Supercopa Arg 2025 EST-IRI programada 11/11/2026 (pendiente) |

## ESTADO AL 14/10/2026 (noche, cierre) — ELO ÚNICO + ESCUDOS EN CURSO
1. **✅ Elo = modelo único y predeterminado.** Se eliminó el selector de modelos del HTML; MODEL='elo' fijo; sin menciones de "en prueba". Textos de "al 12/10" → "al 14/10". Tests verdes: verificar.js (la tabla de referencia ahora es post-SAR-RIV: SAR [17,11,18,17], RIV [14,11,14,13]) y ui.py 15 OK (sin el paso del selector eliminado). Backtest 90 partidos: goles 1.0233/44 vs elo 1.0145/46 vs base 1.0938/38.
2. **✅ SAR-RIV cargado:** Sarmiento 1-1 River (Contrera 14', Montiel 26'ST; gol previo de Montiel anulado por VAR). Fecha 11 COMPLETA: 30 resultados oficiales, 60 pendientes, fecha por defecto 13. POSTP quedó vacío.
3. **🔄 Escudos reales (pedido del usuario 14/10 noche):** 20 de 30 descargados en investigacion/escudos/ — lotes A y C completos (manifest-a.json y manifest-c.json con URL/fuente/licencia). FALTA LOTE B: SLO, DRI, PLA, TAL, CCO, ARG, ROS, GLP, BEL, HUR (el recolector se frenó cuando el usuario se fue; relanzar tal cual estaba el prompt del lote B en el historial). Integración pendiente: incrustar como data-URI/base64 en el HTML único (decisión del archivo único sin red), controlando el peso total.
   - **Tip para el relanzamiento del lote B** (del intento frenado): NO parsear el wikitexto del infobox (los primeros 5 clubes no exponen parámetro `escudo` y la API tiró 429 por ráfaga). Usar la API de MediaWiki prop `pageimages` (imagen original de la infobox) como hizo el lote A con éxito, con pausas entre pedidos para evitar el rate-limit. El lote A también bajó el render a 500px cuando el original pesaba demasiado (caso BOC: 16 MB → 125 KB).
   - Verificación extra que hizo el lote C (recomendable repetir en B): renderizar cada SVG en navegador y confirmar visualmente el club (colores/monogramas), además de la firma de archivo.
   - ALD.svg es fair use de en.wiki (no hay escudo de Aldosivi en Commons ni Wikipedia ES) — anotado en manifest-c.json. BAN.png es CC BY-SA 3.0; INS.png CC BY-SA 4.0; el resto dominio público salvo lo que digan los manifests.
4. Próximos partidos: fecha 13 desde el sáb 17/10 (4 horarios ya en SCH); CONMEBOL 2026 octavos en curso (EST-FLA 15/10); CA 2026 semis 28/10 y 14/11; Supercopa Arg 2025 EST-IRI 11/11.
5. Todo lo del punto anterior (ELO 1106, knockouts.py, etc.) sigue vigente.
   - **Copa Argentina 2026:** el cuadro estaba casi completo; faltan resolver 3 discrepancias: (a) Unión–Agropecuario 2-0 vs 2-1; (b) penales Gimnasia Mza–Gimnasia y Tiro 3-4 vs 6-5; (c) **IRI–ATU del 16/9: el ganador contradice el ejemplo que les di** — el texto de ESPN ("Ind. Rivadavia 1-1 Atl. Tucumán, Gana 3-2 en tiros de penal | Atlético Tucumán") es ambiguo y sugiere que **Atlético Tucumán** ganó la tanda, no Ind. Rivadavia. Verificar bien antes de cargar (mundoascenso también tiene este partido).
   - **CONMEBOL 2025:** el recolector ya tenía el cuadro completo de ambos torneos desde el wikitexto de Wikipedia con enlaces oficiales CONMEBOL por partido; solo faltaba verificar anclas y fechas de Boca–Alianza Lima. El transcript está en C:\Users\Usuario\AppData\Local\hermes\cache\delegation\live\deleg_95b3f52b\task-5.log (revisar si todavía existe).
   - **Otros torneos:** faltaba verificar si el Trofeo de Campeones 2024 se jugó en 2025 (entraría en la ventana del Elo). Transcript: task-7.log.
   - **Copa Argentina 2025:** transcript en task-3.log.

## Reglas de la data (todos los JSON)
- `gl/gv` = marcador al final de los 90 o 120 minutos. NUNCA plegar penales al marcador. `penL/penV` van aparte.
- Tokens: equipo de Primera 2026 o GOD/SMA → su código de 3 letras; brasileño → `BR`; extranjero no brasileño → `EXT`; argentino de divisiones inferiores → `LOW`. `nombreL/nombreV` siempre con el nombre real.
- Solo partidos con ≥1 equipo argentino (de los 30 actuales, GOD o SMA). Sin amistosos.
- Mínimo 1 fuente seria por partido (ideal 2) + coherencia con el cuadro; URLs en `fuentes`.
- **Decisión adoptada (estándar ClubElo, avisar al usuario):** definiciones por penales cuentan como EMPATE en el Elo; el marcador de 120' es el que se carga. Si el usuario quiere otra convención, la data (penL/penV) ya está para recalcular.

## Integración (cuando la data esté)
1. Validar cada JSON contra el cruce ESPN + cuadros; resolver `dudas` con búsquedas propias.
2. Crear `datos/knockouts.py` con los partidos validados (mismo estilo que `cups.py`: fecha real, tokens EXT/BR/LOW) y que `build.py` los agregue a `rows` (tier 3, se ordenan por fecha sola).
3. `python datos/build.py` → ver consistencia; `python datos/build.py --write` → reinyecta ELO_EXTRA.
4. **Actualizar `tests/verificar.js`:** el test espera `ELO_EXTRA.length===864`; cambiarlo al total nuevo.
5. **Actualizar el texto del panel Elo en el HTML** (leyenda que hoy dice "fase de grupos de la liga 2025... más los del Clausura 2026") con las categorías nuevas.
6. Correr `node tests/verificar.js` y `python tests/ui.py` (todo verde).
7. Re-evaluar el backtest (goles vs Elo vs base) y decidir con el usuario si el Elo pasa a ser el modelo por defecto (HANDOFF: solo cuando estén todos los datos).

## Códigos de equipo
Zona A: VEL Vélez Sarsfield · DYJ Defensa y Justicia · GEM Gimnasia y Esgrima (M) · INS Instituto · BOC Boca Juniors · UNI Unión · NOB Newell's Old Boys · IND Independiente · EST Estudiantes (LP) · LAN Lanús · SLO San Lorenzo · DRI Deportivo Riestra · PLA Platense · TAL Talleres (C) · CCO Central Córdoba (SdE)
Zona B: ARG Argentinos Juniors · ROS Rosario Central · GLP Gimnasia y Esgrima (LP) · BEL Belgrano · HUR Huracán · SAR Sarmiento (J) · IRI Independiente Rivadavia · ATU Atlético Tucumán · RIV River Plate · BAR Barracas Central · BAN Banfield · RAC Racing · ERC Estudiantes (RC) · ALD Aldosivi · TIG Tigre
Extras 2025: GOD Godoy Cruz · SMA San Martín (SJ)
