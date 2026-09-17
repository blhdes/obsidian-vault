---
title: Sony a7 IV — disparar en RAW (y por qué salían .HIF)
date: 2026-09-18
tags: [photo-video, sony, a7iv, raw, heif, camara, ajustes]
---

Menús en **inglés**, que es como tengo la cámara. Rutas verificadas contra la guía oficial de Sony para la ILCE-7M4.

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

## Ajuste recomendado para trabajos

| Ajuste | Valor |
|---|---|
| File Format | RAW (o RAW & JPEG si hace falta previo) |
| RAW File Type | Lossless Comp (L) |
| JPEG/HEIF Switch | JPEG |

## Fuentes

- [File Format (still image)](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659396.html)
- [RAW File Type](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000659395.html)
- [JPEG/HEIF Switch](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000657944.html)
