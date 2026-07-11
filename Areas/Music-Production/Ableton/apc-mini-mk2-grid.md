---
title: APC Mini MK2 Grid
date: 2026-07-09
tags: [ableton, apc-mini-mk2, controller, session-view, hardware]
---

# APC Mini MK2 → Session View

The APC Mini MK2 is a **1:1 physical mirror of Session View**. Nothing new to learn musically — every pad press does something you already do with the mouse.

## Setup check

Plug in via USB. Live should auto-detect it (pads light up with your clip colors). If not: **Settings → Link/Tempo/MIDI** → set a **Control Surface** slot to `APC mini mk2`, with Input and Output both `APC mini mk2`.

## The mapping

```
                 8 tracks (columns)
        ┌───────────────────────────┐
        │  ● ● ● ● ● ● ● ●          │ ▶  ← scene launch
   8    │  ● ● ● ● ● ● ● ●          │ ▶     (right column,
 scenes │  ● ● ● ● ● ● ● ●   ...    │ ▶      = the row-launch
 (rows) │  ● ● ● ● ● ● ● ●          │ ▶      buttons in Live)
        └───────────────────────────┘
           [track buttons — bottom row]
           ▮ ▮ ▮ ▮ ▮ ▮ ▮ ▮  + ▮      ← 9 faders
                                        (8 tracks + Master)
```

| Hardware | Session View equivalent |
|---|---|
| **8×8 pad grid** | The clip grid. One pad = one clip slot. Press = launch that clip |
| **Right column (8 buttons)** | Scene launch — fires the whole row |
| **Faders 1–8** | Track volume faders |
| **Fader 9** | Master volume |
| **Bottom row buttons** | Track functions (stop clips; `Shift` unlocks mute/solo/arm modes — later) |

## Pad colors

- **Clip color** = a clip lives there, stopped.
- **Pulsing green** = playing.
- **Unlit** = empty slot.

## Worth knowing

- A **red frame** appears in Session View on screen — that's the 8×8 window the hardware is currently "looking at".
- **Launch Quantization still rules.** Pads obey the same `1 Bar` quantization as mouse clicks — press a pad mid-bar and the clip waits for the next bar. Sloppy timing stays musical for free.
- Live Lite caps projects at **8 tracks**, so the grid covers the entire project — no scrolling needed.
