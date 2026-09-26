---
title: Automatizar la postproducción de vídeo con scripting e IA
date: 2026-09-19
tags: [photo-video, video, workflow, scripting, automatizacion, ia, ffmpeg]
---

Hermano de [[Resources/Photo-Video/automatizar-postproduccion-scripting]], pero para vídeo. Investigado el 19-09-2026 camino de la sesión de Los Antonios, la primera con foto y vídeo a la vez. **Pendiente de evaluar con material real.**

Resumen: sí se puede automatizar una parte, pero el reparto es distinto al de foto, y aquí **el hardware manda más que las herramientas**.

## El condicionante: iMac M1 con 8 GB

No es un detalle, define el flujo entero.

El material sale en **XAVC S 4K 10 bits 4:2:2 H.264**. Ese perfil concreto no entra en el motor de vídeo del **M1 base**, pensado para H.264/HEVC de 8 bits 4:2:0. La aceleración de ProRes y de 4:2:2 llegó con el M1 **Pro** y **Max**.

→ Este Mac descodifica esos clips **a fuerza de CPU**, con 8 GB de RAM. **Editar los originales directamente va a tirones.**

> [!todo] Por comprobar con un clip real
> Medir cuánto tarda de verdad en descodificar un clip de 10 s del material propio. Hasta entonces esto es una previsión razonada, no un dato medido.

### La solución: flujo de proxies

```bash
# proxy ProRes 1080p desde el original 4K
ffmpeg -i clip.MP4 -vf scale=1920:-2 -c:v prores_ks -profile:v 0 \
       -c:a copy proxy/clip.mov
```

Se monta con los proxies y al final se relinkan los originales para exportar.

**Aquí paga el método de captación de [[Resources/Photo-Video/metodo-foto-video-simultaneo]]:** grabando 20 clips de 10 s en vez de 200, los proxies de una sesión entera ocupan **poco más de 1 GB**. Con 200 clips esto sería inviable en este Mac.

## Qué se automatiza y qué no

| Fase | ¿Se automatiza? |
|---|---|
| Ingesta, checksum, organización | **Sí**, ya montado |
| Generar proxies | **Sí**, y es lo que más cambia el día |
| Transcripción y subtítulos | **Sí**, en local |
| Versión vertical desde la horizontal | **Sí, con IA** |
| Color consistente entre clips (LUT) | **Sí** |
| Exportar a los formatos de entrega | **Sí**, reutilizable para siempre |
| **Elegir qué clips entran y en qué orden** | **No** |
| **Dónde cae el corte respecto a la música** | **No** |

Misma conclusión que en foto: **no es un editor, es un ayudante de postproducción.**

## La pieza de IA que gana su sitio: auto-reframe

El caso concreto: entregar **un vertical de 30 s y un horizontal de 60 s** sacados del mismo 4K horizontal. Hay herramientas locales y abiertas que detectan al sujeto y calculan el recorte 9:16 siguiéndolo.

| Herramienta | Qué hace |
|---|---|
| [auto-vertical-reframe](https://github.com/KazKozDev/auto-vertical-reframe) | detecta sujetos por escena y mueve una "cámara virtual" con recorrido suavizado, salida por ffmpeg |
| [FrameShift](https://github.com/fralapo/FrameShift) | versión abierta del AutoFlip de Google, mantiene caras y objetos en cuadro |
| [Autocrop-vertical](https://github.com/kamilstanuch/Autocrop-vertical) | YOLOv8 + ffmpeg, más simple y directo |

- **Funcionan bien con:** personas, alguien hablando, un sujeto claro que se mueve.
- **No funcionan con:** producto, comida, ambiente, detalle. Ahí un recorte centrado fijo sale mejor y se decide a mano en segundos.

## El límite honesto: con 20 clips no compensa

**Automatizar el montaje no sale a cuenta con este volumen.** Hacer el vertical a mano en el programa de edición son unos 20 minutos. Montar y afinar un auto-reframe cuesta más la primera vez, y hay que revisarlo clip a clip igualmente. Esto paga con 200 clips, no con 20.

Donde sí se gana tiempo desde el primer día, por orden de retorno:

1. **Proxies** — salva la edición entera en este Mac.
2. **Exportación a los formatos de entrega** con un script.
3. **Subtítulos**, si hay gente hablando.
4. **LUT uniforme** entre clips.

## DaVinci Resolve: dos límites que afectan

Es el candidato natural y la versión base es gratuita, pero:

- **La API de scripting externa en Python es solo de Studio** (295 €). La gratuita solo tiene consola interna.
- **Smart Reframe**, su auto-reframe, también es **solo Studio**.

→ Resolve gratis vale perfectamente **para montar**, pero **no como pieza scriptable**. La automatización vive fuera, en ffmpeg y Python, antes y después del montaje.

## Herramientas a instalar

| Herramienta | Para qué | Nota en 8 GB |
|---|---|---|
| `ffmpeg` | proxies, recortes, LUT, exportación | **ya instalado** |
| [PySceneDetect](https://www.scenedetect.com/) | detectar cortes, extraer miniaturas, hoja de contactos de clips | ligero |
| [mlx-whisper](https://github.com/orchidsun/mlx-whisper) | transcripción local para subtítulos | modelo `medium` cuantizado a 4 bits, cabe en 8 GB |
| auto-reframe (uno de los tres de arriba) | el vertical automático | solo si se comprueba que compensa |

> [!warning] Whisper: usar la versión MLX, no la de OpenAI
> El Whisper "normal" de Python va muy mal en Apple Silicon. La versión **MLX** es la que aprovecha el chip. Referencia: en un M1, una hora de audio con el modelo `medium` sale en unos 2 minutos con MLX.

## Plan propuesto

Montar **solo los puntos 1 y 2** (proxies y exportación) con el primer material real. Son los que devuelven tiempo desde el primer día y no dependen de nada experimental. El auto-reframe se prueba con un clip real y se decide con datos.

## El límite que no arregla ningún script

Si el vídeo se convierte en ingreso habitual, **el cuello de botella no será el software, serán los 8 GB de RAM**. Es el mismo tipo de límite que el flash de Fujifilm: se trabaja alrededor de él hasta que deje de compensar.

> [!tip] Manual práctico de montaje
> El paso a paso en DaVinci Resolve 21 para la primera entrega: [[Resources/Photo-Video/davinci-resolve-primera-edicion]].
