from pathlib import Path
from flask import Blueprint, render_template, url_for, redirect, session

from auth import requires_auth

blueprint = Blueprint(
    "pages",
    __name__,
    template_folder="web/templates/",
    static_folder="static/",
)

static_folder: str = blueprint.static_url_path.lstrip("/")  # type: ignore


@blueprint.route("/")
@blueprint.route("/index")
def index():
    return render_template("index.html", title="WebPRND")


@blueprint.route("/editor")
@requires_auth
def editor():
    return render_template("editor.html", title="Редактор")


@blueprint.route("/login")
def login():
    # Пока-что тест, нужно для работы editor'а
    session["token"] = "TEST TOKEN"
    return redirect("/editor")


@blueprint.app_errorhandler(404)
def page_not_found(_):
    return render_template('not_found.html', title="404"), 404


# Функция для упрощения доступа к статическому контенту страницы
@blueprint.app_template_global()
def static(file: str):
    return url_for("static", filename=file)


@blueprint.app_template_global()
def theme() -> str:
    return "darkly"


def content_check() -> bool:
    exists = Path("static/").exists()
    if not exists:
        print("Вероятно, необходимый для работы сайта веб-контент не скомпилирован.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-content-check.",
              "(но вероятно, ничего не будет работать)",
              "Вы можете скомпилировать веб-контент c помощью build.py, или же скачать:",
              "PLACEHOLDER", sep="\n")
    return exists
