---
title: warket — Native Swift/SwiftUI Port
date: 2026-05-28
tags: [warket, swift, swiftui, ios, project, index]
---

# warket — Native Swift/SwiftUI Port

Project index for converting **warket** (currently a React + TypeScript web app wrapped in Capacitor) into a **full native iOS app in Swift/SwiftUI**, living in a new folder inside the existing repo. The web app and Supabase backend stay as-is; the native app talks to the **same** Supabase project so existing vaults open on both.

Repo: `/Users/agomezu/Claude/asset.cafe`

## What warket is

Privacy-first asset watchlist. No accounts: a 12-word seed phrase is SHA-256 hashed client-side into a 64-char `vault_hash` — that hash is the only identity. Every Supabase request sends it in an `x-vault-hash` header; database RLS filters rows by it. A one-way-derived **share key** gives read-only access.

Data model (3 tables): `lists`, `assets`, `vault_shares`. Types: `Resource`, `VaultList`, `Asset`.

## Decisions locked in (2026-05-28)

- **Design:** Keep brand (deep-teal accent, dark-first, Instrument Serif display feel) but use **native iOS UX** — system navigation, sheets, real lists.
- **Scope:** **Core-first** MVP, then build out the rest (see [[Projects/warket-native/deferred-backlog|deferred backlog]]).
- **Target:** iOS 17+.
- **Backend:** Reuse existing Supabase project via `supabase-swift` SDK (supports global headers for the `x-vault-hash` trick).

## Core-first MVP scope

- Unlock vault: enter / generate 12-word phrase, hash with **CryptoKit** (must match the JS hash byte-for-byte), open vault.
- Browse lists (grid), tap into a list.
- Assets: view / add / edit — name, ticker, summary, markdown description, tags, resource links, custom image.
- Drag-to-reorder (lists, assets, resources) via SwiftUI `.onMove`.
- **Search + tag filtering** (confirmed in MVP) on both lists and assets screens.

Full step-by-step build plan: [[Projects/warket-native/mvp-implementation-plan|MVP implementation plan]] (self-contained handoff doc with hash test vectors, backend reference, design tokens, file structure, milestones M0–M5).

⚠️ **Hash parity is the critical constraint:** normalization = lowercase → trim → collapse whitespace to single spaces → UTF-8 encode → SHA-256 → lowercase hex. Any drift means existing vaults won't open.

## Notes

- [[Projects/warket-native/mvp-implementation-plan|MVP implementation plan]] — detailed step-by-step build plan.
- [[Projects/warket-native/deferred-backlog|Deferred backlog]] — everything beyond the MVP.
- [[Projects/warket-native/Phases/liquid-glass-redesign|Phase 1 — Liquid Glass Redesign]] — first post-MVP design pass.
- Related learning: [[Resources/Swift/swift|Swift]]

## Status

- [x] Audit existing Capacitor/web project
- [x] Lock design / scope / target decisions
- [x] Plan the SwiftUI project structure (see MVP plan)
- [x] Scaffold Xcode project + add supabase-swift (M0)
- [x] Port crypto (CryptoKit) + verify hash parity (M1)
- [x] Build MVP screens (M2–M5)
- [x] Phase 1 — Liquid Glass redesign (merged to `main`, PR #11)
