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
- [ ] Construir `src/pages/calculadora.astro`
- [ ] Añadir el icono `calculator` y la entrada de nav (`src/data/home.ts`)
- [ ] Probar visualmente en local
- [ ] Crear la rama de trabajo, commitear (**solo con aviso previo del usuario**)
- [ ] Abrir el PR a `prueba-tecnica-calculadora`

## Notas relacionadas

- [[brief-tecnico|Brief técnico]] — lo que hemos encontrado en el repo + las decisiones
  de integración
- [[ideas-fuera-de-alcance|Ideas fuera de alcance]] — cosas que no forman parte de la
  prueba pero podrían valer la pena más adelante
- [[stack-y-filesystem|Stack y filesystem]] — el stack explicado con más detalle y una
  guía carpeta por carpeta / archivo por archivo de cómo se relaciona todo en el repo
- [[teoria-financiera-calculadora|Teoría financiera de la calculadora]] — qué calcula
  exactamente la calculadora (tamaño de posición, ticks, apalancamiento, liquidación...),
  explicado desde cero
