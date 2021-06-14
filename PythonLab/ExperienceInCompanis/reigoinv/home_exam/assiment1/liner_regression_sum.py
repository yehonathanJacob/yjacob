import numpy as np

def liner_regression_sum(d:list):
    d_n_to_1 = np.array(d[1:])
    d_n_1_to_0 = np.array(d[:-1])
    n_1 = len(d) - 1

    ls_to_sum = (d_n_to_1 - d_n_1_to_0) / d_n_1_to_0
    return ls_to_sum.sum() / n_1
