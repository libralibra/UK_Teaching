'''
    Pathfinding workshop using Dijkstra's Algorithm (Uniform Cost Search)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from gui_lib import *
from queue import PriorityQueue


class DIJKSTRA(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=True, nb_size=4) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        # neighbourhood size
        self.nb_size = nb_size
        # neighbourhood size
        self.nb_size = nb_size
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
        # initialise the cost dict
        cost = {(row, col): self.y_grid_num*self.x_grid_num
                for row in range(self.y_grid_num) for col in range(self.x_grid_num)}
        # to visit
        q = PriorityQueue()
        q.put((0, self.start))
        # mark items in q, list is ok, but dict can check existence very quickly
        # 1 for valid, 0 for excluded
        qdict = {(self.start.row, self.start.col): 1}
        # the moving cost from start to any node
        cost[(self.start.row, self.start.col)] = 0
        while not q.empty():
            # pop up the head cell
            c = q.get()[-1]
            qdict[(c.row, c.col)] = -1
            if c == self.end:
                break
            if self.animate and c != self.start:
                self.animateCell(c)
                self.update()
            # get neighbours and add to PriorityQueue
            for n in self.neighbours(c):
                # the cost move from c to n
                new_cost = cost[(c.row, c.col)] + self.grids[n.row][n.col]
                # not in the queue, added
                if (n.row, n.col) not in qdict:
                    q.put((new_cost, n))
                    qdict[(n.row, n.col)] = 1
                    cost[(n.row, n.col)] = new_cost
                # in the queue, cost was saved before, update the cost
                elif new_cost < cost[(n.row, n.col)]:
                    cost[(n.row, n.col)] = new_cost
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
    animate = True
    neighbours = 4
    dijkstra = DIJKSTRA(
        "COMP712/Pathfinding Dijkstra Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours)
    dijkstra.setGridNum(40, 30)
    dijkstra.mainloop()
