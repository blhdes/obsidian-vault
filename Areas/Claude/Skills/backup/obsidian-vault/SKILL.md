---
name: obsidian-vault
description: Save, update, link, or search notes in the user's personal Obsidian vault at /Users/agomezu/Claude/Obsidian/. Use this skill WHENEVER the user asks to "save to the vault", "keep track of this in Obsidian", "write an idea/insight/learning to the vault", "drop this in the Inbox", "add a note about X to Culla/Swift/...", "what did I write about...", or otherwise refers to their vault, PARA folders (Inbox/Projects/Areas/Resources/Archive), the Culla project notes, or Swift learning notes. Also trigger when the user says "remember this" or "capture this" in a note-taking sense, or when they want to retrieve something they previously saved.
---

# Obsidian Vault

The user keeps a personal Obsidian vault at `/Users/agomezu/Claude/Obsidian/`. This skill is the playbook for writing and reading notes there consistently across any chat session.

## Vault structure (PARA method)

```
/Users/agomezu/Claude/Obsidian/
├── Home.md                    ← index / welcome note
├── CLAUDE.md                  ← vault-local instructions (also respected)
├── Inbox/                     ← quick captures, unclear destination
├── Projects/                  ← active work with a defined outcome
│   └── Culla/                 ← the user's iOS app
│       ├── Culla.md           ← project index
│       ├── Ideas/
│       ├── Dev-Insights/
│       └── Phases/
├── Areas/                     ← ongoing responsibilities (no deadline)
├── Resources/                 ← reference / learning material
│   └── Swift/
│       └── Swift.md           ← Swift learning index
└── Archive/                   ← finished / inactive
```

## How to pick the right folder

Use this decision flow when the user doesn't explicitly name a subfolder:

1. **Is it about an active project with an outcome?** → `Projects/<name>/`
   - Culla iOS app → `Projects/Culla/` (pick `Ideas/`, `Dev-Insights/`, or `Phases/` based on content).
   - A project that doesn't have a folder yet → create `Projects/<kebab-name>/` with an index file.
2. **Is it a topic the user is learning / reference material?** → `Resources/<topic>/`
   - Anything Swift → `Resources/Swift/`.
3. **Is it an ongoing responsibility with no deadline (e.g. fitness routine, home admin)?** → `Areas/<name>/`.
4. **Is it finished / no longer active?** → `Archive/`.
5. **Unsure? Don't guess wrong — drop it in `Inbox/`** so the user can file it later. This is the *correct* default when a note is a quick thought or doesn't cleanly fit.

If genuinely ambiguous between two folders, pick one and mention the choice in one sentence so the user can correct you (don't ask a blocking question for small notes).

## Filename conventions

- **kebab-case**, no spaces: `swiftdata-migration-gotcha.md`, `onboarding-flow-idea.md`
- No dates in the filename — the date lives in frontmatter. Exception: daily notes (`2026-04-24.md`) when clearly a journal entry.
- Short, specific, searchable. Aim for <5 words.

## Frontmatter template

Every new note starts with this YAML block:

```yaml
---
title: Short descriptive title
date: YYYY-MM-DD            # today's date
tags: [topic, folder-hint]  # e.g. [swift, swiftui] or [culla, idea]
---
```

Pull today's date from the conversation context (the system provides `currentDate`). If unknown, run `date +%Y-%m-%d`.

## Append vs. create

Before creating a brand-new file, check whether a suitable note already exists on the topic:

- **Similar index note exists** (e.g. `Resources/Swift/swiftui.md` when the user asks about a SwiftUI modifier) → **append** a new dated section rather than making a near-duplicate file:
  ```markdown
  ## 2026-04-24 — [short section title]

  <new content>
  ```
- **No close match** → create a new file.

Rule of thumb: a topic index gets sections appended; a specific "thing that happened" (a bug, an idea, a phase) gets its own file.

## Linking

Use Obsidian `[[wikilinks]]` to connect related notes. Prefer folder-relative names when the note exists in a different folder:

```markdown
See [[Projects/Culla/Culla|Culla]] for context.
Related: [[Resources/Swift/swiftui]]
```

## Worked examples

**Example 1 — idea about Culla**
> User: *"Save this idea to the vault — a weekly color-of-the-week feature where Culla picks a new palette every Monday"*

Action:
1. Folder: `Projects/Culla/Ideas/` (explicit).
2. Filename: `color-of-the-week.md`.
3. Create file with frontmatter (`tags: [culla, idea, feature]`) + the idea body.

**Example 2 — Swift learning**
> User: *"I just learned why `@Observable` replaces `ObservableObject` in iOS 17+. Keep track of this."*

Action:
1. Folder: `Resources/Swift/`.
2. Check if `swiftui.md` exists → if yes, **append** a new `## 2026-04-24 — @Observable vs ObservableObject` section. If no, create `observable-macro.md`.

**Example 3 — vague capture**
> User: *"Quick — remember that the CMYK-to-RGB conversion in Pillow sometimes drifts on dark blues."*

Action:
1. Folder: `Inbox/` (not clearly Culla-specific, not a learning topic index).
2. Filename: `cmyk-rgb-dark-blue-drift.md`.
3. One-line mention in your reply: *"Dropped in Inbox — move to Projects/Culla/Dev-Insights/ if it's Culla-related."*

**Example 4 — retrieval**
> User: *"What did I write about SwiftData migrations?"*

Action:
1. Search the vault: `grep -rli "swiftdata" /Users/agomezu/Claude/Obsidian/` (or use Glob/Grep tools).
2. Read matching files, summarize findings, cite paths with line numbers.

## Dos and don'ts

**Do**
- Keep notes concise and scannable. The user is a beginner programmer — favor plain language and examples.
- Use code blocks with language tags (` ```swift `) for snippets.
- Add `#tags` inline or in frontmatter to make things searchable.
- Tell the user in one line where the note was saved: *"Saved to `Projects/Culla/Ideas/color-of-the-week.md`."*

**Don't**
- Don't overwrite an existing note without reading it first.
- Don't create folders speculatively. Only add a new `Projects/<name>/` or `Resources/<topic>/` folder when the user's note actually needs one.
- Don't leave files without frontmatter — future-you and Obsidian rely on it for search/tags.
- Don't bury the note location in a long reply. Keep confirmations short.

## When the user asks to find something

Use `Grep` / `Glob` on `/Users/agomezu/Claude/Obsidian/` rather than relying on memory. The vault is the source of truth for what's been captured.
