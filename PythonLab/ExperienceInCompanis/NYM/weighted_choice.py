import random

# def weighted_choice(values, weights):
#     lists_values_ratio = [[value]*weight for value, weight in zip(values, weights)]
#     values_ratio = []
#     for list_values_ratio in lists_values_ratio:
#         values_ratio.extend(list_values_ratio)
#     value = random.choice(values_ratio)
#     return value

def weighted_choice(values, weights):
    sum_of_weights = sum(weights)
    select_ratio = random.random()
    select_weight = select_ratio*sum_of_weights

    run_weight = 0
    for index, value, weight  in enumerate(zip(values, weights)):
        run_weight+=weight
        if select_weight < run_weight:
            return value
