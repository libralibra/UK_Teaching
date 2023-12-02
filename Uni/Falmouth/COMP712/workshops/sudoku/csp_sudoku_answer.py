'''
    COMP712 CSP Workshop: Sudoku Solver using CSP

    Daniel.Zhang @ Falmouth University
    2023-2024
'''
from gui_lib import *
from queue import PriorityQueue


class CSP(Canvas):

    def __init__(self, title, width, height, bgcolour='white', animate=True) -> None:
        super().__init__(title, width, height, bgcolour, animate)

    def hasEmptyCell(self) -> bool:
        for row in self.grids:
            for col in row:
                if col > 0:
                    return True
        return False

    def solve(self) -> bool:
        ''' solving Sudoku via CSP '''
        if not self.hasEmptyCell():
            return True
        self.cspUpdate(self.animate)
        # update queue
        _, d = self.domainUpdate()
        q = PriorityQueue()
        for k, v in d.items():
            q.put((len(v), k))
        # get one: (number, key)
        n, k = q.get()
        if n > 1:
            msgbox('Cannot proceed any more using CSP')
            return False
        c = Cell(k[0], k[1])
        # fill it and update csp
        if self.animate:
            self.animateCell(c, FillColour.GUESS)
        self.grids[c.row][c.col] = d[k][0]
        self.fillCell(c, self.grids[c.row][c.col], True)
        # update the csp
        self.cspUpdate(self.animate)
        return self.solve()


if __name__ == '__main__':
    animate = True
    csp = CSP("COMP712/Sudoku CSP Demo - Falmouth University 2023-2024",
              630, 630, 'white', animate)
    csp.setGridNum(9, 9)
    csp.mainloop()
