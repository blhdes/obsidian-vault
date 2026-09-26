---
title: Darktable, blanco y negro contrastado y vintage
date: 2026-09-24
tags: [photo-video, darktable, blanco-y-negro, estilos, referencia]
---

Receta para pasar una foto a blanco y negro con contraste alto y aire de copia antigua. Usada por primera vez en [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]] (24-09-2026). Parte de una foto que ya lleva el ajuste base (`exposure`, `color calibration`, `sigmoid`, `local contrast`, ver [[Resources/Photo-Video/postpro-paso-a-paso#6-8 · Ruta B, revelado desde el catálogo]]).

> [!tip] Dónde están los presets
> En el icono **☰** a la derecha de cada módulo, no en la búsqueda de módulos.

## 1 · Pasar a blanco y negro: `color calibration`, segunda instancia

1. En `color calibration`, icono **⧉** → **new instance**. La primera instancia sigue corrigiendo la dominante; la nueva solo hace el blanco y negro.
2. En la nueva, **☰** → un preset **monochrome**. Para vintage: *Kodak Tri-X* o *Ilford HP5+*.
3. Pestaña **gray**: decide cómo pesa cada color al convertirse en gris. Subir el **rojo** aclara la piel; bajar el **azul** oscurece el cielo.

**Por qué aquí y no desaturando:** desaturar mezcla los colores siempre igual. `color calibration` deja elegir la mezcla, como los filtros de color en la fotografía de película.

## 2 · Contraste: `sigmoid` + `local contrast`

- `sigmoid` → *contrast* **2,0-2,3** (el ajuste base va sobre 1,8).
- Si quieres más textura: `local contrast` → *detail* **~130 %**.

## 3 · Negros lavados: `rgb curve`

Sube un poco el **punto de abajo a la izquierda** de la curva. El negro puro pasa a gris muy oscuro, como una copia antigua. Es lo que más "vintage" da, con poco.

## 4 · Textura: `grain` + `vignetting`

| Módulo | Valor de partida | Para qué |
|---|---|---|
| `grain` | *strength* ~25 %, *coarseness* algo alto | textura de película; también disimula el ruido a ISO alto |
| `vignetting` | *brightness* ~-0,3 | lleva la mirada al centro |

## 5 · Opcional: tono sepia leve

`color balance rgb` → pestaña **4 ways** → luces hacia **naranja**, **3-5 %**. Funciona aunque la foto ya sea gris, porque este módulo va después de `color calibration` en el procesado.

## Aplicarlo a más fotos

1. En la foto terminada: **history stack → compress history**.
2. **styles → create**, marcando solo los módulos de esta receta. Nombre sugerido: `bn-vintage`.
3. Aplicar el estilo a las fotos elegidas desde la lighttable.

> [!note] Con fotogramas de vídeo
> Es la mejor salida para fotogramas con una dominante muy fuerte (el naranja de noche): el blanco y negro rescata más que corregir. Pero el vídeo ya viene con el contraste de la cámara: **sin `sigmoid`** (el contraste se aplicaría dos veces). El contraste, solo con `rgb curve`, con una S suave.

Relacionado: [[Resources/Photo-Video/darktable-crear-estilos]] · [[Resources/Photo-Video/postpro-paso-a-paso]]
