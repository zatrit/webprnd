# Для работы скрипта необходимы такие пакеты Node.js, как typescript и minify

# Я не очень хорошо разбираюсь в JavaScript, поэтому вероятно чего-то не знаю.
# Но мне нужна библиотека VisJS для работы сайта

# И так, к причинам существования этого скрипта:
# 1. Большинство упаковщиков (Java|Type)Script не понимают, что функция createBlock
# нужна, и просто удаляют её.
# 2. Я верю в то, что у JSDelivr сервера быстрее, чем у меня, и если загружать
# тяжёлые скрипты, такие как VisJS с помощью JSDelivr, то это оптимизирует
# загрузку страницы

# И теперь к функционалу этого скрипта:
# Он просто компилирует все* .ts скрипты, удаляет из них import'ы кода, которые
# браузер не может разрешить и завершается с кодом 0

# (*) на момент написания скрипта 1

import os
from glob import glob
import sys
import json5 as json
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--tsc", type=str, default="tsc")
parser.add_argument("--config", type=str, default="tsconfig.json")
parser.add_argument("--dont-minify", default=True,
                    dest="minify", action="store_false")
parser.add_argument("--style-src", type=str, default="web/style/")
parser.add_argument("--style-dest", type=str, default="static/style/")
args = parser.parse_args()


def minify(content: str, kind: str) -> bytes:
    if args.minify:
        shell = sys.platform in ("win32", "cygwin")
        return subprocess.check_output(
            ["minify", "--" + kind, script_file], input=content.encode("utf8"), shell=shell)
    else:
        return content.encode("utf8")


assert os.system(args.tsc) == 0, \
    "TypeScript не установлен или не удалось скомпилировать .ts скрипты"

with open(args.config, "r") as tsconfig:
    scripts_dir = json.load(
        tsconfig)["compilerOptions"]["outDir"]  # type: ignore

os.makedirs(scripts_dir, exist_ok=True)
os.makedirs(args.style_dest, exist_ok=True)

for script_file in glob("*.js", root_dir=scripts_dir, recursive=True):
    print(script_file)
    script_file = os.path.join(scripts_dir, script_file)

    with open(script_file, "r", encoding="utf8") as file:
        lines = "".join(
            filter(lambda line: not line.startswith("import "), file))

    with open(script_file, "wb") as file:
        file.write(minify(lines, "js"))

for style_file in glob("*.css", root_dir=args.style_src):
    print(style_file)
    src_file = os.path.join(args.style_src, style_file)
    dest_file = os.path.join(args.style_dest, style_file)

    with open(src_file, "r", encoding="utf8") as file:
        lines = file.read()

    with open(dest_file, "wb") as file:
        file.write(minify(lines, "css"))
