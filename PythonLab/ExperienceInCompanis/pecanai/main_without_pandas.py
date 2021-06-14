from typing import List
import threading

def say_hello():
    print('Hello, World')

for i in range(5):
    say_hello()

d = [6, 7, 1, 4, 4, 2, 1, 6, 6]

def get_count_of_values(d:List[float]):
    values_count = {}
    for value in d:
        if value not in values_count:
            values_count[value] = 0

        values_count[value] += 1

    return values_count


def sum_values(values_count:dict):
    thread_list = []
    values_sum = {}
    for value, count in values_count.items():
        values_sum[value] = 0
        worker = threading.Thread(target=_sum_value_to_dict, args=(value, count, values_sum))
        worker.start()
        thread_list.append(worker)

    [t.join() for t in thread_list]
    return values_sum

def _sum_value_to_dict(value, count, values_sum):
    for i in range(count):
        values_sum[value] += value

values_count = get_count_of_values(d)
print(values_count)

values_sum = sum_values(values_count)
print(values_sum)


