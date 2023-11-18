"""
author: arrti
github: https://github.com/arrti
blog:   http://www.cnblogs.com/xmwd
"""

# https://github.com/arrti/mcts/blob/master/n_in_row_uct_rave.py

import copy
import time
from random import choice, shuffle
from math import log, sqrt


class Board(object):
    """
    board for game
    """

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))
        self.states = {}  # board states, key:move, value: player as piece type
        # need how many pieces in a row to win
        self.n_in_row = int(kwargs.get('n_in_row', 5))

    def init_board(self):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception(
                'board width and height can not less than %d' % self.n_in_row)

        self.valid_moves = list(
            range(self.width * self.height))  # available moves

        self.states = {}  # key:move as location on the board, value:player as pieces type

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if (len(location) != 2):
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if (move not in range(self.width * self.height)):
            return -1
        return move

    def update(self, player, move):
        self.states[move] = player
        self.valid_moves.remove(move)

    def current_state(self):
        # for hash
        return tuple((m, self.states[m]) for m in sorted(self.states))


class MCTS(object):
    """
    AI player, UCT RAVE
    """

    def __init__(self, board, play_turn, n_in_row=5, time=5, max_actions=1000):
        self.board = board
        self.play_turn = play_turn
        self.calculation_time = float(time)
        self.max_actions = max_actions
        self.n_in_row = n_in_row

        self.player = play_turn[0]  # AI is first at now
        self.confident = 1.96
        self.equivalence = 1000
        self.max_depth = 1

        self.plays = {}      # key:(action, state), value:visited times
        self.wins = {}       # key:(action, state), value:win times
        self.plays_rave = {}  # key:(move, state), value:visited times
        self.wins_rave = {}  # key:(move, state), value:{player: win times}

    def get_action(self):
        if len(self.board.valid_moves) == 1:
            return self.board.valid_moves[0]

        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            # while simulations < 10000: # need many simulations for a better selection
            # simulation will change board's states,
            board_copy = copy.deepcopy(self.board)
            play_turn_copy = copy.deepcopy(self.play_turn)  # and play turn
            self.run_simulation(board_copy, play_turn_copy)
            simulations += 1

        print("total simulations=", simulations)

        move = self.select_one_move()
        location = self.board.move_to_location(move)
        print('Maximum depth searched:', self.max_depth)

        print("AI move: %d,%d\n" % (location[0], location[1]))

        self.prune()

        return move

    def run_simulation(self, board, play_turn):
        """
        UCT RAVE main process
        """

        plays = self.plays
        wins = self.wins
        plays_rave = self.plays_rave
        wins_rave = self.wins_rave
        valid_moves = board.valid_moves

        player = self.get_player(play_turn)
        visited_states = set()
        winner = -1
        expand = True
        states_list = []
        # Simulation
        for t in range(1, self.max_actions + 1):
            # Selection
            # if all moves have statistics info, choose one that have max UCB value
            state = board.current_state()
            actions = [(move, player) for move in valid_moves]
            if all(plays.get((action, state)) for action in actions):
                total = 0
                for a, s in plays:
                    if s == state:
                        total += plays.get((a, s))  # N(s)
                beta = self.equivalence/(3 * total + self.equivalence)

                value, action = max(
                    ((1 - beta) * (wins[(action, state)] / plays[(action, state)]) +
                     beta * (wins_rave[(action[0], state)][player] / plays_rave[(action[0], state)]) +
                     sqrt(self.confident * log(total) / plays[(action, state)]), action)
                    for action in actions)   # UCT RAVE

            else:
                # a simple strategy
                # prefer to choose the nearer moves without statistics,
                # and then the farthers.
                # try ro add statistics info to all moves quickly
                # adjacents = []
                # if len(valid_moves) > self.n_in_row:
                #     adjacents = self.adjacent_moves(board, state, player, plays)

                # if len(adjacents):
                #     action = (choice(adjacents), player)
                # else:
                #     peripherals = []
                #     for action in actions:
                #         if not plays.get((action, state)):
                #             peripherals.append(action)
                #     action = choice(peripherals)
                action = choice(actions)

            move, p = action
            board.update(player, move)

            # Expand
            # add only one new child node each time
            if expand and (action, state) not in plays:
                expand = False
                plays[(action, state)] = 0
                wins[(action, state)] = 0

                if t > self.max_depth:
                    self.max_depth = t

            # states in one simulation by order of visited
            states_list.append((action, state))
            # for i, (m_root, s_root) in enumerate(states_list):
            #     for (m_sub, s_sub) in states_list[i:]:
            #         if (m_sub, s_root) not in plays_rave:
            #             plays_rave[(m_sub, s_root)] = 0
            #             wins_rave[(m_sub, s_root)] = {}
            #             for p in self.play_turn:
            #                 wins_rave[(m_sub, s_root)][p] = 0

            # AMAF value
            # next (action, state) is child node of all previous (action, state) nodes
            for (m, pp), s in states_list:
                if (move, s) not in plays_rave:
                    plays_rave[(move, s)] = 0
                    wins_rave[(move, s)] = {}
                    for p in self.play_turn:
                        wins_rave[(move, s)][p] = 0

            visited_states.add((action, state))

            is_full = not len(valid_moves)
            win, winner = self.has_a_winner(board)
            if is_full or win:
                break

            player = self.get_player(play_turn)

        # Back-propagation
        for i, ((m_root, p), s_root) in enumerate(states_list):
            action = (m_root, p)
            if (action, s_root) in plays:
                plays[(action, s_root)] += 1  # all visited moves
                if player == winner and player in action:
                    wins[(action, s_root)] += 1  # only winner's moves

            for ((m_sub, p), s_sub) in states_list[i:]:
                plays_rave[(m_sub, s_root)] += 1  # all child nodes of s_root
                if winner in wins_rave[(m_sub, s_root)]:
                    # each node is divided by the player
                    wins_rave[(m_sub, s_root)][winner] += 1

    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p

    def select_one_move(self):
        """
        select by win percentage 
        """
        percent_wins, move = max(
            (self.wins.get(((move, self.player), self.board.current_state()), 0) /
             self.plays.get(
                 ((move, self.player), self.board.current_state()), 1),
             move)
            for move in self.board.valid_moves)

        # display the statistics for each possible play,
        # first is MC value, second is AMAF value
        for x in sorted(
                ((100 * self.wins.get(((move, self.player), self.board.current_state()), 0) /
                  self.plays.get(
                      ((move, self.player), self.board.current_state()), 1),
                  100 * self.wins_rave.get((move, self.board.current_state()), {}).get(self.player, 0) /
                  self.plays_rave.get((move, self.board.current_state()), 1),
                  self.wins.get(
                      ((move, self.player), self.board.current_state()), 0),
                  self.plays.get(
                      ((move, self.player), self.board.current_state()), 1),
                  self.wins_rave.get((move, self.board.current_state()), {}).get(
                      self.player, 0),
                  self.plays_rave.get((move, self.board.current_state()), 1),
                  self.board.move_to_location(move))
                 for move in self.board.valid_moves),
                reverse=True):
            print('{6}: {0:.2f}%--{1:.2f}% ({2} / {3})--({4} / {5})'.format(*x))

        return move

    def adjacent_moves(self, board, state, player, plays):
        """
        adjacent moves without statistics info
        """
        moved = list(set(range(board.width * board.height)) -
                     set(board.valid_moves))
        adjacents = set()
        width = board.width
        height = board.height

        for m in moved:
            h = m // width
            w = m % width
            if w < width - 1:
                adjacents.add(m + 1)  # right
            if w > 0:
                adjacents.add(m - 1)  # left
            if h < height - 1:
                adjacents.add(m + width)  # upper
            if h > 0:
                adjacents.add(m - width)  # lower
            if w < width - 1 and h < height - 1:
                adjacents.add(m + width + 1)  # upper right
            if w > 0 and h < height - 1:
                adjacents.add(m + width - 1)  # upper left
            if w < width - 1 and h > 0:
                adjacents.add(m - width + 1)  # lower right
            if w > 0 and h > 0:
                adjacents.add(m - width - 1)  # lower left

        adjacents = list(set(adjacents) - set(moved))
        for move in adjacents:
            if plays.get(((move, player), state)):
                adjacents.remove(move)
        return adjacents

    def prune(self):
        """
        remove not selected path
        """
        length = len(self.board.states)
        keys = list(self.plays)
        for a, s in keys:
            if len(s) < length + 2:
                del self.plays[(a, s)]
                del self.wins[(a, s)]

        keys = list(self.plays_rave)
        for m, s in keys:
            if len(s) < length + 2:
                del self.plays_rave[(m, s)]
                del self.wins_rave[(m, s)]

    def has_a_winner(self, board):
        moved = list(set(range(board.width * board.height)) -
                     set(board.valid_moves))
        if (len(moved) < self.n_in_row + 2):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = self.n_in_row
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def __str__(self):
        return "AI"


class Human(object):
    """
    human player
    """

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_action(self):
        try:
            location = [int(n, 10) for n in input("Your move: ").split(",")]
            move = self.board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in self.board.valid_moves:
            print("invalid move")
            move = self.get_action()
        return move

    def __str__(self):
        return "Human"


class Game(object):
    """
    game server
    """

    def __init__(self, board, **kwargs):
        self.board = board
        self.player = [1, 2]  # player1 and player2
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.time = float(kwargs.get('time', 2))
        self.max_actions = int(kwargs.get('max_actions', 100))

    def start(self):
        p1, p2 = self.init_player()
        self.board.init_board()

        ai = MCTS(self.board, [p1, p2], self.n_in_row,
                  self.time, self.max_actions)
        human = Human(self.board, p2)
        players = {}
        players[p1] = ai
        players[p2] = human
        turn = [p1, p2]
        shuffle(turn)
        self.graphic(self.board, human, ai)
        while (1):
            p = turn.pop(0)
            turn.append(p)
            player_in_turn = players[p]
            move = player_in_turn.get_action()
            self.board.update(p, move)
            self.graphic(self.board, human, ai)
            end, winner = self.game_end(ai)
            if end:
                if winner != -1:
                    print("Game end. Winner is", players[winner])
                break

    def init_player(self):
        plist = list(range(len(self.player)))
        index1 = choice(plist)
        plist.remove(index1)
        index2 = choice(plist)

        return self.player[index1], self.player[index2]

    def game_end(self, ai):
        win, winner = ai.has_a_winner(self.board)
        if win:
            return True, winner
        elif not len(self.board.valid_moves):
            print("Game end. Tie")
            return True, -1
        return False, -1

    def graphic(self, board, human, ai):
        """
        Draw the board and show game info
        """
        width = board.width
        height = board.height

        print("Human Player", human.player, "with X".rjust(3))
        print("AI    Player", ai.player, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == human.player:
                    print('X'.center(8), end='')
                elif p == ai.player:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')


def run():
    n = 4
    try:
        board = Board(width=5, height=5, n_in_row=n)
        game = Game(board, n_in_row=n, time=3)  # more time better
        game.start()
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
