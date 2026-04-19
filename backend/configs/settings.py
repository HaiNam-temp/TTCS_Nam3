"""Configuration layer for backend."""

import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "crawldata")

DATABASE_URL = os.getenv(
	"DATABASE_URL",
	f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
)
ADMIN_DATABASE_URL = os.getenv(
	"ADMIN_DATABASE_URL",
	f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres",
)

# Keep legacy value for old imports that may still exist.
DB_PATH = os.getenv("DB_PATH", "")
active_tokens = {}
