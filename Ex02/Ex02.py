#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

import math
import unittest
import matplotlib.pyplot as plt


def heap_sort(array):
    """Sort a list of objects using the heap sort algorithm.
	uses repair_heap and heapify
    
    keine Liste
    >>> heap_sort(1)    
    Traceback (most recent call last):
        ...
    TypeError: must be a list
    
    leere Liste
    >>> heap_sort([])   
    Traceback (most recent call last):
        ...
    ValueError: empty list
    
    untere Ebene voll
    >>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5, 6]) 
    [1, 1, 2, 2, 3, 3, 3, 4, 5, 5, 6, 9, 10, 11, 45]
    
    1 weniger als volle untere ebene voll
    >>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5])  
    [1, 1, 2, 2, 3, 3, 3, 4, 5, 5, 9, 10, 11, 45]
    
    negative Elemente
    >>> heap_sort([-10, 4, 1, -5, 11]) 
    [-10, -5, 1, 4, 11]
    """
    
    # Check given parameter data type.
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')
    index = len(array) - 1
    #Wiederholen bis Zeiger auf 0 steht
    while index >= 0:   
        #heap aufbauen
        heapify(array, index)
        #heap reparieren
        repair_heap(array, index)
        index -= 1        
    return array


def repair_heap(array, index):
    """move root of tree to sorted items, move last unsorted item to root
    
    leere Liste
    >>> repair_heap([], 0)
    Traceback (most recent call last):
        ...
    ValueError: empty list
    
    keine Liste
    >>> repair_heap(4, 0)
    Traceback (most recent call last):
        ...
    TypeError: must be a list
    
    negatier Index
    >>> repair_heap([2, 5, 1], -1)
    Traceback (most recent call last):
        ...
    ValueError: index negative
    
    Index ausserhalb
    >>> repair_heap([2, 5, 1], 3)
    Traceback (most recent call last):
        ...
    ValueError: index out of bound
    
    Index auf letztem Element
    >>> repair_heap([1,2,3,4,5,6,7,8],6)  
    [7, 2, 3, 4, 5, 6, 1, 8]
    
    Index auf erstem Element
    >>> repair_heap([1,2,3,4,5,6,7,8],0)  
    [1, 2, 3, 4, 5, 6, 7, 8]
    """
    if not type(array) == list:
        raise TypeError("must be a list")
    if not len(array) > 0:
        raise ValueError("empty list")
    if index < 0:
        raise ValueError("index negative")
    if index > len(array) - 1:
        raise ValueError("index out of bound")        
    #Wurzel entfernen, mit letztem Wert austauschen
    array[0], array[index] = array[index], array[0]
    #index verringern
    index -= 1            
    return array
    
def heapify (array, index):
    """check for heap condition and sift until met

    leere Liste
    >>> heapify([], 0)
    Traceback (most recent call last):
        ...
    ValueError: empty list
    
    keine Liste
    >>> heapify(4, 1)
    Traceback (most recent call last):
        ...
    TypeError: must be a list
    
    negativer Index
    >>> heapify([2,5,1], -1)
    Traceback (most recent call last):
        ...
    ValueError: index negative
    
    Index außerhalb d. Grenzen
    >>> heapify([2,5,1], 3)
    Traceback (most recent call last):
        ...
    ValueError: index out of bound

    Normales Heapify
    >>> heapify([2,5,1], 2) 
    [5, 2, 1]
    
    Groesster Wert ganz unten
    >>> list=heapify([50, 40, 30, 100],3)
    list[0]=100
    """
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')
    if index < 0:
        raise ValueError('index negative')
    if index > len(array) - 1:
        raise ValueError('index out of bound') 
    #muss maximal so oft durchgefuehrt werden wie es Ebenen gibt
    depth = int(math.ceil(math.log2(len(array) + 1 - (len(array) - index - 1))))
    d = 0
    size = len(array) - 1
    while d <= depth:  
        #print("Durchlauf tiefe")     
        for i in range(int(math.ceil((len(array) - 1) / 2))):
            #Kinder ueberpruefen, Elemente hinter Index nicht tauschen
            if (2 * i + 1 <= size):
                if array[i] < array[2 * i + 1]:
                    array[i],array[2 * i + 1] = array[2 * i + 1],array[i]
            if (2 * i + 2 <= size):
                if array[i] < array[2 * i + 2]:
                    array[i],array[2 * i + 2] = array[2 * i + 2],array[i]  
        d += 1
    return array


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # Create an unsorted list of integers.
    #numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9]
    numbers = [50, 40, 30, 100]
    # Sort the list.
    print(heap_sort(numbers))
# <<< End of code
