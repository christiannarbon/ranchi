.PHONY: setup lint format check test setup-frontend lint-frontend format-frontend check-frontend check-all

# --- Backend ---
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

# --- Frontend ---
setup-frontend:
	@echo "Setting up frontend environment..."
	cd frontend && npm install
	@echo "Frontend environment setup complete."

lint-frontend:
	@echo "Running ESLint..."
	cd frontend && npm run lint -- --max-warnings=0

format-frontend:
	@echo "Running Prettier..."
	cd frontend && npm run format

check-frontend: lint-frontend
	@echo "Running Prettier format check..."
	cd frontend && npx prettier --check src/

# --- All ---
check-all: check check-frontend
