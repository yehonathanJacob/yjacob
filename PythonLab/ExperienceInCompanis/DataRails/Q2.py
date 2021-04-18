from random import random

def my_func(s:str, n:int):
    arguments_to_random = []
    for char in ['A', 'B', 'C']:
        if char in s:
            s = s.replace(char, f"{{{char}}}")
            arguments_to_random.append(char)

    for _ in range(n):
        format_keywords = {
            k: int(random() * 100)
            for k in arguments_to_random
        }
        s_to_eval = s.format(**format_keywords)
        print(f"{s_to_eval} = {eval(s_to_eval)}")


my_func(s='2*A+B', n=100)