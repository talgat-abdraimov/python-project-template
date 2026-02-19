# python project template :information_desk_person:

This is a highly opinionated template for Python projects that provides a solid foundation for building modern Python applications with best practices and modern tooling.

> **Note:** This project has been tested and verified only on macOS. While it may work on other operating systems, we cannot guarantee full compatibility.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher

- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [just](https://github.com/casey/just) - Command runner
- Docker and Docker Compose - For containerization

## Quick Start

1. On GitHub.com, navigate to the main page of the [repository](https://github.com/talgat-abdraimov/python-project-template).

2. Above the file list, click **Use this template**.

3. Select **Create a new repository**.

4. Type a name for your repository, and an optional description.

5. Click **Create repository from template**.

6. Wait about **20 seconds** then refresh this page. [GitHub Actions](https://docs.github.com/en/actions) will automatically update the README.md.

7. Clone your locally created repository:
   ```bash
   git clone git@github.com/{your-new-repo}.git
   ```
   Then open the project in your favorite IDE.

8. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   pip install uv
   ```

9. Sync dependencies (creates virtual environment automatically):
   ```bash
   just sync
   ```

10. Build the Docker container:
    ```bash
    just build
    ```

11. Start the application:
    ```bash
    just up
    ```

## Project Structure

```
python-project-template/
├── .github/              # GitHub Actions workflows
├── src/                  # Source code
├── tests/                # Test files
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── pyproject.toml        # Project config, dependencies, tool settings
├── uv.lock              # Dependency lock file
├── justfile             # Just commands
└── docker-compose.yml   # Docker configuration
```

## Available Commands

The following commands are available in the justfile:

| Command | Description |
|---------|-------------|
| `sync` | Sync all dependencies (creates .venv automatically) |
| `sync-prod` | Sync production dependencies only |
| `add <pkg>` | Add a production dependency |
| `add-dev <pkg>` | Add a development dependency |
| `remove <pkg>` | Remove a dependency |
| `build` | Build the Docker container |
| `up` | Start the application |
| `stop` | Stop the application |
| `down` | Stop and remove containers |
| `lint` | Run code linting and formatting |
| `test` | Run tests |
| `check` | Run lint + test |
| `clean` | Clean cache and temporary files |

## Development Tools

### just

Just is a command runner that simplifies running project commands. You can install it using your package manager:

- macOS: `brew install just`
- Linux: `sudo apt-get install just` or equivalent for your distribution
- Windows: `choco install just` or `scoop install just`

[see more](https://github.com/casey/just)

### pre-commit

Before you can run hooks, you must have the pre-commit package manager installed. It helps maintain code quality by running checks before each commit.

[see more](https://pre-commit.com/)

### ruff

Ruff aims to be significantly faster than alternative tools while integrating more functionality behind a single, common interface. It's used for linting and formatting Python code.

[see more](https://docs.astral.sh/ruff/)

### pytest

The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

[see more](https://docs.pytest.org/en/7.4.x/)

### uv

An extremely fast Python package manager and project tool, written in Rust. Manages dependencies, virtual environments, and lock files natively.

[see more](https://github.com/astral-sh/uv)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
