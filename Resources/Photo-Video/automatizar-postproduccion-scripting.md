---
title: Automatizar la postproducción fotográfica con scripting (sin Lightroom)
date: 2026-09-17
tags: [photo-video, workflow, scripting, raw, darktable, automatizacion]
---

Pregunta: ¿se puede sustituir el trabajo tedioso de edición por scripting, ahora que ya no uso Lightroom? Respuesta de Claude, guardada como referencia antes de montar el flujo de trabajo. Relacionado: [[Resources/Photo-Video/open-source-alternatives]], [[Resources/Photo-Video/darktable-manual-basico]]. Para vídeo: [[Resources/Photo-Video/automatizar-video-scripting]].

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

Para separar las tomas con flash hay que filtrar por **la huella del perfil de dial**, no por los campos de flash.

**Huella comprobada sobre las 326 del Sopar del Soci (20-09-2026):** el discriminante bueno es `ISOSetting`, o sea si el ISO estaba **fijo** o en **Auto**. Con flash va fijo por necesidad (si flota, cada foto expone el destello distinto), y sin flash va en Auto. Separó las 326 sin una sola ambigüedad.

Ojo con dar por buena una huella teórica: la prevista para esa noche era `1/160` + `ISO 400` + `WB Flash`, y la real acabó siendo **ISO fijo 1600** con `WB Auto` y velocidades de 1/125 a 1/250. **La huella se lee del EXIF de cada sesión, no se asume.**

## Herramientas: entorno ya montado (17-09-2026)

Todo instalado y verificado. Nada de esto depende de Adobe.

| Herramienta | Versión | Para qué | Cómo se llama |
|---|---|---|---|
| `darktable-cli` | 5.6.1 | aplicar estilos `.dtstyle` por lotes a RAW | `darktable-cli` (**wrapper** en `/opt/homebrew/bin`, no un symlink: ver notas sueltas) |
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
- **Corregido el 20-09-2026: el enlace simbólico rompía `darktable-cli`.** Daba `cannot find disk storage module` y no exportaba nada. La causa es que darktable localiza sus módulos con una ruta relativa a `argv[0]`, y a través de un symlink en `/opt/homebrew/bin` busca donde no están. **Un `ln -sf` no vale aquí**; hace falta un wrapper que llame al binario real:

  ```bash
  cat > /opt/homebrew/bin/darktable-cli <<'EOF'
  #!/bin/sh
  exec /Applications/darktable.app/Contents/MacOS/darktable-cli "$@"
  EOF
  chmod +x /opt/homebrew/bin/darktable-cli
  ```

  Comprobación rápida de que va: `darktable-cli foto.ARW /tmp/x.jpg --width 2000 --core --disable-opencl` debe terminar con `[export_job] exported to ...`.

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

## Cadena verificada sobre RAW real (20-09-2026)

Primera prueba de verdad, sobre `AGU01871.ARW` del Sopar del Soci. Las cuatro herramientas funcionan, con una avería encontrada y arreglada (ver arriba).

| Herramienta | Resultado | Tiempo por foto |
|---|---|---|
| `rawpy` | decodifica el `.ARW` sin problema (`half_size`, balance de cámara) | **1,3 s** |
| `darktable-cli` | **estaba roto**, arreglado con wrapper. Revela y exporta | **5 s** |
| `vips` | lee `.ARW` directamente, y redimensiona un JPG ya revelado | **0,12 s** |
| `exiftool` | escribe `Copyright` y `Artist` sobre el JPG exportado | instantáneo |

Escala estimada para una entrega de 326 fotos, en un solo hilo: **~7 min** de medición con rawpy y **~27 min** de revelado con darktable-cli. El revelado se paraleliza por lotes.

## Banco de pruebas: CTNSC Sopar del Soci (326 fotos)

La sesión de [[Resources/Photo-Video/Sesiones/sopar-del-soci-ctnsc]] es el caso de prueba, porque tiene las dos condiciones de luz bien separadas y la nota ya registra el resultado esperado, así que sirve de control.

### El triaje por huella de EXIF funciona y es instantáneo

La nota de la sesión avisa de que **el flash no se puede detectar por EXIF** (el Godox es la versión de Fujifilm y la cámara no registra que hay flash montado). La alternativa es la huella del perfil, y sobre las 326 fotos separa perfecto:

| Config | Huella | Fotos | Tramo |
|---|---|---|---|
| **A · reportaje ambiente** | ISO **Auto** + 1/100 | **98** | 19:59-20:29 |
| **B · premios con flash** | ISO **fijo 1600** | **228** | 20:32-22:19 |

Las 98 de ISO Auto son exactamente las 98 a 1/100: **cero fotos ambiguas**, y los dos bloques salen contiguos en el tiempo. Coste: **8 segundos** de `exiftool` sobre las 326.

> [!important] Por qué este es el primer paso del flujo, y no el revelado
> Revelar 326 fotos con un solo look es el error de calidad más caro que se puede cometer en lotes, porque ambiente a ISO Auto y flash directo a ISO 1600 necesitan tratamientos distintos de ruido, contraste y balance. El triaje es lo que convierte "un lote de 326" en "dos lotes coherentes", y sin él los pasos siguientes no pueden ser buenos.
>
> Además no tiene criterio visual dentro: es determinista, auditable y se comprueba contra lo que ya dice la nota de la sesión.

## Los scripts (20-09-2026)

Viven en `~/Pictures/Postpro/bin/` y se llaman con el Python del entorno de foto:

```bash
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/triaje.py "<carpeta de OneDrive>"
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/culling.py "<carpeta de trabajo>"
```

### La regla que los gobierna: no se pierde nada

Los dos scripts comparten las mismas salvaguardas, y conviene mantenerlas en todo lo que venga despues:

- **La carpeta de OneDrive es de solo lectura.** Es el archivo verificado con checksums. Ningun script escribe, mueve ni borra dentro de ella. `triaje.py` aborta si le pides que trabaje dentro del origen.
- **Todo lo que producen son enlaces simbolicos**, asi que organizar 326 fotos en carpetas cuesta 0 bytes y no duplica los 13 GB.
- **Al limpiar una ejecucion anterior solo borran enlaces.** Si encuentran un archivo real donde esperaban un enlace, se paran y avisan.
- **Verificacion obligatoria al final**: cada foto tiene que aparecer exactamente una vez. Si falta o se repite alguna, el script sale con error.
- Comprobado: tras pasar los dos scripts, **los 652 archivos del origen siguen con el mismo MD5**.

### Estructura que queda en el area de trabajo

```
~/Pictures/Postpro/<nombre de la sesion>/
  00-manifiesto.csv      EXIF completo de cada foto + bloque asignado
  00-triaje.log
  01-triaje/             enlaces, una carpeta por bloque de dial
  02-medidas.csv         cache de nitidez/exposicion/hash
  03-culling/
    1-seleccion/
    2-revisar/           <- lo dudoso, lo decides tu
    3-propuesta-descarte/
    03-decisiones.csv
    03-culling.log
```

### Por que el culling propone tres bandas y no dos

La primera version decidia entre *seleccion* y *descarte* con un solo umbral, y el resultado destapo el problema: en el bloque de flash, **dos de las seis fotos marcadas como borrosas estaban al 98% del umbral**. Eso no es una foto borrosa, es un corte arbitrario donde la distribucion es continua.

Con tres bandas la maquina solo afirma lo que puede medir:

| Banda | Criterio | Sopar del Soci |
|---|---|---|
| **descarte** | nitidez < 0,25 x la mediana del bloque | **3** |
| **revisar** | nitidez < 0,45 x la mediana, o casi identica a otra de la misma rafaga | **51** |
| **seleccion** | el resto | **272** |

Las tres de descarte estan al 27%, 29% y por debajo: esas si son borrosas de verdad. Las 51 de revisar se miran en un par de minutos.

**Las medidas se cachean en `02-medidas.csv`**, asi que reajustar los umbrales cuesta **0,4 s** en vez de los 263 s que tarda decodificar los 326 RAW. Con `--remedir` se fuerza el recalculo.

### Detalles de como mide

- **Nitidez**: varianza del laplaciano, pero partiendo la foto en una rejilla 4x4 y quedandose con **la media de los dos mejores trozos**. La varianza global castigaria el desenfoque de fondo buscado; asi la pregunta que responde es "hay algo enfocado en esta foto", que es la correcta.
- **Umbrales por bloque**, nunca globales: una foto a ISO 1600 con flash y una de ambiente a ISO Auto no tienen la misma textura de ruido.
- **Rafagas**: se agrupan fotos consecutivas con menos de 20 s de diferencia **y** un dHash a distancia <= 6. En esta sesion salieron 266 fotos sueltas, 27 parejas y 2 tercetos, coherente con haber disparado en Single.
- **Avisos** (luces quemadas > 5%, muy oscura): se anotan pero **no descartan por si solos**. Aqui salieron 3.

### Lo que sigue sin poder hacer

Todo lo anterior mide, no mira. Que una foto este enfocada no la hace buena: la expresion, el momento y el encuadre no se miden. Por eso la banda *revisar* existe y por eso el descarte es deliberadamente timido.

## Siguiente paso

Orden previsto, de menos a más riesgo:

1. ~~**Triaje por EXIF**~~ → `triaje.py`. **Hecho.**
2. ~~**Culling asistido**~~ → `culling.py`. **Hecho.**
3. **Repasar a mano la carpeta `2-revisar`** (51 fotos) y las 3 de descarte. Es el unico paso que no se puede automatizar y hay que hacerlo antes de revelar.
4. **Dos estilos de revelado**, uno por bloque, construidos a mano en darktable sobre 5-10 fotos de referencia y exportados como `.dtstyle`. Aqui es donde entra el ojo.
5. **Revelado por lotes** con `darktable-cli --style`, un estilo por bloque. A 5-7 s por foto son unos 25 min para 272, y se paraleliza.
6. **Entrega**: tamanos con `vips`, metadatos con `exiftool`.

Plan: convertir todo esto en una **skill de Claude** dedicada a esta área, una vez el flujo esté probado sobre una entrega real. La skill documentada irá en `Areas/Claude/Skills/` según la convención del vault.
