#-------------------------------------------------------------------------------
# Name:        105_Skyline
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/105.html
# Usage:       python 105_Skyline.py
# Author:      Di Zhuang
# Created:     08/22/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

DEBUG = False

import heapq

class Skyline(object):
    """
    Accomplishes generating the skyline via priority queue


    """

    def __init__(self):
        self.buildings = []

    def addBuilding(self, building):
        assert isinstance(building, tuple) and len(building) == 3, \
            "Invalid building! %r" % building
        heapq.heappush(self.buildings, building)

    def skyline(self):
        skyline = []
        while len(self.buildings):
            start, height, end = heapq.heappop(self.buildings)

            if len(self.buildings) == 0:
                skyline.append((start, height, end))
                break

            start_next, height_next, end_next = self.buildings[0]

            if start < start_next:
                if end < start_next:
                    # if building is to the left of the next building
                    # building A: ----
                    # building B:      ---------
                    skyline.append((start, height, end))
                    skyline.append((end, 0, start_next))
                elif end > start_next:
                    # if building overlaps with the next building
                    # building A: -----
                    # building B:  ------------
                    skyline.append((start, height, start_next))
                    heapq.heappush(self.buildings, (start_next, height, end))
                else: # end == start_next
                    # if building is to the left of the next building
                    # building A: ---
                    # building B:    ---------
                    skyline.append((start, height, end))
            elif start == start_next:
                if end < end_next:
                    # if building overlaps with the next building as shown:
                    # building A: ------
                    # building B: -------------
                    heapq.heapreplace(self.buildings, (end, height_next, end_next))
                    heapq.heappush(self.buildings, (start, max(height, height_next), end))
                elif end > end_next:
                    # if building overlaps with the next building as shown:
                    # building A: ---------------
                    # building B: ------
                    heapq.heapreplace(self.buildings, (end_next, height, end))
                    heapq.heappush(self.buildings, (start, max(height, height_next), end_next))
                else: # end == end_next
                    # if building overlaps completely with the next building
                    # building A: -------------
                    # building B: -------------
                    heapq.heapreplace(self.buildings, (start, max(height, height_next), end))
            else:
                raise ValueError, "Heap invariant is violated!"

        if DEBUG:
            print skyline

        if len(skyline) == 0:
            return []

        outline = list(skyline.pop(0))
        while len(skyline):
            start, height, end = skyline.pop(0)
            assert outline[-1] == start, "Skyline at %d is not continuous!" % start_next

            if height == outline[-2]:
                outline.pop()
                outline.append(end)
            else:
                outline.extend([height, end])

        outline.append(0)

        return outline

def test(filename, answer=""):
    with open(filename, 'r') as f:
        sky = Skyline()
        for line in f:
            building = tuple(map(int, line.strip().split()))
            sky.addBuilding(building)
        sol = " ".join([str(num) for num in sky.skyline()])
        print sol
        print answer
        if sol == answer:
            print "Solution correct!"
        else:
            print "Solution incorrect!"

if __name__ == "__main__":
    test('105_input.txt', answer="1 20 6 13 9 0 12 7 15 8 16 3 19 18 22 3 23 13 29 0")