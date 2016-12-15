#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

from math import sqrt
from itertools import count, islice
import random
from random import randint

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
        if not p >= u:
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
        # print(self.a, self.b)


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


def create_keys(k, u):
    """creates random keys for the universe
    """
    for i in range(k):
        k = randint(1,u)
        yield(k)


def estimate_c_for_single_set(keys, hashfunctionobject):
    """Given a set of keys S, the method calculates the
    mean bucket size for 1000 random hash functions and 
    from this calculates the best possible value of c and returns c
    
    E( S i ) ≤ 1 + c * S/M
    """
    c = 100
    for i in range(10):
        hashfunctionobject.set_random_parameters()
        currentc = (mean_bucket_size(keys, hashfunctionobject) - 1) * hashfunctionobject.m/len(keys)
        if currentc < c:
            c = currentc
    return c   


def estimate_c_for_multiple_sets(n, k, hashfunctionobject):
    """randomly generates a given number n of key sets with a given size k 
    (no duplicates inside one set of keys!) and calculates for each of the n
    key sets the best possible c with the function estimate_c_for_single_set from exercise 2. 
    return mean, minimum and maximum c value
    receives n, k and the hash function object.
    """
    maxc = 0
    minc = 100
    avgc = 0
    for i in range(n):
        currentc = estimate_c_for_single_set(create_random_universe_subset(k, hashfunctionobject.u), hashfunctionobject)
        if currentc < minc:
            minc = currentc
        if currentc > maxc:
            maxc = currentc
        avgc += currentc
    avgc /= n
    return str('\n') + "Maximum C: " + str(maxc) + str('\n') + "Minimum C: " + str(minc) + str('\n') + "Average C: " + str(avgc)


def create_random_universe_subset(k, u):
    """random key list generation
    receives k and the universe size u from the hash function and returns the subset list.
    wrapper to cover Ex. 3. Addition: no doubles!
    """
    keys = list(set(list(create_keys(k, u))))
    while len(keys) < k:
        keys = list(keys)
        keys.append(randint(1, u))
        keys = set(keys)
    return list(keys)


def estimate_case():
    """calculates the values described in exercise 3 for U = 100, m = 100, p = 101 and 
    n = 1000 randomly chosen key sets of size k = 20. 
    Next simulate a non-universal hash function by choosing p = 10 
    and based on this again calculate the values described in exercise
    """
    u = 100
    m = 100
    p = 101
    k = 20
    n = 1000
    h2 = HashFunction(1, 0, p, u, m)
    keys = []
    string1 = "With universal hash: " + str(estimate_c_for_multiple_sets(n, k, h2)) + str('\n')
    h2.p = 10
    string2 = "With non-universal hash: " + str(estimate_c_for_multiple_sets(n, k, h2))
    return string1 + str('\n') + string2
    
    

if __name__ == "__main__":
    """Main routine
    starts random number generator for class HashFunction
    creates an instance of HashFunction
    """
    k = 15
    u = 100
    m = 15
    random.seed()
    keys = list(create_keys(k, u))
    keyswodoubles = create_random_universe_subset(k, u)
    h1 = HashFunction(1, 0, 101, u, m)
    h1.set_random_parameters()
    # print("Ideal Items per Bucket: ", k/m)
    # print("Current Items per Bucket: ", mean_bucket_size(keyswodoubles, h1))
    # print("Estimate C for current set: ", estimate_c_for_single_set(keyswodoubles, h1))
    # print("Estimate C for multiple sets: ", estimate_c_for_multiple_sets(1000, k, h1))
    print("Estimate Case: ", estimate_case())
    

    
    
    



# <<< End of code
