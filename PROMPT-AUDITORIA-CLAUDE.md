# Prompt para Claude — Auditoría pre-publicación de "La calcu del fútbol argentino"

> CÓMO USARLO: la página es UN solo archivo HTML (1,3 MB) con todo embebido
> (HTML + CSS + JS + datos del torneo). La forma más fácil es abrir
> claude.ai, adjuntar el archivo `calculadora-clausura-2026.html` y pegar
> este prompt. Si usás Claude Code, corrélo desde la carpeta del proyecto
> y pegá el prompt igual (él solo leerá los archivos).
> El archivo está en: C:\Users\Usuario\proyectos\calculadora-clausura-2026\

---

Sos un auditor senior de aplicaciones web. Te adjunto **el proyecto completo** de mi página "La calcu del fútbol argentino" — un simulador del Clausura 2026 de la Liga Profesional argentina que está TERMINADO y funciona, pero que aún no está publicado. Necesito dos cosas de vos, en este orden:

## PARTE 1 — Diagnóstico pre-publicación

Auditá el archivo adjunto como si fueras a ponerlo en producción mañana. Buscá problemas REALES, no cosméticos. Especialmente:

### 1. Errores y bugs latentes
- Bugs de JavaScript que no hayan explotado todavía (condiciones de borde, estados raros: ¿qué pasa si ESPN cambia su API? ¿si el localStorage tiene datos viejos de otra versión? ¿si se abre con un hash/URL inválida?)
- Errores en la lógica de datos (RAW de fechas, cálculo de puntos, promedios, Elo)
- Problemas de accesibilidad que falten (la página ya tiene roles ARIA, aria-labels, contraste verificado — decime si falta algo importante)

### 2. Problemas de rendimiento y tamaño
- El archivo pesa 1,3 MB con ~1100 partidos embebidos para el cálculo Elo y 180 escudos como SVG/data-URI. ¿Es razonable? ¿El parseo inicial puede ser lento en celulares? ¿Cómo reducirlo sin reescribir todo?
- Las simulaciones de probabilidades corren 10.000 iteraciones en el navegador. ¿Puede congelar celulares viejos? ¿Conviene moverlas a un Web Worker?

### 3. Riesgos legales y de contenido
- Uso escudos de clubes obtenidos de Wikipedia/Wikimedia. ¿Riesgo real en Argentina? ¿Cómo protegerse (atribución, disclaimer, algo más)?
- Uso el endpoint público de ESPN (site.api.espn.com, sin API key) para resultados en vivo cada 60 segundos. ¿Pueden bloquearme por CORS, rate-limit o términos de servicio? ¿Alternativas (api-sports free tier, otra fuente abierta)?
- Uso nombres de equipos y datos del torneo sin autorización de la AFA/LPF. La página ya dice "herramienta independiente, no afiliada". ¿Alcanza?
- Términos, política de privacidad y aviso legal ya existen como modales. ¿Falta algo exigido en Argentina (Ley 25.326, AAIP, arca de "Datos personales"?) si no registro usuarios ni uso cookies?

### 4. Seguridad
- La CSP ya es estricta (default-src 'none', connect-src 'self' + ESPN, sin recursos externos, sin cookies, sin formularios que envíen datos). Revisá si quedó algún vector que no vi.
- localStorage guarda solo resultados simulados del usuario. ¿Algo más que deba sanitizar?

### 5. SEO y descubrimiento
- La página es una sola URL sin routing real (usa ?m=N con pushState para partidos). ¿Cómo indexa esto Google? ¿Conviene URLs reales? ¿Sitemap? ¿Los JSON-LD que ya tiene alcanzan?
- og:url apunta a "TU-DOMINIO.com" como placeholder — avisame todo lo que haya que cambiar al publicar.

## PARTE 2 — Guía de publicación paso a paso

Después del diagnóstico, dame un plan CONCRETO para publicar. Mi contexto:

- **Es un archivo estático único** (HTML + un demo-live.json de prueba): no hay build, no hay backend, no hay base de datos. Todo corre en el navegador del visitante.
- Cuento con: PC con Windows, git instalado (repo local con 55 commits, SIN remote todavía), y quiero que sea **gratis**.
- Requisitos: HTTPS (necesario para que no me bloqueen el fetch a ESPN en algunos navegadores), dominio simple, que el módulo EN VIVO funciente (hoy solo funciona si la página se sirve por http/https — abierta con file:// el CORS lo bloquea).
- La página está en español rioplatense, apunta a usuarios argentinos.

Dame para cada opción: pasos exactos, ventajas/desventajas, y qué tocar del código:

1. **GitHub Pages** (mi candidato natural): crear el repo, qué va y qué NO va al repo (¿excluyo tests/ y datos/ con .gitignore? ¿el .json de demo?), cómo activar Pages, dominio gratis usuario.github.io
2. **Netlify / Cloudflare Pages / Vercel**: ¿vale la pena la diferencia? Drag-and-drop vs git
3. **Dominio propio**: dónde comprar barato en Argentina (.com.ar requiere CUIT y trámite ante nic.ar; .com en Namecheap/Cloudflare), cómo apuntarlo al hosting elegido
4. Checklist final pre-publicación: title/description/og definitivos, favicon, Google Search Console, analítica sin cookies (Plausible self-hosted ¿o nada?), qué hacer con el modo demo (?demo=1) — ¿lo dejo público o lo quito?

Al final, dame: (a) una lista PRIORIZADA de los problemas encontrados con severidad [crítico/medio/bajo], (b) el plan de publicación recomendado en no más de 10 pasos, y (c) qué le agregarías a esta app como próximas features si crece (mi idea: cron nocturno que cargue los resultados oficiales del día al HTML).

Sé directo: si algo que hice está mal, decilo sin vueltas; si está bien, no lo adornes.
