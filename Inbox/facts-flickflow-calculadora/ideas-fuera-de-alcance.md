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
- **Precio en directo como placeholder por defecto** (2026-09-17). Existen opciones
  gratuitas y sin cuenta: el endpoint no oficial de Yahoo Finance (tickers `NQ=F`,
  `GC=F`, `^VIX`, `BTC-USD`, etc. — cubre casi todos los activos de la lista) o
  `stooq.com` como alternativa. Pegas: son endpoints no documentados (pueden
  romperse o bloquear sin aviso, probablemente haría falta un proxy por CORS desde
  el navegador), y convertirían una calculadora estática y sin dependencias en algo
  con llamada de red + estado de carga/error — más alcance del que pide la prueba
  ("la lógica no se toca").
- (añadir aquí cualquier otra idea que surja durante el desarrollo)
