---
title: Accesibilidad — etiquetas de App Store y mejoras pendientes
date: 2026-07-11
tags: [culla, idea, accessibility, app-store]
---

# Accesibilidad: qué marcar en App Store Connect y qué implementar

Auditoría del código (2026-07-11) frente a las *Accessibility Nutrition Labels* de App Store Connect. Contexto: [[Projects/Culla/Culla|Culla]].

## Estado actual

| Prestación | ¿Marcable? | Situación |
|---|---|---|
| Interfaz oscura | ✅ Sí | Ajuste sistema/claro/oscuro en `CullaApp.swift`; las vistas adaptan colores. |
| Diferenciar no solo con color | 🟡 Probable | Iconos/texto acompañan al color (overlay de borrar, nombres de galerías). Falta repaso visual. |
| Reducir movimiento | 🟠 Casi | Los `symbolEffect` lo respetan solos, pero el fondo animado (`PhotoCarouselBackground.swift`) no consulta el ajuste del sistema. |
| Texto más grande | ❌ No | ~31 fuentes de tamaño fijo (`.system(size:)`) que no escalan; Apple exige 200 %. |
| VoiceOver | ❌ No | Solo `SortChip` tiene etiqueta. Tarjetas de fotos y gesto de deslizar sin etiquetas ni acciones alternativas. |
| Control de voz | ❌ Sin probar | Botones estándar funcionan gratis; el flujo principal depende de gestos de arrastre. Probar en iPhone real. |
| Contraste suficiente | ❓ | El cristal translúcido es arriesgado. Medir texto/fondo (mínimo 4.5:1) en pantalla real. |
| Subtítulos / Audiodescripciones | ➖ No aplica | Reproduce vídeos caseros del usuario sin pistas de subtítulos. No marcar. |

## Implementaciones futuras (de más fácil a más difícil)

1. **Reducir movimiento** — leer `@Environment(\.accessibilityReduceMotion)` y pausar el stream de fotos (ya existe `isPaused` en el `TimelineView`). Pocas líneas.
2. **Texto más grande** — cambiar las fuentes fijas de *texto real* (Paywall, números de Insights, botones, `GlassPanel`) a `.system(size:…, relativeTo: .title)` para que escalen con Dynamic Type. Los tamaños fijos en iconos decorativos pueden quedarse.
3. **Contraste + color** — pasada visual con el ajuste de contraste alto y comprobación 4.5:1 sobre los paneles de cristal.
4. **VoiceOver** (la grande) — etiquetas en tarjetas de fotos (fecha, tipo), `accessibilityAction` para reemplazar el deslizar (conservar / borrar), y recorrido completo del flujo principal.
5. **Control de voz** — probar en dispositivo una vez hecho lo de VoiceOver; suele venir casi gratis después.

## Qué marcar hoy en App Store Connect

Solo **Interfaz oscura** (y **Diferenciar no solo con color** tras el repaso visual). Añadir las demás según se implementen — marcar de más puede dar rechazo o mala experiencia real.
