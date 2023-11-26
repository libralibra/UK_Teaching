'''
    Pathfinding workshop using Depth-First Search (DFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

import sys
from gui_lib import *


class DFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=False, nb_size=4, clever=False, ran_nb=False) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        # neighbourhood size
        self.nb_size = nb_size
        # search towards targets
        self.clever = clever
        # random search surrounding area
        self.ran_nb = ran_nb
        self.showHelp()
        # ----------------------------------------------
        # YOU MAY ADD OTHER CODE HERE IF NEEDED
        # ----------------------------------------------

    def search(self):
        ''' DFS search from start to the end, record the path list '''
        # ----------------------------------------------
        # YOU CODE HERE, CREATE OTHER HELPER FUNCTIONS AS YOU NEED
        # ----------------------------------------------


if __name__ == '__main__':
    clever = False
    randomise_neighbour = False
    if len(sys.argv) > 1:
        if int(sys.argv[1]) == 1:
            clever = True
        elif int(sys.argv[1]) == 2:
            randomise_neighbour = True
    animate = True
    neighbours = 4
    dfs = DFS(
        "COMP712/Pathfinding DFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, clever, randomise_neighbour)
    dfs.setGridNum(40, 30)
    dfs.mainloop()
