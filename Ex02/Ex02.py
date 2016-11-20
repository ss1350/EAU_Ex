#!/usr/bin/python3
# <<< Start of code

import math
import unittest


def heap_sort(array):
"""Sort a list of objects using the heap sort algorithm.
	uses repair_heap and heapify
"""
    # Check given parameter data type.
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise TypeError('empty list')

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

"""
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise TypeError('empty list')
    if index < 0:
        raise TypeError('index negative')
    if index > len(array) - 1:
        raise TypeError('index out of bound')        
    #Wurzel entfernen, mit letztem Wert austauschen
    array[0], array[index] = array[index], array[0]
    #index verringern
    index -= 1            
    return array
    
def heapify (array, index):
"""check for heap condition and sift until met

"""
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise TypeError('empty list')
    if index < 0:
        raise TypeError('index negative')
    if index > len(array) - 1:
        raise TypeError('index out of bound') 
    #muss maximal so oft durchgeführt werden wie es Ebenen gibt
    depth = int(math.ceil(math.log2(len(array) + 1 - (len(array) - index - 1))))
    d = 0
    while d <= depth:  
        #print("Durchlauf tiefe")     
        for i in range((len(array) - 1) // 2):
            #Kinder überprüfen, Elemente hinter Index nicht tauschen
            if (array[i] < array[2 * i + 1]) & (2 * i + 1 < index):
                array[i],array[2 * i + 1] = array[2 * i + 1],array[i]
            if (array[i] < array[2 * i + 2]) & (2 * i + 1 < index):
                array[i],array[2 * i + 2] = array[2 * i + 2],array[i]  
        d += 1
    return array


if __name__ == "__main__":
    # Create an unsorted list of integers.
    numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9]
    #numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5, 6]  #volle untere ebene
    #numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5]  #1 weniger als volle untere ebene
    #numbers = [-10, 4, 1, 0, -2, 3, 11, 3, 9, -55, -5, 297, 1, 2, 55] #negative Elemente
    #numbers = []   #leere liste
    #numbers = [1]  #nur ein Element
    # Sort the list.
    print(heap_sort(numbers))
    

"""Test Cases

"""
>>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5, 6]) #untere Ebene voll
[1,1,2,2,3,3,3,4,5,5,6,9,10,11,45]


>>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5])  #1 weniger als volle untere ebene voll
[1,1,2,2,3,3,3,4,5,5,9,10,11,45]


>>> heap_sort([-10, 4, 1, -5, 11]) #negative Elemente
[-10,-5,1,4,11]


>>> heap_sort(1)    #keine Liste
		  Traceback (most recent call last):
		  ...
TypeError: must be a list

>>> heap_sort([])   #leere Liste
		  Traceback (most recent call last):
		  ...
TypeError: empty list

>>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5, 6]) #untere Ebene voll
[1,1,2,2,3,3,3,4,5,5,6,9,10,11,45]

>>> heap_sort([10, 4, 1, 5, 2, 3, 11, 3, 9, 1, 2, 3, 45, 5])  #1 weniger als volle untere ebene voll
[1,1,2,2,3,3,3,4,5,5,9,10,11,45]

>>> heap_sort([-10, 4, 1, -5, 11]) #negative Elemente
[-10,-5,1,4,11]


>>> heapify([], 0)
		  Traceback (most recent call last):
		  ...
TypeError: empty list
>>> heapify(4, 1)
		  Traceback (most recent call last):
		  ...
TypeError: must be a list
>>> heapify([2,5,1], -1)
		  Traceback (most recent call last):
		  ...
TypeError: index negatve
>>> heapify([2,5,1], 3)
		  Traceback (most recent call last):
		  ...
TypeError: index out of bound

>>> heapify([2,5,1], 2) 
[5,2,1]

repair_heap([], 0):
		  Traceback (most recent call last):
		  ...
TypeError: empty list
repair_heap(4, 0):
		  Traceback (most recent call last):
		  ...
TypeError: must be a list
repair_heap([2,5,1], -1):
		  Traceback (most recent call last):
		  ...
TypeError: index negatve
repair_heap([2,5,1], 3):
		  Traceback (most recent call last):
		  ...
TypeError: index out of bound
# <<< End of code
