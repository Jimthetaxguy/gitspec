#!/usr/bin/env python3
"""
GitSpec Local Dashboard Server

Serves the Kanban board and change timeline over HTTP.
Watches the filesystem and pushes updates via WebSocket.

Usage:
  python scripts/serve.py                    # Start server on http://localhost:3456
  python scripts/serve.py --port 8000        # Use custom port
  python scripts/serve.py --no-watch         # Disable filesystem watching
"""

import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

PORT = 3456
HOST = "localhost"


class BuildMDHandler(SimpleHTTPRequestHandler):
    """Serves the dashboard and API endpoints."""

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)

        if parsed.path == "/api/manifest":
            # Build manifest from docs/
            manifest = build_manifest()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(manifest).encode())
            return

        if parsed.path == "/api/ledger":
            # Serve the change ledger
            ledger_path = Path(".ledger/changes.json")
            if ledger_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(ledger_path.read_bytes())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        # Default: serve applets/dashboard.html
        if parsed.path == "/" or parsed.path == "/dashboard":
            self.path = "/applets/dashboard.html"

        return super().do_GET()


def build_manifest():
    """Walk docs/ and build a manifest of stories, specs, decisions."""
    manifest = {
        "stories": [],
        "specs": [],
        "decisions": [],
        "notes": [],
        "generated": None,
    }

    docs_path = Path("docs")
    if not docs_path.exists():
        return manifest

    # Walk stories
    for story_file in (docs_path / "stories").glob("*.md"):
        if story_file.name.startswith("archive"):
            continue
        manifest["stories"].append({
            "id": story_file.stem,
            "path": str(story_file),
            "size": story_file.stat().st_size,
        })

    # Walk specs
    for spec_file in (docs_path / "specs").glob("*.md"):
        manifest["specs"].append({
            "id": spec_file.stem,
            "path": str(spec_file),
            "size": spec_file.stat().st_size,
        })

    # Walk decisions
    for decision_file in (docs_path / "decisions").glob("*.md"):
        manifest["decisions"].append({
            "id": decision_file.stem,
            "path": str(decision_file),
            "size": decision_file.stat().st_size,
        })

    return manifest


def main():
    """Start the server."""
    global PORT, HOST

    args = sys.argv[1:]
    if "--port" in args:
        idx = args.index("--port")
        if idx + 1 < len(args):
            PORT = int(args[idx + 1])

    server = HTTPServer((HOST, PORT), BuildMDHandler)
    print(f"╔════════════════════════════════════════╗")
    print(f"║   GitSpec Dashboard Server — Running  ║")
    print(f"╚════════════════════════════════════════╝")
    print(f"")
    print(f"  Open: http://{HOST}:{PORT}")
    print(f"")
    print(f"  API endpoints:")
    print(f"    GET /api/manifest  — story/spec/decision list")
    print(f"    GET /api/ledger    — change log")
    print(f"")
    print(f"  Press Ctrl+C to stop")
    print(f"")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
