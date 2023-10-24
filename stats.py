from taquin import Taquin
from algorithms import *
import time
import matplotlib.pyplot as plt
import numpy as np
algorithmMap = {
    1: (AStar, 'A* Search'),
    # 2: (Dfs, 'Depth First Search'),
    # 3: (Bfs, 'Breadth First Search'),
}
print("start")
def compare(size = 4):
    # this function will run all the algorithms and compare them for a shuffle count between 0 and 100
    # it will then display the results using matplotlib
    totalExecutionTime = {}
    for algorithmId, (alg, alg_name) in algorithmMap.items():
        x = []
        y = []
        stats = []
        totalExecutionTime[alg_name] = 0
        for shuffleCount in range(0, 100):
            iters = 1
            interval_seconds = 0
            for _ in range(iters):
                taquin = Taquin(size)
                taquin.shuffle_board(shuffleCount)
                start = time.time()
                solver = alg(taquin)
                if solver.get_path() is None:
                    continue
                end = time.time()
                stat = solver.get_stats()
                stats.append(stat)
                interval_seconds += end - start
            interval_seconds/= iters
            # x.append(solver.get_path()[0].get_cost())
            x.append(shuffleCount)
            y.append(interval_seconds)     
            totalExecutionTime[alg_name]+=interval_seconds * iters    
        plt.scatter(x, y, label=alg_name)
        # plot the regression line
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        plt.plot(x,p(x),"r--", label= alg_name + " fitted line")

    plt.xlabel('Shuffle Count')
    plt.ylabel('Time (s)')
    plt.title('Algorithm Comparison')
    print(totalExecutionTime)
    plt.legend()
    plt.show()


# compare()    

# Run the solver and return execution time for n executions for a given board size
def compare_perf_size(solver, size, executions):
    totalExecutionTime = []
    for _ in range(executions):
        taquin = Taquin(size)
        taquin.shuffle_board(30)
        start = time.time()
        path = solver(taquin, timeout=20).get_path()
        if path is None:
            # add timeout to execution time
            totalExecutionTime += [20]
            continue
        end = time.time()
        totalExecutionTime += [end - start]
    return totalExecutionTime

def compare_size():
    # this function will run all the algorithms and compare them for a size between 3 and 7
    # it will then display the results using matplotlib
    for algorithmId, (alg, alg_name) in algorithmMap.items():
        x = []
        y = []
        for size in range(3, 8):
            execTimes = compare_perf_size(alg, size, executions=10)
            # for each size, we scatter the execution times
            x += [size] * len(execTimes)
            y += execTimes
        plt.scatter(x, y, label=alg_name)
        # plot the regression line
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        plt.plot(x,p(x),"r--", label= alg_name + " fitted line")

    plt.xlabel('Size')
    plt.ylabel('Time (s)')
    plt.title('Algorithm Comparison')
    plt.legend()
    plt.show()

compare_size()
    