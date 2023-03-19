from glob import glob
import shutil

patterns = ("**/__pycache__", "**/.pytest_cache", "db")

for paths in (glob(p, recursive=True) for p in patterns):
    for path in paths:
        shutil.rmtree(path)