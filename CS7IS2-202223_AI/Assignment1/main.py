import sys
import os
import argparse
import numpy as np
myDir = os.getcwd()
sys.path.append(myDir)

from MazeSovler import BFS, DFS, AStar, MDP

algorithms = ['bfs', 'dfs', 'astar', 'mdp-v', 'mdp-p']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', help='rows of maze', type=int)
    parser.add_argument('--cols', help='cols of maze', type=int)
    parser.add_argument('--solver', help='algorithm of solver', type=str)
    parser.add_argument('--fromfile', help='local maze file path', type=str)

    args = parser.parse_args()

    if args.rows is None:
        print("Please specify the maze rows")
        exit(1)

    if args.cols is None:
        print("Please specify the maze cols")
        exit(1)
    
    if args.solver is None:
        print("Please specify the algorithm of maze solver")
        exit(1)
    
    if args.solver not in algorithms:
        print("This algorithm isn't supported!")
        print("Try:")
        print(algorithms)
        exit(1)
    
    return args


def main():
    args = parse_args()
    rows = args.rows
    cols = args.cols
    solver = args.solver
    mazefile = args.fromfile

    if solver == 'bfs':
        run_bfs(rows, cols, mazefile)
    elif solver == 'dfs':
        run_dfs(rows, cols, mazefile)
    elif solver == 'astar':
        run_astar(rows, cols, mazefile)
    elif solver == 'mdp-v':
        run_mdp_value(rows, cols, mazefile)
    elif solver == 'mdp-p':
        run_mdp_policy(rows, cols, mazefile)

def run_mdp_value(rows, cols, mazefile, test=False):
    print("Algorithm: MDP Value Iteration") 
    my_solver = MDP()
    my_solver.generate_maze(rows, cols, fromfile=True, savePath=mazefile)
    # mdp value iteration
    my_solver.value_iteration(0.8)
    if not test:
        my_solver.display()
    
    time_cost, memory_cost, steps = my_solver.print_cost()
    return time_cost, memory_cost, steps

def run_mdp_policy(rows, cols, mazefile, test=False):
    print("Algorithm: MDP Policy Iteration") 
    my_solver = MDP()
    my_solver.generate_maze(rows, cols, fromfile=True, savePath=mazefile)
    my_solver.policy_iteration(0.8)
    if not test:
        my_solver.display()
    
    time_cost, memory_cost, steps = my_solver.print_cost()
    return time_cost, memory_cost, steps

def run_astar(rows, cols, mazefile, test=False):
    print("Algorithm: A Star") 
    my_solver = AStar()
    my_solver.generate_maze(rows, cols, fromfile=True, savePath=mazefile)
    my_solver.solve()
    if not test:
        my_solver.display()
    
    time_cost, memory_cost, steps = my_solver.print_cost()
    return time_cost, memory_cost, steps

def run_dfs(rows, cols, mazefile, test=False):
    print("Algorithm: DFS") 
    my_solver = DFS()
    my_solver.generate_maze(rows, cols, fromfile=True, savePath=mazefile)
    my_solver.solve()
    if not test:
        my_solver.display()
    
    time_cost, memory_cost, steps = my_solver.print_cost()
    return time_cost, memory_cost, steps

def run_bfs(rows, cols, mazefile, test=False):
    print("Algorithm: BFS") 
    my_solver = BFS()
    my_solver.generate_maze(rows, cols, fromfile=True, savePath=mazefile)
    my_solver.solve()
   
    if not test:
        my_solver.display()

    time_cost, memory_cost, steps = my_solver.print_cost()
    return time_cost, memory_cost, steps

def test_performance():
    maze_size = [30, 50, 70]
    save_dir = 'savedMaze'
   
    for s in maze_size:
        time_costs = []
        memory_costs = []
        steps = []
        print("------ Maze: %dx%d ------" % (s, s)) 
        for i in range(5):
            mazefile = '%s/%dx%d_%d.csv' % (save_dir, s, s, i)
            # time_cost, memory_cost, step = run_bfs(s, s, mazefile, True)
            # time_cost, memory_cost, step = run_dfs(s, s, mazefile, True)
            # time_cost, memory_cost, step = run_astar(s, s, mazefile, True)
            # time_cost, memory_cost, step = run_mdp_value(s, s, mazefile, True)
            time_cost, memory_cost, step = run_mdp_policy(s, s, mazefile, True)
            time_costs.append(time_cost) 
            memory_costs.append(memory_cost)
            steps.append(step)
            
        print("%dx%d maze: average time cost: %.3f ms, average memeory cost: %.3f KB, average solution length: %d"
               % (s, s, np.average(time_costs), np.average(memory_costs), np.average(steps)))

if __name__ == '__main__':
    main()
