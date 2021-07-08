from typing import List
import threading

import pandas as pd


def say_hello():
    print('Hello, World')

for i in range(5):
    say_hello()

d = [6, 7, 1, 4, 4, 2, 1, 6, 6]

def get_count_of_values(d:List[float]):
    df_values = pd.DataFrame(d)
    values_count = df_values[0].value_counts()
    df_values_count = pd.DataFrame({'value':values_count.index, 'count':values_count.values})
    return df_values_count

def pow_value_count(value, count, result_list):
    result = value
    for i in range(count-1):
        result += value

    result_list.append([value, result])

def pow_values(df_values_count:pd.DataFrame):
    thread_list = []
    results = []
    for index, row in df_values_count.iterrows():
        worker = threading.Thread(target=pow_value_count, args=(row['value'], row['count'], results))
        worker.start()
        thread_list.append(worker)

    [t.join() for t in thread_list]
    df_values_sum = pd.DataFrame(results, columns={'sum', 'value'})
    return df_values_sum

df_values_count = get_count_of_values(d)
df_values_count.apply(lambda row: print(f"{row['value']}: {row['count']}"), axis =1)

df_values_sum = pow_values(df_values_count)
df_values_sum.apply(lambda row: print(f"{row['value']}: {row['sum']}"), axis =1)


