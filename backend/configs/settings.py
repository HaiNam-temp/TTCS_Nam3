"""Configuration layer for backend."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Detect running inside Docker: either explicit env or /.dockerenv file
IN_DOCKER = os.getenv("IN_DOCKER") == "1" or Path("/.dockerenv").exists()

# Docker/RDS defaults
DOCKER_DEFAULTS = {
	"POSTGRES_HOST": "postgres-pricecomp.c1euissievcs.ap-southeast-2.rds.amazonaws.com",
	"POSTGRES_PORT": 5432,
	"POSTGRES_USER": "postgres",
	"POSTGRES_PASSWORD": "postgres123",
	"POSTGRES_DB": "postgres",
	"POSTGRES_SSLMODE": "verify-full",
	"POSTGRES_SSLROOTCERT": "./global-bundle.pem",
}

LOCAL_DEFAULTS = {
	"POSTGRES_HOST": "localhost",
	"POSTGRES_PORT": 5432,
	"POSTGRES_USER": "postgres",
	"POSTGRES_PASSWORD": "postgres",
	"POSTGRES_DB": "crawldata",
}

# Default behavior: connect to RDS (DOCKER_DEFAULTS) even when running locally.
# To force local DB use, set USE_LOCAL_DB=1 in environment.
USE_LOCAL_DB = os.getenv("USE_LOCAL_DB") == "1"

defaults = LOCAL_DEFAULTS if USE_LOCAL_DB else DOCKER_DEFAULTS

POSTGRES_HOST = os.getenv("POSTGRES_HOST", defaults["POSTGRES_HOST"])
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", str(defaults["POSTGRES_PORT"])))
POSTGRES_USER = os.getenv("POSTGRES_USER", defaults["POSTGRES_USER"])
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", defaults["POSTGRES_PASSWORD"])
POSTGRES_DB = os.getenv("POSTGRES_DB", defaults["POSTGRES_DB"])

# Optional SSL settings for RDS
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", defaults.get("POSTGRES_SSLMODE"))
POSTGRES_SSLROOTCERT = os.getenv("POSTGRES_SSLROOTCERT", defaults.get("POSTGRES_SSLROOTCERT"))

def _build_db_url(user, password, host, port, db, sslmode=None, sslrootcert=None):
	base = f"postgresql://{user}:{password}@{host}:{port}/{db}"
	params = []
	if sslmode:
		params.append(f"sslmode={sslmode}")
	if sslrootcert:
		params.append(f"sslrootcert={sslrootcert}")
	if params:
		return base + "?" + "&".join(params)
	return base

DATABASE_URL = os.getenv(
	"DATABASE_URL",
	_build_db_url(
		POSTGRES_USER,
		POSTGRES_PASSWORD,
		POSTGRES_HOST,
		POSTGRES_PORT,
		POSTGRES_DB,
		POSTGRES_SSLMODE,
		POSTGRES_SSLROOTCERT,
	),
)

ADMIN_DATABASE_URL = os.getenv(
	"ADMIN_DATABASE_URL",
	_build_db_url(
		POSTGRES_USER,
		POSTGRES_PASSWORD,
		POSTGRES_HOST,
		POSTGRES_PORT,
		"postgres",
		POSTGRES_SSLMODE,
		POSTGRES_SSLROOTCERT,
	),
)

# Keep legacy value for old imports that may still exist.
DB_PATH = os.getenv("DB_PATH", "")
active_tokens = {}
