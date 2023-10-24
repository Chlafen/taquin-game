import random
import time
import math
import bcrypt 

class Taquin:
    def __init__(self, size):
        self.size = size
        self._state = self.get_solution()
        self._goal = self.get_state()
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None

    # hash function
    def get_hash(self):
        # hash state
        state = str(self._state)
        return state

   
    def __str__(self):
        # Print the board with the 0 being colored in blue
        result = ''
        for i in range(self.size):
            for j in range(self.size):
                if self._state[i][j] == 0:
                    result += '\033[94m{:3d}\033[0m'.format(self._state[i][j])
                else:
                    result += '{:3d}'.format(self._state[i][j])
            result += '\n'
        return result

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def copy(self):
        result = Taquin(self.size)
        result.set_state(self._state)
        return result

    validDirections = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]
    ]

    def get_solution(self):
        sol = []
        for i in range(0, self.size):
            row = []
            for j in range(0, self.size):
                row.append(i * self.size + j)
            sol.append(row)
        return sol

    def is_valid_square(self, tile):
        return tile[0] >= 0 and tile[0] < self.size and tile[1] >= 0 and tile[1] < self.size

    def swap(self, tile1, tile2):
        self._state[tile1[0]][tile1[1]] = self._state[tile2[0]][tile2[1]]
        self._state[tile2[0]][tile2[1]] = 0
  
    def move(self, direction):

        if direction not in self.validDirections:
            return None

        oldTile = self.get_tile(0)
        newTile = [oldTile[0] + direction[0], oldTile[1] + direction[1]]
        if self.is_valid_square(newTile):
            result = Taquin(self.size)
            result.set_state(self._state)
            result.swap(oldTile, newTile)
            return result
        else:
            return None

    def is_goal(self):
        return self._state == self._goal

    def get_state(self):
        # return a copy of the state
        return [row[:] for row in self._state]

    def set_state(self, newstate):
        self._state = [row[:] for row in newstate]

    def shuffle_board(self, nShuffle=0):
        moves = [
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]
        ]
        random.seed(time.time())
        path = []
        path.append(self.get_state())
        for _ in range(nShuffle):
            stateCosts = []
            # ----------------- GREEDY SHUFFLE -----------------
            for move in moves:
                newboard = self.move(move)
                if newboard is None:
                    continue
                costi = newboard.get_cost()
                stateCosts.append([newboard, costi])
            stateCosts.sort(key=lambda x: x[1], reverse=True)
            maxState = random.choice(stateCosts[:2])[0]
            # ----------------- RAND SHUFFLE -----------------
            # mymove = random.choice(moves)
            # newboard = self.move(mymove)
            # if newboard is None:
            #     continue
            # maxState = newboard
            # ----------------- END SHUFFLE -----------------
            if maxState is not None:
                self.set_state(maxState.get_state())
                path.append(self.get_state())
        return path

    def get_tile(self, tileId):
        for i in range(len(self._state)):
            for j in range(len(self._state)):
                if self._state[i][j] == tileId:
                    return [i, j]
        exit(-1)

    def lower_bound(self):
        # the absolute minimum number of moves to solver board
        goal = self._goal
        return sum([abs(self.get_tile(goal[i][j])[0] - i) + abs(self.get_tile(goal[i][j])[1] - j)
                 if goal[i][j] != self._state[i][j] else 0 for i in range(self.size) for j in range(self.size)])
    def get_cost(self):
        goal = self._goal
        # The
        h1 = sum([1 if goal[i][j] != self._state[i][j]
                 else 0 for i in range(self.size) for j in range(self.size)])
        h2 = self.lower_bound()
        return h1 + h2 



def board_solution(size):
    sol = []
    for i in range(0, size):
        row = []
        for j in range(0, size):
            row.append(i * size + j)
        sol.append(row)
    return sol
