---
title: DaVinci Resolve, primera edición de vídeo (Los Antonios)
date: 2026-09-24
tags: [photo-video, video, davinci-resolve, edicion, color, tutorial, runbook]
---

Manual para el primer montaje con DaVinci Resolve, pensado para el encargo de [[Resources/Photo-Video/Sesiones/los-antonios-valencia-barcelona]]. Solo lo esencial: montar, corregir el color, fundidos, música y exportar.

- **Software:** DaVinci Resolve **21.1.0**, versión **gratuita**, instalada en `/Applications/DaVinci Resolve/` (comprobado el 24-09-2026).
- **Máquina:** iMac **M1 con 8 GB** de RAM. Condiciona el flujo: ver [[Resources/Photo-Video/automatizar-video-scripting]].
- **Fuente:** el manual oficial de la versión 21.1, que viene con la app: `/Applications/DaVinci Resolve/DaVinci Resolve Manual.pdf`. Cada paso cita su capítulo y página, por si quieres ampliar.
- La interfaz está **en inglés**: los nombres entre `comillas` son los que salen en pantalla.

## Lo que pide el cliente

Del correo de Los Antonios (15-09-2026):

| Pieza | Duración | Para qué | Formato de salida |
|---|---|---|---|
| **Vertical** | ~30 s | Reels, Stories, TikTok | 1080×1920, 25p, MP4 H.264 |
| **Horizontal** | ~60 s | archivo de marca, web, YouTube, presentaciones | 3840×2160 (4K), 25p, MP4 H.264 |

- **"Alta calidad"** y **cesión de derechos** para publicidad, redes y web. Esto afecta a la música: ver paso 7.
- **Estética pedida:** *"premium, mediterránea, auténtica, emocional y contemporánea"*, y que **no parezca simplemente el vídeo de una actuación musical**: *"contar historias y transmitir experiencia de marca"*.

> [!tip] Qué significa en la práctica "no parecer una actuación"
> Alternar la banda con lo que provoca: invitados bailando, manos, miradas, detalles del sitio, la pareja. La música es el hilo, pero la historia son las personas. Un orden que funciona: **llegada y ambiente → detalles → la banda → la gente reaccionando → un cierre emocional**.

## El material

107 clips, 16,5 min, en OneDrive: `…/2026-09-19 - Los Antonios - Boda Fran y Elena Valencia (vídeo)/`.

| Dato | Valor | Qué implica |
|---|---|---|
| Vídeo | H.264 **High 4:2:2 10 bits**, 3840×2160, **25p**, 140 Mb/s | pesado de reproducir en un M1 base: **proxies** (paso 2) |
| Color | **rec709** (perfil estándar, no log) | se corrige directamente, sin LUT de conversión |
| Audio | PCM estéreo 48 kHz, micro de cámara | sirve como sonido ambiente y de la banda |
| Luz | día neutro; **dominante naranja fuerte desde las 19:14** (`C0407` en adelante) | esos clips piden corrección fuerte o blanco y negro (paso 5) |

**Carpeta de trabajo** (nada se escribe en OneDrive, que es el archivo):

```
~/Pictures/Postpro/2026-09-19 - Los Antonios - Boda Fran y Elena Valencia/07-video/
  proxies/     copias ligeras para editar (las genera Resolve)
  musica/      pistas de audio extra, si las hay
  exportes/    los dos MP4 finales
```

## Las páginas de Resolve

Abajo de la ventana hay una fila de iconos: cada uno es una "página" con un trabajo. Solo usaremos cuatro:

| Página | Para qué |
|---|---|
| **Media** | importar clips y generar proxies |
| **Edit** | montar: ordenar, cortar, fundidos, audio |
| **Color** | corregir y dar look |
| **Deliver** | exportar |

## Paso 1 · Crear el proyecto (antes de importar nada)

`File → Project Settings…` (o el engranaje abajo a la derecha). En **Master Settings**:

| Ajuste | Valor | Por qué |
|---|---|---|
| `Timeline resolution` | **3840 x 2160 Ultra HD** | la resolución de la pieza horizontal |
| `Timeline frame rate` | **25** | la de los clips. **No se puede cambiar después de importar** (cap. 6, p. 141) |
| `Playback frame rate` | 25 | |
| `Proxy media resolution` | **Half** (1920×1080) | ligera para el M1, suficiente para juzgar |
| `Proxy media format` | **ProRes 422 Proxy** | formato que el M1 reproduce con soltura |
| `Proxy generation location` (en *Working Folders*) | `…/07-video/proxies` | fuera de OneDrive |

En **Image Scaling → Input Scaling**: `Mismatched resolution files` → **`Scale full frame with crop`**. Así, en el timeline vertical el clip llena la pantalla recortando los lados, en lugar de dejar bandas negras (cap. 6, p. 148).

`Save`.

## Paso 2 · Importar y crear proxies

1. Página **Media**: arrastra la carpeta de vídeo de OneDrive al panel `Media Pool` (abajo). Si pregunta por el frame rate, acepta el cambio a 25.
2. **Prueba primero un clip:** doble clic en `C0400` y dale al play. Tiene que verse. Irá a tirones: normal, para eso son los proxies.
3. Selecciona todos los clips (`Cmd+A`), clic derecho → **`Generate Proxy Media`**. Resolve muestra una barra de progreso con el tiempo estimado (cap. 8, p. 208). Son unos 5-6 GB.
4. Arriba a la derecha del visor, el selector **`Proxy Handling`**: que esté en usar proxies. Es global para toda la app (cap. 8, p. 209).

> [!warning] Si un clip no se ve (pantalla negra o "Media Offline")
> La lista oficial de códecs dice que en Mac se descodifica "H.264 (Sony XAVCs)", pero no separa versión gratuita y Studio. Si falla, el plan B es convertir con `ffmpeg` a ProRes antes de importar: el comando está en [[Resources/Photo-Video/automatizar-video-scripting]]. Dímelo y lo lanzo.

**Al exportar, Resolve vuelve a los originales 4K** (paso 9). Los proxies son solo para trabajar con fluidez.

## Paso 3 · Seleccionar los planos buenos

En **Media** o **Edit**, abre cada clip y marca el trozo útil:

- `I` = punto de entrada, `O` = punto de salida.
- Arrastra del visor al timeline solo ese trozo.
- **Clips de 2 a 4 s** en la pieza de 60 s; **1,5 a 3 s** en la de 30 s. Las redes premian el ritmo.

## Paso 4 · Montar la pieza horizontal (60 s)

Página **Edit**.

1. `File → New Timeline`, nombre `Horizontal 60s`.
2. Arrastra los planos en el orden de la historia.
3. **Cortar:** coloca el cabezal (la línea roja) y `Timeline → Split Clips` (**`Cmd+\`**) (cap. 23, p. 533). Borra el trozo sobrante con `Delete`.
4. **Transiciones:** casi todo corte seco. Un fundido cruzado solo para cambios de momento: `Effects → Video Transitions → Cross Dissolve`, arrastrado entre dos clips.
5. La duración total aparece arriba a la derecha del timeline. Objetivo: 55-65 s.

## Paso 5 · Color

Página **Color**. Trabaja **clip a clip** en la tira de miniaturas de arriba.

### 5.0 · Primero, los scopes

`Workspace → Video Scopes → On` (`Cmd+Shift+W`) y elige **Waveform** (forma de onda). Muestra el brillo de la imagen de abajo (negro, 0) a arriba (blanco, 1023). Tu pantalla engaña, el scope no (cap. 127).

- Nada pegado arriba del todo (luces quemadas) ni amontonado abajo (sombras aplastadas), salvo que lo busques.
- Las caras suelen caer hacia el **60-70 %** de la escala.

### 5.1 · El nodo de corrección (uno por clip)

En Resolve los ajustes viven en **nodos** (cajitas en el panel `Nodes`, arriba a la derecha). Cada clip trae uno, el `01`. Úsalo para **corregir**, en este orden, desde la paleta **`Primaries`** (cap. 131, pp. 3141-3146):

| # | Qué | Control | Cómo |
|---|---|---|---|
| 1 | **Balance de blancos** | cuentagotas **White Balance**, abajo a la izquierda de la paleta | clic en algo que deba ser blanco y no esté quemado: una camisa, un mantel (cap. 131, p. 3127) |
| 1b | … o a mano | **`Temp`** (−4000 a +4000) y **`Tint`** (−100 a +100) | `Temp` negativo enfría (quita naranja), positivo calienta. `Tint` corrige verde/magenta |
| 2 | **Exposición** | ruedas **`Lift`** (sombras), **`Gamma`** (medios), **`Gain`** (luces), o **`Offset`** (todo a la vez) | gira el **anillo** bajo cada rueda, no el punto del centro (el punto cambia el color) |
| 3 | **Contraste** | **`Contrast`** + **`Pivot`** | `Contrast` separa claros y oscuros. `Pivot` decide el punto de giro: bájalo en planos oscuros para no aplastar las sombras |
| 4 | **Luces / sombras** | **`Highlights`** y **`Shadows`** (−100 a +100) | `Highlights` negativo recupera un cielo o un vestido quemado. `Shadows` positivo abre las sombras |
| 5 | **Color** | **`Color Boost`** y **`Sat`** | `Color Boost` es la *vibrance*: satura sobre todo lo apagado y respeta la piel. `Sat` (50 = sin cambio) sube todo por igual |

**Para copiar la corrección** a un clip rodado igual, selecciónalo y pulsa **`=`**: copia el grade del clip anterior (cap. 142, p. 3364). Luego retoca lo que haga falta.

### 5.2 · El nodo de look (compartido por todos)

El look va **separado** de la corrección, para poder cambiarlo en todos los clips a la vez.

1. Con el nodo `01` seleccionado, **`Option+S`** (o `Color → Nodes → Add Serial Node`). Sale el nodo `02`, detrás del `01` (cap. 143).
2. Ajusta el look en ese nodo (valores abajo).
3. Clic derecho en el nodo `02` → **`Save as Shared Node`**. Queda bloqueado para no tocarlo por error (cap. 142, pp. 3373-3374).
4. En cada clip: clic derecho en el panel `Nodes` → añade ese Shared Node detrás de su corrección.

**Punto de partida para "premium, mediterráneo, cálido pero natural":**

| Control | Valor | Efecto |
|---|---|---|
| `Temp` | **+200 a +400** | calidez suave, luz de tarde |
| `Contrast` | **1,05 a 1,10** | algo más de cuerpo, sin dureza |
| `Highlights` | **−10 a −20** | luces más suaves, "caras" |
| `Color Boost` | **+10 a +20** | vida sin saturar la piel |
| `Sat` | **50 a 55** | casi neutro |

Son puntos de partida, no una receta: juzga con los scopes y con la piel.

> [!warning] Los clips de noche (desde las 19:14)
> Llevan una dominante naranja muy fuerte (medida: rojo 9-10 veces el azul). El cuentagotas mejora algo, pero no hace milagros. Si la piel sigue naranja, el **blanco y negro** (`Sat` a 0 en el nodo de corrección, algo más de `Contrast`) rescata más que corregir, y enlaza con las fotos en B/N de la entrega: [[Resources/Photo-Video/darktable-blanco-y-negro]].

## Paso 6 · Fundidos de entrada y salida

Página **Edit**.

- **Vídeo:** pasa el ratón por encima del primer clip. En las esquinas superiores aparecen unos **tiradores blancos** (*fader handles*). Arrastra el de la izquierda hacia dentro para un fundido desde negro, y el de la derecha del último clip para uno a negro (cap. 57, p. 1204).
- Alternativa precisa: coloca el cabezal y `Trim → Fade In to Playhead` / `Fade Out to Playhead`.
- **Audio:** los clips de audio tienen los mismos tiradores en sus esquinas (cap. 52, p. 1113). Haz coincidir el fundido de audio con el de vídeo.
- **Duración orientativa:** entrada 0,5-1 s; salida 1-2 s. En la vertical, la entrada más corta o ninguna: en redes los primeros frames tienen que enganchar.

## Paso 7 · Audio y música

**El sonido principal ya lo tienes:** Los Antonios son una banda, y el audio de cámara recoge su música en directo. Para "contar su marca", su propia música es lo más coherente.

**Si se añade música extra:**

- **Tiene que tener licencia de uso comercial.** El cliente se queda los derechos para publicidad y web, así que una canción comercial cualquiera no vale: puede provocar bloqueos en YouTube o en Instagram. La mejor opción: **pedir a Los Antonios la grabación de estudio de una canción suya**. Si no, una librería con licencia comercial explícita.
- Arrastra el archivo a `07-video/musica/`, impórtalo y ponlo en la pista **A2**. El audio de cámara queda en A1, más bajo (clic en el clip → `Inspector → Volume`).
- Fundido de salida en la música (paso 6).

**Nivelar el volumen:** selecciona todos los clips de audio → clic derecho → **`Normalize Audio Levels`**. Elige un estándar de sonoridad (*loudness*) y el objetivo de **−14 LUFS**, que es el de YouTube según el manual (cap. 52, p. 1110; cap. 177, p. 3968). LUFS mide lo fuerte que *suena* algo, no solo sus picos.

## Paso 8 · La pieza vertical (30 s)

Se hace **a partir de la horizontal**: mismo color, otra forma.

1. Selecciona el timeline `Horizontal 60s` en el `Media Pool` → `Edit → Duplicate Timeline`. Renómbralo `Vertical 30s`.
2. Clic derecho en él → `Timelines → Timeline Settings…` → desmarca **`Use Project Settings`** → pon **1920 x 1080** y marca **`Use vertical resolution`** (cap. 6, p. 141; cap. 41, p. 838). Queda en 1080×1920.
3. Con el ajuste del paso 1, cada clip llena la pantalla vertical, pero solo se ve la **franja central**.
4. **Reencuadra clip a clip:** selecciona el clip → `Inspector → Transform → Position X` para mover la franja hasta el sujeto. Puedes ampliar con `Zoom` hasta **~1,1** sin perder nitidez, porque el 4K tiene margen.
5. **Recorta a 30 s**: quédate con los planos más fuertes y un ritmo más rápido.
6. **Zonas seguras:** la interfaz de Reels/TikTok tapa **la parte de abajo** (texto y botones) y **el lateral derecho** (iconos). Deja caras y textos en el centro. `View → Safe Area` superpone las zonas seguras en el visor.

> [!note] El reencuadre automático es solo de Studio
> *Smart Reframe* no está en la versión gratuita. Con 15-20 planos, a mano son unos 20 min.

## Paso 9 · Exportar

Página **Deliver**. Arriba a la izquierda, los presets (cap. 187, pp. 4104-4105):

| Pieza | Preset | Ajustes a revisar |
|---|---|---|
| Horizontal | **`YouTube`** → **2160p** | MP4, H.264, 25p. **`Use Proxy Media` desmarcado** |
| Vertical | **`TikTok`** → **1080p** | **`Use Vertical Resolution` marcado**. **`Use Proxy Media` desmarcado** |

- **`Use Proxy Media` siempre desmarcado:** si no, exporta desde las copias ligeras y pierdes la calidad 4K.
- No marques las casillas de subir a YouTube o TikTok: la entrega va por Drive.
- `Location` → `…/07-video/exportes/`. Nombres: `Boda-Fran-Elena-horizontal-60s` y `Boda-Fran-Elena-vertical-30s`.
- `Add to Render Queue` con cada timeline → **`Render All`**.

**Entrega:** los dos MP4 van a la carpeta del cliente en Drive, `2. BODA VALENCIA - FRAN & ELENA - MASIA DEL CARMEN/VÍDEOS/`. Pesan poco y caben en tu cuota. Lo hace Claude con `rclone` (ver [[Resources/Photo-Video/postpro-paso-a-paso#12 · Enviar: Google Drive + enlace]]).

## Antes de entregar: comprobación

- [ ] Duraciones: ~60 s y ~30 s.
- [ ] Resolución: 3840×2160 y 1080×1920, a 25p.
- [ ] Ningún clip con dominante que salte respecto al de al lado.
- [ ] Fundidos de entrada y salida, en vídeo y audio.
- [ ] Sin cortes de audio bruscos y sin picos que saturen.
- [ ] Exportado **desde originales**, no desde proxies.
- [ ] Ver cada MP4 entero una vez, en el móvil para la vertical.

## Límites de la versión gratuita que nos afectan

| Función | Para qué sería | Alternativa |
|---|---|---|
| **Film Look Creator** | look de película (grano, halación) | nodo de look a mano (paso 5.2) |
| **Smart Reframe** | vertical automático | reencuadre a mano (paso 8) |
| **Scene Cut Detection** | detectar cortes | no hace falta: los clips ya vienen separados |
| API de scripting externa | automatizar desde Python | la automatización vive fuera, en `ffmpeg` |

Con 8 GB de RAM: **cierra el resto de apps** mientras editas, sobre todo Chrome y darktable.

## Fuentes

- *DaVinci Resolve 21.1 Reference Manual*, Blackmagic Design, en `/Applications/DaVinci Resolve/DaVinci Resolve Manual.pdf`. Capítulos citados: 6 (Project Settings), 8 (Proxies), 23 (Split Clips), 41 (Timelines), 52 (Audio en Edit), 57 (Fader Handles), 127 (Video Scopes), 131 (Primaries), 142 (Grade Management), 143 (Nodos), 177 (Loudness), 187 (Rendering Media).
- Lista oficial de códecs soportados (Blackmagic Design, *Supported Formats and Codecs*).
- Formato de los clips medido con `ffprobe` sobre `C0400.MP4` (24-09-2026).
- Requisitos: correo de Los Antonios del 15-09-2026.
