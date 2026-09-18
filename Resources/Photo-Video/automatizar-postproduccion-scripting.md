---
title: Automatizar la postproducción fotográfica con scripting (sin Lightroom)
date: 2026-09-17
tags: [photo-video, workflow, scripting, raw, darktable, automatizacion]
---

Pregunta: ¿se puede sustituir el trabajo tedioso de edición por scripting, ahora que ya no uso Lightroom? Respuesta de Claude, guardada como referencia antes de montar el flujo de trabajo. Relacionado: [[Resources/Photo-Video/open-source-alternatives]], [[Resources/Photo-Video/darktable-manual-basico]].

Resumen: sí para una parte, no para otra, y la diferencia importa mucho antes de montar un flujo de trabajo alrededor de esto.

## Dónde sí ahorra días de verdad

Todo lo repetitivo y mecánico, que suele ser el 70% del tiempo real de una entrega:

- **Ingesta y organización**: copiar de la tarjeta, verificar checksums, renombrar por fecha/evento/número, estructura de carpetas, backup a dos destinos.
- **Culling asistido**: descartar fotos desenfocadas (medida de nitidez por varianza del laplaciano), detectar ráfagas casi idénticas y quedarse con la más nítida, filtrar por EXIF (todo lo que salga a ISO 12800 o a 1/15, por ejemplo).
- **Revelado por lotes con un preset propio**: aquí está el truco. Defines el look en 5 o 10 fotos de referencia en Lightroom, Capture One o darktable, exportas el ajuste (`.xmp`, `.pp3`, preset `.dng`), y el script lo aplica a las 800 restantes con `darktable-cli` o `rawtherapee-cli`, con variantes por condición de luz (interior, exterior, contraluz).
- **Igualar exposición y balance de blancos entre fotos** de la misma escena, que es tedioso a mano y es puro cálculo.
- **Entrega**: exportar en tres tamaños a la vez, sRGB para web y AdobeRGB para imprenta, marca de agua, limpiar o conservar metadatos según cliente, galería de contactos en PDF, empaquetar y nombrar según lo que pida cada cliente.

Eso es reproducible, auditable y se ejecuta en minutos sobre cientos de RAW.

## Dónde no sirve

- **El criterio visual fino.** Claude ve las imágenes a baja resolución, sin gestión de color y sin pantalla calibrada. No puede juzgar un tono de piel, un viraje sutil en las sombras ni si un verde se ha ido. Cualquier decisión de color la tomo yo.
- **Retoque de píxel**: piel, dodge and burn, licuar, eliminar elementos, máscaras complejas. Eso es Photoshop a mano.
- **Las máscaras de IA de Lightroom o los ajustes locales de Capture One**: no las sustituye.

O sea: no es un editor, es un ayudante de postproducción. El ojo lo pongo yo una vez, el script lo multiplica por 800.

## Requisito previo: disparar en RAW

Todo lo de abajo asume archivos RAW. Con HEIF o JPEG el margen para recuperar luces y sombras es mucho menor y el revelado automatizado pierde buena parte de su sentido.

Los ajustes concretos de la a7 IV, con las rutas de menú en inglés: [[Resources/Photo-Video/sony-a7iv-ajustes]].

## Límite conocido del filtrado por EXIF

El culling por metadatos funciona para ISO, velocidad, diafragma y focal, pero **no para detectar flash**. Mi speedlight es la versión de Fujifilm, así que la cámara ni siquiera registra que hay un flash montado: graba `FlashStatus: No Flash present` aunque haya disparado en todas las fotos. Detalle completo en [[Resources/Photo-Video/flash-godox-sony-a7iv]].

Para separar las tomas con flash hay que filtrar por la huella del perfil (`1/160` + `ISO 400` + `WhiteBalance Flash`), no por los campos de flash.

## Herramientas: entorno ya montado (17-09-2026)

Todo instalado y verificado. Nada de esto depende de Adobe.

| Herramienta | Versión | Para qué | Cómo se llama |
|---|---|---|---|
| `darktable-cli` | 5.6.1 | aplicar presets `.xmp` por lotes a RAW | `darktable-cli` (enlace creado en `/opt/homebrew/bin` que apunta dentro de darktable.app) |
| `exiftool` | 13.55 | leer/escribir metadatos EXIF, IPTC, XMP | `exiftool` |
| `vips` | 8.18.6 | procesado rápido de archivos grandes, redimensionado, conversión | `vips`, `vipsthumbnail` |
| `rawpy` | 0.27.1 (LibRaw 0.22.1) | decodificar RAW desde Python | dentro del entorno `~/.venvs/foto` |

### Qué hace cada una

- **`exiftool`** — lee y escribe los datos invisibles del archivo: cámara, objetivo, ISO, velocidad, fecha, GPS, copyright. Sirve para filtrar ("dame todo lo disparado a más de ISO 6400") y para limpiar o firmar metadatos antes de entregar.
- **`vips`** — el motor de fuerza bruta. Abre, redimensiona, convierte y exporta imágenes grandes muy rápido y sin cargarlas enteras en memoria. Para generar los tres tamaños de entrega, las miniaturas y las marcas de agua.
- **`rawpy`** — traduce un `.ARW` a píxeles manejables desde Python. Es lo que permite medir cosas en la foto (nitidez, exposición, dominantes de color) para automatizar el culling.
- **`darktable-cli`** — darktable sin ventana. Coge un preset de revelado y lo aplica a las 800 fotos por línea de comandos. Es el único de los cuatro que revela de verdad.

El reparto, en una línea: **rawpy mide, darktable-cli revela, vips exporta, exiftool etiqueta.**

### El entorno de Python

Las librerías de foto viven en un entorno virtual propio, **no** en el Python del sistema, para no mezclarlas con nada más y poder borrarlo entero sin romper nada:

```
~/.venvs/foto/
```

Contiene: `rawpy` 0.27.1, `numpy` 2.4.6, `pillow` 12.3.0, `scipy` 1.17.1, `imageio` 2.37.4.

Para ejecutar un script con ese entorno se llama a su Python por la ruta completa, sin activar nada:

```bash
~/.venvs/foto/bin/python mi_script.py
```

Instalar algo más ahí dentro:

```bash
~/.venvs/foto/bin/python -m pip install <paquete>
```

### Notas sueltas

- `vips` lee RAW de Sony (`.arw`) directamente vía dcraw, además de `.cr2`, `.cr3`, `.nef`, `.dng` y prácticamente cualquier otro formato de cámara.
- `darktable-cli` no venía en el PATH porque darktable lo esconde dentro del `.app`. El enlace lo arregla. Si algún día actualizas darktable y deja de funcionar, se rehace con:
  ```bash
  ln -sf /Applications/darktable.app/Contents/MacOS/darktable-cli /opt/homebrew/bin/darktable-cli
  ```
- Aún sin probar sobre un RAW real: no hay ningún `.ARW` en el Mac ahora mismo. La primera sesión de fotos sirve de banco de pruebas.

## ¿Hace falta construir el look en darktable, o se puede desde referencias o instrucciones?

Sí se puede sin tocar la interfaz, con un matiz: el look tiene que acabar siendo **un archivo**, pero cómo nace ese archivo es flexible. Tres caminos.

### 1. GUI una vez, luego por lotes (`.dtstyle`)

Ajustas el look en darktable sobre una foto, "crear estilo", y después se aplica a todo:

```bash
darktable-cli entrada/ salida/ --style "mi-look" --width 3000
```

El más fiable, porque usa los módulos buenos de darktable: filmic/sigmoid, calibración de color y los perfiles de ruido específicos de mi cámara.

### 2. LUT `.cube` generada por script

Una LUT (*lookup table*) es una tabla de conversión de color: "este color entra, este sale". Se puede generar desde Python a partir de instrucciones en texto (sombras más frías, pieles algo más saturadas, contraste en S) o deduciéndola de un par de imágenes antes/después. Luego se aplica en darktable con el módulo *lut 3D*, o directamente con `ffmpeg` o `vips`, sin abrir ninguna interfaz.

**Este es el puente real entre "prompt" y revelado**, y es lo que hay dentro de los packs de looks que se venden.

### 3. Transferencia de color desde una referencia visual

Le das una foto que te gusta y se igualan las estadísticas de color entre las dos (media y desviación en espacio Lab, o igualado de histograma). Son unas 20 líneas de numpy.

- Funciona muy bien para **igualar mis propias fotos entre sí** dentro de una misma sesión.
- Para copiar el look de otro fotógrafo funciona a medias: arrastra también su luz y su escena, no solo su estilo.

### Lo que no es viable

Editar el `.xmp` a mano. Los parámetros de cada módulo van codificados en base64, no son texto legible.

### El límite de siempre

Claude puede generar la LUT, pero no puede ver si el resultado deja las pieles verdosas: sin pantalla calibrada y viendo las imágenes a baja resolución, el color lo valido yo.

## Siguiente paso

Para dimensionar cuánto del proceso actual es criterio y cuánto es trabajo mecánico automatizable, hace falta definir: qué cámara, en qué programa revelo ahora, y cómo es una entrega típica (cuántas fotos, qué formatos pide el cliente).

Plan: convertir todo esto en una **skill de Claude** dedicada a esta área, una vez el flujo esté probado sobre una entrega real. La skill documentada irá en `Areas/Claude/Skills/` según la convención del vault.
