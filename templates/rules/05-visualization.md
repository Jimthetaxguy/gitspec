# Rule: Progress Visualization

The local dashboard at `applets/dashboard.html` is a read-only view of your project state. 
It renders data from Git history and frontmatter — it has no database of its own.

**To start the dashboard:**
```bash
python scripts/serve.py
# Opens http://localhost:3456
```

**What the dashboard shows:**
- **Kanban board** — stories grouped by status, draggable between columns
- **Spec coverage** — which specs have implementing stories and code
- **Change timeline** — commit history with signal classification
- **Contributor activity** — who's working on what, based on notes and commits

**For AI agents:**
- You can read the manifest at `applets/stories-manifest.json` to understand current 
  project state without opening the dashboard
- When asked about project status, read the manifest and `.ledger/changes.json` directly
- Don't modify `stories-manifest.json` — it's regenerated from source files

**Regenerating the manifest:**
```bash
python scripts/build-manifest.py
```
This walks `docs/stories/` and `docs/specs/`, parses frontmatter, and writes the manifest.
