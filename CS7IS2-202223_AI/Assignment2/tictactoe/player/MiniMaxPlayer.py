from player.TicTacToePlayer import TicTacToePlayer
import random


class MiniMaxPlayer(TicTacToePlayer):

    def __init__(self, is_first):
        super().__init__(is_first)
        self.name = 'minimax'

    def move(self, board):
        alpha = float('-inf')
        beta = float('inf')
        depth = 0

        best_value = float('-inf')
        best_move = None

        for move in self.available_moves(board):
            board[move - 1] = self.player
            value = self.min_value(board, alpha, beta, depth + 1)
            board[move - 1] = ' '
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def is_game_over(self, board):
        for a, b, c in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]:

            if self.player == board[a] == board[b] == board[c]:
                return (True, 1)
            elif self.opponent == board[a] == board[b] == board[c]:
                return (True, -1)

        if not any([space == ' ' for space in board]):
            return (True, 0)

        return (False, 0)

    def max_value(self, board, alpha, beta, depth):
        in_terminal_state, utility_value = self.is_game_over(board)
        if in_terminal_state or depth >= 9:
            return utility_value

        value = float('-inf')
        for move in self.available_moves(board):
            board[move - 1] = self.player
            value = max(value, self.min_value(board, alpha, beta, depth + 1))
            board[move - 1] = ' '

            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return value

    def min_value(self, board, alpha, beta, depth):
        in_terminal_state, utility_value = self.is_game_over(board)
        if in_terminal_state or depth >= 9:
            return utility_value

        value = float('inf')
        for move in self.available_moves(board):
            board[move - 1] = self.opponent
            value = min(value, self.max_value(board, alpha, beta, depth + 1))
            board[move - 1] = ' '

            beta = min(beta, value)
            if beta <= alpha:
                break

        return value