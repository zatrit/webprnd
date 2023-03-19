import os
import sys
import pytest

sys.path.append("..")
os.chdir("test/")

pytest.main()