from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    cron_secret: str = "super_secret_cron_key"
    slack_bot_token: str
    slack_signing_secret: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Using standard synchronous SQLAlchemy with PostgreSQL
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
