# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:49:31 2018

@author: rarossi
"""

import time
import random

'''
  Peg Solitaire Solver
  Copyright (C) 2014 blackflux.com <pegsolitaire@blackflux.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License version 3 as
   published by the Free Software Foundation.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 '''

'''
  Solver for the English peg solitaire.
  This program finds a random solution for peg solitaire game by using brute force.

  -- Runtime
  A solution is typically found in less than two seconds, but the time does highly
  fluctuate (I've seen everything from a few milliseconds to several seconds).

  -- Implementation

  The implementation is highly optimized and uses bit operators to efficiently find
  a solution. The idea is as following: Since there exists 33 slots on the board, it
  can not be represented by using an integer (32 bits), but we can use a long (64 bits).
  The first 49 bits (7 x 7) of the long represent the board. However there are some bits
  that are not valid and never used, i.e. 0,1,5,6,7,8,12,13 and so on. Checking of
  possible moves and applying them can be done by using simple bit operations.

  A recursive function is then used to check all possible moves for a given board,
  applying each valid move and calling itself with the resulting board. The recursion is
  done "in reverse", starting from the goal board. While this is not conceptually faster [a],
  it allows for a minimum amount of bit operations in the recursion:

  To reverse a move we can simply check
  - (board & twoBalls) == 0 and
  - (board & oneBall) != 0
  where "twoBalls" indicates the two ball that would need to be added for this reversed move.
  If we instead used the intuitive search direction, the same check would require additional
  binary operations, since a simple inversion of the check would not work [b].

  Paper [1] shows how the moves can be ordered to almost instantly find a solution.
  Website [2] gives a nice overview of binary operations and some tricks that
  can be applied.

  [a] Playing the game in reverse is simply the inversion of the original game - just remove all
  balls from the board and place ball where there were none before and you'll understand
  what I mean.
  [b] There is no "single" binary operation to check if two specific bits are set, but there
  is one to check if they are both zero. There is further a binary operation to check if a specific
  bit is set.

  [1] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.4826 (download at the top)
  [2] http://graphics.stanford.edu/~seander/bithacks.html

  https://blackflux.wordpress.com/2014/04/30/peg-solitaire-brute-force/

'''

# goal board (one marble in center)
GOAL_BOARD = 16777216
# initial board (one marble free in center)
INITIAL_BOARD = 124141717933596
# board that contains a ball in every available slot, i.e. GOAL_BOARD | INITIAL_BOARD
VALID_BOARD_CELLS = 124141734710812


class RestaUm():

    def __init__(self):
        self.reset()

    def reset(self):
        # list of seen boards - this is used to prevent rechecking of paths
        self.seenBoards = set()

        # list of solution boards in ascending order - filled in once the solution is found
        self.solution = list()

        # holds all 76 moves that are possible
        # the inner array is structures as following:
        # - first entry holds the peg that is added by the move
        # - second entry holds the two pegs that are removed by the move
        # - third entry holds all three involved pegs
        self.moves = list()

    # print the board
    def printBoard(self, board):
        # loop over all cells (the board is 7 x 7)
        for i in range(49):
            validCell = not ((1 << i) & VALID_BOARD_CELLS) == 0
            print("  " if not validCell else "X " if ((1 << i) & board) else "O ", end='')
            if i % 7 == 6:
                print()
        print("-------------")

    def printSolution(self):
        for step in self.solution:
                self.printBoard(step)

    # create the two possible moves for the three added pegs
    # (this function assumes that the pegs are in one continuous line)
    def createMoves(self, bit1, bit2, bit3):
        self.moves.append([(1 << bit1), (1 << bit2) | (1 << bit3),
                           (1 << bit1) | (1 << bit2) | (1 << bit3)])
        self.moves.append([(1 << bit3), (1 << bit2) | (1 << bit1),
                           (1 << bit1) | (1 << bit2) | (1 << bit3)])

    # do the calculation recursively by starting from
    # the "GOAL_BOARD" and doing moves in reverse
    def search(self, board):
        # for all possible moves
        for move in self.moves:
            # check if the move is valid
            # Note: we place "two ball" check first since it is more
            # likely to fail. This saves about 20% in run time (!)
            if (move[1] & board) == 0 and (move[0] & board) != 0:
                # calculate the board after this move was applied
                newBoard = board ^ move[2]
                # only continue processing if we have not seen this board before
                if newBoard not in self.seenBoards:
                    self.seenBoards.add(newBoard)
                    # check if the initial board is reached
                    if newBoard == INITIAL_BOARD or self.search(newBoard):
                        self.solution.append(board)
                        return True
        return False

    # the main method
    def solve(self, shuffle=True, print_solution=True):

        # add starting board (as this board is not added by the recursive function)
        self.solution = list()
        self.solution.append(INITIAL_BOARD)

        # generate all possible moves
        # holds all starting positions in west-east direction
        startsX = [2, 9, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 37, 44]
        for x in startsX:
            self.createMoves(x, x + 1, x + 2)
        # holds all starting positions in north-south direction
        startsY = [2, 3, 4, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 30, 31, 32]
        for y in startsY:
            self.createMoves(y, y + 7, y + 14)

        # randomize the order of the moves (this highly influences the resulting runtime)
        if shuffle:
            self.moves = random.sample(self.moves, len(self.moves))

        # start recursively search for the initial board from the goal (reverse direction!)
        et = time.time()
        self.search(GOAL_BOARD)
        et = time.time() - et

        # print the found solution
        if print_solution:
            self.printSolution()

        # print required time
        print("Completed in %.3f s." % et)


if __name__ == '__main__':
    resta1 = RestaUm()

    # benchmark 10 runs
    print('Shuffling moves')
    for i in range(10):
        resta1.solve(shuffle=True, print_solution=False)
        resta1.reset()
    print('Not shuffling moves')
    for i in range(10):
        resta1.solve(shuffle=False, print_solution=False)
        resta1.reset()
''' output:

Shuffling moves
Completed in 63.033 s.
Completed in 0.724 s.
Completed in 23.499 s.
Completed in 0.370 s.
Completed in 6.520 s.
Completed in 7.830 s.
Completed in 50.473 s.
Completed in 8.124 s.
Completed in 33.454 s.
Completed in 10.986 s.
Not shuffling moves
Completed in 21.188 s.
Completed in 21.360 s.
Completed in 18.633 s.
Completed in 18.061 s.
Completed in 17.717 s.
Completed in 20.257 s.
Completed in 21.200 s.
Completed in 19.571 s.
Completed in 17.535 s.
Completed in 16.581 s.
'''
