---
topic: Producer Pal
type: tool
updated: 2026-09-26
related: [[INDEX]]
---

# Producer Pal

## Summary
An MCP server running inside Live as a Max for Live device (`Producer_Pal.amxd`). It gives Claude Code read/write control of the Live Set. Registered with:
`claude mcp add producer-pal -- npx producer-pal@latest --live-api`

## Core — connection
| Step | Detail | Source |
|---|---|---|
| Start | `ppal-connect` first. It also returns Producer Pal's own guidance, which should be followed | [ext] |
| Tools missing in `/mcp` | Ableton open + device shows "Producer Pal Running" → restart Claude Code (`claude --continue`) | [live] |
| Config changes | MCP servers load only at session start. Restart after any `claude mcp add` | [live] |

## Core — tool hierarchy
1. Specialized `ppal-*` tools first. They're tuned for reliability. [ext]
2. `ppal-live-api` (Live Object Model) only when no specialized tool reaches the target. Read → write one property → read back. Prefer IDs. Never use it for bulk deletes. [ext]

## Core — addressing
| Target | Path | Source |
|---|---|---|
| Device | `t[track]/d[device]` | [live] |
| Drum Rack pad | `t[track]/d[rack]/p[Note][Octave]` (e.g. `pC1`, `pEb1`) | [live] |
| Device in pad chain | `t4/d0/pEb1/c0/d1` | [live] |

Track indices shift when tracks are inserted. Re-read the set and prefer IDs. [live]

## Gotchas
- **Operator:** `"A Fix On "` / `"B Fix On "` have trailing spaces → use parameter IDs. [live]
- **Operator:** `Ae Sustain` is in dB (`-70` ≈ silence). `Algorithm` needs the full label (`"Alg. 1"`). [live]
- **Toggles** (Operator, Drift, Compressor…) take `"On"` / `"Off"` strings. [live]
- **Drum Rack:** load samples with `ppal-update-device` after the rack exists, one pad at a time, then verify with `ppal-read-device`. [live]
- **Library search:** tag filters often return empty. Use the query only, with `type: 'oneshot'`. Needs Live 12.4+. [live]
- **Sends:** writable since Producer Pal 2.3.0: `ppal-update-track` with `sendReturn` (letter, name or id) + `sendGainDb`, or `sends: [{return, gainDb}]`. The response returns the value read back. Tested on Live 12.4.6: −70 → −30 → −70 dB on an empty track. [live] 2026-09-26
- **Pseudo-params:** Drift's mod-matrix sources (`filterMod1Source`, `pitchMod1Source`…), `voiceMode`, Compressor `sidechainSourceTrackId`, EQ Eight `globalMode`, etc. are set as params. `read-device include:["options"]` lists valid values. [live]
- **Sidechain to a pad:** `"Drum Rack | [Pad Sample Name] | Post Mixer"`. [live]
- **Clip notation:** bare durations (`8bar`, `n/16`). Mixing formats breaks parsing. [live]

## Safe workflow
```
ppal-connect → read set (IDs, tempo, scale) → ppal-read-device → write ≤3 → read back → Ale listens
```

## Sources
- https://producer-pal.org/installation/claude-code
- https://producer-pal.org/features/tools
