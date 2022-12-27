import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def mkdir_tmp_if_not_exist():
    BASE_DIR = Path(__file__).resolve().parent
    path = os.path.join(BASE_DIR, "tmp")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def pytest_runtest_logstart(nodeid, location):
    print("logstart nodeid={} location={}".format(nodeid, location))
