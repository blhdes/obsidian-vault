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

|                    |                                                  |
| ------------------ | ------------------------------------------------ |
| Velocidad          | **1/50**                                         |
| Diafragma          | **todo abierto**                                 |
| ISO                | **Auto**, máximo **12800**                       |
| Balance de blancos | **fijo ~3800 K**, ajustar tras un clip de prueba |
| SteadyShot         | Active                                           |

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

## Después de la sesión (20-09-2026)

**Solo se hizo Valencia. La sesión de Barcelona no llegó a hacerse.** La boda es de **Fran y Elena**, en Valencia.

| Tarjeta | Contenido | Carpeta de destino | Estado |
|---|---|---|---|
| **32 GB** | 83 RAW + 83 JPG | `2026-09-19 - Los Antonios - Boda Fran y Elena Valencia` | **copiada y verificada 20-09**, 166 MD5 idénticos |
| **64 GB** | **solo vídeo**: 107 clips + 107 XML | `2026-09-19 - Los Antonios - Boda Fran y Elena Valencia (vídeo)` | **copiada y verificada 20-09**, 214 MD5 idénticos |

La tarjeta de 32 GB traía además `DCIM/10060918` con las 998 fotos del 18-09. Ya estaban respaldadas en las tres carpetas de aquel día (Cosentino 48 + Rodri 298 + CTNSC 652 = 998, rango `AGU01380`..`AGU01878` sin huecos), así que no se volvieron a copiar. **La tarjeta se puede formatear.**

Dato confirmado en cámara: **no hay ISO 50 en modo vídeo**, así que el plan B quedó en 1/100 + f/16 a pleno sol.

## Auditoría de EXIF (20-09-2026)

83 fotos, `AGU01879`..`AGU01961`, de **16:49 a 20:29**. Todas con el FE 28-70, todas en `M`, compensación de exposición a 0, balance de blancos en Auto, disparo Single. **El flash no disparó ni una sola vez.**

### Qué hueco de dial se usó y cuándo

El **techo de ISO Auto** y el **Creative Style** son la huella que identifica cada hueco, porque se guardan dentro del perfil y no se tocan sobre la marcha. Con eso la sesión se parte en cuatro bloques limpios:

| Bloque | Hora | Fotos | Huella EXIF | Qué es |
|---|---|---|---|---|
| **A** | 16:49-18:51 | 43 | ISO Auto, máx 25600, Standard | **Foto 2** |
| **B** | 18:57-18:59 | 9 | ISO Auto, máx 25600, Standard | **Foto 2**, velocidad subida a mano |
| **C** | 19:33-19:42 | 23 | **ISO fijo, máx 6400, Neutral** | **Foto 1 sin re-registrar** |
| **D** | 20:14-20:29 | 8 | ISO Auto, máx 25600, Standard | **Foto 2** |

> [!warning] Los dos hallazgos
> **1. Foto 3 no se usó nunca.** Cero fotos a 1/250 y cero a f/8 en las 83. El perfil del sol de Valencia no llegó a entrar, porque la sesión arrancó a las 16:49 y no a mediodía.
>
> **2. El hueco Foto 1 nunca se re-registró.** La nota lo marcaba como "re-registrar" y se quedó sin hacer. Al girar el dial al `1` a las 19:33 salió la configuración de la cena del CTNSC del 18-09: ISO fijo, techo de ISO Auto en 6400 y Creative Style **Neutral**. Se confirma comparando con `AGU01871`..`AGU01878` de aquella noche, que tienen esa huella exacta.

Efecto colateral del segundo: **22 fotos de la boda salen en Neutral** y las otras 61 en Standard, así que hay que igualar el perfil al revelar. (`AGU01937`, a las 19:35, es la única del bloque C en Standard: un vistazo suelto al hueco 2 y vuelta.)

### Consistencia de exposición

Medido sobre el **brillo medio real del JPG de cámara**, no sobre el tag `BrightnessValue` (que con ISO fijo da lecturas que no cuadran). 0 = negro, 1 = blanco:

| Bloque            | Brillo medio | Dispersión | Fotos fuera de rango |
| ----------------- | ------------ | ---------- | -------------------- |
| A 16:49-18:51     | 0,418        | 0,052      | **0** de 43          |
| B 18:57-18:59     | 0,290        | 0,016      | **0** de 9           |
| **C 19:33-19:42** | 0,266        | **0,160**  | **7** de 23          |
| D 20:14-20:29     | 0,217        | 0,065      | 1 de 8               |

*(fuera de rango = brillo < 0,15 o > 0,65)*

**El bloque C es el problema, y no por estar oscuro sino por ser inconsistente.** Su dispersión triplica la del resto. Con el ISO clavado a mano (1600 → 800 → 640) mientras la luz caía, cada corrección llegaba tarde: van desde `AGU01952` casi negra (0,013) hasta una quemada a 0,809. **Seis de las diez fotos más oscuras de toda la boda están en esos nueve minutos.**

Los bloques A y B no tienen **ni una sola** foto fuera de rango. El ISO Auto con techo aguantó bien incluso de noche: en D tocó el límite de 25600 en cuatro fotos y aún así mantuvo la dispersión baja.

### El obturador dentro de Foto 2

Dentro del hueco 2 la velocidad sí se movió a mano, que es lo normal (el perfil da el punto de partida):

| Hora | Vel. | Fotos |
|---|---|---|
| 16:49-16:50 | 1/400 | 3 |
| 16:59-17:19 | 1/500 | 8 |
| **17:21-18:51** | **1/100** | **31 seguidas** |
| 18:57-18:59 | 1/160 | 9 |
| 20:14-20:29 | 1/100 | 8 |

A las **18:57**, con el sol ya bajo y el ISO Auto en 5000, la velocidad subió de 1/100 a 1/160. Son 2/3 de paso de luz que el ISO tuvo que compensar justo cuando menos margen quedaba, y se ve en los datos: pasa a 6400-8000 en las nueve fotos siguientes. Salieron bien expuestas, pero con más ruido del necesario.

El tramo de **31 fotos seguidas a 1/100 entre las 17:21 y las 18:51**, sin tocar nada, es el más limpio de la sesión entera.

### Auditoría del vídeo (107 clips, 16,5 min)

`C0360`..`C0466`, de **16:43 a 20:38**, media de 9 s por clip. Formato correcto y constante en los 107: **3840x2160, 25p, AVC140 4:2:2 10 bit, rec709**. Nada de S-Log3, como estaba planeado.

**El plan B de vídeo duró un clip.** `C0360` es el único a **1/100 + f/16**. A partir de `C0361` y durante los 106 restantes la velocidad es **1/50**, o sea la regla de 180° correcta todo el rato. Con la sesión empezando a las 16:43 y no a mediodía, sobraba luz de menos y el plan B no hizo falta.

**El diafragma hizo de ND**, que es exactamente lo que toca sin filtro:

| Hora | f | ISO | WB |
|---|---|---|---|
| 16:43-16:52 | f/16 → f/9 | 100-200 | Daylight |
| 17:20-18:13 | f/13 → f/5.6 | 100-200 | Daylight |
| 18:20-18:34 | f/5 → f/3.5 | 200 | **Custom** |
| 18:41-18:57 | f/4-5 | 400 → 1000 | Custom |
| 19:08-19:32 | f/3.5-4.5 | 3200 → **8000** | Custom |
| 20:30-20:38 | f/4-4.5 | 6400 | **Daylight** |

Balance de blancos **siempre fijo, nunca en Auto**: la regla de la nota se cumplió sin fallo. Cambió a Custom sobre las 18:20 y volvió a Daylight en el último bloque de las 20:30.

> [!warning] Dominante naranja fuerte a partir de las 19:14
> Medida sobre las miniaturas de cámara, la relación R/B pasa de **1,0-1,3** (neutra, de día) a **9-10** desde `C0407`. El brillo medio baja a 0,15-0,21.
>
> Parte es la escena (puesta de sol más luz cálida del sitio) y parte es que el balance fijo no se volvió a tocar cuando la luz viró. No se puede separar una cosa de la otra solo con los datos, y varía mucho según lo que entra en cuadro (`C0444` da 2,9 y `C0466` da 9,1). Lo accionable: **en vídeo eso va cocido**, así que hay que corregirlo en el etalonaje y contar con ello al elegir planos para las piezas de 30 y 60 s.

Detalle a favor: el ISO subió de forma escalonada y ordenada (100 → 200 → 400 → 500 → 1000 → 3200 → 6400 → 8000) sin los saltos erráticos que sí tuvo la foto entre las 19:33 y las 19:42.

Hay un hueco de **58 minutos sin grabar** entre `C0443` (19:32) y `C0444` (20:30), el mismo parón que se ve en la foto entre las 19:42 y las 20:14.

### Para la próxima

1. **Re-registrar los huecos marcados como "re-registrar" antes de salir de casa**, no sobre la marcha. Es el fallo que salió más caro de los tres.
2. **Comprobar el Creative Style dentro de cada hueco**, no solo velocidad, diafragma e ISO. Es el ajuste que se cuela sin avisar y luego obliga a igualar en revelado.
3. **Al anochecer la velocidad baja, no sube.** Si hace falta congelar movimiento, abrir el diafragma antes que subir el obturador.
4. **Con luz cambiante, ISO Auto con techo ganó al ISO manual** por goleada (dispersión 0,05 frente a 0,16). El ISO fijo tiene sentido con flash, donde la exposición la manda el destello; sin flash y con la luz cayéndose es una trampa.
5. La comprobación final que ya recoge la nota (girar el dial fuera y volver a cada hueco) habría cazado lo de Foto 1 en diez segundos. **Hacerla.**
6. **En vídeo, re-fijar el balance de blancos cuando la luz vire**, no solo al empezar. Fijarlo una vez y olvidarlo funcionó hasta la puesta de sol y dejó de funcionar después.
7. El **ND variable de 55 mm** sigue en la lista, pero esta sesión demuestra que a partir de las 17:00 no hace falta: el diafragma solo ya cubrió el rango a 1/50.

### Cómo se hace la copia

Convención de carpeta: `<YYYY-MM-DD> - <Cliente> - <Descripción>` dentro de
`~/Library/CloudStorage/OneDrive-FF8/photo and video/`.

Copiar con **`cp`, nunca `rsync`** (macOS le deniega escribir en CloudStorage), verificar MD5 origen contra destino y dejar el manifiesto en `checksums-md5.txt` dentro de la carpeta.

> [!warning] Si aparece "Operation not permitted" sobre la tarjeta o sobre OneDrive
> Suele significar que **Claude Code se ha actualizado mientras la sesión estaba abierta**. macOS valida el permiso contra el binario firmado, y si ese binario ya no está en disco la comprobación falla. **Solución: reiniciar Claude Code.** No hace falta tocar Full Disk Access.
