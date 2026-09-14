# SwiftUI Redesign — Learnings

Append-only log of patterns, anti-patterns, and API quirks discovered while running `/swiftui-redesign`. Read at the start of each invocation as additional rules; append 0–3 new entries at the end. Be concrete or stay quiet — vague entries pollute the file.

Format:

```markdown
## YYYY-MM-DD — Short title

**Tags:** [api] [gating] [convention] [anti-pattern] [layout] [motion]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action.
```

---

## 2026-05-20 — Read target-level deployment target, not project-level

**Tags:** [gating] [anti-pattern]
**Context:** Culla's `.pbxproj` had `IPHONEOS_DEPLOYMENT_TARGET = 26.2` at the project level but `17.0` at the target level. Xcode uses the target value. The user stated "iOS 18" but neither was the actual floor.
**Lesson:** Always `grep -B2 IPHONEOS_DEPLOYMENT_TARGET` the `.pbxproj` and look at the entry surrounded by `INFOPLIST_KEY_*` lines — that's the target-level value. Gate APIs against the *actual* target, not the user-stated one, and flag the mismatch in caveats so the user can bump it later.

## 2026-05-20 — Centralize Liquid Glass gating in one modifier

**Tags:** [convention] [gating]
**Context:** A pre-existing `GlassOrQuaternaryRounded` modifier was used at only one call site. The redesign needed glass at ~8 sites and would have scattered `if #available(iOS 26, *)` blocks if applied inline.
**Lesson:** Add (or reuse) a single `glassSurface(in:tint:interactive:)` + `GlassStack` helper before the redesign starts. Every call site becomes a one-liner and OS gating lives in one file. Delete any narrower predecessor (like `GlassOrQuaternaryRounded`) the same pass — leaving both creates "which do I use here" decisions.

## 2026-05-20 — `resolveSongs(ids:)` is O(library) — don't use it for single IDs

**Tags:** [api] [anti-pattern]
**Context:** Wrote a hero-preview path that called `MusicLibraryService.resolveSongs(ids: [oneID])` to look up one dismissed song's artwork. The implementation pages through the entire library matching IDs against the target set — fine for batches, brutal for one ID.
**Lesson:** For a single-song lookup, use `MusicLibraryRequest<Song>().filter(matching: \.id, equalTo: MusicItemID(id))` — one round-trip, direct fetch. Reserve `resolveSongs` for batches large enough to amortize the page walk (>10 IDs).

## 2026-05-20 — The CTA usually wins by NOT being glass

**Tags:** [convention] [motion]
**Context:** Considered making the "Start Cullaing" button a Liquid Glass capsule. It would have visually blended into the mode tiles and source pill (also glass) sitting above it.
**Lesson:** On a Liquid-Glass-heavy screen, paint the primary CTA as a bold accent-gradient capsule with an accent-shadow halo. Glass surfaces should frame the *path* to the CTA, not be it. Use `.buttonStyle(.plain)` + a hand-built `Capsule().fill(LinearGradient(...))` to opt out of the system's auto-glassy `.borderedProminent`.

## 2026-05-20 — `accessibilityReduceMotion` should freeze, not soften

**Tags:** [motion]
**Context:** Built `LivingMeshBackground` with a `TimelineView(.animation)` that drives a 9-point mesh. With reduce-motion respected, the question was whether to slow the animation or stop it.
**Lesson:** When reduce-motion is on, **freeze** the timeline (`minimumInterval: .infinity`) and render a single static frame with `t = 0`. Slowing is still motion, just less of it, and accessibility users explicitly opted out. Symbol pulses on focal elements can stay — they're not background ambient.

## 2026-05-20 — Outer `.padding(.horizontal:)` on a ScrollView clips horizontal carousels

**Tags:** [layout] [anti-pattern]
**Context:** An ArtistDetailSheet had `.padding(.horizontal, 20)` on the VStack inside its ScrollView. That inset propagated to every child, including two horizontal `ScrollView(.horizontal)` carousels and a "section card" that wanted full-bleed feel. The carousels couldn't scroll items out to the screen edge and the card looked like it was floating inset from both sides.
**Lesson:** Never apply horizontal padding to the outer content of a ScrollView when it contains horizontal carousels or full-bleed surfaces. Instead, move horizontal padding to each child that should be inset (hero text, section headers, button stacks), and use `.contentMargins(.horizontal:, for: .scrollContent)` (iOS 17+) on horizontal ScrollViews — that insets the content while keeping the scroll bounds at the screen edge.

## 2026-05-20 — `glassSurface` + base color: apply glass FIRST, color background SECOND

**Tags:** [api] [convention]
**Context:** Needed a glass play button with a guaranteed-dark base so white icons stay readable on bright artwork. Tinting the glass directly via `glassSurface(tint: .black)` only adds 0.18 opacity on the iOS 18-25 fallback path — too light. Two backgrounds were needed: glass + a black scrim.
**Lesson:** SwiftUI's `.background` stacks back-to-front in order of *application* — each new `.background` goes *further behind* the previous one. To compose "scrim behind glass behind content," apply `.glassSurface(in: shape, interactive: true)` FIRST, then `.background(.colorScrim, in: shape)` SECOND. Final stack: content → glass/material → color scrim → artwork.

## 2026-05-20 — `.symbolEffect(.bounce, value:)` on appear needs a one-tick defer

**Tags:** [api] [motion]
**Context:** Wanted a one-shot bounce when a HeroIconTile mounts (celebratory beat for "all caught up"). Flipping `appeared` from `false → true` inside `onAppear` sometimes didn't register with SwiftUI's symbol-effect coordinator — the bounce silently dropped on first display.
**Lesson:** Defer the value flip one runloop tick via `DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) { appeared = true }`. This gives the symbol effect coordinator time to see the view laid out before the value change fires. Without the defer the bounce works ~70% of the time and fails silently the rest — exactly the kind of bug that doesn't show in dev but ships broken.

## 2026-05-20 — `contentTransition(.symbolEffect(.replace))` only morphs same-view symbol swaps

**Tags:** [api] [anti-pattern]
**Context:** Tried to animate selection checkmarks in picker sheets via `if isSelected { Image(systemName: "checkmark") }` + `.contentTransition(.symbolEffect(.replace))`. Nothing animated — the checkmark still hard-cut in/out.
**Lesson:** `contentTransition(.symbolEffect(.replace))` only fires when the *same* `Image` view's `systemName` changes (e.g., `circle` ↔ `checkmark.circle.fill`). It does NOT fire when an Image view conditionally appears/disappears. For appear/disappear, use `.opacity` + `.scaleEffect` keyed off the selection bool. For state morphs, render the symbol always and swap its `systemName`.

## 2026-05-20 — Use distinct selection idioms for toggle-rows vs pick-one-rows

**Tags:** [convention] [layout]
**Context:** A redesign pass touched two kinds of selection lists: ManagePlaylistsSheet (multi-select sidebar membership) and SourceScopePickerSheet (pick one scope then dismiss). Using the same indicator pattern in both blurred the semantics.
**Lesson:** Use two distinct idioms. For **multi-select toggles**: always-rendered `circle` ↔ `checkmark.circle.fill` swap via `.contentTransition(.symbolEffect(.replace))` + `.symbolEffect(.bounce, value: isOn)`. The empty circle telegraphs "this can be toggled." For **pick-one-and-dismiss**: reserved-slot checkmark that fades via `.opacity(isSelected ? 1 : 0)` + `.scaleEffect(isSelected ? 1 : 0.4)`. No empty indicator on unselected rows — that would suggest multi-select. The reserved slot prevents row layout shift when selection changes.

## 2026-05-20 — Gesture-tied material `.opacity()` ramps aren't safely replaceable with helper backgrounds

**Tags:** [api] [anti-pattern] [motion]
**Context:** Almost swapped a `Rectangle().fill(.ultraThinMaterial).opacity(Double(dragProgress))` for `glassSurface(in: Rectangle())` during a glass-vocabulary pass on PlaylistSidebarView. The existing pattern uses an explicit Rectangle in a ZStack so its opacity can be bound to the drag-progress value — that's what makes the row fade in *with* the user's gesture.
**Lesson:** When a material or glass surface needs to ramp with a gesture, drag-progress, or any continuous binding, keep the explicit `Rectangle().fill(.material).opacity(binding)` pattern. `glassSurface()` and other `.background(material)` modifiers apply the material to the view, but you lose the ability to control its opacity independently from the content. Replacing such a Rectangle with a helper modifier silently regresses gesture feel — not a compile error, just a worse drag.

## 2026-05-22 — Xcode 16 synchronized file groups skip the pbxproj dance

**Tags:** [convention]
**Context:** Adding `Helpers/SettingsCard.swift` to a project where `objectVersion = 77` and `PBXFileSystemSynchronized` entries exist in the pbxproj. Past projects required editing the pbxproj to register a new file in the build phases; this one auto-includes any Swift file dropped into the synchronized folder.
**Lesson:** Before adding a new file, check HOW the project is managed, in this order: (1) Is the `.xcodeproj` itself gitignored? `git check-ignore <proj>/project.pbxproj` — if yes, the project is *generated*; look for a `project.yml` (XcodeGen) / `Project.swift` (Tuist). If the spec globs a folder for sources (XcodeGen `sources: [path: warket]`), just drop the file in that folder and run the generator — editing the pbxproj is wasted effort that gets wiped on regenerate. (2) Else grep for `PBXFileSystemSynchronized` — and rely ONLY on that grep, NOT on `objectVersion` (counterexample 2026-06-18: warket-ios is `objectVersion = 77` yet fully manual). (3) Else do the manual dance per file: a `PBXBuildFile`, a `PBXFileReference`, the target `PBXGroup` `children` entry, and the `PBXSourcesBuildPhase` `files` entry (4 edits). Verify with `xcodebuild -list` before investing in view edits, then a full build after.

## 2026-05-22 — `allowsHitTesting(false)` on an overlay forecloses every tap inside, including Buttons

**Tags:** [api] [anti-pattern]
**Context:** Tried to make an empty-state tile inside a PlaylistSidebarView tappable to open the Manage sheet. The sidebar lives as an overlay on top of a card with a `DragGesture`, and the overlay carries `.allowsHitTesting(false)` so the drag passes through. Wired a `Button` into the empty state — it compiled, looked correct, but never fired on tap because the parent's hit-test disable cascades to all children. SwiftUI does not let a child re-enable hit testing.
**Lesson:** When a view sits inside an overlay with `.allowsHitTesting(false)`, **no descendant Button or `onTapGesture` will ever fire**. Don't fight this — route the interaction through the owning gesture instead. Detect the relevant state in `onEnded` (e.g., "released while empty sidebar visible") and trigger the action from the parent. The UX often improves: the user doesn't have to release and re-tap. Caveat: copy must reflect the gesture model ("Release to…" not "Tap to…") so the affordance is honest.

## 2026-05-22 — Generic glass-card primitives need an optional trailing slot from day one

**Tags:** [convention] [api]
**Context:** Extracted a `SettingsCard` primitive on the first redesign pass. When two more screens adopted it, one needed a live count chip in the header — folded it into the title string instead and silently lost the existing `.contentTransition(.numericText)` digit tick on toggle.
**Lesson:** When extracting a generic card/panel primitive (especially anything labelled "header"), give it an optional trailing `ViewBuilder` slot using the `where Trailing == EmptyView` overload pattern from day one. Title strings are dead-ends for animation; trailing slots preserve callers' ability to render animated chips, badges, or live counts.

## 2026-05-22 — Replacing `Form` with `ScrollView` is the right move when redesigning settings screens around glass

**Tags:** [convention] [layout]
**Context:** Settings was a stock `Form` with five sections; the redesign called for Liquid Glass cards over `LivingMeshBackground`. Tried keeping `Form` with `.scrollContentBackground(.hidden)` and custom row backgrounds first — the section grouping, default row insets, and grey separators kept fighting the glass cards.
**Lesson:** When a settings/preferences screen redesign needs custom backgrounds AND custom row styling, drop `Form` entirely for a `ScrollView { VStack }` of hand-laid cards. `.scrollContentBackground(.hidden)` only solves the background; it doesn't free you from Form's row insets, grouping behavior, and built-in separators. The rewrite is small (~80 lines for 5 sections) and the result is consistent with non-Form screens in the same app.

## 2026-05-23 — "Cropped / floating" usually means missing layers, not wrong spacing

**Tags:** [layout] [convention]
**Context:** A new carousel screen had its hero artwork centred between two `Spacer()`s with a CTA pinned at the bottom. User said it felt "absolutely cropped." First instinct was to retune the spacing/padding; the real fix was that the screen had only ONE information layer (the art) when it needed THREE — identity above, art in the middle, song metadata below. Once those landed, the spacing took care of itself.
**Lesson:** When the user describes a redesign target as "cropped," "floating," or "stranded," diagnose missing layers before retuning spacing. A modal/exploration screen with a hero centerpiece almost always wants (1) a small identity/breadcrumb strip above and (2) supporting metadata below, with the CTA as a fourth beat. Trying to vertically-center a single element harder just makes the dead space cleaner, not smaller.

## 2026-05-23 — Sequential `withAnimation` + `Task.sleep` beats `phaseAnimator` for per-layer entrance staggers

**Tags:** [motion] [api]
**Context:** Wanted a 4-layer staggered reveal on screen mount (identity → carousel → metadata → CTA) with ~80ms offsets between each. `phaseAnimator([.hidden, .visible])` cycles through phases on a single trigger but doesn't expose per-phase delay knobs — you'd need to choreograph offsets inside the phase view's modifiers, which gets unwieldy with 4+ layers.
**Lesson:** For one-shot multi-layer entrance choreography, use a `@State revealStage: Int` bumped 0→N inside a `Task { @MainActor in ... }` with `try? await Task.sleep(for: .milliseconds(N))` between staged `withAnimation` blocks. Each layer reads `revealStage >= n ? visible : hidden` for its opacity/offset. Gives you exact per-layer timing in one place, plays naturally on every fresh mount, and degrades cleanly under reduce-motion (jump straight to the final stage).

## 2026-05-23 — `.contentTransition(.opacity)` propagates from container to child Texts

**Tags:** [api] [motion]
**Context:** Needed title and subtitle Texts to cross-fade together when the centred song changed in a carousel. Considered applying `.contentTransition(.opacity)` per-Text, but Swift inference and modifier order would have made each Text its own `.animation(value:)` site.
**Lesson:** `.contentTransition(.opacity)` (and friends) apply to **all** descendant Text views below them — put the modifier on the enclosing `VStack`/`HStack` once and trigger with a single `.animation(_:value:)` on the same container. Half the modifier surface; same visual result. (Does NOT work for symbol-effect replace — see the 2026-05-20 entry on symbol swap semantics.)

## 2026-05-24 — "AI slop" is the signal to break the project's vocabulary, not deepen it

**Tags:** [convention] [anti-pattern]
**Context:** A Culla settings screen had been redesigned earlier with the project's full glass vocabulary — `GlassPanel` cards, per-section icons, per-row icon badges, glass theme chips with halos, a 13-swatch palette grid, `LivingMeshBackground` underneath. The user called it "AI slop" and asked for "minimal purity." First instinct was to keep all those primitives and tone them down individually. The right move was to introduce a quieter sibling primitive (`SettingsCard`) used only by that one screen, while leaving the rest of the app's vocabulary untouched.
**Lesson:** When the user calls a screen "AI slop," resist the urge to consistently apply the project's existing primitives. Per-screen visual tiers are valid — a quieter sibling (`SettingsCard` next to `GlassPanel`, `QuietRow` next to `BadgedRow`) scoped to one consumer is better than diluting the brand primitive everywhere. Same shape, different decoration density. Confirm tier scope (this screen only? whole app?) before propagating the quiet version.

## 2026-05-24 — `Menu { Picker }` beats glass chip strips for 3-option selectors when the goal is calm

**Tags:** [api] [convention]
**Context:** A theme picker (System / Light / Dark) used a hand-rolled glass chip strip with accent halos, scale-up on selected, and bouncing symbols. Felt like a centerpiece for a setting people change once. Replaced with a `Menu { Picker("Theme", selection:) { Text("System").tag("system") ... } } label: { rowLabel }` — the row shows the current value and a `chevron.up.chevron.down`, taps open a native menu with automatic checkmarks.
**Lesson:** For any small-N enum selector on a settings/preferences screen, default to `Menu { Picker }` over a custom chip strip. Native menu UI, automatic checkmarks, free haptics, zero animation budget. Reserve the glass chip pattern for selectors that are *the* interaction on the screen (Home mode tiles), not configuration set-and-forgets.

## 2026-05-24 — Decoration that's always-on belongs behind a disclosure row

**Tags:** [convention] [layout]
**Context:** Culla's Settings had a 13-swatch accent palette rendered as a `LazyVGrid` at the top of the Appearance card. The rainbow read as decoration regardless of how disciplined the swatch styling was — it just *was* a wall of color. Moved it behind a `Color  ● Sky  ›` disclosure row that opens an `AccentPalettePickerSheet`. The screen instantly calmed; iOS Settings does the same for Appearance / Wallpaper / Accent Color.
**Lesson:** If a settings screen feels "loud" and one element is a colorful always-on widget (palette grid, theme thumbnails, big enum selector), the structural fix is to tuck it behind a disclosure row that shows the current selection as a single muted glyph. The picker becomes a *destination*, not a *decoration*. This works even when individual styling tweaks (smaller dots, no halo, no scale) have already been exhausted.

## 2026-05-24 — MeshGradient control points outside [0,1] produce empty diagonal triangles

**Tags:** [api] [anti-pattern]
**Context:** `LivingMeshBackground` based its side-middle mesh points at `x=0` and `x=1` and wandered them with amplitude `0.06`. Every animation cycle the points crossed outside the unit square. MeshGradient's bilinear quad triangulation breaks when an interior control point leaves `[0,1]` — the affected triangles render as empty/transparent diagonal cuts. The bug was app-wide but easiest to spot on tall sheets against a static toolbar; user reported it as "the mesh is bugged… some areas are just empty on diagonal cutting lines."
**Lesson:** Every `MeshGradient` control point must stay strictly inside `[0, 1]` across the entire animation cycle. When wandering interior points, base them inboard of the boundary (e.g. `x=0.05` / `x=0.95`) AND pick `amp` so `base ± amp` never reaches 0 or 1. Anchor corner and edge-midpoint vertices without wander. Diagnose mid-edge transparency / triangular voids as a control-point-bounds problem first.

## 2026-05-24 — Section-card primitives need ≥2 sections per sheet to earn their chrome

**Tags:** [convention] [anti-pattern]
**Context:** ManagePlaylistsSheet wrapped its single playlist list in a `GlassPanel(icon: "sidebar.right", title: "Sidebar", trailing: countChip)`. The screen IS the sidebar configurator — the panel header was naming the only section on the sheet, producing "the sidebar section of the sidebar sheet" redundancy. Sibling `LovedPlaylistPickerSheet` has *two* panels (Default + Playlists) and reads fine because the per-section framing earns its place.
**Lesson:** Reserve section-card primitives (`GlassPanel`, `SettingsCard`, etc.) for sheets with 2+ conceptual sections. For single-section sheets, drop the card wrapper — let the rows sit directly on a single glass slab, and put live counts/state in a `.footnote` subtitle line above the slab (with `.contentTransition(.numericText)`), not a chip floating in a panel header. The nav title provides identity; the subtitle provides state; the slab provides the content. Three layers, no redundancy.

## 2026-05-24 — "Broken" on a visual surface often means "inappropriate", not technically broken

**Tags:** [convention] [anti-pattern]
**Context:** User reported "the mesh background is broken" on two settings sub-sheets. `LivingMeshBackground` itself was fine — the diagonal-cut bug had been fixed in a prior commit. What the user was actually seeing: a recently-quieted parent screen (`SettingsView` was retiered from `GlassPanel`+mesh to `SettingsCard`+systemBackground in commit `50513e3`) opening into still-loud sub-sheets. The visual jolt from calm parent → ambient drift child read as a glitch.
**Lesson:** When a user calls a visual surface "broken" or "buggy," check both axes before fixing pixels: (1) is the surface technically broken? (2) does the surface conflict with a recent design shift in its surrounding context? If the parent was recently retiered to a calmer or louder tier, the child probably feels "broken" because it doesn't match — fix by propagating the tier, not by retuning the child's internals. Diagnose context-fit before assuming render bug.

## 2026-05-24 — Retiering a screen requires auditing its presented sheets in the same pass

**Tags:** [convention] [anti-pattern]
**Context:** `SettingsView` was quieted from glass-panel + mesh vocabulary down to a calm utility tier (private `SettingsCard` + `Color(.systemBackground)`). The two sheets it presents (`LovedPlaylistPickerSheet`, `AccentPalettePickerSheet`) kept the old loud vocabulary — `LivingMeshBackground` + `GlassPanel(icon:title:)`. A user opening one of those sheets crossed an unannounced visual tier boundary on every tap. Took a second pass weeks later to catch.
**Lesson:** When retiering a screen's vocabulary (quieter or louder), do a same-pass audit of every `.sheet(isPresented:)`, `.fullScreenCover`, and `NavigationLink` destination it presents. Each presented surface needs the same vocabulary as its presenter, or the user feels a discontinuity at the present boundary. Grep the file for `.sheet(` / `presents:` and walk the tree one level down before declaring the retiering done. Single-tier-per-flow is a hidden invariant.

## 2026-05-24 — Hero CTA primitives don't belong on management/utility sheets

**Tags:** [convention] [anti-pattern]
**Context:** ManagePlaylistsSheet placed a full-width `GradientCapsuleButton("New playlist", icon: "plus")` at the top of the sheet. That primitive is the project's HERO CTA — used for "Start Cullaing" (Home), "Continue" (AuthGate), "Refresh library" (EmptyState). Deploying it for a meta-action on a sheet whose actual purpose is configuration over-promoted "create playlist" and visually out-shouted the list the user came to manage. Demoted to a quiet toolbar leading `Image(systemName: "plus")` button.
**Lesson:** Hero CTA primitives (gradient capsules with accent shadow + halo) mark THE primary action of a screen. On management / picker / configuration sheets where the **content (the list) is the hero**, demote create/add actions to a toolbar `+` icon button — Apple-native, lives in the nav bar, doesn't compete with the rows below. Sibling rule: if the user opens the sheet to do X, the hero CTA should be for X. If it's for Y, Y is a toolbar action.

## 2026-05-25 — Selection state should signal ONCE; the accent shadow bloom is the half to cut

**Tags:** [convention] [anti-pattern]
**Context:** A "too much accent / AI slop" audit found selection states (mode tiles, theme chips) signalling selection THREE ways at once: accent border + glass tint + an accent-tinted `.shadow` bloom. SKILL.md's own convention ("Selected state = accent halo + chevron") had been read as license to stack all of them. The user wanted minimalism.
**Lesson:** When quieting a screen toward minimalism, a selected control needs exactly one accent signal carrying the *meaning* (the border or tint + a chevron) — drop the colored `.shadow` bloom, which is pure decoration radiating outward. The bloom is almost always the right thing to cut first: borders/tints/chevrons say "selected" precisely at the control's edge; a glowing halo just adds visual noise around it. Reserve a colored accent shadow for the ONE hero CTA per screen, and even there soften it (0.55 → ~0.30).

## 2026-05-25 — `replace_all` keys on exact indentation; identical-looking lines at different nesting are NOT both caught

**Tags:** [anti-pattern]
**Context:** Two visually identical `.shadow(color: appAccent.opacity(0.35), radius: pulse ? 28 : 16, y: 12)` lines existed in one file — one nested at 16 spaces inside a `ZStack` branch, one at 8 spaces at the view-modifier top level. An `Edit(replace_all: true)` reported "All occurrences replaced" but only touched the 16-space copy; the 8-space copy was a different exact string and survived silently.
**Lesson:** `replace_all` matches the literal string *including leading whitespace*. "All occurrences" means all occurrences of *that exact indentation*, not all semantically-identical lines. After a `replace_all` on a modifier that could appear at multiple nesting levels, grep the old pattern again to confirm none survived — don't trust the success message. Better: include enough trailing context (the following line) so each site is an explicit, separate `Edit`.

## 2026-05-25 — "Padded / floating sections" means strip card chrome, NOT retune padding values

**Tags:** [layout] [convention]
**Context:** User disliked how an artist sheet's sections were "padded" and wanted "inline integration, elements just above the sheet." The sections were per-section *floating glass cards* (`glassSurface` + white stroke + 20pt side inset each), mixed with full-bleed carousels. The fix wasn't tuning padding numbers — it was removing the card wrappers entirely so content sits flush on the sheet, full-width rows with leading-inset hairline `Divider`s (Apple-Music-style), headers/text at one consistent inset, carousels still full-bleed.
**Lesson:** When a user calls sections "padded," "floating," or "boxed," diagnose the *chrome* first: per-section card backgrounds + strokes + independent side insets are what make a screen read as stacked tiles. Going flush (drop the card, full-width rows, hairline dividers, one shared content inset) is usually the answer. NOTE the contrast with the 2026-05-23 "cropped/floating = missing layers" entry: if the complaint is about EMPTINESS/dead space, add layers; if it's about PADDING/CARDS/boxes, remove chrome. The word "floating" points both ways — disambiguate by what the user is pointing at.

## 2026-05-25 — Balance an official vendor badge by matching its SLOT, never by restyling it

**Tags:** [convention] [layout]
**Context:** A footer paired a custom "Search on Google" filled capsule with Apple's official "Listen on Apple Music" badge image. They looked disproportionate (different widths, weights, shapes). Apple's identity guidelines forbid pill-wrapping, recoloring, or relabeling the badge — so the badge itself can't be restyled to match. The fix: put BOTH in equal-width slots (`HStack` + each `.frame(maxWidth: .infinity).frame(height: 48)`), let the bare badge scale-to-fit centered in its slot, and quiet the custom button (drop its shadow, shorten its label) so the pair reads balanced.
**Lesson:** To balance an untouchable official badge (Apple Music, Sign in with Apple/Google) against a custom control, equalize the *container* — same width via `HStack` equal frames, same fixed height — and tone the custom side toward the badge's restraint. Never wrap or restyle the badge to force symmetry; that violates the vendor's identity rules. The slot does the balancing, not the artwork.

## 2026-05-25 — Solid accent fills need a COMPUTED contrast foreground, not hardcoded white

**Tags:** [api] [convention] [anti-pattern]
**Context:** Culla's mode tiles got a bold solid-accent selected state. The project's CTA (`GradientCapsuleButton`) hardcodes `.foregroundStyle(.white)` on the accent fill, and `AccentPalette`'s doc claims every swatch is "dark enough (lightness ≲ 0.55)" for white text. But swatches added later (Amber 0.93/0.55/0.18, Rose 0.92/0.48/0.62) are *light* — white-on-amber is as unreadable as the black-on-dark bug being fixed.
**Lesson:** When laying text on a solid accent/brand fill that can be any of N palette colors, never hardcode the foreground. Compute it from perceptual luminance (`0.299r+0.587g+0.114b > 0.6` → near-black, else white) via a tiny `Color.idealForeground` helper using `UIColor.getRed` (iOS 17-safe). Don't trust a palette's "tuned for white text" doc comment — new swatches violate it silently, and a hardcoded-white CTA is a latent bug, not a precedent to copy.

## 2026-05-25 — A bold solid-accent selection is OK for THE primary selector, if you still skip the bloom

**Tags:** [convention]
**Context:** The project has a strong accent-restraint stance (memory + the 2026-05-25 "signal ONCE, cut the bloom" learning). The user nonetheless asked for a *bolder* selected mode tile — solid accent fill instead of a faint tint — because the faint tint both hurt black-text contrast and under-sold the selection.
**Lesson:** Accent restraint governs decorative/secondary surfaces; it does NOT forbid a confident solid-accent fill on THE single primary selector of a screen (Home mode tiles, a segmented hero control). When you go bold there: (1) make it a real opaque fill so text contrast is clean, (2) flip ALL tile content to the computed contrast foreground, (3) STILL omit the accent shadow bloom — the fill is the one signal. Bold fill ≠ bloom; the signal-once rule survives.

## 2026-05-26 — To accent small chips/labels, ride the accent on tint+stroke and keep text neutral

**Tags:** [convention] [api]
**Context:** Asked to make neutral playlist-membership chips "pick up the accent." The accent can be an album-derived tint (any hue, often pale) — colouring the chip's *text* with it would fail contrast on the system background, the inverse of the text-ON-accent-fill trap. Also: the dynamic-vs-palette choice was already resolved into `\.appAccent` upstream, so the chip needed zero new setting wiring — it just read the environment.
**Lesson:** When tinting small informational chips/labels with a variable accent, put the accent on the *capsule* (`glassSurface(in:tint:)` + a `Capsule().strokeBorder(accent.opacity(~0.35))` hairline) and keep the text `.primary`. Never use the accent as a foreground colour over a neutral background — pale accents vanish. Bumping `.secondary` → `.primary` is itself half the "more visible" win. And before adding a setting-dependent style branch, check whether the value is already resolved into the environment upstream — it usually is.

## 2026-05-26 — A "single loading state" must live in the reused inner view, not just the entry point

**Tags:** [convention] [anti-pattern]
**Context:** Asked to collapse 3 spinners (resolve / topSongs+similar / Wikipedia bio) in an artist sheet into one clean load. The sheet split work across an outer `ArtistDetailSheet` (does the song→artist resolve) and an inner `ArtistDetailView` (does the detail+bio fetch) — and the inner view is *also* the `navigationDestination` for similar-artist drill-downs. Putting the single loading state only on the outer resolve step would have left the inner view popping spinners on every push.
**Lesson:** Before consolidating loading states, find every entry into the view that loads. If a view is reused as a `navigationDestination`/pushed child, the single-load gate (`@State isReady` + reveal crossfade) must live *inside that reused view*, not just at the outer entry — otherwise the consolidation only fixes the first screen and every drill-down regresses. Use the SAME loading subview in both the outer (pre-resolve) and inner (pre-detail) states so the breathing placeholder stays continuous across the handoff. Bonus: the identity (artist name) is usually known up front, so the loading state shows a named hero skeleton, not a blank spinner.

## 2026-05-26 — Gate the reveal on core data; let slow/optional data fade in spinnerless

**Tags:** [convention] [motion]
**Context:** The artist sheet had a Wikipedia/MusicBrainz bio (two network hops, can be slow or 404) loading concurrently with the MusicKit data. The user wanted "one load then a full sheet." Blocking the whole sheet on the bio would let a slow Wikipedia stall content (songs, similar artists) that was ready instantly.
**Lesson:** When a screen mixes fast/required data with slow/optional data, gate the single reveal on the *required* data only and let the optional source resolve spinnerless: render nothing for its `.loading` and `.empty` states (`case .empty, .loading: EmptyView()`), then `withAnimation(.smooth)` into `.loaded`/`.failed` with `.transition(.opacity)` when it lands. A spinner parked inside already-revealed content is exactly the "too many loading states" smell; a silent slot that fades in is calm. Confirm the gating boundary with the user — "wait for everything" vs "reveal fast, fill in" is a real UX trade, not an implementation detail.

## 2026-05-27 — Re-skin List screens in place; don't convert to ScrollView

**Tags:** [layout] [anti-pattern]
**Context:** Redesigning a photo-app's Galleries + gallery-picker screens. They're `List`s carrying swipe-to-delete, drag-`onMove` reorder, and `EditMode` rename. Converting to a `ScrollView` of glass cards (the obvious "modernize" move) would have silently dropped all three native behaviors.
**Lesson:** When a `List` carries `swipeActions`/`onMove`/`EditMode`, keep the `List` and float glass cards on it instead of rewriting to `ScrollView`: `.listStyle(.plain)` + `.scrollContentBackground(.hidden)` + `.background { LivingMeshBackground() }`, then per-row `.listRowBackground(Color.clear)` + `.listRowSeparator(.hidden)` + `.listRowInsets(...)` with the glass card as the row content. You get the redesign's look with zero behavior regressions. Every row (including headers/stats/empty) needs the clear row-background or it shows an opaque system fill.

## 2026-05-27 — Clamp vivid accent saturation (HSB) before seeding a MeshGradient

**Tags:** [api] [motion]
**Context:** Ported `LivingMeshBackground` from a sibling app whose accent palette was tuned/muted. This app's accents are raw neons (#39FF14, #FF2D78…). Seeded directly, the mesh painted the page electric and iOS-26 glass cards refracted that saturated color through their edges, making the cards look marginless.
**Lesson:** Before seeding a mesh/glass-tint from a *user/brand* accent that can be arbitrarily saturated, clamp it through `UIColor.getHue` into a calm band (e.g. saturation 0.20–0.50, brightness 0.45–0.80) and seed the mesh from the clamped color. Guard `getHue`'s return (false for `.primary`/dynamic colors) and fall back to the raw color. A mesh that "looks fine" with a tuned palette can be garish with a vivid one — don't assume the source palette's restraint.

## 2026-05-29 — Shimmer over a translucent bone: `.clipShape(shape)` the sweep, don't `.mask(content)`

**Tags:** [api] [motion]
**Context:** Built a skeleton-loading shimmer where each placeholder "bone" is a `Shape` filled with a translucent color (`Color.primary.opacity(0.10)`) so it reads as light gray. The instinct is `content.overlay(sweep).mask(content)` to confine the highlight to the bone — but `.mask` uses the content's *alpha*, so a 0.10-alpha fill dims the sweep to ~5% and it's invisible.
**Lesson:** To clip a shimmer/highlight to a translucent skeleton bone, give the bone an explicit `Shape` and clip the sweep with `.clipShape(shape)`, NOT `.mask(content)`. `clipShape` clips by geometry (full-strength highlight inside crisp rounded edges); `.mask` clips by alpha (a faint fill = a faint sweep). Reserve `.mask(content)` for opaque content.

## 2026-05-29 — A loading placeholder must match the revealed content's ALIGNMENT, or the hero slides on reveal

**Tags:** [layout] [motion] [anti-pattern]
**Context:** An artist sheet's loading view centered its hero (`.frame(maxHeight: .infinity)`) while the real content is a top-anchored `ScrollView`. A code comment claimed the hero "stays put across resolve → detail" — it didn't: under the `.transition(.opacity)` crossfade the hero visibly slid from center to top. The fix was simply top-aligning the placeholder (`alignment: .top`) so the hero materializes in place.
**Lesson:** When a loading state crossfades into real content, the placeholder's hero/key element must share the revealed content's alignment and insets, not just its size. Centering a placeholder over top-anchored content (or vice versa) produces a position slide under the crossfade that reads as "placeholder, not content." Match `alignment` + padding to the destination layout; verify by eye that the shared element doesn't move on reveal.

## 2026-05-29 — Phase-sync per-shape shimmers via a shared TimelineView clock — no top-level mask needed

**Tags:** [motion] [api]
**Context:** Wanted one coordinated shimmer sweeping across a multi-bone skeleton (hero tile + 4 rows of varying widths). The "correct" way (a single full-bleed sweep masked by the union of all bones) needs a duplicate copy of the whole layout to mask against — brittle and verbose.
**Lesson:** Instead, drive each bone's own sweep from the SAME global clock: `TimelineView(.animation)` → `phase = (date.timeIntervalSinceReferenceDate % period) / period`, with the sweep offset parameterized by that 0→1 fraction. Every bone places its highlight at the same fraction-across at any instant, so independent per-shape sweeps read as one coordinated shimmer — no shared mask, no layout duplication. Bonus: each bone clips its own sweep, so it composes cleanly with differing shapes/sizes.

## 2026-05-29 — A skeleton for a multi-card DECK mirrors the rest pile, built inside the owning view

**Tags:** [layout] [convention] [anti-pattern]
**Context:** Replaced a hero's single pulsing-material placeholder with a shimmer skeleton. The real loaded state is a 3-card deck (centre + two peeking), so a one-bone placeholder popped 1→3 cards on reveal. The slot transforms (offset/scale/rotation) were `private static let` on the owning view.
**Lesson:** When the loaded state is a multi-element pile/deck, the skeleton must reproduce ALL the resting elements at the SAME transforms, not one bone. Build it as a method *inside* the view that owns the layout constants and reuse those exact constants — Swift `private` is unreachable from sibling types in the same file, so extracting the skeleton to its own file would force exposing or duplicating the geometry (drift risk). The reusable piece is the shimmer primitive (`SkeletonShape`), not the per-screen skeleton arrangement.

## 2026-05-29 — Don't dim skeleton back-bones to the real elements' opacity

**Tags:** [motion] [layout] [anti-pattern]
**Context:** The deck's resting back cards sit at ~0.78–0.85 opacity. Instinct was to apply each slot's `opacity` to its skeleton bone for fidelity. But a translucent-gray bone (`.primary.opacity(0.10)`) × 0.78 is nearly invisible — the deck collapsed back to reading as one card, undoing the whole point.
**Lesson:** Render all skeleton bones at FULL strength even when the real elements they stand in for are partially transparent at rest. The bone is already faint; stacking the real element's slot-opacity on top erases it. Let the actual content fade to its resting opacity on reveal — that subtle settle is correct; an invisible placeholder is not. Match position/size/rotation, NOT opacity.

## 2026-05-29 — Skeleton bones over a variable accent fill need the computed contrast tint, not the default

**Tags:** [convention] [api]
**Context:** A loading "bone" for a count badge sat inside a mode tile whose SELECTED state is a solid accent fill. The default bone fill (`.primary.opacity(0.10)`) nearly vanished on light accents (Amber/Rose). And the default-selected tile's count loads on cold launch, so the over-accent case is the COMMON path, not an edge case.
**Lesson:** When a skeleton bone can render over a variable accent/brand fill, tint it with the same computed contrast foreground used for text on that fill (`isSelected ? accentForeground.opacity(~0.28) : .primary.opacity(0.10)`) — not the default neutral. Same trap as text-on-accent (see 2026-05-25): a fixed neutral disappears on half the palette. Check whether the loading state coincides with the selected/filled state on first launch before assuming the over-accent case is rare.

## 2026-05-30 — A "two-step jump" sheet load is a tall detent + onAppear focus; fit the sheet to content

**Tags:** [motion] [layout] [api]
**Context:** `NewPlaylistSheet` was a one-field `Form` at `.presentationDetents([.medium])` that auto-focused in `onAppear`. The user felt it "loads in two step jumps": the half-screen sheet rose tall-and-empty (motion 1), then `isFocused = true` brought the keyboard up as a *separate* animation (motion 2), stranding one field atop a grey void.
**Lesson:** When a small modal "loads in two jumps," the cause is almost always a tall fixed detent (`.medium`) animating independently from a late-focus keyboard. Fix by sizing the sheet to its content with a custom `.presentationDetents([.height(h)])` so the card and keyboard settle as one move — drive `h` from `@ScaledMetric` so it grows with Dynamic Type instead of clipping the CTA. Keep `onAppear` focus (the keyboard then rises *with* the compact sheet, not after a tall one).

## 2026-05-30 — The "hero CTA off utility sheets" rule has a single-purpose exception

**Tags:** [convention]
**Context:** A prior learning demoted `GradientCapsuleButton` to a toolbar `+` on `ManagePlaylistsSheet` (its hero is the list; create is a meta-action). On `NewPlaylistSheet`, creating the playlist IS the sheet's entire purpose — so the gradient CTA inline at the bottom, right above the keyboard, is correct, not a violation.
**Lesson:** Apply "hero CTA primitives don't belong on management/utility sheets" only when the CTA is a *meta*-action competing with the screen's real hero (a list). On a single-purpose action sheet (create/rename/confirm), the action IS the hero — give it the inline gradient CTA and place it bottom-anchored above the keyboard, not as a tiny top-bar "Save" the typing thumb can't reach.

## 2026-05-30 — "Make the toast smaller" can mean "remove a duplicated affordance," not shrink type

**Tags:** [convention] [anti-pattern]
**Context:** Asked to make a swipe-screen toast "more minimalistic, smaller." Shrinking font/padding helped, but the real bulk was an inline Undo button + divider the toast hosted only for destructive actions — while a separate bottom Undo button already existed (the two were made mutually exclusive via a `!toastUndoable` gate). The user immediately spotted it: "why show Undo again on the toast?"
**Lesson:** When asked to shrink a toast/snackbar, first audit whether any *action* it hosts is already provided by another affordance on the same screen. Consolidating to one undo/action surface is a bigger minimalism win than smaller type, and turns the toast into a pure status pill. If the removed inline affordance had a longer timeout than its surviving sibling, preserve the window by reading the same flag in the survivor's hide-timer (`linger = undoable ? 6 : 2.5`), so nothing regresses.

## 2026-05-30 — `onChange(of:)` sees end-of-batch state, so intra-function mutation order is moot

**Tags:** [api]
**Context:** Worried that `undoCoordinator.record(...)` (which bumps an observed `actionCount`, firing `onChange → flashUndo`) ran a line *before* `setToast(undoable: true)` set the flag `flashUndo` needed to read. Feared the handler would see the stale flag.
**Lesson:** A SwiftUI `onChange(of:)` handler runs after the current synchronous mutation batch completes, not at the instant the tracked value is written. So later same-function mutations (set after the tracked write) are already applied when the handler fires — you can safely have `onChange(of: A)` read a sibling flag `B` that's set a few lines *after* `A` changed. Don't reorder code to "fix" this; verify by tracing the synchronous body instead.

## 2026-05-31 — De-nest a "sub-tab under a tab" by demoting the inner segmented control to a header Menu chip

**Tags:** [convention] [layout] [anti-pattern]
**Context:** ManagePlaylistsSheet had a top segmented control `[Sidebar | Filter queue]` and, when Filter was active, a SECOND full-width segmented control `[Playlists | Artists]` slid in beneath it. Two horizontal pickers stacked vertically read (the user's words) as "a nested toggle sheet bolted onto the bottom of the original one."
**Lesson:** When a screen nests one segmented control under another (a tab with a sub-tab), don't restyle the inner bar — demote it. Move the inner scope switch into the content `List`'s section header as a `Menu { Picker }` chip, paired on the trailing edge with whatever control already lives there (a sort chip). The section header is the right home: it sits directly above the rows it scopes, costs one chip instead of a full-width band, and keeps the ability to jump between two long lists (which a single merged two-section list loses). Relocate any header *count text* to the footer to free the header for the two chips — its `.contentTransition(.numericText)` tick survives the move.

## 2026-05-31 — Make a labeled glass chip by cloning an icon-chip's chrome and swapping `.circle` → `.capsule`

**Tags:** [convention] [api]
**Context:** Needed a new scope-switcher chip to sit beside the existing icon-only `SortChip` (a `Menu` styled with `.buttonStyle(.glass).buttonBorderShape(.circle)` on iOS 26, `.thinMaterial` Circle pre-26). The new chip carries text+chevron, so it can't be the circle.
**Lesson:** To add a *labeled* sibling to an existing icon-only glass chip, copy its chrome `ViewModifier` verbatim and change only `.buttonBorderShape(.circle)` → `.capsule` (and the pre-26 fallback `Circle()` → `Capsule()` with horizontal padding). Same OS gating, same neutral `.tint(.secondary)`, same menu-morph behavior — the two chips then read as one matched family in a header for near-zero new code. Keep label foregrounds explicit (`.primary` text, `.secondary` icon/chevron) so the glass tint doesn't recolor them.

## 2026-05-31 — Toast icon-by-action-type = a semantic enum at the source, never string-sniffing the view

**Tags:** [convention] [anti-pattern]
**Context:** Asked to give a swipe toast a trailing icon that varies by action (loved / dismissed / removed / error…). The toast only carried a `String` + an `undoable: Bool`; the tempting shortcut was to map message prefixes to icons inside the view.
**Lesson:** When a feedback surface (toast/snackbar/banner) must vary its icon or styling by action type, add a SwiftUI-free `Kind` enum (SF Symbol name + a small `Role`) on the data source and thread it through the existing single toast-setter (`setToast(_:kind:undoable:)`) with a safe default. Never infer the type from the message copy in the view — it silently breaks the moment wording changes. The single-funnel setter makes tagging cheap (here ~25 one-line call-site edits) and keeps message+kind from drifting. Map roles to ≤3 colors (brand accent / neutral gray / red) so it stays semantic, not rainbow.

## 2026-05-31 — Re-fire .symbolEffect(.bounce) across in-place content swaps with a monotonic Int

**Tags:** [motion] [api]
**Context:** A toast view is inserted once (onAppear) but then updated in place when back-to-back actions swap its text without it disappearing. A bounce keyed only to onAppear fires on the first toast but never on subsequent same-view swaps; one keyed only to `.symbolEffect(value: message)` skips the very first appearance (value effects fire on change, not initial).
**Lesson:** For a symbol that should react on first show AND on every in-place content change, drive `.symbolEffect(.bounce, value: tick)` off a `@State var tick = 0` bumped in BOTH `.onAppear` (deferred one runloop tick — see 2026-05-20) and `.onChange(of: content)`. The Int guarantees a fresh value even for two consecutive same-kind states. Covers the insert-once-then-mutate lifecycle that conditional overlays (`if let toast = …`) actually have.

## 2026-06-01 — `#available` is runtime-only; verify the installed SDK compiles iOS 26 glass first

**Tags:** [gating] [api] [anti-pattern]
**Context:** Before writing the `glassSurface` helper for a beatmatching app on an iOS 18.0 floor, I ran `xcodebuild -version` + `xcrun --sdk iphonesimulator --show-sdk-version`. They reported Xcode 26.2 / SDK 26.2, so the gated `glassEffect`/`Glass` code compiles. Had the SDK been < 26, that branch would have failed to compile *even behind* `if #available(iOS 26.0, *)`.
**Lesson:** `if #available` is a runtime guard — it does NOT exempt code from compiling against the active SDK. Before committing to a Liquid Glass (or any iOS 26) branch, run `xcrun --sdk iphonesimulator --show-sdk-version`. If it's ≥ 26, write the gated helper; if it's < 26, skip the glass branch entirely and use `.ultraThinMaterial` directly — the gated code won't build on the older SDK no matter how it's wrapped.

## 2026-06-01 — Visualize a numeric RELATIONSHIP as two synced ambient signals, not two readouts

**Tags:** [motion] [convention]
**Context:** A half-time/double-time BPM tool showed source and result as stacked text (input→output). The app's whole point is a *tempo ratio* (×½ / ×2), which the calculator layout rendered invisible. The redesign put the result number inside a ring pulsing at the result tempo, plus a fainter concentric ring pulsing at the source tempo — so HALF mode literally shows the outer ring beating twice per inner beat.
**Lesson:** When an app's core value is a *relationship* between two numbers (a ratio, a tempo, a difference, a conversion), express it as two synchronized ambient signals (overlapping pulse rates, paired motion) rather than two static readouts — the relationship becomes perceptible instead of arithmetic. Keep the primary number itself dead-stable (only the surrounding rings move) so glanceability survives the motion. Beat phase: `phase = (t * bpm/60).truncatingRemainder(dividingBy: 1)`, envelope `exp(-phase * k)` for a metronome spike.

## 2026-06-01 — When motion IS the feature, reduce-motion degrades to opacity-blink, not freeze

**Tags:** [motion] [convention]
**Context:** The pulse rings ARE the app's headline feature (a visual metronome), unlike the ambient `LivingMeshBackground` which freezes flat under reduce-motion per the 2026-05-20 rule. Freezing the metronome entirely would delete the core value for reduce-motion users.
**Lesson:** The "freeze ambient motion under reduce-motion" rule applies to *decorative* motion. When the motion is the screen's primary function, degrade it to the lowest-motion form that still conveys the information — swap `scaleEffect` pulses for opacity blinks (a fade is far less vestibular than a transform) rather than killing it. Still freeze any genuinely-ambient background in the same view. Confirm the choice with the user — "freeze vs minimal blink" is a real accessibility trade, not an implementation default.

## 2026-06-02 — A glassEffectID shape-morph needs two MUTUALLY-EXCLUSIVE states; coexisting elements get materialize instead

**Tags:** [api] [anti-pattern]
**Context:** User approved a "bold" iOS 26 morph of Home's mode-tile cluster *into* the source pill. But the tiles show when `source == nil` and the pill shows whenever `mode == .library` — so when no source is picked, **both are on screen at once**. A shared `glassEffectID` shape-morph between them is semantically wrong: there's no single glass shape traveling from A to B, they coexist then one leaves.
**Lesson:** Before wiring a `glassEffectID` shape-morph between elements A and B, confirm A and B are genuinely mutually-exclusive render states (one replaces the other). If they coexist before the transition, a shape-morph is wrong — deliver the *coordinated* version instead: give each its own id in a shared `GlassEffectContainer` and let the leaving cluster `.materialize` out while the arriving chips `.materialize` in. Same "liquid" read, correct semantics. Tell the user why you reinterpreted their literal ask.

## 2026-06-02 — For `.materialize`, the GlassEffectContainer must live OUTSIDE the `if`, not inside it

**Tags:** [api] [gating]
**Context:** Making a swipe-screen undo chip and a swipe arming coin crystallize in/out via `.glassEffectTransition(.materialize)`. First instinct was to wrap the glass in its container at the same place it's conditionally created.
**Lesson:** A glass child only *materializes* if its `GlassEffectContainer` is a **stable parent** that outlives the child's appear/disappear. Put the container OUTSIDE the `if`/conditional (e.g. `.overlay { GlassStack { undoButton } }` where `undoButton` is the `if`), so the container persists and the child crystallizes inside it. Container inside the `if` = container and child appear together = no materialize, just a plain insert. Corollary: a VStack-based `GlassStack { singleChild }` (even wrapping one `ZStack`) is a zero-layout-cost way to hand an ad-hoc glass element the container `.materialize` requires — no new ZStack-container helper needed.

## 2026-06-08 — "Distribution issues / not integrated" with no card complaint = fragmented metadata + uniform spacing

**Tags:** [layout] [convention]
**Context:** AlbumDetailSheet read as four stacked blocks. The user said "spacing/distribution issues… make it more integrated" — but unlike the "cropped" (missing layers) and "padded/floating" (strip card chrome) families, nothing was empty and the one card wasn't the complaint. The real cause: the album's facts were split across two clusters (year glued to the title, song-count/runtime/© floating a section-gap below) and every block sat at a uniform 24pt, so the identity's internal break equalled the break between identity and body — nothing grouped.
**Lesson:** Add a third branch to the floating/cropped/padded diagnosis family. When a screen "doesn't feel integrated" but isn't empty and has no offending card, look for (1) metadata of one tier fragmented across two blocks — regroup it into a single identity cluster directly under the title — and (2) a single uniform VStack spacing flattening hierarchy — replace it with grouped spacing (tight within a unit, one larger gap to the body). Fixing grouping, not chrome, is the move here.

## 2026-06-08 — Sheets opened from the same affordance must share section/row vocabulary

**Tags:** [convention] [anti-pattern]
**Context:** AlbumDetailSheet and ArtistDetailSheet are both opened from info buttons on the same swipe card. The Artist sheet had already gone flush (full-width rows, leading-inset hairline dividers, per-section headers, per-section insets); the Album sheet still wrapped its single tracklist in a floating glass card with one outer inset and no header. Two sheets from one place, two vocabularies — that mismatch *was* the "not integrated" feeling.
**Lesson:** When redesigning one of a set of sibling sheets reachable from the same entry point (the info buttons on a card, the rows of a list), diff it against its siblings FIRST and inherit their proven structure (outer-vs-per-section padding, header style, card-vs-flush, divider insets) rather than inventing a parallel one. This is the sibling analogue of the 2026-05-24 parent→child retiering audit: there the discontinuity is felt across a present boundary; here it's felt across two paths from the same surface.

## 2026-06-09 — A "raw" instructional/diagram overlay is missing containment + a central referent

**Tags:** [layout] [convention]
**Context:** A first-run swipe guide laid out four bare SF arrows + labels in a cross on a flat fill. User called it "too simple/raw." Retuning fonts/spacing wouldn't have helped — the arrows had nothing to point *at*, and floating text has no form.
**Lesson:** When an instructional/diagram overlay reads "raw," add (1) containment — wrap each item in a soft glass chip so it has edges and depth — and (2) a central referent the directional cues point at (here a small "card token"). Arrows/labels gain meaning from what sits at the center of the diagram; without it they're just decoration. Parallel to the "cropped = missing layers" rule, but for diagrams the missing layer is usually the *thing being acted on*.

## 2026-06-09 — Constrain a full-width hero-CTA primitive with `.frame(maxWidth:)` instead of rebuilding a "compact" one

**Tags:** [convention] [api]
**Context:** Wanted a compact branded "Got it" button on an overlay. The app's `GradientCapsuleButton` is `.frame(maxWidth: .infinity)` with centralized gradient + contrast + shadow. Rebuilding a smaller accent capsule inline would have re-hardcoded white-on-accent and drifted from the app's CTA over time.
**Lesson:** To get a "compact" version of a full-width CTA primitive, wrap the existing primitive in `.frame(maxWidth: <pt>)` rather than hand-rolling a smaller capsule. You keep the centralized gradient/contrast/shadow (so it tracks the real CTA as the design evolves) and only constrain width. Reinventing a "small" variant duplicates the contrast logic the primitive already owns.

## 2026-06-09 — A "shifted/lopsided" diagram = content-hugging cells; lock it to a fixed Grid

**Tags:** [layout] [convention]
**Context:** A swipe-guide "compass" laid out four direction chips in a `VStack[up] / HStack[left·card·right] / VStack[down]`. Each chip hugged its label ("Dismiss" wide, "Add" narrow), so the fat left chip shoved the centre card token off the vertical axis — the cross looked lopsided. User: "shifted/unstructured, ugly." This is the SEQUEL to the same day's "raw overlay = add containment + referent" entry: containment fixed *raw*, but content-sized cells still produced *imbalance*.
**Lesson:** When a directional/cross/compass diagram reads "shifted" or "lopsided," the cause is cells sized to their content, not a spacing value. Move it to a `Grid` (3×3 for a compass: N/E/S/W tiles + centre referent + empty corners) and give every tile an identical fixed `.frame(width:)`. Make each tile's weight label-length-independent — a fixed-size tinted icon *badge* (Circle) over the label, so a 7-letter word and a 3-letter word occupy the same footprint. Wrap the whole grid on ONE glass slab for cohesion (four loose glass chips never read as one instrument no matter how aligned). Diagnosis ladder so far: empty→add layers; padded/boxed→strip chrome; fragmented→regroup; raw→containment+referent; **lopsided→fixed grid + equal-footprint cells.**

## 2026-06-09 — A full-screen first-run overlay should REPLACE the heavy content, not layer over it

**Tags:** [motion] [anti-pattern] [convention]
**Context:** A first-run swipe guide was an `.overlay { if shouldShow { Guide } }` on top of the full swipe deck (card stack + glass chrome + artwork). The user reported the device "lags" while the guide is up — because both the guide AND the deck were fully built and composited the whole time the user reads the guide (steady-state double layer), not just during the transition.
**Lesson:** When an opaque full-screen first-run/modal overlay covers heavy content anyway, make it a **mutually-exclusive branch** of the same ZStack (`if shouldShow { Guide } else if loaded { content }`), not a layer on top — so the heavy view isn't built at all while the overlay shows. Two prerequisites: (1) confirm the data load that the show-condition depends on is triggered OUTSIDE the gated view (e.g. in the router's `startSession`, not a `.task` on the deck) or you deadlock — the overlay needs `!isLoading` but the view that loads is now un-built; (2) re-home any chrome that was implicitly z-covered by the old overlay (a back button overlay now floats *over* the branch — gate it with the same `!shouldShow`). A `.animation(value: shouldShow)` on the ZStack gives a clean single-layer crossfade between overlay and content.

## 2026-06-10 — A learning that flags a latent bug in a shared primitive must fix the primitive in the SAME pass

**Tags:** [anti-pattern] [convention]
**Context:** A 2026-05-25 entry explicitly called `GradientCapsuleButton`'s hardcoded `.foregroundStyle(.white)` "a latent bug, not a precedent to copy" — but only the new ModeTile got the computed `idealForeground`; the flagged primitive itself shipped unfixed. Two weeks later a fresh pass re-discovered the same unreadable white-on-Amber CTA.
**Lesson:** When a redesign pass identifies a defect in a *shared* primitive (CTA button, card, chip), patch the primitive right then, even if the pass's scope is a different view — the fix is usually one line and propagates to every consumer. Writing "this is a bug" into LEARNINGS.md without fixing it just schedules a re-discovery. If the fix genuinely can't land in-pass, say so in the caveats so the user owns the deferral.

## 2026-06-10 — Tune ambient breathe so phase 0 reproduces the old static frame

**Tags:** [motion] [convention]
**Context:** Added a sub-perceptual breathe (opacity 0.30±0.03, scale ±3%, 18s sine) to a previously static background glow that the user had deliberately calmed down from an animated mesh. Reduce-motion freezes the timeline at `t = 0`.
**Lesson:** When animating a previously-static element, parameterize the motion as `static_value ± amplitude · sin(t)` so phase 0 *is* the proven static design. The reduce-motion freeze frame then renders exactly the layout the user already approved (zero regression risk), and reviewing the diff confirms the motionless case by inspection instead of by eye.

## 2026-06-14 — A conditionally-rendered subview's onAppear IS the "entered this mode" initializer

**Tags:** [convention] [api]
**Context:** Extracting an inline custom-accent swatch grid out of `SettingsView`. Its init logic was spread across the parent's `.onChange(of: accentMode)` (seed/select swatch when switching to custom) AND `.onAppear` (restore selection on launch). The grid only renders `if accentMode == "custom"`.
**Lesson:** When an inline block renders behind a condition AND the parent initializes it from both `.onChange` and `.onAppear`, extract it to a self-contained subview that owns its own `@AppStorage`/`@State` and does its init in its OWN `.onAppear`. Because the subview mounts exactly when the condition flips true, its `onAppear` fires at the same moment the old `.onChange` did — so the two parent lifecycle handlers collapse into the child and the parent's `.onChange` shrinks to pure gating (here: the Pro-paywall guard). Net: parent loses a `@State`, a computed prop, a helper, and an entire `.onAppear`.

## 2026-06-14 — Runtime app-icon lookup needs the CFBundleIconFiles path PLUS an "AppIcon" asset fallback

**Tags:** [api]
**Context:** Built a Settings identity header showing the live app icon. The standard `CFBundleIcons → CFBundlePrimaryIcon → CFBundleIconFiles.last` → `UIImage(named:)` lookup returns nil for apps whose icon is an asset-catalog "AppIcon" set (common), silently degrading the header to wordmark-only.
**Lesson:** To render the app's own icon at runtime, try the `CFBundleIconFiles.last` name first, then fall back to `UIImage(named: "AppIcon")` — asset-catalog icons frequently aren't enumerated in `CFBundleIconFiles`. Always provide the wordmark/text-only degradation for the genuinely-nil case (previews, weird configs) rather than a broken-image frame. Can't be verified in `xcodebuild`; flag "confirm the icon renders on-device" in caveats.

## 2026-06-14 — LEARNINGS.md is shared across sibling apps; verify a named-screen entry against THIS repo's git first

**Tags:** [anti-pattern]
**Context:** Two prior entries described redesigning "the Culla settings screen" (replacing chip strips with `Menu { Picker }`, tucking the palette behind an `AccentPalettePickerSheet` disclosure row). Those decisions were actually made in the *sibling* app `culla-music-app` — `AccentPalettePickerSheet` never existed in this `culla-app` repo, whose settings screen kept an inline chip-strip + swatch-grid design throughout. Treating the prior entries as settled history here would have wrongly framed the current design as a regression to undo.
**Lesson:** This global skill is reused across sibling apps (culla-app / culla-music-app share a ported design system), so a LEARNINGS entry that names a screen may describe a *different* repo. Before treating a past redesign as "already settled" for the current file, confirm the cited artifact (a sheet/file/commit) actually exists in THIS repo via `git log -- <path>` / `find`. If it doesn't, critique the current screen fresh rather than as a backslide.

## 2026-06-18 — Float a plain List's rows as glass cards via `.listRowBackground`, not row content

**Tags:** [api] [layout] [convention]
**Context:** Re-skinning warket-ios's Lists/Assets screens (plain `List` + `NavigationLink` + `swipeActions` + `onMove`) to float glass cards over a mesh. Glass can go two ways: as the row CONTENT, or in `.listRowBackground`. Making it row content forces you to deal with the system `NavigationLink` disclosure chevron (no public API hides it per-row), tempting a fragile custom chevron and hand-rolled navigation.
**Lesson:** To turn a plain List's rows into inset floating glass cards while keeping swipe/`onMove`/the native chevron intact, put the glass in `.listRowBackground(Color.clear.glassSurface(in: shape).padding(.horizontal:).padding(.vertical:))` and push the row content inside it with `.listRowInsets(EdgeInsets(...))` (leading ≈ glass-margin + internal-pad), plus `.listRowSeparator(.hidden)`. The background view's own horizontal padding creates the floating-card margins; the row content stays pure (no chevron handling, `NavigationLink(value:)` preserved). Exact insets can't be verified in `xcodebuild` — flag them for on-device tuning.

## 2026-06-18 — A dark-keyed mesh wants a black scrim veil, not `.ultraThinMaterial`

**Tags:** [motion] [api]
**Context:** Built `MarketPulseBackground` from near-black surface colors in the corners with two muted-teal pools through the middle band — a deliberately low-key, calm mesh. SKILL.md says "always cap with a `.ultraThinMaterial` veil for text contrast," but over an already-dark mesh that veil lightens/milks the colors and washes the teal out.
**Lesson:** The "cap the mesh with `.ultraThinMaterial`" rule assumes a bright/saturated mesh. When the mesh is intentionally dark-keyed (corners near-black, low-saturation pools), veil it with a plain `Color.black.opacity(~0.25)` scrim instead — it darkens for text contrast without milking the hues. Tune the scrim so the phase-0 frame reads as the resting design. Material veils counter lightening-risk (bright) meshes; color scrims counter darkening-risk (dark) ones.

## 2026-06-19 — Audit a redesigned sheet's LAUNCHER (upward), not just its children/siblings

**Tags:** [convention] [anti-pattern]
**Context:** Glass-ifying warket's `AddResourceSheet` (mesh + glass field-card) for cohesion. It's reachable from exactly one place — `AssetEditorSheet`, a stock `Form` that must stay a Form (it carries `onMove`/`onDelete`/`EditButton`, and a mesh can't cleanly back a Form: `.scrollContentBackground(.hidden)` makes rows transparent so an animated mesh sits *behind the input text* — busy/illegible). So retiering the child to glass created a flat-Form→glass parent→child step that can't be resolved in-scope.
**Lesson:** Before retiering a sub-sheet, `grep` its launch sites. The vocabulary audit runs in THREE directions, not two: down (sheets *it* presents — 2026-05-24), sideways (siblings from the same affordance — 2026-06-08), and UP (the surface that presents it). If the launcher is a behavior-carrying `Form` that can't be cleanly skinned, either leave the child matching its parent or explicitly flag the deferred parent rewrite in caveats — don't silently ship a new discontinuity while fixing others.

## 2026-06-19 — When the app already has a strong identity, "redesign" usually means propagate it to orphans

**Tags:** [convention]
**Context:** Asked to "/swiftui-redesign today's new implementations." The app had committed to a bold Liquid-Glass-over-mesh identity two commits earlier; today's web-parity work bolted on new surfaces (a share-entry sheet, a title-fetch field, a detail screen) that all reverted to flat stock `Form`/`surface0`. The "redesign" wasn't "go bolder" — it was closing the cohesion gap at the new touch points.
**Lesson:** When the target app already has an established expressive vocabulary, diagnose new/changed surfaces against THAT vocabulary first — the redesign is often pure propagation (reuse the existing `MarketPulseBackground`/`glassSurface` helpers, the existing gradient-CTA pattern) rather than inventing fresh flash, which would itself become a new inconsistency. The bold move is cohesion. Reserve net-new motion/API additions for the one or two beats that genuinely earn it (here: a gradient CTA on a single-purpose action sheet, `variableColor` on the new fetch button).
