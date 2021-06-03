import numpy as np
import pandas as pd

MIN_RANDOM = 0
MAX_RANDOM = 100

VARIABLES = ['A', 'B', 'C']


def make_df(s: str, n: int):
    delta = MAX_RANDOM - MIN_RANDOM
    max_prefix = MIN_RANDOM + int(delta / 2)
    prefix_random_array = np.random.randint(MIN_RANDOM, max_prefix, size=n)
    max_suffix = MAX_RANDOM - max_prefix

    df = pd.DataFrame()
    for var in VARIABLES:
        suffix_random = np.random.randint(0, max_suffix)
        df[var] = prefix_random_array + suffix_random

    # more efficient than that would be to split the data to multiprocess, relevant for very big n
    df['result'] = df.eval(s)

    df['formula'] = ""
    for c in s:
        if c in VARIABLES:
            df['formula'] += df[c].astype(str)
        else:
            df['formula'] += c

    return df['formula'] + " = " + df['result'].astype(str)


if __name__ == '__main__':
    result = make_df('2*A+B/C', 100)
    [print(value) for value in result.values]
