#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

# https://stackoverflow.com/questions/57479512/check-manually-the-number-of-tic-tac-toe-states#:~:text=The%20total%20number%20of%20states%20is%203%5E9%20%283,%28ie%20not%20stopping%20playing%20if%20a%20player%20wins%29


class GameIsFinishedError(Exception):
    pass


class NonEmptyTileError(Exception):
    pass


class OutOfBoundsError(Exception):
    pass


class Board:

    CROSS = "X"
    CIRCLE = "O"

    def __init__(self, board_size):
        self.board_size = board_size
        self.tiles = [[None for _ in range(0, self.board_size)]
                      for _ in range(0, self.board_size)]
        self.moves = {self.CROSS: [], self.CIRCLE: []}
        self.turn = 1

    def play(self, x, y):
        if x >= self.board_size or y >= self.board_size:
            raise OutOfBoundsError()

        if self.game_has_ended:
            raise GameIsFinishedError()

        tile_value = self.CROSS if self.turn % 2 == 1 else self.CIRCLE

        if self.tiles[x][y] is not None:
            raise NonEmptyTileError(f"Tile ({x},{y}) is not empty")

        self.tiles[x][y] = tile_value
        self.moves[tile_value].append((x, y))
        self.turn += 1

    @property
    def board_is_full(self):
        return all(tile is not None for row in self.tiles for tile in row)

    @property
    def someone_won(self):
        # Get values in diagonals
        diag1 = []
        diag2 = []
        for i in range(0, self.board_size):
            diag1.append(self.tiles[i][i])
            diag2.append(self.tiles[self.board_size - i - 1][i])

        for player in (self.CIRCLE, self.CROSS):
            # Check rows
            for row in self.tiles:
                if all(tile == player for tile in row):
                    return player

            # Check columns
            for col in zip(*self.tiles):
                if all(tile == player for tile in col):
                    return player

            # Check diagonals
            if all(tile == player for tile in diag1) or all(tile == player for tile in diag2):
                return player

        return False

    @property
    def possible_moves(self):
        res = []
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile is None:
                    res.append((i, j))
        return res

    @property
    def game_has_ended(self):
        return self.board_is_full or self.someone_won

    def print_board(self):
        for i, row in enumerate(self.tiles):
            row = [elem if elem is not None else " " for elem in row]
            row_str = " " + " | ".join(row) + " "
            print(row_str)
            if i != self.board_size - 1:
                print("-" * (self.board_size * 3) +
                      "-" * (self.board_size - 1))
        print()

    def copy_board(self):
        return deepcopy(self)

###################################################################################################


class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent

    def children(self):
        for x, y in self.board.possible_moves:
            new_board = self.board.copy_board()
            new_board.play(x, y)
            yield self.__class__(new_board, parent=self)

###################################################################################################


class Tree:

    UNIQUE_GAME_COUNTER = 0

    def __init__(self, root):
        self.root = root

    @classmethod
    def step(cls, node):

        if node.board.game_has_ended:
            cls.UNIQUE_GAME_COUNTER += 1
            return

        for child in node.children():
            cls.step(child)

    def browse(self):
        self.step(self.root)


###################################################################################################
#                                            MAIN                                                 #
###################################################################################################
if __name__ == '__main__':

    b = Board(3)
    root = Node(b)
    tree = Tree(root)
    tree.browse()
    print(tree.UNIQUE_GAME_COUNTER)
