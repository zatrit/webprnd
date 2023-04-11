from flask import session, redirect, request
from functools import wraps


# https://stackoverflow.com/a/32514167/12245612
def requires_auth(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'token' not in session:
            return redirect("/login")
        return func(*args, **kwargs)

    return check_token


def requires_auth_api(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        json: dict = request.json or {}
        if "token" not in json:
            return {"error": "Отсутсвует токен"}, 403
        return func(*args, **kwargs)

    return check_token
