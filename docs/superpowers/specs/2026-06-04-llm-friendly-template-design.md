# LLM-Friendly Template Redesign

**Date**: 2026-06-04
**Repo**: talgat-abdraimov/python-project-template
**Goal**: Make the template produce repositories that AI coding agents (Claude Code, Codex, Cursor, Copilot, Gemini) can work in efficiently.

## Problem

The template's AI-context file (`TEMPLATE_CLAUDE.md`, ~400 lines) is mostly generic advice LLMs already know, contains placeholder sections agents misread as content, and contradicts other files (Python 3.12 vs 3.13). Several commands fail out of the box (`just up` needs a manually created Docker network; `pytest` exits code 5 on fresh repos and blocks every commit via the pre-commit hook). `src/_http.py` has docstring rot and no tests, so the 80% coverage gate fails on fresh repos. The init workflow's "Delete LICENSE" step is missing its initial-commit guard, so it runs (and fails) on every push to main.

LLM-friendly means three properties:
1. **Dense context files** — facts only, no tutorials
2. **Self-verifying loops** — commands that work out of the box and fail loudly
3. **Zero doc rot** — no misleading documentation

## Design

### 1. File strategy — AGENTS.md as single source of truth

| File | Template repo | Target repo (after init) |
|------|--------------|--------------------------|
| `TEMPLATE_AGENTS.md` | source with placeholders | renamed to `AGENTS.md`, placeholders sed-filled |
| `AGENTS.md` | template development guide (replaces current CLAUDE.md content, slimmed) | generated from template |
| `CLAUDE.md` | single line: `@AGENTS.md` | single line: `@AGENTS.md` |

- `TEMPLATE_CLAUDE.md` is deleted (replaced by `TEMPLATE_AGENTS.md`).
- Claude Code loads `CLAUDE.md`, follows the `@AGENTS.md` import. Codex, Cursor, Copilot, and Gemini read `AGENTS.md` natively.
- Placeholders kept: `<reponame>`, `<description>`, `<owner>`, `<date>`.

### 2. TEMPLATE_AGENTS.md content (~50 lines)

Sections, in order:

1. **Header** — repo name + description (placeholders)
2. **Commands** — `just sync / lint / test / check / up / build` one line each with when-to-use
3. **Stack facts** — Python 3.13, uv (lock committed), ruff (single quotes, line length 110), pytest (asyncio_mode=auto, coverage gate 80%)
4. **Structure convention** — growth path: start flat in `src/`; when a second business domain appears, restructure to:
   ```
   src/
   ├── entrypoints/        # app.py, consumer.py, scheduler.py — wiring only
   ├── domains/<name>/     # router.py, service.py, models.py, schemas.py
   ├── core/               # config.py, di.py, db.py, exceptions.py
   └── clients/            # outbound HTTP clients
   ```
   One rule: business logic lives only in `service.py`; transport files (routers, handlers, schedulers) stay thin.
5. **Gotchas** — pre-commit only scans `^src/`; direct commits to main/master/develop blocked
6. **Verification loop** — after every change run `just check`; fix until green before committing

Cut entirely: pytest tutorials, example code blocks, best-practice checklists, roadmap/known-limitations placeholder sections, generic troubleshooting.

### 3. Bug fixes

1. **Workflow LICENSE guard** — add `if: steps.check.outputs.initial_commit == 'true'` to the "Delete LICENSE file" step
2. **Workflow generates AGENTS.md** — copy `TEMPLATE_AGENTS.md` → `AGENTS.md`, sed placeholders, write one-line `CLAUDE.md` pointer, remove `TEMPLATE_AGENTS.md`
3. **docker-compose.yml** — drop `external: true` network so `just up` works without manual `docker network create`
4. **Fresh-repo pytest exit 5** — add minimal `tests/test_sanity.py` so pytest collects ≥1 test and the pre-commit hook passes
5. **Version unify** — Python 3.13 everywhere: `requires-python = ">=3.13"`, Dockerfile and pre-commit already 3.13
6. **justfile default recipe** — bare `just` lists available commands (`@just --list`)
7. **README slim** — remove the duplicated commands table; point to `just --list`; keep human-oriented quick-start

### 4. Delete src/_http.py

Removed entirely. Rationale: docstring rot (documents a `response_handler` constructor param that does not exist; `HttpClientError` docstring references nonexistent `BaseError`), zero tests (fails the 80% coverage gate), and it makes the template less framework-agnostic. `src/` ships with only `__init__.py`.

## Out of scope

- No DDD/layered scaffolding in the template itself (structure is documented as a convention in AGENTS.md, not pre-created)
- No changes to ruff/pytest tool configuration beyond the version bump
- No new example code in `src/`

## Verification

- Fresh clone: `just sync && just check` passes
- `just up` starts without manual network creation
- `just` alone prints the command list
- Repo created from template: init workflow runs once, produces filled `AGENTS.md` + pointer `CLAUDE.md`, deletes itself; subsequent pushes to main trigger nothing
- `wc -l TEMPLATE_AGENTS.md` ≈ 50–60
