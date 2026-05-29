---
title: warket Native — MVP Implementation Plan
date: 2026-05-29
tags: [warket, swift, swiftui, ios, plan]
---

# warket Native — MVP Implementation Plan

**Self-contained handoff doc.** A fresh Claude Code session should be able to execute from this note alone. Source web app lives at `/Users/agomezu/Claude/asset.cafe`; read specific files where pointed. Parent: [[Projects/warket-native/warket-native|project index]] · backlog: [[Projects/warket-native/deferred-backlog]].

## Goal

Convert **warket** (React+TS web app wrapped in Capacitor) into a **full native iOS app in Swift/SwiftUI**, in a new folder `warket-ios/` inside the existing repo. Web app + Capacitor `ios/`/`android/` folders stay untouched. Native app uses the **same Supabase project**, so existing vaults open unchanged.

## Locked decisions

- **Design:** keep brand (deep-teal accent, dark-first, Instrument Serif display) + **native iOS UX** (NavigationStack, sheets, real Lists).
- **Scope:** core-first MVP = unlock → lists → assets (view/add/edit: summary, markdown description, tags, resources, image) + drag-reorder **+ search/tag filtering** (confirmed in MVP).
- **Target:** iOS 17+.
- **Backend:** reuse existing Supabase via `supabase-swift` SPM package (global `x-vault-hash` header).
- **Deferred** (separate note): shared read-only vaults, share-key generation, JSON export/import, light theme + toggle, resource title auto-fetch, MarketPulse animation.

## ⚠️ Critical constraint — hash parity

Existing vaults only open if the Swift hash matches the JS hash **byte-for-byte**.

Algorithm (from `src/features/auth/seedPhrase.ts`):
1. Normalize: `lowercased` → `trim` → collapse all whitespace runs to a single space (`\s+` → `" "`).
2. UTF-8 encode the normalized string.
3. SHA-256.
4. Lowercase hex string.

`deriveShareHash(vaultHash)` = SHA-256 of `vaultHash + ":share"`, lowercase hex.

**Reference test vectors (verify in Swift first thing):**
```
raw input:  "  Legal  Winner THANK year wave sausage worth useful legal winner thank yellow  "
normalized: "legal winner thank year wave sausage worth useful legal winner thank yellow"
vault_hash: ecb0e7ba498c5920991f0b3483e91f7abafa9ecc6bd82a9a51494589592b1a8f
share_hash: 4aedbd98322b258ec221d52e62bed851cd76131c7e9452e125eaeecd169c8e7f
```
A `hashSeedPhrase` also throws if the normalized word count != 12.

## Backend reference

**Supabase auth trick:** every request carries header `x-vault-hash: <hash>`. RLS policies call `requesting_vault_hash()` (reads that header) and filter rows. So: create the Supabase client with that header set globally, per vault. (`supabase-swift` supports `SupabaseClientOptions(global: .init(headers: [...]))`.) URL + anon key from existing `.env` (`VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`). Anon key is safe to ship (RLS protects data) but keep out of git.

**Tables** (`supabase/schema.sql`):
- `lists`: `id` uuid pk · `vault_hash` text · `name` text · `tags` text[] · `position` int · `created_at` · `updated_at`
- `assets`: `id` uuid pk · `list_id` uuid fk→lists (cascade delete) · `name` text · `ticker` text · `summary` text (≤250) · `description` text · `tags` text[] · `resources` jsonb · `image_url` text? · `position` int · `created_at`
- `vault_shares`: `vault_hash` pk · `share_hash` unique · `created_at` (only needed for deferred sharing)

**`Resource` jsonb shape:** `{ title: String, url: String, favicon: String }`

**Operations to implement** (mirror `src/lib/queries.ts` + inline calls):
- Lists for vault: `lists` select `*, assets(count)` where `vault_hash` eq, order `position` asc → map `asset_count`.
- Asset search index: `assets` select `list_id,name,ticker` where `list_id` in [...] (powers list-level search).
- Assets for list: `assets` select `*` where `list_id` eq, order `position` asc.
- Create list: insert `{vault_hash, name, tags, position}`.
- Update list: update `{name, tags}` where `id` eq.
- Delete list: delete where `id` eq (cascades assets).
- Add asset: insert `{list_id, name, ticker, summary, tags, resources}` → return row.
- Update asset: update any of `{summary|description|tags|resources|image_url}` where `id` eq.
- Delete asset: delete where `id` eq.
- Reorder (`src/lib/position.ts`): for each `{id, position}` update `position` where `id` eq (parallel).

**Favicon URL:** `https://www.google.com/s2/favicons?domain=<host>&sz=32`.

## Design tokens (dark; from `src/index.css`)

```
accent          #2a9d8f   accent-hover  #228377
surface-0       #08090d   surface-1     #0e1018
surface-2       #161922   surface-3     #1e212d
border-default  #262a38   border-hover  #353a4d   border-active #464b62
text-primary    #f0f0f2   text-secondary #a0a3b1
text-tertiary   #636678   text-muted    #464959
success         #34d399   error         #f87171
radii: sm 2 · md 6 · lg 8 · pill 9999
fonts: display "Instrument Serif" · body "General Sans" (fallback system) · mono "JetBrains Mono"
```
(Light palette in `index.css` `[data-theme="light"]` — deferred.)

## Proposed Xcode project structure

```
warket-ios/
  warket.xcodeproj
  warket/
    warketApp.swift
    Config/   Secrets.xcconfig (gitignored), Info.plist (font registration)
    Theme/    Theme.swift (colors/radii), Fonts.swift (+ font files)
    Models/   Asset.swift, VaultList.swift, Resource.swift (Codable, snake_case CodingKeys)
    Core/     SeedPhrase.swift, Wordlist.swift, VaultClient.swift,
              VaultRepository.swift, Session.swift, Haptics.swift
    Features/ Unlock/UnlockView.swift
              Lists/{ListsView,ListCard,ListEditorSheet}.swift
              Assets/{AssetsView,AssetRow,AssetDetailView,AddAssetSheet,
                      ResourceRow,AddResourceSheet,ImageURLSheet,DescriptionView}.swift
    Components/ {TagPill,SearchField,EmptyStateView}.swift
  warketTests/ HashParityTests.swift
```

## Milestones (execution order)

### M0 — Scaffold + foundation ✅
- [x] Create `warket-ios/` Xcode project (SwiftUI app lifecycle, iOS 17 deployment target, bundle id e.g. `com.blhdes.warket`). *(via XcodeGen — `project.yml` generates `warket.xcodeproj`)*
- [x] Add `supabase-swift` via SPM.
- [x] `Secrets.xcconfig` (gitignored) with Supabase URL + anon key (copy from `.env`); add to `.gitignore`.
- [x] `Theme.swift` — Color + radius constants from tokens above (dark only for MVP).
- [x] `Models/` — `Resource`, `VaultList`, `Asset` Codable structs matching DB columns.
- [x] `SeedPhrase.swift` — `hashSeedPhrase`, `deriveShareHash` (CryptoKit). Optionally port the 534-word wordlist from `src/features/auth/wordlist.ts` for Generate. *(536 words auto-ported)*

### M1 — Hash-parity checkpoint (do before any UI) ✅
- [x] `HashParityTests.swift` asserting the reference vectors above. **Must pass** before proceeding. *(5/5 tests pass; vault + share hashes match byte-for-byte)*

### M2 — Data layer + unlock + lists load ✅
- [x] `VaultClient.swift` — Supabase client factory with global `x-vault-hash` header.
- [x] `VaultRepository.swift` — list/asset operations above.
- [x] `Session.swift` — remember-me (AppStorage; Keychain optional).
- [x] `UnlockView.swift` — phrase entry + Generate + "keep session open" + Access → hash → route to vault.
- [x] App nav: `NavigationStack`; root = Unlock, success → ListsView. Auto-resume if remembered. *(`RootView` auth gate)*
- [x] `ListsView.swift` — grid of `ListCard`s with asset counts loaded from Supabase. **Read path verified against real data.**

### M3 — Assets browse + detail ✅
- [x] `AssetsView.swift` — list of `AssetRow`s for a tapped list.
- [x] `AssetDetailView.swift` — summary, markdown description (render via `AttributedString(markdown:)`), tags, resources (open links, favicons), image. *(block-level markdown needed a custom `MarkdownText` renderer — `AttributedString` alone only does inline)*

### M4 — Full CRUD + reorder + search ✅
- [x] Create/edit/delete lists (`ListEditorSheet`) and assets (`AssetEditorSheet`, inline edits).
- [x] Resources: add (`AddResourceSheet`), remove, reorder; image via inline field in the asset editor *(not a separate `ImageURLSheet`)*.
- [x] Drag-reorder lists/assets/resources with `.onMove` → persist positions.
- [x] Search + tag-pill filtering on both lists and assets screens.
- [x] Haptics via `UIImpactFeedbackGenerator` (light on reorder, etc.).

> **M4 notes:** Lists screen is a native `List` (primary) with the 2-column grid kept as a persisted `@AppStorage` layout toggle (user choice). Notes editor uses a Write/Preview toggle (plain markdown field + live `MarkdownText` preview) rather than a formatting toolbar.

### M5 — Polish ✅
- [x] Loading/empty states, simple toast/banner, safe-area + status-bar styling, font embedding. *(toast banners replace modal alerts; Instrument Serif + JetBrains Mono embedded & verified via test; body stays system SF — General Sans not embedded)*
- [ ] Then pull from [[Projects/warket-native/deferred-backlog]].

---

**MVP status (2026-05-29):** M0–M5 complete. Core flow done: unlock → lists → assets → full CRUD → reorder → search/tag filtering, on embedded brand fonts. Builds clean; 6/6 tests pass. Next: deferred backlog.

## Kickoff after /clear

Point the fresh session here:
> Read `Projects/warket-native/mvp-implementation-plan.md` and start M0 for the warket native iOS port.
