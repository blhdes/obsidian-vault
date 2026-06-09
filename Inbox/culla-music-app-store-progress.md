---
title: Culla Music — App Store submission progress
date: 2026-06-06
tags: [culla-music, app-store, shipping, progress]
---

# Culla Music — App Store submission progress

Where we are in getting **Culla Music** onto the App Store. Picking this up tomorrow.
(Filed in Inbox — move to `Projects/Culla-Music/Phases/` if you want it with the rest.)

## ✅ Done (code side is basically finished)

- **Privacy manifest** — added `CullaMusic/CullaMusic/PrivacyInfo.xcprivacy`. Declares: no tracking, no data collected, one required-reason API (`UserDefaults` via `@AppStorage`, reason `CA92.1`). Validated.
- **Privacy policy URL** — already live at `culla.app/music`. It matches the manifest (no data collected). *Tip: if the site has an anchor that jumps straight to the privacy section, paste that exact URL into App Store Connect.*
- **Bundle ID renamed** — `agu.CullaMusic2` → **`app.culla.music`** (both Debug + Release). No code referenced the old ID.
  - New App ID was **created manually** in the Developer portal with **MusicKit enabled** — catalog requests verified working on device. Description field = "Culla Music".
  - Distribution cert (team `56BK7T2JG7`) is present, so the submission signing path is fine.
- **iOS floor decided** — keeping **iOS 17**, NOT raising to 26. The pre-iOS-26 (non-glass) fallback was reviewed on-device and looks good.
  - Added a debug switch to preview it: `Helpers/DebugFlags.swift` → flip `previewLegacyUI` to `true`, build, look around, flip back. It's `#if DEBUG`-wrapped, so it can never ship enabled.
- **Launch screen** — already auto-generated (`UILaunchScreen_Generation = YES`). Nothing to do.
- **First-use onboarding (2026-06-09)** — added before shipping so new users aren't dropped into the gesture-heavy swipe screen blind. Three one-time hints, each shown once then never again:
  - **Swipe gesture guide** — full-screen compass on first populated deck (↑ Love · ← Dismiss · → Add to playlist · ↓ Share), on an *opaque* `systemBackground` (not a see-through scrim, so it doesn't blend with the deck) and all-semantic colors (correct in light + dark). Also teaches "drag right → slide up/down to pick the playlist", "double-tap to skip", and "tap a card's ⓘ for artist details". New file `Views/SwipeGuideOverlay.swift`.
  - **Home hero hint** — "Drag to peek · tap to browse covers" capsule, floated as an *overlay* on the hero (not a layout row) so dismissing it fades without reflowing the screen. The fan looked static; its drag/tap gestures were undiscoverable.
  - **Note:** sidebar drop-targets are auto-seeded on first launch and an empty sidebar auto-opens Manage on a right-swipe, so no "make a playlist first" tooltip is needed.
  - Existing **Dismissed long-press tip** folded into a shared `CoachTip` (`Helpers/CoachTip.swift`), which also holds `OnboardingFlags` (one place for all the once-seen keys).
  - **Testing:** the tips only show once. To replay them on device without reinstalling, flip `Helpers/DebugFlags.swift` → `replayOnboardingTips = true`, build, then back to `false`. `#if DEBUG`-wrapped, can't reach Release.

## ⏳ Left to do — all in App Store Connect (mostly web work)

1. **Create the app record** in App Store Connect on bundle ID `app.culla.music`.
2. **Screenshots** — 6.9" iPhone size is required (6.5" optional).
3. **Listing text** — name, subtitle, description, keywords. ✅ **Drafted — see "Paste-ready copy" below.**
4. **Privacy questionnaire** — answer **"Data Not Collected"** so it matches the manifest + policy.
5. **Age rating** + **category** (Music).
6. **Reviewer notes** — must flag: app needs Apple Music authorization, and it still works **without** an Apple Music subscription (30s previews). Prevents a Guideline 2.1 rejection if the reviewer tests on a non-subscriber account. ✅ **Drafted — see "Paste-ready copy" below.**
7. **Archive** (Release) in Xcode → upload → submit (TestFlight first is optional but recommended).

## ▶️ Next action for tomorrow

Have Claude **draft items #3 (listing text + keywords) and #6 (reviewer notes)** so they can be pasted straight in. Then move on to screenshots + the App Store Connect record.

## 📝 Paste-ready copy (drafted 2026-06-09)

> Copy straight into App Store Connect. Field limits noted — App Store Connect enforces them.

### #3 — Listing text

**App Name** — *max 30 chars*
```
Culla Music
```
11 chars. Matches the App ID description. If "Culla Music" is already taken on the store (names must be globally unique), use `Culla Music: Swipe to Sort` (26 chars) instead — it also bakes in search keywords.

**Subtitle** — *max 30 chars*
```
Swipe-sort your music library
```
29 chars. Deliberately avoids the word "Apple" — Apple flags its trademark in names/subtitles.

**Keywords** — *max 100 chars, comma-separated, NO spaces (spaces count!)*
```
swipe,sort,playlist,organize,library,cleanup,declutter,curate,songs,tracks,manage,deck
```
86 chars. No "Apple Music" (Apple's trademark, gets flagged). Room for ~1 more, e.g. `,triage`.

**Promotional Text** — *max 170 chars, editable anytime without re-review*
```
Stop scrolling, start swiping. Culla Music turns sorting your library into one quick decision at a time — swipe right to file a song, left to skip, up to love it.
```
159 chars.

**Description** — *max 4000 chars (this draft ≈ 1,750)*
```
Culla Music turns the chore of organizing your music into something you'll actually finish. It shows you one song at a time and asks a single question: where does this go? Swipe right to file it onto a playlist, swipe left to skip it, swipe up to love it. One decision at a time, until your library is sorted.

THREE WAYS TO SORT
• Library — work through your whole library, minus anything you've already filed.
• Unsorted — focus only on songs that aren't in any of your playlists yet.
• Dismissed — revisit the pile you skipped, and bring songs back whenever you change your mind.

WHAT YOU CAN DO
• Swipe to sort — right files a song onto a playlist, left dismisses it, up sends it to a "Loved" playlist.
• Hear before you decide — each card previews automatically, with a scrubbable progress bar you can drag to jump around.
• Cover carousel — the home screen fans out the next few covers in your deck; tap to open a full-screen carousel and pick exactly where to start.
• Copy or move — point the deck at one playlist and copy songs into others, or move them out as you go.
• Never re-sort a song — small pills show which playlists each song already lives in.
• Audition new music — scope the deck to an Apple-curated or editorial playlist to discover tracks that aren't in your library yet.
• Artist hub — tap a song's info for the artist's top tracks, similar artists, and a short bio.
• Undo anything — every swipe is reversible, including the change made to your Apple Music playlists.
• Make it yours — light/dark themes, accent colors, haptics, auto-play, and more in Settings.

WORKS WITH OR WITHOUT A SUBSCRIPTION
Culla Music works with your existing Apple Music library. With an Apple Music subscription you'll hear full songs; without one you'll hear 30-second previews — and the swipe-and-sort flow works either way.

YOUR DATA STAYS YOURS
Culla Music collects no data and includes no tracking. Your library and your choices never leave your device.
```

### #6 — Reviewer notes

> App Store Connect → your version → **App Review Information → Notes**.
```
Thank you for reviewing Culla Music.

WHAT THE APP DOES
Culla Music is a "swipe to sort" tool for the user's own Apple Music library. You swipe through songs one at a time and file them into playlists: swipe right = add to a playlist, left = dismiss, up = add to a "Loved" playlist.

ACCESS REQUIRED — PLEASE GRANT WHEN PROMPTED
On first launch the app requests Apple Music access (MusicKit authorization). Please tap "Allow" — without it the app has no library to display and the deck will be empty. This is the only permission the app requests. No account creation, sign-in, or demo credentials are needed.

WORKS WITHOUT AN APPLE MUSIC SUBSCRIPTION
The app does NOT require an active Apple Music subscription. If you test on an account without a subscription, playback falls back to Apple's standard 30-second previews and the full swipe / sort / playlist flow still works. Please do not reject under Guideline 2.1 on the basis of "no subscription" — the previews are expected, intended behavior, not a defect.

TESTING TIP
For the fullest experience, please test on an account that already has some songs in its Apple Music library and a few playlists, so there is content to swipe through and file.

PRIVACY
The app collects no data and contains no tracking (see the included privacy manifest; the data-collection answer is "Data Not Collected"). Everything stays on device.
```

## Notes / gotchas to remember
- MusicKit capability is **per-App-ID** — that's why the new bundle ID needed it re-enabled. Don't be surprised if anything else App-ID-scoped needs re-doing.
- Don't touch signing unless catalog requests actually 404 — it works as-is.
