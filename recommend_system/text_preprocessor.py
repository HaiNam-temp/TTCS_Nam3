import re


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", flags=re.IGNORECASE)


def normalize_text(value: str) -> str:
    """Normalize text before tokenization."""
    return (value or "").strip().lower()


def tokenize(value: str) -> list[str]:
    """Tokenize text into alphanumeric tokens."""
    normalized = normalize_text(value)
    return TOKEN_PATTERN.findall(normalized)
