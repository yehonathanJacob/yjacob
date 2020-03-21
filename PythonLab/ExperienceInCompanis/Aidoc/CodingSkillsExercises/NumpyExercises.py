__author__ = "Yehonathan Jacob"
__version__ = "0"
__date__ = "04/03/2020"
__email__ = "YehonathanJ@aidoc.com"

# https://www.machinelearningplus.com/python/101-numpy-exercises-python/

import numpy as np

# Q1
np.__version__
# answer:
print(np.__version__)

# Q2
np.array(range(10))
# answer:
np.arange(10)

# Q3
np.array([[True for i in range(3)] for j in range(3)])
# answer:
np.full((3, 3), True, dtype=bool)

# Q4
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

np.array([i for i in arr if i % 2 == 1])
# answer:
arr[arr % 2 == 1]

# Q5
arr = np.arange(10)

for i in arr:
    if i % 2 == 1:
        arr[i] = -arr[i]
# answer:
arr[arr % 2 == 1] = -1

# Q6
arr = np.arange(10)

arr2 = arr.copy()
arr2[arr2 % 2 == 1] = -1
# answer:
out = np.where(arr % 2 == 1, -1, arr)

# Q7
arr = np.arange(10)

arr = np.array([list(arr[:int(len(arr) / 2)]), list(arr[:int(len(arr) / 2)])])
# answer:
arr = arr.reshape(2, -1)

# Q8
a = np.arange(10).reshape(2, -1)
b = np.repeat(1, 10).reshape(2, -1)

np.array(a.tolist() + b.tolist())
# answer:
np.concatenate([a, b], axis=0)
np.vstack([a, b])

# Q9list()
a = np.arange(10).reshape(2, -1)
b = np.repeat(1, 10).reshape(2, -1)

np.concatenate([a, b], axis=1)
np.hstack([a, b])

# Q10
a = np.array([1, 2, 3])

a_part1 = np.repeat(a, 3)
a_part2 = np.array(a.tolist() * 3)
np.concatenate([a_part1, a_part2], axis=0)
# answer
np.r_[np.repeat(a, 3), np.tile(a, 3)]
np.concatenate([np.repeat(a, 3), np.tile(a, 3)], axis=0)

# Q11
a = np.array([1,2,3,2,3,4,3,4,5,6])
b = np.array([7,2,10,2,7,4,9,4,9,8])

np.array(list(set(b)&set(a)))
# answer
np.intersect1d(a,b)

# Q12
a = np.array([1,2,3,4,5])
b = np.array([5,6,7,8,9])

np.array(list(set(a)-set(b)))
# answer
np.setdiff1d(a,b)

# Q13
a = np.array([1,2,3,2,3,4,3,4,5,6])
b = np.array([7,2,10,2,7,4,9,4,9,8])

np.array([i for i in range(min(len(a),len(b))) if a[i] == b[i]])
# answer
np.where(a == b)

# Q14
a = np.array([2, 6, 1, 9, 10, 3, 27])
a[np.where((a>=5) & (a<=10))]

# Q15
a = np.array([5, 7, 9, 8, 6, 4, 5])
b = np.array([6, 3, 4, 8, 9, 7, 1])
def maxx(*parms):
    return max(parms)

pair_max = np.vectorize(maxx, otypes=[float])

pair_max(a, b)

# Q16
arr = np.arange(9).reshape(3,-1)
arr[:,[1,0,2]]

# Q20
rand_arr = np.random.randint(low=5, high=10, size=(5,3)) + np.random.random((5,3))

# Q21
np.set_printoptions(precision=3)

# Q22
np.random.seed(100)
rand_arr = np.random.random([3,3])/1e3
rand_arr

# Q23
np.set_printoptions(threshold=6)
a = np.arange(15)

# Q24
np.set_printoptions(threshold=6)
a = np.arange(15)
np.set_printoptions(threshold=np.nan)

#