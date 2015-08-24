#-------------------------------------------------------------------------------
# Name:        102_Ecological_Bin_Packing.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/102.html
# Usage:       python 102_Ecological_Bin_Packing.py
# Author:      Di Zhuang
# Created:     08/08/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

"""
Brute force
Generate a permutation and compute the savings

If savings (sum of bottles that do not move) is maximal,
then the cost of moving the bottles is minimal.
"""

from itertools import permutations
import numpy as np

class BinPacking(object):
    def __init__(self, config, colors):
        self.config = config
        self.colors = colors
        self.costs = dict()

    def findMinCost(self, DEBUG=False):
        total = np.sum(self.config)

        costs = dict()

        for perm in permutations(self.colors):
            arrangement = ''.join(perm)
            saving = 0
            for i, color in enumerate(self.colors):
                bottle = arrangement.index(color)
                saving += self.config[bottle][i]
            costs[arrangement] = total - saving

        self.costs = sorted(costs.items(), key=lambda x: (x[1],x[0]))

        if DEBUG:
            print "costs for all arrangements for"
            print "%r" % self.config
            print '*' * 80

            for cfg, cost in self.costs:
                print "config = '%s', cost = %d" % (cfg, cost)
            print '*' * 80

        return self.costs[0]

    def result(self):
        for key, val in sorted(self.costs.items(), key=lambda x: (x[1],x[0])):
            print "config = '%s', cost = %d" % (key, val)

def test(filename, colors="BGC"):
    num_colors = len(colors)
    with open(filename, 'r') as f:
        result = []
        for i, line in enumerate(f):
            config = map(int, line.strip().split(" "))
            if len(config) == num_colors * num_colors:
                glass_matrix = np.array(config).reshape((num_colors, num_colors))
                result.append(BinPacking(glass_matrix, colors).findMinCost(DEBUG=False))
            else:
                print "Missing arguments (got {:d}," \
                      " expected {:d}): line {:d}: '{:s}'"\
                    .format(len(config), num_colors*num_colors, i, line.strip())

    for (config, cost) in result:
        print config, cost

if __name__ == "__main__":
    test('102_input.txt', colors="BGC")