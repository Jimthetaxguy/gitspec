# Security Policy

## Project Status

Build.MD is a **released skills pack**, not an actively-maintained service. The author is not acting as a continuous maintainer. Pull requests and security reports are welcome but there is no commitment — express or implied — that any report, issue, or PR will be reviewed, responded to, or acted upon in any timeframe, or at all. Users should plan accordingly and fork the project if they need guaranteed maintenance.

## Scope

Build.MD is a scaffolding tool. It scaffolds Markdown files, shell hooks, and Python scripts into a user's Git repository. It does not run as a long-lived service, does not process untrusted remote input, and does not manage secrets.

That said, it does:

- Write into the user's working tree (files and directories under the target directory).
- Configure `git config core.hooksPath` (local repo config only — never global, never system).
- Install hooks that run on the user's machine during commit/push.

The attack surface worth auditing is therefore: **the installer, the hook scripts, and the helper Python scripts that run in the user's repo after install**.

## Reporting a vulnerability

If you find a security issue, please **do not open a public GitHub issue**. Instead, open a private security advisory on the repository (**Security → Advisories → New draft**) and include affected version/commit, reproduction steps, and the impact you observed.

No acknowledgment, response, or fix is guaranteed. The software is provided **"AS IS"** under the MIT License without warranty of any kind — see `LICENSE` for the full text.

## Non-security bugs

For anything that is not a security issue — install failures, missing features, documentation errors — you may open a regular GitHub issue. Response is not guaranteed. Forks are encouraged.

## What Build.MD will never do

The items below describe the software's intentional behavior. If a future version breaks any of them, it is a regression. These statements describe the software, not a warranty — see the MIT License in `LICENSE` for the applicable disclaimer of warranty.

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
- **Python helpers:** Python 3.9+ standard library only. None require `pip install`.
- **Dashboard:** `applets/dashboard.html` is a single static HTML file. No external JS/CSS, no CDN, no fonts fetched remotely.

## Supply-chain considerations

- All files are plain text (Markdown, shell, Python, HTML, JSON). There are no compiled binaries, no minified bundles, no `node_modules/`, no Git submodules.
- The `principles/PRINCIPLES.md` file is curated content refreshed by `scripts/refresh-principles.py`. The refresh script is currently a scaffold — it does not fetch live content.
