venv:
	@echo "Creating virtual environment..."
	@uv venv

dev-deps:
	@echo "Compiling and Installing dev-requirements.txt..."
	@uv pip compile -o requirements.txt requirements.in
	@uv pip compile -o dev-requirements.txt dev-requirements.in
	@uv pip install -r dev-requirements.txt

deps:
	@echo "Compiling and Installing requirements.txt..."
	@uv pip compile -o requirements.txt requirements.in
	@uv pip install -r requirements.txt

build:
	@echo "Building the server..."
	@docker compose build

up:
	@echo "Starting the server..."
	@docker compose up -d

stop:
	@echo "Stopping the server..."
	@docker compose stop

down:
	@echo "Stopping and removing the server..."
	@docker compose down --remove-orphans --volumes

ruff:
  # Run ruff checks
	ruff check --fix
	ruff format

test:
  # Run tests
	pytest .
