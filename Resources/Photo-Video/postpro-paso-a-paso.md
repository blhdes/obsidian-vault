---
title: Postpro paso a paso, de la tarjeta a la entrega
date: 2026-09-21
tags: [photo-video, workflow, darktable, scripting, runbook, referencia]
---

La guía para repetir el proceso completo en cada entrega. Probada de punta a punta con [[Resources/Photo-Video/Sesiones/cosentino-retrato-carolina]] (21-09-2026, ruta A) y con [[Resources/Photo-Video/Sesiones/sopar-del-soci-ctnsc]] (22-09-2026, ruta B).

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
| 5b | Fotogramas de vídeo (opcional) | Claude + **tú** | `fotogramas.py` + `revisar.py` | ~25 min por 100 clips |
| 6 | **A:** construir el estilo · **B:** editar, rechazar y recortar cada foto | **tú**, guiado | darktable | A: 30-45 min · B: según cuántas |
| 7 | Probar el revelado con 1-3 fotos | Claude | `darktable-cli` | 15 s por foto |
| 8 | Revelado por lotes | Claude | **A:** `--style` · **B:** `--library` | ~12-20 s por foto a tamaño completo |
| 9 | Retoques de fotos concretas (solo ruta A) | **tú** + Claude | darktable + `darktable-cli --library` | según cuántas |
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

Doble clic en **Tria** (`~/Applications/Tria.app`) y pulsa *Revisar culling* en la sesión. O por terminal:

```bash
$P $B/revisar.py "$S"
```

Las mismas teclas en el culling, los fotogramas y la entrega (desde el 24-09-2026). **Las flechas solo mueven, nunca deciden.**

| Tecla | Qué hace |
|---|---|
| `←` `→` | otra foto del grupo; en la cuadrícula mueve el marco gris, en la vista grande pasa **con el mismo zoom y punto** para comparar el foco |
| `↑` `↓` | grupo anterior o siguiente, **aunque ya esté decidido**: ahí se puede cambiar |
| `Espacio` | conservar o descartar la foto del marco (`1`-`9`: por número) |
| `Intro` | confirmar el grupo y pasar al siguiente pendiente |
| `Z` o clic | zoom al 100 %; arrastrar o deslizar dos dedos mueve la foto (en la cuadrícula, clic abre en grande) |
| `G` | cuadrícula o vista grande; `Esc` quita el zoom o vuelve |
| `U` / `Q` | deshacer (vuelve a esa pantalla) / salir |

- **Sueltas** (nitidez dudosa): son un grupo de una. Vienen propuestas como descartadas: `Intro` las descarta; `Espacio` + `Intro` las conserva.
- **Grupo sin ninguna:** desmarca todas y pulsa `Intro` dos veces; se descarta el grupo entero.
- Se puede reabrir desde Tria aunque `2-revisar/` ya esté vacía: el botón sale en ámbar, *Repasar*.

La regla: `2-revisar/` tiene que acabar vacía.

### 5 · Consolidar

```bash
$P $B/consolidar.py "$S"
```

Traduce los JPG elegidos a sus RAW y los deja en `04-para-revelar/`. Se puede volver a ejecutar cuando quieras: por ejemplo, si al revelar descartas alguna más.

### 5b · Fotogramas de vídeo (opcional)

Cuando hay pocas fotos y mucho vídeo. Probado por primera vez con [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]] (23-09-2026). Un fotograma 4K son 3840×2160 (8,3 MP): cubre la versión web y un A4, no una ampliación grande.

```bash
V="$HOME/Library/CloudStorage/OneDrive-FF8/photo and video/<carpeta del vídeo>"
$P $B/fotogramas.py analizar "$S" "$V"        # Claude, ~15 s por clip de 10 s
$P $B/revisar.py "$S/fotogramas"              # tú: un grupo por clip
$P $B/fotogramas.py extraer "$S"              # Claude, después de consolidar.py
```

- **analizar** decodifica cada clip a 1280 px sin escribir nada a disco y mide cada fotograma: **nitidez** (laplaciano) y **movimiento** (cuánto cambia respecto a sus vecinos). Saca los 3 mejores de cada clip, separados al menos 1 s, en JPG 4K.
- **revisar**: en **Tria**, botón *Revisar fotogramas* de la sesión (o el comando de arriba). El mejor de cada clip ya viene en verde. Si del clip no quieres ninguno, desmárcalo e `INTRO`. Mira las caras al 100 %: a 1/50 un gesto puede estar movido con el fondo nítido.
- **extraer** saca los elegidos en **TIFF de 16 bits** con su EXIF real (hora al centisegundo, ISO, velocidad, diafragma, perfil sRGB) y los enlaza en `04-para-revelar/V-fotogramas/`. **Si vuelves a pasar `consolidar.py`, vuelve a pasar `extraer`**: consolidar rehace `04-para-revelar/` entero. Los TIFF no se repiten.
- `entregar.py` los numera **por hora de disparo**, intercalados con las fotos.

> [!warning] En darktable, los fotogramas NO llevan el ajuste de los RAW
> El vídeo ya sale "revelado" de la cámara, con su curva de contraste. Si le pegas `sigmoid` o `exposure` en automático, el contraste se aplica dos veces. Darktable abre el TIFF neutro (medido: 3/255 de diferencia con el original). Tocar solo lo que haga falta: `color calibration` para la dominante, `color balance rgb`, `crop`. Con dominantes muy fuertes (el naranja de noche), el **blanco y negro** suele rescatar más que corregir.

> [!note] Lo que se descartó del plan inicial
> - **Extraer todos los fotogramas a TIFF**: ~50 MB cada uno, más de 1 TB por sesión.
> - **Real-ESRGAN** (ampliar con IA): se inventa detalle en caras, y la web va a 2048 px.
> - **LUT de log**: no hace falta, se graba en rec709 estándar.

> [!tip] Ruta A o ruta B: se decide al empezar el paso 6
> - **A · Estilo** (Cosentino): serie homogénea, misma luz en todas. Un ajuste para todas, revelado con `--style`, retoques puntuales después. Pasos 6 a 9 tal cual.
> - **B · Catálogo** (CTNSC): evento con **zonas de luz distintas**, donde un estilo no encaja. Editas, rechazas y recortas cada foto en darktable, y Claude revela todas **una sola vez desde el catálogo**. No hace falta exportar estilo ni paso 9. Ver [[#6-8 · Ruta B, revelado desde el catálogo]].

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

### 6-8 · Ruta B, revelado desde el catálogo

**Tú, en darktable:**

1. Importar los bloques de `04-para-revelar/`. Hacer un ajuste base en una foto, **con los mismos módulos y en el mismo orden que en la ruta A** (paso 6.4: `exposure`, `color calibration`, `sigmoid`, `local contrast`), y pegarlo a todas (*history stack → copy / paste*; en *selective copy*, solo los módulos tocados).
   > [!note] Hueco detectado el 22-09-2026
   > En CTNSC este paso no enumeraba los módulos y `sigmoid` no se ajustó en el ajuste base: 86 de las 104 entregadas salieron con el contraste por defecto de darktable (1,5), y solo 18 se retocaron a mano (1,47-1,93). Cosentino quedó en 1,88 y Rodri en 1,76.
2. **Segundo culling:** `R` rechaza la foto; `R` otra vez, `Cmd+Z` o `0` lo deshacen. Nunca *remove* ni *delete*.
3. Ajustar cada foto que lo pida: `crop` (en *aspect*, `original image` mantiene el 3:2), `rotate and perspective` (clic derecho y arrastrar sobre una línea que debería ser recta), exposición, etc.
4. **Cerrar darktable.** Y no abrirlo mientras Claude revela: bloquea la configuración y el revelado falla.

**Claude:**

- Lee del catálogo las fotos **no rechazadas** (`flags & 8 = 0`) y las revela una a una con `--library` sobre **una copia** del catálogo, a `05-reveladas/`. Las verticales y los recortes salen como en la app sin hacer nada.
- **La prueba (paso 7)** compara 3 fotos (una vertical, una recortada, una normal) con las miniaturas que guarda darktable en `~/.cache/darktable/mipmaps-*.d/`. Ojo: esas miniaturas están en **Adobe RGB**, hay que pasarlas a sRGB antes de comparar. En CTNSC el color y el brillo medios coincidieron a 1 nivel sobre 255; el resto de diferencia es detalle fino, porque la miniatura se calcula a tamaño reducido.
- El bloque sobrante se puede borrar de `04-para-revelar/`: son enlaces. Pero **no** los enlaces de las rechazadas, que darktable los sigue mostrando.

### 10 · Elegir la entrega, tú

En **Tria**, *Elegir entrega*: al lado se pone cuántas quieres entregar y, si la entrega ya está generada, se marca *versión web* (va mucho más rápido). O por terminal:

```bash
$P $B/seleccionar.py "$S" --objetivo 6
```

| Tecla | Qué hace |
|---|---|
| `←` `→` | pasar foto; en la cuadrícula mueve el marco gris |
| `↑` `↓` | en la cuadrícula, fila de arriba o de abajo |
| `Espacio` | elegir o quitar (marco verde), también desde la cuadrícula |
| `Intro` | en la cuadrícula, abre la foto del marco en grande |
| `Z` o clic | zoom al 100 % en ese punto; arrastrar o dos dedos mueve la foto; `Esc` vuelve |
| `G` | cuadrícula con todas: sirve para ver el conjunto, sin dos casi iguales y con variedad de planos |
| `E` | solo las elegidas, para recortar la lista |
| `U` / `Q` | deshacer / salir |

Cada marca es un enlace en `06-entrega/seleccion/` y se guarda al momento.

**En eventos se hace al revés:** se entrega casi todo, así que Claude enlaza todas en `seleccion/`, genera la entrega (paso 11) y abre la app con **`--previa --objetivo <total>`**. Todas empiezan marcadas en verde y se desmarca lo que sobra. `--previa` muestra la versión web ya generada, mucho más ligera; el zoom llega entonces a 2048 px. Después, `entregar.py --rehacer` renumera sin huecos. En CTNSC: 114 → 104.

### 11 · Impresión y web

```bash
$P $B/entregar.py "$S" --nombre "<Cliente-Sesion>"
```

| Versión | Tamaño | Formato | Metadatos |
|---|---|---|---|
| `impresion/` | completo (7032×4688) | JPG q95 sRGB, **copia exacta** del revelado, sin recomprimir | autor, copyright, fecha y datos de cámara copiados del RAW |
| `web/` | lado largo 2048 px | JPG q85 sRGB | solo autor, copyright y perfil de color |

**Si la entrega es sobre todo web** (eventos), la impresión no hace falta a tamaño completo: **`--imp 4000 --q-imp 90`** la saca a 4000 px de lado largo, calidad 90 (~2,3 MB por foto frente a ~10 MB). Cubre un A4 a 300 ppp, que necesita 3508 px. Los recortes que midan menos no se amplían.

**Sin marcas de agua visibles**, por decisión propia: la firma va solo en los metadatos. Los archivos se llaman `<Nombre>-01.jpg`, `-02`… en orden de disparo, o `-001`, `-002`… si hay más de 99. `indice.csv` dice qué RAW hay detrás de cada uno. Si hay que rehacerlo, añade `--rehacer`: solo borra lo que el propio script generó.

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
| Qt (PySide6) | **Tria**: el menú (`tria.py`) y las dos operaciones, `revisar.py` y `seleccionar.py`, con el visor común `visor.py`. Se abre con doble clic desde `~/Applications/Tria.app`, que solo llama al Python del venv. Desde el 22-09-2026: con Tk el arrastre iba a ~7 fotogramas por segundo en esta Mac |

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
