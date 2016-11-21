#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

import math
import matplotlib.pyplot as plt


def heap_sort(array):
    """Liste von Objekten mit heap sort sortieren, benutzt heapify, repair_heap,
    calc_plotvalues und show_plot

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

    doppelte Elemente
    >>> heap_sort([1, 2, 3, 4, 5, 4, 3, 2, 1, 0])
    [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    """

    # Check given parameter data type.
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')
    index = len(array) - 1
    # Werte für Plot berechnen
    x_list = calc_plotvalues(array)
    # Wiederholen bis Zeiger auf 0 steht
    while index >= 0:
        # heap aufbauen
        heapify(array, index)
        # heap reparieren
        repair_heap(array, index)
        index -= 1
        show_plot(x_list, array)
    return array


def repair_heap(array, index):
    """root zu sortierten elementen, letztes unsortiertes auf root

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

    Nur 1 Element
    >>> repair_heap([5], 0)
    [5]
    """
    if not type(array) == list:
        raise TypeError("must be a list")
    if not len(array) > 0:
        raise ValueError("empty list")
    if index < 0:
        raise ValueError("index negative")
    if index > len(array) - 1:
        raise ValueError("index out of bound")
    # Wurzel entfernen, mit letztem Wert austauschen
    array[0], array[index] = array[index], array[0]
    # index verringern
    index -= 1
    return array


def heapify(array, max_index):
    """heap condition ueberpruefen und so lange siften, bis erfüllt

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

    Index auf 0, keine Aktion
    >>> heapify([2,5,1], 0)
    [2, 5, 1]

    Groesster Wert ganz unten
    >>> heapify([5, 4, 3, 10],3)
    [10, 5, 3, 4]
    """
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')
    if max_index < 0:
        raise ValueError('index negative')
    if max_index > len(array) - 1:
        raise ValueError('index out of bound')
    # muss maximal so oft durchgefuehrt werden wie es Ebenen gibt
    depth = int(math.ceil(math.log2(len(array) + 1 -
                (len(array) - max_index - 1))))
    d = 0
    while d < depth:
        for i in range(int(math.ceil((len(array) - 1) / 2))):
            # Kinder ueberpruefen, Elemente hinter Index nicht tauschen
            if ((2 * i + 1) <= max_index):
                if array[i] < array[2 * i + 1]:
                    array[i], array[2 * i + 1] = array[2 * i + 1], array[i]
            if ((2 * i + 2) <= max_index):
                if array[i] < array[2 * i + 2]:
                    array[i], array[2 * i + 2] = array[2 * i + 2], array[i]
        d += 1
    return array


def calc_plotvalues(array):
    """Werte für Plot berechnen (y-/x-Achse usw)
    leere Liste
    >>> calc_plotvalues([])
    Traceback (most recent call last):
        ...
    ValueError: empty list

    keine Liste
    >>> calc_plotvalues(4)
    Traceback (most recent call last):
        ...
    TypeError: must be a list

    Laenge = 1, nur 1 x wert auf 0 als return wert
    >>> calc_plotvalues([1])
    [0]
    """
    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')
    x_list = []
    array_lenght = len(array)
    max_value = 0
    plt.ion()
    for i in range(array_lenght):
        x_list.append(i)
        if array[i] > max_value:
            max_value = array[i]
    plt.axis([0, array_lenght, 0, max_value+1])
    return x_list


def show_plot(x_list, y_list):
    """Plot zeichnen lassen

    keine Liste
    >>> show_plot([1], 1)
    Traceback (most recent call last):
        ...
    TypeError: must be a list

    keine Liste
    >>> show_plot(1, [1])
    Traceback (most recent call last):
        ...
    TypeError: must be a list

    leere Liste
    >>> show_plot([], [0])
    Traceback (most recent call last):
        ...
    ValueError: empty list

    leere Liste
    >>> show_plot([0], [])
    Traceback (most recent call last):
        ...
    ValueError: empty list
    """
    if not type(x_list) == list:
        raise TypeError('must be a list')
    if not type(y_list) == list:
        raise TypeError('must be a list')
    if not len(x_list) > 0:
        raise ValueError('empty list')
    if not len(y_list) > 0:
        raise ValueError('empty list')
    plt.clf()
    plt.plot(x_list, y_list, 'ro')
    plt.pause(0.1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # Create an unsorted list of integers.
    # numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9]
    numbers = [10, 41, 11, 51, 21, 31, 11, 35, 90, 54, 99, 24, 68, 22]
    # Sort the list.
    print(heap_sort(numbers))

    while True:
        plt.pause(0.5)
# <<< End of code
