#-------------------------------------------------------------------------------
# Name:        103_Stacking_Boxes.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/103.html
# Usage:       python 103_Stacking_Boxes.py
# Author:      Di Zhuang
# Created:     08/08/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import numpy as np

class Box(object):
    SMALLER, LARGER, NO_FIT = range(3)

    """
    A Box is essentially a tuple with a comparison operator overloaded.

    Let SortedA be a tuple of sorted dimensions of Box A,
     and SortedB be a tuple of sorted dimensions of Box B.

    Then, Box A nests inside Box B, if and only if SortedA is less than Sorted B.
    """
    def __init__(self, id, dim):
        self.id = id
        self.dim = list(dim)
        self.sorted = tuple(sorted(dim))

    def compare(self, other):
        cmp1 = []
        cmp2 = []

        for (a, b) in zip(self.sorted, other.sorted):
            cmp1.append(a<b)
            cmp2.append(a>b)

        if all(cmp1): # this box fits inside the other box
            return Box.SMALLER
        elif all(cmp2): # the other box fits inside this box
            return Box.LARGER
        else:
            return Box.NO_FIT

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "%d: Box(%s)" % (self.id, self.dim)

class StackingBoxes(object):
    """
    Sort the sorted dimensions of boxes lexicographically,
    then generate the longest nesting sequence
    """

    def __init__(self):
        self.boxes = []

    def insertBox(self, box):
        self.boxes.append(box)

    def longestNest(self, all_paths=True):
        """
        find and print out a list of the longest nesting of boxes
        :param all_paths: print all longest paths if True
        :return:
        """
        self.boxes = sorted(self.boxes, key=lambda a_box: a_box.sorted)
        seqs = self.lis(self.boxes, all_paths)

        for path in seqs:
            num = len(path)
            msg = " ".join([str(self.boxes[i].id) for i in path])
            print 'longest nest of boxes: %d' % num
            print 'list of boxes: %s' % msg
            print '*' * 80

    def lis(self, boxes, all_paths):
        """
        run longest increasing subsequence algorithm on the sorted list of boxes

        :param boxes: array containing a list of boxes
        :return: all longest increasing sequences as a string
        """
        num_boxes = len(boxes)
        best = np.empty(num_boxes, dtype=np.int8)
        best.fill(1)
        parent = np.empty(num_boxes, dtype=np.int8)
        parent.fill(-1)

        for i in xrange(num_boxes):
            for j in xrange(i):
                if boxes[j].compare(boxes[i]) == Box.SMALLER and \
                        best[i] < best[j] + 1:
                    best[i] = best[j] + 1
                    parent[i] = j

        return self.all_lis(best, parent, all_paths)

    def all_lis(self, best, parent, all_paths):
        """
        find and print out ALL longest increasing subsequences in an array

        :param best: array containing max length of increasing subsequence for that position
        :param parent: location of previously item in longest increasing subsequence
        :param all_paths: if true, return all longest increasings paths
        :return: longest increasing sequences as a list of paths
        """

        if all_paths:
            indices = np.nonzero(best == np.max(best))[0]
        else:
            indices = [np.argmax(best)]

        paths = []
        for index in indices:
            path = []
            while True:
                path.insert(0, index)

                if parent[index] == -1:
                    break

                index = parent[index]

            paths.append(path)

        return paths

def test(filename):
    with open(filename, 'r') as f:
        while True:
            args = f.readline()

            if not args:
                break

            num_boxes, dimensions = map(int, args.strip().split(" "))
            stack_of_boxes = StackingBoxes()

            for i in xrange(num_boxes):
                line = f.readline().strip()
                measurements = map(int, line.split(" "))
                assert len(measurements) == dimensions, \
                    'Invalid measurements! [%s]' % line
                stack_of_boxes.insertBox(Box(i+1, measurements))

            stack_of_boxes.longestNest(all_paths=False)

if __name__ == "__main__":
    test('103_input.txt')