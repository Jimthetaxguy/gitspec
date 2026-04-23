#!/usr/bin/env bash
set -euo pipefail

# Build.MD Installer
# Detects your environment and sets up repo-native project management.
# Works for CLI users, but the init interview can also run inside any AI agent.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_MD_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="${1:-.}"

echo "╔══════════════════════════════════════╗"
echo "║        Build.MD — Installer          ║"
echo "╚══════════════════════════════════════╝"
echo ""

cd "$TARGET_DIR"

# ── Step 1: Check for Git ──
if [ ! -d ".git" ]; then
  echo "No Git repository found. Initialize one? [Y/n]"
  read -r response
  if [[ "$response" =~ ^[Nn] ]]; then
    echo "Build.MD requires Git. Exiting."
    exit 1
  fi
  git init
  echo "✓ Git initialized"
fi

# ── Step 2: Detect agent tools ──
echo ""
echo "Detecting AI agent tools..."

AGENTS=()
[ -f "CLAUDE.md" ] || [ -d ".claude" ] && AGENTS+=("claude")
[ -f ".cursorrules" ] || [ -d ".cursor" ] && AGENTS+=("cursor")
[ -f ".github/copilot-instructions.md" ] && AGENTS+=("copilot")
[ -d ".codex" ] && AGENTS+=("codex")
[ -d ".vscode" ] && AGENTS+=("vscode")

if [ ${#AGENTS[@]} -eq 0 ]; then
  echo "  No agent configs detected — will create AGENTS.md (universal)"
else
  echo "  Found: ${AGENTS[*]}"
fi

# ── Step 3: Create directory structure ──
echo ""
echo "Creating directory structure..."

mkdir -p docs/specs docs/stories/archive docs/notes docs/decisions docs/reports
mkdir -p .ledger .agents/rules meta/schemas applets scripts

# Initialize empty ledger
if [ ! -f ".ledger/changes.json" ]; then
  cat > .ledger/changes.json << 'LEDGER'
{
  "version": "1",
  "generated": null,
  "entries": []
}
LEDGER
fi

echo "✓ Directories created"

# ── Step 4: Copy templates and scripts ──
echo "Copying templates and scripts..."

# Copy rule blocks
for rule in "$BUILD_MD_ROOT/templates/rules/"*.md; do
  [ -f "$rule" ] && cp "$rule" ".agents/rules/"
done

# Copy schemas
for schema in "$BUILD_MD_ROOT/templates/schemas/"*.json; do
  [ -f "$schema" ] && cp "$schema" "meta/schemas/"
done

# Copy scripts
for script in "$BUILD_MD_ROOT/scripts/"*.py "$BUILD_MD_ROOT/scripts/"*.sh; do
  [ -f "$script" ] && cp "$script" "scripts/"
done

# Copy applet
[ -f "$BUILD_MD_ROOT/applets/dashboard.html" ] && cp "$BUILD_MD_ROOT/applets/dashboard.html" "applets/"

# Copy principles
mkdir -p .agents
[ -f "$BUILD_MD_ROOT/principles/PRINCIPLES.md" ] && cp "$BUILD_MD_ROOT/principles/PRINCIPLES.md" ".agents/"

echo "✓ Templates copied"

# ── Step 5: Install git hooks ──
echo ""
echo "Install git hooks? They enforce commit conventions. [Y/n]"
read -r response
if [[ ! "$response" =~ ^[Nn] ]]; then
  # Use core.hooksPath so hooks are tracked in the repo
  mkdir -p .hooks
  for hook in "$BUILD_MD_ROOT/templates/hooks/"*; do
    [ -f "$hook" ] && cp "$hook" ".hooks/" && chmod +x ".hooks/$(basename "$hook")"
  done
  git config core.hooksPath .hooks
  echo "✓ Hooks installed (via core.hooksPath → .hooks/)"
else
  echo "  Skipped hooks"
fi

# ── Step 6: Generate AGENTS.md placeholder ──
if [ ! -f "AGENTS.md" ]; then
  cat > AGENTS.md << 'AGENTSMD'
# Project — Build.MD Agent Contract

> Run `build-md init` or tell your AI agent "initialize Build.MD" to complete this setup.
> This file will be populated with your project-specific conventions.

## Quick Start

This repository uses Build.MD for repo-native project management.
See `.agents/rules/` for the contribution rules and `applets/dashboard.html` for the visual dashboard.
AGENTSMD
  echo "✓ AGENTS.md created (run init to customize)"
fi

# ── Step 7: Summary ──
echo ""
echo "╔══════════════════════════════════════╗"
echo "║       Build.MD — Installed!          ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Tell your AI agent: 'Run build-md init'"
echo "     — or run it conversationally in any coding agent"
echo "  2. The init flow will ask about your project and generate"
echo "     agent configs, documentation structure, and enforcement rules"
echo "  3. Commit everything and start building!"
echo ""
echo "Files created:"
find docs .ledger .agents meta applets scripts AGENTS.md -maxdepth 1 2>/dev/null | sort | head -30
echo ""
