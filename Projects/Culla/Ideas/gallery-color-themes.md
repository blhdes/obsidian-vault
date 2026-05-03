---
title: Gallery Color Themes
date: 2026-05-03
tags: [culla, idea, theming, ui, design-system]
---

# Gallery Color Themes

## Problem

Today, gallery colors are assigned **randomly** from a single hard-coded neon palette:

- `Models/Gallery.swift:38` — picks `Color.neonHexes[displayOrder % count]` at creation.
- `Views/GallerySidebarView.swift:69-96` — the only palette in the app (neons, with light/dark variants).

Every gallery in every user's setup ends up looking the same loud neon. There's no aesthetic choice — and no way to express a "calm" or "monochrome" mood.

## Idea

Introduce **theme palettes** the user can switch between. Each theme is a pre-defined color model that maps gallery `displayOrder` → display color, replacing the single `neonHexes` array.

### Proposed themes (8–10 to start)

1. **Neon** *(current default)* — high-saturation, electric.
2. **Pastel** — soft, low-saturation hues; friendly, calm.
3. **Metallic** — gold / silver / bronze / copper / gunmetal; premium feel.
4. **Mono Fade** — white → gray → black gradient steps for a clean, minimalist look.
5. **Cool Range** — tinted blues/violets/cyans only.
6. **Warm Range** — tinted yellows/oranges/reds only.
7. **Earth** — terracotta, moss, sand, slate; natural tones.
8. **Jewel** — emerald, ruby, sapphire, amethyst; deep saturated.
9. **Liquid Glass** — uses `.ultraThinMaterial` with varying transparency/tint instead of solid colors. Pairs with the existing material backgrounds in `GallerySidebarItem`.
10. **Sunset / Aurora** — gradient-based theme where each gallery is a position along a single multi-stop gradient (this is where the *tone-shift algorithm* lives — see below).

## Tone-Shift Algorithm

For gradient-based themes (Mono Fade, Sunset, Aurora, Cool/Warm Range), color is **derived from N**, not picked from a fixed list:

```
color(i) = interpolate(stops, t = i / max(N-1, 1))
```

- `N` = number of galleries the user has.
- `i` = this gallery's `displayOrder`.
- `stops` = the theme's gradient stops (e.g. white → gray → black for Mono Fade).
- `interpolate` does HSL or OKLCH lerp between the two nearest stops.

This means a 2-gallery setup and a 10-gallery setup *both* span the full gradient — each gallery gets a distinct shade rather than the first two looking identical.

For discrete themes (Neon, Pastel, Metallic, Jewel, Earth) we keep index-based lookup with a wrap-around.

## Data Model Sketch

```swift
struct GalleryTheme: Identifiable, Hashable {
    let id: String              // "neon", "pastel", "mono-fade", ...
    let name: String
    let kind: Kind
    enum Kind {
        case discrete(hexes: [String])               // index lookup
        case gradient(stops: [String])               // tone-shift lerp
        case material(tint: String, opacities: [Double]) // liquid glass
    }
    func color(for index: Int, of total: Int) -> Color
}
```

`Gallery.color` becomes a function of *(active theme, displayOrder, total gallery count)* instead of a stored hex. Stored `colorHex` becomes a per-gallery **override** ("I want THIS one to be red regardless of theme").

## Open Questions

- Do themes apply globally, or per-gallery-set?
- How does theme switching feel during the swipe interaction (`GallerySidebarItem` opacity math)?
- Should Liquid Glass be a *modifier* on top of any theme rather than its own theme?
- Do we need light/dark variants for every theme like `neonHexesLight` / `neonHexesDark`?

## Next Steps

1. Spike `GalleryTheme` enum + `color(for:of:)` for one discrete and one gradient theme.
2. Move the existing neon palette behind the new abstraction without changing visuals.
3. Add a theme picker in Settings.
4. Decide on per-gallery override UX.

## Related

- [[Projects/Culla/Culla|Culla]]
- `culla/Views/GallerySidebarView.swift`
- `culla/Models/Gallery.swift`
