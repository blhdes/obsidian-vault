---
title: Darktable — de cero a dos estilos (.dtstyle) para revelar por lotes
date: 2026-09-20
tags: [photo-video, darktable, raw, tutorial, estilos, automatizacion]
---

Manual paso a paso para construir un **estilo de revelado** en darktable y exportarlo, partiendo de no haber hecho nunca uno. Escrito para el trabajo del CTNSC, donde hacen falta **dos**: uno para las fotos de ambiente y otro para las de flash.

Lo básico de darktable (catálogo, importar, exportar) está en [[Resources/Photo-Video/darktable-manual-basico]]. El flujo automatizado que lleva hasta aquí, en [[Resources/Photo-Video/automatizar-postproduccion-scripting]]. La versión resumida para repetir el proceso: [[Resources/Photo-Video/postpro-paso-a-paso]]. Versión: darktable 5.6.1.

> [!note] Corregido tras el primer uso real (21-09-2026, Cosentino)
> - La interfaz está **en inglés**: los nombres de módulo que salen en pantalla son los ingleses.
> - Tres errores de este manual, ya corregidos abajo: *history stack* y *styles* están en el **panel derecho** de la *lighttable*; faltaba el paso **compress history** antes de crear el estilo; e importar desde OneDrive escribía archivos en el archivo de solo lectura.
> - Lo que se aprendió está al final: [[#Aprendido en la primera entrega real (21-09-2026)]].

## Qué vamos a hacer, en una frase

Ajustar **una** foto hasta que te guste, guardar esos ajustes como un archivo, y que un comando se lo aplique a las otras 290.

## Vocabulario mínimo

Cuatro palabras que van a salir todo el rato:

- **Módulo** — cada herramienta de ajuste de darktable (exposición, contraste, ruido...). Son cajas que se encienden y se apagan, y cada una hace una sola cosa.
- **Estilo** (*style*) — una lista guardada de módulos con sus valores. Es lo que vamos a crear. Se guarda en un archivo `.dtstyle`.
- **Darkroom / Lighttable** — las dos pantallas de darktable. *Lighttable* es la mesa de luz, donde ves todas las fotos en cuadrícula. *Darkroom* es el cuarto oscuro, donde editas una. Se cambia con la tecla `L` y `D`, o arriba a la derecha.
- **Scene-referred** — el modo de trabajo moderno de darktable. Significa que los ajustes se hacen sobre la luz "tal como era en la escena" en vez de sobre la imagen ya comprimida a pantalla. Da mejores resultados en luces altas, y es el que viene por defecto. No lo toques.

> [!note] Darktable no toca tus RAW, nunca
> Todo lo que hagas se guarda como una lista de instrucciones, no como píxeles. Tu `.ARW` sale del proceso byte a byte idéntico. Si la lías, se deshace y ya está.

## Por qué dos estilos y no uno

Las 291 fotos se dispararon en dos condiciones de luz muy distintas, y eso pide tratamientos distintos:

| | Fotos | Cómo se disparó | Qué implica al revelar |
|---|---|---|---|
| **Ambiente** | 81 | ISO Auto de 500 a 4000, 1/100, sin flash | ruido variable, luz cálida de sala, exposición muy pareja |
| **Flash** | 210 | ISO fijo 1600, flash manual directo | ruido constante, pero **la exposición varía 1,3 pasos** según lo lejos que estuviera la gente |

Esa última celda es la clave de todo el manual, y la resolvemos en el paso 4.

---

## Paso 0 · Preparar las fotos de referencia

No importes las 291. Coge **6 u 8 de cada bloque** que sean representativas: una clara, una oscura, alguna con caras en primer plano y alguna de plano general.

Los RAW ya están separados por bloque en enlaces:

```
~/Pictures/Postpro/2026-09-18 - CTNSC - Sopar del Soci/04-para-revelar/
    01-ambiente-ISOauto-max12800-Neutral/      (1 foto)
    02-ambiente-ISOauto-max12800-Standard/     (80 fotos)
    03-flash-o-ISOfijo-Neutral/                (210 fotos)
```

Los bloques **01 y 02 son el mismo estilo**: se separaron porque la cámara tenía distinto *Creative Style*, pero eso solo afecta al JPG. En el RAW es un metadato que darktable ignora.

## Paso 1 · Importar en darktable

0. **Solo la primera vez:** engranaje de arriba a la derecha → *preferences* → **storage** → **create XMP files: `never`**. Por defecto darktable escribe un `.xmp` al lado de cada foto que importa. Con `never`, tus ediciones se guardan igual, en su catálogo.
1. Abre darktable. Arranca en *Lighttable*.
2. Panel izquierdo → **`import`** → **`add to library...`**.
3. Navega a `04-para-revelar/03-flash-o-ISOfijo-Neutral/` y selecciona 6-8 fotos. Si el bloque es pequeño (menos de ~30), impórtalas todas. En el diálogo, las carpetas del sistema salen con su nombre real: `Pictures`, no "Imágenes".

> [!warning] Importa siempre desde los enlaces, nunca desde OneDrive
> Los enlaces funcionan: comprobado con las 18 de Cosentino. Importar desde la carpeta de OneDrive haría que darktable escribiera sus `.xmp` en el archivo de solo lectura, si el paso 0 no está hecho.

4. Doble clic en una foto → entras en *Darkroom*.

## Paso 2 · Entender el panel derecho

En *Darkroom*, la columna de la derecha son los módulos. Arriba hay unos iconos que agrupan por tipo: **técnico**, **tono**, **color**, **corrección**, **efecto**. Para empezar usa el icono de **módulos activos** (parece un interruptor) para ver solo lo que está encendido.

Con el flujo por defecto (*scene-referred, sigmoid*), una foto recién importada trae encendidos estos módulos, comprobado en 5.6.1:

- **Se ajustan en este manual:** `exposure`, `color calibration` y `sigmoid`. Llevan la etiqueta *scene-referred default*, que desaparece cuando cambias algo.
- **No se tocan:** `orientation`, `demosaic`, `highlight reconstruction`, `white balance`, `raw black/white point`, `input color profile` y `output color profile`. Son los que convierten un RAW en imagen; no son decisiones creativas.

El gráfico de arriba a la derecha sale por defecto en modo **forma de onda** (*waveform*), no como histograma: de izquierda a derecha es la foto, y de abajo arriba el brillo. Si algo toca el borde de arriba, está quemado.

> [!important] El orden en pantalla no es el orden en el que trabajas
> Darktable aplica los módulos en un orden interno fijo, de abajo arriba. Tú puedes ajustarlos en el orden que quieras. El orden que propongo abajo es el que menos te hará volver atrás.

---

## Paso 3 · Exposición

Módulo: **`exposure` / `exposición`**.

Es el primero siempre, porque todo lo demás depende de que la foto esté en el brillo correcto. Tiene un deslizador de **exposición** en pasos (EV) y otro de **nivel de negro**.

- Sube o baja hasta que las caras se vean bien. Ignora el fondo por ahora.
- Un **paso (EV)** es el doble o la mitad de luz. `+1.0` duplica el brillo.
- Darktable ya aplica `+0.7 EV` por defecto en Sony: eso es normal, no lo quites.

Fíjate en el gráfico de arriba a la derecha, que por defecto es una **forma de onda** (ver paso 2). Si algo toca el borde superior, hay luces quemadas y ahí ya no hay información que recuperar.

## Paso 4 · El truco del bloque de flash: exposición automática

**Esto solo para el estilo de flash.**

Con flash manual, la exposición de cada foto depende de a qué distancia estaba la gente. Tus 210 fotos van de 0,090 a 0,508 de brillo, o sea unos 2,5 pasos de diferencia. Un valor fijo de exposición en el estilo dejaría media entrega oscura y la otra media clara.

El módulo `exposición` tiene un selector de **modo** con dos opciones: **`manual`** y **`automático`**.

En **automático**, darktable mira el histograma de **cada foto** y calcula su propia corrección. Aparecen dos controles:

- **`percentile`** — qué parte del histograma usa como referencia. Empieza en **50%** (la mediana).
- **`target level`** — a qué brillo quieres llevar ese percentil, en EV. Empieza en **-4.0 EV** y ajusta a ojo.

Es decir: **el estilo lleva la regla, no el número**, y cada foto se normaliza sola. Es exactamente la automatización que tiene sentido aquí, porque igualar exposición es medir, no tener gusto.

Debajo aparece **computed EC**: la corrección que ha calculado para *esta* foto. En cada foto sale un número distinto, y es la señal de que la regla funciona.

> [!warning] Mide el encuadre entero, no la cara
> Si en el encuadre entra mucha superficie clara (pared blanca, mantel, muestras de piedra), darktable cree que la foto ya es clara, la baja un poco, y **la cara sale más oscura**. En Cosentino pasó en 4 de 17 fotos.
>
> **No se arregla cambiando el estilo**: subir el *target level* aclara todas y la diferencia se mantiene. Se arregla foto a foto, subiendo su *target level* +0,2 o +0,3 EV. Cómo encajarlo en el lote: [[Resources/Photo-Video/postpro-paso-a-paso#9 · Retoques de fotos concretas]].

> [!note] Para el bloque de ambiente, modo manual
> Ahí el ISO Auto ya hizo el trabajo: las 81 fotos caben en **0,67 pasos**, prácticamente nada. Un valor fijo va perfecto y te evita que el automático se despiste con una foto de composición rara.

## Paso 5 · Color

Módulo: **`color calibration` / `calibración de color`**.

Deja el módulo `balance de blancos` como está (`as shot`, lo que midió la cámara) y haz el trabajo de color aquí, que es donde darktable quiere que se haga.

- Pestaña **`CAT`** → hay un cuentagotas. Actívalo y **arrastra un rectángulo** sobre algo que en la realidad fuera **gris o blanco neutro**: un mantel, una camisa blanca, una pared. Eso corrige la dominante de la sala. Después, desactiva el cuentagotas.
- Evita superficies que parecen blancas pero tienen su propio color: piedra, mármol, madera clara.
- Al usar el cuentagotas, *illuminant* pasa a **`custom`** y el color se ajusta con **hue** y **chroma**. La lectura **CCT** (por ejemplo, 4380 K) es solo informativa.
- Si no hay nada neutro, deja *illuminant* en `as shot in camera` y ajusta la temperatura a mano: a la izquierda enfría (más azul), a la derecha calienta (más naranja).
- Juzga **la piel**, no la pared.

En la cena del CTNSC la luz de sala era cálida. Con flash, además, se mezclan dos luces de temperatura distinta (el destello es frío, la sala cálida), así que no esperes que quede perfecto: busca que las **caras** tengan buen color y deja que el fondo tire cálido, que además queda bien.

## Paso 6 · Tono y contraste

Módulo: **`sigmoid`** (o `filmic rgb`).

Este es el que decide cómo se reparte la luz entre sombras y luces altas. Darktable trae uno de los dos activado según cómo esté configurado.

**Usa `sigmoid` si puedes**: hace lo mismo que `filmic rgb` pero con tres deslizadores en vez de quince, y para empezar es mucho menos frustrante.

- **`contrast`** — la pendiente. Más contraste = negros más negros y blancos más blancos.
- **`skew`** — hacia dónde tira el contraste. Negativo protege las luces (útil con flash, que quema fácil).
- **`display primaries` / base primaries** — cuánto se saturan los colores al aclarar. Tócalo poco.

Si te lías, ponlo en sus valores por defecto y sube solo `contrast` un poco.

## Paso 7 · Ruido

Módulo: **`denoise (profiled)` / `eliminar ruido (perfilado)`**.

**Antes, comprueba si hace falta:** pon el zoom al 100 % (panel *navigation*, arriba a la izquierda), ve a una sombra y enciende y apaga el módulo. Si no ves diferencia, déjalo **apagado**, porque solo restaría detalle. En Cosentino, a ISO 400, no hizo falta.

Si hace falta, actívalo. No hace falta ajustar casi nada, y la razón es buena: darktable trae **perfiles de ruido medidos para la a7 IV** y lee el ISO del EXIF, así que **se adapta solo a cada foto**. Una foto a ISO 500 recibirá menos reducción que una a ISO 4000, con el mismo estilo.

Eso resuelve el problema del bloque de ambiente, que va de ISO 500 a 4000.

Modo recomendado: **`wavelets`** para empezar, que es el más suave con el detalle.

## Paso 8 · Nitidez y remate

- **`sharpen` / `enfocar`**: opcional. Con el 28-70 y estas fotos, poco o nada. Es mejor quedarse corto.
- **`local contrast` / `contraste local`**: da sensación de nitidez y volumen sin tocar los bordes. Subirlo un poco suele sentar bien en interiores. Ojo con **`detail`**: por encima de 100 % añade textura; **por debajo de 100 % suaviza**, lo que en retrato funciona como un ligero alisado de piel.
- **`vignetting` / `viñeteado`**: solo si quieres el efecto. Es decisión de gusto, no de corrección.

---

## Paso 9 · Comprobar antes de guardar

Esto es lo que separa un estilo que funciona de uno que te arruina 210 fotos.

1. Vuelve a *Lighttable* (`L`).
2. Selecciona la foto que has editado y **copia su historial**: **panel derecho** → módulo **`history stack`** → **`copy`**.
3. Selecciona las otras 5-7 de referencia → **`paste`**.
4. Míralas en grande una a una: doble clic en la primera, y dentro de la *darkroom* `espacio` pasa a la siguiente y `retroceso` vuelve a la anterior.

Lo que buscas: que **ninguna** se rompa. Que la más oscura no quede sucia y la más clara no queme las caras. Si alguna falla, vuelve a la original, corrige y repite.

> [!warning] El error clásico de la primera vez
> Ajustar el estilo sobre la foto que mejor salió. Esa siempre va a quedar bien. **Ajústalo sobre una del montón**, y compruébalo en las extremas.

## Paso 10 · Crear el estilo

Con la foto de referencia seleccionada en *Lighttable*. Los dos módulos que se usan están en el **panel derecho** de la *lighttable*, no en la *darkroom*:

0. **Primero, `history stack` → `compress history`.** No muestra ningún aviso, pero funciona.

> [!danger] Sin este paso, el estilo sale con valores que no son los tuyos
> El historial guarda cada módulo **dos veces**: la versión de serie que darktable aplica al abrir la foto (con la etiqueta *scene-referred default*) y tu versión editada. En la ventana de *create* salen las dos, y es muy fácil marcar la de serie. En Cosentino pasó con `sigmoid` y `color calibration`, y el estilo salió con contraste 1,5 en vez de 1,884.
>
> *Compress history* deja una sola entrada por módulo, y la foto se ve exactamente igual. Después de crear el estilo, Claude puede comparar el `.dtstyle` con tu historial valor por valor.

1. Panel derecho → módulo **`styles` / `estilos`** → botón **`create...`**.
2. Nombre: `ctnsc-flash` (o `ctnsc-ambiente`).
3. Descripción: pon la fecha y para qué es. En tres meses lo agradecerás.
4. Sale una **lista con todos los módulos** y una casilla por cada uno. **Aquí está la decisión importante.**

### Qué incluir y qué dejar fuera

| Módulo | ¿En el estilo? | Por qué |
|---|---|---|
| `exposición` | **SÍ en flash** (modo automático) · **SÍ en ambiente** (manual) | en flash lleva la regla, no el número |
| `calibración de color` | **SÍ** | la dominante de la sala es la misma en todas |
| `sigmoid` / `filmic` | **SÍ** | es el look |
| `denoise (profiled)` | **SÍ si está encendido** | se adapta solo al ISO de cada foto. Si lo apagaste, sigue saliendo en la lista: déjalo sin marcar |
| `local contrast`, `sharpen` | **SÍ**, si los has usado | parte del look |
| `orientation` | **SÍ si hay fotos verticales** | con `--style-overwrite` se pierde la rotación automática (ver paso 13). Su valor es *auto*: lee el EXIF de cada foto, así que vale para todas |
| `balance de blancos` | **NO** | es el de cámara, cada foto ya trae el suyo |
| `recorte`, `rotación` | **NO** | es de cada foto, no del conjunto |
| `máscaras`, ajustes locales | **NO** | están atados a una composición concreta |

La regla mental: **entra lo que vale para las 210; se queda fuera lo que solo vale para esa foto.**

5. **`create`**. El estilo ya aparece en la lista.

## Paso 11 · Exportar el `.dtstyle`

En el mismo módulo `styles`, selecciona el estilo → botón **`export`** → guarda el archivo.

Guárdalos aquí, junto al resto del material de la sesión:

```
~/Pictures/Postpro/2026-09-18 - CTNSC - Sopar del Soci/estilos/
    ctnsc-ambiente.dtstyle
    ctnsc-flash.dtstyle
```

Ese archivo es portátil: se puede importar en otro ordenador o reutilizar en la próxima cena de socios.

## Paso 12 · Repetir para el otro bloque

Vuelve al paso 1 con fotos de `02-ambiente-...`. Cambia dos cosas respecto al de flash:

- Exposición en **modo manual**.
- El color tira más cálido y no hay mezcla con el destello, así que el cuentagotas de `calibración de color` funcionará mejor.

## Paso 13 · Aplicarlo a las 291

Ya sin interfaz. Tres cosas antes de lanzar nada:

1. **Cierra darktable.** `darktable-cli` usa la misma base de datos, que es donde vive el estilo, y con la app abierta no puede entrar.
2. **Prueba con una sola foto** y compárala con tu edición en la app. Tienen que salir idénticas. El comando está en [[Resources/Photo-Video/postpro-paso-a-paso#7 · Probar el estilo con una foto]].
3. **Las opciones de `darktable-cli` van antes de `--core`.** Lo que va detrás se pasa a darktable y no hace lo que parece.

Un comando por bloque. Sin `--width` sale a tamaño completo, que es lo que se quiere: los tamaños de entrega se hacen después con `entregar.py`.

```bash
W="$HOME/Pictures/Postpro/2026-09-18 - CTNSC - Sopar del Soci"
mkdir -p "$W/05-reveladas"

darktable-cli "$W/04-para-revelar/02-ambiente-ISOauto-max12800-Standard" \
              "$W/05-reveladas" \
              --style "ctnsc-ambiente" --style-overwrite \
              --width 3000 --core --disable-opencl

darktable-cli "$W/04-para-revelar/03-flash-o-ISOfijo-Neutral" \
              "$W/05-reveladas" \
              --style "ctnsc-flash" --style-overwrite \
              --width 3000 --core --disable-opencl
```

Qué hace cada opción:

- **`--style`** — el nombre del estilo tal como se llama dentro de darktable (no la ruta del archivo).
- **`--style-overwrite`** — **importante**: reemplaza el historial en vez de añadirse encima. Sin esto, el estilo se apila sobre los ajustes por defecto y el resultado no es el que viste. **Efecto secundario:** el revelado queda con los módulos básicos más los del estilo, y `orientation` no está entre ellos. Una foto vertical saldría tumbada si el estilo no incluye `orientation` (ver la tabla del paso 10). No se ha comprobado todavía con una vertical real.
- **`--width 3000`** — lado largo máximo. Para entrega en alta, súbelo o quítalo.
- **`--core --disable-opencl`** — evita problemas con la aceleración por GPU. Si va bien sin ello, quítalo y será más rápido.

No olvides la foto suelta del bloque `01-...`, que va con el estilo de ambiente.

A 5-7 s por foto, las 291 son unos **25-35 minutos**. Se puede dejar corriendo.

---

## Errores típicos de la primera vez

1. **Olvidar `--style-overwrite`.** El resultado no coincide con lo que viste en pantalla y no entiendes por qué.
2. **Meter el recorte en el estilo.** Te recorta 210 fotos por donde no toca.
3. **Ajustar sobre la mejor foto.** Ver el aviso del paso 9.
4. **Pasarse con la nitidez.** Se nota mucho más en un lote que en una foto suelta.
5. **Exposición manual en el bloque de flash.** Es el error que te costaría rehacer las 210.
6. **Crear el estilo sin *compress history*.** Se cuela la versión de serie de algún módulo. Pasó en la primera entrega real.
7. **Lanzar el lote con darktable abierto.**
8. **Añadir un efecto (viñeteado, virado) solo a unas pocas.** Esas fotos se verán distintas del resto en la galería. Si el efecto gusta, va en el estilo, para todas.

## Aprendido en la primera entrega real (21-09-2026)

Cosentino, retrato de Carolina: 17 fotos, un solo bloque (flash rebotado, ISO 400 fijo). Nota de la sesión: [[Resources/Photo-Video/Sesiones/cosentino-retrato-carolina]].

| Qué | Resultado |
|---|---|
| Importar desde los enlaces de `04-para-revelar/` | funciona, sin avisos |
| Exposición automática | funciona; 4 de 17 necesitaron un retoque individual por mucha pared blanca en el encuadre |
| Estilo frente a tu edición en la app | **idénticos** (diferencia 0,00) una vez rehecho con *compress history* |
| Revelado por lotes, tamaño completo | **3 min 21 s** para 17 fotos, unos 12 s por foto |
| Retoques individuales | se editan en la app y se revelan con `darktable-cli --library` sobre una copia del catálogo. Así no hace falta exportar nada a mano |
| `darktable-cli` y los metadatos | exporta **sin EXIF de cámara**; `entregar.py` copia del RAW la fecha y los datos básicos |

## Lo que este manual no cubre

Retoque de una foto concreta: quitar un objeto, suavizar piel, aclarar una cara sola. Eso es trabajo a mano, foto a foto, y no va en un estilo. Se hace después, sobre las pocas que lo necesiten.
