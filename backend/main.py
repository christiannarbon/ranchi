from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine
from core.config import settings
import models
from routers import users, groups, restaurants, voting, cron, slack

# Automatically create all database tables using SQLAlchemy
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ranchi App API",
    description="Backend API for user groups and nominations",
    version="1.0.0",
)

# Allow the frontend (and Vercel preview deploys) to call the API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
