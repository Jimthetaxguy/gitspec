# Build.MD Audit Summary

**Date:** 2026-04-23  
**Auditor:** Claude  
**Status:** Complete ✓

---

## Issues Found & Fixed

### 1. Naming Inconsistencies ✓

**Problem:** Project referenced as "Build.MD", "build-md", and "rnpm" inconsistently.

**Fixes:**
- **`principles/PRINCIPLES.md` (U-009):** Changed `rnpm new-story` → `build-md new-story` (line 94)
- **Result:** All references now consistently use "Build.MD" (formal name) or "build-md" (CLI command)

### 2. Redundant Cursor Adapter Templates ✓

**Problem:** Both old and new Cursor adapter formats exist:
- `cursorrules.template` (deprecated .cursorrules format)
- `cursor-core.mdc.template` + `cursor-stories.mdc.template` (modern .mdc format)

**Fixes:**
- Moved `templates/adapters/cursorrules.template` → `templates/adapters/cursorrules.template.deprecated`
- Kept modern `.mdc` format (`cursor-core.mdc.template` and `cursor-stories.mdc.template`)
- **Reasoning:** The .mdc format is the modern Cursor standard (supports YAML frontmatter: `description`, `alwaysApply`, `globs`)

### 3. AGENTS.md vs Codex Template Redundancy ✓

**Problem:** `codex.md.template` was a near-duplicate of `AGENTS.md.template`. Since Codex reads `AGENTS.md` natively, the separate template was redundant.

**Fixes:**
- Moved `templates/adapters/codex.md.template` → `templates/adapters/codex.md.template.deprecated`
- Updated `SKILL.md` to clarify that Codex uses `AGENTS.md` natively (no separate adapter needed)
- **Result:** Single source of truth for all agents; platform adapters only exist for tools that need them

### 4. Ledger Update Script Bug ✓

**Problem:** `ledger-update.py` referenced `trailers.get("storys")` instead of `trailers.get("stories")` (typo in plural form).

**Fixes:**
- Line 78: `trailers.get("storys", [])` → `trailers.get("stories", [])`
- Line 133: `trailers.get("storys", [])` → `trailers.get("stories", [])`
- **Impact:** Conditional commit detection for test commits now works correctly

### 5. Missing Files Created ✓

**Problem:** SKILL.md and other docs referenced files that didn't exist yet.

**Created:**

**Schemas:**
- `templates/schemas/ledger.schema.json` — JSON Schema for `.ledger/changes.json`
- `templates/schemas/spec-template.md` — Markdown template for new spec files
- `templates/schemas/story-template.md` — Markdown template for new story files
- `templates/schemas/adr-template.md` — Markdown template for Architecture Decision Records

**Scripts:**
- `scripts/serve.py` — Local HTTP server for dashboard (serves on localhost:3456)
- `scripts/validate-frontmatter.py` — YAML frontmatter validator for specs/stories
- `scripts/generate-report.py` — Change report generator (markdown output)

**Applets:**
- `applets/dashboard.html` — Self-contained Kanban board + timeline dashboard (reads from `/api/manifest` and `/api/ledger`)

**Result:** All referenced files now exist; skill is self-consistent

### 6. Install Script Refinement ✓

**Problem:** Principles directory path was incorrect in install.sh.

**Fix:**
- `scripts/install.sh` line 91: Fixed principles copy to place directly in `.agents/` instead of `.agents/principles/`

### 7. Principles Catalog Review ✓

**Checked:** All 24 principles for vagueness and overlap.

**Findings:**
- **U-002 & U-003:** Adjacent but distinct. U-002 (iteration velocity) focuses on vertical slicing; U-003 (developer velocity) focuses on PM layer friction. Both valid, complementary.
- All other principles are clearly scoped by domain (agent-design, workflow-design, security, research, rapid-prototyping)
- No vague language found
- **Result:** No changes needed; language is crisp

### 8. Commit Hook Quality ✓

**Review:** `templates/hooks/commit-msg`

**Findings:**
- Correctly validates Conventional Commits format
- Properly enforces Story:/Spec: trailers for feat/fix at standard/strict levels
- Handles multi-level enforcement (gentle/standard/strict)
- Validates referenced story/spec files exist (strict only)
- **Result:** No bugs found

### 9. Code Quality Checks ✓

**Script Reviews:**

- **`ledger-update.py`** — Fixes applied ✓
- **`refresh-principles.py`** — Clean stdlib-only implementation; no issues
- **`install.sh`** — Fixes applied ✓
- **`serve.py`** (newly created) — Basic implementation; handles `/api/manifest` and `/api/ledger` endpoints
- **`validate-frontmatter.py`** (newly created) — Uses PyYAML; supports both `meta/schemas/` and `templates/schemas/` paths
- **`generate-report.py`** (newly created) — Stdlib-only; generates markdown reports

---

## Directory Structure (Final)

```
build-md/
├── SKILL.md                          # Main skill description
├── AUDIT_SUMMARY.md                  # This file
├── principles/
│   └── PRINCIPLES.md                 # 24 curated best practices
├── scripts/
│   ├── install.sh                    # Repository initialization (✓ fixed)
│   ├── ledger-update.py              # Change ledger updater (✓ bug fixed)
│   ├── refresh-principles.py         # Principles catalog refresh
│   ├── serve.py                      # Local dashboard server (✓ new)
│   ├── validate-frontmatter.py       # YAML validator (✓ new)
│   └── generate-report.py            # Report generator (✓ new)
├── skills/
│   └── init-interview.md             # Onboarding interview flow
├── templates/
│   ├── AGENTS.md.template            # Canonical agent instructions
│   ├── adapters/
│   │   ├── claude.md.template        # Claude Code adapter
│   │   ├── cursor-core.mdc.template  # Cursor core rules
│   │   ├── cursor-stories.mdc.template # Cursor story rules
│   │   ├── copilot-instructions.md.template # GitHub Copilot
│   │   ├── cursorrules.template.deprecated  # OLD — use .mdc
│   │   └── codex.md.template.deprecated     # OLD — use AGENTS.md
│   ├── hooks/
│   │   └── commit-msg                # Commit message validator
│   ├── rules/
│   │   ├── 01-stories.md             # Story authoring rules
│   │   ├── 02-commits.md             # Commit convention rules
│   │   ├── 03-notes.md               # Note-taking rules
│   │   ├── 04-distillation.md        # ADR synthesis rules
│   │   └── 05-visualization.md       # Dashboard rules
│   └── schemas/
│       ├── story.schema.json         # Story frontmatter schema
│       ├── spec.schema.json          # Spec frontmatter schema
│       ├── ledger.schema.json        # Change ledger schema (✓ new)
│       ├── story-template.md         # Story file template (✓ new)
│       ├── spec-template.md          # Spec file template (✓ new)
│       └── adr-template.md           # ADR file template (✓ new)
└── applets/
    └── dashboard.html                # Kanban board + timeline (✓ new)
```

---

## Summary of Changes

| Category | Type | Count | Status |
|----------|------|-------|--------|
| Naming fixes | Edit | 1 | ✓ |
| Template deprecations | Move to .deprecated | 2 | ✓ |
| Bug fixes | Edit | 2 | ✓ |
| Script quality | Review | 5 | ✓ (2 new, 3 reviewed) |
| New files created | Create | 8 | ✓ |
| Hook quality | Review | 1 | ✓ |
| Principles review | Review | 24 | ✓ |

---

## Tests & Validation

**Checklist:**

- [x] All file references in SKILL.md now point to existing files
- [x] Naming is consistent ("Build.MD" formal, "build-md" CLI)
- [x] No duplicate template files (old formats deprecated)
- [x] Scripts have no stdlib-only dependencies (except validate-frontmatter.py which uses PyYAML)
- [x] Hooks execute without syntax errors
- [x] Principles have clear, non-vague language
- [x] ledger-update.py bug fixed (storys → stories)
- [x] All template files have proper structure and variables

---

## Recommendations

1. **Future:** Run the full init flow on a test project to verify all templates render correctly
2. **Future:** Add CI check to validate JSON schemas in `templates/schemas/`
3. **Future:** Consider adding a pre-commit hook to run `validate-frontmatter.py` on story/spec changes
4. **Note:** The `.deprecated` files can be deleted in a future cleanup; keeping them now for reference

---

## File Manifest

**Total Files:** 30  
**Deprecated (not deleted):** 2  
**New Files:** 8  
**Modified Files:** 3  
**Reviewed (no changes):** 17

---

*Audit completed. Build.MD is now internally consistent and self-contained.*
