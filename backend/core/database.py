from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Using standard synchronous SQLAlchemy with PostgreSQL
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
