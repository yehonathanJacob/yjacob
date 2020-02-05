import Q4
import json

def pytest_generate_tests(metafunc):
    if 'caseName' not in metafunc.fixturenames:
        return
    with open('testCases.json', 'r') as file:
        testCases = json.loads(file.read())
    paramList = [[case_name, data]
                 for case_name, data in testCases.items()]
    metafunc.parametrize("caseName,data", paramList)

def test_each_of_the_cases(caseName,data):
    for case in data:
        sum, expectedResult = case['sum'], case['res']
        result = Q4.sumObjects(*sum)
        assert expectedResult == result, error_format(caseName,sum,expectedResult,result)


def error_format(caseName,sum,expectedResult,result):
    return f"In case: {caseName}, for: {sum}\n\t expected: {expectedResult} got: {result}"

# def test_checkElse(checkElse, expectedResult):
#     result = Q4.sumObjects(*checkElse)
#     assert expectedResult == result, f"for: {checkElse}\n\t expected: {expectedResult} got: {result}"
#
#
# testCases = [
#     # (objects to test,..,expected result)
#     ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),
#     (1, 2, 3, 4, 10),
#     ('a', 'b', 'ab'),
#     ('abc', 'def', 'abcdef'),
#     (None, None)
# ]
#
#
# def test_sumObjects():
#     for case in testCases:
#         objectsToSum = case[:-1]
#         expectedResult = case[-1]
#         result = Q4.sumObjects(*objectsToSum)
#         assert expectedResult == result, f"for: {objectsToSum}\n\t expected: {expectedResult} got: {result}"
