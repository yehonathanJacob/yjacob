import os
from tempfile import TemporaryDirectory
import pytest

from ParallelMatching.parallel_matching import ParallelMatching, Match


@pytest.fixture()
def dir_path():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture()
def A_dir(dir_path):
    return os.path.join(dir_path, 'example_files', 'A')


@pytest.fixture()
def B_dir(dir_path):
    return os.path.join(dir_path, 'example_files', 'B')


@pytest.fixture()
def X():
    return 6


@pytest.yield_fixture
def C_dir():
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_matches_results(dir_path, A_dir, B_dir, X):
    pm = ParallelMatching(A_dir, B_dir, X)
    matches_results = pm.load_matches_results()
    matches_results_set = set(matches_results)

    assert matches_results_set == {Match(source_of_file=os.path.join(A_dir, "file1.csv"), num_intersection=10)}


def test_end_to_end(dir_path, A_dir, B_dir, C_dir, X):
    ParallelMatching.run_parallel_matching(A_dir, B_dir, C_dir, X)

    files_in_C = os.listdir(C_dir)
    assert len(files_in_C) == 2
    assert "scores.txt" in files_in_C
    assert "file1.csv" in files_in_C
    with open(os.path.join(C_dir, "scores.txt")) as f:
        sources_content = f.read()

        assert sources_content == "file1.csv\t10"
