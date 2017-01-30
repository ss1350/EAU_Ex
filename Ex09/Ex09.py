#!/usr/bin/python3

import numpy as np
import math

"""program that proves experimentally that the algorithm satisfies the calculated
time complexity.
plot for [col=2:3] 'points.txt' using 1:col with lines title columnheader
"""

def ex02old(a):
    """Ex02:
    T(n) = 4 * T(n/2) + n²
    calculated time complexity: n²log(n)
    4 calls of size n/2
    takes subarray a, splits into 4 pieces of size len(a)/2
    recombines solution with an n² runtime
    """
    # print(a)
    # trivial case:
    if len(a) <= 1:
        # print("last call")
        return a
    # create subarrays of size len(a)/2
    l1, l2 = np.array_split(a, 2)
    l3, l4 = l1, l2
    # 4 subproblems
    a1 = ex02(l1)
    a2 = ex02(l2)
    a3 = ex02(l3)
    a4 = ex02(l4)
    # recombination, n²: len(a1) = n/2, n²=(n/2 + n/2) * (n/2 + n/2)
    length = math.ceil((len(a1) + len(a2) + len(a3) + len(a4)) / 2)
    for i in range(length):
        for j in range(length):
            a[i] = np.random.randint(10) + j
    return a


def ex02(a):
    """Ex02:
    T(n) = 4 * T(n/2) + n²
    calculated time complexity: n²log(n)
    4 calls of size n/2
    takes number a, splits into 4 pieces of size a/2
    recombines solution with an n² runtime
    no arrays so c*n is small
    """
    # trivial case
    if a <= 1:
        return a
    # create 4 subproblems of size n/2
    a = math.ceil(a/2)
    a1 = ex02(a)
    a2 = ex02(a)
    a3 = ex02(a)
    a4 = ex02(a)
    # recombine in n² runtime
    for dummy in range(a1+a2):
        for dummy in range(a3+a4):
            c = a1+a2+a3+a4
    return a


if __name__ == "__main__":
    import timeit
    print("n" + "\t" + "tExpAlgo2" + "\t" + "tCalcAlgo2")
    timeex02 = 0
    n = 4
    l0 = []
    l0 = np.random.randint(1000, size=n)
    for dummy in range(10):
        timeex02 += timeit.timeit(stmt=lambda: ex02(n),
                                       setup="from __main__ import " +
                                       "ex02", number=1)
        timecalc02 = (pow(n, 2) * math.log10(n))
        print(str(n) + "\t" + str(timeex02) + "\t" + str(timecalc02) + "\t")
        # np.append(l0, np.random.randint(1000, size=n))
        n *= 2

# EOF