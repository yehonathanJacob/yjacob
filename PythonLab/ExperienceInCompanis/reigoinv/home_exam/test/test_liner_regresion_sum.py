import pytest

from assiment1.liner_regression_sum import liner_regression_sum


def test_end_to_end():
    d = list(range(1,11))
    predicted_result = liner_regression_sum(d)
    values_to_sum = [
        (d[i]-d[i-1])/d[i-1]
        for i in range(1,len(d))
    ]
    ground_true_result = sum(values_to_sum) / (len(d)-1)
    assert predicted_result == ground_true_result