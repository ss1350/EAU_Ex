#!/usr/bin/python3

import random
from itertools import count, islice
import math
# import matplotlib.pyplot as plt -> VERY SLOW?

"""Write a program that generates a set of n
    random whole numbers and measures
    the runtime for both (A) and (B) with
    n as input. Repeat the measurement three times for each
    procedure and take the mean.
    Plotted with gnuplot,
    set logscale x 10
    plot for [col=2:3] 'test.txt' using 1:col with lines title columnheader
"""


# =============================================================================
# copied from ex05
# =============================================================================
def isPrime(n):
    """check for prime number
    """
    if n < 2:
        return False
    for number in islice(count(2), int(math.sqrt(n)-1)):
        if not n % number:
            return False
    return True


class HashFunction:
    """     h (a,b) (x) = ((ax + b) mod p) mod m
    """
    def __init__(self, a, b, p, u, m):
        """a, b, p (the prime number), u (universe size), m (hash table size)
        only one hash function per hash table!
        Cond: p a prime number ≥ U and m the size of the hash table with p > m
        1 ≤ a < p, 0 ≤ b < p
        """
        if not (isPrime(p)):
            raise ValueError("p Not a prime Number!")
        if not p >= u:
            raise ValueError("p smaller than u!")
        if not p > m:
            raise ValueError("p <= m!")
        if not 1 <= a < p:
            raise ValueError("Is not 1 ≤ a < p!")
        if not 0 <= b < p:
            raise ValueError("Is not 0 ≤ b < p!")
        self.a, self.b, self.p, self.u, self.m = a, b, p, u, m
        self.table = []
        for i in range(m):
            self.table.append([])

    def apply(self, x):
        """apply hash function specified above to a given
        key value and return hash table index
        """
        index = ((self.a * x + self.b) % self.p) % self.m
        self.table[index].append(x)
        return index

    def get_table(self):
        """returns the hash table
        """
        return self.table
# ==============================================================================
# end of ex05 copy
# ==============================================================================

    def clear_table(self):
        """clears the table, creates a new one
        """
        self.table = []
        for i in range(self.m):
            self.table.append([])


def quicksort(l, start, end):
    """Quicksort the list l, begin at start, end at end,
    recursive!
    Pivotelement at beginning of list.
    """
    if (end - start) < 1:
        return
    i = start
    k = end
    piv = l[start]
    while k > i:
        while l[i] <= piv and i <= end and k > i:
            i += 1
        while l[k] > piv and k >= start and k >= i:
            k -= 1
        if k > i:
            # swap  elements
            (l[i], l[k]) = (l[k], l[i])
    (l[start], l[k]) = (l[k], l[start])
    quicksort(l, start, k - 1)
    quicksort(l, k + 1, end)


def calvAvgRuntimeAndPlot(h, maxp):
    """Calculate the averaged runtime from exercise 2 for
    Increase n as long as your computer is okay with it and the
    computation time is still bearable. Generate a plot with the value of
    n on the x-axis (logarithmic scale) and a curve for the runtime of (A)
    as well as curve for the runtime of (B) (different color).
    """
    def testFnc(l1, h):
        for i in range(len(l1) - 1):
            h.apply(l1[i])

    for p in range(17, maxp):
        n = pow(2, p)
        timeQuicksort = 0
        timeHashtable = 0
        h.clear_table()
        for i in range(3):
            l = createRandomList(n, n)
            l1 = l[:]
            # quicksort
            timeQuicksort += timeit.timeit(stmt=lambda:
                                           quicksort(l, 0, len(l) - 1),
                                           setup="from __main__ import " +
                                           "quicksort", number=1)
            # hash table
            timeHashtable += timeit.timeit(stmt=lambda: testFnc(l1, h),
                                           number=1)
        yield(n, timeQuicksort/3, timeHashtable/3)


def createRandomList(length, maxvalue):
    """create a list with length number of random integers
    smaller than maxvaulue
    """
    l = list()
    for i in range(length):
        l.append(random.randint(0, maxvalue))
    return l


if __name__ == "__main__":
    import timeit
    meanTimeQuicksort = 0
    meanTimeHashtable = 0
    u = 100
    m = 100
    p = 101
    k = 20
    n = 1000
    h = HashFunction(1, 0, p, u, m)

    def testFnc(l1, h):
        for i in range(len(l1) - 1):
            h.apply(l1[i])

    for i in range(3):
        l = createRandomList(pow(2, 10), pow(2, 10))
        l1 = l[:]
        # quicksort
        meanTimeQuicksort += timeit.timeit(stmt=lambda: quicksort(l, 0,
                                                                  len(l) - 1),
                                           setup="from __main__ import " +
                                           "quicksort", number=1)
        # hash table
        meanTimeHashtable += timeit.timeit(stmt=lambda: testFnc(l1, h),
                                           number=1)
        h.clear_table()
    # print(meanTimeQuicksort, meanTimeHashtable)
    maxp = 25
    gen = calvAvgRuntimeAndPlot(h, maxp)
    print("n" + "\t" + "tQuick" + "\t" + "tHeap")
    for i in range(maxp - 1):
        n, tQuick, tHash = next(gen)
        print(str(n) + "\t" + str(tQuick) + "\t" + str(tHash))

# EOF
