from typing import Any, Callable
from auth.crypto import decode_token
from auth.token import generate_token
from data.db_session import create_session
from data.users import User
from form.login import LoginForm
from form.obtain_token import ObtainTokenForm
from form.register import RegisterForm
from flask import request, redirect, render_template
import auth
from . import blueprint


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    def post(default_params):
        auth_error = {"message": "Неверный логин или пароль"}
        login = request.form["login"]
        password = request.form["password"]

        with create_session() as db_sess:
            user = db_sess.query(User).where(User.login == login).first()

            if not user or not user.check_password(password):
                return render_template(**default_params, **auth_error)

            if not (token := generate_token(user, password, 0, "user")):
                return render_template(**default_params, **auth_error)
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
        login = request.form["login"]
        password = request.form["password"]

        with create_session() as db_sess:
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


@blueprint.route("/obtain", methods=["GET", "POST"])
def obtain_token():
    def post(default_params):
        login = decode_token(auth.get_token())[4]
        password = request.form["password"]
        auth_error = {"message": "Неверный пароль"}

        with create_session() as db_sess:
            user = db_sess.query(User).where(User.login == login).first()

            if not user or not user.check_password(password):
                return render_template(**default_params, **auth_error)

            token = generate_token(user, password, 0, "api")

        return render_template(**default_params, token=token)

    return auth_page({
        "template_name_or_list": "obtain_token.html",
        "form": ObtainTokenForm(),
        "container": "container",
        "title": "Получение токена"
    }, post, "/")


def auth_page(default_params: dict, on_post: Callable[[dict], Any], _next: str):
    if request.method == "POST" and default_params["form"].validate_on_submit():
        return on_post(default_params) or redirect(_next)
    else:
        return render_template(**default_params)
