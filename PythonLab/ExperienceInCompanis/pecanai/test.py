import pytest
from main_without_pandas import get_count_of_values, sum_values

@pytest.fixture
def sample_list():
    return [6, 7, 1, 4, 4, 2, 1, 6, 6]


def tes_basic(sample_list):
    values_count = get_count_of_values(sample_list)
    assert values_count == {6: 3, 7: 1, 1: 2, 4: 2, 2: 1}

    values_sum = sum_values(values_count)
    assert values_sum == {6: 18, 7: 7, 1: 2, 4: 8, 2: 2}



def test_pow_value_count(sample_list):
    values_count = get_count_of_values(sample_list)
    values_sum = sum_values(values_count)
    assert values_sum == {6: 18, 7: 7, 1: 2, 4: 8, 2: 2}




