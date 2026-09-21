---
title: Postpro paso a paso, de la tarjeta a la entrega
date: 2026-09-21
tags: [photo-video, workflow, darktable, scripting, runbook, referencia]
---

La guía para repetir el proceso completo en cada entrega. Probada de punta a punta con [[Resources/Photo-Video/Sesiones/cosentino-retrato-carolina]] (21-09-2026).

- El porqué de cada pieza: [[Resources/Photo-Video/automatizar-postproduccion-scripting]]
- El manual de darktable, con capturas mentales de cada módulo: [[Resources/Photo-Video/darktable-crear-estilos]]

> [!tip] Cómo usarla
> Dile a Claude *"vamos a aplicar el proceso de postpo a <sesión>"*. Esta nota es el guion: cada paso dice **quién** lo hace. Lo tuyo es mirar y decidir; lo de Claude es medir, mover y revelar.

## De un vistazo

| # | Paso | Quién | Herramienta | Tiempo real |
|---|---|---|---|---|
| 1 | Copia de la tarjeta + checksums | Claude | `cp` + `md5` | según tarjeta |
| 2 | Triaje por huella de EXIF | Claude | `triaje.py` | segundos |
| 3 | Culling asistido | Claude | `culling.py` | 17 s (24 fotos), 4,5 min (326) |
| 4 | Vaciar `2-revisar/` | **tú** | `revisar.py` | minutos |
| 5 | Consolidar la selección | Claude | `consolidar.py` | segundos |
| 6 | Construir el estilo de revelado | **tú**, guiado | darktable | 30-45 min la primera vez |
| 7 | Probar el estilo con 1 foto | Claude | `darktable-cli` | 15 s |
| 8 | Revelado por lotes | Claude | `darktable-cli --style` | ~12 s por foto a tamaño completo |
| 9 | Retoques de fotos concretas | **tú** + Claude | darktable + `darktable-cli --library` | según cuántas |
| 10 | Elegir las que se entregan | **tú** | `seleccionar.py` | minutos |
| 11 | Versiones de impresión y web | Claude | `entregar.py` | segundos |
| 12 | Subir a Google Drive y sacar el enlace | Claude | `rclone` | segundos |

## Las reglas que no se tocan

- **La carpeta de OneDrive es de solo lectura.** Es el archivo con checksums. Nada escribe ahí, tampoco darktable (ver paso 6).
- **Todo lo intermedio son enlaces simbólicos.** Organizar no duplica gigas, y borrar un enlace no borra ninguna foto.
- **Cada script verifica al terminar** que no falta ni sobra ninguna foto, y se para si encuentra un archivo real donde esperaba un enlace.
- **Lo que se juzga lo decides tú; lo que se mide lo hace la máquina.** El look se decide una vez y se aplica igual a todas.

## Carpetas de una sesión

```
~/Pictures/Postpro/<fecha> - <Cliente> - <Descripción>/
  00-manifiesto.csv     EXIF de cada foto + bloque (triaje)
  01-triaje/            enlaces a los RAW, un bloque por perfil de dial
  02-medidas.csv        nitidez, brillo, hash (culling)
  03-culling/           1-seleccion / 2-revisar / 3-descartadas (enlaces a JPG)
  04-para-revelar/      enlaces a los RAW elegidos, por bloque
  estilos/              el .dtstyle exportado desde darktable
  05-reveladas/         JPG revelados (archivos reales)
  06-entrega/
    seleccion/          enlaces a las elegidas para el cliente
    <Nombre> - impresion/
    <Nombre> - web/
    indice.csv          qué RAW hay detrás de cada archivo entregado
```

## Los pasos, con los comandos

Variables que usan todos los comandos:

```bash
O="$HOME/Library/CloudStorage/OneDrive-FF8/photo and video/<carpeta de la sesión>"
S="$HOME/Pictures/Postpro/<carpeta de la sesión>"
P=~/.venvs/foto/bin/python
B=~/Pictures/Postpro/bin
```

### 1 · Copia de la tarjeta

Una carpeta por sesión en OneDrive: `<AAAA-MM-DD> - <Cliente> - <Descripción>/`. Si la tarjeta tiene varias sesiones, se separan por los huecos de hora del EXIF. Se verifica el MD5 de origen contra destino y se guarda en `checksums-md5.txt`.

> [!warning] Usar `cp`, no `rsync`
> `rsync` no puede escribir en la carpeta de OneDrive (EPERM) aunque Terminal tenga acceso total al disco. `cp` sí puede.

### 2 · Triaje

```bash
$P $B/triaje.py "$O"
```

Separa las fotos por perfil de dial. **Mirar el tramo horario:** en Cosentino había 3 pruebas de flash hechas en casa a las 09:xx, dos horas antes de la sesión. El triaje no las distingue porque tenían la misma configuración, así que se descartan a mano en el paso 4.

### 3 · Culling

```bash
$P $B/culling.py "$S"
```

> [!note] En retratos de ambiente, la "nitidez dudosa" suele ser falsa alarma
> La nitidez se mide sobre toda la foto. En Cosentino, los planos abiertos con estanterías daban ~1100 y los cerrados ~170, y las dos cosas estaban bien enfocadas. Mirar **los ojos al 100 %** antes de descartar.

### 4 · Vaciar `2-revisar/`, tú

```bash
$P $B/revisar.py "$S"
```

`1` `2` `3` marcan cuál te quedas de cada grupo y `INTRO` confirma. `K` conserva, `X` descarta, `Z` o clic hace zoom al 100 %, `U` deshace. La regla: `2-revisar/` tiene que acabar vacía.

### 5 · Consolidar

```bash
$P $B/consolidar.py "$S"
```

Traduce los JPG elegidos a sus RAW y los deja en `04-para-revelar/`. Se puede volver a ejecutar cuando quieras: por ejemplo, si al revelar descartas alguna más.

### 6 · El estilo, tú en darktable

Manual completo: [[Resources/Photo-Video/darktable-crear-estilos]]. Resumen de lo que se hace:

1. **Solo la primera vez:** en *preferences → storage*, pon **create XMP files: `never`**. Si no, darktable escribe un `.xmp` junto a cada foto y rompe la regla de solo lectura.
2. **Importar** desde `04-para-revelar/<bloque>/` (*import → add to library*). Los enlaces funcionan.
3. **Elegir la foto de trabajo:** una **del montón**, no la mejor. Sirve una con el brillo en la mitad del bloque; Claude la saca de `02-medidas.csv`.
4. **Ajustar**, en este orden:
   - `exposure` en **automatic**
   - `color calibration` con el cuentagotas sobre algo blanco neutro
   - `sigmoid`
   - `denoise (profiled)` solo si se nota el ruido
   - `local contrast`
5. **Copiar y pegar** el historial al resto (*history stack → copy / paste*) y revisar **las extremas**: la más oscura, la más clara y las que tengan una composición rara.
6. **`compress history`** en la foto de trabajo. **Sin este paso el estilo sale mal** (ver el manual).
7. **Crear el estilo** (*styles → create*) marcando solo los módulos que has tocado, y **exportarlo** a `estilos/`.
8. **Cerrar darktable.** Mientras está abierto, `darktable-cli` no puede usar la base de datos.

### 7 · Probar el estilo con una foto

Claude revela la foto de trabajo **con el estilo**, y otra vez **con tu edición de la app**, y las compara píxel a píxel. Tienen que salir idénticas.

```bash
T=<carpeta temporal>
darktable-cli "$S/04-para-revelar/<bloque>/<foto>.ARW" "$T/estilo.jpg" \
  --style "<nombre del estilo>" --style-overwrite --core --disable-opencl
cp ~/.config/darktable/library.db "$T/library-copia.db"
darktable-cli "$S/04-para-revelar/<bloque>/<foto>.ARW" "$T/app.jpg" \
  --library "$T/library-copia.db" --core --disable-opencl
```

En Cosentino la diferencia fue **0,00**. Con los ajustes de serie de darktable la diferencia es de ~5,8, así que el test distingue bien.

### 8 · Revelado por lotes

```bash
darktable-cli "$S/04-para-revelar/<bloque>" "$S/05-reveladas" \
  --style "<nombre del estilo>" --style-overwrite --core --disable-opencl
```

Sin `--width` sale a tamaño completo (7032×4688); los tamaños se hacen en el paso 11. Hay un comando por bloque y por estilo.

> [!warning] Las opciones van ANTES de `--core`
> Todo lo que va detrás de `--core` se pasa a darktable, no a `darktable-cli`. Un `--library` puesto detrás de `--core` no hace lo que parece.

### 9 · Retoques de fotos concretas

Para las pocas fotos que no encajan con la regla del estilo. En Cosentino fueron la 01400 a la 01403: la cara salía oscura porque entraba mucha pared blanca en el encuadre.

1. **Tú:** en darktable, editas esa foto. Ya tiene el ajuste del paste del paso 6. Si son varias parecidas, usa *selective copy* para pasar solo lo que has cambiado. Luego cierras darktable.
2. **Claude:** las revela leyendo tu catálogo y sustituye su versión en `05-reveladas/`, guardando antes la versión anterior:

```bash
cp ~/.config/darktable/library.db "$T/library-copia.db"
darktable-cli "$S/04-para-revelar/<bloque>/<foto>.ARW" "$T/<foto>.jpg" \
  --library "$T/library-copia.db" --core --disable-opencl
```

Se trabaja siempre sobre **una copia** del catálogo, para no tocar el de verdad.

### 10 · Elegir la entrega, tú

```bash
$P $B/seleccionar.py "$S" --objetivo 6
```

| Tecla | Qué hace |
|---|---|
| `←` `→` | pasar foto |
| `ESPACIO` o `K` | marcar o desmarcar (marco verde) |
| `Z` o clic | zoom al 100 % en ese punto; `ESC` vuelve |
| `G` | cuadrícula con todas: sirve para ver el conjunto, sin dos casi iguales y con variedad de planos |
| `E` | solo las elegidas, para recortar la lista |
| `U` / `Q` | deshacer / salir |

Cada marca es un enlace en `06-entrega/seleccion/` y se guarda al momento.

### 11 · Impresión y web

```bash
$P $B/entregar.py "$S" --nombre "<Cliente-Sesion>"
```

| Versión | Tamaño | Formato | Metadatos |
|---|---|---|---|
| `impresion/` | completo (7032×4688) | JPG q95 sRGB, **copia exacta** del revelado, sin recomprimir | autor, copyright, fecha y datos de cámara copiados del RAW |
| `web/` | lado largo 2048 px | JPG q85 sRGB | solo autor, copyright y perfil de color |

**Sin marcas de agua visibles**, por decisión propia: la firma va solo en los metadatos. Los archivos se llaman `<Nombre>-01.jpg`, `-02`… en orden de disparo. `indice.csv` dice qué RAW hay detrás de cada uno. Si hay que rehacerlo, añade `--rehacer`: solo borra lo que el propio script generó.

> [!note] Por qué sRGB también para imprimir
> Si la imprenta no lo pide expresamente, sRGB es lo más seguro: un AdobeRGB abierto en un programa sin gestión de color se ve apagado. Y en tonos de piel, madera o piedra no se nota diferencia. Si lo piden, se revela otra vez desde el RAW con `--icc-type ADOBERGB`.

### 12 · Enviar: Google Drive + enlace

```bash
N="<Cliente-Sesion>"
for v in impresion web; do
  rclone copy "$S/06-entrega/$N - $v" "gdrive:Entregas/$N/$N - $v"
  rclone check "$S/06-entrega/$N - $v" "gdrive:Entregas/$N/$N - $v"   # MD5 local = Drive
done
rclone link "gdrive:Entregas/$N"    # enlace de solo lectura para el cliente
```

- El remoto `gdrive` apunta a **agomezurrea@gmail.com**, configurado el 21-09-2026 con permiso mínimo (`scope=drive.file`): rclone solo ve los archivos que ha subido él.
- El enlace no caduca. Para retirarlo, borra la carpeta en Drive o quita el acceso público desde la web.

> [!warning] Caduca en 2026: el `client_id` compartido de rclone
> rclone avisa de que el acceso compartido que usa para hablar con Google deja de funcionar en algún momento de 2026. Para evitarlo hay que crear un `client_id` propio en Google Cloud: es gratis y se hace una sola vez, en ~10 min. Guía: https://rclone.org/drive/#making-your-own-client-id

## Referencia: lo usado hasta ahora

### Herramientas

| Herramienta | Qué hace en el flujo |
|---|---|
| `exiftool` | lee el EXIF para el triaje; firma autor y copyright en la entrega |
| `rawpy` (Python) | decodifica los RAW para medir nitidez y brillo en el culling |
| darktable (app) | donde se decide el look: se construye el estilo y se hacen los retoques puntuales |
| `darktable-cli` | aplica el estilo por lotes y revela los retoques leyendo el catálogo |
| `vips` | genera la versión web, rápido y sin cargar la imagen entera en memoria |
| Tkinter (Python) | las apps `revisar.py` y `seleccionar.py` |

### Módulos de darktable usados

Los valores son los de Cosentino (retrato interior, flash rebotado, ISO 400). Son un punto de partida, no una receta.

| Módulo | Qué hace | Cómo se usó |
|---|---|---|
| `exposure` en **automatic** | lleva un percentil del histograma a un brillo objetivo, **foto a foto** | percentil 50 %, *target level* -3,03 EV |
| `color calibration`, pestaña CAT | corrige la dominante de color de la luz | cuentagotas sobre la pared blanca → *illuminant custom* (~4380 K) |
| `sigmoid` | reparte la luz entre sombras y luces: el contraste general | *contrast* 1,884; *skew* -0,23 |
| `denoise (profiled)` | quita ruido según el ISO de cada foto | **apagado**: a ISO 400 no se notaba |
| `local contrast` | contraste en los detalles; da volumen | *detail* 89 % (por debajo de 100 suaviza la piel), *shadows* 69 %, *highlights* 44 % |
| `vignetting` | oscurece los bordes | solo en 4 retocadas, para que la cara destaque sobre la pared |

### Todavía sin usar

Para ediciones más avanzadas, cuando toque:

- **`color balance rgb`**: saturación y virado de color por separado en sombras, medios tonos y luces. Es el módulo para "dar un look".
- **`tone equalizer`**: aclarar o oscurecer por zonas de brillo. Por ejemplo, levantar solo las sombras de una cara sin tocar la pared.
- **Máscaras** (dibujadas o paramétricas): aplicar cualquier módulo a una sola parte de la foto.
- **`retouch`**: quitar manchas, reflejos o elementos pequeños.
- **`lens correction`**: corrige la distorsión y el viñeteado del objetivo con el perfil del 28-70.
- **`crop` / `rotate and perspective`**: encuadre y verticales. Van foto a foto, **nunca en el estilo**.
- **`lut 3D`**: aplicar un look generado por script. Es el puente entre una descripción en texto y un revelado.
