from player.TicTacToePlayer import TicTacToePlayer
import random


class DefaultPlayer(TicTacToePlayer):

    def __init__(self, is_first):
        super().__init__(is_first)
        # self.name = 'default'
        self.name = 'default'

    def move(self, board):

        # Check if there's a winning move for the player and make it
        for move in self.available_moves(board):
            new_board = board[:move - 1] + list(self.player) + board[move:]
            if self.game_won(self.player, new_board):
                return move

        # if opponent will win in next turn, block it
        for move in self.available_moves(board):
            new_board = board[:move - 1] + list(self.opponent) + board[move:]
            if self.game_won(self.opponent, new_board):
                return move

        # else choose a random move
        return random.choice(self.available_moves(board))


