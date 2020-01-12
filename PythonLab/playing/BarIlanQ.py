import itertools
from collections import defaultdict

from sympy.combinatorics import Permutation

size = 7
dic = defaultdict(list)
permutationsLs = [Permutation(list(per)) for per in itertools.permutations(range(size))]
for first in permutationsLs:
	for second in permutationsLs:
		if first * second == second * first:
			dic[first].append(second)
ls2 = [frozenset(obj) for obj in dic.values()]

print("S7:", len(set(ls2)))

ls = []
dic = defaultdict(list)
permList = [obj for obj in itertools.permutations(range(size)) if Permutation(list(obj)).signature() == 1]
for first in permList:
	for second in permList:
		if Permutation(list(first)) * Permutation(list(second)) == Permutation(list(second)) * Permutation(list(first)):
			ls.append(second)
			dic[first].append(Permutation(list(second)))
ls2 = [frozenset(obj) for obj in dic.values()]

print("A7:", len(set(ls2)))
