import random


class TicTacToe:
    def __init__(self, player_x, player_o):
        self.board = [' '] * 9
        self.player_x, self.player_o = player_x, player_o
        self.player_x_turn = True

    def draw_board(self):
        # reuse board
        print('     |     |     ')
        print('  %s  |  %s  |  %s  ' % (self.board[0],\
                                        self.board[1],\
                                        self.board[2]))
        print('_____|_____|_____')
        print('     |     |     ')
        print('  %s  |  %s  |  %s  ' % (self.board[3],\
                                        self.board[4],\
                                        self.board[5]))
        print('_____|_____|_____')
        print('     |     |     ')
        print('  %s  |  %s  |  %s  ' % (self.board[6],\
                                        self.board[7],\
                                        self.board[8]))
        print('     |     |     ')

    def is_board_full(self):
        return not any([space == ' ' for space in self.board])

    def play_game(self, train=True):
        if not train:
            print('\nNew game!')
            print('Play 1: X, Player 2: O')

        self.player_x.start_game()
        self.player_o.start_game()
        while True:
            if self.player_x_turn:
                player, char, other_player = self.player_x, 'X', self.player_o
            else:
                player, char, other_player = self.player_o, 'O', self.player_x

            if other_player.name == "human":
                self.draw_board()

            move = player.move(self.board)
            self.board[move - 1] = char

            if self.player_wins(char):
                player.reward(1, self.board)
                other_player.reward(-1, self.board)
                if not train:
                    self.draw_board()
                    print(char + ' wins!')
                if char == 'X':
                    return 1
                else:
                    return -1

            if self.is_board_full():
                player.reward(0.5, self.board)
                other_player.reward(0.5, self.board)
                if not train:
                    self.draw_board()
                    print('Draw!')
                return 0

            other_player.reward(0, self.board)
            self.player_x_turn = not self.player_x_turn

    def player_wins(self, char):
        winner_states = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]
        for i, j, k in winner_states:
            if char == self.board[i] == self.board[j] == self.board[k]:
                return True
        return False