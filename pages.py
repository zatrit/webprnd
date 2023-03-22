from pathlib import Path
from flask import Blueprint, render_template, url_for

blueprint = Blueprint(
    "pages",
    __name__,
    template_folder='templates'
)


@blueprint.route("/editor")
def editor():
    params = {
        "editor_script": url_for("static", filename="script/editor.js"),
        "editor_style": url_for("static", filename="style/editor.css"),
        "title": "Редактор"
    }
    return render_template("editor.html", **params)


def scripts_check() -> bool:
    exists = Path("static/script").exists()
    if not exists:
        print("Вероятно, необходимые для работы сайта скрипты не скомпилированы.",
              "Чтобы запустить сервер, игнорируя это сообщение, используйте --no-scripts-check.",
              "Вы можете скомпилировать скрипты командой tsc (нужен установленный TypeScript), или же скачать уже готовые:",
              "PLACEHOLDER", sep="\n")
    return exists
