#!/usr/bin/env python
# Для работы скрипта необходимы такие пакеты Node.js, как esbuild

# Я не очень хорошо разбираюсь в JavaScript, поэтому вероятно чего-то не знаю.
# Но мне нужны библиотеки для работы сайта

# И так, перед запуском этого скрипта надо установить NodeJS и npm,
# а затем выполнить команду npm install в корневой папке репозитория,
# чтобы установить все зависимости проекта

# И так, к причинам существования этого скрипта:
# 1. Их нету, просто гибкий скрипт для сборки проекта

# И теперь к функционалу этого скрипта:
# Он компилирует онтент веб-страниц, находящийся в папке web/ с помощью
# esbuild. Если передан параметр --minify, минимизирует их во время компиляции

from os import path, makedirs
import shutil
import sys
from argparse import ArgumentParser
from subprocess import run, DEVNULL
from typing import Callable
from glob import glob

parser = ArgumentParser()
parser.add_argument("--node-bin", type=str, default="./node_modules/.bin/")
parser.add_argument("--minify", action="store_true", default=False)
parser.add_argument("--encoding", type=str, default="utf8")
parser.add_argument("--root-dir", type=str, default="web/")
parser.add_argument("--out-dir", type=str, default="static/")
args = parser.parse_args()

shell = sys.platform == "win32"

BuildAction = Callable[[str, str], None]


def node_path(file: str):
    return path.join(args.node_bin, file).replace("/", path.sep)


def esbuild(*additional_args: str):
    def _build(source: str, out: str):
        esbuild_path = node_path("esbuild")
        proc_args = [esbuild_path, source, "--outfile="+out, *additional_args]
        if args.minify:
            proc_args += ["--minify"]

        run(proc_args, shell=shell, stdout=DEVNULL, check=True)

    return _build


def build(pattern: str, action: BuildAction, out_ext: str | None = None):
    root_dir = args.root_dir
    for filename in glob(pattern, root_dir=root_dir, recursive=True):
        print(filename.replace(path.sep, "/"))
        *name, ext = filename.split(".")
        name = ".".join(name)
        if not out_ext:
            out_ext = ext
        out_file = path.join(args.out_dir, name + "." + out_ext)
        makedirs(path.abspath(path.join(out_file, path.pardir)), exist_ok=True)

        action(path.join(root_dir, filename), out_file)


build("script/editor.ts", esbuild("--bundle", "--platform=browser", "--format=iife"), "js")
build("**/*.css", esbuild())
build("**/*.json", shutil.copy)
