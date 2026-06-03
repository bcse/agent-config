---
name: python-pre-commit-hooks
description: Use when a Python project needs a git pre-commit hook that runs lint, format, type-check, and tests before each commit (uv/ruff/ty/mypy/pytest projects), or when asked to "add a pre-commit hook", "enforce checks on commit", or "set up git hooks".
---

# Setting Up Python Pre-Commit Hooks

## Overview

Install a **version-controlled** git `pre-commit` hook that runs the project's quality gates (lint, format-check, type-check, tests) before every commit. A failing check aborts the commit.

**Core principle:** Keep the hook *in the repo* under `.githooks/` and point git at it with `core.hooksPath` — never hand-copy scripts into `.git/hooks/` (untracked, drifts per-clone). Every contributor runs one install script and gets the same checks.

## When to Use

- A Python repo wants commits gated on `ruff` / `ty` / `mypy` / `pytest`.
- User asks to "add a pre-commit hook", "enforce formatting on commit", or "set up git hooks".

**When NOT to use:**
- The repo already uses the [`pre-commit` framework](https://pre-commit.com/) (`.pre-commit-config.yaml`) — extend that instead.
- You only need to gate on the server (CI) — use a CI workflow, not a local hook.

## The Pattern (3 pieces)

| File | Role |
|------|------|
| `.githooks/pre-commit` | POSIX `sh` script; the actual checks. Tracked in git. |
| `scripts/install-pre-commit.sh` | Sets `git config --local core.hooksPath .githooks` (idempotent, refuses to clobber a foreign value). |
| `scripts/uninstall-pre-commit.sh` | Unsets `core.hooksPath` only if it points at this repo's `.githooks`. |

Ready-to-copy versions live in `assets/` within this skill.

## Setup Steps

1. **Copy the templates** into the target repo:
   - `assets/pre-commit` → `.githooks/pre-commit`
   - `assets/install-pre-commit.sh` → `scripts/install-pre-commit.sh`
   - `assets/uninstall-pre-commit.sh` → `scripts/uninstall-pre-commit.sh`
2. **Adapt the checks** in `.githooks/pre-commit` to the project's toolchain (see table below). Only keep commands for tools the project actually uses.
3. **Make them executable:** `chmod +x .githooks/pre-commit scripts/*.sh`
4. **Install:** `sh scripts/install-pre-commit.sh`
5. **Verify it runs** without committing: `.githooks/pre-commit` (run it directly — it should print each `==>` step and exit 0 on a clean tree).
6. **Commit** the three files so collaborators can `sh scripts/install-pre-commit.sh` after cloning. Document that one line in the README/AGENTS.md.

## Adapting the Checks

Match each line in `.githooks/pre-commit` to what the project has:

| If the project uses... | Hook line |
|------------------------|-----------|
| ruff (lint)            | `run ruff check` |
| ruff (format)          | `run ruff format --check` |
| ty (Astral type checker) | `run ty check` |
| mypy                   | `run mypy .` |
| pyright                | `run pyright` |
| pytest via uv          | `run uv run pytest` |
| pytest (no uv)         | `run pytest` |

**Type checker — prefer `ty`:** Use exactly one. If the repo already depends on `mypy` or `pyright` (check `pyproject.toml` / lockfile), keep that one. Otherwise default to Astral's `ty` (`run ty check`).

Detect what's present before keeping a line: check `pyproject.toml` for `[tool.ruff]` and `mypy`/`pyright`/`ty`/`pytest` entries in dependencies.

## Why `core.hooksPath` (not `.git/hooks/`)

- **Versioned & shared:** the hook lives in the repo; `.git/hooks/` is local-only and never cloned.
- **One toggle:** install/uninstall flip a single config value instead of copying/deleting files.
- **No clobber:** the install script refuses to overwrite a `core.hooksPath` that points elsewhere, so it won't fight other tooling.
- Requires Git ≥ 2.9 (standard everywhere today).

## Bypassing

For an emergency commit that must skip checks: `SKIP_PRE_COMMIT=1 git commit -m "..."`. Rename the env var per-project (e.g. `MYPROJ_SKIP_PRE_COMMIT`) by editing the guard at the top of `.githooks/pre-commit`. Prefer fixing the failure over routine bypassing — and never bypass on shared branches without saying so.

## Common Mistakes

- **Copying into `.git/hooks/`** — untracked, drifts, not shared. Use `core.hooksPath`.
- **`#!/bin/bash` + bashisms** — keep it `#!/bin/sh` POSIX so it runs everywhere; the templates already do.
- **Forgetting `chmod +x`** — git won't run a non-executable hook. The install script re-applies `chmod +x` defensively.
- **Slow hooks** — a multi-minute test suite makes people bypass the hook. If `pytest` is slow, scope it (e.g. fast subset) and run the full suite in CI.
- **Leaving checks for tools the repo doesn't have** — every `run` line must be a command that exists, or every commit fails.

## Verifying It Works

```sh
sh scripts/install-pre-commit.sh
git config --local --get core.hooksPath     # -> .githooks
.githooks/pre-commit                         # runs all checks, exits 0 on clean tree
# Introduce a lint error, then attempt a commit -> it should be blocked.
```
