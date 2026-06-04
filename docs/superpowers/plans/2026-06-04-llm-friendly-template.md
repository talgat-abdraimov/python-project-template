# LLM-Friendly Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make python-project-template produce repositories that AI coding agents work in efficiently — dense AGENTS.md context, commands that work out of the box, zero doc rot.

**Architecture:** AGENTS.md becomes the single source of truth for AI context (open standard read by Codex/Cursor/Copilot/Gemini); CLAUDE.md is a one-line `@AGENTS.md` pointer for Claude Code. The init workflow fills placeholders into AGENTS.md for target repos. All broken out-of-box commands are fixed; untested example code is deleted.

**Tech Stack:** GitHub template repo, GitHub Actions, uv, just, ruff, pytest, Docker Compose.

**Spec:** `docs/superpowers/specs/2026-06-04-llm-friendly-template-design.md`

**Working branch:** `feature/llm-friendly-template` (already created)

---

### Task 1: Fix workflow LICENSE guard

**Files:**
- Modify: `.github/workflows/new-repo-created.yml` (the "Delete LICENSE file" step, around line 31)

- [ ] **Step 1: Add the missing `if` guard**

In `.github/workflows/new-repo-created.yml`, find:

```yaml
      - name: Delete LICENSE file
        run: |
```

Replace with:

```yaml
      - name: Delete LICENSE file
        if: steps.check.outputs.initial_commit == 'true'
        run: |
```

- [ ] **Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/new-repo-created.yml'))" && echo OK`
Expected: `OK`

(If PyYAML is missing locally, run `uv run --with pyyaml python3 -c "..."` with the same code.)

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/new-repo-created.yml
git commit -m "fix: guard LICENSE deletion to initial commit only"
```

---

### Task 2: Create TEMPLATE_AGENTS.md

**Files:**
- Create: `TEMPLATE_AGENTS.md`

- [ ] **Step 1: Write the file with exactly this content**

```markdown
# <reponame>

<description>

## Commands

| Command | When |
|---------|------|
| `just sync` | install/update deps (after clone, after pyproject.toml edits) |
| `just lint` | ruff check --fix + format |
| `just test` | pytest with coverage (gate: 80%) |
| `just check` | lint + test — run after every change, fix until green |
| `just build` | rebuild docker image (after dependency changes) |
| `just up` | start app via docker compose |

Bare `just` lists all commands. Add deps with `just add <pkg>` / `just add-dev <pkg>` — never edit pyproject.toml dependencies by hand.

## Stack

- Python 3.13, managed by `uv` (`uv.lock` committed)
- Lint/format: ruff — single quotes, line length 110, isort rules included
- Tests: pytest, `asyncio_mode = auto` (no `@pytest.mark.asyncio` needed), coverage fails under 80%
- Docker: `python:3.13-slim`, non-root user, `src/` volume-mounted for hot reload

## Structure

Start flat: modules directly in `src/`, tests mirror them in `tests/`.

When a second business domain appears, restructure to:

```
src/
├── entrypoints/        # app.py, consumer.py, scheduler.py — wiring only
├── domains/<name>/     # router.py, service.py, models.py, schemas.py
├── core/               # config.py, di.py, db.py, exceptions.py
└── clients/            # outbound HTTP clients
```

Rule: business logic lives only in `service.py` files. Transport files (routers, event handlers, schedulers) stay thin — parse input, call service, shape output.

## Rules

- Type hints on all function signatures
- After every change run `just check`; fix until green before committing
- Pre-commit hooks only scan `src/`; direct commits to main/master/develop are blocked
- Never commit secrets; env vars go in `.env` (gitignored)
```

- [ ] **Step 2: Verify length**

Run: `wc -l TEMPLATE_AGENTS.md`
Expected: ~50–60 lines

- [ ] **Step 3: Commit**

```bash
git add TEMPLATE_AGENTS.md
git commit -m "feat: add TEMPLATE_AGENTS.md (dense AI-agent context for target repos)"
```

---

### Task 3: Replace template's own CLAUDE.md with AGENTS.md + pointer; delete TEMPLATE_CLAUDE.md

**Files:**
- Create: `AGENTS.md`
- Modify: `CLAUDE.md` (replace entire content)
- Delete: `TEMPLATE_CLAUDE.md`

- [ ] **Step 1: Create `AGENTS.md` with exactly this content**

```markdown
# python-project-template — development guide

Template repository for new Python projects. You are working on the template itself, not a project created from it.

## Key files

- `TEMPLATE_AGENTS.md` — becomes `AGENTS.md` in repos created from this template; placeholders `<reponame>` and `<description>` are sed-replaced by the init workflow
- `AGENTS.md` (this file) — guide for developing the template itself
- `CLAUDE.md` — pointer (`@AGENTS.md`) so Claude Code loads this file; target repos inherit the same pattern
- `.github/workflows/new-repo-created.yml` — runs once in target repos on first push: deletes LICENSE, generates README.md and AGENTS.md, then deletes itself

## Commands

Same as target repos: `just sync / lint / test / check / build / up`. Bare `just` lists all.

## Rules for editing the template

- `TEMPLATE_AGENTS.md` must stay short (~50–60 lines) — dense facts only, no generic advice
- Only placeholders `<reponame>` and `<description>` are supported; adding new ones requires updating the sed calls in the init workflow
- Workflow changes only affect repos created after the change
- Keep `src/` minimal — every file added must be tested (coverage gate 80%) and free of doc rot

## Verification

- `just sync && just check` must pass on a fresh clone
- `just up` must work without manual docker setup
```

- [ ] **Step 2: Replace `CLAUDE.md` content entirely with**

```markdown
@AGENTS.md
```

- [ ] **Step 3: Delete TEMPLATE_CLAUDE.md**

Run: `git rm TEMPLATE_CLAUDE.md`

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md CLAUDE.md
git commit -m "feat: AGENTS.md as single source of truth, CLAUDE.md as pointer"
```

---

### Task 4: Update init workflow to generate AGENTS.md

**Files:**
- Modify: `.github/workflows/new-repo-created.yml` (the "Update Claude.md" step)

- [ ] **Step 1: Replace the entire "Update Claude.md" step with**

```yaml
      - name: Create AGENTS.md
        if: steps.check.outputs.initial_commit == 'true'
        run: |
          if [ -f "TEMPLATE_AGENTS.md" ]; then
            rm -f AGENTS.md
            cp TEMPLATE_AGENTS.md AGENTS.md

            REPO_NAME="${{ github.event.repository.name }}"
            REPO_DESC="${{ github.event.repository.description }}"

            if [ -z "$REPO_DESC" ]; then
              REPO_DESC="A Python project built with modern tooling and best practices"
            fi

            sed -i "s|<reponame>|${REPO_NAME}|g" AGENTS.md
            sed -i "s|<description>|${REPO_DESC}|g" AGENTS.md

            rm -f TEMPLATE_AGENTS.md

            git config user.name github-actions[bot]
            git config user.email github-actions[bot]@users.noreply.github.com
            git add AGENTS.md TEMPLATE_AGENTS.md
            git commit -m "Create AGENTS.md from template"
            git push
          else
            echo "TEMPLATE_AGENTS.md not found, skipping..."
          fi
```

Notes:
- Target repos inherit the template's `AGENTS.md` (template dev guide) — the `rm -f` + `cp` overwrites it with the filled project version.
- `CLAUDE.md` pointer needs no workflow handling — target repos inherit `@AGENTS.md` which is already correct.
- `<owner>`/`<date>` sed lines from the old step are dropped — TEMPLATE_AGENTS.md does not use them.

- [ ] **Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/new-repo-created.yml'))" && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/new-repo-created.yml
git commit -m "feat: init workflow generates AGENTS.md instead of CLAUDE.md"
```

---

### Task 5: Delete src/_http.py, drop httpx, unify Python 3.13

**Files:**
- Delete: `src/_http.py`
- Modify: `pyproject.toml` (lines 5–6: `requires-python`, `dependencies`)
- Modify: `uv.lock` (regenerated)

- [ ] **Step 1: Delete the file**

Run: `git rm src/_http.py`

- [ ] **Step 2: Update pyproject.toml**

Find:

```toml
requires-python = ">=3.12"
dependencies = ["httpx"]
```

Replace with:

```toml
requires-python = ">=3.13"
dependencies = []
```

- [ ] **Step 3: Regenerate lock and sync**

Run: `uv sync`
Expected: resolves with no production deps, dev group installs (pytest, ruff, etc.), `uv.lock` updated

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock src/_http.py
git commit -m "refactor: delete untested _http.py example, drop httpx, require Python 3.13"
```

---

### Task 6: Add sanity test so fresh repos pass pre-commit

**Files:**
- Create: `tests/test_sanity.py`

Fixes: bare `pytest` exits code 5 (no tests collected) → the always-run `pytest-check` pre-commit hook blocks every commit in fresh repos. The `import src` also guarantees coverage has data to report.

- [ ] **Step 1: Write the test**

```python
import src


def test_sanity():
    assert src is not None
```

- [ ] **Step 2: Run tests, verify they pass including coverage gate**

Run: `uv run pytest .`
Expected: `1 passed`, coverage table shows `src/__init__.py 0 0 100%`, total 100% ≥ 80% gate

If coverage errors with "No data to report": the `import src` line is missing — re-check Step 1.

- [ ] **Step 3: Commit**

```bash
git add tests/test_sanity.py
git commit -m "fix: add sanity test so fresh repos pass pytest pre-commit hook"
```

---

### Task 7: Fix docker-compose external network

**Files:**
- Modify: `docker-compose.yml`

- [ ] **Step 1: Replace entire file content with**

```yaml
x-common-variables: &common-variables
  DEBUG: False

services:
  app:
    build: .
    ports:
      - "8001:8000"
    volumes:
      - ./src:/app/src
    environment:
      <<: *common-variables
    command: echo "Hello, world!"
```

(Removes the `networks:` block — compose auto-creates a default network; `just up` no longer requires manual `docker network create app-network`.)

- [ ] **Step 2: Validate compose file**

Run: `docker compose config -q && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add docker-compose.yml
git commit -m "fix: drop external network so 'just up' works out of the box"
```

---

### Task 8: justfile default recipe

**Files:**
- Modify: `justfile` (add at the very top, before the `sync` recipe)

- [ ] **Step 1: Add as the first recipe in the file**

```just
# List available commands
default:
    @just --list
```

(Must be first — `just` with no arguments runs the first recipe.)

- [ ] **Step 2: Verify**

Run: `just`
Expected: list of all recipes with their comments

- [ ] **Step 3: Commit**

```bash
git add justfile
git commit -m "feat: bare 'just' lists commands"
```

---

### Task 9: Slim README

**Files:**
- Modify: `README.md` (replace entire content)

- [ ] **Step 1: Replace entire README.md with**

```markdown
# python project template :information_desk_person:

Highly opinionated template for modern Python projects: uv, just, ruff, pytest, Docker, pre-commit — plus an `AGENTS.md` so AI coding agents work efficiently out of the box.

> **Note:** Tested on macOS. Should work on Linux; Windows not guaranteed.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) — package manager
- [just](https://github.com/casey/just) — command runner
- Docker + Docker Compose

## Quick Start

1. Click **Use this template** → **Create a new repository**
2. Wait ~20 seconds — GitHub Actions customizes README and AGENTS.md, then removes itself
3. Clone your repository and enter it
4. `just sync` — install dependencies (creates .venv)
5. `pre-commit install` — enable git hooks
6. `just check` — verify everything passes
7. `just up` — start the app

## Commands

Run `just` to list all available commands.

## AI agents

`AGENTS.md` ([open standard](https://agents.md)) carries project context for Codex, Cursor, Copilot, Gemini, and others. `CLAUDE.md` points Claude Code at the same file. One source of truth — keep it short and factual.

## License

MIT — see LICENSE.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: slim README, point to 'just --list' and AGENTS.md"
```

---

### Task 10: Full verification

**Files:** none (verification only)

- [ ] **Step 1: Fresh-state checks**

```bash
just sync
just check
```

Expected: lint clean, `1 passed`, coverage gate satisfied.

- [ ] **Step 2: Docker out-of-box check**

```bash
just build
just up
just down
```

Expected: builds, prints `Hello, world!`, exits cleanly — no manual network creation.

- [ ] **Step 3: Context-file checks**

```bash
wc -l TEMPLATE_AGENTS.md          # ~50–60
cat CLAUDE.md                      # exactly: @AGENTS.md
grep -c "initial_commit == 'true'" .github/workflows/new-repo-created.yml   # 4 (check + LICENSE + README + AGENTS.md steps; self-removal step also guarded = 5 if counting it)
ls TEMPLATE_CLAUDE.md src/_http.py 2>&1                                     # both: No such file
```

- [ ] **Step 4: Push branch and open PR**

```bash
git push -u origin feature/llm-friendly-template
gh pr create --title "LLM-friendly template: AGENTS.md standard + out-of-box fixes" --body "See docs/superpowers/specs/2026-06-04-llm-friendly-template-design.md"
```

---

## Post-merge note (manual, not in this plan)

The init workflow only affects repos created **after** merge. Existing repos created from the old template keep their long CLAUDE.md — migrate them manually if desired.
