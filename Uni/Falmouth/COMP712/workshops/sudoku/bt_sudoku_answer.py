'''
    COMP712 CSP Workshop: Sudoku Solver using Backtracking

    Daniel.Zhang @ Falmouth University
    2023-2024
'''

from gui_lib import *


class BackTracking(Canvas):

    def __init__(self, title, width, height, bgcolour='white', animate=True, forward=True) -> None:
        super().__init__(title, width, height, bgcolour, animate)
        self.forward = forward

    def solve(self, row=0, col=0) -> bool:
        ''' solving Sudoku using backtracking: True if solved, False if not solvable '''
        # reach last row and beyond the last column, done
        if row == self.y_grid_num-1 and col == self.x_grid_num:
            log.log('All filled, done!')
            msgbox('Solved!')
            return True

        # beyond last column, jump to the next row
        if col == self.x_grid_num:
            log.log('The last column, move the next row')
            row += 1
            col = 0

        if self.board[row][col] > 0:
            log.log(f'({row}, {col}) is the fixed cell, try next one')
            return self.solve(row, col + 1)

        # already filled ,next column
        if self.grids[row][col] > 0:
            log.log(
                f'({row}, {col}) has been filled with {self.grids[row][col]}')
            return self.solve(row, col + 1)

        if self.animate:
            self.flashRelatedCell(Cell(row, col))
        # else:
        #     self.animateCell(Cell(row, col), FillColour.GUESS)

        # all domains
        domains = list(range(1, 10))
        if self.forward:
            rows = self.getRow(row)
            cols = self.getCol(col)
            grid = self.getSubGrid(row, col)
            nums = rows+cols+grid
            domains = [x for x in domains if x not in nums]

        log.log(f'({row},{col}) - domain: {domains}')

        # try
        for n in domains:
            # log.log(f' \tTrying ({n}) for ({row}, {col})')

            # check each one of them
            if self.isValid(row, col, n):
                # log.log(f' \t\t({n}) can be filled at ({row}, {col})')

                # make a guess ...
                self.fillCell(Cell(row, col), n, True)

                # and try the next cell
                if self.solve(row, col + 1):
                    return True

            # the guess is wrong, clear the cell and try next number
            self.clearCell(Cell(row, col), True)
            # log.log(f' -- clearing {n} for  ({row}, {col})')

        return False


if __name__ == '__main__':
    animate = False
    forward = True
    bt = BackTracking("COMP712/Sudoku Backtracking Demo - Falmouth University 2023-2024",
                      630, 630, 'white', animate, forward)
    bt.setGridNum(9, 9)
    bt.mainloop()
