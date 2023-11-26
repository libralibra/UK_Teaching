'''
    Pathfinding workshop using Breadth-First Search (BFS)

    Dr Daniel Zhang @ Falmouth University
    2023 - 2024
'''

from gui_lib import *


class BFS(Canvas):
    def __init__(self, title, width, height, bgcolour='white', animate=True, nb_size=4) -> None:
        ''' nb_size controls how may neighbours to search: 4 or 8 '''
        super().__init__(title, width, height, bgcolour)
        self.animate = animate
        self.nb_size = nb_size
        self.showHelp()
        # ----------------------------------------------
        # YOU MAY ADD OTHER CODE HERE IF NEEDED
        # ----------------------------------------------

    def search(self):
        ''' BFS search from start to the end, record the path list '''
        # ----------------------------------------------
        # YOU CODE HERE, CREATE OTHER HELPER FUNCTIONS AS YOU NEED
        # ----------------------------------------------


if __name__ == '__main__':
    animate = True
    neighbours = 4
    bfs = BFS(
        "COMP712/Pathfinding BFS Demo - Falmouth University 2023-2024", 800, 600, 'white', animate, neighbours)
    bfs.setGridNum(40, 30)
    bfs.mainloop()
