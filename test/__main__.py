# Этот скрипт позволяет вынести скрипты для тестов
# в отдельную папку, чтобы не засорять корневой каталог
# проекте тестами
import os
import sys
import pytest

sys.path.append("..")
os.chdir("test/")

pytest.main()