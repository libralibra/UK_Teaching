'''
    Python Library for GUI (PIG) to Specifically for Sudoku Board

    Dr Daniel Zhang @ Falmouth University
    2023

    Note: 
    1. for more colour strings: https://trinket.io/docs/colors
    2. an introduction to tkinter: https://dafarry.github.io/tkinterbook/index.htm

'''

from random import sample, choice
import time
from tkinter import filedialog
import turtle
import logging

logging.basicConfig(level=logging.DEBUG)


class Log:
    def log(self, s):
        logging.info(s)


# global logger
log = Log()


class WrongParameterError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print(f'[##ERROR]: Wrong input parameter {args}')


class FillColour:
    ''' grid colour enums
        https://trinket.io/docs/colors
    '''
    EMPTY = 'white'
    # the working cell
    GUESS = 'light green'
    # 3x3 subgrid background colour
    FILL = 'peach puff'
    # the current checking cell
    CURRENT = 'yellow'


class DrawColour:
    ''' text colour
    '''
    LINES = 'black'
    # original numbers
    KNOWN = 'black'
    # filled numbers
    FILL = 'blue'


class Point:
    ''' represent a point object (x, y) '''

    def __init__(self, x=0, y=0) -> None:
        self.x, self. y = x, y

    def __str__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __sub__(self, v):
        return Point(self.x-v.x, self.y-v.y)

    def __add__(self, v):
        return Point(self.x+v.x, self.y+v.y)


class Cell:
    ''' represent a matrix indices (row, col), parent here can be used to retrieve
        cells of the same sub grid, assign them to be the children of top-left sub grid
    '''

    def __init__(self, row: int, col: int, p=None) -> None:
        self.row, self. col = int(row), int(col)
        self.parent = p

    def __str__(self) -> str:
        return f'Cell({self.row}, {self. col})'

    def __eq__(self, v) -> bool:
        return self.row == v.row and self.col == v.col

    def __lt__(self, v) -> bool:
        # for PriorityQueue() if the priority for some items is equal
        return self.row < v.row or self.col < v.col


def msgbox(message, title='COMP712/Sudoku Demo'):
    ''' show a modal messagebox '''
    turtle.TK.messagebox.showinfo(title=title, message=message)


def questionBox(title, question):
    ''' yes/no question box, return is string (either "yes" or "no") '''
    return turtle.TK.messagebox.askquestion(title, question)


class Canvas:
    ''' represent the drawing canvas, which actually is a turtle.Screen() object '''

    def __init__(self, title, width, height, bgcolour='white', animate=True) -> None:
        self.screen = turtle.Screen()
        self.screen.colormode(255)
        self.bgcolour = bgcolour.strip()
        self.title = title
        self.width, self.height = width, height
        # the grid size and grid number
        self.x_grid_size, self.y_grid_size = self.width, self.height
        self.x_grid_num, self.y_grid_num = 1, 1
        self.grids = [[0]*9 for _ in range(9)]
        # the original board - the puzzle
        self.board = [[0]*9 for _ in range(9)]
        # domain for cp
        self.domains = {}
        # animation
        self.animate = animate
        # has a puzzle
        self.ready = False
        # forward checking for backtracking
        self.forward = True
        # enable backtracking for CP
        self.backtrack = True
        # verbose animation
        self.verbose = False
        self.registerAll()
        self.init()
        self.showHelp()

    def __str__(self) -> str:
        return f'Canvas({self.title}) with size (w, h) = ({self.width}, {self.height}), bgcolor = {self.bgcolour}'

    def __repr__(self) -> str:
        return str(self)

    def mainloop(self):
        self.screen.mainloop()

    def init(self):
        ''' clear the canvas, called by clear() '''
        self.screen.setup(self.width, self.height)
        self.screen.colormode(255)
        self.setBgColour(self.bgcolour)
        self.setTitle(self.title)
        self.screen.tracer(False)
        self.pen = Pen()

    def reset(self):
        ''' clear the canvas and redraw grid lines '''
        self.screen.clear()
        self.init()
        self.grids = [[col for col in row] for row in self.board]
        self.domains = {}
        self.drawGrids()
        self.drawGridLines()
        self.update()
        self.registerAll()
        self.showHelp()

    def exit(self):
        self.screen.bye()

    def update(self):
        ''' force to update the canvas '''
        self.screen.update()

    def setPenColour(self, colour):
        ''' set pen colour for self.pen object '''
        self.pen.setColour(colour)

    def setSize(self, width, height):
        ''' change canvas size '''
        self.screen.setup(width, height)
        self.width, self.height = width, height

    def registerLeftClick(self, func):
        ''' callback for left click '''
        if func:
            self.screen.onclick(func, 1)

    def registerRightClick(self, func):
        ''' callback for right click '''
        if func:
            self.screen.onclick(func, 3)

    def registerMiddleClick(self, func):
        ''' callback for middle click '''
        if func:
            self.screen.onclick(func, 2)

    def registerKey(self, func, key):
        ''' callback for keypress '''
        if func and key:
            self.screen.onkey(func, key)
            self.screen.listen()

    def showHelp(self):
        ''' help information messagebox '''
        s = 'Sudoku Demo\n'
        s += '=[ Operation ]==============================\n'
        s += 'Solve puzzle - SPACE or ENTER\n'
        s += 'Reset puzzle - DELETE, ESC, or right-click\n'
        s += 'Enable CP Forward checking (for Backtracking) - F\n'
        s += 'Enable backtracking (for CP) - B\n'
        s += 'Switch animation - A\n'
        s += 'Very detailed animation - V\n'
        # E, M, D, X, T
        s += '-[ Levels ]----------------------------------\n'
        s += 'New EASY game - E\n'
        s += 'New MEDIUM game - M\n'
        s += 'New HARD game - D\n'
        s += 'New EXPERT game - X\n'
        s += 'New MASTER game - T\n'
        s += '-[ Save/Load ]-------------------------------\n'
        s += 'Save puzzle  - S or W\n'
        s += 'Load puzzle  - L or O\n'
        s += '-[ Help ]------------------------------------\n'
        s += 'Show help   - H'
        # self.pen.writeText(Point(self.width/25, -self.width/7), s)
        msgbox(s, "Sudoku Demo Help")

    def setBgColour(self, colour):
        ''' change background colour '''
        self.screen.bgcolor(colour)
        self.bgcolour = colour

    def getSymmetryCell(self, row, col):
        ''' get rotation symmetric position for deleting '''
        return Cell(8-row, 8-col)

    def defineLevel(self, v=0):
        ''' delete a certain number of cells from the board
            difficulty analysis: https://www.cnblogs.com/candyhuang/archive/2011/08/25/2153668.html
            rating: 
            0: 45-47
            1: 48-50
            2: 51-52
            3: 53-54
            4: 55-56
            for illustration purpose, less number are removed
        '''
        df = {0: [33, 36], 1: [37, 40], 2: [41, 44], 3: [45, 47], 4: [48, 50]}
        # how many numbers to delete
        num = choice(range(df[v][0], df[v][1]+1))
        cnt = 0
        while cnt < num:
            row, col = choice(range(9)), choice(range(9))
            if self.board[row][col] == 0:
                continue
            self.board[row][col] = 0
            sc = self.getSymmetryCell(row, col)
            self.board[sc.row][sc.col] = 0
            cnt += 2

    def getNewGame(self, v=0):
        ''' get a new game from https://sudoku.com/easy/, https://sudoku.com/medium/, 
            https://sudoku.com/hard/, https://sudoku.com/expert/, or https://sudoku.com/evil/
            can be invoked by   E, M, D, X, V
            levels are          0, 1, 2, 3, 4
            algorithm take from: https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
        '''
        # pattern for a baseline valid solution
        def pattern(r, c): return (3*(r % 3)+r//3+c) % 9
        def shuffle(s): return sample(s, len(s))
        # shuffle each 3 rows and 3 cols
        rBase = range(3)
        rows = [g*3 + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g*3 + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, 10))
        # produce board using randomized baseline pattern
        self.board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        # delete
        self.defineLevel(v)
        # copy to grids
        self.grids = [[x for x in row] for row in self.board]
        self.domains = {}
        # update ui
        self.drawGrids()
        self.drawGridLines()
        # ready
        self.ready = True

    def setTitle(self, title):
        ''' change title '''
        if title.strip():
            self.screen.title(title.strip())

    def setGridNum(self, x_num, y_num):
        ''' change grid numbers, grid sizes will be recalculated '''
        if 1 <= x_num < self.width and 1 <= y_num < self.height:
            self.x_grid_num, self.y_grid_num = int(x_num), int(y_num)
            self.x_grid_size = self.width / self.x_grid_num
            self.y_grid_size = self.height / self.y_grid_num
            self.grids = [
                [0] * self.x_grid_num for _ in range(self.y_grid_num)]
            self.drawGrids()
            self.drawGridLines()

    def getGridCentre(self, row, col):
        ''' get the grid centre using row(y) and col(x) index like matrix '''
        if not 0 <= col < self.x_grid_num or not 0 <= row < self.y_grid_num:
            # log.log(f'The input indices ({row}, {col}) is not permitted')
            return Point(0, 0)
        # find the left half num
        x_half_num, y_half_num = self.x_grid_num/2., self.y_grid_num/2.
        x_left = -x_half_num * self.x_grid_size
        y_top = y_half_num * self.y_grid_size
        x = x_left + self.x_grid_size * col + self.x_grid_size/2.
        y = y_top - self.y_grid_size * row - self.y_grid_size/2.
        return Point(x, y)

    def getGridIndices(self, x, y):
        ''' convert position (x,y) to grid indices (row, col) like matrix '''
        if not -self.width/2 <= x <= self.width/2 or not -self.height/2 <= y <= self.height/2:
            # log.log('Outside the main grid')
            return None
        row, col = -1, -1
        x_half_num, y_half_num = self.x_grid_num/2., self.y_grid_num/2.
        x_left = -x_half_num * self.x_grid_size
        y_bot = -y_half_num * self.y_grid_size
        for k in range(self.x_grid_num+1):
            if x_left + k*self.x_grid_size <= x <= x_left + (k+1)*self.x_grid_size:
                col = k
                break
        for k in range(self.y_grid_num+1):
            if y_bot + k*self.y_grid_size <= y <= y_bot + (k+1)*self.y_grid_size:
                row = self.y_grid_num-1-k
                break
        return Cell(int(row), int(col))

    def drawGridLines(self):
        ''' draw the grid lines '''
        if self.x_grid_num > 1 and self.y_grid_num > 1:
            x_half_num, y_half_num = self.x_grid_num/2., self.y_grid_num/2.
            x_left = -x_half_num * self.x_grid_size
            x_right = x_half_num * self.x_grid_size
            y_top = y_half_num * self.y_grid_size
            y_bottom = -y_half_num * self.y_grid_size
            pen = self.pen
            for i in range(self.y_grid_num+1):
                y = y_top - i * self.y_grid_size
                pt_left = Point(x_left, y)
                pt_right = Point(x_right, y)
                if i % 3 == 0:
                    pen.setPenWidth(3)
                pen.drawLine(pt_left, pt_right)
                if i % 3 == 0:
                    pen.setPenWidth(1)
            for i in range(self.x_grid_num+1):
                x = x_left + i * self.x_grid_size
                pt_top = Point(x, y_top)
                pt_bottom = Point(x, y_bottom)
                if i % 3 == 0:
                    pen.setPenWidth(3)
                pen.drawLine(pt_top, pt_bottom)
                if i % 3 == 0:
                    pen.setPenWidth(1)

    def writeText(self, p: Point, s: str, colour='black'):
        ''' write text to canvas'''
        if not s.strip() or not 0 <= p.x <= self.width or not 0 <= p.y <= self.height:
            return
        self.pen.writeText(p, s, colour)

    def colourCell(self, v: Cell, colour, ratio=0.95):
        ''' fill a cell, by default size = 80% '''
        if 0 <= v.row < self.y_grid_num and 0 <= v.col < self.x_grid_num:
            # change the colour a little bit in case running for multiple times
            centre = self.getGridCentre(v.row, v.col)
            # fill it
            self.pen.drawRect(centre,
                              self.x_grid_size * max(min(ratio, 1.0), 0.1),
                              self.y_grid_size * max(min(ratio, 1.0), 0.1),
                              colour)
            self.setPenColour('black')

    def writeCell(self, v: Cell, s=None):
        ''' write the text to the cell '''
        if s is None:
            return
        self.grids[v.row][v.col] = int(s)
        if self.grids[v.row][v.col] != 0:
            pt = self.getGridCentre(v.row, v.col)
            colour = DrawColour.FILL
            if self.board[v.row][v.col] != 0:
                colour = DrawColour.KNOWN
                self.pen.writeText(pt-Point(0, 30), str(s), colour)
            else:
                self.pen.writeText(pt-Point(0, 30), str(s), colour, False)

    def writeDomain(self, v: Cell, s: list, force_update=False):
        ''' write several numbers to the same cell'''
        if len(s) == 0:
            return
        elif len(s) == 1:
            self.fillCell(v, s[0], force_update)
            return
        pt = self.getGridCentre(v.row, v.col)
        for n in range(1, 10):
            if n in s:
                self.pen.writeText(
                    pt-Point(0, (n-1)//3*25)+Point(((n-1) % 3-1)*20, 12), str(n), DrawColour.FILL, True, 15)
        if force_update:
            self.update()

    def clearCell(self, v: Cell, force_update=False):
        ''' clear a cell '''
        self.fillCell(v, 0, force_update)

    def fillCell(self, v: Cell, s: int, force_update=False):
        ''' fill the number, not the colour '''
        if 0 <= v.row < self.y_grid_num and 0 <= v.col < self.x_grid_num and 0 <= int(s) <= 9:
            g = self.getSubGridCell(v.row, v.col)
            colour = FillColour.EMPTY
            if (g.row+g.col) % 2 == 0:
                colour = FillColour.FILL
            self.colourCell(v, colour)
            self.grids[v.row][v.col] = s
            # may need to draw the sub grid
            if v.row in [0, 2, 3, 5, 6, 8] or v.col in [0, 2, 3, 5, 6, 8]:
                self.drawGridLines()
            self.writeCell(v, s)
            if force_update:
                self.update()

    def fillDomain(self, v: Cell, s: list, force_update=False):
        ''' write domain numbers to the cell for cp '''
        if 0 <= v.row < self.y_grid_num and 0 <= v.col < self.x_grid_num and self.grids[v.row][v.col] == 0 and len(s) > 0:
            g = self.getSubGridCell(v.row, v.col)
            colour = FillColour.EMPTY
            if (g.row+g.col) % 2 == 0:
                colour = FillColour.FILL
            self.colourCell(v, colour)
            # may need to draw the sub grid
            if v.row in [0, 2, 3, 5, 6, 8] or v.col in [0, 2, 3, 5, 6, 8]:
                self.drawGridLines()
            if len(s) > 1:
                self.writeDomain(v, s, force_update)
            else:
                self.writeCell(v, s[0])
                if force_update:
                    self.update()
            # log.log(f'{v} - domain: {s}')

    def animateCell(self, c: Cell, colour='white'):
        ''' animate cell colour during the search for special cells '''
        self.colourCell(c, colour)
        self.update()
        self.fillCell(c, self.grids[c.row][c.col], True)

    def flashRelatedCell(self, ce: Cell):
        ''' flash the row, column, and sub grid of the cell '''
        row, col = ce.row, ce.col
        sg = self.getSubGridCell(row, col)
        for c in range(9):
            if c == col and c in range(sg.col*3, sg.col*3+3):
                continue
            self.colourCell(Cell(row, c), FillColour.GUESS)
            if self.grids[row][c] > 0:
                self.writeCell(Cell(row, c), self.grids[row][c])
        for r in range(9):
            if r == row and r in range(sg.row*3, sg.row*3+3):
                continue
            self.colourCell(Cell(r, col), FillColour.GUESS)
            if self.grids[r][col] > 0:
                self.writeCell(Cell(r, col), self.grids[r][col])
        for r in range(sg.row*3, sg.row*3+3):
            for c in range(sg.col*3, sg.col*3+3):
                if r == row and c == col:
                    continue
                self.colourCell(Cell(r, c), FillColour.GUESS)
                if self.grids[r][c] > 0:
                    self.writeCell(Cell(r, c), self.grids[r][c])
        self.colourCell(Cell(row, col), FillColour.CURRENT)
        self.update()
        for c in range(9):
            if c not in range(sg.col*3, sg.col*3+3):
                self.fillCell(Cell(row, c), self.grids[row][c])
        for r in range(9):
            if r not in range(sg.row*3, sg.row*3+3):
                self.fillCell(Cell(r, col), self.grids[r][col])
        for r in range(sg.row*3, sg.row*3+3):
            for c in range(sg.col*3, sg.col*3+3):
                self.fillCell(Cell(r, c), self.grids[r][c])

    def flashRelatedDomain(self, ce: Cell):
        row, col = ce.row, ce.col
        sg = self.getSubGridCell(row, col)

        for c in range(9):
            # no the the current one and not in it's sub grid
            if c == col or c in range(sg.col*3, sg.col*3+3):
                continue
            self.colourCell(Cell(row, c), FillColour.GUESS)
            if self.grids[row][c] > 0:
                self.writeCell(Cell(row, c), self.grids[row][c])
            else:
                self.domains[(row, c)] = self.getDomain(row, c)
                self.writeDomain(Cell(row, c), self.domains[(row, c)])

        for r in range(9):
            if r == row or r in range(sg.row*3, sg.row*3+3):
                continue
            self.colourCell(Cell(r, col), FillColour.GUESS)
            if self.grids[r][col] > 0:
                self.writeCell(Cell(r, col), self.grids[r][col])
            else:
                self.domains[(r, col)] = self.getDomain(r, col)
                self.writeDomain(Cell(r, col), self.domains[(r, col)])

        for r in range(sg.row*3, sg.row*3+3):
            for c in range(sg.col*3, sg.col*3+3):
                if r == row and c == col:
                    continue
                self.colourCell(Cell(r, c), FillColour.GUESS)
                if self.grids[r][c] > 0:
                    self.writeCell(Cell(r, c), self.grids[r][c])
                else:
                    self.domains[(r, c)] = self.getDomain(r, c)
                    self.writeDomain(Cell(r, c), self.domains[(r, c)])

        self.colourCell(Cell(row, col), FillColour.CURRENT)
        self.writeCell(Cell(row, col), self.grids[row][col])
        self.update()

        for c in range(9):
            if c in range(sg.col*3, sg.col*3+3):
                continue
            at = Cell(row, c)
            if self.grids[row][c] > 0:
                self.fillCell(at, self.grids[row][c])
            else:
                self.fillDomain(at, self.getDomain(row, c))
        for r in range(9):
            if r in range(sg.row*3, sg.row*3+3):
                continue
            at = Cell(r, col)
            if self.grids[r][col] > 0:
                self.fillCell(at, self.grids[r][col])
            else:
                self.fillDomain(at, self.getDomain(r, col))
        for r in range(sg.row*3, sg.row*3+3):
            for c in range(sg.col*3, sg.col*3+3):
                at = Cell(r, c)
                if self.grids[r][c] > 0:
                    self.fillCell(at, self.grids[r][c])
                else:
                    self.fillDomain(Cell(r, c), self.getDomain(r, c))
        self.update()

    def getSubGridCell(self, row, col) -> Cell:
        ''' work out the sub grid row and column '''
        return Cell(row//3, col//3)

    def drawGrids(self):
        ''' fill a grid with reduced size unless it's the white background '''
        if len(self.grids) > 0 and len(self.grids[0]) > 0:
            for row in range(len(self.grids)):
                for col in range(len(self.grids[0])):
                    self.fillCell(Cell(row, col), self.grids[row][col])

    def getRow(self, row) -> list:
        ''' get a row of non-zero cell values '''
        if 0 <= row < self.y_grid_num:
            return [x for x in self.grids[row] if x > 0]
        return []

    def getCol(self, col) -> list:
        ''' get a column of non-zero cell values '''
        if 0 <= col < self.x_grid_num:
            return [x for x in [row[col] for row in self.grids] if x > 0]
        return []

    def getSubGrid(self, row, col) -> list:
        ''' get all cell values in the sub grid '''
        if 0 <= row < self.y_grid_num and 0 <= col < self.x_grid_num:
            sg = self.getSubGridCell(row, col)
            return [x for x in [self.grids[r][c] for r in range(sg.row*3, sg.row*3+3) for c in range(sg.col*3, sg.col*3+3)] if x > 0]
        return []

    def getDomain(self, row, col) -> list:
        ''' get possible domain of a cell that combines getRow, getCol, and getSubGrid '''
        rows = self.getRow(row)
        cols = self.getCol(col)
        subs = self.getSubGrid(row, col)
        nums = rows+cols+subs
        return [x for x in range(1, 10) if x not in nums]

    def isValid(self, row, col, num) -> bool:
        ''' check if the value can be filled in that cell '''
        if self.board[row][col] > 0 and num == self.board[row][col]:
            return True
        rows = self.getRow(row)
        if num in rows:
            log.log(f'{num} find in row')
            return False
        cols = self.getCol(col)
        if num in cols:
            log.log(f'{num} find in col')
            return False
        sc = self.getSubGrid(row, col)
        if num in sc:
            log.log(f'{num} find in sub grid')
            return False
        # 2 cells have exactly same single domain
        d = self.getDomain(row, col)
        if len(d) == 1:
            for c in range(9):
                if c != col and self.grids[row][c] == 0:
                    c_domain = self.getDomain(row, c)
                    if d == c_domain:
                        log.log(
                            f'row: ({row},{c}) has the same domain {d[0]} as ({row},{col})')
                        return False
            for r in range(9):
                if r != row and self.grids[r][col] == 0:
                    c_domain = self.getDomain(r, col)
                    if d == c_domain:
                        log.log(
                            f'col: ({r},{col}) has the same domain {d[0]} as ({row},{col})')
                        return False
            sg = self.getSubGridCell(row, col)
            for r in range(sg.row*3, sg.row*3+3):
                for c in range(sg.col*3, sg.col*3+3):
                    if r != row and c != col and self.grids[r][c] == 0:
                        c_domain = self.getDomain(r, c)
                        if d == c_domain:
                            log.log(
                                f'sub-grid: ({r},{c}) has the same domain {d[0]} as ({row},{col})')
                            return False
        return True

    def registerAll(self):
        ''' register callbacks '''
        # mark start and end
        self.registerRightClick(self.processRightClick)
        # key maps: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
        self.registerKey(self.processDelKey, 'Delete')
        self.registerKey(self.processDelKey, 'Escape')
        # run
        self.registerKey(self.processSpaceKey, 'space')
        self.registerKey(self.processSpaceKey, 'Return')
        # save
        self.registerKey(self.processSaveKey, 's')
        self.registerKey(self.processSaveKey, 'w')
        # load
        self.registerKey(self.processLoadKey, 'l')
        self.registerKey(self.processLoadKey, 'o')
        # level selection
        self.registerKey(self.processEasy, 'e')
        self.registerKey(self.processMedium, 'm')
        self.registerKey(self.processHard, 'd')
        self.registerKey(self.processExpert, 'x')
        self.registerKey(self.processMaster, 't')
        # forward checking for backtracking
        self.registerKey(self.processForward, 'f')
        # backtracking search for CP
        self.registerKey(self.processBacktracking, 'b')
        # help
        self.registerKey(self.processVerbose, 'v')
        self.registerKey(self.processAnimate, 'a')
        self.registerKey(self.showHelp, 'h')

        self.screen.listen()

    def processVerbose(self):
        self.verbose = not self.verbose
        msgbox(f'Detailed animation is {self.verbose and "ON" or "OFF"}')

    def processBacktracking(self):
        self.backtrack = not self.backtrack
        msgbox(f'Backtracking is {self.backtrack and "ON" or "OFF"}')

    def processForward(self):
        self.forward = not self.forward
        msgbox(f'Forward checking is {self.forward and "ON" or "OFF"}')

    def processAnimate(self):
        self.animate = not self.animate
        msgbox(f'Animate is {self.animate and "ON" or "OFF"}')

    def processEasy(self):
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Get a new EASY game?")
        if ask is not None and ask.lower().startswith('y'):
            self.getNewGame(0)

    def processMedium(self):
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Get a new MEDIUM game?")
        if ask is not None and ask.lower().startswith('y'):
            self.getNewGame(1)

    def processHard(self):
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Get a new HARD game?")
        if ask is not None and ask.lower().startswith('y'):
            self.getNewGame(2)

    def processExpert(self):
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Get a new EXPERT game?")
        if ask is not None and ask.lower().startswith('y'):
            self.getNewGame(3)

    def processMaster(self):
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Get a new MASTER game?")
        if ask is not None and ask.lower().startswith('y'):
            self.getNewGame(4)

    def processSaveKey(self):
        ''' save the current map to disk '''
        s = '\n'.join([','.join([str(col) for col in row])
                      for row in self.board])
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        f.write(s)
        f.close()
        msgbox(f'File [{f.name}] has been saved')

    def processLoadKey(self):
        ''' load an existing map '''
        f = filedialog.askopenfile(mode='r', defaultextension='.txt')
        if f is None:
            return
        temp_grid = [[int(x) for x in line.strip().split(',')]
                     for line in f.readlines()]
        f.close()
        self.x_grid_num = len(temp_grid[0])
        self.y_grid_num = len(temp_grid)
        self.setGridNum(self.x_grid_num, self.y_grid_num)
        # set grid num will reset grids matrix
        self.grids = [[x for x in row] for row in temp_grid]
        self.board = [[x for x in row] for row in temp_grid]
        self.drawGrids()
        self.drawGridLines()
        self.ready = True

    def processDelKey(self, x=0, y=0):
        ''' process del/esc keypress'''
        self.processRightClick(x, y)

    def processRightClick(self, x, y):
        ''' record start/end of the searching or reset a cell  '''
        # log.log('in right click')
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Reset the puzzle?")
        if ask is not None and ask.lower().startswith('y'):
            self.reset()

    def processSpaceKey(self):
        ''' space/enter keypress: has been setup properly to call .search() method '''
        if not self.ready:
            msgbox("You need to load a puzzle first!", "COMP712 - Sudoku Demo")
            return
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Sudoku Demo", "Start solve?")
        if ask is not None and ask.lower().startswith('y'):
            # start the search
            self.drawGrids()
            self.drawGridLines()
            if self.solve():
                for row in range(self.y_grid_num):
                    for col in range(self.x_grid_num):
                        self.fillCell(Cell(row, col), self.grids[row][col])
            else:
                msgbox("Cannot solve the puzzle", "COMP712 - Sudoku Demo")


class Pen:
    ''' represent the pen for drawing objects on the canvas '''
    pen_id = 0

    def __init__(self, colour='black', name='') -> None:
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed('fastest')
        self.setColour(colour)
        self.colour = colour
        self.pen.up()
        self.name = name
        if not self.name.strip():
            self.name = f'Pen_{Pen.pen_id}'
            Pen.pen_id += 1

    def __str__(self) -> str:
        return f'Pen({self.name} with colour {self.colour})'

    def setColour(self, colour) -> None:
        ''' change pen colour '''
        try:
            self.pen.color(colour)
            self.pen.fillcolor(colour)
            self.colour = colour
        except:
            WrongParameterError(colour)

    def setPenWidth(self, width):
        ''' change pen width '''
        try:
            self.pen.width(width)
        except:
            WrongParameterError(width)

    def drawLine(self, p1: Point, p2: Point, colour='black'):
        ''' draw a line from p1(x1,y1) to p2(x2,y2) '''
        self.setColour(colour)
        self.pen.up()
        self.pen.goto(p1.x, p1.y)
        self.pen.down()
        self.pen.goto(p2.x, p2.y)
        self.pen.up()
        self.setColour('black')

    def drawBoldLine(self, p1: Point, p2: Point, colour='black', pen_wid=3):
        self.setPenWidth(pen_wid)
        self.drawLine(p1, p2, colour)
        self.setPenWidth(1)

    def drawCircle(self, c: Point, r, colour='black') -> None:
        ''' draw a circle centred at c with radius r '''
        self.setColour(colour)
        # the top-left corner
        self.pen.up()
        self.pen.goto(c.x, c.y)
        self.pen.down()
        self.pen.dot(int(r))
        self.pen.up()
        self.setColour('black')

    def drawSquare(self, c: Point, s, colour='black') -> None:
        ''' draw a square centred at c with edge length s '''
        self.drawRect(c, s, s, colour)

    def drawRect(self, c: Point, w, h, colour='black') -> None:
        ''' draw a rectangle with width w and height h '''
        self.setColour(colour)
        # the bottom-left corner
        self.pen.up()
        self.pen.goto(c.x - w/2, c.y - h/2)
        self.pen.down()
        self.pen.begin_fill()
        for _ in range(2):
            self.pen.forward(w)
            self.pen.left(90)
            self.pen.forward(h)
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.up()
        self.setColour('black')

    def drawCross(self, c, r, colour='black') -> None:
        ''' draw a cross centred at c with length r '''
        p_top_left = Point(c.x-r/2, c.y+r/2)
        p_bot_left = Point(c.x-r/2, c.y-r/2)
        p_top_right = Point(c.x+r/2, c.y+r/2)
        p_bot_right = Point(c.x+r/2, c.y-r/2)
        self.drawLine(p_top_left, p_bot_right, colour)
        self.drawLine(p_bot_left, p_top_right, colour)

    def writeText(self, p: Point, s: str, colour='black', bold=True, font_size=40):
        ''' display text on screen '''
        if not s.strip():
            return
        self.pen.up()
        self.pen.goto(p.x, p.y)
        self.pen.down()
        self.setColour(colour)
        self.pen.write(s, align="center", font=(
            'Monaco', font_size, bold and "bold" or "normal"))
        self.setColour('black')
        self.pen.up()


def clickTest(x, y):
    msgbox(f'Clicking at: ({x},{y})')


if __name__ == '__main__':
    canvas = Canvas('Test GUI Lib Demo', 400, 300)
    print(canvas)
    canvas.setBgColour('red')
    canvas.setSize(500, 500)
    canvas.registerLeftClick(clickTest)
    pen_0 = Pen('red')
    pen_1 = Pen()
    print(canvas)
    print(pen_0)
    print(pen_1)
    pen_0.setColour('blue')
    pen_1.setColour('yellow')
    print(pen_0)
    print(pen_1)
    pen_0.drawCircle(Point(), 20)
    canvas.mainloop()
