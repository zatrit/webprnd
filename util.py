from flask import url_for

def flask_static(file: str):
    return url_for("static", filename=file)