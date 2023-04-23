from pathlib import Path
from flask import Blueprint, render_template, url_for, redirect
import auth as _auth
from os import getcwd


def init_pages():
    from . import auth, other


blueprint = Blueprint(
    "pages",
    __name__,
    template_folder="web/templates/",
    static_folder="static/",
    root_path=getcwd()
)
requires_auth = _auth.requires_auth(["user"])

init_pages()


@_auth.error_handler("user")
@_auth.default_error_handler
def auth_error_handler():
    return redirect("/login")


@blueprint.app_errorhandler(404)
def page_not_found(_):
    return render_template("not_found.html", title="404"), 404


# Функция для упрощения доступа к статическому контенту страницы
@blueprint.app_template_global()
def static(file: str):
    return url_for("static", filename=file)


@blueprint.app_template_global()
def theme() -> str:
    return "darkly"


@blueprint.app_template_global()
def lang() -> str:
    return "ru"


def content_check() -> bool:
    exists = Path("static/").exists()
    if not exists:
        print("Вероятно, необходимый для работы сайта веб-контент не скомпилирован.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-content-check.",
              "(но вероятно, ничего не будет работать)",
              "Вы можете скомпилировать веб-контент c помощью build.py, или же скачать:",
              "https://disk.yandex.ru/d/ocXUoe4aSiOMTA", sep="\n")
    return exists
