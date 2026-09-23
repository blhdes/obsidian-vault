---
title: Stack y filesystem — Calculadora Flickflow
date: 2026-09-16
tags: [career, technical-test, flickflow, facts, astro]
---

# Stack y filesystem — Calculadora Flickflow

Ver [[facts-flickflow-calculadora|índice del proyecto]] y [[brief-tecnico|brief técnico]] para
el contexto general. Esta nota amplía el apartado "El sitio" del brief: qué hace cada pieza del
stack y, sobre todo, cómo se relaciona todo en el filesystem real del repo — una guía para poder
mirar cualquier carpeta y saber para qué sirve.

## El stack, pieza a pieza

- **Astro 5** — el framework del sitio. Es un generador de sitio **estático** (SSG, *Static Site
  Generation*): en vez de tener un servidor que responde a cada visita calculando la página al
  vuelo, Astro genera todo el HTML/CSS/JS de antemano (`npm run build`) y eso es lo que se sirve.
  Más rápido y más simple de alojar, a cambio de que el contenido no cambia hasta el siguiente
  build.
- **React 19** — solo está como integración de Astro (`@astrojs/react`), preparado por si algún
  componente necesitara interactividad compleja ("isla" de React dentro de una página, si no
  bastara con JavaScript normal). Hoy el sitio es casi todo Astro puro: no hemos visto ningún
  componente `.tsx` usándose de verdad.
- **Tailwind v4** — clases de utilidad para el CSS (`bg-...`, `text-...`, `flex`, etc.), cargado
  vía `@tailwindcss/vite`. Diferencia importante frente a Tailwind v3: **no hay** un
  `tailwind.config.js` clásico. La v4 se configura directamente en CSS con `@theme inline` (lo
  hace `global.css`, ver más abajo).
- **Keystatic** — el "backoffice" de contenido, o sea, el panel donde alguien sin tocar código
  puede editar los textos de las páginas de producto. Va en modo `storage: local`, que significa
  que no hay ningún servidor externo ni base de datos: Keystatic simplemente **edita los archivos
  JSON del repo** a través de una interfaz web. Solo se monta en desarrollo (`/keystatic`); en el
  build de producción ni siquiera se incluye.
- **TypeScript estricto** (`astro/tsconfigs/strict`) — con un alias de import `@/*` que apunta a
  `src/*` (definido en `tsconfig.json`), así que cualquier `import ... from '@/components/...'`
  que veas en el código es en realidad `src/components/...`.

## ¿Dónde está el "back"?

Este proyecto no tiene un backend en el sentido clásico (servidor + API + base de datos
respondiendo peticiones en vivo). El "back" aquí son dos cosas distintas:

1. **Build time**: cuando se ejecuta `astro build`, Astro lee todo el contenido (los JSON de
   `content/products/`, los datos de `src/data/home.ts`) y genera las páginas HTML finales. Una
   vez generado, no hay nada "corriendo" en el servidor — es solo archivos estáticos.
2. **Keystatic en dev**: es el único momento en que hace falta un servidor Node
   (`@astrojs/node`, en modo `standalone`) corriendo de verdad, y solo para servir el panel de
   edición y guardar los cambios como archivos JSON.

No hay base de datos, ni endpoints de API salvo `sitemap.xml.ts` (que genera el mapa del sitio
para buscadores).

## Guía de carpetas y archivos

- **`astro.config.mjs`** — configuración raíz: activa React y Tailwind, y monta Keystatic *solo*
  si `NODE_ENV !== 'production'`.
- **`keystatic.config.ts`** — define el "formulario" del backoffice: una colección `products`,
  con un campo por cada sección que existe en la plantilla de producto (`hero`, `overview`,
  `features`, `examples`, `comparison`, `faq`, `cta`) más `visibleSections`, que decide qué
  secciones se muestran en cada página. Este schema es un espejo casi 1:1 de lo que consume
  `src/pages/[product].astro`.
- **`content/products/*.json`** — el contenido real de cada página de producto (`calendar.json`,
  `canvas.json`, `charts.json`, `journal.json`, `mcp.json`), editable desde Keystatic o a mano.
  Cada archivo es exactamente el objeto que recibe la plantilla de producto.
- **`src/pages/`** — las rutas del sitio:
  - `index.astro` → la home.
  - `[product].astro` → ruta **dinámica**: una única plantilla sirve *todas* las páginas de
    producto. `getStaticPaths()` recorre `content/products/*.json` con `import.meta.glob` y
    convierte cada JSON en una ruta real (`/charts`, `/calendar`, etc.).
  - `404.astro` → página de error.
  - `sitemap.xml.ts` → el único endpoint que no devuelve HTML.
- **`src/layouts/BaseLayout.astro`** — el `<html>` completo de cada página: `<head>` (meta tags,
  Open Graph, datos estructurados JSON-LD de la empresa), el `ClientRouter` de Astro (navegación
  entre páginas sin recarga completa), el fondo de luz (`ShaderBackground`, con su gama de color
  configurable), y el `Header` + `Footer` envolviendo el `<slot />` (el hueco donde entra el
  contenido de cada página concreta).
- **`src/components/site/`** — cabecera, pie y navegación: `Header.astro`, `Footer.astro`,
  `MegaMenu.astro` (el menú desplegable "Producto"/"Recursos", cuyo contenido sale de
  `src/data/home.ts`), `ToolsDialog.astro` (el popup "ver todas las herramientas"), y el logotipo
  (`BrandMark.astro`, `Logo.astro`, `brandPaths.js` — los trazos reales de la marca).
- **`src/components/sections/`** — los bloques grandes de la home (`Hero`, `Faq`, `Stats`,
  `Tools`, `Canvas`, `Install`, `Integrations`, `Principles`, `Commitments`, `FinalCta`,
  `TrustBar`). Son componentes "tontos": cada uno pinta la porción de `src/data/home.ts` que le
  corresponde, sin lógica de negocio propia.
- **`src/components/product/`** — piezas específicas de la plantilla de producto:
  `ProductComparison.astro` (la tabla comparativa) y `ProductExamplesTabs.astro` (las pestañas de
  ejemplos con el MCP).
- **`src/components/ui/`** — el sistema de diseño reutilizable: `Button`, `Panel`, `Cell`,
  `Cells`, `Section`, `SectionHeader`, `Badge`, `Tabs`, `SpecTable`, `Stat`, `Icon` (+
  `icons.ts`, el catálogo propio de iconos, trazo simple, `viewBox 24×24`), `Accordion`,
  `Dialog`/`Modal`, `ShaderBackground` + `shaderPalettes.ts` (las gamas de color por producto:
  `brand`/`cool`/`gold`/`neutral`), `AuraFrame`, `LogoMarquee`, `ProductFrame`, `Terminal`,
  `Testimonial`, `ToolCard`, `Container`.
- **`src/data/home.ts`** — todo el texto y contenido estructurado de la home vive aquí, fuera de
  los componentes (`nav`, `hero`, `trust`, `tools`, `features`, `useCases`, `canvas`,
  `commitments`, `integrations`, `principles`, `finalCta`, `faq`, `footer`). Es el patrón
  "contenido separado de la plantilla" — cambiar un texto de la home no toca ningún `.astro`.
- **`src/styles/tokens.css`** — la única fuente de verdad visual, en dos capas:
  - **Primitivas** (`--p-*`) → valores crudos de color y tipografía, sacados del brandbook. Es lo
    único que se tocaría si cambiara la identidad de marca.
  - **Semánticas** (`--ff-*`) → el significado (`--ff-text`, `--ff-accent`, `--ff-radius-md`...).
    Los componentes usan **solo** estas, nunca una primitiva directa — regla dura del proyecto:
    nunca `bg-[#fff]` ni `text-slate-600`, solo utilidades del tema.
  - Tema oscuro por defecto (fondo negro puro); tema claro opcional con `data-theme="light"` en
    el `<html>`; acento por producto con `data-accent="brand|cool|gold|neutral"` (lo fija
    `BaseLayout` según la prop `shader` de cada página, para que cada herramienta se reconozca
    por su color antes de leer el titular).
- **`src/styles/global.css`** — el puente entre `tokens.css` y Tailwind v4 (`@theme inline`) más
  utilidades globales.
- **`src/styles/fonts.css`** — carga Inter (variable, vía `@fontsource`) como tipografía de
  cuerpo, y Safiro como tipografía de marca para titulares — aunque de momento faltan los
  archivos `.woff2` reales de Safiro, así que cae a Inter mientras tanto.
- **`public/`** — estáticos servidos tal cual, sin procesar: iconos, favicons, fuentes `.woff2`,
  vídeos de producto (referenciados desde `content/products/*.json`), logos de marca
  (`logos/`) y logos de fuentes de datos (`logos/sources/` — CoinGecko, TradingView, FRED, etc.,
  usados en la barra de confianza/integraciones).
- **`scripts/brand-assets.mjs`** — genera assets de marca derivados (como `og.png`). Herramienta
  de build, no se ejecuta en producción ni en el navegador.
- **`prueba-tecnica/calculadora-posicion-futuros.html`** — el entregable de la prueba técnica: un
  HTML independiente (**no integrado en Astro todavía**), con toda su lógica en un único
  `<script>` inline. Es el punto de partida a "vestir" con el sistema de componentes de arriba —
  ver [[teoria-financiera-calculadora|qué calcula exactamente]].
- **`README.md`** — el que añadimos nosotros para orientarnos durante la prueba (no es el README
  real del proyecto, es un documento local de trabajo).

## El flujo completo, con un ejemplo real: `/charts`

Para entender cómo se conecta todo, sigue el camino de una sola página, de principio a fin:

1. **`content/products/charts.json`** contiene el contenido de la página: título, descripción,
   features, FAQ...
2. **`keystatic.config.ts`** define el "molde" (schema) que ese JSON debe cumplir — es lo que ve
   quien edita desde el panel de Keystatic.
3. **`src/pages/[product].astro`** lee el JSON (vía `getStaticPaths()` + `import.meta.glob`) y lo
   convierte en la ruta `/charts`. Dentro, decide qué secciones pintar según `visibleSections`.
4. **`src/layouts/BaseLayout.astro`** envuelve toda la página: head, fondo de luz, header, footer.
5. Los componentes de **`src/components/ui/`** (`Section`, `Cell`, `Accordion`...) pintan cada
   sección con el contenido recibido.
6. **`src/styles/tokens.css`** da la forma y el color final a todo eso — sin tokens, los
   componentes no tendrían ni radios ni colores definidos.

Ese es el "back → front" real de este proyecto: no hay una petición HTTP a una API en el momento
de la visita, sino una cadena de transformación que ocurre **en build time**, del JSON al HTML
final.

## Dónde encajaría la calculadora

La prueba consiste en repetir un camino parecido al de arriba, pero para la calculadora: convertir
`prueba-tecnica/calculadora-posicion-futuros.html` en una página real (`src/pages/calculadora.astro`)
que reutilice `BaseLayout`, los componentes de `src/components/ui/` y los tokens de
`tokens.css`, conservando intacta la lógica de cálculo del script original. Decisiones ya tomadas
sobre esto en [[brief-tecnico]].
