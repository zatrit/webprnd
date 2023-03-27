#!/usr/bin/env python
import pages
from flask import Flask
from pathlib import Path
import mimetypes

# Исправляет неверный MIME-тип для скриптов и стилей
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

key = Path(".key")
key = key.read_text() if key.exists() else ""  # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = key

app.register_blueprint(pages.blueprint)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--no-content-check", dest="content_check",
                        action="store_false", default=True)

    args = parser.parse_args()

    if args.content_check and not pages.content_check():
        exit()

    from data.db_session import global_init

    global_init("db/users.db")

    app.run(port=args.port)


if __name__ == "__main__":
    main()
