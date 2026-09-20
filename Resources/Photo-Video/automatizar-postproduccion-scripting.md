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
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/triaje.py     "<carpeta de OneDrive>"
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/culling.py    "<carpeta de trabajo>"
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/revisar.py    "<carpeta de trabajo>"   # app visual
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/consolidar.py "<carpeta de trabajo>"
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
  01-triaje/             enlaces a los RAW, una carpeta por bloque de dial
  02-medidas.csv         cache de nitidez/exposicion/hash
  03-culling/            <- aqui trabajas tu, con enlaces a los JPG
    LEEME.txt
    1-seleccion/
    2-revisar/a-nitidez-dudosa/
    2-revisar/b-casi-iguales/
    3-descartadas/
    03-decisiones.csv
  04-para-revelar/       enlaces a los RAW de la seleccion, por bloque
```

> [!important] El culling enlaza los JPG, no los RAW
> Medir se hace sobre el **RAW**, que es lo honesto: sin el nitidado ni la reduccion de ruido que la camara aplica al JPG. Pero **previsualizar** un `.ARW` en Finder tarda segundos por foto, y repasar 300 asi es inviable.
>
> Asi que: **se mide el RAW y se enlaza el JPG hermano**. Abren al instante con la barra espaciadora y se pasan con las flechas. El RAW se recupera despues por el nombre, que es el mismo. De eso se encarga `consolidar.py`.

### El flujo de trabajo: tres carpetas y una regla

La parte automatica deja una **propuesta**. Lo que tu haces es corregirla moviendo enlaces entre carpetas en Finder.

| Carpeta | Que hay | Que haces |
|---|---|---|
| `1-seleccion/` | lo que va a revelado | nada, salvo sacar algo que no te guste |
| `2-revisar/` | lo que la maquina no se atreve a juzgar | **dejarla vacia**: cada foto va a 1 o a 3 |
| `3-descartadas/` | borrosas de verdad | ojear por encima, rescatar si algo se salva |

Dentro de `2-revisar/` hay dos motivos distintos, porque se repasan de forma distinta:

- **`a-nitidez-dudosa/`** — salen algo blandas al medirlas pero no lo bastante para tirarlas solas. Se miran una a una.
- **`b-casi-iguales/`** — cada una tiene otra foto casi identica a segundos de distancia. **La mas nitida de cada pareja ya esta en `1-seleccion/`**; estas son las otras. Si la expresion es mejor en esta, la mueves tu y mandas la otra a descartadas. La columna `ParejaDe` del CSV dice con cual va.

La regla es una sola: **`2-revisar/` tiene que acabar vacia.**

Se puede hacer arrastrando enlaces en Finder, pero es mas rapido con `revisar.py` (abajo). Las instrucciones estan tambien en `LEEME.txt` dentro de la propia carpeta.

### `revisar.py`: la app para vaciar `2-revisar`

Repasar 51 fotos arrastrando enlaces en Finder funciona, pero tiene dos problemas serios:

1. **En una vista ajustada a pantalla no se puede juzgar la nitidez.** Para eso hace falta zoom al 100%, y en Finder eso son varios clics por foto.
2. **Para las casi-iguales tienes que ver las dos a la vez**, y estan en carpetas distintas (la mas nitida ya esta en `1-seleccion/`).

La app resuelve las dos cosas. Es **Tkinter**, que viene con el Python del entorno, asi que no hay nada que instalar:

```bash
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/revisar.py "<carpeta de la sesion>"
```

#### Dos modos

**CASI IGUALES** — Muestra **todas** las fotos del grupo lado a lado, no solo la candidata: recupera la que ya estaba en `1-seleccion/` usando la columna `Grupo` del CSV. Marcas con `1` `2` `3` con cuales te quedas (en verde) y confirmas con INTRO. Puedes quedarte con las dos, con una, o con ninguna.

> [!important] El zoom es sincronizado
> Al ampliar, **las dos o tres fotos se amplian al mismo punto a la vez**. Es lo que convierte "comparar dos fotos casi identicas" en algo de un segundo en vez de un ejercicio de memoria. Se pulsa `Z`, o se hace clic donde quieras mirar.

**NITIDEZ DUDOSA** — La foto sola y grande, con el mismo zoom al 100%. `K` conserva, `X` descarta.

#### Por grupo, no por pareja

Lo pense como parejas y acabe haciendolo **por grupo**, porque en esta sesion habia **2 tercetos** ademas de 25 parejas, y un modelo de parejas los habria partido mal. Resultado: las 51 fotos se resuelven en **49 pantallas** (27 grupos + 22 sueltas).

#### Teclas

| | |
|---|---|
| `1` `2` `3` | marcar/desmarcar cada foto del grupo |
| `INTRO` | confirmar el grupo |
| `K` o `->` | conservar (modo suelta) |
| `X` o `<-` | descartar (modo suelta) |
| `Z` / clic | zoom 100%, clic elige el punto |
| `S` | saltar, lo dejo para luego |
| `U` | deshacer la ultima decision |
| `Q` | salir |

#### Detalles de diseno

- **Cada decision se escribe en disco al momento.** Puedes cerrar la app a media faena y retomar: al arrancar lee **donde estan las fotos ahora**, no lo que decia el CSV, asi que da igual si has movido cosas a mano en Finder entre medias.
- **Solo mueve enlaces** dentro de `03-culling/`, con `os.rename`. Si encuentra un archivo real donde esperaba un enlace, se para.
- **Deshacer real**: cada confirmacion guarda los movimientos y `U` los revierte.
- Las marcas vienen **preseleccionadas con la propuesta automatica**, asi que si estas de acuerdo basta con pulsar INTRO.
- Precarga la siguiente pantalla en un hilo aparte. Los JPG de camara son de 8,2 MP y decodifican en **22 ms**, asi que va fluido.

Probado en headless (cola, movimientos, deshacer y los tres modos de pintado) sobre las 326 del Sopar del Soci, con el estado restaurado despues.

### `consolidar.py` cierra el ciclo

Cuando `2-revisar/` esta vacia:

```bash
~/.venvs/foto/bin/python ~/Pictures/Postpro/bin/consolidar.py "<carpeta de la sesion>"
```

Lee como has dejado las carpetas y:

- **Comprueba que estan las 326.** Si falta alguna o alguna aparece dos veces, se para y lo dice.
- **Se niega a seguir si queda algo en `2-revisar/`** (se salta con `--permitir-revisar`, que las trata como descartadas).
- Avisa si Finder ha **copiado** en vez de mover algun enlace.
- Traduce los JPG de `1-seleccion/` a sus **RAW**, y los deja en `04-para-revelar/`, **separados por bloque de luz**, mas un `.txt` con las rutas absolutas.
- Dice **en que te has apartado de la propuesta**: cuantas rescataste y cuantas tiraste.

Probado de punta a punta: con 10 fotos rescatadas de `2-revisar` y el resto descartadas, sale 282 en seleccion y 44 descartadas, las 326 contabilizadas.

### Resultado real del primer pase completo (20-09-2026)

Las 326 del Sopar del Soci pasadas por el flujo entero, con el repaso hecho en `revisar.py`:

| | Propuesta automatica | Despues de tu repaso |
|---|---|---|
| seleccion | 272 | **291** |
| descartadas | 3 | **35** |
| a revisar | 51 | 0 |

**Donde te apartaste de la maquina:** rescataste **24** de las que estaban en `2-revisar`, y **descartaste 5 que la maquina habia dado por buenas** y puesto en `1-seleccion`.

Esas 5 son el dato interesante. Confirman que la banda de *seleccion* no es una decision cerrada sino un punto de partida, y que merece la pena pasar el ojo tambien por ahi. Ninguna medida automatica iba a cazarlas: no eran blandas ni casi-duplicadas, simplemente no valian.

Tiempo total de maquina para las 326: ~8 s de triaje + ~4,5 min de medicion. El repaso manual, 51 fotos en 49 pantallas.

> [!note] Los bloques 01 y 02 comparten estilo de revelado
> El triaje los separa porque tienen distinto `CreativeStyle` (Neutral / Standard), y eso delata un cambio de hueco de dial. Pero **el Creative Style solo afecta al JPG de camara: en el RAW es un metadato que darktable ignora**. Los dos bloques son la misma condicion de luz (ambiente, ISO Auto, 1/100), asi que a la hora de revelar van con **el mismo estilo**.
>
> O sea que aqui hay **dos estilos que construir, no tres**: uno para ambiente (81 fotos) y otro para flash (210).

### ¿Se puede automatizar la exposición, curvas, contraste y luces/sombras?

Pregunta del 20-09-2026, y la respuesta se parte en tres, porque no todo lo que suena parecido lo es.

#### 1. Igualar exposición dentro de un bloque: SÍ, y además hace falta

Esto no es gusto, es medir, así que se automatiza bien. Y los datos de esta sesión dicen que en un bloque hace falta y en el otro no:

| Bloque | Fotos | Rango de exposición (p5-p95) | ¿Normalizar? |
|---|---|---|---|
| **ambiente** | 81 | **0,67 pasos** | no hace falta, el ISO Auto ya igualó |
| **flash** | 210 | **1,34 pasos** (extremos: 2,5) | **sí** |

La diferencia tiene una causa clara: en flash el ISO iba fijo a 1600, así que la exposición de cada foto dependía de a qué distancia estaba la gente del destello. Comprobado además que **el revelado por defecto de darktable no lo arregla**: la más oscura y la más clara entran con 2,5 pasos de diferencia y salen con 2,1.

**La solución no es un script, es un ajuste dentro del estilo.** El módulo `exposición` de darktable tiene modo **`automático`** (parámetros `percentile` y `target level`): mira el histograma de cada foto y calcula su propia corrección. Así **el estilo lleva la regla en vez del número**, y cada una se normaliza sola. Detalle en [[Resources/Photo-Video/darktable-crear-estilos]].

Igual de importante: `denoise (profiled)` **ya se adapta solo al ISO de cada foto**, porque lleva los perfiles de ruido medidos de la a7 IV y lee el EXIF. Un mismo estilo sirve para el bloque de ambiente entero aunque vaya de ISO 500 a 4000.

#### 2. Decidir el look (curvas, contraste, color): NO, y no por una limitación técnica

Aquí el problema no es que la máquina no sepa hacerlo, es que **para una entrega la consistencia vale más que el óptimo por foto**.

291 fotos cada una optimizada por separado quedan **peor como conjunto** que 291 con un mismo criterio, aunque foto a foto alguna gane. El cliente no mira una foto, mira la galería, y lo que salta a la vista es la incoherencia: una con las sombras frías y la siguiente cálidas, una contrastada y la siguiente plana. Un lote coherente con un look imperfecto se lee como un trabajo; un lote de óptimos locales se lee como un desastre.

Por eso el reparto correcto es: **el look se decide una vez a mano y se aplica igual a todas**, y lo que varía por foto es solo lo que se puede medir (exposición, ruido).

#### 3. Un modelo de IA mirando las fotos y decidiendo: no, con este montaje

Ya recogido más arriba en "Dónde no sirve", pero conviene repetirlo aquí porque es la pregunta que uno se hace: sin pantalla calibrada, sin gestión de color y viendo las imágenes a baja resolución, **no se puede validar un tono de piel ni un viraje en las sombras**. Se puede generar una LUT o proponer valores, pero alguien con una pantalla buena tiene que decir si vale. Y ese alguien eres tú.

Los modelos de "mejora automática" tipo un clic existen y funcionan razonablemente en una foto suelta, pero fallan justo en lo que importa aquí: **no son consistentes entre fotos**, que es el problema del punto 2.

> [!important] Resumen en una línea
> Automatiza **lo que se mide** (exposición, ruido), decide a mano **lo que se juzga** (el look), y aplica ese juicio por lotes. Eso ya es el 90% del ahorro de tiempo, y no compra el ahorro a costa de la calidad.

### Lo que sigue sin poder hacer

Todo lo anterior mide, no mira. Que una foto este enfocada no la hace buena: la expresion, el momento y el encuadre no se miden. Por eso la banda *revisar* existe y por eso el descarte es deliberadamente timido.

## Siguiente paso

Orden previsto, de menos a más riesgo:

1. ~~**Triaje por EXIF**~~ → `triaje.py`. **Hecho.**
2. ~~**Culling asistido**~~ → `culling.py`. **Hecho.**
3. ~~**Repasar `2-revisar` con `revisar.py`**~~ y ~~`consolidar.py`~~. **Hecho:** 291 RAW listos en `04-para-revelar/`.
4. **Dos estilos de revelado** (ambiente y flash), construidos a mano en darktable y exportados como `.dtstyle`. Manual paso a paso: [[Resources/Photo-Video/darktable-crear-estilos]]. **Aqui es donde entra el ojo, y es el siguiente paso.**
5. **Revelado por lotes** con `darktable-cli --style`. A 5-7 s por foto son unos 25-30 min para las 291, y se paraleliza.
6. **Entrega**: tamanos con `vips`, metadatos con `exiftool`.

Plan: convertir todo esto en una **skill de Claude** dedicada a esta área, una vez el flujo esté probado sobre una entrega real. La skill documentada irá en `Areas/Claude/Skills/` según la convención del vault.
