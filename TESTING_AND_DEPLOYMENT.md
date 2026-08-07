# Ranchi Testing & Deployment Guide

This document provides a step-by-step walkthrough of how to test and verify Ranchi locally, as well as how to deploy the application components to production.

---

## Section 1: Testing & Local Verification

Ranchi consists of a **FastAPI backend** and a **Vue 3 frontend**. We use a centralized `Makefile` in the project root to coordinate validation and test suites.

### 1.1 Backend Verification

The Python backend uses [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management, [pytest](https://docs.pytest.org/) for unit tests, and [Ruff](https://docs.astral.sh/ruff/) for linting/formatting.

#### 1. Setup Backend Environment
```bash
make setup
```
This synchronizes your local virtual environment (`backend/.venv`) and installs all lockfile dependencies.

#### 2. Run Python Unit Tests
```bash
make test
```
*This executes `pytest` targeting the unit tests under `backend/test/unit` against an in-memory SQLite database.*

#### 3. Lint and Format Checks
Verify code compliance with lint rules and check formatting styling:
```bash
# Check code style with Ruff linter
make lint

# Automatically format codebase using Ruff formatter
make format

# Run formatting validations (CI dry-run)
make check
```

---

### 1.2 Frontend Verification

The frontend uses Node.js, [Vitest](https://vitest.dev/) for unit testing, and [ESLint](https://eslint.org/) / [Prettier](https://prettier.io/) for code quality.

#### 1. Setup Frontend Environment
```bash
make setup-frontend
```
This installs the required Node modules in the `frontend/` directory.

#### 2. Run Frontend Unit Tests
```bash
cd frontend && npm run test:unit
```
This runs the frontend unit tests using Vitest.

#### 3. Lint and Format Checks
```bash
# Lint the Vue templates and Javascript logic
make lint-frontend

# Check formatting via Prettier
make check-frontend

# Automatically fix format discrepancies
make format-frontend
```

---

### 1.3 Full Verification Suite
Verify both backend and frontend stacks in a single command before pushing:
```bash
make check-all
```

---

## Section 2: Canonical Production Deployment

Ranchi is architected to run on serverless cloud platforms for production:
- **Database:** Supabase (Managed PostgreSQL + Transaction Connection Pooler)
- **Backend API:** Vercel (FastAPI serverless Python runtime)
- **Frontend client:** Vercel (Static Vue 3 client)

---

### 2.1 Database Provisioning (Supabase)

1. Sign in to the [Supabase Dashboard](https://supabase.com) and create a **New Project**.
2. Go to **Project Settings → Database** and find the **Connection String** section.
3. Select the **Connection Pooler** URI, choose **Transaction Mode**, and set the port to **6543** (recommended for serverless environments to prevent connection exhaustion).
4. Append `?sslmode=require` to your connection string. The final string format should look like:
   ```
   postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres?sslmode=require
   ```
5. Run schema migrations against the database from the `backend/` directory:
   ```bash
   DATABASE_URL="<your-supabase-connection-string>" make migrate
   ```

---

### 2.2 Backend Deployment (Vercel)

The backend deployment configuration is defined in [vercel.json](file:///Users/christianedensorarbon/personal_dev/ranchi/backend/vercel.json) and uses the entrypoint [index.py](file:///Users/christianedensorarbon/personal_dev/ranchi/backend/api/index.py).

1. In the Vercel dashboard, click **Add New → Project** and import the Git repository.
2. Under **Root Directory**, click edit and select **backend**.
3. Keep **Framework Preset** as **Other**.
4. Configure the following **Environment Variables**:
   - `DATABASE_URL`: The Supabase Transaction Pooler URL.
   - `CRON_SECRET`: A secure key used to authorize cron trigger requests.
   - `SLACK_BOT_TOKEN`: Your Slack bot token (`xoxb-...`).
   - `SLACK_SIGNING_SECRET`: Your Slack application's signing secret.
   - `GOOGLE_PLACES_API_KEY`: Google Cloud API key for places search.
   - `CORS_ORIGINS`: Comma-separated origins representing allowed frontends (e.g. `https://ranchi.vercel.app`).
5. Click **Deploy**. Verify it is live by navigating to `<backend-url>/health` or `<backend-url>/docs` (Swagger UI).

---

### 2.3 Frontend Deployment (Vercel)

1. Create another **New Project** on Vercel and import the same repository.
2. Select **frontend** as the **Root Directory**.
3. Choose **Vite** as the **Framework Preset**.
4. Set the following **Environment Variable**:
   - `VITE_API_URL`: The URL of your deployed backend (e.g. `https://ranchi-backend.vercel.app`, no trailing slash).
5. Click **Deploy**. Vercel will bundle and serve the Vue application.

---

### 2.4 Configure CORS and Finalize

Once the frontend URL is generated:
1. Update `CORS_ORIGINS` in your Vercel backend project environment variables to include the new frontend URL.
2. Trigger a backend redeploy (**Deployments → Redeploy**) so the CORS middleware registers the new domain.

---

### 2.5 Scheduled Cron Jobs

Schedules are declared under the `"crons"` block in `vercel.json` and are triggered automatically daily:
- **Morning Status Prompt (`GET /cron/morning-prompt`)**: Runs at 09:00 JST (00:00 UTC) Mon–Fri.
- **Vote Finalization (`GET /cron/finalize-votes`)**: Runs at 13:00 JST (04:00 UTC) Mon–Fri.

Requests to these endpoints are authenticated via `Authorization: Bearer <CRON_SECRET>` headers.

---

## Section 3: Local Containerized Deployment (Docker Compose)

To run a production-like replica stack locally in Docker containers:
```bash
docker-compose up --build
```
This deploys:
1. **db**: PostgreSQL database container.
2. **backend**: FastAPI web server accessible at `http://localhost:8000`.
3. **frontend**: Built Vue frontend served through Nginx at `http://localhost:80`.

*Note: The Docker Compose configuration is for local previewing and verification and is not utilized for live production environments.*
