'''
    Pathfinding workshop using Depth-First Search (DFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

import sys
import random
from gui_lib import *


class DFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=False, nb_size=4, clever=False, ran_nb=False) -> None:
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        self.nb_size = nb_size
        # search towards target
        self.clever = clever
        # randomise neighbours
        self.ran_nb = ran_nb
        self.showHelp()

    def neighbours2(self, c: Cell):
        n = []
        if self.start.row == self.end.row:
            if self.start.col < self.end.col:
                # log.log('START -> END: east')
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
            elif self.start.col > self.end.col:
                # log.log('START -> END: west')
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
        elif self.start.row < self.end.row:
            if self.start.col <= self.end.col:
                # log.log('START -> END: south/south-east')
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
            elif self.start.col > self.end.col:
                # log.log('START -> END: south-west')
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
        elif self.start.row > self.end.row:
            if self.start.col <= self.end.col:
                # log.log('START -> END: north/north-east')
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
            elif self.start.col > self.end.col:
                # log.log('START -> END: north-west')
                n.append(self.getValidNeighbour(c, 'west'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-west'))
                n.append(self.getValidNeighbour(c, 'north'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'north-east'))
                n.append(self.getValidNeighbour(c, 'east'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-west'))
                n.append(self.getValidNeighbour(c, 'south'))
                if self.nb_size == 8:
                    n.append(self.getValidNeighbour(c, 'south-east'))
        # DFS, so FILO
        n = [x for x in n if x][::-1]
        if self.ran_nb:
            random.shuffle(n)
        return n

    def neighbours(self, c: Cell):
        ''' get the neighbours of the given cell '''
        n = []
        # north
        if c.row > 0 and self.grids[c.row-1][c.col] != CellType.BLOCK:
            n.append(Cell(c.row-1, c.col, c))
        # north east
        if self.nb_size == 8:
            if c.row > 0 and c.col < self.x_grid_num-1 and self.grids[c.row-1][c.col+1] != CellType.BLOCK:
                n.append(Cell(c.row-1, c.col+1, c))
        # east
        if c.col < self.x_grid_num-1 and self.grids[c.row][c.col+1] != CellType.BLOCK:
            n.append(Cell(c.row, c.col+1, c))
        # south east
        if self.nb_size == 8:
            if c.row < self.y_grid_num-1 and c.col < self.x_grid_num-1 and self.grids[c.row+1][c.col+1] != CellType.BLOCK:
                n.append(Cell(c.row+1, c.col+1, c))
        # south
        if c.row < self.y_grid_num-1 and self.grids[c.row+1][c.col] != CellType.BLOCK:
            n.append(Cell(c.row+1, c.col, c))
        # south west
        if self.nb_size == 8:
            if c.row < self.y_grid_num-1 and c.col > 0 and self.grids[c.row+1][c.col-1] != CellType.BLOCK:
                n.append(Cell(c.row+1, c.col-1, c))
        # west
        if c.col > 0 and self.grids[c.row][c.col-1] != CellType.BLOCK:
            n.append(Cell(c.row, c.col-1, c))
        # north west
        if self.nb_size == 8:
            if c.row > 0 and c.col > 0 and self.grids[c.row-1][c.col-1] != CellType.BLOCK:
                n.append(Cell(c.row-1, c.col-1, c))
        # shuffle
        if self.ran_nb:
            random.shuffle(n)
        return n

    def search(self):
        ''' DFS search from start to the end, setup the path list '''
        if not self.start or not self.end or self.y_grid_num == 0 or self.x_grid_num == 0:
            return False
        # to visit
        q = [self.start]
        # visited
        v = []
        # the checking cell
        c = self.start
        while len(q) > 0:
            c = q.pop()
            v.append(c)
            if c == self.end:
                break
            if self.animate and c != self.start:
                self.colourCell(c, 'gray')
                self.update()
            # get neighbours
            nbs = self.neighbours(c)
            if self.clever:
                nbs = self.neighbours2(c)
            [q.append(n) for n in nbs if n not in v and n not in q]
        # backtrack
        if c == self.end:
            self.path = []
            while c.parent:
                self.path.append(c)
                c = c.parent
            self.path.append(self.start)
            # reverse to get from the start to end
        self.path = self.path[::-1]
        return len(self.path) > 0


if __name__ == '__main__':
    clever = False
    randomise_neighbour = False
    if len(sys.argv) > 1:
        if int(sys.argv[1]) == 1:
            clever = True
        elif int(sys.argv[1]) == 2:
            randomise_neighbour = True
    animate = True
    neighbours = 4
    dfs = DFS(
        "COMP712/Pathfinding DFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, clever, randomise_neighbour)
    dfs.setGridNum(40, 30)
    dfs.mainloop()
