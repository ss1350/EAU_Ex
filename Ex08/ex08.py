#!/usr/bin/python3

import random
import time
# import matplotlib.pyplot as plt -> VERY SLOW?

"""Write a program that generates a set of n
    random whole numbers and measures
    the runtime for both (A) and (B) with
    n as input. Repeat the measurement three times for each
    procedure and take the mean.
    Plotted with gnuplot,
    plot for [col=2:3] 'test.txt' using 1:col with lines title columnheader
"""


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


def calvAvgRuntimeAndPlot(maxp):
    """Calculate the averaged runtime from exercise 2 for
    Increase n as long as your computer is okay with it and the
    computation time is still bearable. Generate a plot with the value of
    n on the x-axis (logarithmic scale) and a curve for the runtime of (A)
    as well as curve for the runtime of (B) (different color).
    """
    for p in range(17, maxp):
        n = pow(2, p)
        timeQuicksort = 0
        timeHashtable = 0
        for i in range(3):
            l = createRandomList(n, 10000)
            l1 = l[:]
            # quicksort
            start = time.time()
            quicksort(l, 0, len(l) - 1)
            stop = time.time()
            timeQuicksort += stop - start
            # hash table
            data = {}
            start = time.time()
            for i in range(len(l1) - 1):
                data[str(l1[i])] = i
            stop = time.time()
            data = {}
            timeHashtable += stop - start
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
    meanTimeQuicksort = 0
    meanTimeHashtable = 0
    for i in range(3):
        l = createRandomList(pow(2, 20), 10000)
        l1 = l[:]
        # quicksort
        start = time.time()
        quicksort(l, 0, len(l) - 1)
        stop = time.time()
        meanTimeQuicksort += stop - start
        # hash table
        data = {}
        start = time.time()
        for i in range(len(l1) - 1):
            data[str(l1[i])] = 1
        stop = time.time()
        data = {}
        meanTimeHashtable += stop - start
    # print(meanTimeQuicksort, meanTimeHashtable)
    maxp = 30
    gen = calvAvgRuntimeAndPlot(maxp)
    print("n" + "\t" + "tQuick" + "\t" + "tHeap")
    for i in range(maxp - 1):
        n, tQuick, tHash = next(gen)
        print(str(n) + "\t" + str(tQuick) + "\t" + str(tHash))

# EOF
