#!/usr/bin/env python3
"""
GitSpec Change Ledger — Two-Phase ID Model

Parses conventional commits with Story:/Spec: trailers and appends significant
changes to .ledger/changes.json. Uses a two-phase ID model to prevent collision
during parallel agent work:

**Phase 1: Pending (branch work)**
  - IDs are CHG-PENDING-{7-char short hash}
  - Allows parallel agents to create entries without conflicts
  - Pre-push hook validates the pending ledger

**Phase 2: Finalized (main branch only)**
  - IDs are reassigned to sequential CHG-NNNN format
  - Run after merge to main to finalize IDs
  - Main branch always has clean sequential IDs

Usage:
  python scripts/ledger-update.py                    # Process HEAD~1..HEAD (assigns pending)
  python scripts/ledger-update.py --since abc1234    # Process abc1234..HEAD (assigns pending)
  python scripts/ledger-update.py --full-rebuild     # Rebuild entire ledger from history
  python scripts/ledger-update.py --validate         # Validate existing ledger integrity
  python scripts/ledger-update.py --finalize         # Reassign pending IDs to sequential (main only)

No external dependencies — uses only Python stdlib (subprocess, json, re, pathlib).
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path(".ledger/changes.json")

SIGNAL_MAP = {
    "feat": "critical",
    "fix": "critical",
    "perf": "notable",
    "refactor": "notable",
    "docs": "notable",
    "test": "conditional",
    "revert": "critical",
}

EXCLUDED_TYPES = {"chore", "style", "ci", "build"}


def git(*args):
    """Run a git command and return stripped stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def parse_trailers(text: str) -> dict:
    """Extract Story:, Spec:, and Notes: trailers from commit message."""
    trailers = {}
    for line in text.splitlines():
        match = re.match(r"^(Story|Spec|Notes):\s*(.+)$", line, re.IGNORECASE)
        if match:
            key = match.group(1).lower() + "s"
            values = [v.strip() for v in match.group(2).split(",")]
            trailers.setdefault(key, []).extend(values)
    return trailers


def parse_type_scope(subject: str):
    """Parse conventional commit subject into type, scope, breaking, summary."""
    match = re.match(r"^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)$", subject)
    if not match:
        return None, None, False, subject
    ctype, scope, breaking, summary = match.groups()
    return ctype, scope, breaking == "!", summary


def is_significant(ctype: str, trailers: dict) -> bool:
    """Determine if a commit should be written to the ledger."""
    if ctype in EXCLUDED_TYPES:
        return False
    tier = SIGNAL_MAP.get(ctype)
    if tier == "conditional":
        return bool(trailers.get("stories", []))
    return tier in ("critical", "notable")


def parse_commit(sha: str) -> dict | None:
    """Parse a single commit into a ledger entry candidate."""
    # Use null-byte delimiters for reliable parsing
    fmt = "%H\x00%an <%ae>\x00%aI\x00%s\x00%b"
    raw = git("show", f"--pretty=format:{fmt}", "--name-only", sha)
    if not raw:
        return None

    parts = raw.split("\x00", 4)
    if len(parts) < 5:
        return None

    commit_hash, author, date, subject, rest = parts

    # Split body from file list (files come after blank line in --name-only output)
    lines = rest.strip().splitlines()
    blank_idx = next(
        (i for i, line in enumerate(lines) if line.strip() == ""), len(lines)
    )
    body_lines = lines[:blank_idx]
    file_lines = [
        line
        for line in lines[blank_idx + 1 :]
        if line.strip() and not line.startswith("diff")
    ]

    body = "\n".join(body_lines)
    full_message = subject + "\n\n" + body

    # Parse trailers from full message
    trailers = parse_trailers(full_message)

    # Parse conventional commit
    ctype, scope, breaking, summary = parse_type_scope(subject)
    if ctype is None:
        return None

    if not is_significant(ctype, trailers):
        return None

    return {
        "commit": commit_hash,
        "shortHash": commit_hash[:7],
        "author": author,
        "date": date,
        "type": ctype,
        "scope": scope,
        "signal": SIGNAL_MAP.get(ctype, "notable"),
        "summary": summary,
        "body": body.strip(),
        "specs": trailers.get("specs", []),
        "stories": trailers.get("stories", []),
        "notes": trailers.get("notes", []),
        "filesChanged": file_lines,
        "breakingChange": breaking or "BREAKING CHANGE" in body,
        "supersededBy": None,
        "tags": [],
    }


def load_ledger() -> dict:
    """Load the existing ledger or create a new one."""
    if LEDGER_PATH.exists():
        try:
            return json.loads(LEDGER_PATH.read_text())
        except json.JSONDecodeError:
            print("Warning: Corrupted ledger, starting fresh")
    return {"version": "1", "generated": None, "entries": []}


def save_ledger(ledger: dict):
    """Write ledger to disk."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger["generated"] = datetime.now(timezone.utc).isoformat()
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2) + "\n")


def next_id_pending(short_hash: str) -> str:
    """Generate a pending CHG ID using short hash (no collision)."""
    return f"CHG-PENDING-{short_hash}"


def next_id_sequential(ledger: dict) -> str:
    """Generate the next sequential CHG ID (for finalize phase)."""
    n = len(ledger["entries"]) + 1
    return f"CHG-{n:04d}"


def handle_revert(entry: dict, ledger: dict):
    """If this is a revert commit, mark the original entry as superseded."""
    revert_match = re.search(
        r"This reverts commit ([a-f0-9]+)", entry.get("body", "")
    )
    if revert_match:
        reverted_hash = revert_match.group(1)
        for existing in ledger["entries"]:
            if existing["commit"].startswith(reverted_hash):
                existing["supersededBy"] = entry.get("id")
                break


def update(since: str = "HEAD~1"):
    """
    Process new commits and append to ledger with pending IDs.

    Assigns CHG-PENDING-{shortHash} IDs to allow parallel agents to work
    without collision. Call finalize_ids() on main branch to reassign
    to sequential CHG-NNNN format.
    """
    ledger = load_ledger()
    existing_commits = {e["commit"] for e in ledger["entries"]}

    log_output = git("log", f"{since}..HEAD", "--pretty=format:%H", "--reverse")
    if not log_output:
        print("No new commits to process")
        return

    new_shas = [
        sha
        for sha in log_output.splitlines()
        if sha and sha not in existing_commits
    ]

    added = 0
    for sha in new_shas:
        entry = parse_commit(sha)
        if entry:
            short_hash = entry["shortHash"]
            entry["id"] = next_id_pending(short_hash)
            entry["schemaVersion"] = "1"
            handle_revert(entry, ledger)
            ledger["entries"].append(entry)
            added += 1

    save_ledger(ledger)
    total = len(ledger["entries"])
    print(f"Ledger updated: +{added} entries ({total} total)")


def full_rebuild():
    """
    Rebuild the entire ledger from git history using pending IDs.

    Assigns CHG-PENDING-{shortHash} IDs. Use finalize_ids() afterward
    to convert to sequential format.
    """
    ledger = {"version": "1", "generated": None, "entries": []}

    log_output = git("log", "--first-parent", "--pretty=format:%H", "--reverse")
    if not log_output:
        print("No commits found")
        return

    added = 0
    for sha in log_output.splitlines():
        if not sha:
            continue
        entry = parse_commit(sha)
        if entry:
            short_hash = entry["shortHash"]
            entry["id"] = next_id_pending(short_hash)
            entry["schemaVersion"] = "1"
            handle_revert(entry, ledger)
            ledger["entries"].append(entry)
            added += 1

    save_ledger(ledger)
    print(f"Ledger rebuilt: {added} entries from full history (pending IDs)")


def validate():
    """
    Validate the existing ledger for consistency.

    Checks for duplicate IDs and commits. For sequential (finalized) ledgers,
    also validates the ID sequence. Pending ledgers are allowed to have
    CHG-PENDING-{hash} format without sequential ordering.
    """
    if not LEDGER_PATH.exists():
        print("No ledger found. Run 'ledger-update.py' to create one.")
        return False

    ledger = load_ledger()
    errors = []

    # Check for duplicate IDs
    ids = [e["id"] for e in ledger["entries"]]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate entry IDs found")

    # Check for duplicate commits
    commits = [e["commit"] for e in ledger["entries"]]
    if len(commits) != len(set(commits)):
        errors.append("Duplicate commit hashes found")

    # Check if ledger is finalized (sequential IDs) and validate sequence
    is_finalized = all(e["id"].startswith("CHG-") and not e["id"].startswith("CHG-PENDING") for e in ledger["entries"])
    if is_finalized:
        for i, entry in enumerate(ledger["entries"]):
            expected = f"CHG-{i + 1:04d}"
            if entry["id"] != expected:
                errors.append(f"ID gap: expected {expected}, got {entry['id']}")
                break

    if errors:
        print(f"Validation FAILED ({len(errors)} errors):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        mode = "finalized" if is_finalized else "pending"
        print(f"Validation OK: {len(ledger['entries'])} entries ({mode}), no issues")
        return True


def finalize_ids():
    """
    Reassign all pending IDs to sequential CHG-NNNN format.

    This is meant to run on the main branch only, after all pending changes
    are merged. It rewrites all CHG-PENDING-{hash} IDs to CHG-0001, CHG-0002, etc.
    in the order they appear in the ledger.
    """
    ledger = load_ledger()

    # Check if any IDs are still pending
    pending_count = sum(1 for e in ledger["entries"] if e["id"].startswith("CHG-PENDING"))
    if pending_count == 0:
        print("Ledger already finalized; no pending IDs to convert")
        return

    # Reassign all IDs sequentially
    for i, entry in enumerate(ledger["entries"]):
        old_id = entry["id"]
        entry["id"] = f"CHG-{i + 1:04d}"

    save_ledger(ledger)
    print(f"Finalized: {pending_count} pending IDs → sequential CHG-NNNN format")


def main():
    args = sys.argv[1:]

    if "--full-rebuild" in args:
        full_rebuild()
    elif "--finalize" in args:
        finalize_ids()
    elif "--validate" in args:
        sys.exit(0 if validate() else 1)
    elif "--since" in args:
        idx = args.index("--since")
        since = args[idx + 1] if idx + 1 < len(args) else "HEAD~1"
        update(since)
    else:
        update()


if __name__ == "__main__":
    main()
