from taquin import Taquin
import bisect
import time



def AStar(taquin: Taquin, timeout = 10):
    solver = _AStar(taquin)
    solver.solve(timeout=timeout)
    return solver

class _AStar: 
    def __init__(self, taquin):
        self.taquin = taquin
        self.open = []
        self.closed = []
        self.closed_map_hash = {}
        self.path = []
        self.max_open = 1
        self.g = 0
        self.h = 0
        self.f = 0

    def solve(self, timeout = 10):
        self.open.append(self.taquin)
        start = time.time()
        while len(self.open) > 0:
            end = time.time()
            if end - start > timeout:
                print("Timed out")
                self.path = None
                return None
            # self.open.sort(key=lambda x: x.f, reverse=False)
            current = self.open.pop(0)
            # self.closed.append(current)
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
                if len([open_node for open_node in self.open if child == open_node and child.g > open_node.g]) > 0:
                    continue
                bisect.insort(self.open, child)
            if len(self.open) > self.max_open:
                self.max_open = len(self.open)
        self.path = None
        return None

    def get_path(self):
        return self.path
    
    def get_stats(self):
        if self.path is None:
            return None
        return {
            "max_open_count": self.max_open,
            "closed_count": len(self.closed_map_hash.keys()),
            "path_len": len(self.path)
        }
