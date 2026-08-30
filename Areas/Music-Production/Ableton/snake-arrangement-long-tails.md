---
title: MDD SnAkE en Arrangement — Imprimir Secuencia y Colas Largas
date: 2026-08-30
tags: [ableton, snake, mdd, max-for-live, arrangement-view, freeze, resampling, ethereal-canyon]
---

# MDD SnAkE en Arrangement — imprimir secuencia y colas largas (Ethereal Canyon)

## El problema de fondo

**SnAkE es un secuenciador MIDI generativo.** Dispara notas por su propio reloj interno e **ignora por completo los clips MIDI de la pista**. El clip solo actúa como contenedor para que la pista suene; las notas las genera el dispositivo, no el clip. Por eso "ningún clip cuenta".

Cuando el instrumento (p. ej. **Ethereal Canyon**) tiene **reverb + delay muy largos**, aparece un segundo problema: la **cola de audio** nace en tiempo real *después* de que la nota deja de sonar, así que no cabe dentro del bloque exacto de bars donde ocurre la nota. Imprimir solo el MIDI no resuelve esto, porque la cola no es MIDI: es audio generado a posteriori.

**Regla general:** para la secuencia rítmica → imprime MIDI. Para la cola larga → captura AUDIO.

---

## Paso 1 — Imprimir el MIDI del SnAkE a una pista aparte

Fija la secuencia como notas reales, editables y con arreglo estándar.

1. Pon el SnAkE en una pista MIDI y ajústalo como quieras (shapes, gates, notas, swing).
2. Crea una **segunda pista MIDI**.
   - *MIDI From* → la pista del SnAkE.
   - Desplegable inferior → **Post FX** (captura la salida ya procesada por el SnAkE).
   - *Monitor* → **In**.
3. Arma (record enable) la segunda pista y graba en Arrangement.
4. Las notas quedan impresas como clip MIDI normal, ya sin depender del dispositivo. A partir de aquí puedes desactivar/quitar el SnAkE y editar con clips reales (cortar, mover, duplicar por sección, etc.).

> Esto es lo que el propio autor recomienda para grabar la secuencia: enrutar la salida MIDI del SnAkE hacia otra pista MIDI.

---

## Paso 2 — Capturar la cola larga como AUDIO

Aquí es donde encaja el carácter de Ethereal Canyon (reverb + delay largos). Dos enfoques.

### Opción A — Resample a audio (la más limpia para encajar en estructura)

1. Con el MIDI ya impreso disparando el instrumento, crea una **pista de audio** nueva.
2. Configúrala:
   - *Audio From* → la pista del instrumento (o **Resampling**).
   - *Monitor* → **In**.
   - Armar.
3. Graba **dejando correr la grabación varios bars de más** tras la última nota, para que la cola de reverb + delay se registre **entera** como audio.
4. Resultado: un clip de audio donde el cuerpo rítmico encaja en los bars exactos y la cola se extiende de forma natural más allá. Colócalo en Arrangement empezando en el bar exacto que quieras; la cola se solapa con lo que venga después, como en una mezcla real.

### Opción B — Freeze & Flatten (rápida, sin routing)

1. Con la pista del instrumento (SnAkE + Ethereal Canyon) sonando en Arrangement: clic derecho → **Freeze Track**.
2. Ableton añade por defecto tiempo de cola extra al freeze, precisamente para capturar reverbs/delays largos.
3. Luego **Flatten** → queda audio con la cola incluida.

> **Aviso con colas muy largas:** el freeze captura un margen de cola **limitado**. Si el delay es de varios segundos con feedback alto, la cola puede **truncarse**. En ese caso usa la Opción A (grabar manualmente dejando correr los bars extra) para tener control total sobre cuánta cola conservas.

---

## Encajar en la estructura exacta de bars

- Lo que encaja en bars exactos es el **ataque/cuerpo rítmico**. La cola, por definición, es tiempo sobrante — y normalmente eso es **deseable**: quieres que la reverb de la última nota de una sección respire dentro de la siguiente.
- Si en cambio quieres que la cola **se corte en seco** en un punto (p. ej. antes de un drop): trabaja el **clip de audio ya impreso**, ponle un **fade out manual** en el bar exacto o recórtalo. Esto **solo** se puede hacer con audio, nunca con el MIDI.

---

## Truco recomendado: efectos en un Return Track

Para dar carácter sin que la cola se descontrole:

- Pon el **delay/reverb largo en un return track**, no dentro del instrumento.
- **Automatiza el send por secciones.**
- Así imprimes el instrumento **seco** en bars exactos y controlas la cola aparte, pudiendo cortarla o dejarla correr con una sola automatización de send.

---

## Control en directo dentro de Arrangement (si aún no imprimes)

Como el dispositivo no responde a clips, el "arreglo" en vivo se hace **automatizando parámetros por sección**:

- La mayoría de parámetros son **MIDI-mapeables**.
- Randomización enviando notas al dispositivo:
  - **C2** → randomiza *todos* los secuenciadores.
  - **D2** → randomiza *solo* las notas.
- Automatizar los **patrones compás a compás** funciona muy bien (reportado por usuarios).
- Para arrancar/parar limpio: usa el **on/off del dispositivo** o el **volumen de pista**, no clips.

---

## Detalles útiles del autor

- **Longitud de nota variable:** añade un MIDI Effect **Note Length** *después* del SnAkE y mapea el parámetro *custom* a la longitud.
- **Nota colgada al detener:** un **Note Length** o un filtro MIDI después del SnAkE ayuda a cortarla.

---

## Flujo recomendado (resumen)

1. Ajusta el SnAkE hasta tener la secuencia que quieres.
2. Imprime el **MIDI** a una segunda pista MIDI (Post FX) → secuencia fija y editable.
3. Captura el **audio** con la cola completa (Resample dejando correr bars extra, o Freeze & Flatten).
4. Ajusta la cola en el arreglo: dejarla respirar o fade/recorte manual en el bar exacto.
5. (Opcional) Efectos largos en un **return** con send automatizado para máximo control.

## Relacionado

- [[arrangement-view-basics|Arrangement View Basics]]
- [[exporting-your-track|Exporting Your Track]] (Render Tail para reverb)
- [[clip-envelopes|Clip Envelopes]]
