---
title: Darktable, dar vida y estilo después del ajuste base
date: 2026-09-24
tags: [photo-video, darktable, color, estilos, referencia]
---

Qué añadir cuando la foto ya lleva el ajuste base (`exposure`, `color calibration`, `sigmoid`, `local contrast`) y se ve correcta pero plana. Probado en la ruta B de [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]] (24-09-2026), salvo `tone equalizer`, que queda apuntado para la próxima. Ordenado por impacto.

> [!tip] Dónde están los presets
> En el icono **☰** a la derecha de cada módulo, no en la búsqueda de módulos. Elegir un preset activa el módulo solo.

| # | Módulo | Punto de partida | Qué hace |
|---|---|---|---|
| 1 | `color balance rgb` | **☰ → basic colorfulness: vibrant colors** (o *natural skin*, más suave) | el que más vida da; luego afinar *vibrance* y *saturation* |
| 2 | `tone equalizer` *(aún sin probar)* | **☰ → compress shadows/highlights: soft** | aclara caras en sombra sin quemar el cielo |
| 3 | `vignetting` | *brightness* -0,2 a -0,3 | oscurece los bordes, la mirada va al centro |
| 4 | `grain` | *strength* 10-15 % | textura de película, disimula el ruido a ISO alto. Opcional, de gusto |

## Vibrance frente a saturation

- **vibrance** satura sobre todo los colores apagados y respeta más la piel.
- **saturation** sube todos por igual. Con piel en cuadro, tirar de *vibrance* primero.

## Virado cálido-frío (pestaña 4 ways de `color balance rgb`)

Sombras un poco hacia **azul/verde**, luces hacia **naranja**. Muy poco: **2-5 %**. Es un look muy de boda; pasado de ahí se nota el filtro.

## Aplicarlo a una sesión

- Pegarlo a los carretes de **RAW** con *history stack → selective copy / paste*, marcando solo estos módulos.
- A los **fotogramas de vídeo**, aparte y **más suave**: el vídeo ya sale saturado de la cámara.

Relacionado: [[Resources/Photo-Video/darktable-blanco-y-negro]] · [[Resources/Photo-Video/postpro-paso-a-paso]] · [[Resources/Photo-Video/darktable-crear-estilos]]
