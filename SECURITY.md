# Security Policy

## Scope

Build.MD is a scaffolding tool. It scaffolds Markdown files, shell hooks, and Python scripts into a user's Git repository. It does not run as a long-lived service, does not process untrusted remote input, and does not manage secrets.

That said, it does:

- Write into the user's working tree (files and directories under the target directory).
- Configure `git config core.hooksPath` (local repo config only — never global, never system).
- Install hooks that run on the user's machine during commit/push.

The attack surface worth auditing is therefore: **the installer, the hook scripts, and the helper Python scripts that run in the user's repo after install**.

## Reporting a vulnerability

If you find a security issue, please **do not open a public GitHub issue**. Instead:

1. Open a private security advisory on the repository: **Security → Advisories → New draft**.
2. Include: affected version/commit, reproduction steps, and the impact you observed.

We aim to acknowledge reports within 7 days and publish a fix or mitigation within 30 days for confirmed vulnerabilities.

## Non-security bugs

For anything that is not a security issue — install failures, missing features, documentation errors — please open a regular GitHub issue.

## What Build.MD will never do

These are commitments, not defaults. If a future version breaks any of them, that is itself a security issue.

1. **No network calls during install.** The installer reads and writes only within the local clone and the target directory.
2. **No telemetry.** Build.MD does not phone home. Ever.
3. **No global configuration changes.** `git config` writes are repo-local (no `--global`, no `--system`). Shell configs (`.bashrc`, `.zshrc`) are not modified.
4. **No operations outside the target directory.** The installer rejects paths it cannot resolve to an existing directory.
5. **No privileged operations.** No `sudo`, no package-manager invocations.
6. **No `curl | bash` of remote code.** The installer refuses to run if `$BASH_SOURCE` is not a real file path.

## Auditing the install before running it

```bash
git clone https://github.com/Jimthetaxguy/build-md.git
cd build-md

# Read the installer:
less scripts/install.sh

# Preview every action without modifying anything:
./scripts/install.sh /path/to/your/project --dry-run
```

The `--dry-run` flag exits before any write, after printing the full list of planned actions. Every real install writes a receipt to `<target>/.build-md-install-receipt.txt` with a timestamp and each action taken.

## Dependencies

- **Installer:** `bash`, `git`, `cp`, `mkdir`, `chmod`. POSIX-standard. No third-party shell libraries.
- **Python helpers:** Python 3.9+ standard library only. `scripts/build-graph.py`, `scripts/ledger-update.py`, `scripts/validate-frontmatter.py`, `scripts/generate-report.py`, `scripts/refresh-principles.py`, `scripts/serve.py` — none require `pip install`. Verify with `python3 -c "import ast; import json; import pathlib"` (all standard library).
- **Dashboard:** `applets/dashboard.html` is a single static HTML file. No external JS/CSS, no CDN, no fonts fetched remotely. Opens in a browser as `file://` or served by `scripts/serve.py` (Python's built-in `http.server`).

## Supply-chain considerations

- All files are plain text (Markdown, shell, Python, HTML, JSON). There are no compiled binaries, no minified bundles, no `node_modules/`, no Git submodules.
- The `principles/PRINCIPLES.md` file is curated content refreshed by `scripts/refresh-principles.py`. The refresh script is currently a scaffold — it does not fetch live content. If a future version adds remote fetching, it will require explicit opt-in via a flag.

## Version support

Only the latest released version receives security fixes. Users on older versions should update before reporting or filing issues.
