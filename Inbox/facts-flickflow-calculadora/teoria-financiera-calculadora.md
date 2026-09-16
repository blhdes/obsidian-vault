---
title: Teoría financiera de la calculadora — Flickflow
date: 2026-09-16
tags: [career, technical-test, flickflow, facts, trading, finanzas]
---

# Teoría financiera de la calculadora — Flickflow

Ver [[facts-flickflow-calculadora|índice del proyecto]] y [[brief-tecnico|brief técnico]] para el
contexto general. Esta nota explica, desde cero, **qué calcula exactamente**
`prueba-tecnica/calculadora-posicion-futuros.html` y por qué — pensada para quien no tiene
formación previa en teoría financiera. Cada concepto se enlaza con la fórmula real que aparece en
el `<script>` del archivo.

## 1. Qué problema resuelve esto: "tamaño de posición"

La calculadora **no** predice si una operación (un "trade") va a salir bien o mal. Eso no lo sabe
nadie de antemano. Lo que hace es otra cosa, más aburrida pero mucho más importante: decidir
**cuánto** arriesgar en cada operación para que, si sale mal, la pérdida sea pequeña y controlada
— y así poder encajar una racha de operaciones perdidas sin quedarse sin cuenta.

Esto se llama **gestión de riesgo** (*risk management*), y "tamaño de posición" (*position
sizing*) es la técnica concreta: calcular cuántas unidades de un activo comprar o vender para que
una pérdida máxima, en dinero, quede fijada de antemano.

## 2. Los inputs base: cuenta, riesgo y dólares en juego

- **Cuenta** (`cuenta`): el capital total con el que se opera. En el ejemplo del HTML, 25.000 $.
- **Riesgo por operación** (`riesgoPct`): el porcentaje de la cuenta que se está dispuesto a
  perder en **esta** operación concreta, si sale mal. No es un dato del mercado, es una regla de
  disciplina que se impone el propio trader — habitualmente 1-2 %. Arriesgar más que eso por
  operación es lo que hace que una mala racha (5-10 pérdidas seguidas, algo normal
  estadísticamente) pueda arruinar una cuenta entera.
- **Riesgo en dólares**: `riesgoDolares = cuenta × (riesgoPct / 100)`. Con los valores por
  defecto: 25.000 × 1 % = **250 $**. Este es el número que de verdad importa: la pérdida máxima
  aceptada para el trade, en dinero real.

## 3. Precio de entrada y stop loss

- **Precio de entrada** (`entrada`): el precio al que se abre la operación.
- **Stop loss** (`stop`): el precio al que se cierra la operación automáticamente si el mercado va
  en contra, para cortar la pérdida ahí y no dejar que siga creciendo.
- **Distancia del stop**: `distanciaPrecio = |entrada − stop|`. Cuánto tiene que moverse el precio
  en contra antes de que salte el stop.

La calculadora deja rellenar el stop **por precio** o **por distancia en puntos**, y sincroniza
los dos automáticamente (`syncDesdePrecios` / `syncDesdePuntos`) según la **dirección**:

- **Compra** (posición "larga", se gana si el precio sube): el stop va **por debajo** de la
  entrada.
- **Venta** (posición "corta", se gana si el precio baja): el stop va **por encima** de la
  entrada.

## 4. Qué es un futuro y qué es un "tick"

Un **futuro** es un contrato estandarizado para comprar o vender un activo (un índice bursátil,
una materia prima, una divisa, un bono, incluso cripto) a un precio acordado, negociado en un
mercado organizado (un *exchange*, como el CME). A diferencia de comprar el activo directamente,
un futuro es un instrumento **apalancado**: con un depósito relativamente pequeño se controla una
exposición mucho mayor — y el exchange, no el trader, fija cuánto vale cada movimiento de precio.

- **Tick**: el movimiento mínimo de precio que el contrato puede tener. Por ejemplo, el futuro del
  Nasdaq 100 (NQ) se mueve en saltos de 0,25 puntos — no puede moverse 0,1.
  - **Valor del tick** (`vt`): cuántos dólares vale ese movimiento mínimo, **para un solo
    contrato**. Viene fijado por el exchange, no se elige. Para el NQ: tick = 0,25 puntos =
    **5 $**. Eso significa que un punto entero de índice vale 20 $/contrato (5 $ ÷ 0,25).

## 5. Por qué existen "tiers" (E-mini, Micro, E-nano...)

En el código, cada activo tiene varios `tiers`: por ejemplo el Nasdaq aparece como E-mini (NQ),
Micro (MNQ) y E-nano (NNQ). **No son productos distintos** — es el mismo índice, con contratos de
tamaño (multiplicador) distinto, pensados para que cuentas de distinto tamaño puedan operarlo sin
que el riesgo en dólares por contrato se dispare. Un contrato Micro tiene un valor de tick mucho
más pequeño que uno E-mini, así que hace falta arriesgar mucho menos dinero por cada uno.

## 6. La fórmula central, paso a paso

Usando los valores por defecto del HTML (cuenta 25.000 $, riesgo 1 %, NQ E-mini, entrada 18.000,
stop 17.960 → distancia 40 puntos):

```
riesgo permitido ($)     = cuenta × riesgoPct%           = 25.000 × 1%      = 250 $
riesgo por contrato ($)  = (distancia / tick) × valorTick = (40 / 0,25) × 5 = 800 $
contratos                = riesgo permitido / riesgo por contrato = 250 / 800 = 0,3125
```

Esto es exactamente lo que hace `calcular()` en el código, para cada `tier` del activo elegido.

**¿Qué significa un resultado de 0,3125 contratos?** Que, con esta cuenta y esta regla de riesgo,
ni un solo contrato E-mini "cabe" dentro del 1 % de riesgo permitido — operar uno solo ya
arriesgaría 800 $ (3,2 % de la cuenta), muy por encima de la regla. Hace falta bajar al tier Micro
o E-nano (con un valor de tick mucho menor) para que el número de contratos se acerque a un
entero razonable dentro del presupuesto de riesgo.

## 7. El redondeo: por qué hace falta y qué implica

No se pueden comprar 0,3125 contratos — solo unidades enteras. La calculadora ofrece dos opciones:

- **Abajo** (por defecto, más conservador): te quedas *por debajo* del riesgo permitido. Nunca
  arriesgas más de lo que decidiste, aunque el uso de tu presupuesto de riesgo sea menos eficiente.
- **Arriba**: te acerca más al número exacto, pero puede **superar** el % de riesgo que te habías
  marcado — de ahí el aviso en ámbar que muestra el código cuando esto ocurre.

## 8. La ficha del contrato: $/punto y $/pip

El bloque "ficha del contrato" muestra cuánto vale cada punto (o pip) de movimiento:

- Activos normales: `valorTick / tick` → dólares por **punto** de precio.
- FX (divisas): `valorTick × (pip / tick)` → dólares por **pip**.

Un **pip** es la unidad en la que los traders de FX hablan del movimiento del precio por
convención (normalmente 0,0001 para la mayoría de pares) — no siempre coincide con el tick real
(el incremento mínimo que el exchange permite), que puede ser más fino. Por eso el código separa
ambos conceptos.

## 9. El modo perpetuo (cripto)

Un **perpetual swap** (o "futuro perpetuo") es un derivado parecido a un futuro normal, pero **sin
fecha de vencimiento** — se puede mantener abierto indefinidamente. Sigue el precio al contado
("spot") del activo mediante un mecanismo llamado *funding rate* (un pequeño pago periódico entre
compradores y vendedores que mantiene el precio del perpetuo pegado al spot; no hace falta entrar
en más detalle para entender la calculadora).

Al no tener contratos de tamaño fijo, el cálculo cambia de forma: en vez de "contratos", se calcula
una **cantidad** de unidades del activo:

```
cantidad     = riesgoDolares / distanciaPrecio
nocional     = cantidad × entrada
margen       = nocional / apalancamiento
precio liq.  ≈ entrada × (1 − 1/apalancamiento)   (posición larga)
             ≈ entrada × (1 + 1/apalancamiento)   (posición corta)
```

- **Apalancamiento** (*leverage*): cuánta exposición se controla por cada dólar de margen
  depositado. Con 10x, 1.000 $ de margen controlan 10.000 $ de exposición.
- **Nocional**: el valor total de mercado que se controla, como si no hubiera apalancamiento.
- **Margen**: el capital real que hay que depositar para abrir esa posición apalancada.
- **Precio de liquidación**: el precio al que el exchange cierra la posición a la fuerza porque el
  margen depositado ya no cubre la pérdida acumulada. Es una fórmula simplificada (sin comisiones
  ni funding), pero suficiente para la idea.

**El aviso crítico** (`stopAntesLiq` en el código): si el stop loss está *más allá* del precio de
liquidación, el exchange liquida la posición **antes** de que el stop llegue a saltar — se pierde
el margen entero (mucho más que el riesgo planeado), no la pérdida controlada que se había
calculado. Es uno de los errores de razonamiento más peligrosos en trading apalancado, y es
justo lo que este aviso previene.

## 10. Y esto, ¿para qué más sirve?

[[ideas-fuera-de-alcance|Ideas fuera de alcance]] apunta que un bloque de texto instructivo en la
propia página (explicando qué es el "tamaño de posición" o cómo usar la calculadora) quedó fuera
del alcance de la prueba técnica, por no pedirlo el cliente y por riesgo de sobre-construir el
entregable. Esta nota es, en efecto, la base de conocimiento de la que saldría ese texto si algún
día se decide escribirlo.

---

Volver a [[brief-tecnico|Brief técnico]] · [[facts-flickflow-calculadora|Índice del proyecto]]
