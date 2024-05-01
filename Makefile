dev-deps:
	@echo "Compiling and Installing dev-requirements.txt..."
	@pip-compile -o dev-requirements.txt dev-requirements.in
	@pip install -r dev-requirements.txt

deps:
	@echo "Compiling and Installing requirements.txt..."
	@pip-compile -o requirements.txt requirements.in
	@pip install -r requirements.txt

ruff:
  # Run ruff checks
	ruff check --fix
	ruff format

test:
  # Run tests
	pytest .
