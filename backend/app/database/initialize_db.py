"""
One command to prepare the database:

    python -m app.database.initialize_db            (run inside the backend folder)

Steps
  1. CREATE DATABASE IF NOT EXISTS ambulance_routing_db   (safe to repeat)
  2. Run Alembic migrations -> creates / updates tables   (keeps existing data)
  3. Insert sample demo data only into EMPTY tables

Use --no-seed to skip step 3.
"""
import argparse
import re
import sys

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from app.config import BACKEND_DIR, settings


def create_database_if_missing():
    if not re.fullmatch(r"[A-Za-z0-9_]+", settings.db_name):
        raise SystemExit("DB_NAME may only contain letters, numbers and underscore.")
    engine = create_engine(settings.server_url)
    with engine.connect() as conn:
        conn.execute(text(
            f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        ))
        conn.commit()
    engine.dispose()
    print(f"[1/3] Database '{settings.db_name}' is ready")


def run_migrations():
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    command.upgrade(cfg, "head")
    print("[2/3] Migrations applied (tables are up to date)")


def seed():
    from app.database.connection import SessionLocal
    from app.database.seed import seed_sample_data

    with SessionLocal() as db:
        for line in seed_sample_data(db):
            print("      -", line)
    print("[3/3] Sample data step finished")


def main():
    parser = argparse.ArgumentParser(description="Create and prepare the project database")
    parser.add_argument("--no-seed", action="store_true", help="do not insert sample demo data")
    args = parser.parse_args()

    try:
        create_database_if_missing()
        run_migrations()
        if not args.no_seed:
            seed()
    except Exception as exc:  # show a readable message instead of a long traceback
        print(f"\nDatabase setup failed: {exc}")
        print("Check that MySQL is running and DB_USER / DB_PASSWORD / DB_HOST in .env are correct.")
        sys.exit(1)
    print("\nDone. You can now start the API with: uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
