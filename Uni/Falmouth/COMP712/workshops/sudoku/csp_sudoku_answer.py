'''
    COMP712 CSP Workshop: Sudoku Solver using CSP

    Daniel.Zhang @ Falmouth University
    2023-2024
'''

from numpy import true_divide
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

    def propagete(self, row, col):
        ''' propagate the new filled number '''
        log.log(f'propagate ({row},{col}) - {self.grids[row][col]}')
        for c in range(9):
            if c != col and (row, c) in self.domains:
                self.domains[(row, c)] = [
                    x for x in self.domains[(row, c)] if x != self.grids[row][col]]

                if self.verbose:
                    self.flashRelatedDomain(Cell(row, c))
                elif self.animate:
                    self.animateCell(Cell(row, c), FillColour.GUESS)

                if len(self.domains[(row, c)]) == 1:
                    self.grids[row][c] = self.domains.pop((row, c))[0]
                    self.fillCell(
                        Cell(row, c), self.grids[row][c], True)
                    self.propagete(row, c)
                else:
                    self.fillDomain(
                        Cell(row, c), self.domains[(row, c)], True)
        for r in range(9):
            if r != row and (r, col) in self.domains:
                self.domains[(r, col)] = [
                    x for x in self.domains[(r, col)] if x != self.grids[row][col]]

                if self.verbose:
                    self.flashRelatedDomain(Cell(r, col))
                elif self.animate:
                    self.animateCell(Cell(r, col), FillColour.GUESS)

                if len(self.domains[(r, col)]) == 1:
                    self.grids[r][col] = self.domains.pop((r, col))[0]
                    self.fillCell(
                        Cell(r, col), self.grids[r][col], True)
                    self.propagete(r, col)
                else:
                    self.fillDomain(
                        Cell(r, col), self.domains[(r, col)], True)
        sg = self.getSubGridCell(row, col)
        for r in range(sg.row*3, sg.row*3+3):
            for c in range(sg.col*3, sg.col*3+3):
                if r != row and c != col and (r, c) in self.domains:
                    self.domains[(r, c)] = [
                        x for x in self.domains[(r, c)] if x != self.grids[row][col]]

                    if self.verbose:
                        self.flashRelatedDomain(Cell(r, c))
                    elif self.animate:
                        self.animateCell(Cell(r, c), FillColour.GUESS)

                    if len(self.domains[(r, c)]) == 1:
                        self.grids[r][c] = self.domains.pop((r, c))[0]
                        self.fillCell(
                            Cell(r, c), self.grids[r][c], True)
                        self.propagete(r, c)
                    else:
                        self.fillDomain(
                            Cell(r, c), self.domains[(r, c)], True)

    def bt(self, row=0, col=0) -> bool:
        ''' solving Sudoku using backtracking: True if solved, False if not solvable '''
        # reach last row and beyond the last column, done
        if row == self.y_grid_num-1 and col == self.x_grid_num:
            msgbox('Solved!')
            return True

        # beyond last column, jump to the next row
        if col == self.x_grid_num:
            log.log('The last column, move the next row')
            row += 1
            col = 0

        if self.board[row][col] > 0:
            log.log(f'({row}, {col}) is the fixed cell, try next one')
            return self.bt(row, col + 1)

        # already filled ,next column
        if self.grids[row][col] > 0:
            log.log(
                f'({row}, {col}) has been filled with {self.grids[row][col]}')
            return self.bt(row, col + 1)

        # do not flash the related cells
        if self.verbose:
            self.animateCell(Cell(row, col), FillColour.GUESS)

        # all domains
        domains = list(range(1, 10))
        if self.forward:
            domains = self.getDomain(row, col)

        log.log(f'({row},{col}) - domain: {domains}')

        # try
        for n in domains:
            log.log(f' \tTrying ({n}) for ({row}, {col})')

            # check each one of them
            if self.isValid(row, col, n):
                log.log(f' \t\t({n}) can be filled at ({row}, {col})')

                # make a guess ...
                self.fillCell(Cell(row, col), n, True)

                # and try the next cell
                if self.bt(row, col + 1):
                    return True

            # the guess is wrong, clear the cell and try next number
            log.log(f' \t\t --> clear ({n}) at ({row}, {col})')
            self.clearCell(Cell(row, col), True)

        return False

    def solve(self) -> bool:
        ''' solving Sudoku using CSP, last domain to check the change '''

        # update domains to see if changes
        # scan
        for row in range(9):
            for col in range(9):
                # filled already
                if self.grids[row][col] > 0:
                    continue
                # flash the cell
                if self.verbose:
                    self.flashRelatedDomain(Cell(row, col))
                elif self.animate:
                    self.animateCell(Cell(row, col), FillColour.GUESS)
                else:
                    self.clearCell(Cell(row, col), self.animate)
                # get all domains
                d = self.getDomain(row, col)
                if len(d) > 1:
                    self.fillDomain(Cell(row, col), d, True)
                    self.domains[(row, col)] = d
                elif len(d) == 1:
                    self.grids[row][col] = d[0]
                    self.fillCell(Cell(row, col),
                                  self.grids[row][col], True)
                    log.log(
                        f'({row},{col}) - unique domain: {self.grids[row][col]}')
                    # remove current from domain
                    self.domains.pop((row, col), None)
                    # propagate to row, col, and sub grid
                    self.propagete(row, col)
        if not self.hasEmptyCell():
            msgbox('Solved!')
            return True

        # no change with empty cell(s)
        if self.backtrack:
            log.log('CSP cannot solve it, try backtrack')
            return self.bt(0, 0)

        return False


if __name__ == '__main__':
    animate = False
    backtrack = True
    csp = CSP("COMP712/Sudoku CSP Demo - Falmouth University 2023-2024",
              630, 630, 'white', animate, backtrack)
    csp.setGridNum(9, 9)
    csp.mainloop()
