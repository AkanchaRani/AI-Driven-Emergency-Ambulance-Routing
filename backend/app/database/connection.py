"""
Database connection.

- engine      : the actual connection pool to MySQL
- SessionLocal: creates a session (one "conversation" with the database)
- Base        : parent class of every model in models.py
- get_db      : FastAPI dependency that gives each request its own session
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# pool_pre_ping checks a connection is alive before using it,
# pool_recycle avoids MySQL's "server has gone away" after idle time.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
