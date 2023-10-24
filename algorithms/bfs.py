from taquin import Taquin


def Bfs(taquin: Taquin):
    solver = _Bfs(taquin)
    solver.solve()
    return solver

class _Bfs:
    def __init__(self, taquin: Taquin):
        self.taquin = taquin
        self.open = []
        self.closed = []
        self.path = []
        self.g = 0
        self.h = 0
        self.f = 0

    def solve(self):
        return None
    
    def get_path(self):
        raise NotImplementedError('BFS is not implemented yet')
        return self.path