---
title: Flash Godox TT685 + Sony a7 IV — manual de consulta rápida
date: 2026-09-18
tags: [photo-video, sony, a7iv, flash, godox, iluminacion, eventos]
---

Manual para consultar sobre la marcha en un trabajo. Relacionado: [[Resources/Photo-Video/sony-a7iv-ajustes]].

> [!warning] Comprobar el modelo del flash
> Godox usa la última letra para indicar la marca de cámara: `TT685C` Canon, `TT685N` Nikon, **`TT685S` Sony**, **`TT685F` Fujifilm**, `TT685O` Olympus/Panasonic.
>
> **Si mi flash es un `TT685F`, es la versión de Fujifilm.** Montado en la a7 IV dispararía en manual por el contacto central, pero **sin TTL ni HSS**, que es lo que asume todo lo de abajo. Para Sony hace falta `TT685S` o `TT685 II S`.

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
| Flash | `TTL`, cabezal 90° arriba con la tarjetita blanca fuera, o rebote en pared detrás de mí |

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
