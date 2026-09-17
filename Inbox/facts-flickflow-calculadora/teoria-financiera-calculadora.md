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
Micro (MNQ) y E-nano (NNQ). Son **contratos distintos sobre el mismo índice**, de tamaño
(multiplicador) distinto, pensados para que cuentas de distinto tamaño puedan operarlo sin
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
- **Arriba**: redondea al entero superior (con 0,3125 contratos, a uno entero), así que puede
  **superar** el % de riesgo que te habías marcado. De ahí el aviso que muestra el código cuando
  esto ocurre (ámbar en el original, naranja de acento en la versión integrada).

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
  margen depositado ya no cubre la pérdida acumulada. Es una fórmula simplificada: no tiene en
  cuenta comisiones, funding ni, sobre todo, el **margen de mantenimiento** (el mínimo que el
  exchange exige mantener en la posición). En un exchange real la liquidación llega antes, así que
  el precio real de liquidación está algo más cerca de la entrada que el que muestra la calculadora.

**El aviso crítico** (`stopAntesLiq` en el código): si el stop loss está *más allá* del precio de
liquidación, el exchange liquida la posición **antes** de que el stop llegue a saltar — se pierde
el margen entero (mucho más que el riesgo planeado), no la pérdida controlada que se había
calculado. Es uno de los errores de razonamiento más peligrosos en trading apalancado, y es
justo lo que este aviso previene.

## 10. Y esto, ¿para qué más sirve?

[[ideas-fuera-de-alcance|Ideas fuera de alcance]] apuntaba que un bloque de texto instructivo en
la propia página quedaba fuera del alcance de la prueba. El 2026-09-17 el usuario propuso una
versión acotada: un **Info View** inspirado en el de Ableton Live, que explica cada campo al pasar
el ratón (o al tocarlo en el móvil). Esta nota es la base de la que salen sus textos (ver abajo).

## Revisión (2026-09-17)

Revisada contra el código de la calculadora. Los conceptos y fórmulas son correctos. Correcciones:

- §5: los tiers no son "el mismo producto", son **contratos distintos** sobre el mismo índice.
- §7: redondear arriba no siempre acerca al número exacto (0,3125 → 1 se aleja más que → 0);
  lo que hace es subir al entero superior.
- §9: la fórmula de liquidación tampoco tiene en cuenta el **margen de mantenimiento**, que en
  la práctica adelanta la liquidación.
- Duda abierta: no he podido confirmar que los tiers "E-nano" (NNQ, NES, NDOW, N2K) existan como
  contratos del CME. Son datos del cliente; mejor no afirmar nada sobre ellos en los textos.

Sobre lo "técnico": lo que más pesa son los nombres del código (`riesgoPct`, `syncDesdePrecios`,
`stopAntesLiq`) mezclados con la explicación. Los conceptos en sí son asequibles.

## Textos del Info View

Una o dos frases por elemento, sin nombres de código. Reglas de voz de Flickflow (`home.ts`):
se dice "trader", sin promesas de rentabilidad ni señales.

| Elemento | Texto |
|---|---|
| Activo | El mercado que quieres operar. Cada activo tiene sus propios contratos, y cada contrato gana o pierde una cantidad fija de dinero por cada salto de precio. |
| Tamaño de cuenta | El dinero total con el que operas. Es la base sobre la que se calcula cuánto puedes perder en esta operación. |
| Riesgo por operación | El porcentaje de tu cuenta que aceptas perder si la operación sale mal. Es una regla que te pones tú, no un dato del mercado: muchos traders usan entre el 1 % y el 2 %. |
| Dirección | Compra si esperas que el precio suba, venta si esperas que baje. Decide a qué lado de la entrada va el stop: por debajo en una compra, por encima en una venta. |
| Precio de entrada | El precio al que abres la operación. Junto con el stop, marca cuánto puede moverse el precio en tu contra. |
| Precio de stop | El precio al que se cierra la operación si va en tu contra, para que la pérdida no siga creciendo. Basta con rellenar este campo o la distancia. |
| Distancia del stop | Cuánto tiene que moverse el precio en tu contra hasta llegar al stop, en puntos. Si la escribes, el precio de stop se calcula solo, y al revés. |
| Tamaño del tick | El salto mínimo que puede dar el precio de un contrato. Por ejemplo, el Nasdaq 100 se mueve de 0,25 en 0,25 puntos. |
| Valor del tick | Cuánto dinero gana o pierde un contrato por cada tick. Lo fija el mercado donde cotiza, no se elige. |
| Apalancamiento | Cuánto mercado controlas por cada dólar que depositas: con 10x, 1.000 $ controlan 10.000 $. Cuanto más alto, más cerca de tu entrada queda el precio de liquidación. |
| Contratos a operar | Cuántos contratos de cada tamaño puedes abrir sin que la pérdida, si salta el stop, pase de tu riesgo permitido. El número pequeño es el resultado exacto, antes de redondear. |
| Tamaño de posición (perpetuo) | Cuántas unidades del activo puedes operar sin que la pérdida, si salta el stop, pase de tu riesgo permitido. Debajo: el valor total que controlas, el dinero que depositas y el precio aproximado de liquidación. |
| Redondeo | No se pueden operar fracciones de contrato. Abajo te mantiene dentro de tu riesgo; arriba sube al entero siguiente y puede pasarse del porcentaje que marcaste. |
| Ficha del contrato | Los datos fijos de cada contrato: su tick, cuánto vale cada tick y cuánto vale cada punto (o pip, en divisas). De ahí sale el cálculo del resultado. |

---

Volver a [[brief-tecnico|Brief técnico]] · [[facts-flickflow-calculadora|Índice del proyecto]]
