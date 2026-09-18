---
title: Flash Godox TT685 + Sony a7 IV — manual de consulta rápida
date: 2026-09-18
tags: [photo-video, sony, a7iv, flash, godox, iluminacion, eventos]
---

Manual para consultar sobre la marcha en un trabajo. Relacionado: [[Resources/Photo-Video/sony-a7iv-ajustes]].

> [!warning] Mi flash es un TT685**F**, la versión de Fujifilm
> Confirmado el 18-09-2026. Godox usa la última letra para la marca de cámara: `TT685C` Canon, `TT685N` Nikon, `TT685S` Sony, **`TT685F` Fujifilm**, `TT685O` Olympus/Panasonic.
>
> En la a7 IV **funciona solo en manual**. Todo lo que diga `TTL` en esta nota no me aplica hasta que tenga un flash de Sony. Ver la sección final: [[#Qué puedo y qué no con el TT685F en la Sony]].

## 1. Montaje y encendido

El orden importa:

1. Apagar cámara y flash antes de montar.
2. Deslizar el flash en la zapata y girar la rueda de bloqueo hasta que quede firme.
3. Encender **primero la cámara**, luego el flash.
4. En el flash, pulsar `MODE` hasta ver `TTL` o `M`.

## 2. Los dos modos que uso

| Modo | Qué hace | Cuándo |
|---|---|---|
| **TTL** | el flash calcula la potencia solo | movimiento, prisa, situaciones cambiantes (evento, grupos) |
| **M** | yo fijo la potencia, de 1/1 (máxima) a 1/128 (mínima) | escena estable, resultados repetibles (retrato, plano fijo) |

En `M` la potencia se cambia con la rueda trasera del flash.

## 3. Ajustes en la a7 IV

| Ajuste | Valor |
|---|---|
| Modo de disparo | `M` (manual) o `A` (prioridad apertura) |
| Velocidad | **máximo 1/250** (ver abajo) |
| ISO | 100 a 400 de partida |
| Balance de blancos | Flash o Auto |
| Formato | RAW, para poder corregir después |

### El límite de 1/250: sincronización

**1/250 s es la velocidad de sincronización de la a7 IV** en formato completo (en modo APS-C/Super35 sube a 1/320). Es el dato oficial de Sony.

Por encima de esa velocidad, la cortinilla del obturador no llega a abrir el sensor entero a la vez, así que el flash ilumina solo una parte y **sale una banda negra** en la foto.

**Es el error más común con flash. Grabárselo.**

### Excepción: HSS (sincronización de alta velocidad)

Los TT685 de Sony soportan **HSS**, que permite pasar de 1/250 y llegar hasta 1/8000 sin banda negra. El flash emite una ráfaga continua de pulsos en vez de un destello único.

- **Para qué sirve:** abrir a f/1.8 o f/2.8 a pleno sol sin quemar la foto. Sin HSS, a 1/250 e ISO 100 el sol obliga a cerrar a f/11 y se pierde el desenfoque de fondo.
- **Peaje:** el HSS reduce bastante la potencia efectiva del flash, así que hay que acercarlo al sujeto.
- Se activa en el flash con el botón de sincronización hasta que aparece el símbolo `H` en pantalla.

## 4. El truco que más cambia el resultado: rebotar

El flash apuntando de frente aplana la cara y deja sombras duras detrás.

- **En interior:** inclinar el cabezal hacia arriba (45° a 90°) o hacia una pared lateral. La luz rebota, se ensancha y llega suave y natural.
- **En exterior sin techo:** no hay dónde rebotar, así que de frente pero bajando la potencia.

## 5. La regla mental

| Control | Qué afecta |
|---|---|
| **Apertura (f)** | cuánta luz de flash entra. Más abierto (f/2.8) = más flash, más cerrado (f/8) = menos |
| **ISO** | sube o baja todo el conjunto a la vez |
| **Velocidad** | **solo la luz ambiente** (el fondo). No afecta al flash |

Esa última línea es la clave de todo: **si el fondo sale oscuro, bajo la velocidad; si el sujeto sale oscuro, toco flash, f o ISO.**

## Configuraciones listas

### A) Retrato, una persona, interior

| | |
|---|---|
| Cámara | `M` · f/2.8-f/4 · 1/160 · ISO 200 |
| Flash | `TTL`, cabezal inclinado 60° hacia arriba (rebote en techo) |

Cara suave, fondo con algo de ambiente. Si el fondo sale muy oscuro, subir ISO a 400.

### B) Foto de grupo, interior o evento

| | |
|---|---|
| Cámara | `M` · f/5.6 · 1/160 · ISO 400 |
| Flash | `M`, cabezal 90° arriba con la tarjetita blanca fuera (**el difusor dentro**, ver abajo), o rebote en pared detrás de mí |

El f/5.6 da profundidad suficiente para que varias filas de gente salgan nítidas.

### C) Plano general de interior, ambiente de sala

| | |
|---|---|
| Cámara | `M` · f/4 · 1/60 · ISO 800 |
| Flash | `TTL` o `M` a 1/16, rebotado al techo |

El 1/60 deja entrar la luz de la sala y el flash solo rellena. A esa velocidad hay que sujetar firme o apoyar la cámara.

### D) Exterior de día con sol fuerte, relleno

| | |
|---|---|
| Cámara | `M` · f/4-f/5.6 · 1/250 · ISO 100 |
| Flash | `TTL`, cabezal de frente, compensación de flash a −1 si ilumina de más |

Elimina las sombras duras bajo ojos y nariz sin quemar la escena. Es el uso más útil del flash en exteriores de día.

→ Si quiero abrir a f/2 para desenfocar el fondo con ese mismo sol, aquí es donde entra el **HSS**.

## El EXIF miente: la cámara no sabe que llevo flash

Comprobado el 18-09-2026 con las 24 fotos del retrato de Carolina, todas disparadas con flash. Esto es lo que guardó la cámara:

| Campo | Valor |
|---|---|
| `Flash` | `Off, Did not fire` |
| `FlashAction` | `Did not fire` |
| **`FlashStatus`** | **`No Flash present`** |
| `LightSource` | `Flash` |
| `WhiteBalance` | `Flash` |

No es que crea que no disparó: **no detecta ni que hay un flash montado**. Sin comunicación por los contactos no tiene manera de saberlo. Los dos campos que sí dicen "Flash" vienen del balance de blancos que puse yo a mano, no de ninguna detección.

**Consecuencia para el flujo automatizado:** no puedo filtrar las fotos con flash por EXIF (ver [[Resources/Photo-Video/automatizar-postproduccion-scripting]]).

**Huella alternativa que sí funciona:** el perfil Foto 1 dispara siempre a `1/160 + ISO 400 + WhiteBalance Flash`. Esa combinación identifica las fotos con flash sin ambigüedad, y un script puede filtrar por ahí:

```bash
exiftool -if '$ExposureTime eq "1/160" and $ISO == 400 and $WhiteBalance eq "Flash"' -p '$FileName' *.ARW
```

## El zoom del flash

Con el TT685F en la Sony el zoom **solo funciona en manual** (`M Zoom` en pantalla). El flash no puede preguntarle a la cámara qué focal llevo puesta, así que el zoom automático no existe. Es otra consecuencia de que sea la versión de Fujifilm.

El zoom abre o cierra el haz de luz:

| Zoom | Efecto |
|---|---|
| 12-24mm | haz muy ancho, la luz se reparte y se desperdicia |
| **35-50mm** | **el punto dulce para rebotar al techo** |
| 105-200mm | mancha pequeña y dura en el techo, pierde suavidad |

**Rebotando, pasar de 12mm a 35mm gana alrededor de punto y medio de luz.** Concentra el haz en la zona del techo que interesa en vez de iluminar paredes y suelo. Con ese punto y medio se puede bajar la potencia de 1/4 a 1/8: misma exposición, recarga en la mitad de tiempo y el doble de batería.

Se cambia con el botón **`Zm/C.Fn`** y la rueda.

> [!warning] Si el zoom no responde y está clavado en 12mm
> La **tarjetita blanca** y el **difusor traslúcido** salen del mismo hueco, uno detrás del otro. Con el difusor fuera, el flash **fuerza el zoom a 12mm y bloquea la rueda**, porque con él puesto el haz es siempre ultra ancho.
>
> **Solución: empujar el difusor traslúcido hacia dentro y dejar fuera solo la tarjetita blanca opaca.** (Pasó el 18-09-2026 en los retratos de Barcelona.)

## Dos ajustes de C.Fn que compensan la limitación

- **Pitido de flash listo: activarlo.** Como el flash no habla con la cámara, **no hay indicador de flash cargado en el visor**. El pitido es el único aviso de que ya puede disparar. Sin él, algunas fotos salen a media luz.
- **Apagado automático: alargarlo.** Entre foto y foto el flash se duerme, y la primera después de despertarlo se pierde.

> [!note] La regla de distancias de la pantalla es decorativa
> La escala de metros que aparece abajo está calculada con un ISO y un diafragma que el flash supone. Como no puede leer los reales de la Sony, no significa nada. **El histograma manda.**

## Si algo va mal

| Síntoma | Causa | Solución |
|---|---|---|
| Banda negra en la foto | pasé de 1/250 sin HSS | bajar la velocidad o activar HSS |
| Todo quemado, blanco | exceso de potencia | bajar potencia en `M`, o compensación de flash en negativo en `TTL` |
| Fondo negro, sujeto brillante | falta luz ambiente | bajar la velocidad o subir ISO |
| El flash no dispara | zapata o emparejamiento | revisar que esté bien encajado y que cámara y flash compartan canal y grupo |

## Para el 80% de un evento

`TTL` + rebote al techo. Resuelve casi todo sin pensar.

## Fuentes

- [Especificaciones ILCE-7M4 (velocidad de sincronización)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000660153.html)
- [Godox TT685 C/N/S/F/O](https://www.godox.com/product-d/TT685.html)


---

## Qué puedo y qué no con el TT685F en la Sony

El flash es la versión de Fujifilm. La zapata de cualquier cámara lleva un **contacto central universal**, que es un simple "dispara ahora" sin más información. Eso funciona entre marcas. Todo lo demás (TTL, HSS, compensación) viaja por los contactos adicionales, que son propietarios de cada fabricante y no se entienden entre sí.

### Sí funciona

| | |
|---|---|
| Disparar | sí, por el contacto central |
| Potencia manual | 1/1 a 1/128, con la rueda trasera |
| Cabezal | rebote, inclinación, zoom, tarjetita blanca |
| Radio Godox 2.4 GHz | para controlar otros Godox en manual |
| Velocidades de 1/250 hacia abajo | sin problema |

### No funciona

| | Consecuencia |
|---|---|
| **TTL** | la potencia la calculo yo en cada situación |
| **HSS** | **techo absoluto de 1/250**, sin excepciones |
| Compensación de flash desde la cámara | se ajusta en el flash, no en el cuerpo |
| Sincronización a segunda cortinilla | no se puede controlar desde la cámara |
| Aviso de flash listo en el visor | hay que mirar el propio flash |

### Cómo quedan mis cuatro escenarios

| Escenario | Estado | Qué cambia |
|---|---|---|
| **A) Retrato interior** | funciona | flash en `M`, empezar en **1/16** rebotado y ajustar mirando la foto |
| **B) Grupo interior** | funciona | flash en `M`, empezar en **1/8** (f/5.6 pide más potencia que f/2.8) |
| **C) Plano general de sala** | funciona | ya estaba pensado en `M` a 1/16, sin cambios |
| **D) Exterior a pleno sol** | **tocado** | sin HSS me quedo en 1/250, así que a ISO 100 el sol obliga a f/8-f/11 y pierdo el fondo desenfocado |

### Trabajar en manual sin volverse loco

Como la luz de interior no cambia entre foto y foto, el manual es perfectamente llevadero. La rutina:

1. Poner el flash en `M` a **1/16**, rebotado al techo.
2. Disparar una de prueba y mirar el **histograma**, no la pantalla.
3. Ajustar y dejarlo fijo mientras no cambie la sala.

Dos reglas para corregir rápido:

- **Subir un paso de potencia** (de 1/16 a 1/8) = **+1 punto de luz**.
- **Acercarse a la mitad de distancia** = **+2 puntos de luz**. La distancia pesa el doble que la potencia.

### Si quiero recuperar TTL y HSS

- **Un `TT685S` o `V860III-S`**, la versión de Sony del mismo flash. Es la solución directa.
- Un disparador **Godox X2T-S / XPro II-S** para Sony con este flash de esclavo por radio: gano control de potencia a distancia, pero **sigo sin TTL ni HSS**, porque el protocolo del flash no cambia. Por comprobar antes de confiar en ello en un trabajo.

### Candidatos para sustituirlo (precios consultados el 18-09-2026)

Los tres acaban en **S**, que es justo lo que falló con el TT685**F**. Todos dan TTL y HSS en la a7 IV, y todos hablan el radio Godox X de 2,4 GHz, así que el TT685F actual podría quedarse de esclavo manual en un segundo punto de luz en vez de venderse.

| Modelo | Precio | Notas |
|---|---|---|
| **Godox TT685 II-S** | **139 €** | mismo cuerpo y misma ergonomía que el que ya tengo, pilas AA. El cambio más barato y sin curva de aprendizaje |
| **Godox V860 III-S** | **225 €** (Amazon.es 248 €) | batería de litio: recarga mucho más rápida y ~480 disparos a máxima potencia. La opción de trabajo |
| **Godox V1 Pro S** | ~290-320 € *(sin verificar)* | cabezal redondo, luz más suave de origen. El salto grande |

- [TT685II-S en bargainfotos](https://bargainfotos.com/tt685ii/14931-flash-godox-tt685ii-para-sony-6952344223697.html)
- [V860III-S en Fotocasión](https://www.fotocasion.es/catalogo/flash-godox-v860-iii-sony-con-carg-bateria-vp18/53340/)
- [V860III-S en Amazon.es](https://www.amazon.es/V860III-S-V860IIIS-2600mAh-Modelado-Compatible/dp/B09D9C9P5P)

### Prioridad

Para eventos de interior el manual es asumible. **El TT685S se vuelve necesario el día que tenga que trabajar a pleno sol con el diafragma abierto**, que es exactamente donde el HSS marca la diferencia.
