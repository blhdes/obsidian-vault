# Vault instructions (for Claude)

This folder is the user's **Obsidian vault**. When the user asks to "save to the vault", "keep track of this", "write an idea/insight/note", or points to a subfolder here — create or update `.md` files in this directory.

## Rules

1. **Use Markdown** with kebab-case filenames (`swiftdata-migration-gotcha.md`).
2. **Add YAML frontmatter** to every new note:
   ```yaml
   ---
   title: <short title>
   date: YYYY-MM-DD  # today's date
   tags: [<relevant>, <tags>]
   ---
   ```
3. **Pick the right folder** based on PARA:
   - `Inbox/` — quick captures, unclear where they belong yet
   - `Projects/<name>/` — active work with a defined outcome (`Projects/Culla/` exists)
   - `Areas/` — ongoing responsibilities, no deadline
   - `Resources/<topic>/` — reference / learning material (`Resources/Swift/` exists)
   - `Archive/` — finished / inactive
4. **If unsure about the folder**, either drop it in `Inbox/` or ask the user one quick question.
5. **Append vs. create:** if a suitable note already exists for the topic, append a new dated section (`## 2026-04-24`) instead of creating a near-duplicate file.
6. **Link related notes** with `[[wikilinks]]` when relevant.
7. **Don't overwrite** existing notes without reading them first.

## Reading the vault
Feel free to read any `.md` in here to ground answers when the user asks about past notes, ideas, or decisions.
