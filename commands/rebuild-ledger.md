---
name: rebuild-ledger
description: Re-derive .ledger/changes.json from git log when it has drifted, become corrupted, or is missing entries. Atomic write (temp → move) with schema validation. Use when the dashboard shows stale data, status-check reports ledger gaps, or after a force-push / rebase.
---

# /rebuild-ledger

The change ledger at `.ledger/changes.json` is the single source of truth for "what significant work has happened." When it drifts from git history (rebase, force-push, manual edits, missed commits), the dashboard misleads and traceability breaks.

This command rebuilds the ledger from `git log` deterministically and atomically.

## Pre-flight checks (fail fast)

1. Confirm `.ledger/changes.json` exists OR confirm the user explicitly wants a fresh build (ask once if file is absent).
2. Confirm `meta/schemas/ledger.schema.json` exists — refuse to write a ledger we can't validate.
3. Confirm working tree is clean. If dirty, refuse — rebuilding while files are uncommitted produces an inconsistent snapshot. Tell the user to commit or stash first.
4. Confirm we're on a real branch (not detached HEAD).

## Procedure

### Step 1 — Snapshot existing ledger

```bash
cp .ledger/changes.json .ledger/changes.json.bak-$(date -u +%Y%m%dT%H%M%SZ)
```

This is the rollback path if anything goes wrong. Never delete the backup automatically.

### Step 2 — Derive from git log

Use `scripts/ledger-update.py` if it supports a `--from-git-log` (or equivalent rebuild) flag. Check first:

```bash
python3 scripts/ledger-update.py --help
```

If a rebuild flag exists, use it:

```bash
python3 scripts/ledger-update.py --rebuild --output .ledger/changes.json.new
```

If not, fall back to deriving manually:

1. Read `git log --format='%H%n%an%n%ai%n%s%n%b%n---END---'` from the repo's first commit forward.
2. For each commit, parse:
   - `Story:` and `Spec:` trailers (multi-value supported)
   - The `<type>` prefix (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`)
3. Filter: include only `feat` and `fix` by default, plus any commit explicitly carrying a trailer, **unless** the user requests `--include-all`.
4. Generate fresh `CHG-NNNN` IDs in commit-date order, starting at `CHG-0001`.
5. For each entry, set: `id`, `commit_sha`, `author`, `date`, `type`, `summary`, `stories`, `specs`.

### Step 3 — Validate

```bash
python3 scripts/validate-frontmatter.py --schema meta/schemas/ledger.schema.json .ledger/changes.json.new
```

If validation fails, do NOT replace the existing ledger. Report the error and stop. The backup is still in place; nothing is lost.

### Step 4 — Atomic swap

```bash
mv .ledger/changes.json.new .ledger/changes.json
```

`mv` on the same filesystem is atomic on POSIX systems. Either the new ledger replaces the old one entirely or nothing changes — no torn writes.

### Step 5 — Report

Tell the user:
- How many entries the new ledger has vs the old.
- The first new entry's `id`, `summary`.
- The last new entry's `id`, `summary`.
- The path to the backup file.
- Whether any commits were *excluded* (and the count, for sanity).

## Constraints

- **Never delete the `.bak-*` backup automatically.** The user removes it manually after they're satisfied.
- **Never run on a dirty working tree.** Refuse and explain why.
- **Never run on detached HEAD.** Refuse and explain why.
- **Never write directly to `.ledger/changes.json`** — always write to `.new` then `mv`.
- **CHG-NNNN ID stability is not guaranteed across rebuilds.** If a tool elsewhere depends on stable IDs, it must reference `commit_sha` instead. Mention this in the report.

## Failure modes to handle explicitly

| Symptom | Action |
|---|---|
| `git log` empty (new repo) | Write an empty-entries ledger and exit cleanly. |
| Multiple commits with identical timestamps | Order by commit SHA lexicographically as tiebreaker. |
| Trailer present but malformed (e.g., `Story:` with no value) | Skip that trailer with a warning; do not skip the whole commit. |
| `ledger-update.py` missing | Use the manual fallback (Step 2 alternative path). |

## Reuses

- `scripts/ledger-update.py` — primary builder.
- `scripts/validate-frontmatter.py` — schema validation.
- `meta/schemas/ledger.schema.json` — schema authority.

## When this command is invoked

- `/rebuild-ledger` — interactive; asks for confirmation before replacing.
- `/rebuild-ledger --yes` — non-interactive; for CI or scripted recovery.
- `/rebuild-ledger --include-all` — include all commit types, not just `feat`/`fix` + trailered.
