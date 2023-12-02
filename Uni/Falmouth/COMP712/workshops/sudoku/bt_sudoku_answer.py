'''
    COMP712 CSP Workshop: Sudoku Solver using Backtracking

    For more details about Sudoku: 
    https://www.learn-sudoku.com/
    https://www.sudokuoftheday.com/difficulty

    Mathematical analysis of sudoku:
    https://ar5iv.labs.arxiv.org/html/1403.7373

    Daniel.Zhang @ Falmouth University
    2023-2024
'''

from gui_lib import *


class BackTracking(Canvas):

    def __init__(self, title, width, height, bgcolour='white', animate=True) -> None:
        super().__init__(title, width, height, bgcolour, animate)

    def solve(self, row=0, col=0) -> bool:
        ''' solving Sudoku using backtracking: True if solved, False if not solvable '''
        # reach last row and beyond the last column, done
        if row == self.y_grid_num-1 and col == self.x_grid_num:
            log.log('All filled, done!')
            return True

        # beyond last column, jump to the next row
        if col == self.x_grid_num:
            log.log('The last column, move the next row')
            row += 1
            col = 0

        if self.animate:
            self.animateCell(Cell(row, col), FillColour.GUESS)

        if self.board[row][col] > 0:
            log.log(f'({row}, {col}) is the fixed cell, try next one')
            return self.solve(row, col + 1)

        # already filled ,next column
        if self.grids[row][col] > 0:
            log.log(
                f'({row}, {col}) has been filled with {self.grids[row][col]}')
            return self.solve(row, col + 1)

        # try
        for n in range(1, 10):
            log.log(f' \tTrying ({n}) for ({row}, {col})')

            # check each one of them
            if self.isValid(row, col, n):
                log.log(f' \t\t({n}) can be filled at ({row}, {col})')

                # make a guess ...
                self.fillCell(Cell(row, col), n, True)

                # and try the next cell
                if self.solve(row, col + 1):
                    return True

            # the guess is wrong, clear the cell and try next number
            self.clearCell(Cell(row, col), True)
            log.log(f' -- clearing {n} for  ({row}, {col})')

        return False


if __name__ == '__main__':
    animate = True
    bt = BackTracking("COMP712/Sudoku Backtracking Demo - Falmouth University 2023-2024",
                      900, 900, 'white', animate)
    bt.setGridNum(9, 9)
    bt.mainloop()
