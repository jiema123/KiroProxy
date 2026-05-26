"""Simple session auth for KiroProxy Web UI."""

import hmac
import secrets
from typing import Optional

from ..env_config import ADMIN_PASSWORD, ADMIN_USERNAME


SESSION_COOKIE_NAME = "kiroproxy_session"

_active_sessions: set[str] = set()


def get_admin_username() -> str:
    return ADMIN_USERNAME


def get_admin_password() -> str:
    return ADMIN_PASSWORD


def verify_credentials(username: str, password: str) -> bool:
    expected_user = get_admin_username().encode("utf-8")
    expected_password = get_admin_password().encode("utf-8")
    return hmac.compare_digest(username.encode("utf-8"), expected_user) and hmac.compare_digest(
        password.encode("utf-8"), expected_password
    )


def create_session() -> str:
    token = secrets.token_hex(32)
    _active_sessions.add(token)
    return token


def is_authenticated(session_token: Optional[str]) -> bool:
    return bool(session_token and session_token in _active_sessions)


def clear_session(session_token: Optional[str]) -> None:
    if session_token:
        _active_sessions.discard(session_token)
