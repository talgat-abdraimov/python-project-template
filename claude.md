# Claude AI Development Guide

This document helps AI assistants (like Claude) understand your project structure and assists developers in using AI effectively for development tasks.

## Project Overview

**Repository**: <reponame>  
**Description**: <description>

This project is built on a modern Python template with best practices and modern tooling. The project is designed to be framework-agnostic and provides a solid foundation for building Python applications.

### Tech Stack
- **Python**: 3.10+
- **Package Manager**: `uv` (fast Rust-based package installer)
- **Task Runner**: `just` (command runner for project tasks)
- **Testing**: `pytest`
- **Code Quality**: `ruff` (linting and formatting)
- **Pre-commit**: Automated code quality checks
- **Containerization**: Docker and Docker Compose

### Project Structure
```
<reponame>/
├── .github/                    # GitHub Actions workflows (CI/CD)
├── src/                        # Application source code
├── tests/                      # Test files (pytest)
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── dev-requirements.in        # Development dependencies
├── requirements.in            # Production dependencies
├── justfile                   # Command definitions (similar to Makefile)
└── docker-compose.yml         # Docker container configuration
```

## AI-Assisted Development Workflow

### Getting Started with This Project

When helping with this project, AI assistants should:

1. **Understand the Context**
   - Review the repository name (<reponame>) and description
   - Check existing code in `src/` to understand the project domain
   - Look at `requirements.in` to see dependencies and infer architecture

2. **Follow Existing Patterns**
   - Match the code style of existing files
   - Use similar naming conventions
   - Follow the established project structure

3. **Maintain Quality Standards**
   - All code must pass `just ruff`
   - All features need tests that pass `just test`
   - Type hints are mandatory
   - Docstrings are required

### Working with Dependencies

**Adding New Dependencies:**
```bash
# Production dependency
echo "package-name" >> requirements.in
just deps

# Development dependency
echo "package-name" >> dev-requirements.in
just dev-deps
```

**Important**: Always add dependencies to `.in` files, not `.txt` files. The `uv` tool will compile them.

### Code Quality Standards

This project enforces high code quality through:

1. **Ruff**: Fast linting and formatting
   - Run before committing: `just ruff`
   - Ruff replaces multiple tools (black, isort, flake8, etc.)
   
2. **Pre-commit hooks**: Automatic checks on commit
   - Install: `pre-commit install`
   - Manually run: `pre-commit run --all-files`

3. **Testing**: pytest for all tests
   - Run tests: `just test`
   - Write tests in `tests/` directory
   - Follow pytest conventions

### Available Commands (justfile)

When working with this project, use these commands:

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `just venv` | Create virtual environment | Initial setup |
| `just dev-deps` | Install dev dependencies | After cloning, adding dev deps |
| `just deps` | Install production dependencies | After adding production deps |
| `just build` | Build Docker container | When Docker config changes |
| `just up` | Start application | Running the app |
| `just stop` | Stop application | Pausing the app |
| `just down` | Stop and remove containers | Clean shutdown |
| `just ruff` | Lint and format code | Before committing |
| `just test` | Run all tests | Before committing, in CI |

## AI Development Guidelines

### When Writing Code

1. **Follow Python Best Practices**
   - Type hints for all functions
   - Docstrings for modules, classes, and functions
   - Keep functions small and focused
   - Use meaningful variable names

2. **Testing First**
   - Write tests alongside code
   - Aim for high test coverage
   - Use pytest fixtures for common setups
   - Test edge cases and error conditions

3. **Code Organization**
   - Place all application code in `src/`
   - Keep tests in `tests/` mirroring `src/` structure
   - Use `__init__.py` files appropriately
   - Separate concerns into modules

### When Modifying Files

**Always Run Quality Checks:**
```bash
just ruff  # Format and lint
just test  # Run tests
```

**Before Suggesting Code:**
- Ensure it follows the project's patterns
- Include appropriate type hints
- Add or update tests
- Consider Docker compatibility (if containerized)

### Common Tasks and AI Assistance

**Creating a New Module:**
```python
# src/my_module.py
"""Module description.

This module provides...
"""

from typing import Any


def my_function(param: str) -> dict[str, Any]:
    """Function description.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    return {"result": param}
```

**Adding a Test:**
```python
# tests/test_my_module.py
"""Tests for my_module."""

import pytest
from src.my_module import my_function


def test_my_function():
    """Test my_function with valid input."""
    result = my_function("test")
    assert result == {"result": "test"}


def test_my_function_edge_case():
    """Test my_function with edge case."""
    # Test edge cases here
    pass
```

**Updating Dependencies:**
When suggesting new packages:
1. Check if the package is necessary
2. Prefer well-maintained, popular packages
3. Add to appropriate `.in` file
4. Document why the dependency is needed

### Docker Development

**When Working with Docker:**
- Ensure Python code is compatible with the container environment
- Update `docker-compose.yml` if new services are needed
- Rebuild container after dependency changes: `just build`
- Test both locally and in container

### Environment Variables

**Best Practices:**
- Never commit secrets or credentials
- Use `.env` files (add to `.gitignore`)
- Document required environment variables
- Provide `.env.example` template

## Context for AI Assistants

### Project Philosophy
- **Modern Tooling**: Uses latest Python tools (uv, ruff, just)
- **Developer Experience**: Focus on fast, simple commands
- **Code Quality**: Automated checks and high standards
- **Testing**: Comprehensive test coverage expected
- **Docker First**: Application should run in containers

### Conventions
- Use `just` commands instead of direct tool invocation
- All code must pass `ruff` checks
- All code should have tests
- Type hints are mandatory
- Docstrings follow Google or NumPy style

### When to Suggest Refactoring
- Functions longer than 50 lines
- Modules longer than 500 lines
- Code duplication (DRY principle)
- Poor separation of concerns
- Missing tests or type hints

## Quick Reference for AI

**Adding a Feature:**
1. Create module in `src/`
2. Write tests in `tests/`
3. Add dependencies to `requirements.in` if needed
4. Run `just deps` (if dependencies added)
5. Run `just ruff` and `just test`
6. Commit (pre-commit hooks will run)

**Debugging Issues:**
1. Check test output: `just test -v`
2. Check linting: `just ruff`
3. Check Docker logs: `docker-compose logs`
4. Verify dependencies: `uv pip list`

**Best Practices Checklist:**
- [ ] Code has type hints
- [ ] Code has docstrings
- [ ] Tests are written
- [ ] `just ruff` passes
- [ ] `just test` passes
- [ ] No hardcoded secrets
- [ ] Dependencies documented

## Project-Specific Context

### Current Architecture
<!-- Update this section as your project evolves -->
- Framework: [Specify if using Flask, FastAPI, Django, etc.]
- Database: [Specify if using PostgreSQL, MongoDB, etc.]
- External APIs: [List any external services]

### Domain Knowledge
<!-- Add domain-specific information that AI should know -->
- Business logic: [Key business rules or domain concepts]
- Data models: [Important data structures or entities]
- User workflows: [How users interact with the system]

### Known Limitations
<!-- Document any technical debt or known issues -->
- [Issue 1]
- [Issue 2]

### Future Plans
<!-- Help AI understand the roadmap -->
- [Planned feature 1]
- [Planned feature 2]

## Notes for Specific Scenarios

### Web Framework (if adding)
If adding Flask, FastAPI, or Django:
- Add framework to `requirements.in`
- Update `docker-compose.yml` with appropriate ports
- Configure application in `src/`
- Add health check endpoints
- Update tests for API endpoints

### Database (if adding)
If adding database support:
- Choose ORM (SQLAlchemy, Tortoise, etc.)
- Add to `requirements.in`
- Create `migrations/` directory
- Add database service to `docker-compose.yml`
- Use environment variables for connection strings
- Add database fixtures for tests

### CLI Application (if creating)
If building CLI tool:
- Consider using `click` or `typer`
- Add console_scripts entry point
- Add comprehensive help text
- Include input validation
- Add CLI tests

## Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure virtual environment is activated
2. **Dependencies Not Found**: Run `just deps` or `just dev-deps`
3. **Tests Failing**: Check test output, verify fixtures
4. **Ruff Errors**: Run `just ruff` to auto-fix formatting
5. **Docker Issues**: Rebuild with `just build`

## Additional Resources

- Repository: https://github.com/<owner>/<reponame>
- Documentation: [Link to docs if available]
- Issue Tracker: https://github.com/<owner>/<reponame>/issues

---

**For AI Assistants**: This document provides context about the project structure, conventions, and best practices. When helping users, prioritize code quality, testing, and following the established patterns. Always suggest running `just ruff` and `just test` before committing code. Reference this document when making architectural decisions or suggesting new features.

**Last Updated**: <date>
