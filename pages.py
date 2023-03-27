from pathlib import Path
from flask import Blueprint, render_template, url_for

blueprint = Blueprint(
    "pages",
    __name__,
    template_folder="templates",
    static_folder="static",
)

static_folder: str = blueprint.static_url_path.lstrip("/")  # type: ignore


@blueprint.route("/editor")
def editor():
    params = {
        "title": "Редактор",
        "static": flask_static
    }
    return render_template("editor.html", **params)


def content_check() -> bool:
    exists = Path("static/").exists()
    if not exists:
        print("Вероятно, необходимый для работы сайта веб-контент не скомпилирован.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-content-check.",
              "Вы можете скомпилировать веб-контент c помощью build.py, или же скачать:",
              "PLACEHOLDER", sep="\n")
    return exists


# Функция для упрощения доступа к статическому контенту страницы
def flask_static(file: str):
    return url_for("static", filename=file)
