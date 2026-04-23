# Changelog

All notable changes to GitSpec are documented in this file. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-04-23

### BREAKING
- **Project renamed from Build.MD → GitSpec.** GitHub repository moved from `Jimthetaxguy/build-md` to `Jimthetaxguy/gitspec` (GitHub auto-redirects the old URL). The kebab-case identifier is now `gitspec`. Display name is `GitSpec`. Install receipt filename is `.gitspec-install-receipt.txt`. Existing v1.x installs continue to work — this is a name change, not an API change. Re-clone from the new URL when convenient.

### Added
- `/onboard-agent` — slash command. Brings a fresh agent session up to speed in a GitSpec-equipped repo. Reads rule blocks, AGENTS.md, current backlog, and principles, then returns a compact orientation briefing. Solves the cold-start problem for agents joining mid-project.
- `/rebuild-ledger` — slash command. Re-derives `.ledger/changes.json` from `git log` when it has drifted (after rebase, force-push, manual edits, or corruption). Atomic write with schema validation; never destroys the existing ledger without backup.
- **Global skill at `~/.claude/skills/gitspec/`** — invoke `/gitspec` from any Claude Code session to learn what GitSpec is, get install instructions, or see the architecture, without needing a target repo.

### Changed
- All 142 internal references updated from `Build.MD` → `GitSpec` (109 brand) and `build-md` → `gitspec` (33 identifier).
- `README.md` and `SKILL.md` slash-commands tables updated to include the two new commands.

### Migration
For users on v1.1.0:
- The old GitHub URL still works (auto-redirects).
- Existing installed projects continue to function — the receipt filename does not affect runtime behavior.
- To install fresh: `git clone https://github.com/Jimthetaxguy/gitspec.git`.

## [Unreleased]

### Added
- `SECURITY.md` — intentional-behavior statements and audit checklist (no SLA; explicit no-guarantee-of-response).
- `CONTRIBUTING.md` — contribution workflow and commit style (explicit skills-pack framing, no maintenance commitment).
- `CHANGELOG.md` — this file.
- `ci/smoke.sh` — end-to-end install smoke test (clones into temp dir, runs `--dry-run`, runs real install, asserts expected tree).
- `.github/workflows/ci.yml` — runs `shellcheck` on shell scripts and `ci/smoke.sh` on every push and PR.
- `.github/ISSUE_TEMPLATE/` — bug report and feature request templates.
- `.github/pull_request_template.md` — PR template with checklist.
- Attribution and disclaimer section in `principles/PRINCIPLES.md` clarifying that source citations indicate inspiration, not endorsement or authorship, and that all trademarks belong to their respective owners.

### Changed
- `SKILL.md` install instructions updated to the clone-first pattern (removed placeholder `org/gitspec` URLs and the unsupported `curl | bash` and `degit` options).
- `README.md` "Project Status" reframed as a released skills pack (no maintenance commitment).
- `scripts/install.sh` hardened:
  - Refuses to run via `curl | bash` (requires a local clone so it can copy templates).
  - Detects non-TTY stdin and requires `--yes` for non-interactive runs.
  - New `--dry-run` flag prints the full action plan without touching the filesystem.
  - New `--no-hooks` flag for CI environments that shouldn't install Git hooks.
  - Validates the source tree for required subdirectories before proceeding.
  - Validates the target directory exists before `cd`-ing into it.
  - Writes a receipt to `<target>/.gitspec-install-receipt.txt` on every real install.
  - Fixes bash precedence ambiguity in agent detection (`[ -f ] || [ -d ] && ...`) with explicit `{ ...; }` grouping.
- `README.md` clarified:
  - Install section points to `git clone` + `./scripts/install.sh` (the only supported install path) instead of `curl | bash`.
  - Added Requirements, What It Does Not Do, and Troubleshooting sections.
  - Added direct links to `SECURITY.md` and `CONTRIBUTING.md`.

### Removed
- Untracked `.DS_Store` files scrubbed from the working tree (already in `.gitignore`, never committed).
- Stale `scripts/__pycache__/` removed from the working tree (already in `.gitignore`).

## [1.1.0] — 2026-04-23

### Added
- Five slash commands for Claude Code and compatible agents:
  - `/new-story "title"` — scaffold a story with auto-incremented ID.
  - `/new-spec "domain" "title"` — scaffold a spec with domain-scoped ID.
  - `/distill STORY-NNN` — synthesize raw notes into an ADR.
  - `/status-check` — health check (orphaned TODOs, missing trailers, stale stories).
  - `/pr-prep` — distill notes, generate PR description, validate trailers.
- VS Code platform adapter (`templates/adapters/vscode-instructions.md.template`).
- `README.md` with public-facing positioning and quick-start.
- `LICENSE` (MIT).

### Changed
- `SKILL.md` references the new slash commands.

## [1.0.0] — 2026-04-22

### Added
- Initial nine-layer architecture: dual config targets, init skill, multi-agent contributor model, appended rules, change ledger, docs + Git as visualization backend, spec and code traceability, HTML Kanban, report generation.
- Platform adapters for Claude Code, Cursor (`.mdc`), GitHub Copilot.
- `AGENTS.md` template with YAML frontmatter schema.
- Git hook templates (`commit-msg`, `pre-push`).
- Rule blocks (`templates/rules/01-stories.md` through `07-annotations.md`).
- Schemas (`story.schema.json`, `spec.schema.json`, `ledger.schema.json`, `rnpm-status.schema.json`).
- Helper scripts: `build-graph.py`, `ledger-update.py`, `validate-frontmatter.py`, `generate-report.py`, `refresh-principles.py`, `serve.py`.
- Local dashboard (`applets/dashboard.html`).
- Curated principles file (`principles/PRINCIPLES.md`) — 24 entries from 17 organizations.
