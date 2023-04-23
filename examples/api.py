#!/usr/bin/python
# Это пример использования API данного проекта
# Пока что не готов
from pathlib import Path
import requests
from argparse import ArgumentParser
import urllib.parse as urlparse
import ujson

parser = ArgumentParser()
parser.add_argument("token", type=str)
parser.add_argument("--host", type=str, help="Адрес сервера",
                    default="https://zatrit156.pythonanywhere.com/")
parser.add_argument("--format", type=str, default="base64json")
args = parser.parse_args()

# Дабы не переписывать файл каждый раз, просто напишу так
data = ujson.loads(Path("./web/json/default.project.json").read_text())
data["token"] = args.token
data["format"] = args.format

url = urlparse.urljoin(args.host, "/api/v1/random")
response = requests.post(url, json=data, allow_redirects=False)

print(response.content.decode('unicode_escape'))
