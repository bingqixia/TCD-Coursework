import numpy as np

class Connect4(object):
    def __init__(self, player_x, player_o):
        self.row_size = 5
        self.column_size = 6
        self.window_length = 4

        self.player_x, self.player_o = player_x, player_o

        self.PLAYER_PIECE = 1
        self.OPPONENT_PIECE = -1
        self.EMPTY = 0

        self.player_x_turn = True

        self.board = self.create_board()

    def create_board(self):
        board = np.zeros((self.row_size, self.column_size))
        return board

    def set_move(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.row_size - 1][col] == 0

    def get_available_row(self, col):
        # return first available row
        for r in range(self.row_size):
            if self.board[r][col] == 0:
                return r

    def draw_board(self):
        print(np.flip(self.board, 0))

    def player_wins(self, piece):
        # Check vertical
        for c in range(self.column_size):
            for r in range(self.row_size - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped
        for c in range(self.column_size - 3):
            for r in range(self.row_size - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and \
                        self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped
        for c in range(self.column_size - 3):
            for r in range(3, self.row_size):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and \
                        self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

        # Check horizontal locations for win
        for c in range(self.column_size - 3):
            for r in range(self.row_size):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][c + 3] == piece:
                    return True

    def is_terminal_node(self):
        return self.player_wins(self.PLAYER_PIECE) or self.player_wins(self.OPPONENT_PIECE) or len(
            self.get_valid_locations()) == 0

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.column_size):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def play_game(self, train=True):
        if not train:
            print('\nNew game!')
            print('Play 1: X, Player 2: O')

        while True:
            if self.player_x_turn:
                player, piece, other_player = self.player_x, self.PLAYER_PIECE, self.player_o
            else:
                player, piece, other_player = self.player_o, self.OPPONENT_PIECE, self.player_x

            move = player.move(self.board)
            self.set_move(move[0], move[1], piece)

            if self.player_wins(piece):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                if piece == self.PLAYER_PIECE:
                    if not train:
                        print("X wins!")
                    return 1
                elif piece == self.OPPONENT_PIECE:
                    if not train:
                        print("O wins!")
                    return -1

            if len(self.get_valid_locations()) == 0:
                player.reward(0.5, self.board)
                other_player.reward(0.5, self.board)
                if not train:
                    print('Draw!')
                return 0

            self.player_x_turn = not self.player_x_turn