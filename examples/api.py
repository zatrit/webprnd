#!/usr/bin/python
# Это пример использования API данного проекта
# Пока что не готов
import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--host", type=str, help="Адрес сервера",
                    default="https://zatrit.pythonanywhere.com/")
args = parser.parse_args()

data = {}

requests.post(args.host + "/api/v1/random", data)