# Contributing to GitSpec

GitSpec is a **released skills pack**, not an actively-maintained service. Pull requests and issues are welcome but there is no commitment that any PR or issue will be reviewed, responded to, or merged. If you need guaranteed maintenance or continuous development, please fork the project — the MIT License explicitly permits this.

If you'd still like to contribute upstream, the guidelines below describe what a good contribution looks like.

## What belongs in GitSpec

**Good fits:**
- Fixes to the installer, hooks, or helper scripts.
- New platform adapters (new AI agents or editors that need their own config format).
- New slash commands that map directly to the documented layers.
- Clarifications and corrections to SKILL.md or README.md.
- Additional schema validators or rule templates.

**Probably out of scope:**
- New layers in the nine-layer architecture.
- New runtime dependencies (Python packages, Node modules, shell libraries).
- External service integrations (Jira, Linear, Slack, etc.). GitSpec is repo-native by design.
- Telemetry, analytics, or any network call during install.

## Workflow

1. **Fork and branch.** Work on a topic branch named `feat/...`, `fix/...`, or `docs/...`.
2. **Dogfood the tool.** If you change `install.sh`, run `./scripts/install.sh /tmp/test-repo --dry-run` and then a real install into a scratch repo before opening the PR.
3. **Run the smoke test.** `bash ci/smoke.sh` should pass locally.
4. **Open a PR** against `main`. Explain the motivation in the description.

## Commit style

Commit messages follow the same convention GitSpec installs for its users:

```
<type>: <short imperative summary>

<optional body explaining what changed and why>
```

Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`.

## Code standards

- **Bash:** `set -euo pipefail`. `shellcheck scripts/*.sh ci/smoke.sh` should pass.
- **Python:** Python 3.9+ standard library only. No `pip install`. Keep scripts self-contained.
- **Markdown:** YAML frontmatter where the schema requires it. Line length is not enforced — prioritize readability.

## What a good PR looks like

- One logical change per PR.
- Tests or a smoke-test update if the change is non-trivial.
- Documentation updated in the same PR.
- A PR description that explains the motivation, not just the diff.

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License (see `LICENSE`).
