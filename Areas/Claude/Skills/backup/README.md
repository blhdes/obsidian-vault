---
title: Claude skills — file backup
date: 2026-09-14
tags: [claude, skill, backup, meta]
---

# 📦 Claude skills backup

A raw copy of every custom Claude Code skill set up on this Mac, as of **2026-09-16**. This exists so the skills survive a machine wipe/migration and so they can be **shared** (a folder to zip and hand over, or push to a public repo later) without exposing personal secrets or library data.

Each subfolder here mirrors a folder under `~/.claude/` on this Mac. The prose explaining *what each skill does and how to use it* lives in the sibling `Docs/` folder — see [[../_index|the skills index]] and each skill's own note (linked below) — this folder is just the files.

## What's backed up

| Folder here | Source on this Mac | Type |
|---|---|---|
| `career-launch/` | `~/.claude/skills/career-launch/` | Skill (auto-fire) |
| `download-music/` | `~/.claude/commands/download-music.md` + `~/.claude/skills/download-music/*.py` | Slash command + scripts |
| `glassify/` | `~/.claude/skills/glassify/` | Skill (explicit `/glassify`) |
| `music-production/` | `~/.claude/skills/music-production/` | Skill (auto-fire) |
| `obsidian-vault/` | `~/.claude/skills/obsidian-vault/` | Skill (auto-fire) |
| `swift-localize/` | `~/.claude/skills/swift-localize/` | Skill (explicit `/swift-localize`) |
| `swift-refine/` | `~/.claude/skills/swift-refine/` | Skill (explicit `/swift-refine`) |
| `swiftui-redesign/` | `~/.claude/skills/swiftui-redesign/` | Skill (explicit `/swiftui-redesign`) |
| `tunebat/` | `~/.claude/skills/tunebat/` | Skill (auto-fire) + scripts |

## Deliberately excluded (don't add these back)

This backup is meant to be shareable, so personal secrets and runtime state were left out on purpose:

| File | Why excluded |
|---|---|
| `download-music/.discogs_token` | Discogs personal access token — a secret |
| `download-music/.cover_options.json` | Cache of cover-art picks tied to this Mac's `~/Soulseek Downloads/` paths |
| `download-music/queue.md` | The live download queue/history — personal, changes constantly |
| `download-music/.engine_sync_ignore` | Personal list of this user's deliberately-excluded library folders |
| `*/__pycache__/` | Compiled bytecode, not source |

If restoring this backup onto a new Mac, `download-music` still works without `.discogs_token` — the Discogs cover/genre step just gets silently skipped until you generate a new token (see [[../Docs/download-music|download-music]] → "One-time setup: Discogs token").

## Restoring onto a Mac

```bash
# Skills (all except download-music)
for s in career-launch glassify music-production obsidian-vault swift-localize swift-refine swiftui-redesign tunebat; do
  mkdir -p ~/.claude/skills/$s
  cp backup/$s/* ~/.claude/skills/$s/
done

# download-music is a slash command + a scripts folder
cp backup/download-music/download-music.md ~/.claude/commands/download-music.md
mkdir -p ~/.claude/skills/download-music
cp backup/download-music/scripts/*.py ~/.claude/skills/download-music/
```

Then, only for `download-music`, redo the one-time Discogs token setup (see above) and install its dependencies (`yt-dlp`, `ffmpeg`, `mutagen`, `requests`, `Pillow` — see [[../Docs/download-music|download-music]]).

## Keeping this in sync

This backup is a **snapshot**, not a live mirror — it does not auto-update when a `SKILL.md` changes on this Mac. Re-copy the relevant file here (and bump the date above) whenever a skill is meaningfully edited. The per-skill vault notes below are the place to log *why* something changed; this folder just needs the current file.

## Per-skill documentation

All in the sibling `Docs/` folder:

- [[../Docs/career-launch|career-launch]]
- [[../Docs/download-music|download-music]]
- [[../Docs/glassify|glassify]]
- [[../Docs/music-production|music-production]]
- [[../Docs/obsidian-vault|obsidian-vault]]
- [[../Docs/swift-localize|swift-localize]]
- [[../Docs/swift-refine|swift-refine]]
- [[../Docs/swiftui-redesign|swiftui-redesign]]
- [[../Docs/tunebat|tunebat]]

## Related notes

- [[../_index|_index]] — Claude skills index
- [[../../claude-config-files|claude-config-files]]
