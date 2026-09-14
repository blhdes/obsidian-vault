---
title: swift-localize skill
date: 2026-09-14
tags: [claude, skill, swift, localization, i18n]
---

# 🌍 `swift-localize` skill

Localizes a Swift/SwiftUI app end-to-end via String Catalogs (`.xcstrings`). Default language set (confirmed with the user first): **es, de, fr, it, ja, pt-BR, zh-Hans** on an **en** source — Claude writes the translations itself, no external translation service.

## Where it lives

```
~/.claude/skills/swift-localize/SKILL.md
```

## How to invoke

**Explicit invocation** — type `/swift-localize`, or ask to "add languages", "translate the app", "localize", or "add localization" to an iOS/macOS project.

## The phases

1. **Audit** — checks for an existing `.xcstrings`/`.strings`, reads `project.pbxproj` for `knownRegions` and localization build settings, checks for Xcode 16+ synced folders (no manual file-reference surgery needed there).
2. **Extract** — creates an empty catalog, then runs `xcodebuild -exportLocalizations` (never a plain `xcodebuild build` — that Xcode-IDE-only sync doesn't populate the catalog from the CLI) to populate keys and sync the source catalog in place.
3. **Fix invisible strings** — hunts for copy that the compiler doesn't auto-extract: custom-component `String` params (→ `LocalizedStringKey`), computed `String` properties/functions (→ `String(localized:)`), ternaries that infer `String`, enum `rawValue`s doubling as display text (→ a separate `displayName: LocalizedStringKey`), and system-facing strings (notification content, `NSError`, alerts).
4. **Translate** — writes translations directly into the catalog JSON; brand names and bare symbols get `shouldTranslate: false`; multi-arg format keys get positional specifiers (`%1$lld`) so word order can vary safely per language; validates full key coverage before writing.
5. **System surfaces** — translates `InfoPlist.xcstrings` (permission usage descriptions) and appends new language codes to `knownRegions` in `project.pbxproj`.
6. **Verify** — confirms the build still compiles and the new locales show up.

## When NOT to use it

- The app already has full, correct localization and you just want to add one missing string → do it directly, invoking the whole skill is overkill.
- Non-Apple-platform localization (web, Android) → this skill is String-Catalog-specific.

## Backup

`SKILL.md` is mirrored at [[backup/README|Areas/Claude/Skills/backup/swift-localize/]], last synced **2026-09-14**. Re-copy it there after any real change to this skill.

## Related notes

- [[swift-refine]] — inward Swift audits (not localization)
- [[swiftui-redesign]] — visual redesigns (not localization)
- [[_index]] — Claude skills index
- [[Resources/Swift/Swift]]
