# Create virtual environment
venv:
    @echo "Creating virtual environment..."
    @uv venv

# Install development dependencies
dev-deps:
    @echo "Compiling and Installing dev-requirements.txt..."
    @uv pip compile -o requirements.txt requirements.in
    @uv pip compile -o dev-requirements.txt dev-requirements.in requirements.in
    @uv pip install -r dev-requirements.txt

# Install production dependencies
deps:
    @echo "Compiling and Installing requirements.txt..."
    @uv pip compile -o requirements.txt requirements.in
    @uv pip install -r requirements.txt

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
