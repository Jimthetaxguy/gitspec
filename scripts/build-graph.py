#!/usr/bin/env python3
"""
GitSpec Traceability Graph Generator

Reads the ledger, story/spec directories, and scans source files for rnpm[...]
annotations to build a complete traceability graph. Outputs .ledger/graph.json
with nodes (stories, specs, changes, annotations) and edges (implements,
references, depends, verifies).

Node types:
  - story: STORY-NNN from docs/stories/
  - spec: SPEC-XXX from docs/specs/
  - change: CHG-NNNN from .ledger/changes.json
  - annotation: src/path:line with rnpm[...] marker

Edge relations:
  - implements: story→spec, change→story/spec
  - references: change→story/spec
  - depends: annotation→spec
  - impl: annotation→spec (implements the spec)
  - verify: annotation→spec (test verifying spec)
  - risk: annotation→spec (known risk related to spec)
  - workaround: annotation→spec (temporary workaround)

Usage:
  python scripts/build-graph.py                       # Build from cwd
  python scripts/build-graph.py --output custom.json  # Custom output path
  python scripts/build-graph.py --scan-only src/      # Scan only specific dir

No external dependencies — uses only Python stdlib.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_ledger() -> dict:
    """Load the change ledger."""
    ledger_path = Path(".ledger/changes.json")
    if not ledger_path.exists():
        return {"entries": []}
    try:
        return json.loads(ledger_path.read_text())
    except json.JSONDecodeError:
        return {"entries": []}


def load_stories() -> dict:
    """Load all stories from docs/stories/ and return {id: story_data}."""
    stories = {}
    stories_dir = Path("docs/stories")
    if not stories_dir.exists():
        return stories

    for md_file in stories_dir.glob("*.md"):
        frontmatter = parse_frontmatter(md_file)
        if frontmatter and "id" in frontmatter:
            story_id = frontmatter["id"]
            stories[story_id] = {
                "id": story_id,
                "title": frontmatter.get("title", ""),
                "status": frontmatter.get("status", ""),
                "spec": frontmatter.get("spec"),
            }

    return stories


def load_specs() -> dict:
    """Load all specs from docs/specs/ and return {id: spec_data}."""
    specs = {}
    specs_dir = Path("docs/specs")
    if not specs_dir.exists():
        return specs

    for md_file in specs_dir.glob("*.md"):
        frontmatter = parse_frontmatter(md_file)
        if frontmatter and "id" in frontmatter:
            spec_id = frontmatter["id"]
            specs[spec_id] = {
                "id": spec_id,
                "title": frontmatter.get("title", ""),
                "status": frontmatter.get("status", ""),
                "stories": frontmatter.get("stories", []),
            }

    return specs


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text()
    except Exception:
        return {}

    if not content.startswith("---"):
        return {}

    # Find closing ---
    lines = content.split("\n")
    end_idx = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end_idx is None:
        return {}

    frontmatter_lines = lines[1:end_idx]
    fm = {}
    for line in frontmatter_lines:
        line = line.strip()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()

        # Simple value parsing
        if val.startswith("[") and val.endswith("]"):
            # Array: [item1, item2]
            items = [x.strip() for x in val[1:-1].split(",")]
            fm[key] = items
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val

    return fm


def scan_annotations(root_dir: str = ".") -> list:
    """
    Scan source files for rnpm[...] annotations.

    Returns list of {file, line, kind, spec_id} dicts.
    """
    annotations = []
    root = Path(root_dir)

    # Common source file extensions
    extensions = {".py", ".js", ".ts", ".rs", ".go", ".java", ".c", ".h", ".cpp", ".tsx", ".jsx"}

    for src_file in root.rglob("*"):
        if src_file.is_file() and src_file.suffix in extensions:
            # Skip node_modules, venv, .git, etc.
            parts = src_file.parts
            if any(p in parts for p in ("node_modules", "venv", ".git", ".venv", "build", "dist")):
                continue

            try:
                lines = src_file.read_text().split("\n")
            except Exception:
                continue

            for line_num, line in enumerate(lines, start=1):
                # Match rnpm[kind SPEC-ID] patterns
                match = re.search(r"rnpm\[([\w]+)\s+(SPEC-[\w-]+)\]", line)
                if match:
                    kind = match.group(1)
                    spec_id = match.group(2)
                    rel_path = str(src_file.relative_to(root))
                    annotations.append(
                        {
                            "file": rel_path,
                            "line": line_num,
                            "kind": kind,
                            "spec_id": spec_id,
                        }
                    )

    return annotations


def build_graph(ledger: dict, stories: dict, specs: dict, annotations: list) -> dict:
    """Build the full traceability graph."""

    nodes = []
    edges = []
    node_ids = set()

    # Add story nodes
    for story_id, story in stories.items():
        nodes.append(
            {
                "id": story_id,
                "type": "story",
                "status": story.get("status"),
            }
        )
        node_ids.add(story_id)

    # Add spec nodes
    for spec_id, spec in specs.items():
        nodes.append(
            {
                "id": spec_id,
                "type": "spec",
                "status": spec.get("status"),
            }
        )
        node_ids.add(spec_id)

    # Add change nodes (from ledger)
    for entry in ledger.get("entries", []):
        change_id = entry.get("id")
        if change_id:
            nodes.append(
                {
                    "id": change_id,
                    "type": "change",
                    "signal": entry.get("signal"),
                }
            )
            node_ids.add(change_id)

    # Add annotation nodes
    annotation_nodes = {}
    for ann in annotations:
        node_id = f"{ann['file']}:{ann['line']}"
        annotation_nodes[node_id] = ann
        nodes.append(
            {
                "id": node_id,
                "type": "annotation",
                "kind": ann["kind"],
            }
        )
        node_ids.add(node_id)

    # Build edges: story → spec (implements)
    for story_id, story in stories.items():
        if story.get("spec"):
            spec_id = story["spec"]
            if spec_id in node_ids:
                edges.append(
                    {
                        "from": story_id,
                        "to": spec_id,
                        "relation": "implements",
                    }
                )

    # Build edges: change → story/spec (references)
    for entry in ledger.get("entries", []):
        change_id = entry.get("id")
        if not change_id:
            continue

        for story_id in entry.get("stories", []):
            if story_id in node_ids:
                edges.append(
                    {
                        "from": change_id,
                        "to": story_id,
                        "relation": "references",
                    }
                )

        for spec_id in entry.get("specs", []):
            if spec_id in node_ids:
                edges.append(
                    {
                        "from": change_id,
                        "to": spec_id,
                        "relation": "references",
                    }
                )

    # Build edges: annotation → spec (impl, verify, risk, depends, workaround)
    for ann in annotations:
        spec_id = ann["spec_id"]
        node_id = f"{ann['file']}:{ann['line']}"

        if spec_id in node_ids:
            relation = ann["kind"]  # impl, verify, risk, depends, workaround
            edges.append(
                {
                    "from": node_id,
                    "to": spec_id,
                    "relation": relation,
                }
            )

    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": edges,
    }


def main():
    args = sys.argv[1:]

    output_path = ".ledger/graph.json"
    scan_root = "."

    # Parse arguments
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif args[i] == "--scan-only" and i + 1 < len(args):
            scan_root = args[i + 1]
            i += 2
        else:
            i += 1

    # Load all data
    ledger = load_ledger()
    stories = load_stories()
    specs = load_specs()
    annotations = scan_annotations(scan_root)

    # Build graph
    graph = build_graph(ledger, stories, specs, annotations)

    # Write output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(graph, indent=2) + "\n")

    print(f"Graph built: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
