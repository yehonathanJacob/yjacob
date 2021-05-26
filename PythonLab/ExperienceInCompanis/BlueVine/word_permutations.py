word_dict = {}

def prepare_key(word):
    sorted_word = sorted(word)
    return tuple(sorted_word)

def get_word_permutations(word):
    key = prepare_key(word)

    if key not in word_dict:
        word_dict[key] = set()

    word_dict[key].add(word)

    return list(word_dict[key])

print(get_word_permutations('abab'))    # ['abab']
print(get_word_permutations('aabb'))    # ['aabb', 'abab']
print(get_word_permutations('abc'))     # ['abc']
print(get_word_permutations('bbaa'))    # ['aabb', 'bbaa', 'abab']
print(get_word_permutations('abab'))    # ['aabb', 'bbaa', 'abab']
