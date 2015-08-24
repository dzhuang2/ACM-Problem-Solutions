#-------------------------------------------------------------------------------
# Name:        100_3n_1.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=36
# Usage:       python 100_3n_1.py
# Author:      Di Zhuang
# Created:     07/30/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

import time

def timeit(func):
    def decorator():
        start = time.clock()
        func()
        end = time.clock()
        #print 'start(clock): %0.6f secs' % start
        #print 'end: %0.6f secs' % end
        print '%s took %0.6f secs' % (func.__name__, end - start)

    return decorator

def memoized(func):
    arr = [0] * 1000001
    arr[1] = 1 # count the 1 at the end as part of the cycle

    def decorator(n):
        if n < len(arr):
            if arr[n] == 0:
                arr[n] = func(n)
            return arr[n]
        else:
            return func(n)

    return decorator

@memoized
def cycle(n):
    if n == 1:
        return 0
    else:
        if n % 2 == 1:
            return cycle(n + (n >> 1) + 1) + 2
        else:
            return cycle(n >> 1) + 1

@timeit
def test():
    pairs = [(1, 10), (100, 200), (201, 210), (900, 1000)]
    for start, end in pairs:
        max_cycle_length = 0
        for i in xrange(start, end+1):
            max_cycle_length = max(max_cycle_length, cycle(i))
        print start, end, max_cycle_length

@timeit
def test2():
    pairs = [(1, 1000000)]
    for start, end in pairs:
        max_cycle_length = 0
        for i in xrange(start, end+1):
            max_cycle_length = max(max_cycle_length, cycle(i))
        print start, end, max_cycle_length

if __name__ == "__main__":
    test()
    #test2()
