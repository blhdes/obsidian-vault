---
title: "Phase 2 — Web Parity Pass"
date: 2026-06-19
tags: [warket, swift, swiftui, ios, phase]
---

# Phase 2 — Web Parity Pass

Second post-MVP phase, landed the day after [[Projects/warket-native/Phases/liquid-glass-redesign|Phase 1 — Liquid Glass Redesign]]. Closes out nearly all of the [[Projects/warket-native/deferred-backlog|deferred backlog]]: sharing, JSON export/import, adaptive theming, and resource title auto-fetch.

> Not captured in the vault until this audit (2026-09-14) — this note was reconstructed from `git log` and the `warket-ios/` source, not written at the time.

> Status: **shipped & merged to `main`** — commits `443b37a` → `22e08e5` → `08e10eb`, merged via `cce2151` (all 2026-06-19).

## What shipped

- **Read-only sharing** — `Core/ShareResolver.swift` resolves a share key back to a vault hash (mirrors the web app's `resolveShareKey`). `ListsView` gains a "Share (read-only)" action that upserts a share key via `VaultRepository` and copies it to the clipboard. `UnlockView` gains an "Open a shared vault" entry sheet. `Session.readOnly` threads through the views to gate edit/add/delete UI.
- **JSON export/import** — `Core/VaultTransfer.swift` defines a `VaultExport` format byte-compatible with the web app's `vaultExport.ts` (`version`, `app`, `exported_at`, `lists[]`), with matching validation messages. `ListsView` wires it to SwiftUI's `.fileExporter`/`.fileImporter`. `VaultRepository.importVault` does the same-name list merge the backlog called for.
- **System-adaptive theme** — `Theme/Theme.swift` tokens became `Color.adaptive(dark:light:)`, resolving off `UITraitCollection.userInterfaceStyle`. This retires the "light theme" backlog item, but **not** with an explicit in-app toggle the way the web app has one (`ThemeContext.tsx` + a UI switch) — it only follows the system setting.
- **Resource title auto-fetch** — `Core/TitleFetcher.swift`: a direct `URLSession` fetch of the page (native has no CORS restriction, unlike the web app's 6-proxy race in `fetchTitle.ts`), with `api.microlink.io` as a fallback for JS-rendered pages. Wired into `AddResourceSheet`, with a single-flight/cancel-on-supersede guard added in the immediate follow-up refactor commit (`22e08e5`).
- **Glass-over-mesh follow-up** (`08e10eb`) — pulled the newly-added surfaces (`AssetDetailView`, `AddResourceSheet`, the share-entry sheet) into the Liquid-Glass-over-mesh visual language from Phase 1, so they don't revert to flat/stock chrome.

## Backlog items this closes

From [[Projects/warket-native/deferred-backlog|deferred backlog]]: **Sharing** (both items), **Data portability** (both items), **Resource enrichment** (auto-fetch title). **Theming** is closed differently than scoped — system-adaptive, no manual toggle. See that note for per-item status marks.

## Not verified in this audit

- No on-device confirmation of pixel-level glass alignment on the new surfaces (same open item as Phase 1).
- Whether the light-mode hex values match the web app's `[data-theme="light"]` tokens exactly wasn't diffed line-by-line — code review only confirmed the `Color.adaptive` mechanism is wired up correctly.

---
Project index: [[Projects/warket-native/warket-native|warket — Native Port]] · Previous: [[Projects/warket-native/Phases/liquid-glass-redesign|Phase 1 — Liquid Glass Redesign]]
