#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import numpy as np

# adapt the algorithm from: https://github.com/hrbang/Minimax-algorithm-PY/blob/master/py_version/minimax.py


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
        return '\n'.join([' '.join(str(int(col)) for col in row) for row in self.board])+f'\n Next player: {"X" if self.next_player == State.x else "O"}'

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
        return 0 <= move[0] < self.board_size and \
            0 <= move[1] < self.board_size and \
            self.board[move[0], move[1]] == 0
        return move[-1] == self.next_player and \
            0 <= move[0] < self.board_size and \
            0 <= move[1] < self.board_size and \
            self.board[move[0], move[1]] == 0

    def move(self, move):
        ''' make the move '''
        if not self.is_valid(move):
            raise ValueError("cannot play the move " +
                             str(move) + " on board \n" + str(self.board) + f"\n next player: {self.next_player}")
        # make a copy of the current board
        new_board = np.copy(self.board)
        # make the move
        new_board[move[0], move[1]] = self.next_player
        # swap player
        next_player = State.o if self.next_player == State.x else State.x
        # return the new board after move
        return State(new_board, next_player)

    def undo(self, move):
        if self.board[move[0], move[1]] == 0:
            raise ValueError("undo " + str(move) +
                             " is valid on board " + str(self.board))
        # make a copy of the current board
        new_board = np.copy(self.board)
        # make the move
        new_board[move[0], move[1]] = 0
        # swap player
        next_player = State.o if self.next_player == State.x else State.x
        return State(new_board, next_player)

    def get_valid_moves(self):
        ''' all empty cells would be valid '''
        indices = np.where(self.board == 0)
        return [(coords[0], coords[1], self.next_player) for coords in list(zip(indices[0], indices[1]))]


def minimax(state: State):
    if state.winner is not None:
        return (-1, -1, state.winner)
    good_moves = []
    best_value = -10 if state.next_player == State.x else 10
    for move in state.get_valid_moves():
        state = state.move(move)
        score = minimax(state)
        state = state.undo(move)
        if state.next_player == State.x:
            if score[-1] > best_value:
                best_value = score[-1]
                good_moves = (move[0], move[1], score[-1])
            if best_value > 0:
                break
        elif state.next_player == State.o:
            if score[-1] < best_value:
                best_value = score[-1]
                good_moves = (move[0], move[1], score[-1])
            if best_value < 0:
                break
    return good_moves


# ----------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------


def draw(board):
    ''' draw the current board status with offset '''
    if isinstance(board, State):
        board = board.board
    print("The current board: (X - AI; O - Human)")
    print()
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


def clean():
    ''' clean the command window '''
    os_name = platform.system().lower()
    if 'windows' in os_name:
        os.system('cls')
    else:
        os.system('clear')


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
        move = (x, y, -1)
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


# ----------------------------------------------------------------
# THE MAIN LOOP
# ----------------------------------------------------------------
if __name__ == "__main__":

    clean()
    print('AI    player: X')
    print('Human player: O')
    print('AI is searching, game will start in 2 secs...')
    board = np.zeros((3, 3))

    # main loop
    while True:
        # AI move
        state = State(board=board, next_player=1)
        best_move = minimax(state)
        state = state.move(best_move)

        # update game state
        clean()
        print("___________________________________")
        print(f"AI's move X(row,col): {best_move[0]},{best_move[1]}")
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
        if game_over(state):
            break
