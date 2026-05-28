---
title: warket Native — Deferred Backlog
date: 2026-05-28
tags: [warket, swift, swiftui, ios, backlog]
---

# warket Native — Deferred Backlog

Everything intentionally left **out of the core-first MVP** ([[Projects/warket-native/warket-native|project index]]). Build these in later passes once the MVP (unlock → lists → assets + reorder) works end-to-end.

## Sharing
- **Read-only shared vault view** — native equivalent of `SharedVaultPage.tsx`: resolve a share key → load that vault read-only (no edit/add/delete UI).
- **Share-key generation** — `deriveShareHash(vault_hash)` (SHA-256 of `vault_hash + ":share"`), upsert into `vault_shares`, copy key to clipboard.

## Data portability
- **JSON export** — port `vaultExport.exportVault`: dump lists + assets to a JSON file, share via iOS share sheet. Match the existing format (`version`, `app: "warket"`, `exported_at`, `lists[]`).
- **JSON import** — port `vaultExport.importVault`, including **same-name list merge** (lists matched case-insensitively by name; assets appended after current max position) and `validateImportData` checks.

## Theming
- **Light theme + toggle** — MVP can ship dark-only. Later: full light palette (tokens already captured from `index.css`) and a toggle, persisting choice. Native: drive via SwiftUI `colorScheme` / app storage.

## Resource enrichment
- **Auto-fetch page title** — when adding a resource URL, fetch the page and extract `og:title` / `<title>`. Native is *simpler* than web (no CORS) — a single `URLSession` request + HTML parse replaces the web app's 6-proxy race in `fetchTitle.ts`.

## Browsing niceties (confirm if wanted in MVP)
- **Search + tag filtering** — search lists/assets/tickers; filter by tag pills. Central to the web UX; decide whether it belongs in MVP or here.

## Visual flourish (low priority / maybe drop)
- **Landing MarketPulse animation** — the animated canvas background on the web landing page (`MarketPulse.tsx`). Native equivalent would be a SwiftUI Canvas/TimelineView; likely skip or replace with something simpler.

## Other web-only bits to revisit
- "Keep session open" / remember-me persistence (decide MVP vs later; native uses Keychain/AppStorage).
- Markdown rendering for descriptions (`marked` → `AttributedString` or a markdown lib) — needed wherever descriptions are *viewed*, so partly MVP.
- Favicon display for resources (Google favicon service URL, same as web).
