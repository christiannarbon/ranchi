# Ranchi

[![Backend Lint](https://github.com/christiannarbon/ranchi/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/christiannarbon/ranchi/actions/workflows/backend-ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393.svg)](https://fastapi.tiangolo.com/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Status: Development](https://img.shields.io/badge/Status-Development-orange.svg)]()

**Ranchi** is a collaborative Lunch Group formation app explicitly designed for those participating in RTO (Return to Office). It allows users to flag if they are looking for lunch, form groups dynamically, vote on a shortlist of restaurants, and seamlessly finalize a winner.

## Features

- **Daily Statuses**: Mark yourself as "Looking" for a lunch group via automated morning cron jobs.
- **Dynamic Groups**: Join groups of up to 6 people.
- **Restaurant Nominations**: Propose up to 3 restaurants to visit using Google Places data.
- **Collaborative Voting**: Vote for your preferred lunch spot. Ties are automatically handled.
- **Webhook Integration**: Includes serverless cron job endpoints for sending automated Slack-style notifications.

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL (via standard synchronous SQLAlchemy 2.0)
- **Validation**: Pydantic V2
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://docs.astral.sh/ruff/)

## Local Development

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed locally

### Setup

Use the provided `Makefile` to instantly configure the backend environment:

```bash
make setup
```

This will initialize the `.venv` and securely lock the dependencies.

### Code Quality

Before pushing code, ensure you run the linters and formatters:

```bash
# Lint the code
make lint

# Auto-format the code
make format

# Run the strict CI check
make check
```

*(Note: The repository includes a pre-push hook that automatically runs `make check` to ensure no malformed code reaches GitHub).*

## 📄 License
Please review the `LICENSE` file in the root directory for more details.
