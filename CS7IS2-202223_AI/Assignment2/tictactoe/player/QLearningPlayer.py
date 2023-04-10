import os.path
import random
from player.TicTacToePlayer import TicTacToePlayer
import pickle
import os


class QLearningPlayer(TicTacToePlayer):
    def __init__(self, is_first, save_path):
        super().__init__(is_first)
        self.name = 'qlearning'
        self.q_table = {}
        self.epsilon = 0.2
        self.alpha = 0.5
        self.gamma = 0.9
        self.last_state = (' ',) * 9
        self.last_move = None
        self.save_path = save_path
        self.load_qtable()

    def move(self, board):
        actions = self.available_moves(board)
        if random.random() < self.epsilon:
            self.last_move = random.choice(actions)
            self.last_state = tuple(board)
            return self.last_move
        qs = [self.getQ(self.last_state, each) for each in actions]
        maxQ = max(qs)
        if qs.count(maxQ) > 1:
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)
        self.last_move = actions[i]
        self.last_state = tuple(board)
        return self.last_move

    def start_game(self):
        self.last_state = (' ',) * 9
        self.last_move = None

    def getQ(self, state, action):
        if self.q_table.get((state, action)) is None:
            self.q_table[(state, action)] = 1.0

        return self.q_table.get((state, action))

    def save_qtable(self):
        filehandler = open(self.save_path, 'wb')
        pickle.dump(self.q_table, filehandler)

    def load_qtable(self):
        if os.path.exists(self.save_path):
            filehandler = open(self.save_path, 'rb')
            self.q_table = pickle.load(filehandler)
            print("Q Table Size: %d" % len(self.q_table))

    def reward(self, value, board):
        if self.last_move:
            self.learn(self.last_state, self.last_move, value, tuple(board))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max(
            [self.getQ(result_state, a) for a in self.available_moves(state)]
        )
        self.q_table[(state, action)] = prev + \
            self.alpha * ((reward + self.gamma * maxqnew) - prev)


