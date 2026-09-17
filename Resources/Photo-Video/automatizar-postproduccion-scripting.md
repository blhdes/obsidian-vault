---
title: Automatizar la postproducción fotográfica con scripting (sin Lightroom)
date: 2026-09-17
tags: [photo-video, workflow, scripting, raw, darktable, automatizacion]
---

Pregunta: ¿se puede sustituir el trabajo tedioso de edición por scripting, ahora que ya no uso Lightroom? Respuesta de Claude, guardada como referencia antes de montar el flujo de trabajo. Relacionado: [[Resources/Photo-Video/open-source-alternatives]], [[Resources/Photo-Video/darktable-manual-basico]].

Resumen: sí para una parte, no para otra, y la diferencia importa mucho antes de montar un flujo de trabajo alrededor de esto.

## Dónde sí ahorra días de verdad

Todo lo repetitivo y mecánico, que suele ser el 70% del tiempo real de una entrega:

- **Ingesta y organización**: copiar de la tarjeta, verificar checksums, renombrar por fecha/evento/número, estructura de carpetas, backup a dos destinos.
- **Culling asistido**: descartar fotos desenfocadas (medida de nitidez por varianza del laplaciano), detectar ráfagas casi idénticas y quedarse con la más nítida, filtrar por EXIF (todo lo que salga a ISO 12800 o a 1/15, por ejemplo).
- **Revelado por lotes con un preset propio**: aquí está el truco. Defines el look en 5 o 10 fotos de referencia en Lightroom, Capture One o darktable, exportas el ajuste (`.xmp`, `.pp3`, preset `.dng`), y el script lo aplica a las 800 restantes con `darktable-cli` o `rawtherapee-cli`, con variantes por condición de luz (interior, exterior, contraluz).
- **Igualar exposición y balance de blancos entre fotos** de la misma escena, que es tedioso a mano y es puro cálculo.
- **Entrega**: exportar en tres tamaños a la vez, sRGB para web y AdobeRGB para imprenta, marca de agua, limpiar o conservar metadatos según cliente, galería de contactos en PDF, empaquetar y nombrar según lo que pida cada cliente.

Eso es reproducible, auditable y se ejecuta en minutos sobre cientos de RAW.

## Dónde no sirve

- **El criterio visual fino.** Claude ve las imágenes a baja resolución, sin gestión de color y sin pantalla calibrada. No puede juzgar un tono de piel, un viraje sutil en las sombras ni si un verde se ha ido. Cualquier decisión de color la tomo yo.
- **Retoque de píxel**: piel, dodge and burn, licuar, eliminar elementos, máscaras complejas. Eso es Photoshop a mano.
- **Las máscaras de IA de Lightroom o los ajustes locales de Capture One**: no las sustituye.

O sea: no es un editor, es un ayudante de postproducción. El ojo lo pongo yo una vez, el script lo multiplica por 800.

## Herramientas: entorno ya montado (17-09-2026)

Todo instalado y verificado. Nada de esto depende de Adobe.

| Herramienta | Versión | Para qué | Cómo se llama |
|---|---|---|---|
| `darktable-cli` | 5.6.1 | aplicar presets `.xmp` por lotes a RAW | `darktable-cli` (enlace creado en `/opt/homebrew/bin` que apunta dentro de darktable.app) |
| `exiftool` | 13.55 | leer/escribir metadatos EXIF, IPTC, XMP | `exiftool` |
| `vips` | 8.18.6 | procesado rápido de archivos grandes, redimensionado, conversión | `vips`, `vipsthumbnail` |
| `rawpy` | 0.27.1 (LibRaw 0.22.1) | decodificar RAW desde Python | dentro del entorno `~/.venvs/foto` |

### El entorno de Python

Las librerías de foto viven en un entorno virtual propio, **no** en el Python del sistema, para no mezclarlas con nada más y poder borrarlo entero sin romper nada:

```
~/.venvs/foto/
```

Contiene: `rawpy` 0.27.1, `numpy` 2.4.6, `pillow` 12.3.0, `scipy` 1.17.1, `imageio` 2.37.4.

Para ejecutar un script con ese entorno se llama a su Python por la ruta completa, sin activar nada:

```bash
~/.venvs/foto/bin/python mi_script.py
```

Instalar algo más ahí dentro:

```bash
~/.venvs/foto/bin/python -m pip install <paquete>
```

### Notas sueltas

- `vips` lee RAW de Sony (`.arw`) directamente vía dcraw, además de `.cr2`, `.cr3`, `.nef`, `.dng` y prácticamente cualquier otro formato de cámara.
- `darktable-cli` no venía en el PATH porque darktable lo esconde dentro del `.app`. El enlace lo arregla. Si algún día actualizas darktable y deja de funcionar, se rehace con:
  ```bash
  ln -sf /Applications/darktable.app/Contents/MacOS/darktable-cli /opt/homebrew/bin/darktable-cli
  ```
- Aún sin probar sobre un RAW real: no hay ningún `.ARW` en el Mac ahora mismo. La primera sesión de fotos sirve de banco de pruebas.

## Siguiente paso

Para dimensionar cuánto del proceso actual es criterio y cuánto es trabajo mecánico automatizable, hace falta definir: qué cámara, en qué programa revelo ahora, y cómo es una entrega típica (cuántas fotos, qué formatos pide el cliente).

Plan: convertir todo esto en una **skill de Claude** dedicada a esta área, una vez el flujo esté probado sobre una entrega real. La skill documentada irá en `Areas/Claude/Skills/` según la convención del vault.
