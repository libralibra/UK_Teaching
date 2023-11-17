#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/lucianzhong/MCTS_demo/blob/master/MCTS_to_play_Tic-Tac-Toe.py

from uu import Error
import numpy as np
from collections import defaultdict


def info(s):
    ''' print information '''
    s = s.strip()
    if s:
        print(f'[INFO   ]: {s}')


def warn(s):
    ''' print out warning information '''
    s = s.strip()
    if s:
        print(f'[WARNING]: {s}')


def error(s):
    ''' print out error information '''
    s = s.strip()
    if s:
        print(f'[ERROR  ]: {s}')


def transpose(m):
    ''' help function to transpose a matrix '''
    return [[m[row][col] for row in range(len(m))] for col in range(len(m[0]))]


def diag(m):
    ''' get the main diagonal of the matrix (top-left to bottom-right) '''
    if len(m) != len(m[0]):
        raise Error(
            f"The matrix must be square, current shape is ({len(m), len(m[0])})")
    return [m[r][r] for r in range(len(m))]


def rot90(m):
    ''' rotate matrix 90 degrees anti-clockwise '''
    return [[m[row][col] for row in range(len(m)-1, -1, -1)] for col in range(len(m[0]))]


def has0(m):
    ''' return true if the matrix has 0 as element(s) '''
    for row in m:
        for col in row:
            if col == 0:
                return True
    return False

# Tic-Tac-Toe game move


class Move(object):
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return "x:" + str(self.x) + " y:" + str(self.y) + " v:" + str(self.value)

# Tic-Tac-Toe game state


class State(object):
    ''' state object: AI = 1, Human = -1, Empty = 0 '''
    x = 1
    o = -1

    def __init__(self, board, next_move=1):
        if len(board.shape) != 2 or board.shape[0] != board.shape[1]:
            raise ValueError(
                f"The board must be a 2D square, current size is {board.shape}")
        self.board = board
        self.board_size = board.shape[0]
        self.next_move = next_move

    def get_winner(self):
        # check if game is over
        # row_sum = np.sum(self.board, 0)
        row_sum = [int(sum(row)) for row in self.board]
        # col_sum = np.sum(self.board, 1)
        col_sum = [int(sum(row)) for row in transpose(self.board)]
        # diag_sum_tl = self.board.trace()
        diag_sum_tl = [sum([int(x) for x in diag(self.board)])]
        # diag_sum_tr = self.board[::-1].trace()
        diag_sum_tr = [sum([int(x) for x in diag(rot90(self.board))])]

        all_sums = row_sum + col_sum + diag_sum_tl + diag_sum_tr

        # if any(row_sum == self.board_size) or any(col_sum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
        if 3 in all_sums:
            return 1
        elif -3 in all_sums:
            return -1
        elif not has0(self.board):
            return 0
        # elif any(row_sum == -self.board_size) or any(col_sum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:
            # return -1
        # elif np.all(self.board != 0):
            # return 0
        else:
            # if not over - no result
            return None

    def is_game_over(self):
        return self.get_winner() != None

    def is_valid_move(self, move):
        # check if correct player moves
        if move.value != self.next_move:
            return False

        # check if inside the board
        x_in_range = move.x < self.board_size and move.x >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y < self.board_size and move.y >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.x, move.y] == 0

    def move(self, move):
        if not self.is_valid_move(move):
            raise ValueError("move " + move + " on board " +
                             self.board + " is not legal")
        new_board = np.copy(self.board)
        new_board[move.x, move.y] = move.value
        next_move = State.o if self.next_move == State.x else State.x
        return State(new_board, next_move)

    def get_valid_moves(self):
        indices = np.where(self.board == 0)
        return [Move(coords[0], coords[1], self.next_move) for coords in list(zip(indices[0], indices[1]))]

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(int(col)) for col in row) for row in self.board])


# Node


class Node(object):
    def __init__(self, state: State, parent=None):
        self.visits_ = 0
        self.results_ = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def valid_moves(self):
        if not hasattr(self, 'valid_moves_'):
            self.valid_moves_ = self.state.get_valid_moves()
        return self.valid_moves_

    @property
    def q(self):
        wins = self.results_[self.parent.state.next_move]
        loses = self.results_[-1 * self.parent.state.next_move]
        return wins - loses

    @property
    def n(self):
        return self.visits_

    def expansion(self):
        action = self.valid_moves.pop()
        next_state = self.state.move(action)
        child_node = Node(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def playout(self):
        ''' Default policy: randomly play the game till terminate state '''
        current_state = self.state
        while not current_state.is_game_over():
            possible_moves = current_state.get_valid_moves()
            action = self.random_move(possible_moves)
            current_state = current_state.move(action)
        return current_state.get_winner()

    def back_propagation(self, result):
        self.visits_ += 1.
        self.results_[result] += 1
        if self.parent:
            self.parent.back_propagation(result)

    def is_fully_expanded(self):
        return len(self.valid_moves) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [(c.q / (c.n)) + c_param *
                           np.sqrt((2 * np.log(self.n) / (c.n))) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def random_move(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
# Node end


# search
class MonteCarloTreeSearch:
    def __init__(self, node: Node):
        self.root = node

    def best_move(self, steps):
        for _ in range(0, steps):
            v = self.selection()
            reward = v.playout()
            v.back_propagation(reward)
        # exploitation only
        return self.root.best_child(c_param=0.)

    def selection(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expansion()
            else:
                current_node = current_node.best_child()
        return current_node
# search end


# run
def init():
    board = np.zeros((3, 3))
    # print("board",board)
    print('AI    player: X')
    print('Human player: O')
    print("_______________________________")
    initial_board_state = State(board=board, next_move=1)
    print("initial_board_state.board")  # all zeros
    print(initial_board_state)

    root = Node(state=initial_board_state, parent=None)
    print("root.state")
    print(root.state)

    mcts = MonteCarloTreeSearch(root)

    best_node = mcts.best_move(1000)

    c_state = best_node.state
    c_board = c_state.board
    # print("c_board",c_board) #c_board [[0. 0. 0.] [0. 1. 0.] [0. 0. 0.]]
    return c_state, c_board

# draw game board


def draw_board(board):
    print("_______________________________")
    print("The current board:")
    print('   '+''.join(["{0:4}".format(x) for x in range(board.shape[0])]))
    for i in range(board.shape[0]):
        print("{0:4}".format(i).center(4)+"|", end='')
        for j in range(board.shape[0]):
            if c_board[i][j] == 0:
                print('_'.center(4), end='')
            if c_board[i][j] == 1:
                print('X'.center(4), end='')
            if c_board[i][j] == -1:
                print('O'.center(4), end='')
        print()
    print()


def get_action(state):
    try:
        location = input("Your move (row,col): ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 2:
            return -1
        x, y = location
        move = Move(x, y, -1)
    except Exception as e:
        move = -1
    if move == -1 or not state.is_valid_move(move):
        print("[WARNING]:\t invalid move")
        move = get_action(state)
    return move


def check(state):
    if state.is_game_over():
        if state.get_winner() == 1:
            print("Ops, you LOSE!")
        if state.get_winner() == 0:
            print("Um, it's a TIE!")
        if state.get_winner() == -1:
            print("Yeah, you WIN!")
        return 1
    else:
        return -1


if __name__ == "__main__":

    c_state, c_board = init()
    # print("c_board",c_board)
    draw_board(c_board)

    # function UCTSEARCH(s0)
    while True:
        move1 = get_action(c_state)
        c_state = c_state.move(move1)
        c_board = c_state.board
        draw_board(c_board)

        board_state = State(board=c_board, next_move=1)
        root = Node(state=board_state, parent=None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_move(1000)
        c_state = best_node.state
        c_board = c_state.board
        draw_board(c_board)
        if check(c_state) == 1:
            break
        elif check(c_state) == -1:
            continue
    # run end
