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
        # ----------------------------------
        # YOUR CODE HERE
        # ----------------------------------

        return False


if __name__ == '__main__':
    animate = False
    forward = True
    bt = BackTracking("COMP712/Sudoku Backtracking Demo - Falmouth University 2023-2024",
                      630, 630, 'white', animate, forward)
    bt.setGridNum(9, 9)
    bt.mainloop()
