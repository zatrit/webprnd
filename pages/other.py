from flask import render_template
from . import blueprint, requires_auth


@blueprint.route("/editor")
@requires_auth
def editor():
    return render_template("editor.html", title="Редактор")
