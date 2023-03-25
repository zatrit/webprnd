from pathlib import Path
from flask import Blueprint, render_template

blueprint = Blueprint(
    "pages",
    __name__,
    template_folder="templates",
    static_folder="static"
)

static_folder: str = blueprint.static_url_path.lstrip("/")  # type: ignore


@blueprint.route("/editor")
def editor():
    params = {
        "title": "Редактор"
    }
    return render_template("editor.html", **params)


def scripts_check() -> bool:
    exists = Path("static/script").exists()
    if not exists:
        print("Вероятно, необходимые для работы сайта скрипты не скомпилированы.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-scripts-check.",
              "Вы можете скомпилировать скрипты c помощью compile_scripts.py, или же скачать уже готовые:",
              "PLACEHOLDER", sep="\n")
    return exists
