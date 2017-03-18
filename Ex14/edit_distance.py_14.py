#!/usr/bin/python3

import sys
import numpy


def compute_ed_recursively(x, y):
    """ Compute edit distance from x to y recursively.

    >>> compute_ed_recursively("", "")
    0
    >>> compute_ed_recursively("donald", "ronaldo")
    2
    """
    n = len(x)
    m = len(y)
    if n == 0:
        return m
    if m == 0:
        return n
    # Insert case.
    ed1 = compute_ed_recursively(x, y[0:-1]) + 1
    # Delete case.
    ed2 = compute_ed_recursively(x[0:-1], y) + 1
    # Replace case.
    ed3 = compute_ed_recursively(x[0:-1], y[0:-1])
    # If last characters do not match, add replace costs.
    if x[-1] != y[-1]:
        ed3 += 1
    return min(ed1, ed2, ed3)


def compute_ed_via_table(x, y):
    """ Compute edit distance via dynamic programming table.

    >>> compute_ed_recursively("", "")
    0
    >>> compute_ed_via_table("","")
    0
    >>> compute_ed_via_table("asd","")
    3
    >>> compute_ed_via_table("","asd")
    3
    >>> compute_ed_via_table("GRAU","RAUM")
    2
    
    This function should calculate the edit distance between two strings x and y in time
    using the dynamic programming table approach from the lecture.
    create a 2d array, initalize with high values
        x1 x2 x3 ...
    y1
    y2
    y3
    ...
    cycle through array
    differenciate the different cases, return a map with the correct values
    """
    # save the length of x and y
    leny = len(y)
    lenx = len(x)
    # check if one of the strings has length zero
    if lenx == 0:
        if leny == 0:
            return 0
        return leny
    if leny == 0:
        return lenx
    ed = 0
    # create the 2d array [line][row]
    # initialize with high values
    a = numpy.full((leny + 1, lenx + 1), 100)    
    # cycle through the array, line by line
    for yaddr in range(leny + 1):
        for xaddr in range(lenx + 1):
            # starting in first line: yaddr = 0, just increment every slot
            if yaddr == 0:
                a[0][xaddr] = xaddr
                continue
            # first row: just del!
            if xaddr == 0:
                a[yaddr][0] = yaddr 
                continue
            # special case: first REPL is always possible and gives 1
            if xaddr == 1 and yaddr == 1:
                a[1][1] = 1
                continue
            # INS: increment last element
            temp = a[yaddr][xaddr - 1] + 1
            if temp < a[yaddr][xaddr]:
                a[yaddr][xaddr] = temp  
            # REPL: both values are equal! Repl. Operation w/o cost
            if x[xaddr - 1] == y[yaddr - 1]:
                temp = a[yaddr - 1][xaddr - 1]
            # REPL: values are different! Repl Operation w cost
            else:
                temp = a[yaddr - 1][xaddr - 1] + 1 
            if temp < a[yaddr][xaddr]:
                a[yaddr][xaddr] = temp
            # DEL: inkrement upper one
            temp = a[yaddr - 1][xaddr] + 1
            if temp < a[yaddr][xaddr]:
                a[yaddr][xaddr] = temp
    return a[leny][lenx]


if __name__ == "__main__":
    # Read in two strings from command line.
    nr_args = len(sys.argv)
    if not nr_args == 3:
        raise Exception("script excepts two input strings")
    x = sys.argv[1]
    y = sys.argv[2]
    print("x = %s" % (x))
    print("y = %s" % (y))
    # ed = compute_ed_recursively(x, y)
    ed = compute_ed_via_table(x, y)
    print("Edit distance (x -> y): %i" % (ed))
