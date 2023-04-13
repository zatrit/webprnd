from typing import Any, Callable
from auth.token import generate_token
from data.db_session import create_session
from data.users import User
from form.login import LoginForm
from form.register import RegisterForm
from flask import request, redirect, render_template
import auth
from . import blueprint


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    def post(default_params):
        with create_session() as db_sess:
            login = request.form["login"]
            password = request.form["password"]
            user = db_sess.query(User).where(User.login == login).first()

            if not user or not user.check_password(password):
                return render_template(**default_params,
                                       message="Неправильный логин или пароль")

            token = generate_token(user, password, 0, "user")
            print(token)
        auth.store_token(token)

    return auth_page({
        "template_name_or_list": "login.html",
        "form": LoginForm(),
        "container": "container",
        "title": "Авторизация"
    }, post, "/editor")


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    def post(default_params):
        with create_session() as db_sess:
            login = request.form["login"]
            password = request.form["password"]
            user = db_sess.query(User).where(User.login == login).first()

            if user:
                return render_template(**default_params,
                                       message="Пользователь с таким логином уже существует")

            user = User.new(login, password)
            db_sess.add(user)
            db_sess.commit()

    return auth_page({
        "template_name_or_list": "register.html",
        "form": RegisterForm(),
        "container": "container",
        "title": "Регистрация"
    }, post, "/login")


def auth_page(default_params: dict, on_post: Callable[[dict], Any], _next: str):
    if request.method == "POST":
        return on_post(default_params) or redirect(_next)
    elif request.method == "GET":
        return render_template(**default_params)
    return "Invalid method", 405
