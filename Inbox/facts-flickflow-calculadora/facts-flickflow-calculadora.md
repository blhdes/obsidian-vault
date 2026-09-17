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
  sección de referencia de componentes
  - [x] Bug corregido: los toggles Compra/Venta y Abajo/Arriba en estado activo
    (fondo claro) dejaban el texto ilegible — `text-text-muted` (pensado para
    fondo oscuro) se quedaba puesto a la vez que `text-text-inverse`, compitiendo
    por la cascada. Arreglado con un helper `setSegActive()` que intercambia los
    dos pares de clases (fondo + texto) en bloque, nunca uno solo
  - [ ] Resto del rediseño de interacción pendiente
- [ ] Crear la rama de trabajo, commitear (**solo con aviso previo del usuario**)
- [ ] Abrir el PR a `prueba-tecnica-calculadora`

## Antes de commitear: qué NO va al PR

Dos archivos viven sin trackear en el repo, solo para nuestro uso durante el
desarrollo — hay que acordarse de dejarlos fuera del `git add`:

- `README.md` (raíz del repo) — chuleta local de arranque/testing
- `public/dev/calculadora-original.html` — copia de referencia de la calculadora
  original, sin procesar

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
