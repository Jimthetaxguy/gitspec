#!/usr/bin/env bash
# End-to-end smoke test for Build.MD.
# Runs the installer into a fresh temp directory (both --dry-run and real) and
# asserts the expected tree is created. Safe to run locally — writes only to
# a scratch dir under $TMPDIR that it creates and cleans up itself.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRATCH="$(mktemp -d -t build-md-smoke-XXXXXX)"
TARGET="${SCRATCH}/sample-project"
mkdir -p "${TARGET}"

cleanup() { rm -rf "${SCRATCH}"; }
trap cleanup EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }
pass() { echo "PASS: $1"; }

echo "Smoke test — Build.MD installer"
echo "  Source: ${REPO_ROOT}"
echo "  Target: ${TARGET}"
echo ""

# ── 1. Dry run should not write anything ──────────────────────────────────────
BEFORE="$(find "${TARGET}" -mindepth 1 2>/dev/null | wc -l | tr -d ' ')"
"${REPO_ROOT}/scripts/install.sh" "${TARGET}" --dry-run --no-hooks >/dev/null
AFTER="$(find "${TARGET}" -mindepth 1 2>/dev/null | wc -l | tr -d ' ')"
[[ "${BEFORE}" == "${AFTER}" ]] || fail "dry-run modified the filesystem (before=${BEFORE}, after=${AFTER})"
pass "--dry-run made zero filesystem changes"

# ── 2. Real install (non-interactive, no hooks for CI safety) ─────────────────
"${REPO_ROOT}/scripts/install.sh" "${TARGET}" --yes --no-hooks >/dev/null

# ── 3. Assert expected tree ───────────────────────────────────────────────────
EXPECT=(
  "docs/specs" "docs/stories/archive" "docs/notes" "docs/decisions" "docs/reports"
  ".ledger/changes.json" ".agents/rules" "meta/schemas" "applets/dashboard.html"
  ".agents/PRINCIPLES.md" "AGENTS.md" ".build-md-install-receipt.txt" ".git"
)
for path in "${EXPECT[@]}"; do
  [[ -e "${TARGET}/${path}" ]] || fail "missing expected path: ${path}"
done
pass "expected tree created"

# ── 4. Assert ledger is valid JSON ────────────────────────────────────────────
python3 -c "import json,sys; json.load(open('${TARGET}/.ledger/changes.json'))" \
  || fail ".ledger/changes.json is not valid JSON"
pass ".ledger/changes.json is valid JSON"

# ── 5. Assert rule files copied ───────────────────────────────────────────────
RULE_COUNT="$(find "${TARGET}/.agents/rules" -name '*.md' | wc -l | tr -d ' ')"
[[ "${RULE_COUNT}" -ge 1 ]] || fail "no rule files copied to .agents/rules/"
pass "rule files copied (${RULE_COUNT} found)"

# ── 6. Assert schema files copied ─────────────────────────────────────────────
SCHEMA_COUNT="$(find "${TARGET}/meta/schemas" -name '*.json' | wc -l | tr -d ' ')"
[[ "${SCHEMA_COUNT}" -ge 1 ]] || fail "no schema files copied to meta/schemas/"
pass "schema files copied (${SCHEMA_COUNT} found)"

# ── 7. Assert receipt is well-formed ──────────────────────────────────────────
grep -q "^Date: " "${TARGET}/.build-md-install-receipt.txt" || fail "receipt missing Date line"
grep -q "^Source: " "${TARGET}/.build-md-install-receipt.txt" || fail "receipt missing Source line"
pass "install receipt well-formed"

# ── 8. Refuse curl-pipe invocation ────────────────────────────────────────────
# Simulate by piping the installer to bash with no BASH_SOURCE.
set +e
ERR_OUTPUT="$(bash < "${REPO_ROOT}/scripts/install.sh" 2>&1)"
RC=$?
set -e
[[ ${RC} -ne 0 ]] || fail "installer should refuse curl-pipe invocation but succeeded"
echo "${ERR_OUTPUT}" | grep -q "curl | bash" || fail "curl-pipe refusal message not shown"
pass "curl-pipe invocation refused with guidance"

echo ""
echo "All checks passed."
