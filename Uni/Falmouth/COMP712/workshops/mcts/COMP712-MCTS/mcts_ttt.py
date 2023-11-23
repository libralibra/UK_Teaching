#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import turtle

# ----------------------------------------------------------------
# GLOBAL PARAMETERS
# ----------------------------------------------------------------
pen = turtle.Turtle()
pen.hideturtle()
pen.speed('fastest')
board = np.zeros((3, 3))
screen = turtle.Screen()
screen.setup(400, 400)
turtle.title("COMP712/MCTS Demo - Falmouth University 2023-2024")

# ----------------------------------------------------------------
# MOVE CLASS: (x, y, who to play)
# ----------------------------------------------------------------


class Move(object):
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

    def __str__(self):
        return f'Move (x: {self.x}, y: {self.y}, p: {self.player})'


# ----------------------------------------------------------------
# STATE CLASS: (board, who to play)
# ----------------------------------------------------------------
class State(object):
    x = 1
    o = -1

    def __init__(self, board, next_player=1, win_num=3):
        if len(board.shape) != 2 or board.shape[0] != board.shape[1]:
            raise ValueError("Board must be a 2D square matrix")
        self.board = board
        self.board_size = board.shape[0]
        self.win_num = win_num
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

        if self.win_num in all_sums:
            return 1
        elif -self.win_num in all_sums:
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
                             move + " on board " + self.board)
        # make a copy of the current board
        new_board = np.copy(self.board)
        # make the move
        new_board[move.x, move.y] = move.player
        # swap player
        next_player = State.o if self.next_player == State.x else State.x
        # return the new board after move
        return State(new_board, next_player, self.win_num)

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

    def expansion(self, node):
        ''' make expansion from the given node '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------

    def best_child(self, node, c_param):
        ''' find the best child node with best payoff '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------

    def tree_policy(self):
        ''' MCTS tree policy that combines selection and expansion process '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------

    def default_policy(self, node):
        ''' random play from the current state '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------

    def back_propagate(self, v, winner):
        ''' back propagation from node v to the root '''
        # ---------------------------------------------------
        # YOUR CODE HERE
        # ---------------------------------------------------


# ----------------------------------------------------------------
# MAIN GAME PLAY PROCESS
# ----------------------------------------------------------------
def game_play(x, y):
    ''' main logic here, player plays first '''
    global board

    # player move
    r, c = get_mat_index(x, y)
    state = State(board=board, next_player=State.o)
    state = state.move(Move(r, c, State.o))
    board = state.board
    ui_update(state)

    if game_over(state):
        return

    # AI move
    state = State(board=board, next_player=State.x, win_num=win_num)
    root = Node(state=state, parent=None)
    mcts = MCTS(root, steps=steps, c=c)
    best_move = mcts.UCT_search()

    # AI move
    ai_move = get_ai_move(best_move.state, state)
    state = best_move.state
    board = state.board
    ui_update(state)

    print("___________________________________")
    print(f"AI's move X(row,col): {ai_move[0]},{ai_move[1]}")

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


# ----------------------------------------------------------------
# THE MAIN LOOP
# ----------------------------------------------------------------
if __name__ == "__main__":
    steps, c = 1000, 0
    bd_size, win_num = 3, 3
    board = np.zeros((bd_size, bd_size))
    state = State(board=board, next_player=1, win_num=win_num)

    ui_init()
    turtle.onscreenclick(game_play)
    turtle.mainloop()
    turtle.done()
