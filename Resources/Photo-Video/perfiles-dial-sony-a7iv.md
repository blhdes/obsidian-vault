---
title: Sony a7 IV — los tres perfiles del dial (1, 2, 3)
date: 2026-09-18
tags: [photo-video, sony, a7iv, perfiles, flujo-trabajo, eventos]
---

Configuraciones guardadas en las posiciones **1, 2 y 3** del dial de modos, para cambiar de situación girando el dial en vez de recorrer menús con el cliente esperando.

Relacionado: [[Resources/Photo-Video/sony-a7iv-ajustes]], [[Resources/Photo-Video/flash-godox-sony-a7iv]].

## Lo primero: son 3 por cada modo, no 3 en total

La a7 IV guarda **3 perfiles por cada posición del selector Foto / Vídeo / S&Q**. La documentación de Sony lo dice así:

> *"You can register up to 3 often-used modes or product settings per shooting mode (Still/Movie/S&Q Motion) to the product and up to 4 (M1 through M4) to the memory card."*

Es decir: el `1` del dial en Foto y el `1` del dial en Vídeo son **dos perfiles distintos**. El vídeo no gasta huecos de foto.

> [!warning] Mi objetivo no llega a f/2.8
> Confirmado el 18-09-2026 leyendo el EXIF: uso un **FE 28-70mm F3.5-5.6 OSS**. Abre a **f/3.5 a 28mm** y se cierra solo a **f/5.6 a 70mm**.
>
> Donde estos perfiles decían `f/2.8` hay que leer *"todo lo abierto que dé"*. Zoomear de 28 a 70mm cuesta **1,3 puntos de luz**, así que en interior con poca luz conviene quedarse ancho y acercarse físicamente.

## Estado actual

| Hueco | Perfil cargado ahora | Registrado |
|---|---|---|
| Foto 1 | **Flash directo, evento techo alto** (variante de "Flash en interior") | ✔ 18-09-2026 |
| Foto 2 | **Reportaje nocturno interior** (variante de "Reportaje sin flash") | ✔ 18-09-2026 |
| Foto 3 | Exterior a pleno sol | ✔ 18-09-2026 |
| Vídeo 1 | 4K 25p | ✔ 18-09-2026 |
| Vídeo 2 | libre | — |
| Vídeo 3 | libre | — |

Quedan dos huecos de vídeo sin usar. Candidatos para cuando haga falta: 4K 50p para ralentizar, o un perfil de interior con ISO alto.

## Cómo se graba un perfil

> [!important] En el `1`, `2` o `3` no se configura, solo se recupera
> Si pongo el dial en `1` y no me deja tocar la velocidad, es porque el perfil guardado ahí está en un modo que no la deja ajustar (P o A), o está vacío. **El perfil se construye en `M` y luego se guarda en el hueco.**

1. Poner el selector **Foto / Vídeo / S&Q** en el modo que toque.
2. Girar el dial de modos a **`M`** (la M de verdad, no el 1).
3. Ajustar ahí todo: velocidad, diafragma, ISO, balance de blancos, enfoque.
4. `MENU → (Shooting) → [Shooting Mode] → [Camera Set. Memory] → 1, 2 o 3` y confirmar con el centro de la rueda.

Para recuperarlo: girar el dial a `1`, `2` o `3`. La velocidad será ajustable porque el perfil guardado está en modo `M`.

## Cómo modificar un perfil ya guardado

Lo que cambie estando en el `1` **no se guarda solo**. Para modificarlo:

1. Volver el dial a `M`.
2. Dejar la cámara como la quiero ahora.
3. Registrar otra vez encima del mismo hueco con `[Camera Set. Memory]`.
4. **Actualizar la tabla de Estado actual de esta nota** con la fecha y el cambio.

> [!note] Lo que no entra en el perfil
> Los ajustes de archivo y de tarjeta (`File Format`, `Rec. Media Settings`, `File/Folder Settings`) son globales, y la potencia del flash vive en el flash. Después de registrar cada perfil conviene girar el dial fuera y volver, para verificar que recupera lo esperado.

---

# Foto

## Foto 1 · Flash en interior

Retrato, grupo y plano de sala. Cubre los escenarios A, B y C de [[Resources/Photo-Video/flash-godox-sony-a7iv]].

| Ajuste | Valor |
|---|---|
| Modo | `M` |
| Velocidad | **1/160** |
| Diafragma | **f/4** |
| ISO | **400 fijo** |
| Balance de blancos | Flash |
| Enfoque | AF-S, zona amplia |
| Disparo | Single |

**Por qué ISO fijo:** mi flash es manual (versión Fujifilm, sin TTL). Si el ISO flotara según la luz ambiente, cada foto expondría el flash de forma distinta y perdería la consistencia que es justamente la ventaja del manual.

**Por qué 1/160 y no 1/250:** deja margen por debajo del límite de sincronización, para no rozar la banda negra si algo se descuadra.

**Ajuste sobre la marcha:** para grupos, cerrar a **f/5.6** para que salgan nítidas varias filas de gente, y subir la potencia del flash un paso para compensar.

## Foto 2 · Reportaje sin flash

Luz ambiente, gente moviéndose, situaciones que cambian rápido.

| Ajuste | Valor |
|---|---|
| Modo | `M` |
| Velocidad | **1/250** |
| Diafragma | **todo abierto**: f/3.5 a 28mm, f/5.6 a 70mm (ver aviso del objetivo) |
| ISO | **Auto**, máximo 6400, mínimo 100 |
| Balance de blancos | Auto |
| Enfoque | AF-C con reconocimiento de personas y ojos |
| Disparo | Continuo Lo |

**Cómo se controla el brillo:** con la **compensación de exposición**, que en `M` se activa precisamente porque el ISO está en Auto (rango −5 a +5 EV). Velocidad y diafragma quedan fijos, el ISO se mueve solo, y yo solo subo o bajo la compensación.

**Por qué 1/250 exacto:** congela el movimiento **y** coincide con el límite de sincronización, así que puedo montar el flash y disparar sin tocar nada más.

## Foto 3 · Exterior a pleno sol

El caso difícil, porque sin HSS estoy atado a 1/250.

| Ajuste | Valor |
|---|---|
| Modo | `M` |
| Velocidad | **1/250** (techo absoluto sin HSS) |
| Diafragma | **f/8** |
| ISO | **100 fijo** |
| Balance de blancos | Daylight |
| Enfoque | AF-C |

**Para qué sirve:** relleno de flash que elimina las sombras duras bajo ojos y nariz al mediodía.

**La limitación asumida:** a f/8 el fondo sale bastante definido, se pierde el desenfoque. Es el precio de no tener HSS. El día que tenga un `TT685S`, este perfil pasaría a 1/1000 y f/2.8.

---

# Vídeo

## Vídeo 1 · 4K 25p

Los clips cortos de 10 a 60 segundos.

| Ajuste | Valor |
|---|---|
| File Format | **XAVC S 4K** |
| Rec Frame Rate | **25p** |
| Record Setting | **140M 4:2:2 10bit** |
| Modo | `M` |
| Velocidad | **1/50** |
| Diafragma | f/4 |
| ISO | fijo, o Auto con tope 6400 |
| SteadyShot | Active si voy a mano |
| Breathing Comp. | ~~On~~ — **no disponible**, mi objetivo actual no es compatible (18-09-2026) |

### Nota sobre Breathing Comp.

Está en `MENU → (Shooting) → [Image Quality] → [Lens Compensation] → [Breathing Comp.]`, no como ajuste suelto. Solo aparece con el dial en vídeo **y con un objetivo de la lista de compensación automática de Sony** (G y GM recientes). Con mi objetivo actual no está disponible, así que de momento no aplica.

### El 1/50 no es un error: la regla de 180°

En vídeo la velocidad de obturación debe ser aproximadamente **el doble de los fotogramas por segundo**. A 25p eso son **1/50**.

Es lo que produce la cantidad de desenfoque de movimiento que el ojo asocia con "esto es cine". Si grabo a 1/250 cada fotograma sale congelado, y al reproducirse el movimiento va a saltos, con aspecto de videojuego o de vídeo doméstico.

**Consecuencia práctica:** en exterior de día, 1/50 deja entrar muchísima luz y la imagen se quema. La solución correcta **no** es subir la velocidad, sino poner un **filtro ND** delante del objetivo, que es un cristal oscuro que reduce la luz sin tocar nada más. Es el accesorio que más falta va a hacer para grabar de día.

---

## Resumen para llevar encima

| Dial | Modo | Vel. | f | ISO |
|---|---|---|---|---|
| **Foto 1** Flash | M | 1/160 | f/4 | 400 fijo |
| **Foto 2** Reportaje | M | 1/250 | abierto (f/3.5-5.6) | Auto, máx 6400 |
| **Foto 3** Sol | M | 1/250 | f/8 | 100 fijo |
| **Vídeo 1** 4K | M | 1/50 | f/4 | fijo o Auto |

## 2026-09-18 — Registrado: variante de evento nocturno

Foto 1 y Foto 2 llevan ahora la configuración preparada para la cena del club deportivo (*Sopar del Soci* CTNSC, **2026**), detallada en [[Resources/Photo-Video/evento-interior-techo-alto]].

| Hueco      | Antes (perfil base)                              | Ahora (evento nocturno)                                        |
| ---------- | ------------------------------------------------ | -------------------------------------------------------------- |
| **Foto 1** | 1/160 · f/4 · ISO 400 · WB Flash · AF-S · rebote | **1/80 · f/4-5.6 · ISO 1600 · WB Auto · AF-C · flash directo** |
| **Foto 2** | 1/250 · abierto · ISO Auto máx 6400 · AF-C       | **1/100 · abierto · ISO Auto máx 12800 · AF-C**                |

Los perfiles base siguen documentados más arriba en las secciones de Foto 1 y Foto 2, así que se pueden restaurar cuando haga falta. Los cambios de fondo que conviene mantener pase lo que pase:

- **Tope de ISO Auto a 12800** en Foto 2. Con un objetivo de f/3.5-5.6 en interior, 6400 se queda corto.
- Donde pone `f/2.8`, leer *"todo lo abierto que dé"*.

Foto 3 sin tocar.

## Fuentes

- [Camera Set. Memory](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000616724.html)
- [Recall Camera Setting](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000617341.html)
