from taquin import Taquin
import time


def Dfs(taquin: Taquin, timeout=10):
    solver = _Dfs(taquin)
    solver.solve(timeout=timeout)
    return solver

class _Dfs:
    def __init__(self, taquin: Taquin):
        self.taquin = taquin
        self.open = []
        self.closed = []
        self.path = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.max_open = 1

    def solve(self, timeout = 60):
        MAXLIM = 35
        start = time.time()
        for lim in range(MAXLIM):
            end = time.time()
            if end - start > timeout:
                self.path = None
                return None
            self.closed = [self.taquin]
            if self._dfs(lim, 0, self.taquin):
                self.path+= [self.taquin]
                self.path = self.path[::-1]
                return self.path
        return None

    def _dfs(self, lim, g, parent, open_count=0):
        self.max_open = max(self.max_open, open_count)
        if parent.is_goal():
            while parent.parent:
                self.path.append(parent)
                parent = parent.parent
            return True
        if lim <= 0:
            return False
        if parent.get_state() in self.closed:
            return False
        self.closed.append(parent.get_state())
        
        possibleMoves = []
        movements = [
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]
        ]
        for direction in movements:
            movedTile = parent.move(direction)
            if movedTile is None:
                continue
            cost = movedTile.get_cost()
            movedTile.parent = parent
            possibleMoves.append((cost, movedTile))
            

        possibleMoves = sorted(possibleMoves, key=lambda x: x[0], reverse=False )
        for cost, st in possibleMoves:
            if self._dfs(lim-1, g+1+cost, st, open_count+1):
                return True 
    
    def get_path(self):
        return self.path

    def get_stats(self):
        return {
            "max_open_count": self.max_open,
            "closed_count": len(self.closed),
            "path_len": len(self.path)
        }
