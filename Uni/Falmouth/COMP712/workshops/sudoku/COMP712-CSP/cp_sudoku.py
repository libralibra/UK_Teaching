'''
    COMP712 CSP Workshop: Sudoku Solver using CP

    Daniel.Zhang @ Falmouth University
    2023-2024
'''
from gui_lib import *


class CP(Canvas):

    def __init__(self, title, width, height, bgcolour='white', animate=True, backtrack=True) -> None:
        super().__init__(title, width, height, bgcolour, animate)
        self.backtrack = backtrack

    def solve(self) -> bool:
        ''' solving Sudoku using CP '''
        # ----------------------------------
        # YOUR CODE HERE
        # ----------------------------------

        return False


if __name__ == '__main__':
    animate = False
    backtrack = True
    cp = CP("COMP712/Sudoku CP Demo - Falmouth University 2023-2024",
            630, 630, 'white', animate, backtrack)
    cp.setGridNum(9, 9)
    cp.mainloop()
