# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->


## Build & Test

There is no Makefile and no test framework — this is a directory of standalone
scripts, and most have no tests. Nothing is built; scripts run from `~/bin`,
which is on PATH.

```bash
shellcheck -s bash vm vm-test   # lint (brew install shellcheck)
./vm-test                       # the one suite that exists: 55 checks, ~1s, no VM
```

If you add tests for another script, follow `vm-test`: a plain executable
alongside the script it covers, fast enough to run every time, no dependencies.

## Architecture Overview

Flat collection of ~40 independent scripts, each solving one problem, plus a
few data files they read. There is no shared library and no build step; scripts
do not import each other. Treat each as its own project.

The larger ones worth knowing: `vm` (disposable Ubuntu VMs over multipass, with
`vm-test` and `vm-cloud-init/`), `worklog` and `timesheet-sheet` (evidence
harvesting for timesheet reconstruction), `init_python_project`, and
`git-show-branches`.

## Conventions & Patterns

- **New scripts**: `#!/usr/bin/env bash` + `set -euo pipefail`, a `show_help()`
  heredoc, and `-h|--help`. `git-show-branches` and `vm` are the models. Older
  scripts use `#!/bin/sh` or `#!/bin/bash`; leave them alone rather than
  converting.
- **Non-interactive flags everywhere** — see AGENTS.md. `rm`/`cp`/`mv` are
  aliased to `-i` in this user's shell and will hang an agent until timeout.
- **Comments explain why, not what.** The audience is a senior dev re-reading
  this in a year, usually to answer "why is this done the hard way?"
- **Destructive paths are guarded and never tested against live state.** `vm`
  has `VM_PROTECTED`; `vm-test` only ever names a VM that cannot exist. A guard
  that fails open has already destroyed a real VM here once.
- **Bash traps that have bitten this repo**: errexit is suppressed through a
  function's entire body when it is called from `if`, `&&` or `||`, so guard
  steps inside the function rather than at the call site; and `[[ "$a" == "$b" ]]`
  compares literally because the right side is quoted — leave it unquoted when
  you want a glob.
