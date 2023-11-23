#!/usr/bin/env python
# -*- coding: utf-8 -*-

import turtle
import numpy as np

# adapt the algorithm from: https://github.com/hrbang/Minimax-algorithm-PY/blob/master/py_version/minimax.py


# ----------------------------------------------------------------
# GLOBAL PARAMETERS
# ----------------------------------------------------------------
pen = turtle.Turtle()
pen.hideturtle()
pen.speed('fastest')
board = np.zeros((3, 3))
screen = turtle.Screen()
screen.setup(400, 400)
turtle.title("COMP712/Minimax Demo - Falmouth University 2023-2024")


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

    def move(self, move):
        ''' make the move '''
        if not self.is_valid(move):
            raise ValueError("cannot play the move " +
                             str(move) + " on board " + str(self.board))
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
        # undo the move
        new_board[move[0], move[1]] = 0
        # swap player
        next_player = State.o if self.next_player == State.x else State.x
        return State(new_board, next_player)

    def get_valid_moves(self):
        ''' all empty cells would be valid '''
        indices = np.where(self.board == 0)
        return [(coords[0], coords[1], self.next_player) for coords in list(zip(indices[0], indices[1]))]


# ----------------------------------------------------------------
# MINIMAX ALGORITHM
# ----------------------------------------------------------------
def minimax(state: State):
    ''' minimax algorithm to return the best move from the current state'''
    if state.winner is not None:
        return (-1, -1, state.winner)

    good_move = []
    best_value = -10 if state.next_player == State.x else 10
    for move in state.get_valid_moves():
        state = state.move(move)
        score = minimax(state)
        state = state.undo(move)
        if state.next_player == State.x:
            if score[-1] > best_value:
                best_value = score[-1]
                good_move = (move[0], move[1], score[-1])
            if best_value > 0:
                break
        elif state.next_player == State.o:
            if score[-1] < best_value:
                best_value = score[-1]
                good_move = (move[0], move[1], score[-1])
            if best_value < 0:
                break
    return good_move


# ----------------------------------------------------------------
# MAIN GAME PLAY PROCESS
# ----------------------------------------------------------------


def game_play(x, y):
    ''' main logic here, player plays first '''
    global board

    # player move
    r, c = get_mat_index(x, y)
    state = State(board=board, next_player=State.o)
    state = state.move((r, c, State.o))
    board = state.board
    ui_update(state)

    if game_over(state):
        return

    # AI move
    best_move = minimax(state)
    state = state.move(best_move)
    board = state.board
    ui_update(state)

    print("___________________________________")
    print(f"AI's move X(row,col): {best_move[0]},{best_move[1]}")

    if game_over(state):
        return


# ----------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------
def game_over(state: State):
    ''' true if game over, if it's an over state, output results '''
    if state.winner is None:
        return False

    if state.winner == 1:
        s = "Ops, you LOSE!"
    elif state.winner == 0:
        s = "Um, it's a TIE!"
    elif state.winner == -1:
        s = "Yeah, you WIN!"
    msgbox(s, 'Game Over:')
    turtle.exitonclick()
    return True


def msgbox(s, t=''):
    ''' show a modal message box '''
    if s.strip():
        turtle.TK.messagebox.showinfo(
            title=t, message=s.strip())


def draw_line(p1, p2, color, size=5):
    ''' draw a line from p1 to p2 '''
    pen.pensize(size)
    pen.pencolor(color)
    pen.up()
    pen.goto(p1)
    pen.down()
    pen.goto(p2)


def draw_circle(c1, r1, color='red'):
    # global pen
    pen.up()
    pen.color(color)
    pen.goto(c1)
    pen.dot(r1, color)


def draw_square(c1, r1, color='blue'):
    ''' draw a filled square with center c1 and size r1 '''
    cx = c1[0]-r1/2+5
    cy = c1[1]+r1/2-5
    pen.up()
    pen.goto(cx, cy)
    pen.down()
    pen.color(color)
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(4):
        pen.forward(r1-10)
        pen.right(90)
    pen.end_fill()


def ui_init(ui_size=300):
    ''' initialisation of the board '''
    s = ui_size/3
    hs = s/2
    screen.clear()
    screen.bgcolor("white")
    draw_line((-hs, -s-hs), (-hs, s+hs), 'black', 5)
    draw_line((hs, -s-hs), (hs, s+hs), 'black', 5)
    draw_line((-s-hs, -hs), (s+hs, -hs), 'black', 5)
    draw_line((-s-hs, hs), (s+hs, hs), 'black', 5)
    draw_line((-hs, -s-hs), (-hs, s+hs), 'black', 5)
    screen.tracer(False)


def get_ui_pos(row, col, ui_size=300):
    ''' convert matrix index to screen position of the block center '''
    s = ui_size/3
    return ((col-1)*s, (2-row-1)*s)


def get_mat_index(x, y, ui_size=300):
    ''' convert screen position to matrix indices '''
    s = ui_size/3
    r = y < -s/2 and 2 or (y <= s/2 and 1 or 0)
    c = x > s/2 and 2 or (x >= -s/2 and 1 or 0)
    return (r, c)


def ui_update(state, size=300):
    ''' update ui with the current state '''
    turtle.update()
    for i in range(state.board.shape[0]):
        for j in range(state.board.shape[1]):
            pos = get_ui_pos(i, j, size)
            if state.board[i, j] == 1:
                draw_square(pos, size/3-10, 'blue')
            elif state.board[i, j] == -1:
                draw_circle(pos, size/3-5, 'red')
                draw_circle(pos, size/3-20, 'white')


# ----------------------------------------------------------------
# THE MAIN LOOP
# ----------------------------------------------------------------
if __name__ == "__main__":
    ui_init()
    turtle.onscreenclick(game_play)
    turtle.mainloop()
    turtle.done()
