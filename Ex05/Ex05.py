#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

from math import sqrt
from itertools import count, islice
import random
from random import randint

"""pick hash function randomly from h, hash values and sort into buckets

"""

def isPrime(n):
    """check for prime number
    """
    if n < 2: return False
    for number in islice(count(2), int(sqrt(n)-1)):
        if not n%number:
            return False
    return True


class HashFunction:
    """     h (a,b) (x) = ((ax + b) mod p) mod m
    """
    def __init__(self, a, b, p, u, m):
        """a, b, p (the prime number), u (universe size), m (hash table size)
        only one hash function per hash table!
        Cond: p a prime number ≥ U and m the size of the hash table with p > m
        1 ≤ a < p, 0 ≤ b < p
        """
        if not (isPrime(p)):
            raise ValueError("p Not a prime Number!")
        if not p <= u:
            raise ValueError("p smaller than u!")
        if not p > m:
            raise ValueError("p <= m!")
        if not 1 <= a < p:
            raise ValueError("Is not 1 ≤ a < p!")
        if not 0 <= b < p:
            raise ValueError("Is not 0 ≤ b < p!")
        self.a, self.b, self.p, self.u, self.m = a, b, p, u, m
        self.table = []
        for i in range(m):
            self.table.append([])

        
    def apply(self, x):
        """apply hash function specified above to a given key value and return 
        hash table index
        """
        index = ((self.a * x + self.b) % self.p) % self.m
        self.table[index].append(x)
        # print(x, index)
        return index
    

    def set_random_parameters(self):
        """set randoms for a and b, no return
        """
        self.a = randint(1,self.p - 1)
        self.b = randint(0,self.p) 


    def get_table(self):
        """returns the hash table
        """
        return self.table

def mean_bucket_size(S, h):
    """ given set of keys S and hash function h
        returns mean number of elements that you have to look at in the bucket 
        in order to find the wanted key
        For this you only have to average over the buckets 
        with at least one key (i.e. S divided by the number of
        non-empty buckets). Why?
        
        - algorithm won't even look into the empty buckets because 
        none of the keys that are hashed point into empty buckets
    """
    buckets = []
    uniquebuckets = []
    for i in range(len(S)):
        buckets.append((h.apply(S[i])))
    uniquebuckets = set(buckets)
    return len(S)/len(uniquebuckets)
    

def create_keys(size):
    """creates random keys for the universe
    """
    for i in range(size):
        k = randint(-10000,10000)
        yield(k)


if __name__ == "__main__":
    """Main routine
    starts random number generator for class HashFunction
    creates an instance of HashFunction
    """
    universesize = 200
    hashtablesize = 100
    random.seed()
    keys = list(create_keys(universesize))
    h1 = HashFunction(1, 0, 101, universesize, hashtablesize)
    h1.set_random_parameters()
    print("Ideal Items per Bucket: ", universesize/hashtablesize)
    print("Current Items per Bucket: ", mean_bucket_size(keys, h1))
    

    
    
    



# <<< End of code