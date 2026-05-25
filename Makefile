.PHONY: setup lint format check

setup:
	@echo "Setting up backend environment with uv..."
	cd backend && uv sync
	@echo "Backend environment setup complete."

lint:
	@echo "Running ruff linter..."
	cd backend && uv run ruff check .

format:
	@echo "Running ruff formatter..."
	cd backend && uv run ruff format .

check: lint test
	@echo "Running ruff format check..."
	cd backend && uv run ruff format --check .

test:
	@echo "Running unit tests with pytest..."
	cd backend && uv run pytest test/unit
