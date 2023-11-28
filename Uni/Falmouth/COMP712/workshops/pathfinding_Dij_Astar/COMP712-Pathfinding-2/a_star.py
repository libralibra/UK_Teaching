'''
    Pathfinding workshop using A* Algorithm (Non-Uniform Cost Search)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from gui_lib import *
from queue import PriorityQueue


class ASTAR(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=True, nb_size=4, euclidean_dist=False) -> None:
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
        ''' A* search from start to the end, record the path list '''
        # ----------------------------------------------
        # YOU CODE HERE, CREATE OTHER HELPER FUNCTIONS AS YOU NEED
        # ----------------------------------------------


if __name__ == '__main__':
    euclidean_dist = True
    animate = True
    neighbours = 4
    a_star = ASTAR(
        "COMP712/Pathfinding A* Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours, euclidean_dist)
    a_star.setGridNum(40, 30)
    a_star.mainloop()
