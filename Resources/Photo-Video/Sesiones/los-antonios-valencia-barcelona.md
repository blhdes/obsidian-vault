---
title: Los Antonios — Valencia (mediodía) + Barcelona (noche)
date: 2026-09-19
tags: [photo-video, sesion, sony, a7iv, video, flash, exteriores]
cliente: Los Antonios
lugar: Valencia y Barcelona
---

Primera sesión con **foto y vídeo a la vez**. Dos plazas el mismo día, mayoritariamente exteriores (según sus redes).

Método de captación en [[Resources/Photo-Video/metodo-foto-video-simultaneo]]. Perfiles base en [[Resources/Photo-Video/perfiles-dial-sony-a7iv]].

## Lo que piden

- Cobertura audiovisual del momento principal.
- Fotografías seleccionadas del evento.
- **1 vídeo vertical de ~30 s** (Reels, Stories, TikTok).
- **1 vídeo horizontal de ~60 s** (archivo de marca, web, YouTube, presentaciones).
- Entrega en alta calidad.
- Cesión de derechos de uso para comunicación, publicidad, redes, web y acciones comerciales.

## Horario

| Sesión | Hora | Luz |
|---|---|---|
| Valencia | 12:00-13:00 o más tarde | sol alto, exterior |
| Barcelona | noche | exterior, luz artificial |

## Vídeo a mediodía sin filtro ND (decidido: plan B)

**No hay ND variable para esta sesión.** Se descarta y se tira de plan B. A 25p la velocidad correcta es 1/50 (regla de 180°), y a pleno sol con ISO 100 eso obliga a f/22, que ya es difracción visible.

La solución es ceder **un paso** de velocidad en vez de cerrar hasta f/22:

| Situación | Vel. | f | ISO | Regla 180° |
|---|---|---|---|---|
| **Sol directo** | **1/100** | f/16 | 100 | 1 paso fuera, apenas se nota |
| **Sombra abierta** | **1/50** | f/8 | 100 | correcta |
| **Interior o tarde** | **1/50** | f/4-5.6 | 100-400 | correcta |

**Por qué 1/100 + f/16 y no 1/200 + f/11** (misma exposición): te alejas un paso de la regla de 180° en vez de dos, y la difracción de f/16 se disimula casi entera porque el 4K sale de un remuestreo desde 7K, o sea que la salida son 8,3 MP y no 33. Se nota antes un movimiento con cadencia rara que un pelín de blandura.

> [!important] Grabar en sombra siempre que se pueda
> No es solo exposición: la sombra abierta a mediodía te da **la velocidad correcta y un diafragma usable a la vez**. Y el sol alto es mala luz para vídeo de marca, con sombras duras bajo ojos y nariz y la gente entrecerrando los ojos.

### Tres cosas que comprobar en el menú

1. **¿Hay ISO 50 en modo vídeo?** Si lo hay, a pleno sol se puede rodar a **1/50 + f/16**, o sea la regla de 180° correcta. Es exactamente el paso de luz que falta.
2. **Nada de S-Log3.** Su ISO base es **800**, tres pasos por encima de 100. Sin ND obligaría a f/45. Perfil estándar y listo.
3. **Cualquier filtro de 55 mm sirve de algo.** Un polarizador (CPL) corta 1,5-2 pasos y además limpia reflejos y satura el cielo. Medio ND gratis.

### Separación de fondo sin poder abrir

A f/16 sale todo enfocado, así que la única palanca es **la distancia**:

- **Detalle: 70 mm a 1-1,5 m.** A 70 mm, f/16 y 1,5 m hay unos 44 cm de profundidad de campo, suficiente para despegar al sujeto del fondo.
- **Plano general: da igual**, ahí el foco profundo es lo que se busca.

### Para otra ocasión

ND variable de **55 mm** (diámetro del FE 28-70), rango **ND8-ND128** (3-7 pasos), 25-50 €. Evitar los ND2-ND400 baratos: hacen una X en la imagen en los extremos del rango.

## Los diales

| Dial | Para qué | Modo | Vel. | f | ISO | Notas |
|---|---|---|---|---|---|---|
| **Foto 3** | Valencia, sol | M | 1/250 | f/8 | 100 | ya registrado, no tocar |
| **Foto 2** | ambiente y sombra | M | 1/100 | abierto | Auto, máx 25600 | re-registrar |
| **Foto 1** | BCN noche + flash | M | 1/100 | f/5.6 | **1600 fijo** | re-registrar. Flash `M` ~1/32 directo |
| **Vídeo 1** | sombra e interior | M | **1/50** | f/4-5.6 | 100-400 | ya registrado |
| **Vídeo 2** | día sin ND | M | **1/100** sol · **1/50** sombra | f/16 sol · f/8 sombra | 100 | hueco libre |
| **Vídeo 3** | BCN noche | M | **1/50** | abierto | Auto, máx 12800 | hueco libre |

**Por sesión son dos posiciones de dial:**

- **Valencia** → Foto 3 + Vídeo 2
- **Barcelona** → Foto 1 + Vídeo 3

**ISO fijo en Foto 1** por lo aprendido en [[Resources/Photo-Video/Sesiones/sopar-del-soci-ctnsc]]: con flash manual, si el ISO flota cada foto expone el flash distinto.

**Flash en exterior de noche:** no hay techo ni paredes donde rebotar, así que **directo**, igual que en la sala de techo alto. Techo de 1/250 sin HSS.

## Hoja de registro de perfiles

Los perfiles se construyen en `M` y luego se guardan en el hueco. Lo que se toque estando ya en el `1` o el `2` **no se guarda solo**.

```
MENU → (Shooting) → [Shooting Mode] → [Camera Set. Memory] → hueco
```

Tope de ISO Auto: `MENU → (Exposure/Color) → [Exposure] → [ISO] → ISO AUTO`, y pulsando a la derecha aparecen `ISO AUTO Maximum` y `Minimum`.

### Antes de empezar: ajustes globales

No se guardan dentro de ningún perfil, hay que dejarlos puestos una vez:

| Ajuste | Valor |
|---|---|
| `NTSC/PAL Selector` | **PAL** |
| `File Format` | **XAVC S 4K** |
| `Rec Frame Rate` | **25p** |
| `Record Setting` | **140M 4:2:2 10bit** |
| `Auto Switch Media` | **Off** |
| `Anti-flicker Shoot.` | **On** (obturador mecánico) |
| Perfil de imagen | **estándar, nada de S-Log3** |

### Selector en Foto, dial en `M`

**Foto 1 — Barcelona noche + flash**

| | |
|---|---|
| Velocidad | **1/100** |
| Diafragma | **f/5.6** |
| ISO | **1600 fijo** |
| Balance de blancos | Auto |
| Enfoque | AF-C, cara y ojos |
| Disparo | Single |

→ `Camera Set. Memory` → **1**

**Foto 2 — ambiente y sombra**

| | |
|---|---|
| Velocidad | **1/100** |
| Diafragma | **todo abierto** (f/3.5 a 28 mm) |
| ISO | **Auto**, mínimo 100, **máximo 25600** |
| Balance de blancos | Auto |
| Enfoque | AF-C, cara y ojos |
| Disparo | Continuo Lo |

→ `Camera Set. Memory` → **2**

### Selector en Vídeo, dial en `M`

> [!important] En vídeo el balance de blancos va fijo, nunca en Auto
> En foto se dispara en RAW y el balance se corrige gratis después. En vídeo el color va **cocido en el archivo**, y un balance automático que se mueve a mitad de plano es muy visible y muy difícil de arreglar. Se fija antes de rodar y se deja.

**Vídeo 2 — día sin ND**

| | |
|---|---|
| Velocidad | **1/100** a pleno sol · **1/50** en sombra |
| Diafragma | **f/16** al sol · **f/8** en sombra |
| ISO | **100 fijo** (o 50 si el modo vídeo lo ofrece) |
| Balance de blancos | **Daylight fijo** |
| SteadyShot | Active si voy a mano |

→ `Camera Set. Memory` → **2**

**Vídeo 3 — Barcelona noche**

| | |
|---|---|
| Velocidad | **1/50** |
| Diafragma | **todo abierto** |
| ISO | **Auto**, máximo **12800** |
| Balance de blancos | **fijo ~3800 K**, ajustar tras un clip de prueba |
| SteadyShot | Active |

→ `Camera Set. Memory` → **3**

### Comprobación final

Girar el dial fuera y volver a cada hueco, y verificar que recupera lo esperado. Es el paso que más disgustos ahorra.

## Antes de salir

1. **Formatear la de 64 GB en la cámara**, solo con la copia del 18-09 ya confirmada.
2. **`Auto Switch Media` → `Off`.** Con la de 32 GB en el Slot 1 bloquea el 4K. Ver [[Resources/Photo-Video/sony-a7iv-ajustes]].
3. Verificar **PAL · XAVC S 4K · 25p · 140M 4:2:2 10bit**.
4. **Baterías de sobra.** Foto + vídeo en dos ciudades con una sola no llega; el vídeo consume mucho más.
5. Flash: pilas cargadas, **difusor traslúcido dentro**, **pitido de flash listo activado**.
6. **Anti-parpadeo activado** para la noche en Barcelona, que hay luz artificial.
7. Comprobar si **ISO 50** está disponible en modo vídeo. **Perfil estándar, nada de S-Log3.**

## Audio

Una pieza de 30/60 s para redes se monta casi siempre sobre música, así que el micro interno vale. Aun así, grabar ambiente y **no hablar cerca de la cámara mientras rueda**.

## Después de la sesión

Rellenar aquí qué se usó de verdad y qué falló, como en [[Resources/Photo-Video/Sesiones/sopar-del-soci-ctnsc]].
