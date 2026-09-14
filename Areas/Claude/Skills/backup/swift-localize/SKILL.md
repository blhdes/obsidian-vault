---
name: swift-localize
description: Localize a Swift/SwiftUI app into multiple languages using String Catalogs (.xcstrings). Use when the user types /swift-localize or asks to "add languages", "translate the app", "localize", or "add localization" to an iOS/macOS project. Covers extraction, fixing strings invisible to the compiler, translation, Info.plist permission prompts, and an in-app language shortcut.
---

# Swift App Localization via String Catalogs

Localize the current Xcode project end-to-end. Default language set (confirm with the user, AskUserQuestion with multiSelect): **es, de, fr, it, ja, pt-BR, zh-Hans** on an **en** source. Claude writes the translations itself — no external service.

## Phase 0 — Audit

1. `find . -name "*.xcstrings" -o -name "*.strings"` — does localization already exist?
2. Check `project.pbxproj` for `knownRegions`, `SWIFT_EMIT_LOC_STRINGS`, `LOCALIZATION_PREFERS_STRING_CATALOGS`, and `INFOPLIST_KEY_NS*UsageDescription` (permission texts often live in build settings, not Info.plist).
3. Check for `PBXFileSystemSynchronizedRootGroup` (Xcode 16+ synced folders). If present, new files dropped into the source folder are auto-included — no pbxproj file-reference surgery needed.

## Phase 1 — Extract

1. Create an empty catalog at `<AppFolder>/Localizable.xcstrings`:
   ```json
   { "sourceLanguage" : "en", "strings" : { }, "version" : "1.0" }
   ```
2. **Do NOT rely on a regular `xcodebuild build` to populate it** — that sync only happens inside the Xcode IDE. From the CLI use:
   ```
   xcodebuild -exportLocalizations -localizationPath /tmp/loc -scheme <Scheme>
   ```
   This **also syncs the source catalog in place** (and generates an InfoPlist.xcstrings inside the .xcloc you can crib from).
3. Dump the key list with python/json and count.

## Phase 2 — Fix invisible strings

`Text("literal")` is auto-extracted (LocalizedStringKey). Everything flowing through plain `String` is NOT. Hunt for:

- **Custom components with `String` title/label params** (buttons, cards, toggle rows, tooltips): change the param type to `LocalizedStringKey`. Call-site literals — including interpolated ones like `"Delete (\(count))"` — then extract automatically as `Delete (%lld)`.
  - Only do this when all call sites pass literals. A call site passing a dynamic value (gallery/user names) must keep `String` — wrap the *literal* call sites in `String(localized:)` instead.
- **Computed `String` properties / functions returning copy** (button titles, toast messages, tour copy): wrap each literal in `String(localized: "...")` — also extracted by the compiler.
- **Ternaries**: `Text(flag ? "Done!" : someString)` infers `String`, killing extraction — wrap the literal: `flag ? String(localized: "Done!") : someString`.
- **Enums whose `rawValue` doubles as display text**: NEVER translate the raw value (it may be persisted / used as an identifier). Add a separate `var displayName: LocalizedStringKey` and switch `Text(option.rawValue)` → `Text(option.displayName)`. Files that aren't SwiftUI need `import SwiftUI` for `LocalizedStringKey`.
- **UNMutableNotificationContent** title/body, `NSError` userInfo descriptions, alert message strings: `String(localized:)`.
- `#Preview` bodies are not extracted — ignore them.

Verify: re-run `-exportLocalizations` and probe that the new keys appeared in the catalog.

## Phase 3 — Translate

Write a python script (`/tmp/translate.py`) holding a dict `key -> (es, de, fr, it, ja, pt-BR, zh-Hans)` and merge into the catalog JSON:

- Entry shape: `"localizations": { "<lang>": { "stringUnit": { "state": "translated", "value": "..." } } }`.
- Brand names, the app name, and bare symbols (`·`, `—`, `%lld`) get `"shouldTranslate": false` instead of translations.
- Keys with **2+ format args** must use positional specifiers in every translation (`%1$lld`, `%2$@`) so word order can change safely. The export already rewrites the `en` value this way.
- Validate before writing: every catalog key covered, no extra keys; fail loudly otherwise.
- `json.dump(..., ensure_ascii=False, indent=2)`.
- Translation tone: match Apple platform conventions per language (de informal *du*, fr *vous*, es *tú*; use each locale's standard terms for Settings/Done/Undo etc.).

## Phase 4 — System surfaces

1. **`InfoPlist.xcstrings`** next to the catalog: translate `NSPhotoLibraryUsageDescription` & friends (keys work even when the values come from `INFOPLIST_KEY_*` build settings). `CFBundleDisplayName` → `shouldTranslate: false`.
2. **`knownRegions`** in `project.pbxproj`: append the language codes (quote `"pt-BR"`, `"zh-Hans"`).

## Phase 5 — Verify

1. `xcodebuild ... CODE_SIGNING_ALLOWED=NO build` → must succeed.
2. Check the built product contains one `<lang>.lproj` per language.
3. Per-language key counts in the catalog should match (total − shouldTranslate-false).
4. Build only — never launch the simulator; the user tests on a physical device (Settings → Apps → \<App> → Language switches just that app).

## Optional — In-app language row

Don't build a custom picker. Add a Settings row that deep-links to the system per-app language page (appears automatically once ≥2 localizations ship; changing it relaunches the app):

```swift
guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
UIApplication.shared.open(url)
```

Remember to add the row's strings to the catalog with translations.
