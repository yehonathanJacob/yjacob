import math
import numpy as np

DEFAULT_MAX_FILTERS = 100


def db_query(table_name, **kwargs):
    where_clause = ' and '.join([f'{x} in ({",".join([t for t in y])})' for x, y in kwargs.items()])
    return f'SELECT * from {table_name} where {where_clause}'


def my_db_query(table_name, **kwargs):
    query_generator = QueryGenerator(table_name, kwargs)
    return query_generator.generate_query()


class QueryGenerator:
    def __init__(self, table_name, all_condition: dict):
        self.table_name = table_name
        self.all_condition = all_condition

    def generate_query(self, max_filters: int = DEFAULT_MAX_FILTERS):
        remain_conditions = list(self.all_condition.keys())
        current_condition = {}
        return self.recursion_create_query(remain_conditions, current_condition, max_filters)

    def recursion_create_query(self, conditions: list, current_condition: dict, max_filters: int = DEFAULT_MAX_FILTERS):
        if len(conditions) == 0:
            return [db_query(self.table_name, **current_condition)]

        next_condition = conditions[0]
        remain_conditions = conditions[1:]

        number_of_option = len(self.all_condition[next_condition])
        number_of_bins = math.ceil(number_of_option / max_filters)
        bin_list = np.array_split(self.all_condition[next_condition], number_of_bins)
        query_list = []

        for bin_of_options in bin_list:
            current_condition[next_condition] = list(bin_of_options)
            queries_with_current_bin = self.recursion_create_query(remain_conditions, current_condition, max_filters)
            query_list.extend(queries_with_current_bin)

        return query_list


if __name__ == '__main__':
    table_name = 'Test1'
    conditions = {
        'A': ['1', '2', '3'],
        'B': ['a', 'b', 'c', 'd']
    }
    max_filters = 2
    query_generator = QueryGenerator(table_name, conditions)
    results = query_generator.generate_query(max_filters)
    assert results == [
        'SELECT * from Test1 where A in (1,2) and B in (a,b)',
        'SELECT * from Test1 where A in (1,2) and B in (c,d)',
        'SELECT * from Test1 where A in (3) and B in (a,b)',
        'SELECT * from Test1 where A in (3) and B in (c,d)'
    ]

    table_name = 'Test2'
    conditions = {
        'A': [str(x) for x in range(100)]
    }
    results = my_db_query(table_name, **conditions)
    assert len(results) == 1

    table_name = 'Test2'
    conditions = {
        'A': [str(x) for x in range(150)],
        'B': [str(x) for x in range(300)],
    }
    results = my_db_query(table_name, **conditions)
    assert len(results) == 6

    print('All tests pass')
