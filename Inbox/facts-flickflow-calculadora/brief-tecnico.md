---
title: Brief técnico — Calculadora Flickflow
date: 2026-09-16
tags: [career, technical-test, flickflow, facts]
---

# Brief técnico — Calculadora Flickflow

Ver [[facts-flickflow-calculadora|índice del proyecto]] para el contexto general.

## La calculadora original

`prueba-tecnica/calculadora-posicion-futuros.html` — calculadora de tamaño de posición
para futuros. Un único archivo HTML con estilos inline y un `<script>` con toda la
lógica:

- Elegir un activo entre grupos: índices EE. UU., índices Europa, materias primas,
  divisas (FX), renta fija, volatilidad (VIX), cripto (CME), perpetuos cripto, o un
  instrumento personalizado (tick + valor de tick a mano)
- Inputs: tamaño de cuenta, riesgo por operación (%), dirección (compra/venta), precio
  de entrada, y el stop — por precio o por distancia en puntos (se sincronizan solos)
- Salida: contratos a operar por cada tamaño de contrato disponible del activo
  (E-mini/Micro/E-nano, etc.), con redondeo arriba/abajo y avisos si el redondeo se
  pasa del riesgo permitido o si en un perpetuo el stop queda después del precio de
  liquidación
- **La lógica no se toca.** Solo cambia la piel (marcado + estilos) para integrarla en
  el sistema de componentes del sitio.

## El sitio: Flickflow marketing site

- **Stack:** Astro 5 + Tailwind v4. Contenido de las páginas de producto completas
  gestionado por Keystatic (backoffice, solo en dev) — la calculadora no necesita esa
  maquinaria, es una página estática simple.
- **Tema:** oscuro por defecto. Acento naranja de marca (`--ff-accent` / `text-accent`)
  para acciones; acento teal (`--ff-info` / `text-info`) reservado para "el sistema te
  está señalando algo" (así lo dice el propio código) — no se mezclan.
- **Tokens** en `src/styles/tokens.css`: escala de radios fija (4/6/8/12/16/24px),
  duración/easing de transiciones, sombras, tipografía (Inter + Safiro display). Puente
  a Tailwind vía `@theme inline` en `global.css` — la regla del propio código es "nunca
  `bg-[#fff]`, nunca `text-slate-600`", solo las utilidades del tema.
- **Componentes reutilizables** en `src/components/ui/`: `Button`, `Panel`, `Cell`,
  `Section`, `SectionHeader`, `Badge`, `Tabs`, `SpecTable`, `Stat`, `Icon`. No hay
  ningún input de formulario (number/select) en ningún otro sitio del código — seríamos
  los primeros en sentar ese patrón, con los tokens ya existentes.
- **Navegación** en `src/data/home.ts` (`export const nav`). El menú "Recursos" hoy
  tiene dos ítems de relleno que no enlazan a nada real (`#academy`, `#blog`, anclas
  que ni siquiera existen en la home). Las páginas de herramienta reales (`/charts`,
  `/calendar`, `/mcp`, `/canvas`) son rutas planas de primer nivel, aunque cuelguen del
  menú "Producto" — no hay ningún prefijo `/recursos/...` en uso.
- **Iconos** en `src/components/ui/icons.ts`: trazo simple, `viewBox 0 0 24 24`,
  hereda `currentColor`. No existe ningún icono de calculadora.

## Decisiones de integración (confirmadas 2026-09-16)

1. **Ruta:** `/calculadora`, plana, de primer nivel — mismo patrón que `/charts`,
   `/calendar`, `/mcp`.
2. **Ubicación en el menú:** primer ítem del grupo "Recursos" (por delante de Academy
   y Blog, que hoy no son reales).
3. **Flujo de ramas:** una rama nueva a partir de `prueba-tecnica-calculadora` (p. ej.
   `feature/calculadora-recursos`), trabajo ahí, PR de vuelta a
   `prueba-tecnica-calculadora`. **Sin commits hasta aviso explícito del usuario.**
4. **Alcance:** re-vestir el marcado y conservar la lógica de cálculo tal cual. Solo se
   añade lo mínimo fuera de la página en sí: el icono `calculator` en `icons.ts` y una
   entrada en `nav.items` (Recursos) dentro de `src/data/home.ts`. Cualquier otra idea
   va a [[ideas-fuera-de-alcance]], no al código.

## Pendiente

- Construir `src/pages/calculadora.astro` con el marcado adaptado al sistema de
  componentes (formularios, resultado, ficha del contrato)
- Probar en local: `npm install && npm run dev` → `http://localhost:4321/calculadora`
- Revisión visual contra el resto del sitio antes de cualquier commit
