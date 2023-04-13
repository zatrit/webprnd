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
import sys
from argparse import ArgumentParser
from typing import Callable
import shutil

parser = ArgumentParser()
parser.add_argument("--node-bin", type=str, default="./node_modules/.bin/")
parser.add_argument("--minify", action="store_true", default=False)
parser.add_argument("--encoding", type=str, default="utf8")
parser.add_argument("--root-dir", type=str, default="web/")
parser.add_argument("--out-dir", type=str, default="static/")
args = parser.parse_args()

shell = sys.platform == "win32"

BuildAction = Callable[[str, str], None]
BytesAction = Callable[[bytes], bytes]


def node_path(file: str):
    return path.join(args.node_bin, file).replace("/", path.sep)


def esbuild(*additional_args: str):
    from subprocess import run, DEVNULL

    def _build(source: str, out: str):
        esbuild_path = node_path("esbuild")
        proc_args = [esbuild_path, source, "--outfile="+out, *additional_args]
        if args.minify:
            proc_args += ["--minify", "--drop:console", "--drop:debugger",
                          "--ignore-annotations", "--mangle-props=_$", "--tree-shaking=true"]

        run(proc_args, shell=shell, stdout=DEVNULL, check=True)

    return _build


def svg_scour(source: str, out: str):
    from scour import scour
    with open(source, "rb") as infile, open(out, "wb") as outfile:
        scour.start({}, infile, outfile)


def png_zopfli(source: str, out: str):
    from zopfli import ZopfliPNG
    zopfli_png = ZopfliPNG(True)
    with open(source, "rb") as infile, open(out, "wb") as outfile:
        outfile.write(zopfli_png.optimize(infile.read()))


def json(source: str, out: str):
    import ujson
    with open(source, "r") as infile, open(out, "w") as outfile:
        ujson.dump(ujson.load(infile), outfile)


def minify_or_copy(func: BuildAction):
    """Способ оптимизации сборки, подразумевающий уменьшение времени
    засчёт простого копирования контента, работающего без компиляции"""
    return func if args.minify else shutil.copy


def build(pattern: str, action: BuildAction, out_ext: str | None = None,
          root_dir: str = args.root_dir, out_dir: str = args.out_dir):
    from glob import glob
    for filename in glob(pattern, root_dir=root_dir, recursive=True):
        print(filename.replace(path.sep, "/"))
        *name, ext = filename.split(".")
        name = ".".join(name)
        if not out_ext:
            out_ext = ext
        out_file = path.join(out_dir, name + "." + out_ext)
        makedirs(path.abspath(path.join(out_file, path.pardir)), exist_ok=True)

        action(path.join(root_dir, filename), out_file)


build_ts = esbuild("--bundle", "--platform=browser", "--format=iife")
md_dir = path.join(args.out_dir, "md")

build("script/editor.ts", build_ts, "js")
build("script/index.ts", build_ts, "js")
build("**/*.png", minify_or_copy(png_zopfli))
build("**/*.css", minify_or_copy(esbuild()))
build("**/*.json", minify_or_copy(json))
build("**/*.svg", minify_or_copy(svg_scour))
build("readme.md", shutil.copy, root_dir=".", out_dir=md_dir)
