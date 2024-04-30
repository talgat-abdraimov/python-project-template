dev-deps:
  # Compile and Install dev dependencies
	pip-compile -o dev-requirements.txt dev-requirements.in

deps:
  # Compile and Install dependencies
  pip-compile -o requirements.txt requirements.in

ruff:
  # Run ruff checks
	ruff check --fix
	ruff format

test:
  # Run tests
	pytest .
