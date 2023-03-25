# Для работы скрипта необходимы такие пакеты Node.js, как typescript и minify

# Я не очень хорошо разбираюсь в JavaScript, поэтому вероятно чего-то не знаю.
# Но мне нужна библиотека PixiJS для отрисовки некоторых элементов страницы,
# которые я не способен сделать на чистом HTML + CSS.

# И так, к причинам существования этого скрипта:
# 1. Большинство упаковщиков (Java|Type)Script не понимают, что функция createBlock
# нужна, и просто удаляют её.
# 2. Я верю в то, что у JSDelivr сервера быстрее, чем у меня, и если загружать
# тяжёлые скрипты, такие как PixiJS с помощью JSDelivr, то это оптимизирует
# загрузку страницы

# И теперь к функционалу этого скрипта:
# Он просто компилирует все* .ts скрипты, удаляет из них import'ы кода, которые
# браузер не может разрешить и завершается с кодом 0

# (*) на момент написания скрипта 1

import os
from glob import glob
import json5 as json
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--tsc", type=str, default="tsc")
parser.add_argument("--config", type=str, default="tsconfig.json")
parser.add_argument("--dont-minify", default=True,
                    dest="minify", action="store_false")
args = parser.parse_args()

assert os.system(args.tsc) == 0, \
    "TypeScript не установлен или не удалось скомпилировать .ts скрипты"

with open(args.config, "r") as tsconfig:
    scripts_dir = json.load(
        tsconfig)["compilerOptions"]["outDir"]  # type: ignore

for script_file in glob("*.js", root_dir=scripts_dir, recursive=True):
    print(script_file)
    script_file = os.path.join(scripts_dir, script_file)

    with open(script_file, "r", encoding="utf8") as file:
        lines = "".join(
            filter(lambda line: not line.startswith("import "), file))

    if args.minify:
        minified = subprocess.check_output(
            ["minify", "--js", script_file], input=lines.encode("utf8"), shell=True)
    else:
        minified = lines.encode("utf8")

    with open(script_file, "wb") as file:
        file.write(minified)
