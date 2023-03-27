#!/usr/bin/env python
# Для работы скрипта необходимы такие пакеты Node.js, как typescript и minify

# Я не очень хорошо разбираюсь в JavaScript, поэтому вероятно чего-то не знаю.
# Но мне нужна библиотека VisJS для работы сайта

# И так, перед запуском этого скрипта надо установить NodeJS и npm,
# а затем выполнить команду npm install в корневой папке репозитория,
# чтобы установить все зависимости проекта

# И так, к причинам существования этого скрипта:
# 1. Большинство упаковщиков (Java|Type)Script не понимают, какие функции
# мне нужны, а какие нет
# 2. Я верю в то, что у CDN'ов сервера быстрее, чем у меня, и если загружать
# JavaScript-библиотеки с помощью JSDelivr/Unpkg, то это оптимизирует загрузку страницы

# И теперь к функционалу этого скрипта:
# Он компилирует все* .ts скрипты, удаляет из них import'ы кода, которые
# браузер не может найти, минимизирует файлы и стилей и завершается с кодом 0

# Контент веб-страниц находится в папке web/

# (*) на момент написания скрипта 1

from os import path, makedirs
from glob import glob
import sys
import json5 as json
from subprocess import DEVNULL, check_output, run as run_process
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--tsc", type=str, default="tsc",
                    help="Компилятор TypeScript")
parser.add_argument("--config", type=str,
                    default="tsconfig.json", help="Файл tsconfig.json")
parser.add_argument("--dont-minify", default=True,
                    dest="minify", action="store_false",
                    help="Выключает минификацию скриптов")
args = parser.parse_args()

shell = sys.platform in ("win32", "cygwin")


def minify(content: str, kind: str) -> bytes:
    if args.minify:
        return check_output(
            ["minify", "--" + kind, script_file], input=content.encode("utf8"), shell=shell)
    else:
        return content.encode("utf8")


run_options = {"stdout": DEVNULL, "shell": shell}

# Компиляция скриптов с помощью tsc
assert run_process([args.tsc, "-p", args.config], **run_options).returncode == 0, \
    "TypeScript не установлен или не удалось скомпилировать .ts скрипты"

# Проерка на наличие minify
assert not args.minify or run_process(["minify", "-v"], **run_options).returncode == 0, \
    "minify не установлен, используйте npm install или параметр --dont-minify"

with open(args.config, "r") as tsconfig:
    compile_options = json.load(tsconfig)["compilerOptions"]  # type: ignore
    out_dir = compile_options["outDir"]
    src_dir = compile_options["rootDir"]

makedirs(out_dir, exist_ok=True)

for script_file in glob("**/*.js", root_dir=out_dir, recursive=True):
    print(script_file)
    script_file = path.join(out_dir, script_file)

    with open(script_file, "r", encoding="utf8") as file:
        lines = "".join(
            filter(lambda line: not line.startswith("import "), file))

    with open(script_file, "wb") as file:
        file.write(minify(lines, "js"))

for style_file in glob("**/*.css", root_dir=src_dir, recursive=True):
    print(style_file)
    dest_file = path.join(out_dir, style_file)
    makedirs(path.split(dest_file)[0], exist_ok=True)

    with open(path.join(src_dir, style_file), "r", encoding="utf8") as file:
        lines = file.read()

    with open(dest_file, "wb") as file:
        file.write(minify(lines, "css"))
