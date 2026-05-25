from fastapi import FastAPI
from database import engine
import models
from routers import users, groups, restaurants, voting, cron

# Automatically create all database tables using SQLAlchemy
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ranchi App API",
    description="Backend API for user groups and nominations",
    version="1.0.0"
)

# Include the routers
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(restaurants.router)
app.include_router(voting.router)
app.include_router(cron.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ranchi App API! Visit /docs for Swagger UI."}
