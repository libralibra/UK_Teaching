![Games Academy](../../../../Falmouth/common/ga_uni_logo.png)

# COMP712: Classical Artificial Intelligence 

# Workshop: Constraint Satisfaction Problem (CSP)

Dr Daniel Zhang @ Falmouth University\
2023-2024 Study Block 1

![Sudoku Solver Demo](bt_sudoku.apng)

<div id="top"></div>

# Table of Contents
- [COMP712: Classical Artificial Intelligence](#comp712-classical-artificial-intelligence)
- [Workshop: Constraint Satisfaction Problem (CSP)](#workshop-constraint-satisfaction-problem-csp)
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [The Game](#the-game)
- [The Repository](#the-repository)
  - [Code Structure](#code-structure)
- [Your Task](#your-task)
- [Further Reading](#further-reading)

# Introduction

# The Game

# The Repository
## Code Structure

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
- `getDomain(row, col)`: combines `getRow()`, `getCol()`, and `getSubGrid()` that returns the possible options to fill for the specified cell `(row, col)`
- `isValid(row, col, num)`: returns `True` is the number `num` can be filled at cell `(row, col)`

# Your Task

# Further Reading

1. [Sudoku Online](https://www.learn-sudoku.com/)
2. [Sudoku Difficulty Analysis](https://www.sudokuoftheday.com/difficulty)
3. [Mathematical Analysis of Sudoku](https://ar5iv.labs.arxiv.org/html/1403.7373)
    