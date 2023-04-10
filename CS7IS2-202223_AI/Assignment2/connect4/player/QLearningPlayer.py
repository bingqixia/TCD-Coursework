import numpy as np
import random
from player.Connect4Player import Connect4Player
import pickle
import os


class QLearningPlayer(Connect4Player):
    def __init__(self, is_first, save_path):
        super().__init__(is_first)
        self.name = 'qlearning'
        self.q_table = {}
        # learning rate
        self.alpha = 0.5
        self.epsilon = 0.5
        self.gamma = 0.9  # discount factor
        self.last_state = np.zeros((self.row_size, self.column_size))
        self.last_move = None
        self.save_path = save_path
        self.load_qtable()

    def save_qtable(self):
        filehandler = open(self.save_path, 'wb')
        pickle.dump(self.q_table, filehandler)

    def load_qtable(self):
        if os.path.exists(self.save_path):
            filehandler = open(self.save_path, 'rb')
            self.q_table = pickle.load(filehandler)
            print("Q Table Size: %d" % len(self.q_table))

    def start_game(self):
        self.last_state = np.zeros((self.row_size, self.column_size))
        self.last_move = None

    def tuple_state(self, state):
        return tuple(map(tuple, state))

    def getQ(self, state, action):
        state = self.tuple_state(state)
        if self.q_table.get((state, action)) is None:
            self.q_table[(state, action)] = 1.0  # Initial all q as 1

        return self.q_table.get((state, action))

    def move(self, board):
        actions = self.get_valid_locations(board)

        if random.random() < self.epsilon:  # To balance exploration and exploitation
            col = random.choice(actions)
            row = self.get_available_row(board, col)
            self.last_move = row, col
            self.last_state = self.tuple_state(board)
            return self.last_move

        qs = [self.getQ(self.last_state, each) for each in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        col = actions[i]
        row = self.get_available_row(board, col)
        self.last_move = row, col
        self.last_state = self.tuple_state(board)

        return self.last_move

    def reward(self, value, board):
        if self.last_move:
            self.learn(self.last_state, self.last_move, value, self.tuple_state(board))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max(
            [self.getQ(result_state, a) for a in self.get_valid_locations(state)]
        )
        self.q_table[(state, action)] = prev + \
                                  self.alpha * ((reward + self.gamma * maxqnew) - prev)
