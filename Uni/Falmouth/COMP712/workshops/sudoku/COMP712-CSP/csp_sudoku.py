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

    def solve(self, last_d=None) -> bool:
        ''' solving Sudoku using CSP, last domain to check the change '''
        # ----------------------------------
        # YOUR CODE HERE
        # ----------------------------------

        return False


if __name__ == '__main__':
    animate = False
    backtrack = True
    csp = CSP("COMP712/Sudoku CSP Demo - Falmouth University 2023-2024",
              630, 630, 'white', animate, backtrack)
    csp.setGridNum(9, 9)
    csp.mainloop()
