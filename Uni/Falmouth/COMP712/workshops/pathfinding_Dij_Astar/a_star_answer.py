'''
    Pathfinding workshop using A* Algorithm (Non-Uniform Cost Search)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from math import fabs
import sys
from gui_lib import *
from queue import PriorityQueue


class ASTAR(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=True, nb_size=4, euclidean_dist=False) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
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
        ''' Dijkstra search from start to the end, record the path list '''
        if not self.start or not self.end or self.y_grid_num == 0 or self.x_grid_num == 0:
            return False
        # to visit
        q = PriorityQueue()
        q.put((0, self.start))
        # the moving cost from start to any node
        cost = {(self.start.row, self.start.col): 0}
        while not q.empty():
            # pop up the head cell
            c = q.get()[-1]
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
                # the cost move from c to n
                g_cost = cost[(c.row, c.col)] + self.grids[n.row][n.col]
                t = (n.row, n.col)
                if t not in cost or g_cost < cost[t]:
                    if self.euc_dist:
                        h_cost = self.getGridEuclideanDist2(n, self.end)
                    else:
                        h_cost = self.getGridDist(n, self.end)
                    cost[t] = g_cost
                    q.put((g_cost+h_cost, n))
                    if self.animate:
                        self.animateCell(n, GridColour.TOUCH)
                        self.update()
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
    a_star = ASTAR(
        "COMP712/Pathfinding A* Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, euclidean_dist)
    a_star.setGridNum(40, 30)
    a_star.mainloop()
