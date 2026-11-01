"""
Central configuration.

All settings come from environment variables (loaded from the .env file in the
project root). Nothing secret is written in the code.
"""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

# backend/app/config.py -> parents[2] is the project root folder
ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"

load_dotenv(ROOT_DIR / ".env")


class Settings:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "3306")
        self.db_user = os.getenv("DB_USER", "")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "ambulance_routing_db")

        # Comma separated list of frontend URLs that may call the API
        origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
        self.cors_origins = [o.strip() for o in origins.split(",") if o.strip()]

        # Optional full URL override (used by the automated tests)
        self._database_url_override = os.getenv("DATABASE_URL")

    def _credentials(self) -> str:
        if not self.db_user:
            raise RuntimeError(
                "DB_USER is not set. Copy .env.example to .env in the project "
                "root folder and fill in your MySQL username and password."
            )
        # quote_plus makes passwords containing @ : / # safe inside a URL
        return f"{quote_plus(self.db_user)}:{quote_plus(self.db_password)}"

    @property
    def server_url(self) -> str:
        """URL of the MySQL server without a database (used to create the database)."""
        return f"mysql+pymysql://{self._credentials()}@{self.db_host}:{self.db_port}/"

    @property
    def database_url(self) -> str:
        if self._database_url_override:
            return self._database_url_override
        return (
            f"mysql+pymysql://{self._credentials()}@{self.db_host}:{self.db_port}"
            f"/{self.db_name}?charset=utf8mb4"
        )


settings = Settings()
