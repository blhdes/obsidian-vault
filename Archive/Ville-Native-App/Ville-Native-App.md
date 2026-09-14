---
title: Ville Native App
date: 2026-04-25
tags: [ville, ios, swiftui, letterboxd, project-index]
---

# Ville Native App

> ⚠️ **Early stage — brainstorming & scaffolding phase.**
> This project has just been started. The files below are the initial skeleton. Nothing has been run in Xcode yet, and most decisions are still reversible. Treat everything here as a working hypothesis, not a final plan.

---

## What is VILLE?

A minimal, 100% offline-first iOS app that lets you read Letterboxd reviews from people you follow — beautifully, calmly, without any social layer, login, or server.

Think of it as a **cinematic reading app**. You add Letterboxd usernames; VILLE fetches their public RSS feeds, caches everything locally, and presents reviews as large, immersive cards. No account, no algorithm.

---

## Why build this?

The existing [[../../Projects/ville-du-cinema-web/|Ville du Cinéma]] app had grown into a full social platform (auth, takes, comments, Supabase backend). VILLE strips all of that out and focuses on the single thing that made it special: *discovering cinema through other people's writing*.

---

## Core features (initial scope)

- Add Letterboxd usernames to follow (no login needed — uses public RSS)
- Merged, reverse-chronological feed of review cards
- Tap a card → immersive full-screen reader
- Everything cached via SwiftData → works offline after first fetch
- Liquid Glass aesthetic: dark, cinematic, high-contrast

---

## File structure

```
village/
├── CLAUDE.md                         ← AI context + architecture notes
└── VILLE/
    ├── VILLEApp.swift                ← @main entry point + SwiftData container
    ├── Models/
    │   └── Review.swift              ← SwiftData model (id, movieTitle, rating, reviewHTML…)
    ├── Services/
    │   └── RSSService.swift          ← Async URLSession + XMLParser, zero deps
    ├── ViewModels/
    │   └── FeedViewModel.swift       ← @Observable, upserts reviews into SwiftData
    └── Views/
        ├── FeedView.swift            ← Main screen + pull-to-refresh
        ├── ReviewCard.swift          ← Liquid Glass card (movie title, rating, excerpt)
        └── ReviewDetailView.swift    ← Full-screen immersive reader
```

> The Xcode project file (`.xcodeproj`) has **not been created yet** — that's the immediate next manual step.

---

## Tech stack

| Area | Choice |
|---|---|
| UI | SwiftUI only, iOS 18+ |
| State | `@Observable` (Observation framework) |
| Persistence | SwiftData (offline-first, single source of truth) |
| Networking | URLSession + XMLParser (no third-party deps) |
| Design | Liquid Glass, dark mode only |

---

## Next steps

These are rough ideas — **not committed, not ordered**:

- [x] Create the Xcode project and verify the scaffold compiles
- [ ] Build a followed-users management UI (add/remove Letterboxd usernames)
- [ ] Replace the basic HTML renderer in `ReviewDetailView` with a proper rich-text view (blockquotes, images, bold)
- [ ] Word-level text selection in the reader (like the original `ReviewReaderScreen`)
- [ ] Persist followed usernames in SwiftData (currently hard-coded seed values)
- [ ] Custom fonts for the cinematic typography
- [ ] Multi-tab layout: Feed / Saved / Profile
- [ ] Widget / Live Activities (far future)

---

## Source reference

The logic (RSS parsing, HTML sanitisation, rating extraction) is ported from the existing React Native app:

- **Local path**: `../ville-du-cinema-mobile/` (branch `feature/tos-compliant-rebuild`)
- Key files: `services/feed.ts`, `types/database.ts`, `components/ReviewCard.tsx`, `screens/ReviewReaderScreen.tsx`
