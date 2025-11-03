# CLAUDE.md

This file provides guidance to Claude Code (CLAUDE.ai/code) when working with code in this repository.

## Repository Context

This is **python-project-template** - a template repository for creating new Python projects with modern tooling and best practices. You are working on the template itself, not a project created from it.

### Key Files

- **`TEMPLATE_CLAUDE.md`**: Instructions template for target repositories (gets copied to `CLAUDE.md` in new repos)
- **`CLAUDE.md`** (this file): Development guide for this template repository
- **`.github/workflows/new-repo-created.yml`**: Initialization workflow that customizes new repositories

## Development Commands

### Setup
```bash
uv venv                    # Create virtual environment
source .venv/bin/activate  # Activate (macOS/Linux)
just dev-deps              # Install development dependencies
```

### Development Workflow
```bash
just lint                  # Run ruff linting and formatting
just test                  # Run pytest tests
just check                 # Run all quality checks (lint + test)
just clean                 # Clean cache and temporary files
```

### Docker
```bash
just build                 # Build Docker container (no cache)
just up                    # Start application
just up -d                 # Start in detached mode
just stop                  # Stop application
just down                  # Stop and remove containers/volumes
just logs                  # View logs
just logs -f               # Follow logs
```

### Dependency Management
Dependencies are managed using `uv` with `.in` files:
```bash
# Add to requirements.in or dev-requirements.in, then:
just deps                  # Compile and install production dependencies
just dev-deps              # Compile and install dev dependencies
```

The `just dev-deps` command automatically compiles both `requirements.txt` and `dev-requirements.txt` from their `.in` files.

## Testing

### Run All Tests
```bash
just test                  # or: pytest .
```

### Run Specific Tests
```bash
pytest tests/test_file.py                    # Single file
pytest tests/test_file.py::test_function     # Single test
pytest -k "test_pattern"                     # Tests matching pattern
pytest -v                                    # Verbose output
pytest --cov=src                             # With coverage
```

### Pre-commit Hooks
Pre-commit hooks run automatically on commit and include:
- Syntax checking (AST validation)
- JSON/TOML validation
- Ruff linting and formatting
- Trailing whitespace removal
- pytest tests

Block commits to main/master/develop branches by default.

```bash
pre-commit install                    # Install hooks
pre-commit run --all-files           # Run manually on all files
```

## Architecture

### Template Initialization Workflow

When a new repository is created from this template, `.github/workflows/new-repo-created.yml` runs on the first push to main:

1. **Checks if initial commit**: Only runs once on repository creation
2. **Deletes LICENSE**: Template license removed (users add their own)
3. **Generates README.md**: Creates custom README with repository name and setup instructions
4. **Creates CLAUDE.md**: Copies `TEMPLATE_CLAUDE.md` → `CLAUDE.md` (uppercase) and replaces placeholders:
   - `<reponame>` → actual repository name
   - `<description>` → repository description (or default)
   - `<owner>` → repository owner
   - `<date>` → current date
5. **Configures branch protection**: Sets up main branch protection requiring:
   - Pull request reviews (1 approver required)
   - Stale review dismissal
   - Conversation resolution before merge
   - No force pushes or deletions
6. **Self-destructs**: Removes the workflow file itself

### File Naming Strategy

- **`CLAUDE.md`** (lowercase): This file, for template repository development
- **`TEMPLATE_CLAUDE.md`**: Template for target repositories
- **`CLAUDE.md`** (uppercase): Generated in target repositories from `TEMPLATE_CLAUDE.md`

This separation prevents conflicts between template development and target repositories.

### Docker Configuration

The Docker setup uses:
- **Base image**: `python:3.12.0-slim-bookworm`
- **Non-root user**: Runs as user ID 1000 for security
- **Volume mount**: `./src:/app/src` for development hot-reload
- **Network**: Uses external `app-network` (must be created manually: `docker network create app-network`)
- **Port mapping**: 8001 (host) → 8000 (container)

The default command is `echo "Hello, world!"` - intended to be overridden in target repositories.

### Dependency Structure

```
requirements.in          → requirements.txt (compiled by uv)
dev-requirements.in      → dev-requirements.txt (compiled by uv)
  ↓ includes
requirements.in
```

Development dependencies automatically include production dependencies via `-r requirements.in`.

## Modifying the Template

### Updating TEMPLATE_CLAUDE.md

This file becomes the `CLAUDE.md` in target repositories. When editing:
- Use placeholders: `<reponame>`, `<description>`, `<owner>`, `<date>`
- Keep instructions generic and framework-agnostic
- Test workflow replacement logic if changing placeholders

### Updating the Initialization Workflow

The workflow (`.github/workflows/new-repo-created.yml`):
- Only runs when `is_template` is false (i.e., in target repos, not the template itself)
- Uses `sed` for placeholder replacement
- Each step commits separately with `github-actions[bot]` as the author
- Final step removes itself

**Critical**: Changes to this workflow only affect new repositories created after the change.

### Adding Example Code

Place minimal example code in `src/` to demonstrate:
- Project structure
- Best practices
- Integration with tooling (pytest, ruff, Docker)

Keep it generic and easily removable by users.

## Code Quality Standards

- **Python version**: 3.13+ (updated from 3.10)
- **Type hints**: Required for all functions
- **Docstrings**: Required for modules, classes, and public functions
- **Formatting**: Automated with Ruff
- **Testing**: pytest with async support (`pytest-asyncio`)
- **Coverage**: Available via `pytest-cov`

## Pre-commit Configuration Notes

- **Scope**: Only runs on files in `src/` directory (configured via `files: ^src/`)
- **Fail fast**: Stops on first error for faster feedback
- **Branch protection**: Blocks direct commits to main/master/develop
- **Python version**: Uses Python 3.12 for pre-commit hooks

## Platform Support

Primarily tested on **macOS**. Linux support expected but not guaranteed. Windows compatibility uncertain.
