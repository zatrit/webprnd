#!/usr/bin/env python
from data.db_session import global_init
from nodes import init_nodes
from flask import Flask
import flask_ujson
import mimetypes
import pages
import toml
import api

# Исправляет неверный MIME-тип для скриптов и стилей
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")

app = Flask(__name__)
app.config.update({
    "SESSION_COOKIE_SAMESITE": "Strict",
    "SESSION_COOKIE_SECURE": True,
    "SECRET_KEY": "test_key",
    "JSON_SORT_KEYS": False
})
# Загружаем config.toml
app.config.from_file("config.toml", toml.load, True)

app.register_blueprint(pages.blueprint)
app.register_blueprint(api.blueprint)

# Я не использую Flask-SQLAlchemy, так как не
# хочу делать всё приложение зависимым от Flask
global_init("db/users.db")
flask_ujson.init_app(app)
init_nodes()


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    # Я не знаю, зачем это нужно тут,
    # но на всякий случай оставлю это тут
    parser.add_argument("--no-content-check", dest="content_check",
                        action="store_false", default=True)

    args = parser.parse_args()

    if args.content_check and not pages.content_check():
        exit()

    app.run(port=args.port)


if __name__ == "__main__":
    main()
