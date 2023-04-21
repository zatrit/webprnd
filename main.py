#!/usr/bin/env python
import toml
import pages
import api
from flask import Flask
import mimetypes
from nodes import init_nodes

# Исправляет неверный MIME-тип для скриптов и стилей
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")

app = Flask(__name__)
app.config.update({
    "SESSION_COOKIE_SAMESITE": "Strict",
    "SESSION_COOKIE_SECURE": True,
    "CONFIG_KEY": "",
    "JSON_SORT_KEYS": False
})
app.config.from_file("config.toml", toml.load, True)

app.register_blueprint(pages.blueprint)
app.register_blueprint(api.blueprint)


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

    from data.db_session import global_init

    global_init("db/users.db")
    init_nodes()

    app.run(port=args.port)


if __name__ == "__main__":
    main()
