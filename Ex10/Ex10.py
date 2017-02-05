#!/usr/bin/python3

import timeit
import random

"""Plotted with gnuplot,
    set logscale x 10
    plot for [col=2:4:2] 'plotpoints.txt' using 1:col with lines title
    columnheader
    plot for [col=3:5:2] 'plotpoints.txt' using 1:col with lines title
    columnheader
"""


class BinarySearchTree:
    """combined data structures: linked list and binary tree
    >>> tree = BinarySearchTree()
    >>> tree.to_string()
    'null'
    >>> tree.getDepth()
    0
    >>> tree.insert("a")
    Traceback (most recent call last):
        ...
    TypeError: Not of node type
    >>> tree.insert(node(4, "a"))
    >>> tree.getDepth()
    0
    >>> tree.insert(node(3, "b"))
    >>> tree.getDepth()
    1
    >>> tree.insert(node(5, "c"))
    >>> tree.lookup(5).getValue()
    'c'
    >>> tree.insert(node(3, "x"))
    >>> tree.lookup(3).getValue()
    'x'
    >>> tree.to_string()
    '[(4, "a"), left: [(3, "x"), left: null, right: null], right: [(5, "c"), left: null, right: null]]'
    """

    def __init__(self):
        """Constructor:
        """
        self.itemCount = 0
        self.root = None
        self.head = node()
        self.last = self.head
        self.depth = 0

    def insert(self, n):
        """insert a node into data structure
        check if key already in data, if yes: return
        go through binary tree, find correct place for the node
        go left if key of node < key of current position
        go right if key of node >= key of current position
        """
        if type(n).__name__ is not "node":
            raise TypeError('Not of node type')
        if self.root is None:
            self.root = n
            self.head.nxt = n
            self.head.pre = n
            n.pre = self.head
            n.nxt = self.head
            return
        tmp = self.lookup(n.getKey())
        if (tmp is not None):
            # key already in, change value
            tmp.setValue(n.getValue())
            return
        cur = self.root
        level = 0
        while(cur is not None):
            if n.key < cur.key:
                if cur.childL is None:
                    n.nxt = cur
                    n.pre = cur.pre
                    cur.pre.nxt = n
                    cur.pre = n
                    cur.childL = n
                    n.parent = cur
                    level += 1
                    # increment depth if creating a new layer
                    if cur.childR is None and level > self.depth:
                        self.depth = level
                    break
                level += 1
                cur = cur.childL
            if n.key >= cur.key:
                if cur.childR is None:
                    n.nxt = cur.nxt
                    n.pre = cur
                    cur.nxt.pre = n
                    cur.nxt = n
                    cur.childR = n
                    n.parent = cur
                    level += 1
                    # increment depth if creating a new layer
                    if cur.childL is None and level > self.depth:
                        self.depth = level
                    break
                level += 1
                cur = cur.childR
        self.itemCount += 1

    def lookup(self, key):
        """look for a specific key in the data structure
        returns true if already in, false if not in
        start at head + 1 and then cycle through linked list using .next
        """
        key = str(key)
        cur = self.head.nxt
        while cur.getKey() != key:
            cur = cur.nxt
            # check if cycled through whole list
            if cur is self.head:
                return None
        return cur

    def to_string(self):
        """outputs a string representation of the binary tree
        """
        return self.recursiveWrite(self.root)

    def recursiveWrite(self, cur):
        """recursively enters every branch
        """
        if cur is not None:
            s = "[(" + cur.getKey() + ", " + '"' + cur.getValue() + '"), '
            s += "left: " + str(self.recursiveWrite(cur.childL))
            s += ", right: " + str(self.recursiveWrite(cur.childR)) + "]"
        else:
            s = "null"
        return s

    def getDepth(self):
        """outputs the maximum depth of the binary tree
        """
        return self.depth

    def getItemCount(self):
        """outputs number of elements
        """
        return self.itemCount

# --------- gives recursion depth errors! not suited for n > 2^11 --------
#     def getDepth(self):
#         """measures depth of the tree
#         """
#         count = self.recursiveDepth(self.root, 0, "0")
#         return count
#
#     def recursiveDepth(self, cur, counter, maxcounter):
#         """recursively enters every node
#         """
#         if cur.childL is not None:
#             counter += 1
#             if counter > int(maxcounter):
#                 maxcounter = str(counter)
#             tmp = self.recursiveDepth(cur.childL, counter, maxcounter)
#             if int(tmp) > int(maxcounter):
#                 maxcounter = int(tmp)
#         if cur.childR is not None:
#             counter += 1
#             if counter > int(maxcounter):
#                 maxcounter = str(counter)
#             tmp = self.recursiveDepth(cur.childR, counter, maxcounter)
#             if int(tmp) > int(maxcounter):
#                 maxcounter = int(tmp)
#         return maxcounter


class node:
    """each element consists of a key (int) and a value (str)
    >>> n = node(4, "a")
    >>> n.getKey()
    '4'
    >>> n.getValue()
    'a'
    >>> n.setValue("c")
    >>> n.getValue()
    'c'
    """
    def __init__(self, key=None, value=None, pre=None, nxt=None):
        """Constructor with default values None
        """
        self.pre = pre
        self.nxt = nxt
        self.key = key
        self.value = value
        self.parent = None
        self.childL = None
        self.childR = None

    def getKey(self):
        return str(self.key)

    def getValue(self):
        return str(self.value)

    def setValue(self, s):
        self.value = s


def insIntoEmpty(tree, ndLst):
    """insert sorted nodes into empty tree
    """
    for i in range(len(ndLst)):
        tree.insert(ndLst[i])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
#     tree = BinarySearchTree()
#     tree.insert(node(1, "a"))
#     print(tree.getDepth())
#     tree.insert(node(2, "b"))
#     print(tree.getDepth())
#     tree.insert(node(3, "c"))
#     print(tree.getDepth())
#     tree.insert(node(4, "a"))
#     print(tree.getDepth())
#     print(tree.to_string())
#     print(tree.to_string(), print(tree.getDepth()))
#     lst = []
#     for i in range(100):
#         lst.append(node(i, "c"))
#     random.shuffle(lst)
#     for i in range(100):
#         tree.insert(lst[i])
#     print(tree.to_string(), tree.getDepth())
#     cur = tree.head.nxt
#     for i in range(100):
#         print(cur.getKey())
#         cur = cur.nxt
    # Measure Time and depth (Ex 2)
    srtLst = []
    unsLst = []
    # create Lists: sorted and unsorted
    print("Nodes" + '\t' + "timeSorted" + '\t' + "depthSorted" + '\t' +
          "timeUnSorted" + '\t' + "depthUnsorted")
    for n in range(10, 20, 1):
        for i in range(pow(2, n)):
            srtLst.append(node(i, "x"))
            unsLst.append(node(i, "x"))
        random.shuffle(unsLst)
        sortedTree = BinarySearchTree()
        unsortedTree = BinarySearchTree()
        timeSorted = timeit.timeit(stmt=lambda: insIntoEmpty(sortedTree,
                                                             srtLst),
                                   setup="from __main__ import insIntoEmpty",
                                   number=1)
        timeUnSorted = timeit.timeit(stmt=lambda: insIntoEmpty(unsortedTree,
                                                               unsLst),
                                     setup="from __main__ import insIntoEmpty",
                                     number=1)
        depthSorted = sortedTree.getDepth()
        depthUnsorted = unsortedTree.getDepth()
        print(str(sortedTree.getItemCount()) + '\t' + str(timeSorted) + '\t' +
              str(depthSorted) + '\t' + str(timeUnSorted) + '\t' +
              str(depthUnsorted))
        unsortedTree = []
        sortedTree = []
        srtLst = []
        unsLst = []

# EOF
