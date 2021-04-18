# you can write to stdout for debugging purposes, e.g.
print("This is a debug message")
arr = [3, -8, 5, 2, -5]

arr2 = [1, 2, -1, 9, 14, 0, 0, 0]


def is_three_zero(arr):
    sorted_arr = sorted(arr)

    founded = set()

    for x in arr:
        expecting_for = 0 - x
        left_arr = sorted_arr.copy()
        left_arr.remove(x)
        i = 0
        j = len(left_arr) - 1
        while i < j:
            if left_arr[i] + left_arr[j] == expecting_for:
                founded_list = sorted([x, left_arr[i], left_arr[j]])
                founded_tuple = tuple(founded_list)
                if founded_tuple not in founded:
                    founded.add(founded_tuple)
                    break

            if left_arr[i] + left_arr[j] > expecting_for:
                j += -1
            else:
                i += 1

    return founded


print(is_three_zero(arr2))
