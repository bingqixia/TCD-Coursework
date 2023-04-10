class Connect4Player(object):
    def __init__(self, is_first):
        self.name = 'human'
        self.player = 1
        self.opponent = -1
        self.is_first = is_first
        self.EMPTY = 0

        self.row_size = 5
        self.column_size = 6
        self.window_length = 4

        self.set_player()

    def start_game(self):
        pass

    def reward(self, value, board):
        pass

    def set_move(self, board, row, col, piece):
        board[row][col] = piece

    def move(self, board):
        return int(input('Your move? '))

    def is_valid_location(self, board, col):
        return board[self.row_size - 1][col] == self.EMPTY

    def get_available_row(self, board, col):
        for r in range(self.row_size):
            if board[r][col] == self.EMPTY:
                return r

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.column_size):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def set_player(self):
        if not self.is_first:
            self.opponent = 1
            self.player = -1

    def available_moves(self, board):
        return [i + 1 for i in range(0, 9) if board[i] == ' ']

    def game_won(self, player, board):

        winning_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for positions in winning_states:
            if all(board[pos] == player for pos in positions):
                return True
        return False