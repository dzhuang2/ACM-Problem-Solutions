#-------------------------------------------------------------------------------
# Name:        106_Fermat_Pythagoras
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/106.html
# Usage:       python 106_Fermat_Pythagoras
# Author:      Di Zhuang
# Created:     8/22/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import numpy as np

def gcd(a, b):
    if a % b == 0:
        return b
    return gcd(b % a, a)

class PythagoreanTriples(object):
    """
    Find Pythagorean Triples less than N

    The formula to find all relatively prime Pythagorean Triples is as follows:
    x = (r^2 - s^2)^2
    y = (2rs)^2
    z = (r^2 + s^2)^2

    The triple (x, y, z) must be relative prime
    """

    def __init__(self, N):
        self.n = N
        self.arr = np.zeros(N+1, dtype=np.int)

    def findTriples(self):
        # in order for z to be less than N, r and s must both be smaller than this value
        limit = int(np.ceil(np.sqrt(self.n)))

        counter = 0

        triples = []
        for r in xrange(1, limit):
            for s in xrange(r):
                x, y, z = sorted([r*r - s*s, 2*r*s, r*r + s*s])
                if 1 < x and z <= self.n:
                    if gcd(x, y) == 1:
                        counter += 1

                        if DEBUG:
                            triples.append((x, y, z))

                        for i in xrange(1, self.n / z + 1):
                            self.arr[i * x] = 1
                            self.arr[i * y] = 1
                            self.arr[i * z] = 1

        if DEBUG:
            # print all relatively prime triples (8 per line)
            for i in xrange(0, len(triples), 8):
                print ", ".join([str(trip) for trip in triples[i:i+8]])

        non_triples = self.n - len(np.nonzero(self.arr)[0])

        return counter, non_triples


def test(filename):
    with open(filename, 'r') as f:
        for line in f:
            n = int(line.strip())
            pt = PythagoreanTriples(n)
            num_triples, non_components = pt.findTriples()
            print num_triples, non_components

if __name__ == "__main__":
    test('106_input.txt')