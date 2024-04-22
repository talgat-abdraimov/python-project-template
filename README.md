# python project template :information_desk_person:

This is a highly opinionated template for Python projects.

---

## Usage

1. On GitHub.com, navigate to the main page of the [repository](https://github.com/talgat-abdraimov/python-project-template).

2. Above the file list, click **Use this template**.

3. Select **Create a new repository**.

4. Type a name for your repository, and an optional description.

5. Click **Create repository from template**.

6. Wait about 20 seconds then refresh this page. [GitHub Actions](https://docs.github.com/en/actions) will automatically update the README.md

7. Clone locally created repository `git clone git@github.com/{your-new-repo}.git` and open the project in your fav IDE.

8. Create a virtual environment for project `python -m venv venv` then activate it `source ./venv/bin/activate`

9. Install [pip-tools](https://pip-tools.readthedocs.io/en/stable/) `pip install pip-tools` and type in terminal `make dev-deps`

## Tools

### pre-commit

Before you can run hooks, you must have the pre-commit package manager installed.

[see more](https://pre-commit.com/)

### ruff

Ruff aims to be significantly faster than alternative tools while integrating more functionality behind a single, common interface.

[see more](https://docs.astral.sh/ruff/)

### pytest

The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries. [see more](https://docs.pytest.org/en/7.4.x/)
