---
title: Claude skills — index
date: 2026-05-22
tags: [claude, skill, meta, reference, index]
---

# 🧩 Claude skills on this Mac

Every Claude skill currently visible in a Claude Code session on this machine, grouped by source. Built-in skills come from Anthropic and don't need detailed notes here (their playbooks are upstream). User-created skills get their own note so personal context isn't lost.

## TL;DR — where skills live

| Source | Path | Visible? |
|---|---|---|
| **User-created** | `~/.claude/skills/<name>/SKILL.md` | Every session, every project |
| **Custom slash commands** | `~/.claude/commands/<name>.md` | Every session, every project |
| **Plugins** (marketplace) | `~/.claude/plugins/cache/<marketplace>/<name>/` | Every session |
| **Built-in** | Bundled with Claude Code itself | Every session |

See [[claude-config-files]] for the full config layering.

---

## 👤 User-created skills

Skills the user built or heavily customized. These have their own notes because they encode personal workflow.

| Skill | Note | Trigger | What it does |
|---|---|---|---|
| `obsidian-vault` | [[obsidian-vault]] | "save to vault", "drop in Inbox", "what did I write about…" | Reads/writes notes in `/Users/agomezu/Claude/Obsidian/` following PARA conventions |
| `swift-refine` | [[swift-refine]] | `/swift-refine`, "tighten", "optimize this view" | Audits a Swift/SwiftUI file for performance, allocations, races, dead branches. Plan-then-implement |
| `swiftui-redesign` | [[swiftui-redesign]] | `/swiftui-redesign`, "rethink", "modernize this view" | Redesigns a SwiftUI screen using modern Apple APIs (Liquid Glass, MeshGradient, symbolEffect) |
| `download-music` | [[download-music]] | `/download-music <YouTube URL>` | Downloads from YouTube via `yt-dlp`, embeds album art via `embed_cover.py` (MusicBrainz → iTunes → YT thumbnail) |

---

## 🏠 Built-in Claude Code skills

These ship with Claude Code itself. Treated as a reference — no need to document the implementation, but useful to know they exist.

| Skill | Trigger | What it does |
|---|---|---|
| `init` | `/init` | Creates a `CLAUDE.md` for the current project with codebase docs |
| `review` | `/review` | Reviews a pull request |
| `code-review` | `/code-review`, `--comment` | Reviews the current diff for correctness bugs. Effort levels: low/medium/high/max. `--comment` posts findings as inline PR comments |
| `security-review` | `/security-review` | Security review of pending changes on the current branch |
| `verify` | "verify this PR works", "test the change manually" | Runs the app and observes behavior to confirm a code change actually does what it should |
| `run` | "run the app", "start it", "screenshot it" | Launches the project's app (CLI, server, TUI, Electron, browser). Looks for a project skill first; otherwise falls back to built-in patterns |
| `loop` | `/loop 5m /foo`, "check the deploy every 5 minutes" | Runs a prompt or slash command on a recurring interval. Omit the interval for self-paced loops |
| `schedule` | `/schedule`, "run this at 3pm tomorrow" | Create/update/list/run remote agents on a cron schedule (one-time or recurring) |
| `update-config` | "allow npm", "set DEBUG=true", "when claude stops show X" | Configures `~/.claude/settings.json` (permissions, env vars, hooks). Hooks are the only way to enforce automated behaviors |
| `keybindings-help` | "rebind ctrl+s", "add a chord shortcut" | Modifies `~/.claude/keybindings.json` |
| `fewer-permission-prompts` | "reduce permission prompts" | Scans recent transcripts for common read-only Bash/MCP tool calls and adds them to project `.claude/settings.json` allowlist |
| `claude-api` | Imports of `anthropic` SDK, "build a Claude API app", model migrations | Builds/debugs/optimizes Claude API & Anthropic SDK apps with prompt caching. Also migrates between Claude versions |

---

## 🧩 Plugin skills

Installed from `claude-plugins-official` marketplace. Cached at `~/.claude/plugins/cache/claude-plugins-official/<name>/`.

| Skill | Trigger | What it does |
|---|---|---|
| `frontend-design:frontend-design` | "build a landing page", "design a frontend" | Generates distinctive, production-grade frontend interfaces. Avoids generic AI aesthetics |

Other plugins installed but not surfaced as user-invocable skills: `swift-lsp` (LSP server bridge for Swift work).

---

## How to add a new skill

A skill is just a folder under `~/.claude/skills/<name>/` with a `SKILL.md` inside. The frontmatter `description:` is what Claude reads to decide *when* to trigger. Everything below the frontmatter is the playbook Claude follows once triggered.

Two flavors that come up often:

- **Auto-fire on trigger phrases** (like `obsidian-vault`) — description lists natural-language phrases; Claude detects them and runs the skill without needing `/<name>`.
- **Explicit-invocation only** (like `swift-refine`, `swiftui-redesign`) — description states "Explicit-invocation only — use when the user types `/<name>`". Claude won't fire automatically.

A skill can also be implemented as a **slash command** (`~/.claude/commands/<name>.md`) instead of a `SKILL.md`. The command file gets loaded into the conversation verbatim when the user types `/<name>`. `download-music` works this way.

## Related notes

- [[claude-config-files]] — full Claude config file map
- [[obsidian-vault]] — the meta-skill that wrote this very note
- [[Home]]
