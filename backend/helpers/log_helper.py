"""Log helper layer."""

from typing import Optional

from logger_config import get_logger


def get_module_logger(name: Optional[str] = None):
    return get_logger(name)
