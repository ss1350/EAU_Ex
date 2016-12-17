#!/usr/bin/python3
import doctest
import math

class PriorityQueueItem:
    """ Provides a handle for a queue item.
    A simple class implementing a key-value pair, 
    where the key is an integer, and the value can 
    be an arbitrary object. Index is the heap array 
    index of the item.
    """
    def __init__(self, key, value, index):
        self._key = key
        self._value = value
        self._index = index
    
    def __lt__(self, other):
        """ Enables us to compare two items with a < b.
        The __lt__ method defines the behavior of the 
        < (less than) operator when applied to two 
        objects of this class. When using the code a < b,
        a.__lt__(b) gets evaluated.
        There are many other such special methods in Python.
        See "python operator overloading" for more details.
        """
        return self._key < other._key

    def get_heap_index(self):
        """ Return heap index of item."""
        return self._index

    def set_heap_index(self, index):
        """ Update heap index of item."""
        self._index = index

    def get_key(self):
        return self._key


    def get_value(self):
        return self._value


    def get_index(self):
        return self._index


    def set_key(self, key):
        self._key = key


    def set_value(self, value):
        self._value = value


    def set_index(self, index):
        self._index = index


class PriorityQueueMinHeap:
    """Priority queue implemented as min heap."""

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._list = []


    def get_key_in_index(self, index):
        return self._list[index].get_key()


    def _repair_heap_up(self, index):
        """reinstall heapcriteria upwards
        start at index in _list, check if uppermost element, then exit
        sift upwards (check parent)
        when done sifting upwards (no change needed), check downwards!
        finished when checked downwards
        >>> tQueue._list = []
        >>> tQueue._list.append(tItem1)
        >>> tQueue._list.append(tItem4)
        >>> tQueue._list.append(tItem5)
        >>> tQueue._list.append(tItem2)
        >>> tQueue._list.append(tItem3)        
        >>> tQueue._list[1].get_key()
        4
        >>> tQueue._repair_heap_up(4)
        >>> tQueue._list[1].get_key()
        2
        """
        if (math.floor((index - 1) / 2) < 0):
            return
        parent = math.floor((index - 1) / 2)
        child = index
        while self._list[child] < self._list[parent]:
            self._swap_items(child, parent)
            if (math.floor((parent - 1) / 2)) >= 0:
                child = parent
                parent = math.floor((parent - 1) / 2)
        self._repair_heap_down(child)


    def _repair_heap_down(self, index):
        """reinstall heapcriteria upwards
        start at index in _list, check if lowest element, then exit
        sift downwards (check children)
        finished when checked downwards
        >>> tQueue._list = []
        >>> tQueue._list.append(tItem5)
        >>> tQueue._list.append(tItem4)
        >>> tQueue._list.append(tItem3)
        >>> tQueue._list.append(tItem2)
        >>> tQueue._list.append(tItem1)        
        >>> tQueue._list[0].get_key()
        5
        >>> tQueue._repair_heap_up(4)
        >>> tQueue._list[0].get_key()
        1
        """
        if  2 * index + 1 > self.size() - 1:
            return
        parent = index
        while  2 * parent + 2 <= self.size() - 1:
            child_l = 2 * parent + 1
            child_r = 2 * parent + 2
            if self._list[child_l] < self._list[parent]:
                self._swap_items(parent, child_l)
                if self._list[child_r] < self._list[parent]:
                    self._swap_items(parent, child_r)
                    parent = child_r
                    break
                parent = child_l
            elif self._list[child_r] < self._list[parent]:
                self._swap_items(parent, child_r)
                parent = child_r
            else:
                break
        if 2 * parent + 1 <= self.size() - 1:
            child_l = 2 * parent + 1
            if self._list[child_l] < self._list[parent]:
                self._swap_items(parent, child_l)
                parent = child_l


    def _swap_items(self, i, j):
        """swap two given items in list, also swap their index (which means that the index stays the same!)
        >>> tQueue1._list = []
        >>> object1 = tQueue1.insert(1, "A")
        >>> object2 = tQueue1.insert(2, "B")
        >>> tQueue1._swap_items(0, 1)
        >>> tQueue1._list[0].get_key()
        2
        >>> tQueue1._list[1].get_key()
        1
        >>> tQueue1._list[0].get_value()
        'B'
        >>> tQueue1._list[1].get_value()
        'A'
        >>> tQueue1._list[0].get_index()
        0
        >>> tQueue1._list[1].get_index()
        1
        """
        temp = self._list[j].get_index()
        self._list[j].set_index(self._list[i].get_index())
        self._list[i].set_index(temp)
        self._list[i], self._list[j] = self._list[j], self._list[i]


    def size(self):
        """return size of _list
        >>> tQueue3._list = []
        >>> tQueue3._list.insert(1, "A")
        >>> tQueue3.size()
        1
        """
        return len(self._list)


    def insert(self, key, value):
        """insert(self, key, value) -> return inserted item object
        therefore: generate new itemhandle, append to end of _list, repair heap condition
        >>> tQueue2._list = []
        >>> object = tQueue2.insert(3, "D")
        >>> object.get_key()
        3
        >>> object.get_value()
        'D'
        >>> object.get_index()
        0
        >>> object2 = tQueue2.insert(4, "C")
        >>> object2.get_key()
        4
        >>> object2.get_value()
        'C'
        >>> object2.get_index()
        1
        """
        itemhandle = PriorityQueueItem(key, value, self.size())
        self._list.append(itemhandle)
        self._repair_heap_up(self.size() - 1)
        return itemhandle


    def change_key(self, item, new_key):
        """change the key of the item, reorder the whole thing
        only one item has been changed, that's why up and then down is enough!
        >>> tQueue4._list = []
        >>> object1 = tQueue4.insert(1, "A")
        >>> object2 = tQueue4.insert(2, "B")
        >>> object3 = tQueue4.insert(3, "C")
        >>> object4 = tQueue4.insert(4, "D")
        >>> object5 = tQueue4.insert(5, "E")
        >>> object6 = tQueue4.insert(6, "F")
        >>> object7 = tQueue4.insert(7, "G")
        >>> object5.get_key()
        5
        >>> tQueue4.change_key(object5, 0)
        >>> object5.get_key()
        0
        """
        item.set_key(new_key)
        self._repair_heap_up(item.get_index())


    def get_min(self):
        """
        return item._key and item._value
        >>> tQueue5._list = []
        >>> object1 = tQueue5.insert(40, "A")
        >>> object2 = tQueue5.insert(50, "B")
        >>> object3 = tQueue5.insert(20, "C")
        >>> object4 = tQueue5.insert(90, "D")
        >>> tQueue5.get_min()
        (20, 'C')
        """
        if self.size() > 0:
            # return str(self._list[0].get_key()) + " " + str(self._list[0].get_value())
            return self._list[0].get_key(), self._list[0].get_value()
        else:
            return None


    def delete_min(self):
        """-> return item._key and item._value
        >>> tQueue6._list = []
        >>> object1 = tQueue6.insert(40, "A")
        >>> tQueue6.get_min()
        (40, 'A')
        >>> object2 = tQueue6.insert(50, "B")
        >>> tQueue6.get_min()
        (40, 'A')
        >>> object3 = tQueue6.insert(20, "C")
        >>> tQueue6.get_min()
        (20, 'C')
        >>> object4 = tQueue6.insert(90, "D")
        >>> tQueue6.get_min()
        (20, 'C')
        >>> tQueue6.size()
        4
        >>> tQueue6.delete_min()
        >>> tQueue6.size()
        3
        >>> tQueue6._list[0].get_key()
        40
        """
        self._swap_items(0, self.size() - 1)
        self._list.pop()
        self._repair_heap_down(0)


if __name__ == "__main__":
    doctest.testmod(extraglobs={'tQueue': PriorityQueueMinHeap(), 'tQueue1': PriorityQueueMinHeap(),
                                'tQueue2': PriorityQueueMinHeap(), 'tQueue3': PriorityQueueMinHeap(),
                                'tQueue4': PriorityQueueMinHeap(), 'tQueue5': PriorityQueueMinHeap(),
                                'tQueue6': PriorityQueueMinHeap(),
                                'tItem1': PriorityQueueItem(1, "A", 10), 'tItem2': PriorityQueueItem(2, "B", 11),
                                'tItem3': PriorityQueueItem(3, "C", 12), 'tItem4': PriorityQueueItem(4, "D", 13),
                                'tItem5': PriorityQueueItem(5, "E", 14)})
    # Create priority queue object.
    pq1 = PriorityQueueMinHeap()
    # Insert some flights into queue.
    pq1_item3 = pq1.insert(666,"Flight 666")
    pq1_item2 = pq1.insert(45,"Bermuda Triangle Blues (Flight 45)")
    pq1_item1 = pq1.insert(1, "Airforce One")
    # ....
    for i in range(pq1.size()):
        print(pq1.get_key_in_index(i))
