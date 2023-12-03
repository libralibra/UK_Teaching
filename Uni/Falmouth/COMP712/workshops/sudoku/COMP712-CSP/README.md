# COMP712-CSP
Constraint Satisfaction Problem (CSP) Workshop

This repository contains the materials for COMP712 - CSP workshop.

- `demo_sudoku_bt.pyc`: demo of solving Sudoku using Backtracking algorithm (BT)
- `demo_sudoku_cp.pyc`: demo of solving Sudoku using Constraint Propagation (CP)
- 2 predefined puzzles
- Press <kbd>H</kbd> for help

The `gui_lib` contains helper functions for visualisation. Some of them are:

- `fillCell(v: Cell, s: int, force_update=False)`: fills a specific cell `v` using the number `s`, update the board if `force_update` is `True`
- `clearCell(v: Cell, force_update=False)`: clears a cell `v` and update the board if `force_update` is `True`
- `animateCell(c: Cell, colour='white')`: changes the specified cell **`c`**'s background colour with `colour`, then resets it to the default colour
- `getRow(row)`: returns a list of the numbers in the `row`
- `getCol(col)`: returns a list of the numbers in the `col`
- `getSubGrid(row, col)`: returns a list of the numbers in the sub-grid which the cell `(row, col)` belongs to, it will automatically calculate the grid position
- `getDomain(row, col)`: combines `getRow()`, `getCol()`, and `getSubGrid()` that returns the possible options to fill for the specified cell `(row, col)`
- `isValid(row, col, num)`: returns `True` is the number `num` can be filled at cell `(row, col)`

# Task:

1. implement Backtracking (BT) algorithm in `bt_sudoku.py`
2. implement Constraint Propagation (CP) in `cp_sudoku.py`
3. you don't need to implement any GUI functionalities as long as **the `.solve()` function was implemented properly**. It should return either `True` or `False` to indicate the solvability of the Sudoku puzzle.
   1. All the sudoku puzzle generated by pressing the keyboard shortcuts are solvable.
   2. Some loaded externally might not be solvable.
4. Compare BT and CP approach, combine them together to either:
   1. reduce the search space by `CP` in `BT` 
   2. continue searching with `BT` if `CP` cannot proceed further