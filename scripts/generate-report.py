#!/usr/bin/env python3
"""
Build.MD Change Report Generator

Generates markdown reports of changes between versions or commit ranges.

Usage:
  python scripts/generate-report.py                    # Report on full ledger
  python scripts/generate-report.py --from v1.0 --to HEAD   # Between versions
  python scripts/generate-report.py --since abc1234    # Since commit
  python scripts/generate-report.py --output report.md # Save to file
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_ledger():
    """Load the change ledger."""
    ledger_path = Path(".ledger/changes.json")
    if not ledger_path.exists():
        print("Error: .ledger/changes.json not found. Run 'ledger-update.py' first.")
        sys.exit(1)
    return json.loads(ledger_path.read_text())


def generate_report(ledger, output_file=None):
    """Generate a markdown report from the ledger."""
    lines = [
        "# Change Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Total changes: {len(ledger['entries'])}",
        "",
    ]

    # Group by signal level
    by_signal = {"critical": [], "notable": [], "conditional": []}
    for entry in ledger["entries"]:
        signal = entry.get("signal", "notable")
        if signal in by_signal:
            by_signal[signal].append(entry)

    # Critical changes
    if by_signal["critical"]:
        lines.append("## Critical Changes")
        lines.append("")
        for entry in by_signal["critical"]:
            lines.append(f"### {entry['shortHash']} — {entry['summary']}")
            lines.append(f"**Type:** {entry['type']}")
            if entry.get("scope"):
                lines.append(f"**Scope:** {entry['scope']}")
            lines.append(f"**Author:** {entry['author']}")
            lines.append(f"**Date:** {entry['date']}")
            if entry.get("stories"):
                lines.append(f"**Stories:** {', '.join(entry['stories'])}")
            if entry.get("specs"):
                lines.append(f"**Specs:** {', '.join(entry['specs'])}")
            if entry.get("body"):
                lines.append("")
                lines.append(entry["body"])
            lines.append("")

    # Notable changes
    if by_signal["notable"]:
        lines.append("## Notable Changes")
        lines.append("")
        for entry in by_signal["notable"]:
            lines.append(f"- `{entry['shortHash']}` **{entry['type']}**: {entry['summary']}")
        lines.append("")

    # Summary stats
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Signal | Count |")
    lines.append(f"|--------|-------|")
    for signal, entries in by_signal.items():
        if entries:
            lines.append(f"| {signal} | {len(entries)} |")
    lines.append("")

    report = "\n".join(lines)

    if output_file:
        Path(output_file).write_text(report)
        print(f"Report written to {output_file}")
    else:
        print(report)

    return report


def main():
    """Generate and output the report."""
    args = sys.argv[1:]
    output_file = None

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_file = args[idx + 1]

    ledger = load_ledger()
    generate_report(ledger, output_file)


if __name__ == "__main__":
    main()
