# COMP712-Pathfinding-1

This repository contains the materials for COMP712 - Pathfinding (1) workshop.

There are three demos available:

- `demo_bfs.pyc`: Demonstrates Breadth-first search
- `demo_dfs.pyc`: Demonstrates Depth-first search
- `demo_gbfs.pyc`: Demonstrates Greedy best-first search 
- 5 pre-defined maps are provided, which can be loaded by key <kbd>`L`</kbd>

The `gui_lib.py` file contains all the necessary GUI capabilities that shouldn't be altered. However, some functions might aid in pathfinding visualisation:

- `getValidNeighbour(Cell, direction):` Retrieves the neighbour on the specified `direction`.
  - `Cell` represents a cell object, while `direction` can be one of `east`, `north-east`, `north`, `north-west`, `west`, `south-west`, `south`, `south-east`.
- `colourCell(Cell, colour, ratio=0.8)`: Fills the specified `Cell` with the given `colour`. The default `ratio` is `0.8`, filling `80%` of the cell with the colour.

Each algorithm should be implemented in its respective `.py` file:

- The `search()` function is mandatory in each file as the main lib relies on it for the search process.
- The `search()` function must return either `True` or `False`
- You may want to call `animateCell(c)` to animate the searching process. But you don't have to as it shouldn't affect the result.
- Feel free to create additional helper functions as required.

