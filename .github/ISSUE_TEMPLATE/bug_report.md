---
name: Bug report
about: Something isn't working as documented
title: "bug: "
labels: bug
---

**What happened**
A clear, one-paragraph description of the bug.

**What you expected to happen**
What you thought the behavior would be.

**Reproduction**
Steps to reproduce. The smallest possible example is the most useful.

```
1. git clone ...
2. ./scripts/install.sh /tmp/demo --dry-run
3. ...
```

**Environment**
- OS and version:
- Bash version (`bash --version`):
- Git version (`git --version`):
- Build.MD commit SHA (`git rev-parse HEAD`):
- Which agent(s) you use (Claude Code, Cursor, Codex, Copilot, VS Code, Gemini):

**Install receipt (if applicable)**
Paste the contents of `.build-md-install-receipt.txt` from the target directory.

**Additional context**
Anything else that might help — logs, screenshots of the dashboard, etc.
