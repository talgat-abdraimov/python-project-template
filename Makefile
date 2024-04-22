dev-deps:
  # Install dependencies
	pip-compile -o dev-requirements.txt dev-requirements.in

ruff:
  # Run ruff checks
	ruff check --fix
	ruff format

test:
  # Run tests
	pytest .
