'''
    Pathfinding workshop using Dijkstra's Algorithm (Uniform Cost Search)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from gui_lib import *
from queue import PriorityQueue


class DIJKSTRA(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=True, nb_size=4) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        # neighbourhood size
        self.nb_size = nb_size
        # neighbourhood size
        self.nb_size = nb_size
        self.showHelp()
        # ----------------------------------------------
        # YOU MAY ADD OTHER CODE HERE IF NEEDED
        # ----------------------------------------------

    def search(self):
        ''' Dijkstra search from start to the end, record the path list '''
        # ----------------------------------------------
        # YOU CODE HERE, CREATE OTHER HELPER FUNCTIONS AS YOU NEED
        # ----------------------------------------------


if __name__ == '__main__':
    animate = True
    neighbours = 4
    dijkstra = DIJKSTRA(
        "COMP712/Pathfinding Dijkstra Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours)
    dijkstra.setGridNum(40, 30)
    dijkstra.mainloop()
