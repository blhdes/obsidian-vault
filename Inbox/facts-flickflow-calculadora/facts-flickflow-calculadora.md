---
title: f*acts — Prueba Técnica Flickflow (Calculadora)
date: 2026-09-16
tags: [career, job-search, technical-test, flickflow, facts]
---

# f*acts — Prueba técnica: Calculadora Flickflow

Nota índice de este mini-proyecto. Vive en `Inbox/` de forma temporal — se moverá a
`Projects/` o se archivará/eliminará cuando la prueba termine.

## Contexto

**f*acts** (madebyfacts.com) es una agencia. Su fundador, **Lucas M. Suárez**, contactó
en frío el 2026-09-16 sobre un cliente suyo, **Flickflow** (herramientas de análisis
para traders, en español) — primer contacto entrante real desde que se abrió el
outreach, no viene de nuestra lista de empresas contactadas. Ver
[[Projects/Portfolio/Job-Search/Job-Search|Job-Search]] para el estado general de la
búsqueda.

## El encargo

Integrar una calculadora ya funcional (position sizing para futuros) como una página
real dentro del marketing site de Flickflow, en el menú **Recursos → Calculadora**,
respetando el sistema de diseño existente del sitio.

- **Repo:** `flickflow-lab/flickflow-marketing-site` (privado, invitación aceptada)
- **Rama de la prueba:** `prueba-tecnica-calculadora`
- **Archivo de partida:** `prueba-tecnica/calculadora-posicion-futuros.html` (la lógica
  de cálculo ya está completa ahí dentro, no se toca)
- **Entregable:** un PR de vuelta a `prueba-tecnica-calculadora`, con el trabajo hecho
  en una rama aparte (regla explícita de Lucas en su PD)
- **Plazo:** sin fecha fijada por él ("lo que te lleve"). Autoimpuesto: **~2026-09-23**
  (una semana desde el encargo)

## Estado

- [x] Repo clonado en `/Users/agomezu/Claude/flickflow-marketing-site`
- [x] Exploración del sistema de diseño y la arquitectura del sitio — ver
  [[brief-tecnico]]
- [x] Decisiones de integración confirmadas con el usuario (2026-09-16) — ver
  [[brief-tecnico]]
- [x] Servidor local levantado (`npm install && npm run dev`), verificado en Safari
- [x] **Primera pasada** — `src/pages/calculadora.astro`: traducción literal de la
  calculadora original a los tokens/clases del sitio, entrada de nav añadida
  (`src/data/home.ts`, icono placeholder `bolt`), sección de referencia de
  componentes debajo de una línea divisoria
- [x] **Página de referencia dev** — `public/dev/calculadora-original.html`, copia
  byte a byte del archivo original de la prueba, servida sin tocar en
  `/dev/calculadora-original.html`, para comparar en directo durante el rediseño
- [ ] **Segunda pasada** — rediseño de interacción de la calculadora apoyado en la
  sección de referencia de componentes. Dirección en
  [[segunda-pasada-diseno|segunda-pasada-diseno.md]]
  - [x] Bug corregido: los toggles Compra/Venta y Abajo/Arriba en estado activo
    (fondo claro) dejaban el texto ilegible — `text-text-muted` (pensado para
    fondo oscuro) se quedaba puesto a la vez que `text-text-inverse`, compitiendo
    por la cascada. Arreglado con un helper `setSegActive()` que intercambia los
    dos pares de clases (fondo + texto) en bloque, nunca uno solo
  - [x] **Sandbox de progresión creado** — `src/pages/dev/calculadora-redesign.astro`
    (`/dev/calculadora-redesign`), enlazado desde `/calculadora` justo debajo del
    link a la original. Ids con prefijo `v1-`, `v2-`... para apilar versiones sin
    colisión; cada versión nueva se añade arriba, las anteriores se conservan
    debajo para comparar
  - [x] **Versión 1** construida: full-bleed, columna única (Cuenta+Riesgo y
    Tick+Valor de tick comparten fila para ahorrar alto, pero sigue siendo lectura
    vertical), resultado al final. Defaults como `placeholder` + `numField()` que
    calcula con el placeholder mientras no se escriba nada. Sembrado del spinner
    vía flechas de teclado (fiable) + heurística de clic en los últimos ~20px del
    campo (**pendiente de confirmar que se sostiene en Safari real**). Ficha del
    contrato en un SpecTable con borde propio. Headings h3/h4 en vez de líneas.
    **Sin resolver todavía:** si el objetivo "sin scroll" se sostiene en pantallas
    bajas — no se fuerza `overflow:hidden` a propósito, para poder ver un
    desbordamiento en vez de que se recorte en silencio
  - [x] v1 revisada por el usuario en Safari; iterada hasta la versión final
- [x] **Versión final en `/calculadora`** (2026-09-22). La empresa preguntó cómo iba
  y el usuario decidió pulir y entregar ya. La v1 pasa a `src/pages/calculadora.astro`,
  sin sección de componentes ni enlaces de desarrollo. Cambios respecto a la v1:
  - `Section` del sitio (como el 404), con los raíles verticales de su retícula.
  - Info View en móvil justo bajo el panel tocado (opción a); en escritorio,
    hueco reservado de 72px (el texto más largo mide 65px).
  - Script inline con `data-astro-rerun` y escuchas globales cortadas al salir:
    sin eso, al volver a la página sin recargar (ClientRouter) llegaba vacía.
  - `<label for>` en cada campo y títulos de grupo como `h2` bajo el `h1`.
  - `/calculadora` añadida al sitemap (`src/pages/sitemap.xml.ts`).
  - Verificado en Chrome headless: escritorio 1476×825 cabe sin scroll en los
    tres modos; tablet 1024×768 cabe en modo normal (en Personalizado/Perpetuo
    el texto del Info View queda 30-50px por debajo); móvil sin desbordamiento;
    ida y vuelta sin recargar sin errores. `npm run build` pasa.
- [x] **Riesgo en % o en dólares** (idea del usuario, 2026-09-22): selector
  compacto `% | $` dentro de la fila, con la pastilla deslizante. Al cambiar de
  unidad, lo escrito se convierte para que el riesgo no cambie (2 % de 25.000 $ →
  500 $). En $, el ejemplo sigue a la cuenta (el 1 %) y la nota muestra el % que
  equivale. Si el riesgo supera el capital, se calcula con el 100 % y la nota avisa
  en naranja, sin reescribir lo tecleado; aplica a los dos modos (antes un 150 % no
  avisaba). El aviso de redondeo habla en la unidad elegida. Texto del Info View
  actualizado aquí y en [[teoria-financiera-calculadora]]. Verificado en Chrome
  headless; la fila mide lo mismo que las demás del panel (margen negativo en el
  selector). A 320px de ancho la etiqueta pasa a dos líneas, sin desbordar.
- [x] **Icono del menú:** `calculator` de Lucide (lucide-static 1.47.0, ISC),
  geometría tomada del SVG oficial y pasada a un solo trazo en `icons.ts`.
- [x] **Fundido del Info View**, rehecho el 2026-09-22 porque al pasar de un hover
  a otro los efectos se solapaban (dos fundidos independientes, panel y texto,
  con temporizadores propios). Ahora es una sola animación cada vez (Web
  Animations API) en fases que no se pisan: aparecer (sube 6px, 300ms), cambiar
  de campo (baja a 0 en 110ms, cambia el texto, sube en 180ms), desaparecer (solo
  opacidad, 180ms). El texto solo cambia con el panel invisible; en una ráfaga de
  campos se muestra el último. Espera de 160ms antes de ocultarse. Verificado en
  tiempo real controlando Chrome por su protocolo de depuración (el reloj
  simulado del modo headless no avanza animaciones): todos los cambios de texto
  a opacidad 0, nunca más de una animación a la vez, en escritorio y móvil.
  - **Segunda corrección, solo Safari (2026-09-22):** el usuario seguía viendo
    choque entre el bloque saliente y el entrante, con el texto "más blanco". En
    Chrome no se reproduce (hover con ratón real vía CDP, carga directa y
    navegación sin recarga: un solo panel, un solo script, cambios a opacidad 0).
    Causas WebKit conocidas y corregidas: (1) destello del valor final, porque la
    opacidad de base se fijaba al final antes de que arrancara la animación; ahora
    la base queda en el punto de partida y el final se fija al terminar, con
    `fill: 'forwards'`; (2) cambio de suavizado del texto al entrar y salir de su
    capa de composición; ahora el panel está siempre en su propia capa
    (`will-change`, `translateZ(0)`), como el blur del header del sitio.
    **Pendiente: confirmación del usuario en Safari.**
- [x] **Avisos integrados con el sistema** (2026-09-22). Revisión previa: el sitio no
  tiene componente de alerta; sí tokens de estado (`info`, `danger`, `success` y sus
  `-subtle`, sin usar) y la regla "naranja = acción de marca, turquesa = el sistema
  te señala algo". Los avisos de la calculadora estaban en naranja: error corregido.
  El usuario eligió 3 opciones:
  - **Avisos en línea con chapa de icono** (`icon-chip` tintada): turquesa (info)
    para redondeo hacia arriba y riesgo por encima del capital; rojo (danger) para
    la liquidación antes del stop. Texto en blanco, color solo en la chapa. Iconos
    `info` y `alert` de Lucide (1.47.0, ISC) añadidos a `icons.ts`.
  - **El "—" explica por qué:** cuenta a 0, riesgo a 0, entrada a 0 (perpetuo),
    stop igual a la entrada, tick sin definir.
  - **Aviso legal** bajo la ficha: el mismo `footer.disclaimer` del sitio.
  - Descartados: marcar el panel del resultado (el sistema pide contención) y los
    diálogos (su propio criterio: nada de avisos flotantes).
  - Verificado en Chrome headless: todos los casos, colores de chapa e icono
    correctos, sin desbordamiento en móvil, todo cabe en escritorio.
- [x] **Revisión de código antes del PR** (2026-09-22, skill `/code-review` +
  verificación propia). 7 hallazgos, todos confirmados en el código:
  - Míos, corregidos: (2) la heurística del ratón en las flechas del campo
    convertía el ejemplo en texto al hacer clic en el borde derecho → quitada, se
    ocultan las flechas nativas y el sembrado queda solo con teclado; (3) la
    distancia pasaba a valor real aunque saliera de un stop de ejemplo → un
    derivado solo es real si todo lo que lo forma está escrito; (6) el "exacto"
    redondeaba (2,996 → "3,00" junto a un 2) → se trunca; (7) el Info View no se
    recolocaba al cruzar el breakpoint → se recoloca.
  - Heredados del original, corregidos: (4) al cambiar la entrada se perdía la
    distancia escrita → se respeta lo que rellenó el trader (stop o distancia);
    (5) apalancamiento 0 daba un aviso de liquidación falso → pide un valor > 0.
  - Encontrado al probar: la dirección se deducía del stop de ejemplo (del
    Nasdaq), y con otro activo daba la vuelta sola → solo se deduce de un stop
    escrito.
  - (1) Contratos en € comparados con un riesgo en $ sin convertir (heredado).
    **Decisión del usuario (opción 2):** la cuenta y el riesgo van en la divisa del
    contrato. Con DAX o Euro Stoxx 50, el sufijo de la cuenta, el botón de importe
    del riesgo (con su `aria-label`), las notas y los avisos pasan a €; en el resto,
    $. Sin tipo de cambio. El modo del riesgo pasa de `usd` a `importe` en el
    código. Info View de cuenta y riesgo reescritos (siguen en 2 líneas) y
    sincronizados con [[teoria-financiera-calculadora]]. Verificado en headless.
  - Limpiezas: una sola comprobación de validez (la del motivo del "—"), los
    contratos se calculan una vez, fuera `rpc` (sin uso). Repaso de comentarios:
    mapa de lectura arriba y un comentario por decisión, no por línea.
  - Verificado en Chrome (headless y en tiempo real vía CDP): todos los casos,
    fundido del Info View, ida y vuelta sin recargar, sin errores. Build pasa.
- [x] **Entregado (2026-09-23).** Rama `calculadora-recursos` (commit `9b43e9c`,
  4 archivos: `calculadora.astro`, `home.ts`, `sitemap.xml.ts`, `icons.ts`) y
  **PR #7** hacia `prueba-tecnica-calculadora`:
  https://github.com/flickflow-lab/flickflow-marketing-site/pull/7
  - Siguen sin commitear, a propósito: `package-lock.json`, `README.md`,
    `public/dev/`, `src/pages/dev/`.
- [~] Crear la rama de trabajo, commitear (hecho, ver arriba)
  - Rama: `calculadora-recursos` (el repo usa nombres en español sin prefijo)
  - Van al commit: `src/pages/calculadora.astro`, `src/data/home.ts`,
    `src/pages/sitemap.xml.ts`, `src/components/ui/icons.ts`
  - No van: `package-lock.json` (solo lo tocó `npm install`), `README.md`,
    `public/dev/`, `src/pages/dev/`
- [ ] Abrir el PR a `prueba-tecnica-calculadora`

## Antes de commitear: qué NO va al PR

Dos archivos viven sin trackear en el repo, solo para nuestro uso durante el
desarrollo — hay que acordarse de dejarlos fuera del `git add`:

- `README.md` (raíz del repo) — chuleta local de arranque/testing
- `public/dev/calculadora-original.html` — copia de referencia de la calculadora
  original, sin procesar
- `src/pages/dev/calculadora-redesign.astro` — sandbox de progresión del rediseño

La sección "solo referencia interna" dentro de `calculadora.astro` (los componentes
de muestra bajo la línea divisoria) también hay que retirarla antes del PR — esa sí
está dentro del archivo que sí se commitea, así que requiere una edición, no solo
dejarla fuera del `git add`.

## Notas relacionadas

- [[brief-tecnico|Brief técnico]] — lo que hemos encontrado en el repo + las decisiones
  de integración
- [[ideas-fuera-de-alcance|Ideas fuera de alcance]] — cosas que no forman parte de la
  prueba pero podrían valer la pena más adelante
- [[segunda-pasada-diseno|Segunda pasada — dirección de diseño]] — apuntes del
  usuario (2026-09-17) para el rediseño de interacción: full-bleed sin scroll,
  columna única, defaults como placeholder, SpecTable real, headings en vez de
  líneas
- [[stack-y-filesystem|Stack y filesystem]] — el stack explicado con más detalle y una
  guía carpeta por carpeta / archivo por archivo de cómo se relaciona todo en el repo
- [[teoria-financiera-calculadora|Teoría financiera de la calculadora]] — qué calcula
  exactamente la calculadora (tamaño de posición, ticks, apalancamiento, liquidación...),
  explicado desde cero
