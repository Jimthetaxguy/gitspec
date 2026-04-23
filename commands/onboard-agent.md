---
name: onboard-agent
description: Bring a fresh agent session up to speed in a GitSpec-equipped repo — reads rule blocks, AGENTS.md, current backlog, and principles; returns a compact orientation briefing. Use at the start of any session in a repo that has GitSpec installed.
---

# /onboard-agent

You are joining a repository that uses GitSpec for project management. Your job in this turn is to read the local conventions and produce a short orientation briefing — not to start working on stories yet.

## What to read (in this order, parallel where possible)

1. **`AGENTS.md`** at the repo root — the canonical contract.
2. **`.agents/rules/*.md`** — every file. These are the appended rule blocks (typically `01-stories.md` through `07-annotations.md`). Read all of them.
3. **`.agents/PRINCIPLES.md`** — the principles catalog. Skim, don't memorize.
4. **`docs/specs/`** — list filenames only. Count them.
5. **`docs/stories/`** — list filenames; identify any story currently in `in_progress` status (read the frontmatter to check).
6. **`docs/stories/archive/`** — list filenames only. Count them.
7. **`docs/decisions/`** — list filenames; read titles only.
8. **`.ledger/changes.json`** — read it; report `entries.length` and the last entry's `id` and `summary`.

## What to NOT read

- Source code (until you have a specific task)
- `docs/notes/` (working notes are noisy; only read if a specific story references them)
- `docs/reports/` (historical, not current state)

## What to produce — a briefing in this exact format

```
## GitSpec Orientation Briefing

**Project:** {name from AGENTS.md or repo dir name}
**Enforcement level:** {gentle | standard | strict — from AGENTS.md}
**Current backlog:** {N specs, M stories (P in_progress, Q ready, R blocked), S archived}
**Last ledger entry:** CHG-NNNN — {summary} ({date})

### Conventions you must follow in this repo
- {3-7 bullets — the *non-default* rules from .agents/rules/, e.g. "commits of type feat/fix MUST include a Story: trailer"}

### Active work
- {1-3 bullets — any story currently in_progress, with its STORY-ID and one-line goal}
- {if none: "No story currently in progress. Pick from `ready` or ask the user."}

### Recent decisions worth knowing
- {1-3 bullets — most recent ADRs from docs/decisions/ by filename date, title only}

### What I will NOT do without asking
- {2-3 bullets — based on rule blocks: e.g., "I will not delete files in docs/stories/archive/", "I will not amend commits that have a Story: trailer"}
```

## Constraints

- Keep the briefing under 400 words.
- Do not make recommendations or start work — orient only.
- If `AGENTS.md` is missing or stub-only, say so and stop. Do not invent conventions.
- If `.agents/rules/` is missing, the repo is not GitSpec-installed — say so and stop.

## Reuses

- `scripts/validate-frontmatter.py` — to safely parse story/spec frontmatter without LLM hallucination.
- `scripts/build-graph.py` — only if the briefing needs to mention spec→code coverage (typically not on first onboard).

## When this command is invoked

`/onboard-agent` (no arguments) — operates on the current working directory's repo.

`/onboard-agent --verbose` — also include the full list of specs and stories (capped at 20 each).
