import pages
from flask import Flask
from pathlib import Path

key = Path(".key")
key = key.read_text() if key.exists() else ""  # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = key


app.register_blueprint(pages.blueprint)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--no-scripts-check", dest="scripts_check",
                        action="store_false", default=True)

    args = parser.parse_args()

    if args.scripts_check and not pages.scripts_check():
        exit()

    from data.db_session import global_init

    global_init("db/users.db")

    app.run(port=args.port)


if __name__ == "__main__":
    main()
