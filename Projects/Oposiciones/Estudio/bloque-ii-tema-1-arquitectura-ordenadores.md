---
title: Bloque II, Tema 1 — Arquitectura de ordenadores
date: 2026-08-17
tags: [oposiciones, tai, temario, bloque-ii, estudio]
---

# Bloque II — Tema 1: Informática básica, representación de la información, arquitectura de ordenadores

Contenido completo (no solo introducción). Contexto en [[Projects/Oposiciones/Oposiciones|Oposiciones]] y temario en [[Projects/Oposiciones/temario-tai|Temario TAI]].

**Enunciado oficial** (Anexo V, BOE-A-2025-26262): *"Informática básica. Representación y comunicación de la información: elementos constitutivos de un sistema de información. Características y funciones. Arquitectura de ordenadores. Componentes internos de los equipos microinformáticos."*

**Sesión 1 — 2026-08-17.** Primera pasada + ampliación tras contraste con el examen real de mayo 2026.

## 1. Elementos constitutivos de un sistema de información

Un sistema de información no es solo "el programa" — son 5 piezas que trabajan juntas:

- **Hardware** — los equipos físicos (ordenador, servidor, red)
- **Software** — los programas que procesan la información
- **Datos** — la información en sí (lo que se guarda, mueve, consulta)
- **Procedimientos** — las normas de cómo se usa el sistema (protocolos, políticas)
- **Personas** — usuarios y administradores del sistema

## 2. Representación de la información

**Bit y byte:**
- Bit = unidad mínima (0 o 1). Byte = 8 bits.
- Múltiplos: **decimal** (1 KB = 1.000 bytes) vs. **binario** (1 KiB = 1.024 bytes) — distinción clásica de examen.

**Sistemas de numeración:**
- **Binario** (base 2), **octal** (base 8), **hexadecimal** (base 16).
- **Conversión hex↔binario**: cada dígito hexadecimal equivale exactamente a 4 bits (un "nibble"). Ej: hex `A` = binario `1010`. Por eso el hex es tan usado — es una forma compacta y directa de escribir binario, sin cálculo real de por medio.
- **Conversión binario→decimal**: suma de potencias de 2 en las posiciones con un 1. Ej: `1011` = 1·8 + 0·4 + 1·2 + 1·1 = 11.
- **Números negativos — complemento a dos**: la forma estándar de representar enteros negativos en binario (se invierten los bits del positivo y se suma 1). La usan prácticamente todos los procesadores actuales.
- **Coma flotante (estándar IEEE 754)**: cómo se representan los números con decimales — signo + exponente + mantisa. Es lo que hay detrás de los tipos `float`/`double` en cualquier lenguaje.

**Codificación de caracteres:**
- **ASCII**: 7-8 bits, alfabeto inglés básico + símbolos.
- **Unicode / UTF-8**: longitud variable (1 a 4 bytes por carácter) — los caracteres ASCII básicos ocupan 1 byte, emojis y alfabetos no latinos pueden ocupar hasta 4.

## 3. Arquitectura de ordenadores — el modelo de Von Neumann

- **CPU (Unidad Central de Proceso)**:
  - **Unidad de Control (UC)** — dirige y coordina las operaciones
  - **Unidad Aritmético-Lógica (ALU)** — hace los cálculos y comparaciones
  - **Registros**, incluyendo los específicos: **PC (Program Counter)** — guarda la dirección de la siguiente instrucción a ejecutar; **IR (Instruction Register)** — guarda la instrucción que se está ejecutando ahora mismo; **MAR/MBR** — registros de dirección y de datos de memoria
- **El ciclo de instrucción (fetch–decode–execute)** — cómo la CPU procesa cada instrucción, en 3 fases que se repiten sin parar:
  1. **Fetch (búsqueda)** — la UC busca en RAM la siguiente instrucción, señalada por el PC
  2. **Decode (decodificación)** — la UC interpreta qué operación pide esa instrucción
  3. **Execute (ejecución)** — la ALU (o el componente que corresponda) la ejecuta
- **Memoria principal (RAM)** — volátil, guarda instrucciones y datos mientras el equipo está encendido
- **Buses**: de **datos** (mueve la información), de **direcciones** (indica dónde está) y de **control** (coordina cuándo pasa cada cosa)
- **Dispositivos de entrada/salida (E/S)**
- **Von Neumann vs. Harvard**: Von Neumann comparte una única memoria para datos e instrucciones (de ahí el "cuello de botella" al acceder a ambos a la vez). La arquitectura **Harvard** separa memoria de datos y de instrucciones — se usa sobre todo en microcontroladores, no en PCs de propósito general.

## 4. Componentes internos de un equipo microinformático

- **Placa base** y **chipset** — conectan y coordinan todos los componentes
- **Procesador**: núcleos, frecuencia (GHz), y **jerarquía de caché precisa**:
  - **L1**: integrada físicamente dentro de cada núcleo, la más rápida y la más pequeña (normalmente dividida en caché de instrucciones y de datos)
  - **L2**: por núcleo o compartida entre pares de núcleos, más grande y algo más lenta que L1
  - **L3**: compartida entre todos los núcleos del procesador, la más grande y la más lenta de las tres
- **Memoria RAM**: tipos actuales (DDR4, DDR5)
- **Almacenamiento**:
  - **SSD**: dispositivo para almacenar datos en memoria no volátil, sin partes móviles
  - **HDD**: mecánico, con cabezales de lectura y discos magnéticos giratorios
  - **RAID** (formalmente Bloque IV, pero el examen real lo mezcló con este tema):
    - RAID 0: reparte datos entre discos (velocidad), sin redundancia — un fallo pierde todo
    - RAID 1: duplica los datos en dos discos (espejo) — tolera 1 fallo
    - **RAID 5: reparte datos + paridad entre 3+ discos — tolera exactamente 1 fallo de disco**
    - RAID 10: combina espejo (1) + reparto (0) — más caro, más robusto
- **Puertos y periféricos, con cifras reales** (esto ya amplía hacia el Tema 2, pero el examen los mezcló aquí):
  - USB: 2.0 = 480 Mbps · 3.0 = 5 Gbps · 3.1 = 10 Gbps · 3.2 = 20 Gbps · USB4 = 40 Gbps
  - **HDMI 2.1: 48 Gbps de ancho de banda máximo**
  - SATA III: 6 Gbps · PCIe 4.0 (por carril): ~2 GB/s
- **Fuente de alimentación**: convierte la corriente eléctrica al voltaje que necesitan los componentes

## Resumen para repaso rápido

| Concepto | Idea clave |
|---|---|
| Sistema de información | Hardware + Software + Datos + Procedimientos + Personas |
| KB vs KiB | Decimal (1.000) vs binario (1.024) |
| Hexadecimal | 1 dígito hex = 4 bits |
| Complemento a dos | Forma estándar de representar enteros negativos |
| IEEE 754 | Estándar de coma flotante para números con decimales |
| Ciclo de instrucción | Fetch → Decode → Execute |
| Von Neumann vs Harvard | Memoria compartida vs. memoria separada (datos/instrucciones) |
| Caché L1/L2/L3 | L1 dentro del núcleo (más rápida, más pequeña) → L3 compartida (más lenta, más grande) |
| SSD vs HDD | No volátil sin partes móviles vs. mecánico con cabezales |
| RAID 5 | Tolera 1 fallo de disco |
| HDMI 2.1 | 48 Gbps máximo |

## Contraste con el examen real — hecho

Del [Cuestionario Modelo A](https://sede.inap.gob.es/sites/sede/files/public/2026-05/Cuestionario%20TAI-L-ModeloA.pdf) (examen real, mayo 2026), preguntas 23-27 caen directamente sobre este tema:

- **P23** (nivel de caché integrado en el núcleo → L1) — lo teníamos, pero sin el detalle "integrada dentro del núcleo"
- **P24** (función del bus del sistema) — coincide exacto con lo estudiado ✓
- **P25** (características de un SSD) — coincide en concepto; la formulación exacta del examen ("memoria no volátil sin partes móviles") no la teníamos memorizada así
- **P26** (ancho de banda máximo HDMI 2.1 = 48 Gbps) — no lo cubríamos, dato muy específico
- **P27** (tolerancia a fallos de RAID 5 = 1 fallo) — no lo cubríamos, formalmente de otro bloque pero mezclado en el examen

**Resultado: 3 de 5 con la versión introducción, 5 de 5 con la ampliación de hoy.** Confirma el patrón: el examen premia el dato exacto, no solo el concepto — por eso a partir de ahora se estudia el contenido completo desde el principio, no en pasadas sucesivas.

## Estado

✅ `repasado` — contenido completo + contraste con examen real hecho el 2026-08-17.
