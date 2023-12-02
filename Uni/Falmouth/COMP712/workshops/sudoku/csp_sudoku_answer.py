'''
    COMP712 CSP Workshop: Sudoku Solver using CSP

    Daniel.Zhang @ Falmouth University
    2023-2024
'''
from gui_lib import *


class CSP(Canvas):

    def __init__(self, title, width, height, bgcolour='white', animate=True, backtrack=True) -> None:
        super().__init__(title, width, height, bgcolour, animate)
        self.backtrack = backtrack

    def hasEmptyCell(self) -> bool:
        for row in self.grids:
            for col in row:
                if col > 0:
                    return True
        return False

    def domainUpdate(self):
        ''' update domains, return 
            ck: list of (row,col) where self.grids[row][col] is fixed
            d: dict of (row,col)->list of possible values for empty cell
        '''
        d = {}
        for row in range(9):
            for col in range(9):
                if self.grids[row][col] == 0:
                    if self.animate:
                        self.animateCell(Cell(row, col), FillColour.GUESS)
                    else:
                        self.clearCell(Cell(row, col), True)
                    rows = self.getRow(row)
                    cols = self.getCol(col)
                    subs = self.getSubGrid(row, col)
                    nums = rows+cols+subs
                    d[(row, col)] = [x for x in range(1, 10) if x not in nums]
                    if len(d[(row, col)]) == 1:
                        # actually filled
                        self.grids[row][col] = d[(row, col)][0]
                        self.fillCell(Cell(row, col),
                                      self.grids[row][col], True)
                        # mark the cell as filled
                        del d[(row, col)]
                        log.log(
                            f'({row},{col}) - unique domain: {self.grids[row][col]}')
                    else:
                        self.fillDomain(Cell(row, col), d[(row, col)], True)
        return d

    def solve(self, last_d=None) -> bool:
        ''' solving Sudoku using CSP, last domain to check the change '''
        if not self.hasEmptyCell():
            msgbox('Solved!')
            return True
        # update domains
        d = self.domainUpdate()
        log.log(
            f'Domain length: {len(d)} - last domain length: {0 if last_d is None else len(last_d)}')
        if len(d) == 0:
            msgbox('Solved!')
            return True
        # no change with empty cell(s)
        if last_d is not None and d == last_d:
            if not self.backtrack:
                return False
            else:
                log.log('CSP cannot solve it, try backtrack')
                # guess one
                for k, v in d.items():
                    row, col = k
                    # remove the current cell from domain list
                    dd = {x: y for x, y in d.items() if x != k}
                    for n in v:
                        # check each one of them
                        if self.isValid(row, col, n):
                            # make a guess ...
                            self.fillCell(Cell(row, col), n, True)
                            # and try the next cell
                            if self.solve(dd):
                                return True

                        # the guess is wrong, clear the cell and try next number
                        self.clearCell(Cell(row, col), True)

        # recursive try, solved
        return self.solve(d)


if __name__ == '__main__':
    animate = False
    backtrack = True
    csp = CSP("COMP712/Sudoku CSP Demo - Falmouth University 2023-2024",
              630, 630, 'white', animate, backtrack)
    csp.setGridNum(9, 9)
    csp.mainloop()
