import numpy as np
import random
from player.Connect4Player import Connect4Player


class MiniMaxPlayer(Connect4Player):

    def __init__(self, is_first):
        super().__init__(is_first)
        self.name = 'minimax'

    def player_wins(self, board, piece):
        # Check horizontal
        for c in range(self.column_size - 3):
            for r in range(self.row_size):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece \
                        and board[r][c + 3] == piece:
                    return True

        # Check vertical
        for c in range(self.column_size):
            for r in range(self.row_size - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and \
                        board[r + 3][c] == piece:
                    return True

        # Check positively sloped
        for c in range(self.column_size - 3):
            for r in range(self.row_size - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped
        for c in range(self.column_size - 3):
            for r in range(3, self.row_size):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.player
        if piece == self.player:
            opp_piece = self.opponent

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.column_size // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.row_size):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.column_size - 3):
                window = row_array[c:c + self.window_length]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.column_size):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row_size - 3):
                window = col_array[r:r + self.window_length]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.row_size - 3):
            for c in range(self.column_size - 3):
                window = [board[r + i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, piece)

        for r in range(self.row_size - 3):
            for c in range(self.column_size - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, piece)

        return score


    def is_terminal_node(self, board):
        return self.player_wins(board, self.player) or self.player_wins(board, self.opponent) or len(
            self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, isMax):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.player_wins(board, self.player):
                    return (None, self.player)
                elif self.player_wins(board, self.opponent):
                    return (None, self.opponent)
                else:  # draw
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, self.player))
        if isMax:
            value = float('-inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row(board, col)
                b_copy = board.copy()
                self.set_move(b_copy, row, col, self.player)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row(board, col)
                b_copy = board.copy()
                self.set_move(b_copy, row, col, self.opponent)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def move(self, board):
        max_depth = 5
        col, minimax_score = self.minimax(board, max_depth, float('-inf'), float('inf'), True)

        if self.is_valid_location(board, col):
            row = self.get_available_row(board, col)
            self.set_move(board, row, col, self.opponent)
            return row, col
