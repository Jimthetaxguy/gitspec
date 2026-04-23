#!/usr/bin/env python3
"""
GitSpec Principles Refresh Script

Checks for updates to the GitSpec principles catalog from upstream sources.
Can be run manually, as a cron job, or as a GitHub Action.

Usage:
  python scripts/refresh-principles.py                    # Check and report
  python scripts/refresh-principles.py --apply            # Apply updates
  python scripts/refresh-principles.py --sources          # List tracked sources
  python scripts/refresh-principles.py --schedule weekly   # Show cron config

This script is intentionally simple — it uses only stdlib modules so it runs
anywhere Python 3.8+ is installed, no pip install needed.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

PRINCIPLES_PATH = Path(".agents/principles/PRINCIPLES.md")
UPSTREAM_SOURCES = {
    "anthropic": {
        "name": "Anthropic",
        "docs_url": "https://docs.anthropic.com",
        "topics": ["agent design", "safety", "MCP", "Claude best practices"],
    },
    "openai": {
        "name": "OpenAI",
        "docs_url": "https://platform.openai.com/docs",
        "topics": ["agents SDK", "structured outputs", "safety", "Codex"],
    },
    "google": {
        "name": "Google DeepMind",
        "docs_url": "https://ai.google.dev",
        "topics": ["Gemma", "responsible AI", "code quality"],
    },
    "meta": {
        "name": "Meta",
        "docs_url": "https://ai.meta.com",
        "topics": ["Llama", "open source AI", "research practices"],
    },
    "microsoft": {
        "name": "Microsoft",
        "docs_url": "https://learn.microsoft.com",
        "topics": ["Copilot", "VS Code agents", "enterprise AI"],
    },
    "langchain": {
        "name": "LangChain",
        "docs_url": "https://docs.langchain.com",
        "topics": ["agent architectures", "tool use", "chains"],
    },
    "cursor": {
        "name": "Cursor",
        "docs_url": "https://cursor.com/docs",
        "topics": ["agent best practices", "rules", "fast iteration"],
    },
    "replit": {
        "name": "Replit",
        "docs_url": "https://docs.replit.com",
        "topics": ["rapid prototyping", "deployment", "AI agents"],
    },
    "ramp": {
        "name": "Ramp",
        "docs_url": "https://engineering.ramp.com",
        "topics": ["engineering velocity", "architecture decisions"],
    },
    "sakana": {
        "name": "Sakana AI",
        "docs_url": "https://sakana.ai",
        "topics": ["AI scientist", "automated research", "evolutionary methods"],
    },
    "harvey": {
        "name": "Harvey AI",
        "docs_url": "https://harvey.ai",
        "topics": ["legal AI workflows", "document processing", "precision"],
    },
    "toltiq": {
        "name": "ToltIQ",
        "docs_url": "https://toltiq.com",
        "topics": ["tax technology", "compliance workflows", "AI accuracy"],
    },
    "hebbia": {
        "name": "Hebbia",
        "docs_url": "https://hebbia.ai",
        "topics": ["knowledge management", "document analysis", "RAG"],
    },
}


def check_upstream_repo():
    """Check if there's a newer version of the principles catalog upstream."""
    # In a real implementation, this would check a GitHub release or raw URL
    # For now, it reports the current state
    if PRINCIPLES_PATH.exists():
        content = PRINCIPLES_PATH.read_text()
        # Extract last_refreshed from the metadata block
        for line in content.splitlines():
            if line.strip().startswith("last_refreshed:"):
                last_date = line.split(":")[1].strip()
                print(f"Last refreshed: {last_date}")
                break
    else:
        print("No principles file found. Run 'gitspec init' first.")


def list_sources():
    """Print all tracked upstream sources."""
    print("GitSpec Principles Sources")
    print("=" * 50)
    for key, source in UPSTREAM_SOURCES.items():
        print(f"\n{source['name']} ({key})")
        print(f"  Docs: {source['docs_url']}")
        print(f"  Topics: {', '.join(source['topics'])}")


def generate_refresh_report():
    """Generate a report of what should be checked for updates."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"\nRefresh Report — {now}")
    print("=" * 50)
    print("\nTo update principles, review these sources for new publications:")
    print()
    for key, source in UPSTREAM_SOURCES.items():
        print(f"  [{source['name']}]")
        print(f"    Check: {source['docs_url']}")
        print(f"    Look for: {', '.join(source['topics'])}")
        print()
    print("After reviewing, add new principles to PRINCIPLES.md following the existing format.")
    print("Mark deprecated principles with 'deprecated: true' — never delete them.")
    print(f"\nUpdate the 'last_refreshed' field to: {now}")


def show_schedule_config(frequency="weekly"):
    """Print cron and GitHub Actions configs for scheduled refresh."""
    cron_map = {
        "daily": "0 9 * * *",
        "weekly": "0 9 * * 1",
        "monthly": "0 9 1 * *",
    }
    cron = cron_map.get(frequency, cron_map["weekly"])

    print(f"\nSchedule: {frequency}")
    print(f"\nCron: {cron}  # (runs at 9 AM UTC)")
    print(f"\nGitHub Actions workflow:")
    print(f"""
# .github/workflows/refresh-principles.yml
name: Refresh GitSpec Principles
on:
  schedule:
    - cron: '{cron}'
  workflow_dispatch:  # manual trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python scripts/refresh-principles.py --report
      - name: Create issue if updates needed
        run: |
          gh issue create \\
            --title "GitSpec Principles Refresh - $(date +%Y-%m-%d)" \\
            --body "$(python scripts/refresh-principles.py --report 2>&1)" \\
            --label "documentation"
        env:
          GH_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
""")


def main():
    args = sys.argv[1:]

    if "--sources" in args:
        list_sources()
    elif "--schedule" in args:
        idx = args.index("--schedule")
        freq = args[idx + 1] if idx + 1 < len(args) else "weekly"
        show_schedule_config(freq)
    elif "--report" in args:
        generate_refresh_report()
    elif "--apply" in args:
        check_upstream_repo()
        generate_refresh_report()
        print("\nTo apply updates, edit .agents/principles/PRINCIPLES.md directly.")
        print("The --apply flag is a placeholder for future automated fetching.")
    else:
        check_upstream_repo()
        print("\nUse --report for a full review checklist")
        print("Use --sources to see all tracked sources")
        print("Use --schedule [daily|weekly|monthly] for automation config")


if __name__ == "__main__":
    main()
