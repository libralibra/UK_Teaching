'''
    Pathfinding workshop using Greedy Best-First Search (GBFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

import sys
from gui_lib import *
from queue import PriorityQueue


class GBFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=False, nb_size=4,  euclidean_dist=False) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        # neighbourhood size
        self.nb_size = nb_size
        # use Euclidean distance rather than Manhattan distance
        self.euc_dist = euclidean_dist
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
    euclidean_dist = False
    if len(sys.argv) > 1 and int(sys.argv[1]) == 1:
        euclidean_dist = True
    animate = True
    neighbours = 4
    gbfs = GBFS(
        "COMP712/Pathfinding GBFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, euclidean_dist)
    gbfs.setGridNum(40, 30)
    gbfs.mainloop()
