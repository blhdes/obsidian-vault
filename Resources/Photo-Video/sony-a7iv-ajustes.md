---
title: Sony a7 IV — ajustes de captura (foto RAW y vídeo)
date: 2026-09-18
tags: [photo-video, sony, a7iv, raw, heif, video, xavc, camara, ajustes]
---

Menús en **inglés**, que es como tengo la cámara. Rutas verificadas contra la guía oficial de Sony para la ILCE-7M4.

# Foto

## El problema

Al vaciar una tarjeta el 18-09-2026 vi que las 1.379 fotos eran `.HIF`, el HEIF de Sony, no RAW. Desde HEIF el margen para recuperar luces y sombras es mucho menor, así que el revelado posterior (ver [[Resources/Photo-Video/automatizar-postproduccion-scripting]]) pierde buena parte de su sentido.

La causa: **son tres ajustes distintos**, y el tercero puede dejarte en HEIF sin que te enteres.

## 1. File Format

```
MENU → (Shooting) → [Image Quality] → [Image Quality Settings] → [File Format]
```

| Opción | Qué graba |
|---|---|
| **RAW** | solo RAW ← lo que quiero |
| RAW & JPEG | RAW + un JPEG de previo |
| RAW & HEIF | RAW + un HEIF de previo |
| JPEG | solo JPEG |
| HEIF | solo HEIF |

## 2. RAW File Type

```
MENU → (Shooting) → [Image Quality] → [Image Quality Settings] → [RAW File Type]
```

| Opción | Qué hace |
|---|---|
| Uncompressed | RAW sin comprimir, archivos muy grandes |
| **Lossless Comp (L)** | compresión sin pérdida, resolución completa ← por defecto |
| Lossless Comp (M) | sin pérdida, resolución reducida |
| Lossless Comp (S) | sin pérdida, resolución más reducida |
| Compressed | con pérdida, la mitad de tamaño que sin comprimir |

*Lossless Comp (L)* da calidad íntegra ocupando aproximadamente la mitad que *Uncompressed*. No hay motivo para usar *Uncompressed* salvo exigencia concreta de un cliente.

## 3. JPEG/HEIF Switch

```
MENU → (Shooting) → [Image Quality] → [JPEG/HEIF Switch]
```

Opciones: `JPEG` / `HEIF(4:2:0)` / `HEIF(4:2:2)`.

**Este era el culpable de los `.HIF`.** Decide si el archivo no-RAW sale como JPEG o como HEIF, y además cambia las opciones que muestran los otros menús.

- Con *File Format* en **RAW** puro, este ajuste da igual.
- Si quiero RAW más un previo rápido para revisar o entregar al momento: *File Format* en **RAW & JPEG** y este interruptor en **JPEG**.

## Aviso de compatibilidad

Los HEIF grabados por esta cámara no se abren en cámaras ni programas que no soporten el formato. Un motivo más para que el previo sea JPEG.

## Ajuste de foto en uso (18-09-2026)

| Ajuste | Valor | Por qué |
|---|---|---|
| File Format | RAW & JPEG | RAW para revelar, JPEG como previo rápido |
| RAW File Type | Lossless Comp (L) | calidad íntegra, la mitad de tamaño que sin comprimir |
| JPEG/HEIF Switch | JPEG | evita los `.HIF` |
| JPEG Quality | Light | el JPEG es solo previo, no entrega |
| JPEG Image Size | S (8.2M) | ocupa lo mínimo en tarjeta |

El previo pesa poco a propósito: no se entrega, sirve para revisar en cámara y para tener una vista rápida antes de revelar.

---

# Vídeo

Pensado para **clips cortos de 10 a 60 segundos**, máxima calidad posible sin cambiar de tarjeta. Zona PAL (España), así que 25p / 50p.

## Qué aguantan mis tarjetas

Comprobado leyendo los metadatos de lo ya grabado en la tarjeta de 64 GB: **4K 25p a ~100 Mbps de forma habitual, con un pico de 186 Mbps**, en H.264 (XAVC S). O sea, son al menos U3 / V30.

Según la tabla oficial de Sony, con U3 / V30 se puede grabar **todo hasta 200 Mbps**. Solo los modos All-Intra (XAVC S-I) exigen más:

| Formato | Bitrate | Tarjeta que exige Sony |
|---|---|---|
| XAVC S HD | 100 Mbps | SDHC/SDXC U3 / V30 |
| XAVC S 4K | 200 Mbps | SDHC/SDXC U3 / V30 |
| XAVC HS 4K | 200 Mbps | SDHC/SDXC U3 / V30 |
| XAVC S-I HD | 222 Mbps | SDXC **V90** |
| XAVC S-I 4K | 600 Mbps | SDXC **V90** |

En S&Q (cámara lenta) los 4K a 200 Mbps suben la exigencia a **V60**.

Por debajo de 60 Mbps vale cualquier SDHC/SDXC Clase 10.

### Aviso en cámara: SDHC vs SDXC

Al configurar XAVC HS 4K con la tarjeta de **32 GB** puesta, la cámara avisa:

> *"To perform shooting with this setting, use a memory card higher than SDXC U3/V30. Slot 2"*

Causa: **una tarjeta de 32 GB nunca es SDXC**, el estándar SDXC empieza por encima de 32 GB. Con la de 64 GB (SDXC) desaparece el aviso. Curioso, porque la tabla oficial de Sony dice "SDHC/SDXC (U3/V30 or higher)" para este formato, pero la cámara es más estricta que el manual.

→ **La de 32 GB no sirve para vídeo 4K en estos formatos.** Queda para fotos o para modos de 60 Mbps o menos.

## Configuración elegida

```
MENU → (Shooting) → [Image Quality] → [Movie Settings]
```

| Ajuste | Valor |
|---|---|
| File Format | **XAVC S 4K** |
| Rec Frame Rate | **25p** |
| Record Setting | **140M 4:2:2 10bit** |

Y en `MENU → (Setup) → [Area/Date] → [NTSC/PAL Selector]`: **PAL**, que es lo que habilita 25p y 50p.

### El error que casi cometo: XAVC HS 4K no tiene 25p

Primero configuré XAVC HS 4K pensando en grabar a 25p. **No existe esa combinación.** En la a7 IV, XAVC HS 4K solo ofrece:

- **60p/50p**
- **24p** (y solo con el selector en NTSC)

Estando en PAL, el 24p está bloqueado, así que XAVC HS 4K se queda **fijo en 50p** y la cámara responde *"Cannot change when set to PAL"* al intentar cambiarlo. No es un fallo de la tarjeta ni de la cámara, es que ese formato no tiene ese fotograma.

Para 25p hay que usar **XAVC S 4K**, que sí tiene fila de 30p/25p.

### Por qué esta configuración

- **25p a sensor completo.** En 4K 50p la cámara fuerza el modo APS-C/Super35, o sea recorte 1.5x: la guía oficial dice literalmente que ese modo *"is locked to On when shooting movies in 4K 60p/50p"*. En 25p usa el ancho completo y submuestrea desde 7K, que es el 4K más nítido que sabe hacer.
- **140M 4:2:2 10 bits** es el techo de calidad de XAVC S 4K a 25p. Los 10 bits 4:2:2 son los que dan margen real para corregir color; en 8 bits 4:2:0 el cielo se escalona en cuanto tocas curvas.
- **Entra de sobra en U3/V30.** Sony permite hasta 200 Mbps en ese tipo de tarjeta.
- **Peaje:** es H.264, no H.265, así que pesa más que si XAVC HS tuviera 25p. Es el precio de no recortar el sensor.

### Cuánto ocupa

140 Mbps = 17,5 MB por segundo.

| Clip | Peso |
|---|---|
| 10 s | 175 MB |
| 60 s | ~1,05 GB |
| Tarjeta 64 GB llena | ~61 min |

### Si quiero HEVC o cámara lenta

`File Format` → **XAVC HS 4K**, `Rec Frame Rate` → **50p**, `Record Setting` → **200M 4:2:2 10bit**.

Gano la eficiencia de H.265 y el 50p para ralentizar, pero asumo el recorte Super35 1.5x. Entra en V30 para grabación normal; desde el modo **S&Q** Sony sube la exigencia a **V60**.

### Lo que no puedo usar con estas tarjetas

**XAVC S-I** (All-Intra), ni en 4K ni en HD. Necesita V90. Es el formato que mejor se edita, porque cada fotograma es independiente, pero a 600 Mbps llenaría la tarjeta de 64 GB en 14 minutos. No compensa para clips de 10-60 s.

## Fuentes

- [File Format (still image)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659396.html)
- [RAW File Type](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659395.html)
- [JPEG/HEIF Switch](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000657944.html)
- [Movie Settings (movie)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000640834.html)
- [Memory cards that can be used](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000640149.html)
