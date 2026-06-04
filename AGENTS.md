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
