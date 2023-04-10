from player.MiniMaxPlayer import MiniMaxPlayer
from player.DefaultPlayer import DefaultPlayer
from player.QLearningPlayer import QLearningPlayer
from game.Connect4 import Connect4
import time

def print_result(title, player_x, player_o, xcount, ocount, dcount, battle_numbers, time_cost):
    print(title)
    print("time_cost: %.2fs" % time_cost)
    print(
        'Number of player_x ( %s ) wins = %d, rate: %.2f' % (player_x.name, xcount, xcount * 1.0 / battle_numbers))
    print(
        'Number of player_o ( %s ) wins = %d, rate: %.2f' % (player_o.name, ocount, ocount * 1.0 / battle_numbers))
    print('Number of draw = %d, rate: %.2f' % (dcount, dcount * 1.0 / battle_numbers))

def battle(title, player_x, player_o, battle_numbers):
    xcount = 0
    ocount = 0
    dcount = 0

    start = time.time()
    for x in range(battle_numbers):
        t = Connect4(player_x, player_o)
        result = t.play_game()

        if result == 1:
            xcount += 1
        elif result == -1:
            ocount += 1
        else:
            dcount += 1
    end = time.time()
    print_result(title, player_x, player_o, xcount, ocount, dcount, battle_numbers, end-start)


def train_q_vs_default(save_path):
    train_num = 100000
    player1 = QLearningPlayer(is_first=True, save_path=save_path)
    print("start training")
    start = time.time()
    p2 = DefaultPlayer(is_first=False)
    for i in range(0, train_num):  # Train Qlearning player with another Qlearning player
        if i >= 100 and i % 10000 == 0:
            print("----- epic %d ----" % (i))
        t = Connect4(player1, p2)
        t.play_game()
    player1.save_qtable()
    player1.epsilon = 0
    end = time.time()
    print("end training %.2f" % (end - start))


if __name__ == "__main__":
    battle_times = 100
    # battle("MiniMax VS Default", MiniMaxPlayer(is_first=True), DefaultPlayer(is_first=False), battle_times)
    # battle("Default VS MiniMax", MiniMaxPlayer(is_first=False), DefaultPlayer(is_first=True), battle_times)
    ttt_save_path = './q_vs_default_connect41'
    # train_q_vs_default(ttt_save_path)

    battle("Q-Learning VS Default", QLearningPlayer(is_first=True, save_path=ttt_save_path), DefaultPlayer(is_first=False), battle_times)
    battle("Default VS Q-Learning", QLearningPlayer(is_first=False, save_path=ttt_save_path), DefaultPlayer(is_first=True), battle_times)

    # battle("Q-Learning VS MiniMax", QLearningPlayer(is_first=True, save_path=ttt_save_path),
    #        MiniMaxPlayer(is_first=False), battle_times)
    # battle("MiniMax VS Q-Learning", QLearningPlayer(is_first=False, save_path=ttt_save_path),
    #        MiniMaxPlayer(is_first=True), battle_times)
