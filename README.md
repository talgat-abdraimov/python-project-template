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
