#-------------------------------------------------------------------------------
# Name:        107_Cat_in_Hat
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/107.html
# Usage:       python 107_Cat_in_Hat
# Author:      Di Zhuang
# Created:     8/22/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import numpy as np

class CatInHat(object):
    """
    Find solution

    The crux of the problem rely on solving the system of equations:
        c0 = (N+1) ^ k
        c1 = N ^ k

    While the solution N cannot be found analytically,
    f(N) = ln(N+1) / ln(N) is a monotonically decreasing function,
    meaning that a binary search can be done to find N in O(logN) time

    The first value is the number of internal nodes, which is
        inode = (N ^ k - 1) / (N - 1)

    The second value is the internal path length, which is
        ipl = (N + 1) ^ (k + 1) - N ^ (k + 1)
    """

    def __init__(self, *args):
        assert len(args) == 2, "Invalid input!"
        self.height, self.workers = args

    def solution(self):
        if self.workers == 1:
            # there is just 1 worker at the bottom, then the tree is linear
            # height moves up in powers of 2

            if self.height == 1: # just a single worker
                return 0, 1
            else:
                k = np.rint(np.log(self.height) / np.log(2))
                return k, 2 ** (k + 1) - 1

        ratio = np.log(self.height) / np.log(self.workers)
        N = self.binary_search(ratio, 1, self.workers)

        if N is None:
            raise ValueError, "No solution exists for [%d, %d]!" \
                              % (self.height, self.workers)

        k = np.rint(np.log(self.workers) / np.log(N))
        assert self.height == (N+1) ** k, \
            "This should not happen!"

        inodes = (self.workers - 1) / (N - 1)
        ipl = self.height * (N+1) - self.workers * N

        return inodes, ipl

    def binary_search(self, key, start, end, tol=1e-12):
        if end < start:
            return None

        mid = (start + end) / 2
        val = np.log(mid+1) / np.log(mid)
        if key > val + tol:
            return self.binary_search(key, start, mid-1)
        elif key < val - tol:
            return self.binary_search(key, mid+1, end)
        else:
            return mid

def test(filename):
    with open(filename, 'r') as f:
        while True:
            args = map(int, f.readline().strip().split())

            if args == [0, 0]:
                break

            p = CatInHat(*args)
            print "%d %d" % p.solution()

if __name__ == "__main__":
    test('107_input.txt')