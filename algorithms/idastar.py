from taquin import Taquin
import bisect
import time



def IDAStar(taquin: Taquin, timeout = 60):
    solver = _IDAStar(taquin)
    solver.solve(timeout=timeout)
    return solver

class _IDAStar: 
    # uses lower bound pruning and iterative deepening
    def __init__(self, taquin):
        self.taquin = taquin
        self.open = []
        self.closed = []
        self.closed_map_hash = {}
        self.path = []
        self.max_open = 1 

    def solve(self, timeout = 60):
        initial_depth = self.taquin.lower_bound()
        start = time.time()
        depth = initial_depth
        initial_taquin = Taquin(self.taquin.size)
        initial_taquin.set_state(self.taquin.get_state())
        while True:
            self.open = []
            self.closed = []
            self.closed_map_hash = {}
            self.path = []
            self.max_open = 1 
            self.taquin = initial_taquin.copy()
            end = time.time()
            if end - start > timeout:
                print("Timed out")
                self.path = None
                return None
            self.open.append(self.taquin)
            while len(self.open) > 0:
                end = time.time()
                if end - start > timeout:
                    print("Timed out")
                    self.path = None
                    return None
                current = self.open.pop(0)
                self.closed_map_hash[current.get_hash()] = 1
                if current.is_goal():
                    self.path.append(current)
                    while current.parent:
                        self.path.append(current.parent)
                        current = current.parent
                    self.path = self.path[::-1]
                    return self.path

                children = []
                directions = Taquin.validDirections
                for direction in directions:
                    child = current.move(direction)
                    if child is not None:
                        children.append(child)

                for child in children:
                    # if len([closed_child for closed_child in self.closed if closed_child == child]) > 0:
                    #     continue
                    if child.get_hash() in self.closed_map_hash:
                        continue
                    child.g = current.g + 1
                    child.h = child.get_cost()
                    child.f = child.g + child.h
                    child.parent = current
                    if child.lower_bound() + child.g <= depth:
                        bisect.insort(self.open, child)
                        self.max_open = max(self.max_open, len(self.open))
            depth += 1
            

    
    def get_path(self):
        return self.path
    
    def get_stats(self):
        return {
            "max_open": self.max_open,
            "closed_count": len(self.closed_map_hash.keys()),
            "open": len(self.open)
        }
