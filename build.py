#!/usr/bin/env python
# Для работы скрипта необходимы такие пакеты Node.js, как esbuild

# Я не очень хорошо разбираюсь в JavaScript, поэтому вероятно чего-то не знаю.
# Но мне нужна библиотека VisJS для работы сайта

# И так, перед запуском этого скрипта надо установить NodeJS и npm,
# а затем выполнить команду npm install в корневой папке репозитория,
# чтобы установить все зависимости проекта

# И так, к причинам существования этого скрипта:
# 1. Я верю в то, что у CDN'ов сервера быстрее, чем у меня, и если загружать
# JavaScript-библиотеки с помощью JSDelivr, то это оптимизирует загрузку страницы

# И теперь к функционалу этого скрипта:
# Он компилирует онтент веб-страниц, находящийся в папке web/ с помощью
# esbuild. Если не передан параметр --dont-minify, минимизирует их во
# время компиляции

from io import BytesIO, StringIO
from os import path, makedirs
from glob import glob
import sys
import ujson
from subprocess import check_output
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--node-bin", type=str, default="./node_modules/.bin/",
                    help="Путь к каталогу с исполняемыми файлами Node")
parser.add_argument("--dont-minify", default=True,
                    dest="minify", action="store_false",
                    help="Выключает минификацию скриптов с помощью esbuild")
parser.add_argument("--out-dir", type=str, default="static/",
                    help="Выходной путь")
parser.add_argument("--src-dir", type=str, default="web/",
                    help="Входной путь")
parser.add_argument("--encoding", type=str, default="utf8")
args = parser.parse_args()

shell = sys.platform == "win32"


def node_path(file: str):
    return path.join(args.node_bin, file).replace("/", path.sep)


def esbuild(content: str, kind: str) -> bytes:
    proc_args = [node_path("esbuild"), "--loader=" +
                 kind, "--platform=browser"]
    if args.minify:
        proc_args.append("--minify")
    return check_output(proc_args, input=content.encode(args.encoding), shell=shell)


def minify_json(content: str, kind: str) -> bytes:
    assert kind == "json", "Каким-то образом, в minify_json был передан не json"
    return ujson.dumps(ujson.loads(content)).encode("utf8")


# Компилирует все файлы определённого типа
def compile_tree(patt: str, kind: str, line_filter=None, out_ext=None, action=esbuild):
    for src_file in glob(patt, root_dir=args.src_dir, recursive=True):
        print(src_file)
        dest_file = path.join(args.out_dir, ".".join(
            (path.splitext(src_file)[0], out_ext or kind)))

        makedirs(path.split(dest_file)[0], exist_ok=True)

        with open(path.join(args.src_dir, src_file), "r", encoding=args.encoding) as file:
            lines = "".join(filter(line_filter, file))

        with open(dest_file, "wb") as file:
            file.write(action(lines, kind))


compile_tree("**/*.ts", "ts",
             lambda line: not line.startswith("import "), out_ext="js")
compile_tree("**/*.json", "json", action=minify_json)
compile_tree("**/*.css", "css")
