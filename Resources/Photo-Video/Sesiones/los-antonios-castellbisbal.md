---
title: Los Antonios, boda Javier y Andrea en Castellbisbal
date: 2026-10-03
tags: [photo-video, sesion, sony, a7iv, boda, exteriores, sol]
cliente: Los Antonios
lugar: Castellbisbal
fecha_sesion: 2026-09-26
---

Segunda boda para **Los Antonios** (la primera: [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]]). Foto y vídeo en tarjetas separadas.

## Contexto

- **Cuándo:** 26-09-2026, de 11:21 a 15:17.
- **Luz:** todo exterior, media mañana con sol potente.

## Resultado (EXIF)

| | |
|---|---|
| Fotos | 165 RAW + 165 JPG, una sola sesión |
| Modo | `M` en todas, ISO 100 fijo, sin flash, compensación 0 |
| Velocidad | 1/250 en 112 · 1/400 en 23 · 1/100 en 12 · el resto entre 1/80 y 1/800 |
| Diafragma | f/5.6 en 119 · el resto entre f/4.5 y f/10 |
| Objetivo | FE 28-70 mm, sobre todo 28 mm y 33-50 mm |
| Perfil | Standard, PP2 |

## Copia (03-10-2026)

- **Fotos:** `OneDrive-FF8/photo and video/2026-09-26 - Los Antonios - Boda Javier y Andrea Castellbisbal/`, 6,7 GB, MD5 verificado en `checksums-md5.txt`.
- **Vídeo:** `... Castellbisbal (vídeo)/`, 84 clips (MP4 + XML), 12 GB, 9,4 min en total. 4K a 25p, de 11:xx a 15:xx. MD5 verificado en `checksums-md5.txt`.

## Postpro

- **Triaje (03-10-2026):** un solo bloque, `01-flash-o-ISOfijo-Standard` (165). El nombre engaña: no hubo flash. Sale así porque el script mete en ese bloque todo lo que tiene ISO fijo, y aquí era ISO 100 a pleno sol.
- **Culling (03-10-2026):** 117 selección · 35 a revisar (24 nitidez dudosa, 11 casi iguales) · 13 descartadas. Nitidez mediana 640, umbrales de serie (0,25 y 0,45).
- **Luces quemadas:** 11 fotos con más del 5 % de la imagen quemada (la peor, `AGU02083`, con el 13 %). Se mide sobre el JPG de la cámara; el RAW guarda algo más de margen en las luces, así que puede que se recuperen en darktable.
- **Revisión + consolidación (03-10-2026):** 130 para revelar, 35 descartadas. Rescatadas a mano 17, descartadas a mano 4 (`AGU01981`, `02022`, `02024`, `02112`). RAW en `04-para-revelar/01-flash-o-ISOfijo-Standard/`.
- **darktable (03-10-2026):** primer culling interno con `R`; ninguna en blanco y negro al final. Estilo `castellbisbal-sol` creado sobre `AGU02064` (brillo medio): exposure auto, color calibration, **tone equalizer (primera vez)**, sigmoid, local contrast, color balance rgb (natural skin + virado), vignetting/grain. Se aplica en la app a todas las no rechazadas y luego recorte/rotación foto a foto, es decir, **ruta B** con `revelar-catalogo.py`.

### Estilo `castellbisbal-sol` (03-10-2026)

Archivo: `~/Pictures/Postpro/2026-09-26 - Los Antonios - Boda Javier y Andrea Castellbisbal/estilos/castellbisbal-sol.dtstyle`. Hecho sobre `AGU02064`. Valores leídos del propio `.dtstyle`:

| Módulo | Valor |
|---|---|
| `exposure` | **automatic**, percentile 50 %, target level **-3,56 EV** |
| `color calibration` | illuminant custom, ~3485 K (cuentagotas) |
| `tone equalizer` | preset **compress shadows/highlights (eigf): soft** (±0,25-0,42 EV), máscara con las dos varitas de *advanced* |
| `sigmoid` | contrast **1,748**, skew **-0,08** |
| `local contrast` | local laplacian, detail **109 %**, highlights 61 %, shadows 45 %, midtone 0,50 |
| `color balance rgb` | base *natural skin* · vibrance **12,9 %** · saturation global +20 %, luces -50 %, sombras +30 % · **shadows lift** hue 196° chroma 2,7 % · **highlights gain** hue 41° chroma 2,2 % |
| `vignetting` | brightness **-0,15**, saturation -0,08, scale 86 %, fall-off 38 % |

- Sin `grain` ni blanco y negro.
- Aplicado en la app (*styles → append*) a las no rechazadas; luego recorte y rotación foto a foto. **48** sin rechazar de 137.
- Para recuperarlo en otra boda soleada: *styles → import* el `.dtstyle`.

### Entrega (03-10-2026)

- **Revelado:** 48 con `revelar-catalogo.py` (~40 s por foto a tamaño completo, el `tone equalizer` lo hace más lento). `revisar-bordes.py`: 3 marcadas (`AGU02028`, `02041`, `02062`), las 3 escena real.
- **Blanco y negro:** 6 hechas a mano en darktable con la receta de [[Resources/Photo-Video/darktable-blanco-y-negro]] (2.ª instancia de `color calibration` en monocromo + `rgb curve` + `grain`): entregas **22, 26, 30, 32, 35, 42** (`AGU02033`, `02041`, `02062`, `02067`, `02077`, `02103`). Van mezcladas con las de color.
- **Archivos:** `Boda-Javier-Andrea-01` a `-48`, alta resolución a tamaño completo, un solo formato (como Valencia). 464 MB. `entregar.py --nombre "Boda-Javier-Andrea"`.
- **Drive del cliente:** `06. BODA JAVIER & ANDREA - CASTELLBISBAL` (id `1LI82JuzHII1Iby39DEdzuQ-M_jm4g6yi`, de losantonios.oficial) → `FOTOS/` (sin subcarpeta: no hay fotogramas en esta boda). Subido con `rclone copy` a `"gdrive,root_folder_id=<id>:"` y comprobado con `rclone check`.

### Pendiente (al cerrar el 03-10-2026)

1. **Fotogramas de vídeo** (paso 5b), pendiente de decidir.
2. **Vídeo:** montaje (vertical 30 s + horizontal 60 s si lo piden como en Valencia), irá a `VÍDEOS/`.
3. Antes de formatear las dos tarjetas, mirar en Finder que OneDrive ha terminado de sincronizar.
