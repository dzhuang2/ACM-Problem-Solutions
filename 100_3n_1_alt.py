#-------------------------------------------------------------------------------
# Name:        100_3n_1_alt.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=36
#              count the number of times memoization saves
# Usage:       python 100_3n_1_alt.py
# Author:      Di Zhuang
# Created:     07/30/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

import time
import numpy as np

def timeit(func):
    def decorator(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        #print 'start(clock): %0.6f secs' % start
        #print 'end: %0.6f secs' % end
        print '%s took %0.6f secs' % (func.__name__, end - start)

    return decorator

class max_cycle(object):
    def __init__(self, arrlen=1000000):
        self.__arr = np.zeros(arrlen, dtype=np.int32)
        self.__arr[1] = 1
        self.__lenarr = arrlen
        self.__count = np.zeros(arrlen, dtype=np.int32) # count the number of calls saved via memoization

    def count(self):
        return sum(self.__count)

    def cycle(self, n, opt=True):
        if n < self.__lenarr:
            if self.__arr[n] == 0:
                self.__arr[n] = self.func(n, opt)
            else:
                self.__count[n] += 1
            return self.__arr[n]
        else:
            return self.func(n, opt)

    def func(self, n, opt=True):
        if n == 1:
            return 0
        else:
            if n % 2 == 1:
                if opt:
                    if n < self.__lenarr: # otherwise, the number is not memoized
                        self.__count[n] += 1
                    return self.cycle(n + (n >> 1) + 1) + 2
                else:
                    return self.cycle(3 * n + 1) + 1
            else:
                return self.cycle(n >> 1) + 1

    def trial(self, start, end, opt=True):
        t0 = time.clock()

        max_cycle_length = 0
        for i in xrange(start, end+1):
            max_cycle_length = max(max_cycle_length, self.cycle(i, opt))

        duration = time.clock() - t0

        return max_cycle_length, self.count(), duration

def run_trials():
    print "{:^12s}\t{:>10s}\t{:>10s}\t{:>12s}\t{:s}".format("range", "max cycle", "shortcut", "saved calls", "time")
    for i in xrange(2, 7):
        for opt in [True, False]:
            mc = max_cycle()
            max_cycle_length, saved_calls, duration = mc.trial(1, 10**i, opt)
            print '{:1d} - {:>8d}\t{:>10d}\t{:>10s}\t{:>12d}\t{:>5.6f} secs'.format(
                1, 10**i, max_cycle_length, str(opt), saved_calls, duration)

if __name__ == "__main__":
    run_trials()