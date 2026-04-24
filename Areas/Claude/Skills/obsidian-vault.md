---
title: obsidian-vault skill
date: 2026-04-24
tags: [claude, skill, obsidian, meta]
---

# 🧩 `obsidian-vault` skill

A **personal Claude skill** that teaches any Claude agent — in any chat — how to read and write into this very vault consistently. Created on 2026-04-24.

## Where it lives

```
/Users/agomezu/.claude/skills/obsidian-vault/SKILL.md
```

Because it sits under `~/.claude/skills/`, it's **user-global** — every Claude Code session on this machine can see and trigger it automatically, regardless of the working directory.

## How it's configured

A skill is just a folder with a `SKILL.md` file. The top of `SKILL.md` has YAML frontmatter that tells Claude **when** to fire the skill and **what** it does:

```yaml
---
name: obsidian-vault
description: Save, update, link, or search notes in the user's personal Obsidian vault... (trigger phrases here)
---
```

Everything below the frontmatter is the **playbook** Claude follows once the skill fires — folder map, naming conventions, frontmatter template, append-vs-create rules, examples.

No extra setup, no plugin install. Claude auto-discovers anything under `~/.claude/skills/`.

## How to use it

Just talk naturally. The skill's description watches for phrases like:

| You say… | Skill does… |
|---|---|
| *"save this idea to the vault"* | Creates a `.md` file in the right PARA folder |
| *"keep track of this in Obsidian"* | Same, with a sensible folder guess |
| *"drop this in the Inbox"* | Writes to `Inbox/` for later triage |
| *"add a dev-insight to Culla about X"* | Creates file in `Projects/Culla/Dev-Insights/` |
| *"new Swift note about async/await"* | Creates (or appends to) a note in `Resources/Swift/` |
| *"what did I write about SwiftData?"* | Greps the vault and summarizes matches |
| *"remember this…"* / *"capture this…"* | Picks a folder + creates the note |

You can also be **explicit** about the path — *"save this to `Projects/Culla/Phases/beta-release.md`"* — and the skill will honor it exactly.

## What the skill enforces

Every note it creates will have:

1. **kebab-case filename** (`my-new-idea.md`)
2. **YAML frontmatter** with `title`, `date` (today's date), `tags`
3. **A one-line confirmation reply** like *"Saved to `Projects/Culla/Ideas/color-of-the-week.md`."*

It also follows an **append-vs-create** rule: if a suitable topic-index note already exists (e.g. `Resources/Swift/swiftui.md`), it appends a new `## YYYY-MM-DD — section title` block instead of making a near-duplicate file.

## How to edit or extend

- **Change behavior / conventions** → edit `/Users/agomezu/.claude/skills/obsidian-vault/SKILL.md` directly.
- **Add more project folders** (e.g. a new app under `Projects/`) → no skill change needed; the skill already handles "create a new project folder" on demand.
- **Turn it off for one chat** → say *"don't use the obsidian-vault skill"*; Claude will skip it for that session.
- **Create a sibling skill** → make a new folder `~/.claude/skills/<name>/` with its own `SKILL.md`. Same pattern.

## Syncing & multi-device access

The vault is a **private GitHub repo** (set up 2026-04-24) cloned at `/Users/agomezu/Claude/Obsidian/`.

**Desktop workflow (current):**
- Use the **Obsidian Git** community plugin → auto-pulls on open, auto-commits/pushes every N minutes.
- Or manual: `git add . && git commit -m "notes" && git push` from the vault folder.

**Mobile is NOT set up yet.** If added later, the tradeoffs are:

| Option | Cost | Friction | Merge conflicts? |
|---|---|---|---|
| **Git on iOS** (Working Copy app) | ~$20 one-time | Manual pull/push; no background sync | Yes if you edit same note on 2 devices unsynced |
| **Obsidian Sync** (official) | ~$4–8/month | Zero — real-time background sync | Rare, handled silently |
| **iCloud Drive** | Free | Auto-sync but no version history | Last-writer-wins, can lose edits |

**Recommendation when you want mobile**: if you edit often from phone → Obsidian Sync. If phone is read-mostly + occasional edits → Working Copy + Git. Skip iCloud Drive (no history, the whole point of the repo would be lost).

## Related notes

- [[Home]] — vault entry point & conventions
- [[Projects/Culla/Culla]]
- [[Resources/Swift/Swift]]
