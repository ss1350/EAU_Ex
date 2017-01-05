#!/usr/bin/python3

# import argparse
import numpy as np
import math
import random
import argparse
import time

class DynamicIntArray:
    """Dynamic integer array class implemented with fixed-size numpy array."""

    
    def __init__(self):
        """Create empty array with length 0 and capacity 1."""
        self._n = 0  # Number of elements in array
        self._c = 1  # Capacity
        self._a = self._create_array(self._c)
        
        
    def setarray(self, n, c, a):
        """Create empty array with length 0 and capacity 1."""
        self._n = n  # Number of elements in array
        self._c = c  # Capacity
        self._a = a

    
    def __len__(self):
        """Return number of elements in the array."""
        return self._n

    
    def __getitem__(self, i):
        """Return element at index i."""
        # Check for index out of bounds error.
        if not 0 <= i < self._n:
            raise IndexError('index out of bounds')
        return self._a[i]
    
    def getarrayid(self):
        return id(self._a)

    
    def append(self, value):
        """Add integer value to end of array."""
        # Check if given value is of integer type.
        if not isinstance(value, int):
            raise TypeError('value is not integer')
        if self._n == self._c:  # time to resize
            self._resize(2 * self._c)
        self._a[self._n] = value
        self._n += 1
        
    
    def remove(self):
        """Remove integer value from end of array."""
        if self._n <= 0:
            return -1
        if self._n <= math.floor(1 / 3 * self._c): # time to resize
            self._resize(math.floor(2 * self._n))
        self._n -= 1
#         self._a = np.delete(self._a, self._n) # -> creates new array! (reallocation)
        self._a[self._n] = 0

        

    
    def _resize(self, new_c):
        """Resize array to capacity new_c."""
        b = self._create_array(new_c)
        for i in range(self._n):
            b[i] = self._a[i]
        # Assign old array reference to new array.
        self._a = b
        self._c = new_c

    
    def _create_array(self, new_c):
        """Return new array with capacity new_c."""
        return np.empty(new_c, dtype=int)  # data type = integer


def test1():
    """empty array, 10M append operations"""
    t1 = DynamicIntArray()
    start = time.time()
    for i in range(100000):
        t1.append(random.randint(0, 10000))
        print(i, "\t", time.time() - start)
        
def test2():
    """array containing 10M elements, 10M remove operations"""
    t2 = DynamicIntArray()
    for i in range(10000000):
        t2.append(random.randint(0, 1000000))
    start = time.time()
    for i in range(10000000):
        t2.remove()
        print(i, "\t", time.time() - start)
        
        
def test3():
    """array containing 1M elements, 10M operations, first append, then remove after reallocation and so on
    reallocation: look for id of object!
    Modes: 1 = append, -1 = remove"""
    t3 = DynamicIntArray()
    for i in range(1000000):
        t3.append(random.randint(0, 1000000))
    start = time.time()
    tempid = t3.getarrayid()
    mode = 1
    i = 0
    while i < 10000000:
        while (tempid == t3.getarrayid() and mode == 1):
            t3.append(random.randint(0, 1000000))
            i += 1
            print(i, "\t", time.time() - start)
            if i == 10000000:
                break
        mode = -1
        tempid = t3.getarrayid()
        while tempid == t3.getarrayid() and mode == -1:
            if t3.remove() == -1:
                mode = 1
                print(i, "\t", time.time() - start)
                i += 1
                break
            print(i, "\t", time.time() - start)
            i += 1
            if i == 10000000:
                break
        mode = 1 
    tempid = t3.getarrayid()
    
    

def test4():
    """array containing 1M elements, 10M operations, first remove, then append after reallocation and so on
    reallocation: look for id of object!"""
    t4 = DynamicIntArray()
    for i in range(1000000):
        t4.append(random.randint(0, 1000000))
    start = time.time()
    tempid = t4.getarrayid()
    mode = -1
    i = 0
    while i < 10000000:
        while (tempid == t4.getarrayid() and mode == 1):
            t4.append(random.randint(0, 1000000))
            i += 1
            print(i, "\t", time.time() - start)
            if i == 10000000:
                break
        mode = -1
        tempid = t4.getarrayid()
        while tempid == t4.getarrayid() and mode == -1:
            if t4.remove() == -1:
                mode = 1
                i += 1
                print(i, "\t", time.time() - start)
                break
            i += 1
            print(i, "\t", time.time() - start)
            if i == 10000000:
                break
        mode = 1 
        tempid = t4.getarrayid()
    
    

if __name__ == "__main__":
    random.seed()    
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument("--test1", help="execute test function 1", action="store_true")
    parser.add_argument("--test2", help="execute test function 2", action="store_true")
    parser.add_argument("--test3", help="execute test function 3", action="store_true")
    parser.add_argument("--test4", help="execute test function 4", action="store_true")
    args = parser.parse_args()
    if args.test1:
        test1()
    if args.test2:
        test2()
    if args.test3:
        test3()
    if args.test4:
        test4()
    a1 = DynamicIntArray()
    a1.append(5)
    a1.append(10)  # remove(), tests, 