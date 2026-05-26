"""API key auth for proxy endpoints."""

import secrets
from typing import Optional

from .env_config import PROXY_API_KEY


def get_api_key() -> str:
    return PROXY_API_KEY


def extract_bearer_token(header_value: Optional[str]) -> Optional[str]:
    if not header_value:
        return None
    parts = header_value.strip().split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None


def verify_api_key(header_value: Optional[str]) -> bool:
    token = extract_bearer_token(header_value)
    if not token:
        return False
    return secrets.compare_digest(token, get_api_key())
