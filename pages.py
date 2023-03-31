from pathlib import Path
from flask import Blueprint, render_template, url_for

blueprint = Blueprint(
    "pages",
    __name__,
    template_folder="templates",
    static_folder="static",
)

static_folder: str = blueprint.static_url_path.lstrip("/")  # type: ignore


@blueprint.route("/")
@blueprint.route("/editor")
def editor():
    params = {
        "title": "Редактор",
        "theme": get_theme()
    }
    return render_template("editor.html", **params)


@blueprint.app_errorhandler(404)
def page_not_found(_):
    return render_template('not_found.html', theme=get_theme()), 404


# Функция для упрощения доступа к статическому контенту страницы
@blueprint.app_template_global()
def static(file: str):
    return url_for("static", filename=file)


def content_check() -> bool:
    exists = Path("static/").exists()
    if not exists:
        print("Вероятно, необходимый для работы сайта веб-контент не скомпилирован.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-content-check.",
              "(но вероятно, ничего не будет работать)",
              "Вы можете скомпилировать веб-контент c помощью build.py, или же скачать:",
              "PLACEHOLDER", sep="\n")
    return exists


def get_theme() -> str:
    return "darkly"
