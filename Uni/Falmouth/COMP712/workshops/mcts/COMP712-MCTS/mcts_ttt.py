#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np


# ----------------------------------------------------------------
# MOVE CLASS: (x, y, who to play)
# ----------------------------------------------------------------
class Move(object):
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

    def __repr__(self):
        return f'Move (x: {self.x}, y: {self.y}, p: {self.player})'


# ----------------------------------------------------------------
# STATE CLASS: (board, who to play)
# ----------------------------------------------------------------
class State(object):
    x = 1
    o = -1

    def __init__(self, board, next_player=1):
        if len(board.shape) != 2 or board.shape[0] != board.shape[1]:
            raise ValueError("Board must be a 2D square matrix")
        self.board = board
        self.board_size = board.shape[0]
        self.next_player = next_player

    def __str__(self) -> str:
        ''' for printing '''
        return '\n'.join([' '.join(str(int(col)) for col in row) for row in self.board])

    @property
    def winner(self):
        ''' get the winner player (1 for AI, -1 for player, 0 for tie) or None '''
        # get the sum of each row, each column, and 2 diagonals
        col_sum = list(np.sum(self.board, 0))
        row_sum = list(np.sum(self.board, 1))
        diag_main = [self.board.trace()]
        diag_second = [self.board[::-1].trace()]
        # connect them together as a single list
        all_sums = row_sum + col_sum + diag_main + diag_second

        if self.board_size in all_sums:
            return 1
        elif -self.board_size in all_sums:
            return -1
        elif np.all(self.board != 0):
            return 0
        else:
            return None

    def is_valid(self, move):
        ''' check if the specified move is valid '''
        return move.player == self.next_player and \
            0 <= move.x < self.board_size and \
            0 <= move.y < self.board_size and \
            self.board[move.x, move.y] == 0

    def move(self, move):
        ''' make the move '''
        if not self.is_valid(move):
            raise ValueError("cannot play the move " +
                             move + " on board " + str(self.board))
        # make a copy of the current board
        new_board = np.copy(self.board)
        # make the move
        new_board[move.x, move.y] = move.player
        # swap player
        next_player = State.o if move.player == State.x else State.x
        # return the new board after move
        return State(new_board, next_player)

    def get_valid_moves(self):
        ''' all empty cells would be valid '''
        indices = np.where(self.board == 0)
        return [Move(coords[0], coords[1], self.next_player) for coords in list(zip(indices[0], indices[1]))]


# ----------------------------------------------------------------
# NODE CLASS: (state, parent node)
# ----------------------------------------------------------------
class Node(object):
    def __init__(self, state: State, parent=None):
        self.visits_ = 0
        self.results = {1: 0, -1: 0, 0: 0}
        self.state = state
        self.parent = parent
        self.children = []

    def __str__(self) -> str:
        ''' for printing '''
        return str(self.state)

    @property
    def valid_moves(self):
        ''' get all valid moves from current node '''
        if not hasattr(self, 'valid_moves_'):
            self.valid_moves_ = self.state.get_valid_moves()
        return self.valid_moves_

    @property
    def q(self):
        ''' ratio of winning '''
        if not self.parent:
            return 0
        wins = self.results[self.parent.state.next_player]
        loses = self.results[-self.parent.state.next_player]
        return wins - loses

    @property
    def n(self):
        ''' number of visits for current node '''
        return self.visits_

    def is_terminal(self):
        ''' return true if it's a terminal node '''
        return self.state.winner is not None

    def fully_expanded(self):
        ''' check if the current node is fully expanded (no more valid moves) '''
        return len(self.valid_moves) == 0


# ----------------------------------------------------------------
# MCTS class: (Node, Simulation Steps, Parameter C)
# ----------------------------------------------------------------
class MCTS:
    def __init__(self, node: Node, steps=1000, c=1.4):
        ''' build MCTS at given node with steps and param c '''
        self.root = node
        self.steps = steps
        self.c = c

    def UCT_search(self):
        ''' find the best move after simulation '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass

    def tree_policy(self):
        ''' MCTS tree policy that combines selection and expansion process '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass

    def default_policy(self, node):
        ''' random play from the current state '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass

    def back_propagate(self, v, winner):
        ''' back propagation from node v to the root '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass

    def expansion(self, node):
        ''' make expansion from the given node '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass

    def best_child(self, node, c_param):
        ''' find the best child node with best payoff '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------
        pass


# ----------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------


def draw(board):
    ''' draw the current board status with offset '''
    if isinstance(board, State):
        board = board.board
    print("The current board: (X - AI; O - Human)")
    print(' '*19 + ''.join(["{0:4}".format(x) for x in range(len(board))]))
    print(' '*20 + '|' + '-'*11 + '|')
    for i in range(len(board)):
        print("{0:20}".format(i).center(4)+"|", end='')
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print('_'.center(3)+'|', end='')
            if board[i][j] == 1:
                print('X'.center(3)+'|', end='')
            if board[i][j] == -1:
                print('O'.center(3)+'|', end='')
        print()
        print(' '*20 + '|' + '-'*11 + '|')
    print()


def get_action(state):
    ''' get a valid player's move '''
    try:
        print("-----------------------------------")
        location = input("Your move O(row,col): ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 2:
            return -1
        x, y = location
        move = Move(x, y, -1)
    except Exception as e:
        move = -1
        print(f'Exception: {e}')

    if move == -1 or not state.is_valid(move):
        print("[WARNING]:\t invalid move")
        move = get_action(state)
    return move


def game_over(state: State):
    ''' true if game over, if it's an over state, output results '''
    if state.winner is None:
        return False
    if state.winner == 1:
        print("Ops, you LOSE!")
    if state.winner == 0:
        print("Um, it's a TIE!")
    if state.winner == -1:
        print("Yeah, you WIN!")
    return True


def get_ai_move(s1, s2):
    ''' compare 2 game states and extract AI move position (row, col) '''
    if isinstance(s1, Node):
        s1 = s1.state.board
    if isinstance(s2, Node):
        s2 = s2.state.board
    if isinstance(s1, State):
        s1 = s1.board
    if isinstance(s2, State):
        s2 = s2.board
    # find the position with non-zero element, only one can be found
    d = np.where(s2-s1)
    return list(zip(d[0], d[1]))[0]


def clean():
    ''' clean the command window '''
    os_name = platform.system().lower()
    if 'windows' in os_name:
        os.system('cls')
    else:
        os.system('clear')


# ----------------------------------------------------------------
# THE MAIN LOOP
# ----------------------------------------------------------------
if __name__ == "__main__":
    steps, c = 1000, 0

    clean()
    print('AI    player: X')
    print('Human player: O')
    board = np.zeros((3, 3))
    state = State(board=board, next_player=1)

    # main loop
    while not game_over(state):
        # AI move
        state = State(board=board, next_player=1)
        root = Node(state=state, parent=None)
        mcts = MCTS(root, steps=steps, c=c)
        best_move = mcts.UCT_search()

        # reveal AI's move info
        ai_move = get_ai_move(best_move.state, state)
        state = best_move.state

        # update game state
        clean()
        print("___________________________________")
        print(f"AI's move X(row,col): {ai_move[0]},{ai_move[1]}")
        draw(state)
        if game_over(state):
            break

        # player move
        human_move = get_action(state)
        state = state.move(human_move)
        board = state.board

        # update game state
        clean()
        draw(state)
