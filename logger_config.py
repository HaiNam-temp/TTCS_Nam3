"""Compatibility wrapper for logger config moved under backend package."""

from backend.logger_config import get_logger

__all__ = ["get_logger"]
