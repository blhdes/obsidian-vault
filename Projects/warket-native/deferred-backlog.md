---
title: warket Native — Deferred Backlog
date: 2026-05-28
tags: [warket, swift, swiftui, ios, backlog]
---

# warket Native — Deferred Backlog

Everything intentionally left **out of the core-first MVP** ([[Projects/warket-native/warket-native|project index]]). Build these in later passes once the MVP (unlock → lists → assets + reorder) works end-to-end.

> **2026-09-14 audit note:** nearly everything below has since shipped. Cross-checked against `git log` in `/Users/agomezu/Claude/asset.cafe` and the `warket-ios/` source. See [[Projects/warket-native/Phases/web-parity-pass|Phase 2 — Web Parity Pass]] for what landed and when. Left this file in place (not deleted) as the historical record of what was scoped out of the MVP and why.

## Sharing — ✅ done (Phase 2)
- **Read-only shared vault view** — native equivalent of `SharedVaultPage.tsx`: resolve a share key → load that vault read-only (no edit/add/delete UI). *Shipped: `Core/ShareResolver.swift` + `Session.readOnly` gating.*
- **Share-key generation** — `deriveShareHash(vault_hash)` (SHA-256 of `vault_hash + ":share"`), upsert into `vault_shares`, copy key to clipboard. *Shipped: `ListsView` "Share (read-only)" action.*

## Data portability — ✅ done (Phase 2)
- **JSON export** — port `vaultExport.exportVault`: dump lists + assets to a JSON file, share via iOS share sheet. Match the existing format (`version`, `app: "warket"`, `exported_at`, `lists[]`). *Shipped: `Core/VaultTransfer.swift` + `.fileExporter`.*
- **JSON import** — port `vaultExport.importVault`, including **same-name list merge** (lists matched case-insensitively by name; assets appended after current max position) and `validateImportData` checks. *Shipped: `VaultRepository.importVault` + `.fileImporter`.*

## Theming — ⚠️ done differently (Phase 2)
- **Light theme + toggle** — MVP can ship dark-only. Later: full light palette (tokens already captured from `index.css`) and a toggle, persisting choice. Native: drive via SwiftUI `colorScheme` / app storage. *Shipped as **system-adaptive only** (`Theme.swift` → `Color.adaptive(dark:light:)`, follows `UITraitCollection.userInterfaceStyle`) — no explicit in-app toggle like the web app's. If a manual override is ever wanted, that part is still open.*

## Resource enrichment — ✅ done (Phase 2)
- **Auto-fetch page title** — when adding a resource URL, fetch the page and extract `og:title` / `<title>`. Native is *simpler* than web (no CORS) — a single `URLSession` request + HTML parse replaces the web app's 6-proxy race in `fetchTitle.ts`. *Shipped: `Core/TitleFetcher.swift` (with `api.microlink.io` fallback), single-flight guard added same week.*

## Browsing niceties — ✅ done (shipped in the MVP itself, not deferred after all)
- **Search + tag filtering** — search lists/assets/tickers; filter by tag pills. Central to the web UX. Ended up going into MVP milestone M4 rather than staying deferred — see [[Projects/warket-native/mvp-implementation-plan|MVP plan]].

## Visual flourish — ✅ retired (Phase 1)
- **Landing MarketPulse animation** — the animated canvas background on the web landing page (`MarketPulse.tsx`). Native equivalent would be a SwiftUI Canvas/TimelineView; likely skip or replace with something simpler. *Retired: replaced by the `MarketPulseBackground` `MeshGradient` in [[Projects/warket-native/Phases/liquid-glass-redesign|Phase 1 — Liquid Glass Redesign]].*

## Other web-only bits to revisit — ✅ all done (MVP)
- "Keep session open" / remember-me persistence (decide MVP vs later; native uses Keychain/AppStorage). *Shipped in MVP: `Core/Session.swift`.*
- Markdown rendering for descriptions (`marked` → `AttributedString` or a markdown lib) — needed wherever descriptions are *viewed*, so partly MVP. *Shipped in MVP: custom `MarkdownText` block renderer.*
- Favicon display for resources (Google favicon service URL, same as web). *Shipped in MVP (M3).*

## What's actually still open
Nothing on this list remains unstarted except the manual light/dark **toggle** (theming currently follows system only). No further backlog items are outstanding as of 2026-09-14.
