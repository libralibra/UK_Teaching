'''
    Pathfinding workshop using Greedy Best-First Search (GBFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

import sys
from gui_lib import *
from queue import PriorityQueue


class GBFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=False, nb_size=4, euclidean_dist=False) -> None:
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        # neighbourhood size
        self.nb_size = nb_size
        # use Euclidean distance rather than Manhattan distance
        self.euc_dist = euclidean_dist
        self.showHelp()

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
        return n

    def search(self):
        ''' DFS search from start to the end, setup the path list '''
        if not self.start or not self.end or self.y_grid_num == 0 or self.x_grid_num == 0:
            return False
        # to visit
        q = PriorityQueue()
        if self.euc_dist:
            q.put((self.getGridEuclideanDist2(self.start, self.end), self.start))
        else:
            q.put((self.getGridDist(self.start, self.end), self.start))
        # item in q
        qlist = [self.start]
        # visited
        v = []
        while not q.empty():
            c = q.get()[-1]
            v.append(c)
            qlist.append(c)
            if c == self.end:
                break
            if self.animate and c != self.start:
                self.animateCell(c)
                self.update()
            # get neighbours and add to PriorityQueue
            for n in self.neighbours(c):
                # early break
                if n == self.end:
                    q.put((0, n))
                    break
                if n in v or n in qlist:
                    continue
                if self.animate:
                    self.colourCell(n, GridColour.TOUCH, 0.8)
                    self.update()
                if self.euc_dist:
                    q.put((self.getGridEuclideanDist2(n, self.end), n))
                    qlist.append(n)
                else:
                    q.put((self.getGridDist(n, self.end), n))
                    qlist.append(n)
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
    euclidean_dist = True
    animate = True
    neighbours = 4
    gbfs = GBFS(
        "COMP712/Pathfinding GBFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, euclidean_dist)
    gbfs.setGridNum(40, 30)
    gbfs.mainloop()
