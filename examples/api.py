#!/usr/bin/python
# Это пример использования API данного проекта
# Пока что не готов
import requests
from argparse import ArgumentParser
import urllib.parse as urlparse

parser = ArgumentParser()
parser.add_argument("token", type=str)
parser.add_argument("--host", type=str, help="Адрес сервера",
                    default="https://zatrit.pythonanywhere.com/")
args = parser.parse_args()

data = {
    "token": args.token,
    "nodes": [
        {
            "type": "output",
            "name": "json",
            "id": 0,
            "uses": [1, 2],
            "props": {
                "pretify": True
            }
        },
        {
            "type": "seed",
            "name": "time",
            "id": 1,
        },
        {
            "type": "random",
            "name": "linear_congruential",
            "id": 2,
            "uses": [1],
            "props": {
                "a": 1664525,
                "c": 1013904223,
                "m": 0x7FFFFFFF,
            },
        },
    ]
}

url = urlparse.urljoin(args.host, "/api/v1/random")
response = requests.post(url, json=data)

print(json := response.json())
