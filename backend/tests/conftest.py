"""
Tests run on a temporary SQLite file, so they never touch your MySQL data.
(Real MySQL behaviour is checked by running the app - see TEAM_SETUP.md.)
"""
import os
import tempfile

_db_file = os.path.join(tempfile.gettempdir(), "ambulance_routing_test.db")
if os.path.exists(_db_file):
    os.remove(_db_file)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_file}"
os.environ.setdefault("DB_USER", "test")

import pytest
from fastapi.testclient import TestClient

from app.database import models  # noqa: F401
from app.database.connection import Base, SessionLocal, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield TestClient(app)


@pytest.fixture()
def db():
    with SessionLocal() as session:
        yield session
