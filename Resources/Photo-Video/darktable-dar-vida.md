---
title: Darktable, dar vida y estilo después del ajuste base
date: 2026-09-24
tags: [photo-video, darktable, color, estilos, referencia]
---

Qué añadir cuando la foto ya lleva el ajuste base (`exposure`, `color calibration`, `sigmoid`, `local contrast`) y se ve correcta pero plana. Probado en la ruta B de [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]] (24-09-2026), `tone equalizer` se usa por primera vez en [[Resources/Photo-Video/Sesiones/los-antonios-castellbisbal]]. Ordenado por impacto.

> [!tip] Dónde están los presets
> En el icono **☰** a la derecha de cada módulo, no en la búsqueda de módulos. Elegir un preset activa el módulo solo.

| # | Módulo | Punto de partida | Qué hace |
|---|---|---|---|
| 1 | `color balance rgb` | **☰ → basic colorfulness: vibrant colors** (o *natural skin*, más suave) | el que más vida da; luego afinar *vibrance* y *saturation* |
| 2 | `tone equalizer` *(aún sin probar)* | **☰ → compress shadows/highlights: soft** | aclara caras en sombra sin quemar el cielo |
| 3 | `vignetting` | *brightness* -0,2 a -0,3 | oscurece los bordes, la mirada va al centro |
| 4 | `grain` | *strength* 10-15 % | textura de película, disimula el ruido a ISO alto. Opcional, de gusto |

## Tone equalizer, cómo se usa (darktable 5.6, según el manual)

1. **☰ → compress shadows/highlights (eigf): soft.** Activa el módulo con una curva suave.
2. **Pestaña advanced** (no *masking*, aunque el nombre despiste): debajo de la curva, clic en la **varita** de *mask exposure compensation* y luego en la de *mask contrast compensation*.
3. En esa misma pestaña, el histograma de la máscara tiene que ocupar casi todo el ancho. Si está apelotonado, rehacer las varitas o mover a mano esos dos sliders. Con *display exposure mask* (abajo del módulo) se ve la máscara en gris: la foto, pero muy borrosa.
4. **Afinar sobre la foto:** con el cursor sobre una cara en sombra, la **rueda del ratón** sube o baja solo esa zona tonal.
5. *preserve details* en **eigf** (el de serie). Si salen halos en bordes de alto contraste (pelo contra cielo), subir *smoothing diameter*.

> [!warning] Va en el estilo, pero la máscara se recalcula en cada foto
> Las varitas se aplican sobre la foto de trabajo. En un lote, una foto mucho más clara u oscura puede tener la máscara descentrada: revisar las extremas.

## Vibrance frente a saturation

- **vibrance** satura sobre todo los colores apagados y respeta más la piel.
- **saturation** sube todos por igual. Con piel en cuadro, tirar de *vibrance* primero.

## Virado cálido-frío (pestaña 4 ways de `color balance rgb`)

Sombras un poco hacia **azul/verde**, luces hacia **naranja**. Muy poco: **2-5 %**. Es un look muy de boda; pasado de ahí se nota el filtro.

## Aplicarlo a una sesión

- Pegarlo a los carretes de **RAW** con *history stack → selective copy / paste*, marcando solo estos módulos.
- A los **fotogramas de vídeo**, aparte y **más suave**: el vídeo ya sale saturado de la cámara.

Relacionado: [[Resources/Photo-Video/darktable-blanco-y-negro]] · [[Resources/Photo-Video/postpro-paso-a-paso]] · [[Resources/Photo-Video/darktable-crear-estilos]]
