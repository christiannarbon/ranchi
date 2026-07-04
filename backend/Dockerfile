# LOCAL DEVELOPMENT ONLY. Production runs on Vercel + Supabase (see DEPLOYMENT.md).
# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables for optimized Python and uv execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install uv securely via pip (pinned version for strict reproducibility)
RUN pip install --no-cache-dir uv==0.11.16

# Copy only the dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Create a virtual environment and install dependencies cleanly
# --frozen ensures we strictly use the lockfile
# --no-install-project skips trying to install the directory as a pip package
# --no-dev skips installing development tools like ruff
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the backend application code
COPY . .

# Expose the port Uvicorn runs on
EXPOSE 8000

# Start the FastAPI application using uvicorn (executed inside the uv venv)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
