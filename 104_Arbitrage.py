#-------------------------------------------------------------------------------
# Name:        104_Arbitrage.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/104.html
# Usage:       python 103_Arbitrage.py
# Author:      Di Zhuang
# Created:     08/08/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import numpy as np

class ExchangeTable(object):
    """
    Apply a modified Floyd-Warshall Algorithm to find arbitrage
    """

    NULL = -1

    def __init__(self, exchange_rates):
        self.table = np.array(exchange_rates)

    def findArbitrage(self, threshold=0.01):
        """
        find the shortest number of exchanges that result in an arbitrage and
        print out the sequence that accomplishes this task
        :param threshold: profit margin to exceed to be considered to be an arbitrage
        """
        profit, seq = self.floyd_warshall(threshold)
        if profit == self.NULL:
            print "no arbitrage sequence exist"
        else:
            print "profit = %f, length = %d, sequence = %s" % \
                  (profit, len(seq) - 1, " ".join([str(i+1) for i in seq]))

    def floyd_warshall(self, threshold):
        """
        run a modified floyd_warshall algorithm to find the shortest number of exchanges
        that will yield an arbitrage.
        """
        n = self.table.shape[0]
        profit = np.empty(shape=(n, n), dtype=np.float)
        dist = np.empty(shape=(n, n), dtype=np.int)
        next = np.empty(shape=(n, n), dtype=np.int)

        # fill in the initial values for 0 length paths
        for i in xrange(n):
            for j in xrange(n):
                profit[i][j] = self.table[i][j]
                dist[i][j] = 1
                next[i][j] = j

        # run the Floyd-Warshall main algorithm
        for k in xrange(n):
            for i in xrange(n):
                for j in xrange(n):
                    if profit[i][j] < profit[i][k] * profit[k][j]:
                        profit[i][j] = profit[i][k] * profit[k][j]
                        dist[i][j] = dist[i][k] + 1
                        next[i][j] = next[i][k]

        # reconstruct path
        return self.path_reconstruct(profit, dist, next, threshold)

    def path_reconstruct(self, profit, dist, next_t, threshold):
        """
        Reconstruct path of arbitrage opportunities

        :param profit: greatef st exchange rates computed after Floyd-Warshall
        :param dist: number of currencies used to obtain the exchange rate
        :param next_t: previous currency used to construct a sequence for arbitrage
        :param threshold: margin over par to be considered an arbitrage opportunity

        :return: a list of arbitrage sequences
        """
        n = profit.shape[0]

        # acs stands for arbitrageable currencies
        acs = [i for i in xrange(n) if profit[i][i] > (1+threshold)]

        if len(acs) == 0:
            return self.NULL, []

        min_len = np.inf
        for i in acs:
            if min_len > dist[i][i]:
                min_len = dist[i][i]
                result = i

        path = []
        child = result
        while True:
            path.append(child)
            child = next_t[child][result]

            if child == result:
                path.append(result)
                break

        return i, path

def test(filename):
    with open(filename, 'r') as f:
        while True:
            args = f.readline()

            if not args:
                break

            exchange_rate_matrix = []
            currencies = int(args.strip())

            for i in xrange(currencies):
                line = f.readline().strip()
                exchange_rates = map(float, line.split())
                assert len(exchange_rates) == currencies - 1, \
                    'Invalid exchange_rates! [%s]' % line
                exchange_rates.insert(i, 1.0)
                exchange_rate_matrix.append(exchange_rates)

            table = ExchangeTable(exchange_rate_matrix)
            table.findArbitrage()

if __name__ == "__main__":
    test('104_input.txt')