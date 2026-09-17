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

## Configuración elegida

```
MENU → (Shooting) → [Image Quality] → [Movie Settings]
```

| Ajuste | Valor |
|---|---|
| File Format | **XAVC HS 4K** |
| Rec Frame Rate | **25p** |
| Record Setting | **100M 4:2:2 10bit** |

Y en `MENU → (Setup) → [Area/Date] → [NTSC/PAL Selector]`: **PAL**, que es lo que habilita 25p y 50p.

### Por qué esta y no otra

- **XAVC HS en vez de XAVC S.** XAVC HS es H.265/HEVC, XAVC S es H.264. H.265 comprime mucho mejor, así que 100 Mbps en HS dan aproximadamente la calidad de 200 Mbps en S. Menos peso en tarjeta por la misma imagen. Se edita sin problema en Mac con Apple Silicon, que descodifica HEVC por hardware.
- **25p y no 50p.** En 4K 50p la a7 IV recorta el sensor a Super35 (factor 1.5x) y deja de submuestrear desde 7K. En 25p usa el ancho completo del sensor y genera el 4K más nítido que sabe hacer. El 50p se reserva para cuando quiera ralentizar.
- **4:2:2 10 bits.** Es lo que da margen real para corregir color después. En 8 bits 4:2:0 el cielo se escalona en cuanto tocas curvas.
- **3840×2160 es el techo.** La a7 IV no graba por encima de 4K, así que "máxima resolución" es esto en cualquier formato.

### Cuánto ocupa

100 Mbps = 12,5 MB por segundo.

| Clip | Peso |
|---|---|
| 10 s | 125 MB |
| 60 s | 750 MB |
| Tarjeta 64 GB llena | ~85 min |
| Tarjeta 32 GB llena | ~42 min |

### Si quiero cámara lenta

`Rec Frame Rate` → **50p**, `Record Setting` → **200M 4:2:2 10bit**. Entra en V30 para grabación normal, pero si lo hago desde el modo **S&Q** Sony pide **V60**. Con estas tarjetas, mejor grabar a 50p normal y ralentizar en edición.

### Lo que no puedo usar con estas tarjetas

**XAVC S-I** (All-Intra), ni en 4K ni en HD. Necesita V90. Es el formato que mejor se edita, porque cada fotograma es independiente, pero a 600 Mbps llenaría la tarjeta de 64 GB en 14 minutos. No compensa para clips de 10-60 s.

## Fuentes

- [File Format (still image)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659396.html)
- [RAW File Type](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659395.html)
- [JPEG/HEIF Switch](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000657944.html)
- [Movie Settings (movie)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000640834.html)
- [Memory cards that can be used](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000640149.html)
