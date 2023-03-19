from flask import Flask
from pathlib import Path

key = Path(".key")
key = key.read_text() if key.exists() else "" # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = key

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)

    args = parser.parse_args()

    app.run(port=args.port)
