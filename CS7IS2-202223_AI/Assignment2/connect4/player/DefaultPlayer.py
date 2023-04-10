from player.Connect4Player import Connect4Player
import random
# set Default as second player


class DefaultPlayer(Connect4Player):
    def __init__(self, is_first):
        super().__init__(is_first)
        self.name = 'default'
        self.column_size = 6
        self.row_size = 5

    def available_moves(self, board):
        valid_locations = []
        for col in range(self.column_size):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def is_valid_location(self, board, col):
        return board[self.row_size - 1][col] == 0

    def move(self, board):
        # Check if there's a winning move for the opponent and block it
        for col in self.available_moves(board):
            row = self.get_available_row(board, col)
            b_copy = board.copy()
            self.set_move(b_copy, row, col, self.opponent)
            if self.game_won(b_copy, self.opponent):
                return row, col

        # Check if there's a winning move for the player and make it
        for col in self.available_moves(board):
            row = self.get_available_row(board, col)
            b_copy = board.copy()
            self.set_move(b_copy, row, col, self.player)
            if self.game_won(b_copy, self.player):
                return row, col

        # If no winning move for the player or the opponent, choose a random move
        column = random.choice(self.available_moves(board))
        row = self.get_available_row(board, column)
        return row, column

    def reward(self, value, board):
        pass

    def game_won(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.column_size - 3):
            for r in range(self.row_size):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_size):
            for r in range(self.row_size - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.column_size - 3):
            for r in range(self.row_size - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.column_size - 3):
            for r in range(3, self.row_size):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True
