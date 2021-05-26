import os
from tempfile import TemporaryDirectory
from distutils.dir_util import copy_tree

import pytest
from fastapi.testclient import TestClient

from WebServer.main import app, Directories

client = TestClient(app)


@pytest.fixture()
def example_files():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example_files')


@pytest.yield_fixture
def tmpdir(example_files):
    with TemporaryDirectory() as tmpdir:
        copy_tree(example_files, tmpdir)
        yield tmpdir


def test_basic():
    response = client.get("/")
    assert response.status_code == 200


def test_add_row(tmpdir):
    Directories.setup_directories(tmpdir)
    response = client.get("/add_row/A?values=1&values=3&values=2&file_name=tmpfile.csv")

    assert response.json() == {"side": "A", "number_of_values": 3, "file_name": "tmpfile.csv"}


def test_match(tmpdir):
    Directories.setup_directories(tmpdir)
    response = client.get("/match/6")

    assert response.json() == ["file1.csv\t10"]


def test_status(tmpdir):
    Directories.setup_directories(tmpdir)
    response = client.get("/status/")

    assert response.json() == {"A": 2, "B": 3}
