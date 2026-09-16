---
title: Ideas fuera de alcance — Calculadora Flickflow
date: 2026-09-16
tags: [career, technical-test, flickflow, facts, backlog]
---

# Ideas fuera de alcance

Cosas que han salido durante la exploración pero que **no** forman parte del entregable
de la prueba técnica. Se apuntan aquí para no perderlas y para no desviar el alcance
mientras se construye. Ver [[facts-flickflow-calculadora|índice del proyecto]].

- **Enlazar "Calculadora" en el footer.** La columna "Recursos" del footer
  (`src/data/home.ts` → `footer.columns`) ya lista textos de recursos, pero hoy TODOS
  los enlaces del footer son placeholders (`href="#"`) — no están conectados a rutas
  reales en ningún sitio del código. Añadir el texto "Calculadora" a esa lista costaría
  nada, pero conectarlo de verdad implicaría reescribir cómo `Footer.astro` resuelve
  sus enlaces (hoy son solo strings, no objetos con `href`), que es más cambio del que
  pide la prueba.
- **Texto instructivo.** Explicar en la propia página qué es el "tamaño de posición" o
  cómo se usa la calculadora. La copy actual del sitio es deliberadamente corta y
  concreta (reglas de voz de marca en `home.ts`: nunca prometer rentabilidad, nada de
  relleno). Un bloque explicativo podría añadir valor, pero no lo pidió Lucas y podría
  leerse como sobre-construir la prueba.
- (añadir aquí cualquier otra idea que surja durante el desarrollo)
