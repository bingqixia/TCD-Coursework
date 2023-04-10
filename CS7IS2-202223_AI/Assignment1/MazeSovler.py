from pyamaze.pyamaze import maze, agent, COLOR, textLabel
import os
import time
from collections import deque
from queue import Queue, PriorityQueue
import numpy as np
import psutil

class MazeSolver(object):
    def __init__(self, start=None):
        self.title = ''
        self.name = ''
        self.directions = 'ESNW'
        self.start = start
        self.saved_path = {}
        self.solution = {}
        self.search_path = []
        
        self.mazeDir = 'savedMaze'
        self.start_time = 0
        self.end_time = 0
        self.iterations = 0
        
        self.memory_before = 0 
        self.memory_after = 0


    # start position: (maze.rows, maze.cols)
    # goal position: (1, 1)
    # keep maze same for different algorithms
    def generate_maze(self, rows, cols, fromfile=False, savePath=None):
        self.maze = maze(rows, cols)
        self.title = "%dx%d" % (rows, cols)
        if self.start is None:
            self.start=(self.maze.rows, self.maze.cols)

        if fromfile and savePath is not None and os.path.exists(savePath):
            self.maze.CreateMaze(theme='light', loadMaze=savePath)
        elif savePath is not None:
            self.maze.CreateMaze(loopPercent=50, theme='light', saveMaze=True, savePath=savePath)
        else:
            self.maze.CreateMaze(loopPercent=50, theme='light', saveMaze=False)
        return self.maze
    

    def get_neighbors(self, current_node):
        all_neighbors = self.maze.maze_map[current_node]
        available_neighbors = []
        for direction in self.directions:
            if(all_neighbors[direction] == 1):
                if direction == 'E':
                    available_neighbors.append((current_node[0], current_node[1]+1))
                elif direction == 'W':
                    available_neighbors.append((current_node[0], current_node[1]-1))
                elif direction == 'S':
                    available_neighbors.append((current_node[0]+1, current_node[1]))
                elif direction == 'N':
                    available_neighbors.append((current_node[0]-1, current_node[1]))
        return available_neighbors
    

    def solve(self):
        pass

    def reverse_path(self):
        node = self.maze._goal
        while node != self.start:
            self.solution[self.saved_path[node]] = node
            node = self.saved_path[node]
    
    def display(self):
        solution_agent = agent(self.maze, footprints=True, color=COLOR.red)
        self.maze.tracePath({solution_agent: self.solution}, delay=100)
        text = textLabel(self.maze, title=self.title, value=self.name)
        text.drawLabel()
        self.maze.run()

    def get_memory_usage(self):
        process = psutil.Process()
        # KB
        memory_info = process.memory_info().rss / 1024
        return memory_info

    def print_cost(self):
        time_cost = (self.end_time-self.start_time)*1000 
        memory_cost = self.memory_after - self.memory_before
        print("------- Sovle the maze by %s algorithm ------" % (self.name))
        print("Run Time: %f ms" % (time_cost))
        print("Iteration Numbers: %d" % (self.iterations))
        print("Length of Solution Path: %d" % (len(self.solution)))
        return time_cost, memory_cost, len(self.solution)


class DFS(MazeSolver):
    def __init__(self, start=None):
        super().__init__(start)
        self.name = 'DFS'
        

    def solve(self):
        self.iterations = 0
        self.start_time = time.process_time()
        self.memory_before = self.get_memory_usage()
        stack = deque()
        visited_node = set()

        stack.append(self.start)
        visited_node.add(self.start)

        while stack:
            
            current_node = stack.pop()
            if(current_node == self.maze._goal):
                break
            
            self.iterations += 1
            self.search_path.append(current_node)
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited_node:
                    stack.append(neighbor)
                    visited_node.add(neighbor)
                    # there are multiple next steps, so we need reverse the key and value
                    self.saved_path[neighbor] = current_node
        
        self.end_time = time.process_time() 
        self.memory_after = self.get_memory_usage()     
        self.reverse_path()
        return self.solution


class BFS(MazeSolver):
    def __init__(self, start=None):
        super().__init__(start)
        self.name = 'BFS'
        

    def solve(self):
        self.start_time = time.process_time()
        self.memory_before = self.get_memory_usage()  
        queue = Queue()
        visited_node = set()

        queue.put(self.start)
        visited_node.add(self.start)
        self.iterations = 0
        while not queue.empty():
            current_node = queue.get()
            if current_node == self.maze._goal:
                break
            self.iterations += 1
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited_node:
                    queue.put(neighbor)
                    visited_node.add(neighbor)
                    # there are multiple next steps, so we need reverse the key and value
                    self.saved_path[neighbor] = current_node
                    self.search_path.append(neighbor)
        
        self.end_time = time.process_time()
        self.memory_after = self.get_memory_usage()  
        self.reverse_path()
        
        return self.solution


class AStar(MazeSolver):
    def __init__(self, start=None):
        super().__init__(start)
        self.name = 'AStar'
    

    def manhattan(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1-x2) + abs(y1-y2)
    
    
    def solve(self):
        self.start_time = time.process_time()
        self.memory_before = self.get_memory_usage()  
        self.iterations = 0

        queue = PriorityQueue()
        # use manhattan distance as h(n), for the start position, g(n)=0. f(n) = h(n) + g(n)
        initalH = self.manhattan(self.start, self.maze._goal)
        queue.put((initalH, initalH, self.start))

        # init g(n) and f(n)
        g_score = {row: float("inf") for row in self.maze.grid}
        g_score[self.start] = 0

        f_score = {row: float("inf") for row in self.maze.grid}
        f_score[self.start] = initalH

        while not queue.empty():
            # get current node
            first = queue.get()
            current_node = first[2]
            if(current_node == self.maze._goal):
                break
            
            self.iterations += 1
            self.search_path.append(current_node)

            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                tmp_g_score = g_score[current_node] + 1
                tmp_h = self.manhattan(neighbor, self.maze._goal)
                tmp_f_score = tmp_g_score + tmp_h

                if tmp_f_score < f_score[neighbor]:
                    g_score[neighbor] = tmp_g_score
                    f_score[neighbor] = tmp_f_score
                    queue.put((tmp_f_score, tmp_h, neighbor))
                
                    # there are multiple next steps, so we need reverse the key and value
                    self.saved_path[neighbor] = current_node
        
        self.end_time = time.process_time()
        self.memory_after = self.get_memory_usage()  
        self.reverse_path()
        return self.solution


class MDP(MazeSolver):
    def __init__(self, start=None):
        super().__init__(start)
        self.probabilities=(0.8, 0.1, 0.1)   #forward, right, left
        self.actions = {
            'N': ['N', 'W', 'E'],
            'S' : ['S', 'E', 'W'],
            'W' : ['W', 'S', 'N'],
            'E' : ['E', 'N', 'S']
        }

        self.rewards = {}
        self.trans_probs = {}

    
    def setupMdp(self):
        self.rewards = self.init_rewards()


    # define a function to get the next state and reward given a current state and action
    def get_next_state_reward(self, current_state, action):
        x, y = current_state
        normal_reward = -0.5
        goal_reward = 1
        wall_reward = -1

        # Arrive the goal
        if current_state == self.maze._goal:
            next_state = current_state
            reward = goal_reward
        else:
            # On the path
            if action == 'N':
                if self.maze.maze_map[current_state]['N'] == 1:
                    next_state = (x-1, y)
                    reward = normal_reward
                else:
                    next_state = current_state
                    reward = wall_reward
            elif action == 'S':
                if self.maze.maze_map[current_state]['S'] == 1:
                    next_state = (x+1, y)
                    reward = normal_reward
                else:
                    next_state = current_state
                    reward = wall_reward
            elif action == 'W':
                if self.maze.maze_map[current_state]['W'] == 1:
                    next_state = (x, y-1)
                    reward = normal_reward
                else:
                    next_state = current_state
                    reward = wall_reward
            elif action == 'E':
                if self.maze.maze_map[current_state]['E'] == 1:
                    next_state = (x, y+1)
                    reward = normal_reward
                else:
                    next_state = current_state
                    reward = wall_reward
        return next_state, reward


    def init_rewards(self):
        # R(s, a)
        rewards = {}
        for state in self.maze.maze_map:
            rewards[state] = {}
            for action in self.actions:
                rewards[state][action] = {}
                next_state, current_reward = self.get_next_state_reward(state, action)
                rewards[state][action] = (next_state, current_reward)
        return rewards

    
    # get possible action and prob for an action
    def get_possible_action(self, state, action):
        # action: prob
        possible_actions = {}
        for i in range(len(self.actions[action])):
             # there are 0.2 noise that the agent moves to left/right
            possible_action = self.actions[action][i]
            prob = self.probabilities[i]
            next_state = self.rewards[state][possible_action][0]

            possible_actions[possible_action] = {'prob': prob, 'state': next_state}
        
        return possible_actions
                

    def value_iteration(self, gamma, error=1e-10):
        self.name = 'MDP-Value Iteration'
        self.iterations = 0
        if not self.rewards:
            self.setupMdp()
        self.start_time = time.process_time()
        self.memory_before = self.get_memory_usage()  
        V = {}
        policy = {}
        all_states = self.maze.maze_map
        for state in all_states:
            V[state] = 0
            policy[state] = 'N' # initialize policy to any action

        while True:
            delta = 0
            self.iterations += 1
            for state in all_states:
                v = V[state]
                max_v = -np.inf
                best_action = 'N' # initialize best action to any action
                for action in self.actions:
                    action_v = 0
                    curret_reward = self.rewards[state][action][1]
                   
                    possible_actions = self.get_possible_action(state, action)

                    for pa in possible_actions:
                        next_state, _ = self.rewards[state][pa]
                        prob = possible_actions[pa]['prob']
                        action_v += (prob*V[next_state])
                    action_v = action_v * gamma + curret_reward
                   
                    if action_v > max_v:
                        max_v = action_v
                        best_action = action
                   
                V[state] = max_v
                policy[state] = best_action
                
                delta = max(delta, abs(v - V[state]))

            if delta < error:
                break
        self.end_time = time.process_time()
        self.memory_after = self.get_memory_usage()  
        # trace path
        current_state = self.start
        while current_state != self.maze._goal:
            # print(current_state)
            action = policy[current_state]
            next_state, _ = self.rewards[current_state][action]
            self.solution[current_state] = next_state
            current_state = next_state
        # print('Optimal path:', self.solution)
        
        return V, policy


    def policy_iteration(self, gamma, error=1e-10):
        self.name = 'MDP-Policy Iteration'
        self.iterations = 0
        if not self.rewards:
            self.setupMdp()
        self.start_time = time.process_time()
        self.memory_before = self.get_memory_usage()  
        V = {}
        policy = {}
        all_states = self.maze.maze_map
        for state in all_states:
            V[state] = 0
            policy[state] = 'N' # initialize policy to any action

        while True:
            # policy evaluation step
            while True:
                delta = 0
                for state in all_states:
                    v = V[state]
                    action = policy[state]
                    curret_reward = self.rewards[state][action][1]

                    possible_actions = self.get_possible_action(state, action)
                    action_v = 0
                    for pa in possible_actions:
                        next_state, _ = self.rewards[state][pa]
                        prob = possible_actions[pa]['prob']
                        action_v += (prob*V[next_state])
                    action_v = action_v * gamma + curret_reward
                    V[state] = action_v

                    delta = max(delta, abs(v - V[state]))

                if delta < error:
                    break

            # policy improvement step
            policy_stable = True
            for state in all_states:
                old_action = policy[state]
                max_v = -np.inf
                best_action = 'N' # initialize best action to any action
                for action in self.actions:
                    action_v = 0
                    curret_reward = self.rewards[state][action][1]

                    possible_actions = self.get_possible_action(state, action)
                    for pa in possible_actions:
                        next_state, _ = self.rewards[state][pa]
                        prob = possible_actions[pa]['prob']
                        action_v += (prob*V[next_state])
                    action_v = action_v * gamma + curret_reward

                    if action_v > max_v:
                        max_v = action_v
                        best_action = action

                policy[state] = best_action

                if old_action != best_action:
                    policy_stable = False

            self.iterations += 1
            if policy_stable:
                break

        self.end_time = time.process_time()
        self.memory_after = self.get_memory_usage()  
        # trace path
        current_state = self.start
        while current_state != self.maze._goal:
            # print(current_state)
            action = policy[current_state]
            next_state, _ = self.rewards[current_state][action]
            self.solution[current_state] = next_state
            current_state = next_state
        # print('Optimal path:', self.solution)

        return V, policy
