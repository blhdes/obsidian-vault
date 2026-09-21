---
title: Cosentino, retrato entrevista Carolina
date: 2026-09-18
tags: [photo-video, sesion, sony, a7iv, flash, retrato, interior, entrega]
cliente: Cosentino
lugar: showroom con estanterías de muestras Silestone
---

Retrato de **Carolina** para una entrevista de **Cosentino** (18-09-2026), en un showroom: estanterías de madera con muestras de piedra, paredes blancas y mesa de trabajo. Es la **primera sesión que ha recorrido el flujo de postpo completo**, de la tarjeta a la entrega. La guía que salió de aquí: [[Resources/Photo-Video/postpro-paso-a-paso]].

## Lo que piden

- Fotos para un **dossier impreso** de buena calidad, y para **web**.
- No se entregan todas: una selección de **5-6**.

## Configuración (leída del EXIF)

| Ajuste | Valor |
|---|---|
| Modo | `M` |
| Velocidad | 1/160 |
| Diafragma | f/4.5 |
| ISO | **400 fijo** |
| Balance de blancos | Flash |
| Focal | 33-51 mm (FE 28-70) |
| Luz | flash rebotado |

Las 24 fotos tienen exactamente la misma configuración, así que el triaje dio **un solo bloque**.

## Resultado de la postpo (21-09-2026)

| Paso | Resultado |
|---|---|
| Tarjeta | 24 RAW + JPG |
| Descartadas a mano | **4**: AGU01380-01382, pruebas de flash en casa a las 09:xx; AGU01383, estantería vacía (prueba en el sitio) |
| Culling + `revisar.py` | 3 más fuera: AGU01384, AGU01393 y AGU01397 (de cada pareja casi igual se quedó la más nítida) |
| Reveladas | **17**, de AGU01385 a AGU01403, a tamaño completo en 3 min 21 s |
| Retocadas a mano | **4**, de AGU01400 a AGU01403: la cara salía oscura por la mucha pared blanca del encuadre |
| Entrega | *pendiente: selección con `seleccionar.py`* |

## El estilo: `Cosentino Retratos Flash`

Construido sobre **AGU01385**, elegida por tener el brillo en la mitad del bloque. Archivo: `~/Pictures/Postpro/2026-09-18 - Cosentino - Retrato entrevista Carolina/estilos/Cosentino Retratos Flash.dtstyle`.

| Módulo | Valor |
|---|---|
| `exposure` | **automatic**, percentil 50 %, *target level* -3,03 EV |
| `color calibration` | cuentagotas sobre la pared blanca → *custom*, hue 55,2°, chroma 17,2 % (≈ 4380 K) |
| `sigmoid` | contrast 1,884 · skew -0,23 |
| `local contrast` | detail 89 % · highlights 44 % · shadows 69 % · midtone range 0,5 |
| `denoise (profiled)` | apagado: a ISO 400 no hacía falta |

**Retoque de AGU01400 a AGU01403**, fuera del estilo: exposición con percentil 47,52 % y *target* -2,85 EV, más `vignetting`. En el lote, el centro de la imagen subió unos 14 niveles de brillo y las esquinas se quedaron igual.

## Para la próxima sesión parecida

- **Apuntar las pruebas de flash**, o hacerlas con la tapa puesta. Aquí se colaron 4 fotos que no eran de la sesión.
- **Retrato con pared blanca detrás:** la exposición automática oscurece la cara en los planos abiertos. Hay que contar con retocar esas pocas a mano.
- **Si gusta el viñeteado, meterlo en el estilo** para todas, en vez de solo en unas pocas.
