from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import engine  # noqa: F401
from core.database import get_db
from core.config import settings
import models  # noqa: F401
from routers import users, groups, restaurants, voting, cron, slack

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.0)

app = FastAPI(
    title="Ranchi App API",
    description="Backend API for user groups and nominations",
    version="1.0.0",
)

# Allow the frontend (and Vercel preview deploys) to call the API from the browser.
cors_kwargs = {
    "allow_origins": settings.cors_origins_list,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
if settings.cors_origin_regex:
    cors_kwargs["allow_origin_regex"] = settings.cors_origin_regex
app.add_middleware(CORSMiddleware, **cors_kwargs)

# Include the routers
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(restaurants.router)
app.include_router(voting.router)
app.include_router(cron.router)
app.include_router(slack.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Ranchi App API! Visit /docs for Swagger UI."}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok"}
