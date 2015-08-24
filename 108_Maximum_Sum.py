#-------------------------------------------------------------------------------
# Name:        108_Maximum_Sum.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/108.html
# Usage:       python 108_Maximum_Sum.py
# Author:      Di Zhuang
# Created:     8/23/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import numpy as np

class MaxSumSubarray(object):
    """
    Find a rectangular region in an array with the maximal sum.

    For example, for array

                 0  -2  -7   0
                 9   2  -6   2
                -4   1  -4   1
                -1   8   0  -2

    Maximal sum subarray is [9 2; -4 1; -1 8] with sum 15.

    """

    def __init__(self):
        pass

    def kadane2D(self, array):

        # Modify the array's elements to now hold the sum
        # of all the numbers that are above that element in its column

        N = array.shape[0]
        tmp = np.copy(array)

        for i in xrange(1, N):
            for j in xrange(N):
                tmp[i][j] += tmp[i-1][j]

        max_subsum = -np.inf  # Holds the maximum sum matrix found till now
        max_top = 0
        max_down = 0
        max_left = 0
        max_right = 0

        for top in xrange(N):
            for bottom in xrange(top, N):
                # loop over all the N^2 sub problems
                if top == 0:
                    sums = tmp[bottom] # ensures no empty subarrays
                else:
                    sums = tmp[bottom] - tmp[top-1]

                # O(n) time to run 1D kadane's on this sums array
                val, start_col, end_col = self.kadane1D(sums)

                if max_subsum < val:
                    max_subsum = val
                    max_top = top
                    max_down = bottom
                    max_left = start_col
                    max_right = end_col

        return max_subsum, max_top, max_down, max_left, max_right

    @staticmethod
    def kadane1D(A):
        max_ending_here = max_so_far = A[0]
        max_start_index = 0
        max_end_index = 0
        startIndex = 0

        for i in xrange(1, len(A)):
            if A[i] > max_ending_here + A[i]:
                startIndex = i
                max_ending_here = A[i]
            else:
                max_ending_here += A[i]

            if max_so_far < max_ending_here:
                max_so_far = max_ending_here
                max_start_index = startIndex
                max_end_index = i

        return max_so_far, max_start_index, max_end_index

def test(filename):
    with open(filename, 'r') as f:
        text = f.read()

    buffer = text.split()

    x = MaxSumSubarray()
    while len(buffer):
        dim = int(buffer.pop(0))
        A = [int(buffer.pop(0)) for _ in xrange(dim*dim)]
        A = np.array(A, dtype=np.int).reshape((dim, dim))
        val, up, down, left, right = x.kadane2D(A)
        print "sum = %d" % val
        print "subarray with maximal sum is:"
        print "-" * 60
        print A[up:down+1, left:right+1]
        print "*" * 60

if __name__ == "__main__":
    test('108_input.txt')