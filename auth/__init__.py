from functools import wraps
from flask import session, request
from .token import validate_token
from typing import Callable

ErrorHandler = Callable[[], str]

__error_handlers: dict[str | None, ErrorHandler] = {}
__default_error_handler: ErrorHandler


def requires_auth(roles: list[str]):
    def _requires_auth(fn):
        @wraps(fn)
        def check_auth():
            token = get_token()
            if validate_token(token, roles):
                return fn()
            else:
                role = next(filter(__error_handlers.__contains__, roles), None)
                return __error_handlers.get(role, __default_error_handler)()
        return check_auth
    return _requires_auth


def error_handler(role: str):
    def _error_handler(fn):
        __error_handlers[role] = fn
        return fn
    return _error_handler


def default_error_handler(fn):
    global __default_error_handler
    __default_error_handler = fn
    return fn


def store_token(token: str | None):
    session["TOKEN"] = token


def get_token() -> str:
    has_json = request.method == "POST" and request.content_type == "application/json"
    json = (request.json if has_json else {}) or {}
    return session.get("TOKEN") or json.get("token") or ""
