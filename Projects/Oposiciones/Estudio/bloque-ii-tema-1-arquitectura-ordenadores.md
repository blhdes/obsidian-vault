---
title: Bloque II, Tema 1 — Arquitectura de ordenadores
date: 2026-08-17
tags: [oposiciones, tai, temario, bloque-ii, estudio]
---

# Bloque II — Tema 1: Informática básica, representación de la información, arquitectura de ordenadores

Primera sesión de estudio real del temario TAI. Contexto completo en [[Projects/Oposiciones/Oposiciones|Oposiciones]] y listado del temario en [[Projects/Oposiciones/temario-tai|Temario TAI]].

**Enunciado oficial del tema** (Anexo V, BOE-A-2025-26262): *"Informática básica. Representación y comunicación de la información: elementos constitutivos de un sistema de información. Características y funciones. Arquitectura de ordenadores. Componentes internos de los equipos microinformáticos."*

**Sesión 1 — 2026-08-17.** Sin manual todavía (biblioteca sin ediciones recientes, muestras de academia solo dan el Tema 1 del Bloque I). Contenido explicado en sesión + apuntes propios.

## 1. Elementos constitutivos de un sistema de información

Un sistema de información no es solo "el programa" — son 5 piezas que trabajan juntas:

- **Hardware** — los equipos físicos (ordenador, servidor, red)
- **Software** — los programas que procesan la información
- **Datos** — la información en sí (lo que se guarda, mueve, consulta)
- **Procedimientos** — las normas de cómo se usa el sistema (protocolos, políticas)
- **Personas** — usuarios y administradores del sistema

*Paralelismo con tu experiencia:* cuando construyes una app como Culla, el "sistema de información" completo no es solo el código Swift — es el iPhone (hardware), las fotos y metadatos del usuario (datos), cómo se espera que se use la app (procedimientos) y la persona que la usa. La oposición pide saber nombrar esas 5 piezas de forma formal.

## 2. Representación de la información

**Bit y byte:**
- Bit = unidad mínima (0 o 1). Byte = 8 bits.
- Múltiplos: ojo con la diferencia entre **decimal** (1 KB = 1.000 bytes, usado por fabricantes de almacenamiento) y **binario** (1 KiB = 1.024 bytes, usado por sistemas operativos) — esta distinción cae con frecuencia en preguntas tipo test.

**Sistemas de numeración:**
- **Binario** (base 2): el lenguaje nativo del hardware.
- **Octal** (base 8) y **Hexadecimal** (base 16): formas compactas de representar binario. El hexadecimal ya lo conoces de los colores CSS (`#FF5733`) — cada par de dígitos hex son 8 bits (1 byte). En informática de sistemas se usa igual, para direcciones de memoria, direcciones MAC, volcados de depuración, etc.

**Codificación de caracteres:**
- **ASCII**: 7-8 bits, cubre el alfabeto inglés básico + símbolos.
- **Unicode / UTF-8**: longitud variable, cubre todos los alfabetos y emojis. Los `String` de Swift ya son Unicode internamente — este concepto ya lo usas sin pensarlo.

## 3. Arquitectura de ordenadores — el modelo de Von Neumann

Casi todos los ordenadores actuales siguen este esquema clásico:

- **CPU (Unidad Central de Proceso)**, dividida en:
  - **Unidad de Control (UC)** — dirige y coordina las operaciones
  - **Unidad Aritmético-Lógica (ALU)** — hace los cálculos y comparaciones
  - **Registros** — memoria ultra-rápida dentro del propio procesador
- **Memoria principal (RAM)** — guarda instrucciones y datos mientras el equipo está encendido; es volátil (se borra al apagar)
- **Buses** — las "carreteras" que conectan los componentes:
  - Bus de **datos** — mueve la información
  - Bus de **direcciones** — indica dónde está esa información
  - Bus de **control** — coordina cuándo pasa cada cosa
- **Dispositivos de entrada/salida (E/S)** — teclado, pantalla, disco, red

## 4. Componentes internos de un equipo microinformático

- **Placa base**: conecta físicamente todos los componentes; incluye el **chipset**, que gestiona la comunicación entre ellos.
- **Procesador (CPU)**: número de **núcleos**, **frecuencia** (GHz), y **caché** (L1/L2/L3 — memoria intermedia, cada vez más grande pero más lenta, entre el procesador y la RAM).
- **Memoria RAM**: tipos actuales (DDR4, DDR5), medida en capacidad (GB).
- **Almacenamiento**: HDD (mecánico, más barato/lento) vs. SSD (electrónico, más rápido) — distinción básica; el detalle de periféricos de almacenamiento se amplía en el Tema 2.
- **Fuente de alimentación**: convierte la corriente eléctrica al voltaje que necesitan los componentes.

## Resumen para repaso rápido

| Concepto | Idea clave |
|---|---|
| Sistema de información | Hardware + Software + Datos + Procedimientos + Personas |
| KB vs KiB | Decimal (1.000) vs binario (1.024) |
| Hexadecimal | Compacta binario, 1 dígito hex = 4 bits |
| Von Neumann | CPU (UC+ALU+registros) + RAM + Buses + E/S |
| Caché | Memoria intermedia rápida entre CPU y RAM (L1→L2→L3) |
| SSD vs HDD | Electrónico y rápido vs. mecánico y lento |

## Contraste con el examen real

**Pendiente** — siguiente sesión: repasar el [Cuestionario Modelo A](https://sede.inap.gob.es/sites/sede/files/public/2026-05/Cuestionario%20TAI-L-ModeloA.pdf) y el [Modelo B](https://sede.inap.gob.es/sites/sede/files/public/2026-05/Cuestionario%20TAI-L-ModeloB.pdf) del examen real de mayo 2026, localizar las preguntas relacionadas con arquitectura/representación de la información, y comprobar si este contenido responde bien a ese nivel real.

## Estado

`en curso` — primera pasada del Tema 1 hecha. Falta: contraste con examen real, y un repaso en unos días antes de pasar al Tema 2.
