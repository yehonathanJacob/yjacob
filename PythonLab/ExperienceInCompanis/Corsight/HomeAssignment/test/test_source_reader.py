import os
from tempfile import TemporaryDirectory
import pytest
from SourceReader.sources import PandasReader, DirectoryReader


@pytest.fixture()
def dir_path():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture()
def file1_path(dir_path):
    return os.path.join(dir_path, 'example_files', 'A', 'file1.csv')


@pytest.fixture()
def example_files(dir_path):
    return os.path.join(dir_path, 'example_files')


@pytest.yield_fixture
def tmpdir():
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_pandas_reader_basic(file1_path):
    pandas_reader = iter(PandasReader(file1_path))
    for pandas_value, test_value in zip(pandas_reader, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
        assert pandas_value == test_value



def test_pandas_reader_file_not_found(tmpdir):
    file_path = os.path.join(tmpdir, "tmp.tmp")
    with pytest.raises(FileNotFoundError):
        PandasReader(file_path)


def test_pandas_reader_got_directory(tmpdir):
    with pytest.raises(IsADirectoryError):
        PandasReader(tmpdir)


def test_directory_reader_basic(dir_path, example_files):
    directory_reader = iter(DirectoryReader(example_files))
    assert len(list(directory_reader)) == 5


def test_directory_reader_not_found(dir_path, file1_path):
    with pytest.raises(NotADirectoryError):
        directory_reader = DirectoryReader(file1_path)
