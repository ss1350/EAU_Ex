# Copyright 2016 Tobias Faller

import random
import timeit


def heap_sort(lst):
    """Sorts a list in-place using the heapsort algorithm

    >>> heap_sort([5, 8, 1, 5, 6, 2, 6])
    [1, 2, 5, 5, 6, 6, 8]
    """

    # Create the initial heap condition
    heapify(lst)

    for j in range(len(lst) - 1, -1, -1):
        # Swap the max to the end
        lst[j], lst[0] = lst[0], lst[j]

        # Repair the heap
        repair_heap(lst, 0, j)

    return lst


def heapify(lst):
    """Creates an inital heap condition"""

    # Create heap, updating the heap condition from the bottom layer up.
    # We only need to start after the first half (ignore the leaves)
    size = len(lst)
    for j in range(int(size / 2 - 1), -1, -1):
        repair_heap(lst, j, size)


def repair_heap(lst, parent, size):
    """Repairs a heap downwards from the given index"""

    # We swap the elements downwards (sift) to build the heap
    # from the bottom up
    while True:
        left = parent * 2 + 1
        right = parent * 2 + 2
        maximum = parent

        # If the parent element is larger swap the parent element
        # with the child. We have to explicitly choose the child.

        if left < size - 1 and lst[maximum] < lst[left]:
            maximum = left
        if right < size - 1 and lst[maximum] < lst[right]:
            maximum = right

        if maximum != parent:
            lst[maximum], lst[parent] = lst[parent], lst[maximum]

            # Repair downwards
            parent = maximum
        else:  # Heap condition is created
            break

    return lst


def gen(size):
    """Generates a random list for testing"""

    lst = [i for i in range(size)]
    random.shuffle(lst)
    return lst


if __name__ == "__main__":
    # Plot the rumtime for 0 to 5000 elements
    with open('runtime.csv', 'w') as f:
        f.write("x;y\n")
        for m in range(0, 100):
            m = m * 50
            result = ('%d;%.6f\n' % (m, timeit.timeit('heap_sort(lst)',
                      setup='from __main__ import heap_sort, gen\nlst = gen(' +
                      str(m) + ')', number=5))).replace('.', ',')
            print(result)
            f.write(result)
