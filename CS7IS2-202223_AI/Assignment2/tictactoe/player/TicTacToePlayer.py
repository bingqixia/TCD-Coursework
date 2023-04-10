class TicTacToePlayer(object):
    def __init__(self, is_first=True):
        self.name = 'human'
        self.player = 'X'
        self.opponent = 'O'
        self.is_first = is_first
        self.set_player()

    def start_game(self):
        pass

    def move(self, board):
        return int(input('Your move? '))

    def set_player(self):
        if not self.is_first:
            self.opponent = 'X'
            self.player = 'O'

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

    def reward(self, value, board):
        pass