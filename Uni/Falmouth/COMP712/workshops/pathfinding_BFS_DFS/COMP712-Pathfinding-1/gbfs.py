'''
    Pathfinding workshop using Greedy Best-First Search (GBFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from gui_lib import *
from queue import PriorityQueue


class GBFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=False, nb_size=4) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        self.nb_size = nb_size
        self.showHelp()
        # ----------------------------------------------
        # YOU MAY ADD OTHER CODE HERE IF NEEDED
        # ----------------------------------------------

    def search(self):
        ''' GBFS search from start to the end, record the path list '''
        # ----------------------------------------------
        # YOU CODE HERE, CREATE OTHER HELPER FUNCTIONS AS YOU NEED
        # ----------------------------------------------


if __name__ == '__main__':
    animate = True
    neighbours = 4
    gbfs = GBFS(
        "COMP712/Pathfinding GBFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours)
    gbfs.setGridNum(40, 30)
    gbfs.mainloop()
