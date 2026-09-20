---
title: Darktable — manual de uso básico (RAW → catálogo → edición → exportación)
date: 2026-09-16
tags: [photo-video, darktable, raw, tutorial]
---

Flujo de trabajo completo desde que tienes una carpeta de RAW hasta que exportas la foto editada. Versión: darktable 5.6.1. Relacionado: [[Resources/Photo-Video/open-source-alternatives]].

> [!tip] Para revelar un lote entero con un mismo look
> Esta nota cubre editar **una** foto. Para construir un estilo reutilizable y aplicarlo a cientos por línea de comandos: [[Resources/Photo-Video/darktable-crear-estilos]].

## 0. Antes de abrir darktable

Ten tus RAW ya organizados en una carpeta normal del Finder, por ejemplo:

```
~/Fotos/2026-09-16-sesion-X/
```

Darktable **no mueve ni copia** tus archivos a una carpeta especial — trabaja directamente sobre donde ya están. Así que decide antes dónde va a vivir tu librería de fotos (disco interno, disco externo, etc.) porque si luego mueves la carpeta, darktable puede "perder" las fotos hasta que se lo indiques de nuevo.

## 1. Catálogo (Library)

Darktable usa un **catálogo** (una base de datos, no una copia de las fotos) para recordar qué ediciones has hecho a cada RAW.

- La primera vez que abres la app, ya crea un catálogo por defecto en `~/Library/Application Support/darktable/library.db`. Para uso normal (una sola persona, un único set de fotos en curso) **no hace falta crear catálogos nuevos** — usa el que viene por defecto.
- Si algún día quieres separar catálogos (por ejemplo, uno para trabajo y otro personal), al abrir darktable mantén pulsada la tecla `Option/⌥` mientras haces clic en el icono de la app: te deja elegir o crear otro archivo `.db`. Para empezar, ignora esto.

## 2. Importar las fotos

1. Abre darktable → entras en el módulo **Lighttable** (la vista de miniaturas, es la vista por defecto).
2. En el panel izquierdo, busca **"import"** (importar).
3. Elige **"add folder"** (añadir carpeta) si solo quieres que darktable "vea" la carpeta donde ya están tus RAW (no copia nada, solo indexa). Es la opción recomendada si ya tienes tu propio sistema de carpetas.
   - La alternativa **"import"** (a secas) sirve para cuando conectas una tarjeta SD/cámara y quieres que darktable copie las fotos a una carpeta que tú elijas mientras importa. Úsala si vienes directo de la tarjeta.
4. Selecciona la carpeta con tus RAW y confirma. Verás las miniaturas aparecer en el Lighttable.

Tip: activa la opción de "recursivo" si tienes subcarpetas dentro de la carpeta que importas.

## 3. Seleccionar una foto para editar

- En el Lighttable, haz doble clic sobre una miniatura → te lleva al módulo **Darkroom**, que es donde se edita.
- Puedes volver al Lighttable en cualquier momento con la tecla `L`, y volver a Darkroom con `D`.

## 4. Edición básica (Darkroom)

En Darkroom, la foto ocupa el centro y a la derecha tienes los **módulos** de edición, organizados por pestañas (activo, básico, color, efectos, etc.). Para empezar, con estos 5 módulos cubres el 90% de una edición básica:

1. **Exposición (exposure)** — sube o baja el brillo general de la foto. Es lo primero que se ajusta.
2. **Balance de blancos (white balance)** — corrige si la foto se ve muy azulada (fría) o muy anaranjada (cálida). Puedes usar los presets (nublado, sombra, tungsteno...) o el selector de "punto gris" haciendo clic sobre algo que sepas que es blanco/gris en la foto.
3. **Tono/contraste — "color balance rgb" o "contraste básico"** — controla el contraste general y la saturación del color. Es el módulo más potente de darktable, pero para lo básico basta con mover el control de contraste general.
4. **Recorte y rotación (crop)** — endereza el horizonte y recorta el encuadre si hace falta.
5. **Nitidez (sharpen)** — suele venir activado por defecto con un valor razonable; no hace falta tocarlo al principio.

Cómo activar un módulo: haz clic en su nombre para desplegarlo, mueve los sliders, y se aplica en tiempo real sobre la foto. Cada módulo tiene un interruptor a la izquierda de su nombre para activarlo/desactivarlo sin perder los ajustes.

Todo lo que edites es **no destructivo**: el archivo RAW original nunca se modifica, todo se guarda como instrucciones en el catálogo (y opcionalmente en un archivo `.xmp` al lado del RAW).

### Comparar antes/después
Pulsa la tecla `W` (o el botón correspondiente) para ver una comparación rápida del original vs. editado.

## 5. Exportar

Cuando termines de editar:

1. Vuelve al **Lighttable** (`L`).
2. Selecciona la(s) foto(s) que quieras exportar (clic, o `Cmd+A` para todas).
3. En el panel izquierdo busca el módulo **"export"** (exportar).
4. Configura:
   - **Formato de salida:** JPEG para compartir/web, TIFF si necesitas máxima calidad para seguir editando en otro programa.
   - **Tamaño máximo:** en píxeles, si quieres reducir el tamaño para redes sociales (ej. 2048 px en el lado largo). Déjalo en blanco para exportar a tamaño completo.
   - **Calidad JPEG:** 90-95 es un buen punto para uso normal.
   - **Carpeta de destino:** por defecto exporta a la misma carpeta que el RAW original, con sufijo. Puedes cambiarlo a otra carpeta tipo `~/Fotos/exportadas/`.
5. Haz clic en **"export"**. Aparece una barra de progreso; al terminar, la foto ya editada está en la carpeta que elegiste.

## Resumen del flujo completo

```
Carpeta con RAW  →  Lighttable: import (add folder)  →  doble clic en una foto (Darkroom)
→ exposición → balance de blancos → contraste/color → recorte → (nitidez ya viene bien)
→ volver a Lighttable → seleccionar fotos → export (JPEG/TIFF) → carpeta de destino
```
