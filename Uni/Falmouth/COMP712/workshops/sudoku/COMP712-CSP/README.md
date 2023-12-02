# COMP712-CSP
Constraint Satisfaction Problem Workshop

This repository contains the materials for COMP712 - CSP workshop.

- `demo_bt_sudoku.pyc`: demo of solving Sudoku using backtracking
- `demo_csp_sudoku.pyc`: demo of solving Sudoku using CSP
- 2 predefined puzzles
- Press <kbd>H</kbd> for help

The `gui_lib` contains helper functions for visualisation. Some of them are:

- `fillCell(v: Cell, s: int, force_update=False)`: fills a specific cell `v` using the number `s`, update the board if `force_update` is `True`
- `clearCell(v: Cell, force_update=False)`: clears a cell `v` and update the board if `force_update` is `True`
- `animateCell(c: Cell, colour='white')`: changes the specified cell **`c`**'s background colour with `colour`, then resets it to the default colour
- `getRow(row)`: returns a list of the numbers in the `row`
- `getCol(col)`: returns a list of the numbers in the `col`
- `getSubGrid(row, col)`: returns a list of the numbers in the sub-grid which the cell `(row, col)` belongs to, it will automatically calculate the grid position
- `isValid(row, col, num)`: returns `True` is the number `num` can be filled at cell `(row, col)`