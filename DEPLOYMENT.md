# Deploying Ranchi to Vercel + Supabase

This guide walks you through getting a live, testable instance of **Ranchi** running using:

- **Supabase** — managed PostgreSQL database
- **Vercel (project #1)** — the FastAPI backend, deployed as Python serverless functions
- **Vercel (project #2)** — the Vue 3 / Vite frontend, deployed as a static site

> This is a **test/preview** deployment guide, optimized for getting something working quickly — not a hardened production setup. Notes on production hardening are called out where relevant.

```
                  ┌─────────────────────┐
   Browser  ───►  │ Frontend (Vercel)   │   Vue + Vite static SPA
                  │  VITE_API_URL ──────────────┐
                  └─────────────────────┘       │
                                                 ▼
                  ┌─────────────────────┐
                  │ Backend (Vercel)    │   FastAPI serverless
                  │  DATABASE_URL ──────────────┐
                  └─────────────────────┘       │
                                                 ▼
                  ┌─────────────────────┐
                  │ Supabase Postgres   │
                  └─────────────────────┘
```

---

## Prerequisites

- A [Supabase](https://supabase.com) account
- A [Vercel](https://vercel.com) account
- This repo pushed to GitHub (Vercel deploys from a Git repo)
- Optional, for testing the real integrations:
  - A **Google Places API key** (restaurant nominations)
  - A **Slack bot token + signing secret** (morning prompts / winner announcements)

> The backend's settings (`backend/core/config.py`) require `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, and `GOOGLE_PLACES_API_KEY` to be **present**, or the app won't boot. If you only want to click around the UI and don't need Slack/Google, you can set them to dummy placeholder strings — just know those specific features will fail when exercised.

---

## Part 1 — Database on Supabase

1. Go to <https://supabase.com/dashboard> → **New project**.
2. Pick an org, name it (e.g. `ranchi`), and **set a strong database password** — copy it somewhere, you'll need it in a moment.
3. Choose a region close to where you'll host the Vercel functions, then **Create new project** and wait for it to provision (~2 min).
4. Get your connection string: **Project Settings → Database → Connection string**.

   You'll see a few options. For Vercel serverless functions, use the **Connection Pooler** string (Supavisor), **Transaction mode**, which looks like:

   ```
   postgresql://postgres.<project-ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:6543/postgres
   ```

   - Replace `[YOUR-PASSWORD]` with the password from step 2.
   - Port **6543** = transaction pooler (recommended for serverless — many short-lived connections).
   - Append `?sslmode=require` to the end.

   Final form:

   ```
   postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres?sslmode=require
   ```

   Keep this handy — it becomes `DATABASE_URL` for the backend.

> **Why the pooler?** Each serverless invocation can open a new DB connection. Direct connections (port 5432) exhaust Postgres quickly under serverless. The transaction pooler is designed for this. The app uses synchronous `psycopg2` with `pool_pre_ping=True` (`backend/core/database.py`), which works fine with the pooler.

> **Schema creation:** You do **not** need to run Alembic for a first deploy. On startup, `backend/main.py` calls `models.Base.metadata.create_all(bind=engine)`, which creates all tables automatically the first time the backend boots. (For real migrations later, use the Alembic setup in `backend/alembic/`.)

---

## Part 2 — Backend (FastAPI) on Vercel

Vercel can run FastAPI via its Python serverless runtime. The backend lives in `backend/`, so you'll deploy that subdirectory as its own Vercel project. The two files Vercel needs are **already committed to the repo** — they're documented here so you know what they do.

### 2.1 The Vercel entrypoint — `backend/api/index.py` (already in repo)

```python
# Vercel Python serverless entrypoint.
# Vercel detects the ASGI `app` and serves it.
from main import app  # noqa: F401
```

### 2.2 The routing config — `backend/vercel.json` (already in repo)

This routes every incoming request to the FastAPI app:

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index" }
  ]
}
```

### 2.3 Confirm dependencies are installable

Vercel's Python builder installs from `backend/requirements.txt`, which already exists in this repo. No action needed unless you change dependencies. (`psycopg2-binary` is already included, which is what you want on serverless — no system build tools required.)

### 2.4 Create the Vercel project

1. Vercel dashboard → **Add New → Project** → import this GitHub repo.
2. **Root Directory:** click **Edit** and set it to `backend`. *(Critical — this makes `main.py`, `core/`, `routers/` importable.)*
3. **Framework Preset:** Other.
4. Expand **Environment Variables** and add:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | the Supabase pooler URL from Part 1 |
   | `CRON_SECRET` | any long random string (e.g. `openssl rand -hex 32`) |
   | `SLACK_BOT_TOKEN` | your `xoxb-...` token (or a placeholder) |
   | `SLACK_SIGNING_SECRET` | your Slack signing secret (or a placeholder) |
   | `GOOGLE_PLACES_API_KEY` | your Google Places key (or a placeholder) |
   | `CORS_ORIGINS` | your frontend URL(s), comma-separated (you can fill this in after Part 3 and redeploy) |

5. **Deploy.**

   > You won't know the frontend URL yet — that's fine. Set `CORS_ORIGINS` now if you do, or come back to it in Part 4. Vercel preview URLs (`*.vercel.app`) are allowed by default regardless.

### 2.5 Verify the backend

Once deployed you'll get a URL like `https://ranchi-backend.vercel.app`. Test it:

```bash
curl https://ranchi-backend.vercel.app/
# {"message":"Welcome to the Ranchi App API! Visit /docs for Swagger UI."}
```

Open `https://ranchi-backend.vercel.app/docs` for the Swagger UI. **Copy the backend base URL** — the frontend needs it next.

> **Troubleshooting:** If you get a 500 on first load, check **Vercel → your project → Logs**. The two most common causes are (a) a bad `DATABASE_URL` (wrong password / missing `?sslmode=require`), or (b) a missing required env var, which raises a Pydantic validation error at import time.

---

## Part 3 — Frontend (Vue + Vite) on Vercel

The frontend reads the backend URL from `VITE_API_URL` (`frontend/src/api/client.js`), falling back to `http://localhost:8000` locally.

1. Vercel dashboard → **Add New → Project** → import the **same** GitHub repo again (this creates a second, separate project).
2. **Root Directory:** set it to `frontend`.
3. **Framework Preset:** Vercel should auto-detect **Vite**. If not, set:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
4. Add an environment variable:

   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | your backend URL from Part 2 (e.g. `https://ranchi-backend.vercel.app`) — **no trailing slash** |

   > Vite inlines `VITE_*` variables **at build time**. If you change this value later, you must **redeploy** the frontend for it to take effect.

5. **Deploy.**

You'll get a URL like `https://ranchi.vercel.app`. Open it and the app should load and talk to the backend.

---

## Part 4 — CORS (do this after both URLs exist)

CORS middleware is **already wired up** in `backend/main.py` and driven by env vars (`backend/core/config.py`), so you don't need to change code — just set the env var on the backend Vercel project:

| Key | Value |
|-----|-------|
| `CORS_ORIGINS` | comma-separated frontend origins, e.g. `http://localhost:5173,https://ranchi.vercel.app` (**no trailing slash**) |

After adding/changing it, **redeploy the backend** (Vercel → backend project → Deployments → Redeploy) so the new value is picked up.

> **Vercel preview deploys** (each branch gets a unique `*.vercel.app` URL) are already allowed by default via the `CORS_ORIGIN_REGEX` setting, which defaults to `https://.*\.vercel\.app`. You can override or tighten it with the `CORS_ORIGIN_REGEX` env var. For a production deployment, set `CORS_ORIGINS` to your real domain(s) and consider removing the broad regex.

---

## Part 5 — (Optional) Scheduled cron jobs

Ranchi has two cron endpoints (`backend/routers/cron.py`):

- `GET /cron/morning-prompt`
- `GET /cron/finalize-votes`

The app uses Vercel Cron to schedule these jobs. The schedules are configured in `backend/vercel.json` under `"crons"`:

```json
[
  { "path": "/cron/morning-prompt", "schedule": "0 0 * * 1-5" },
  { "path": "/cron/finalize-votes",  "schedule": "0 4 * * 1-5" }
]
```

Vercel automatically sends the `Authorization: Bearer <CRON_SECRET>` header to cron requests when the `CRON_SECRET` environment variable is configured in your backend Vercel project settings, so no extra scheduling configuration is required.

> **Note:** The Vercel Hobby plan limits cron frequency to daily granularity; the weekday schedules (`1-5` for Monday–Friday) defined above are fully acceptable under these limits.

You can trigger them manually to test:

```bash
curl https://ranchi-backend.vercel.app/cron/morning-prompt \
  -H "Authorization: Bearer <your CRON_SECRET value>"
```

---

## Quick checklist

- [ ] Supabase project created; pooler `DATABASE_URL` copied (`:6543`, `?sslmode=require`)
- [ ] Repo pushed to GitHub (includes `backend/api/index.py` and `backend/vercel.json`)
- [ ] Backend Vercel project: Root Directory = `backend`, all 5 env vars set
- [ ] `GET /` and `/docs` respond on the backend URL
- [ ] Frontend Vercel project: Root Directory = `frontend`, `VITE_API_URL` set to backend URL
- [ ] `CORS_ORIGINS` set on the backend to the frontend origin, backend redeployed
- [ ] App loads at the frontend URL and can talk to the API

---

## Common gotchas

| Symptom | Likely cause |
|---|---|
| Backend 500 on first request | Bad `DATABASE_URL` (password/sslmode) or a missing required env var |
| Frontend loads but every API call fails (CORS error in console) | CORS middleware not added (Part 4) or wrong frontend origin listed |
| Frontend calls `localhost:8000` in production | `VITE_API_URL` not set, or set after build without a redeploy |
| DB connection errors under load | Using the direct connection (`:5432`) instead of the pooler (`:6543`) |
| `relation "..." does not exist` | Backend never successfully booted, so `create_all` never ran — fix the boot error first |
