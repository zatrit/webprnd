from functools import wraps
from flask import session, request
from .token import validate_token


__error_handlers = {}


def requires_auth(role: str):
    def _requires_auth(fn):
        @wraps(fn)
        def check_auth():
            token = get_token()
            if validate_token(token, role):
                return fn()
            else:
                return __error_handlers[role]()
        return check_auth
    return _requires_auth


def error_handler(role: str):
    def _error_handler(fn):
        __error_handlers[role] = fn
        return fn
    return _error_handler


def store_token(token: str | None):
    session["TOKEN"] = token


def get_token():
    json = (request.json if request.method == "POST" else {}) or {}
    return session.get("TOKEN") or json.get("token")
