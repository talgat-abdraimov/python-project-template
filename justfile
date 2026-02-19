# Sync all dependencies (creates .venv automatically)
sync:
    @echo "Syncing dependencies..."
    @uv sync

# Sync production dependencies only
sync-prod:
    @echo "Syncing production dependencies..."
    @uv sync --no-dev

# Add a production dependency
add *packages:
    @uv add {{packages}}

# Add a development dependency
add-dev *packages:
    @uv add --group dev {{packages}}

# Remove a dependency
remove *packages:
    @uv remove {{packages}}

# Build the server
build:
    @echo "Building the server..."
    @docker compose build --no-cache -q

# Start the server
up *args="":
    @echo "Starting the server..."
    @docker compose up {{args}}

# Stop the server
stop:
    @echo "Stopping the server..."
    @docker compose stop

# Stop and remove the server
down:
    @echo "Stopping and removing the server..."
    @docker compose down --remove-orphans --volumes

# Show logs
logs *args="":
    @echo "Showing logs..."
    @docker compose logs {{args}}

# Run ruff checks
lint:
    @echo "Running ruff checks..."
    ruff check --fix
    ruff format

# Run tests
test:
    @echo "Running tests..."
    pytest .

# Run all quality checks
check:
    @echo "Running all quality checks..."
    @just lint
    @just test

clean:
    @echo "Cleaning up..."
    @rm -rf .pytest_cache
    @rm -rf .ruff_cache
    @rm -rf .mypy_cache
    @rm -rf .coverage
    @rm -rf htmlcov/
    @find . -type d -name __pycache__ -exec rm -rf {} +
    @find . -name "*.pyc" -delete
