def reverse_func(function):
    def run_function_with_reverse_args(*args, **keywords):
        return function(*args[::-1], **keywords)

    return run_function_with_reverse_args


@reverse_func
def print_args(*args, **keywords):
    for arg in args:
        print(f"arg: {arg}")

    for k, v in keywords.items():
        print(f"keyword: k:{k} v:{v}")


@reverse_func
def sub(a, b):
    return a - b



if __name__ == '__main__':
    print_args()
    print_args(1, 2, 3, 4)
    print_args(1, 2, 3, 4, a=5, b=6, c=7)

    print(sub(3, 2))
    print(sub(a=3, b=2))


