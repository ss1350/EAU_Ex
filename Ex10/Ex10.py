#!/usr/bin/python3


class BinarySearchTree:
    """combined data structures: linked list and binary tree
    >>> tree = BinarySearchTree()
    >>> tree.to_string()
    'null'
    >>> tree.insert("a")
    Traceback (most recent call last):
        ...
    TypeError: Not of node type
    >>> tree.insert(node(4, "a"))
    >>> tree.insert(node(3, "b"))
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
        if (self.lookup(n.getKey()) is not None):
            # key already in, change value
            self.lookup(n.getKey()).setValue(n.getValue())
            return
        cur = self.root
        while(cur is not None):
            if n.key < cur.key:
                if cur.childL is None:
                    n.nxt = cur
                    n.pre = cur.pre
                    cur.pre.nxt = n
                    cur.pre = n
                    cur.childL = n
                    n.parent = cur
                    break
                cur = cur.childL
            if n.key >= cur.key:
                if cur.childR is None:
                    n.nxt = cur.nxt
                    n.pre = cur
                    cur.nxt.pre = n
                    cur.nxt = n
                    cur.childR = n
                    n.parent = cur
                    break
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    tree = BinarySearchTree()
    tree.insert(node(4, "a"))
    tree.insert(node(3, "b"))
    tree.insert(node(5, "c"))
    tree.insert(node(3, "a"))
#     tree.insert(node(3, "a"))
#     tree.insert(node(5, "b"))
#     tree.insert(node(6, "c"))
#     tree.insert(node(2, "g"))
#     tree.insert(node(10, "x"))
#     tree.insert(node(0, "d"))
    print(tree.to_string())

# EOF
