#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

import math
import matplotlib.pyplot as plt


def heap_sort(array):
    """Liste von Objekten mit heap sort sortieren
    zuerst heapify bis Heapcondition hergestellt
    danach erstes Entfernen, repair heap
    so lange, bis nur noch ein Element übrig

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
    """

    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')

    x_list = calc_plotvalues(array)
    heapify(array)
    heap_size = len(array)
    while (heap_size > 1):
        repair_heap(array, 0, heap_size)
        array[0], array[heap_size - 1] = array[heap_size - 1], array[0]
        heap_size -= 1
        show_plot(x_list, array)
    return array


def repair_heap(array, start_index, heap_size):
    """fängt bei index an und überprüft Kinder. Wenn Kinder größer -> tauschen
    dann weiter runter siften, bis unten angekommen
    Kontrolle mit heap_size, ob index out of bounds


    leere Liste
    >>> repair_heap([], 0, 0)
    Traceback (most recent call last):
        ...
    ValueError: empty list

    keine Liste
    >>> repair_heap(4, 0, 0)
    Traceback (most recent call last):
        ...
    TypeError: must be a list

    negatier Index
    >>> repair_heap([2, 5, 1], -1, 3)
    Traceback (most recent call last):
        ...
    ValueError: index negative

    Index ausserhalb
    >>> repair_heap([2, 5, 1], 0, 4)
    Traceback (most recent call last):
        ...
    ValueError: index out of bound
    """

    if not type(array) == list:
        raise TypeError("must be a list")
    if not len(array) > 0:
        raise ValueError("empty list")
    if start_index < 0:
        raise ValueError("index negative")
    if heap_size > len(array):
        raise ValueError("index out of bound")

    while True:
        parent = array[start_index]
        if (2 * start_index + 1 < heap_size):
            left = array[2 * start_index + 1]
            if (parent < left):
                parent, left = left, parent
                array[start_index],
                array[2 * start_index + 1] = parent, left
            if (2 * start_index + 2 < heap_size):
                right = array[2 * start_index + 2]
                if (parent < right):
                    parent, right = right, parent
                    array[start_index],
                    array[2 * start_index + 2] = parent, right
            start_index += 1
        else:
            break
    return array


def heapify(array):
    """initiale heap condition herstellen:
    repair heap von unten nach oben durchfuehren
    unterste Position: Laenge von array - unterste Ebene: 2 pow tiefe - 2


    leere Liste
    >>> heapify([])
    Traceback (most recent call last):
        ...
    ValueError: empty list

    keine Liste
    >>> heapify(4)
    Traceback (most recent call last):
        ...
    TypeError: must be a list
    """

    if not type(array) == list:
        raise TypeError('must be a list')
    if not len(array) > 0:
        raise ValueError('empty list')

    max_index = (len(array) / 2) - 1
    for i in range(math.floor(max_index), -1, -1):
        repair_heap(array, i, len(array))

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
    plt.axis([0, array_lenght, 0, max_value + 1])
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
    """main routine
    Groesster Wert ganz unten
    >>> heap_sort([5, 4, 3, 2, 10])
    [2, 3, 4, 5, 10]

    unterste Reihe mit einem Element
    >>> heap_sort([5, 4, 3, 1])
    [1, 3, 4, 5]

    unterste Reihe voll
    >>> heap_sort([5, 4, 3, 1, 44, 11, 30])
    [1, 3, 4, 5, 11, 30, 40]

    vorsortierte Liste
    >>> heap_sort([1, 2, 3, 4, 5, 6])
    [1, 2, 3, 4, 5, 6]

    andersherum sortierte Liste
    >>> heap_sort([6, 5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5, 6]

    Liste mit doppelten Elementen
    >>> heap_sort([6, 5, 6, 4, 4, 5])
    [4, 4, 5, 5, 6, 6]
    """
    import doctest
    doctest.testmod()
    numbers = [11, 55, 42, 98, 0, 5, 67, 32, 24]
    # numbers = [1, 2, 3, 4, 5]
    print("Eingabe: ", numbers)
    print("Ergebnis: ", heap_sort(numbers))

    while True:
        plt.pause(0.5)
# <<< End of code
