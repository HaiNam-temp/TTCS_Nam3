"""Database schema initialization layer."""

import uuid
from datetime import datetime
import psycopg2
from psycopg2 import sql

from backend.configs import ADMIN_DATABASE_URL, DATABASE_URL, POSTGRES_DB
from backend.helpers import hash_password
from logger_config import get_logger

logger = get_logger(__name__)


def init_database() -> None:
    _ensure_database_exists()

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS platforms (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL,
            url TEXT UNIQUE,
            image TEXT,
            rating REAL,
            review_count INTEGER,
            metadata JSONB,
            created_at TEXT NOT NULL
        )
        """
    )

    _ensure_products_columns(cursor)

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    existing_admin = cursor.fetchone()
    admin_password_hash = hash_password("admin")

    if existing_admin:
        cursor.execute(
            """
            UPDATE users
            SET is_admin = TRUE,
                password_hash = %s,
                email = 'admin@example.com'
            WHERE username = 'admin'
            """,
            (admin_password_hash,),
        )
        logger.info("Admin account updated (username: admin, password: admin)")
    else:
        admin_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        cursor.execute(
            """
            INSERT INTO users (id, username, email, password_hash, full_name, is_admin, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (admin_id, "admin", "admin@example.com", admin_password_hash, "Administrator", True, created_at),
        )
        logger.info("Default admin account created (username: admin, password: admin)")

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def _ensure_database_exists() -> None:
    admin_conn = psycopg2.connect(ADMIN_DATABASE_URL)
    admin_conn.autocommit = True
    cursor = admin_conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_DB,))
    exists = cursor.fetchone()
    if not exists:
        logger.info("Creating PostgreSQL database: %s", POSTGRES_DB)
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(POSTGRES_DB)))
    cursor.close()
    admin_conn.close()


def _ensure_products_columns(cursor) -> None:
    expected = {
        "image": "TEXT",
        "rating": "REAL",
        "review_count": "INTEGER",
        "metadata": "JSONB",
        "created_at": "TEXT",
    }
    for col, col_type in expected.items():
        cursor.execute(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'products' AND column_name = %s
            """,
            (col,),
        )
        if cursor.fetchone() is None:
            logger.info("Altering products table to add missing column: %s %s", col, col_type)
            cursor.execute(sql.SQL("ALTER TABLE products ADD COLUMN {} {};").format(sql.Identifier(col), sql.SQL(col_type)))
