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
- Docker: `python:3.13-slim-bookworm`, non-root user, `src/` volume-mounted for hot reload

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
