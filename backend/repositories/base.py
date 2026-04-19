import json
from contextlib import contextmanager
from typing import Any, Dict, Optional

from backend.db import get_db


@contextmanager
def db_cursor():
    conn = get_db()
    try:
        yield conn, conn.cursor()
        conn.commit()
    finally:
        conn.close()


def to_json(value: Optional[Dict[str, Any]]) -> Optional[str]:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False)


def from_json(value: Optional[str]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    try:
        return json.loads(value)
    except Exception:
        return None
