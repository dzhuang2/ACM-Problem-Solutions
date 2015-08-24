#-------------------------------------------------------------------------------
# Name:        101_Blocks.py
# Purpose:     Solves the ACM Problem
#              https://uva.onlinejudge.org/external/1/101.html
# Usage:       python 101_Blocks.py
# Author:      Di Zhuang
# Created:     07/31/2015
# Copyright:   (c) Di Zhuang 2015
#-------------------------------------------------------------------------------

"""
Central Idea:

Each block is essentially a node with 2 links, one to its parent and one to its children.
Each world is a dummy block with its parent Null.
Moving the blocks now amount to doubly linked list surgery.
"""

class Block(object):
    def __init__(self, block_id, prev, next):
        self.id = block_id # id is used to find the home world of this block
        self.prev = prev
        self.next = next # next is a pointer to the next block on top of this one

class RoboProgram(object):
    def __init__(self, blocks=10):
        self.world = [None] * blocks
        self.blocks = [None] * blocks

        for i in xrange(blocks):
            block = Block(i, None, None)
            world = Block(i, None, None)
            world.next = block
            block.prev = world
            self.world[i] = world # each world starts out with its own blocks
            self.blocks[i] = block # self.block holds a reference to the block directly

    def moveOnto(self, i, j):
        fromBlock, toBlock = self.blocks[i], self.blocks[j]
        self.pop(fromBlock)
        self.pop(toBlock)
        RoboProgram.stackOnTop(fromBlock, toBlock, self.isDescendent(i, j)) # the last entry should be false

    def moveOver(self, i, j):
        fromBlock, toBlock = self.blocks[i], self.blocks[j]
        self.pop(fromBlock)
        top = RoboProgram.last(toBlock)
        RoboProgram.stackOnTop(fromBlock, top, self.isDescendent(i, j))

    def pileOnto(self, i, j):
        fromBlock, toBlock = self.blocks[i], self.blocks[j]
        self.pop(toBlock)
        RoboProgram.stackOnTop(fromBlock, toBlock, self.isDescendent(i, j))
        toBlock.prev = fromBlock.prev

    def pileOver(self, i, j):
        fromBlock, toBlock = self.blocks[i], self.blocks[j]
        top = RoboProgram.last(toBlock)
        RoboProgram.stackOnTop(fromBlock, top, self.isDescendent(i, j))

    def isDescendent(self, i, j):
        block = self.blocks[i]

        found = None
        while block.next:
            if block.next.id == j:
                found = block
                break
            block = block.next

        return found

    def displayWorld(self):
        for i in xrange(len(self.world)):
            print "%d:" % i,
            block = self.world[i]

            while block.next:
                block = block.next
                print "%d" % block.id,

            print

    def pop(self, currentBlock):
        # return the blocks on top of block i to its original world
        nextBlock = currentBlock.next
        if nextBlock: # if this block is not the top most, return block to homeworld
            currentBlock.next = None
            self.world[nextBlock.id].next = nextBlock
            nextBlock.prev = self.world[nextBlock.id]
            self.pop(nextBlock)

    @staticmethod
    def stackOnTop(fromBlock, toBlock, descendent=None):
        toBlock.next = fromBlock
        if not descendent:
            fromBlock.prev.next = None # update the previous parent
        else:
            descendent.next = None
            fromBlock.prev.next = toBlock
            toBlock.prev = fromBlock.prev
        fromBlock.prev = toBlock # reflect the new relationship

    @staticmethod
    def last(block):
        while block.next:
            block = block.next
        return block

def test(filename):
    with open(filename, 'r') as f:
        world = int(f.readline().strip())
        robo = RoboProgram(world)

        for line in f:
            print '*' * 80
            command = line.strip().split(" ")
            if len(command) == 4:
                action, block1, cmd_type, block2 = command
                block1 = int(block1)
                block2 = int(block2)

                if block1 == block2:
                    print "command '%s' is illegal and ignored" % line.strip()
                else:
                    print "%s" % line.strip()

                    if action == "move" and cmd_type == "over":
                        robo.moveOver(block1, block2)
                    elif action == "move" and cmd_type == "onto":
                        robo.moveOnto(block1, block2)
                    elif action == "pile" and cmd_type == "over":
                        robo.pileOver(block1, block2)
                    elif action == "pile" and cmd_type == "onto":
                        robo.pileOnto(block1, block2)
                    else:
                        print "command '%s' is illegal and ignored" % line.strip()

                    robo.displayWorld()

            elif len(command) == 1 and command[0] == "quit":
                print 'Final world view: '
                robo.displayWorld()
            else:
                print "command '%s' is illegal and ignored" % line.strip()

if __name__ == "__main__":
    test('101_input.txt')