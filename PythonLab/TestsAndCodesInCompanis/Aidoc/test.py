import json

import pytest

import my_stream


@pytest.fixture()
def test_cases():
	with open('testing_caes.json', 'r') as f:
		jsonData = f.read()
	data = json.loads(jsonData)
	return data


def test(test_cases):
	print()  # blank line
	for case in test_cases:
		iterators_list = case['iterators_list']
		expected_result = case['expected_result']
		print(f'Testing:\n\titerators_list:\t{iterators_list}\n\texpected_result:\t{expected_result}')
		generated_iterator_list = []
		for iter_obj in iterators_list:
			next_iter_item = iter_obj if type(iter_obj).__name__ == 'list_iterator' else iter(iter_obj)
			generated_iterator_list.append(next_iter_item)
		testedObj = iter(my_stream.MyStream(iter(generated_iterator_list)))
		result = []
		for output in testedObj:
			result.append(output)
		assert result == expected_result
