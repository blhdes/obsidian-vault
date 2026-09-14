---
title: village-swift (VILLE)
date: 2026-09-14
tags: [project, ios, swift, swiftui, swiftdata, ville, village, letterboxd, paused]
---

# 🎬 village-swift — VILLE

> Vault project name is **`village-swift`**, matching the real GitHub repo
> (**`blhdes/village`**) with a `-swift` suffix that flags what it actually is:
> the native Swift/SwiftUI remodel of the **village-du-cinema** family (Expo app +
> web). The app itself is still called **VILLE** in code (product name, bundle,
> Xcode project) — only the vault/folder naming changed, 2026-09-14.

> ⏸️ **Paused.** Scaffolded (app skeleton + Feed/Models/Services/ViewModels/Views)
> but not actively worked on right now. Kept as its own project because it's
> **architecturally independent** from the rest of the Ville du Cinéma family —
> see "Not the same project as" below.

A brand-new, minimal, **100% offline-first iOS app** — a beautiful Letterboxd RSS
client focused exclusively on **discovering cinema through reviews**. Source code
lives at `/Users/agomezu/Claude/village/VILLE/`.

## What it does (vision)

- A phone-first, calm, cinematic **reading** app — no social layer, no auth, no server.
- Add Letterboxd usernames (no login — public RSS only).
- Feed = merged, reverse-chronological review cards from all followed users.
- Tap a card → immersive reader.
- Everything cached via **SwiftData** → works offline after the first fetch.

## Not the same project as…

VILLE is a **radical simplification / refactor** of [[../Ville-Expo/Ville-Expo|Ville Expo]]
(the React Native + Expo "Ville du Cinéma Mobile" app, source at
`../ville-du-cinema-mobile/`, reference branch `feature/tos-compliant-rebuild`). It
strips out everything except the reading experience: no auth (Supabase), no social
features (takes, comments, follows-via-Supabase), no web layer, **no React Native /
Expo / JS at all**. That's the whole point of keeping it a separate project note —
it doesn't share a codebase, a language, or a dependency graph with
[[../Ville-Expo/Ville-Expo|Ville Expo]] or
[[../ville-du-cinema-web/ville-du-cinema-web|Ville du Cinéma (web)]] — only the
subject matter (Letterboxd reviews) and some porting reference.

## Architecture decisions

| Area | Choice | Reason |
|---|---|---|
| UI | **SwiftUI only** (iOS 18+) | Latest design system (Liquid Glass), no UIKit bridges |
| State | **`@Observable`** (Observation framework) | Modern, value-type friendly, replaces ObservableObject |
| Persistence | **SwiftData** as single source of truth | First-class SwiftUI integration, offline-first by design |
| Networking | `URLSession` + `XMLParser` (Foundation) | Zero third-party deps |
| Concurrency | `async/await` everywhere | No Combine, no callbacks |
| Design | **Liquid Glass**, dark-only | Cinematic, premium feel |
| Target | iOS 18+, iPhone 13 and newer | Allows full use of Liquid Glass + Observation |
| Deps | **None** (outside Apple SDKs) | Keep it minimal, future-proof |

Data flow: `RSSService` → `FeedViewModel` → SwiftData `Review` objects → `@Query` in
`FeedView`. The view always reads from SwiftData (never directly from `RSSService`),
so the UI is identical online and offline.

## Folder structure

```
VILLE/
├── VILLEApp.swift              ← @main App entry, ModelContainer, dark-mode enforcement
├── Models/Review.swift         ← SwiftData @Model — mirrors Review type from the RN project
├── Services/RSSService.swift   ← Async Letterboxd RSS fetch + XML parsing
├── ViewModels/FeedViewModel.swift  ← @Observable, orchestrates refresh + cache
└── Views/
    ├── FeedView.swift          ← Main screen, TabView-ready
    ├── ReviewCard.swift        ← Liquid Glass cinematic card
    └── ReviewDetailView.swift  ← Immersive full-screen reader
```

## Next steps (backlog)

Rough ideas from the original planning note — not committed, not ordered:

- [x] Create the Xcode project and verify the scaffold compiles
- [ ] Build a followed-users management UI (add/remove Letterboxd usernames)
- [ ] Replace the basic HTML renderer in `ReviewDetailView` with a proper rich-text view (blockquotes, images, bold)
- [ ] Word-level text selection in the reader (like the original `ReviewReaderScreen`)
- [ ] Persist followed usernames in SwiftData (currently hard-coded seed values)
- [ ] Custom fonts for the cinematic typography
- [ ] Multi-tab layout: Feed / Saved / Profile
- [ ] Widget / Live Activities (far future)

## Quick links

- Repo: `/Users/agomezu/Claude/village/` · GitHub: **`blhdes/village`** (private, initialized 2026-09-14)
- Full build/style rules: `/Users/agomezu/Claude/village/CLAUDE.md`

## Status

**Paused at scaffold stage** (2026-09-14). The Xcode project and all five source
files exist (App entry, Model, Service, ViewModel, 3 Views), but git wasn't even
initialized until today — no commits beyond the initial one, no Ideas/Dev-Insights/
Phases subfolders yet since there's no iteration history to log. Pick this up by
reading `/Users/agomezu/Claude/village/CLAUDE.md` first — it holds the full vision,
architecture decisions, and porting-reference table for pulling logic out of
[[../Ville-Expo/Ville-Expo|Ville Expo]].

> This note absorbed and replaces `Projects/Ville-Native-App/` (2026-09-14) — an
> earlier planning-stage note for this exact same app, written 2026-04-25 before
> any code existed. Archived rather than kept as a duplicate.

Related: [[../Ville-Expo/Ville-Expo|Ville Expo]] · [[../ville-du-cinema-web/ville-du-cinema-web|Ville du Cinéma (web)]]
