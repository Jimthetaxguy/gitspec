#!/usr/bin/env bash
# Build.MD Installer
# Scaffolds repo-native project management into a Git repository.
#
# Usage:
#   ./scripts/install.sh [TARGET_DIR] [--dry-run] [--yes] [--no-hooks]
#
# Flags:
#   --dry-run    Print the actions that would be taken without modifying anything.
#   --yes        Non-interactive: accept all prompts. Required when stdin is not a TTY.
#   --no-hooks   Skip installing Git hooks (useful for CI smoke tests).
#   -h|--help    Show this help.
#
# Safety model:
#   - Never touches files outside TARGET_DIR.
#   - Refuses to run via `curl | bash` (no sibling template directory available).
#   - Lists every action in the plan phase before executing.
#   - Writes a receipt to .build-md-install-receipt.txt on success.
#   - No network calls. No privileged operations. No telemetry.

set -euo pipefail

# ── Resolve paths ──────────────────────────────────────────────────────────────
SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
if [[ -z "${SCRIPT_PATH}" || "${SCRIPT_PATH}" == "bash" || "${SCRIPT_PATH}" == "-" ]]; then
  echo "ERROR: This installer cannot be run via \`curl | bash\`." >&2
  echo "" >&2
  echo "It needs a local clone so it can copy templates, schemas, and scripts from" >&2
  echo "the repository. Run this instead:" >&2
  echo "" >&2
  echo "  git clone https://github.com/Jimthetaxguy/build-md.git" >&2
  echo "  cd build-md && ./scripts/install.sh /path/to/your/project" >&2
  echo "" >&2
  exit 2
fi
SCRIPT_DIR="$(cd "$(dirname "${SCRIPT_PATH}")" && pwd)"
BUILD_MD_ROOT="$(dirname "${SCRIPT_DIR}")"

# ── Parse args ─────────────────────────────────────────────────────────────────
TARGET_DIR=""
DRY_RUN=0
ASSUME_YES=0
NO_HOOKS=0
for arg in "$@"; do
  case "${arg}" in
    --dry-run)  DRY_RUN=1 ;;
    --yes|-y)   ASSUME_YES=1 ;;
    --no-hooks) NO_HOOKS=1 ;;
    -h|--help)
      sed -n '2,19p' "${SCRIPT_PATH}" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    --*)
      echo "ERROR: unknown flag: ${arg}" >&2; exit 2 ;;
    *)
      if [[ -z "${TARGET_DIR}" ]]; then TARGET_DIR="${arg}"; else
        echo "ERROR: unexpected argument: ${arg}" >&2; exit 2
      fi ;;
  esac
done
TARGET_DIR="${TARGET_DIR:-.}"

# ── Validate source tree ───────────────────────────────────────────────────────
for required in templates/rules templates/schemas templates/hooks scripts applets/dashboard.html principles/PRINCIPLES.md; do
  if [[ ! -e "${BUILD_MD_ROOT}/${required}" ]]; then
    echo "ERROR: source tree incomplete — missing ${BUILD_MD_ROOT}/${required}" >&2
    echo "This installer must be run from a full clone of the build-md repository." >&2
    exit 3
  fi
done

# ── Validate target ────────────────────────────────────────────────────────────
if [[ ! -d "${TARGET_DIR}" ]]; then
  echo "ERROR: target directory does not exist: ${TARGET_DIR}" >&2; exit 4
fi
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"

# ── Non-interactive detection ──────────────────────────────────────────────────
if [[ ! -t 0 && "${ASSUME_YES}" -eq 0 && "${DRY_RUN}" -eq 0 ]]; then
  echo "ERROR: stdin is not a TTY. Pass --yes to run non-interactively, or --dry-run to preview." >&2
  exit 5
fi

# ── Banner ─────────────────────────────────────────────────────────────────────
echo "╔══════════════════════════════════════╗"
echo "║        Build.MD — Installer          ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Source:       ${BUILD_MD_ROOT}"
echo "Target:       ${TARGET_DIR}"
echo "Dry run:      $([[ ${DRY_RUN} -eq 1 ]] && echo yes || echo no)"
echo "Install hooks: $([[ ${NO_HOOKS} -eq 1 ]] && echo no || echo yes)"
echo ""

# ── Detect existing agent configs (informational only) ─────────────────────────
cd "${TARGET_DIR}"
AGENTS=()
{ [[ -f "CLAUDE.md" ]] || [[ -d ".claude" ]]; }                      && AGENTS+=("claude")
{ [[ -f ".cursorrules" ]] || [[ -d ".cursor" ]]; }                   && AGENTS+=("cursor")
[[ -f ".github/copilot-instructions.md" ]]                           && AGENTS+=("copilot")
[[ -d ".codex" ]]                                                    && AGENTS+=("codex")
[[ -d ".vscode" ]]                                                   && AGENTS+=("vscode")
if [[ ${#AGENTS[@]} -eq 0 ]]; then
  echo "Detected agents: none (will create AGENTS.md as the universal contract)"
else
  echo "Detected agents: ${AGENTS[*]}"
fi
echo ""

# ── Plan phase ─────────────────────────────────────────────────────────────────
echo "Plan — the following changes will be made inside ${TARGET_DIR}:"
echo "  1. Initialize Git repo (only if .git/ is absent)"
echo "  2. Create directories: docs/{specs,stories/archive,notes,decisions,reports},"
echo "                         .ledger, .agents/rules, meta/schemas, applets, scripts"
echo "  3. Initialize .ledger/changes.json (only if absent)"
echo "  4. Copy $(ls "${BUILD_MD_ROOT}/templates/rules/"*.md 2>/dev/null | wc -l | tr -d ' ') rule files → .agents/rules/"
echo "  5. Copy $(ls "${BUILD_MD_ROOT}/templates/schemas/"*.json 2>/dev/null | wc -l | tr -d ' ') schema files → meta/schemas/"
echo "  6. Copy $(ls "${BUILD_MD_ROOT}/scripts/"*.py 2>/dev/null | wc -l | tr -d ' ') Python scripts → scripts/"
echo "  7. Copy applets/dashboard.html, principles/PRINCIPLES.md → .agents/"
echo "  8. Copy $(ls "${BUILD_MD_ROOT}/commands/"*.md 2>/dev/null | wc -l | tr -d ' ') slash commands → .claude/commands/"
if [[ ${NO_HOOKS} -eq 0 ]]; then
  echo "  9. Install Git hooks via core.hooksPath → .hooks/"
fi
echo " 10. Create AGENTS.md placeholder (only if absent)"
echo " 11. Write install receipt → .build-md-install-receipt.txt"
echo ""

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "Dry run complete. No changes made."
  exit 0
fi

# ── Confirm ────────────────────────────────────────────────────────────────────
if [[ ${ASSUME_YES} -eq 0 ]]; then
  echo "Proceed? [Y/n]"
  read -r response
  if [[ "${response}" =~ ^[Nn] ]]; then
    echo "Aborted. No changes made."; exit 0
  fi
fi

RECEIPT="${TARGET_DIR}/.build-md-install-receipt.txt"
: > "${RECEIPT}"
log() { echo "$1" | tee -a "${RECEIPT}" >/dev/null; }
log "Build.MD install receipt"
log "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "Source: ${BUILD_MD_ROOT}"
log "Target: ${TARGET_DIR}"
log ""

# ── Execute ────────────────────────────────────────────────────────────────────
# Step 1: Git
if [[ ! -d ".git" ]]; then
  git init -q
  echo "✓ Initialized Git repository"; log "git init"
fi

# Step 2: Directories
mkdir -p docs/specs docs/stories/archive docs/notes docs/decisions docs/reports \
         .ledger .agents/rules meta/schemas applets scripts
log "mkdir -p <scaffold directories>"
echo "✓ Directories created"

# Step 3: Ledger
if [[ ! -f ".ledger/changes.json" ]]; then
  cat > .ledger/changes.json <<'LEDGER'
{
  "version": "1",
  "generated": null,
  "entries": []
}
LEDGER
  log "wrote .ledger/changes.json"
  echo "✓ Ledger initialized"
fi

# Step 4-7: Copy templates, schemas, scripts, applet, principles
copy_if() { [[ -f "$1" ]] && cp "$1" "$2" && log "cp $1 → $2"; }
for rule in "${BUILD_MD_ROOT}/templates/rules/"*.md;   do copy_if "${rule}"   ".agents/rules/"; done
for s in    "${BUILD_MD_ROOT}/templates/schemas/"*.json; do copy_if "${s}"    "meta/schemas/"; done
for s in    "${BUILD_MD_ROOT}/scripts/"*.py "${BUILD_MD_ROOT}/scripts/"*.sh; do copy_if "${s}" "scripts/"; done
copy_if "${BUILD_MD_ROOT}/applets/dashboard.html"     "applets/"
copy_if "${BUILD_MD_ROOT}/principles/PRINCIPLES.md"   ".agents/"
echo "✓ Templates, schemas, scripts copied"

# Step 8: Slash commands (only if the commands/ dir exists in source)
if [[ -d "${BUILD_MD_ROOT}/commands" ]]; then
  mkdir -p .claude/commands
  for cmd in "${BUILD_MD_ROOT}/commands/"*.md; do copy_if "${cmd}" ".claude/commands/"; done
  echo "✓ Slash commands installed to .claude/commands/"
fi

# Step 9: Hooks
if [[ ${NO_HOOKS} -eq 0 ]]; then
  INSTALL_HOOKS=1
  if [[ ${ASSUME_YES} -eq 0 ]]; then
    echo ""
    echo "Install Git hooks? They enforce commit conventions via core.hooksPath. [Y/n]"
    read -r response
    if [[ "${response}" =~ ^[Nn] ]]; then INSTALL_HOOKS=0; fi
  fi
  if [[ ${INSTALL_HOOKS} -eq 1 ]]; then
    mkdir -p .hooks
    for hook in "${BUILD_MD_ROOT}/templates/hooks/"*; do
      if [[ -f "${hook}" ]]; then
        cp "${hook}" ".hooks/" && chmod +x ".hooks/$(basename "${hook}")"
        log "installed hook: $(basename "${hook}")"
      fi
    done
    git config core.hooksPath .hooks
    log "git config core.hooksPath .hooks"
    echo "✓ Hooks installed (via core.hooksPath → .hooks/)"
  else
    echo "  Skipped hooks"
  fi
fi

# Step 10: AGENTS.md
if [[ ! -f "AGENTS.md" ]]; then
  cat > AGENTS.md <<'AGENTSMD'
# Project — Build.MD Agent Contract

> Run `build-md init` or tell your AI agent "initialize Build.MD" to complete this setup.
> This file will be populated with your project-specific conventions.

## Quick Start

This repository uses Build.MD for repo-native project management.
See `.agents/rules/` for the contribution rules and `applets/dashboard.html` for the visual dashboard.
AGENTSMD
  log "wrote AGENTS.md placeholder"
  echo "✓ AGENTS.md created (run init to customize)"
fi

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
echo "║       Build.MD — Installed!          ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Tell your AI agent: 'Run build-md init'"
echo "  2. The init flow asks about your project and fills out AGENTS.md"
echo "  3. Commit the scaffold: git add -A && git commit -m 'chore: scaffold Build.MD'"
echo ""
echo "Receipt: ${RECEIPT}"
