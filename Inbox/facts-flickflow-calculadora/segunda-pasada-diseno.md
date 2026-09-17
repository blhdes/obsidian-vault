---
title: Segunda pasada — dirección de diseño
date: 2026-09-17
tags: [career, technical-test, flickflow, facts, design]
---

# Segunda pasada — dirección de diseño (2026-09-17)

Apuntes del usuario para el rediseño de interacción de `/calculadora`, tomados antes
de tocar código. Ver [[facts-flickflow-calculadora|índice del proyecto]] y
[[brief-tecnico]].

## Layout

- **Full-bleed**, buscando una experiencia más orgánica y cercana — se abandona el
  contenedor estrecho actual (`Container width="narrow"`, 720px).
- **Jerarquía vertical**: una sola columna, no las dos actuales — el resultado de la
  posición va **abajo del todo**, después de rellenar los campos.
- **Sin scroll**: el full-bleed tiene que caber en una pantalla, sin necesitar hacer
  scroll para llegar al resultado, a cualquier tamaño de viewport (responsive). Es
  el mismo espíritu que la técnica "fit-screen" (`body.fit-screen`,
  `overflow:hidden`) que ya usamos en el portfolio propio — aquí habrá que
  adaptarla a un formulario más largo, así que probablemente implique compactar
  bastante los campos, no solo copiar la misma clase.
- La división a dos columnas actual queda descartada — "hace un uso del espacio
  desequilibrado".

## Inputs: valores por defecto como placeholder, no como valor fijo

- Ahora mismo los `value="25000"` (etc.) se sienten "fijos": al escribir, el usuario
  edita un número que ya estaba ahí, en vez de partir de un campo limpio.
- Cambiar a: el default se muestra como **placeholder**, el campo empieza **vacío**
  de verdad. Escribir reemplaza el placeholder de forma natural.
- **Caso único**: si el usuario usa las flechas arriba/abajo del `<input
  type="number">` (el spinner nativo) sin haber escrito nada antes, el placeholder
  SÍ debe escribirse como valor real del campo antes de aplicar el
  incremento/decremento — si no, el spinner nativo parte de 0 (o de `min`), no del
  default visible, y confundiría.
  - Nota técnica para cuando implementemos: el evento `input`/`change` del spinner
    no distingue por sí solo "vino de las flechas" vs "el usuario escribió" — hay
    que decidir la detección exacta (candidatos: `mousedown`/`pointerdown` sobre la
    zona del spinner, o comparar que el valor cambió sin evento de teclado de por
    medio). Pendiente de resolver en la implementación, no ahora.

## Tablas informativas → SpecTable real

- La ficha del contrato (y probablemente la lista de tiers del resultado) deben
  vivir dentro de un contenedor tipo `SpecTable.astro` de verdad (borde propio,
  `overflow-hidden`, radio, filas separadas por `border-rule`) — no las filas
  sueltas con un simple `border-t` que tienen ahora, que no las separa del fondo de
  la página.

## Separación de contenido vía heading, no vía líneas

- Para separar bloques dentro de la calculadora, usar más la jerarquía de
  **headings** (tope: `h3`, nunca más grande) en vez de líneas divisorias.
- Nota: coincide con el criterio que el usuario ya aplica en su propio portfolio
  (nunca separar secciones con una simple línea de 1px — escala tipográfica +
  espacio en blanco en su lugar). Aquí se aplica dentro del propio widget de la
  calculadora; el resto del sitio de Flickflow sí usa líneas como parte de su
  retícula (`Section`, `border-rule`), así que es una decisión específica para el
  contenido interno de la calculadora, no un cambio del sistema del sitio.

## Versión 1 — correcciones (2026-09-17)

Primer intento construido en `src/pages/dev/calculadora-redesign.astro`
(`/dev/calculadora-redesign`). Dos correcciones tras la primera revisión del
usuario:

- **"Full-bleed" no era eso** — la primera versión tenía `max-w-[560px] mx-auto`,
  justo lo contrario de full-bleed (una caja estrecha centrada). Corregido: el
  fondo/sección llega al gutter del sitio (`--ff-gutter`), pero cada CAMPO tiene su
  propio ancho fijo según lo que se escribe en él (números cortos, campos cortos) —
  full-bleed es el fondo, no el ancho de cada input.
- **El resultado no aparecía con los placeholders** — el cálculo a mano confirma que
  la lógica sí producía un resultado real (NQ con los defaults: E-mini→0, Micro→3,
  E-nano→31), así que no era un bug de cálculo. Sospecha: el script de Astro se
  cargaba como módulo externo (`type="module"`), con un salto perceptible frente al
  archivo original (que es inline y síncrono). Solución aplicada: el script pasa a
  `is:inline` + JS plano (sin TypeScript), ejecutándose de forma síncrona igual que
  el original — sin depender de la carga de un módulo aparte.

## Ideas HIG (Apple Human Interface Guidelines) — propuestas, no implementadas

Pedidas por el usuario, generadas repasando las HIG Foundations
(https://developer.apple.com/design/human-interface-guidelines/foundations):

1. **Lista agrupada tipo Settings.app** — en vez de cada campo flotando con su
   propia etiqueta suelta, agrupar los campos principales en un único panel con
   borde (como una "inset grouped list"): fila = etiqueta a la izquierda + control a
   la derecha, filas separadas por `border-rule` dentro del MISMO panel. No es lo
   mismo que "usar líneas para separar bloques" (que se ha descartado) — es la
   separación interna esperada de una lista, no una raya suelta entre dos secciones
   grandes.
2. **Segmented control con indicador deslizante** — Compra/Venta y Abajo/Arriba ya
   son conceptualmente el "Segmented Control" de las HIG; llevarlo más lejos:
   segmentos de ancho igual y un indicador de selección que se desliza (en vez de
   solo cambiar el color de fondo del botón activo), más cercano al control nativo.
   Requiere más JS/CSS (medir posición o usar un truco de `peer`/grid) — no
   implementado todavía.

**Ya implementadas en v1** (no solo propuestas):
- La "ficha del contrato" es un `<details>` plegado por defecto — divulgación
  progresiva, mismo patrón sin JS que ya usa el sitio en el mega menú y el nav
  móvil. Ayuda directamente al objetivo "sin scroll" al reducir el alto inicial.
- **Lista agrupada tipo Settings.app** (idea #1) probada: los campos ya no van
  etiqueta-arriba/input-abajo, sino en paneles con borde propio, fila = etiqueta a
  la izquierda + control a la derecha, filas separadas por `border-rule` dentro del
  MISMO panel. Los inputs van sin borde propio (el límite lo da la regla de la
  fila, como un campo de una fila de Ajustes). Se agrupó en tres paneles con su
  propio heading encima — "Cuenta y riesgo", "Operación", "Stop loss" — en vez de
  un único panel gigante, así el heading sigue haciendo el trabajo de separar
  bloques grandes y el panel agrupa solo lo afín. Efecto lateral bueno: al compartir
  fila, cada campo ocupa menos alto vertical que antes — ayuda también al objetivo
  "sin scroll".

**Sigue pendiente, no implementada:** segmented control con indicador deslizante
(idea #2).

## Verificación en Chrome (2026-09-17, viewport 1476×825)

- ✅ El resultado aparece desde la carga con los placeholders (NQ: E-mini 0 · Micro
  3 · E-nano 31), igual que el cálculo a mano. Sin errores en consola.
- ✅ Toggles legibles en estado activo.
- 🔧 **Arreglado:** el toggle Abajo/Arriba salía descentrado (también en
  `/calculadora`) — usaba `inline-flex`, y `mx-auto` solo centra cajas de bloque.
  Cambiado a `flex` en las dos páginas, verificado centrado.
- 🔧 **Arreglado:** la cabecera del sandbox quedaba debajo de la barra fija del
  sitio (le faltaba el padding de `--ff-header-h`).
- ⚠️ **Sin resolver — decisión de diseño:** en pantalla ancha, las filas tipo
  Settings estiran la etiqueta y su valor a **~1100px** de distancia. El patrón de
  Ajustes funciona porque iOS es estrecho; a sangre completa en escritorio cuesta
  relacionar cada etiqueta con su valor.
- ⚠️ **"Sin scroll" no se cumple:** la calculadora mide 972px y el espacio útil bajo
  la barra es 752px (~220px de más).
- ⚠️ **Incoherencia:** "Distancia (puntos)" muestra un valor real (texto blanco)
  mientras el resto son placeholders (gris) — la sincronización stop↔puntos escribe
  el valor calculado en el campo.

## Ajustes aplicados tras la verificación (2026-09-17)

Aprobados por el usuario y medidos en Chrome headless (1476×825):

- ✅ **Columna a 600px**, alineada al gutter; la página sigue a sangre completa.
  Distancia etiqueta→valor: de ~1100px a **319px**.
- ✅ **Notas de la versión movidas debajo del resultado** (idea del usuario), y la
  cabecera larga del sandbox reducida a una línea — la calculadora empieza ya a
  125px del borde superior (barra de 73px + aire), como en una página real.
- ✅ **Más aire bajo las notas de contexto** (riesgo permitido, distancia al stop):
  8px de separación del panel (antes quedaban pegadas).
- ✅ **Espaciado más compacto:** filas `py-2.5`, títulos `mt-4`, panel de resultado
  `py-4`. Alto de la calculadora: de 972px a **879px**.
- ✅ **Campos derivados en gris:** "Distancia (puntos)" y "Precio de stop" se
  quedan como placeholder mientras no se haya escrito en sus campos de origen.
  Probado: escribir entrada 19000 → distancia pasa a valor real (1040); borrar →
  vuelve a gris (40); pulsar Venta sin nada escrito → el stop gris pasa a 18040;
  Compra → vuelve a 17960. El resultado se recalcula bien en todos los casos.
- ⚠️ **Sigue sin caber sin scroll:** el resultado termina en 1004px y la pantalla
  mide 825px → faltan **~180px**. Quitando solo aire no llega; hace falta una
  decisión de estructura (ver opciones en el chat del 2026-09-17: resultado fijo
  abajo tipo sticky, unir paneles, o aceptar scroll en pantallas bajas).

## Resultado a la derecha (2026-09-17)

Propuesta del usuario: volver a poner el resultado a la derecha, como en la
original. **Revierte a propósito la "jerarquía vertical"** de los apuntes iniciales,
pero con una diferencia clave frente a la original: anchos fijos (campos hasta
600px, resultado 380px) en vez de dos fracciones casi iguales dentro de 720px, que
era lo que se leía desequilibrado.

- Desde `lg` (1024px): dos columnas. El resultado se queda fijo (sticky) al hacer
  scroll.
- En móvil: el resultado vuelve debajo de los campos (orden vertical).

Medido en Chrome headless:

- ✅ **1476×825:** todo cabe sin scroll (campos hasta 680px, resultado 153–473px).
  Con la ficha del contrato abierta los campos llegan a 805px y siguen cabiendo; al
  hacer scroll, el resultado se queda visible arriba a la derecha.
- ✅ **1024×768:** cabe sin scroll; la columna de campos se estrecha a 530px, sin
  desbordamiento horizontal.
- ✅ **390×844 (móvil):** resultado debajo, sin desbordamiento horizontal. Aquí sí
  hay scroll (esperado con orden vertical).
- Detalle visual menor: el panel del resultado empieza ~8px más abajo que el
  primer panel de campos, porque su título ("Resultado", tamaño h3) es más alto
  que "Cuenta y riesgo" (h4).

## Estado

Apuntes de dirección + primera corrección de v1 ya construidos. Pendiente:
revisión del usuario en Safari real, decidir sobre las dos ideas HIG propuestas, y
si se sigue iterando sobre v1 o se apila una v2.
