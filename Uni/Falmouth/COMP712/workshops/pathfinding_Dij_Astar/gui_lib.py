'''
    Python Library for GUI (PIG) to demonstrate pathfinding algorithms using Turtle Module

    Dr Daniel Zhang @ Falmouth University
    2023

    ChangeLog: 

    v 0.0.3 - 27 Nov 2023
        1. add GridColour enum to distinguish different areas
        2. update CellType to reflect the change

    v 0.0.2 - 23 Nov 2023
        1. add grid controls
        2. add key board and mouse click events
        3. enable searching multiple times

    v 0.0.1 - 21 Nov 2023
        1. Initiated the library development for teaching activities
        2. basic function like: draw line, draw circle, draw square, draw rectangle, etc. 

    Note: 
    1. for more colour strings: https://trinket.io/docs/colors
    2. an introduction to tkinter: https://dafarry.github.io/tkinterbook/index.htm

'''

from tkinter import filedialog
import turtle
import logging
logging.basicConfig(level=logging.DEBUG)


class Log:
    def log(self, s):
        logging.info(s)


# global logger
log = Log()

# status of the three special keys
ctrl_flag, shift_flag, alt_flag = False, False, False


def ctrlDown():
    global ctrl_flag
    ctrl_flag = True


def ctrlUp():
    global ctrl_flag
    ctrl_flag = False


def shiftDown():
    global shift_flag
    shift_flag = True


def shiftUp():
    global shift_flag
    shift_flag = False


def altDown():
    global alt_flag
    alt_flag = True


def altUp():
    global alt_flag
    alt_flag = False


class WrongParameterError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        print(f'[##ERROR]: Wrong input parameter {args}')


class CellType:
    ''' hardcoded cell type enums '''
    BLOCK = -1
    EMPTY = 1
    START = 2
    END = 3
    GRASS = 4
    SAND = 5
    WATER = 6


class GridColour:
    ''' grid colour enums
        https://trinket.io/docs/colors
    '''
    BLOCK = 'black'
    EMPTY = 'white'
    START = 'blue'
    END = 'red'
    GRASS = 'spring green'
    SAND = 'orange'
    WATER = 'dodger blue'
    PATH = 'cyan'
    SEARCH = 'gray'


class Point:
    ''' represent a point object (x, y) '''

    def __init__(self, x=0, y=0) -> None:
        self.x, self. y = x, y

    def __str__(self) -> str:
        return f'Point({self.x}, {self.y})'


class Cell:
    ''' represent a matrix indices (row, col) '''

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


def msgbox(message, title='COMP712/Pathfinding Demo'):
    ''' show a modal messagebox '''
    turtle.TK.messagebox.showinfo(title=title, message=message)


def questionBox(title, question):
    ''' yes/no question box, return is string (either "yes" or "no") '''
    return turtle.TK.messagebox.askquestion(title, question)


class Canvas:
    ''' represent the drawing canvas, which actually is a turtle.Screen() object '''

    def __init__(self, title, width, height, bgcolour='white') -> None:
        self.screen = turtle.Screen()
        self.screen.colormode(255)
        self.bgcolour = bgcolour.strip()
        self.title = title
        self.width, self.height = width, height
        # the grid size and grid number
        self.x_grid_size, self.y_grid_size = self.width, self.height
        self.x_grid_num, self.y_grid_num = 1, 1
        self.grids, self.path = [[CellType.EMPTY]], []
        self.start, self.end = None, None
        # press left button for continuous drawing
        self.on_move = False
        # gray colour to highlight the searching process
        self.search_colour = GridColour.SEARCH
        # path colour
        self.path_colour = GridColour.PATH
        # searching in progress
        self.searching = False
        self.registerAll()
        self.init()

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

    def exit(self):
        self.screen.bye()

    def update(self):
        ''' force to update the canvas '''
        self.screen.update()

    def showHelp(self):
        ''' help information messagebox '''
        s = 'BFS Pathfinding Demo\n'
        s += 'Mark START  - The 1st right-click\n'
        s += 'Mark END    - The 2nd right-click\n'
        s += 'Reset Cell  - Right-click on the cell\n'
        s += 'Mark BLOCK  - Left-click\n'
        s += 'Mark GRASS  - CTRL + Left-click\n'
        s += 'Mark SAND   - SHIFT + Left-click\n'
        s += 'Mark WATER  - ALT + Left-click\n'
        s += 'Search Path - SPACE or ENTER\n'
        s += 'New board   - DELETE, ESC, or middle-click\n'
        s += 'Save board  - S or W\n'
        s += 'Load board  - L or O\n'
        s += 'Show help   - H'
        # self.pen.writeText(Point(self.width/25, -self.width/7), s)
        msgbox(s, "Pathfinding Demo Help")

    def clear(self):
        ''' clear the canvas and redraw grid lines '''
        self.screen.clear()
        self.init()
        self.start, self.end = None, None
        self.grids = [[CellType.EMPTY] *
                      self.x_grid_num for _ in range(self.y_grid_num)]
        self.path = []
        self.search_colour = GridColour.SEARCH
        self.searching = False
        self.drawGridLines()
        self.registerAll()
        self.showHelp()

    def setBgColour(self, colour):
        ''' change background colour '''
        self.screen.bgcolor(colour)
        self.bgcolour = colour

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
            self.grids = [[CellType.EMPTY] *
                          self.x_grid_num for _ in range(self.y_grid_num)]
            self.drawGridLines()

    # def setGridSize(self, x_size, y_size):
    #     if 1 <= x_size < self.width and 1 <= y_size < self.height:
    #         self.x_grid_size = x_size
    #         self.y_grid_size = y_size
    #         self.x_grid_num = int(self.width / x_size)
    #         self.y_grid_num = int(self.height / y_size)
    #         self.grids = [[CellType.EMPTY]*self.x_grid_num for _ in range(self.y_grid_num)]
    #         self.drawGridLines()

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

    def getCoordDist(self, p1: Point, p2: Point):
        ''' work out Euclidean distance between 2 points '''
        return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5

    def getGridDist(self, c1: Cell, c2: Cell):
        ''' work out Manhattan distance between 2 cells '''
        return abs(c1.row-c2.row)+abs(c1.col-c2.col)

    def getGridEuclideanDist2(self, c1: Cell, c2: Cell):
        ''' work out Manhattan distance between 2 cells '''
        return (c1.row-c2.row)**2+(c1.col-c2.col)**2

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
        # log.log(
        #     f' Bot left ({x_left,y_bot}) - grid size ({self.x_grid_size, self.y_grid_size})')
        return Cell(int(row), int(col))

    def drawGridLines(self):
        ''' draw the grid lines '''
        if self.x_grid_num > 1 and self.y_grid_num > 1:
            x_half_num, y_half_num = self.x_grid_num/2., self.y_grid_num/2.
            x_left = -x_half_num * self.x_grid_size
            x_right = x_half_num * self.x_grid_size
            y_top = y_half_num * self.y_grid_size
            y_bottom = -y_half_num * self.y_grid_size
            pen = Pen()
            for i in range(self.y_grid_num+1):
                y = y_top - i * self.y_grid_size
                pt_left = Point(x_left, y)
                pt_right = Point(x_right, y)
                pen.drawLine(pt_left, pt_right)
            for i in range(self.x_grid_num+1):
                x = x_left + i * self.x_grid_size
                pt_top = Point(x, y_top)
                pt_bottom = Point(x, y_bottom)
                pen.drawLine(pt_top, pt_bottom)

    def writeText(self, p: Point, s: str, colour='black'):
        ''' write text to canvas'''
        if not s.strip() or not 0 <= p.x <= self.width or not 0 <= p.y <= self.height:
            return
        self.pen.writeText(p, s, colour)

    def colourCell(self, v: Cell, colour, ratio=0.8):
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

    def animateCell(self, c: Cell):
        ''' animate cell colour during the search for special cells '''
        if self.grids[c.row][c.col] != CellType.BLOCK:
            self.colourCell(c, self.search_colour, 0.8)
        self.update()
        if self.grids[c.row][c.col] == CellType.START:
            self.colourCell(c, GridColour.START, 0.8)
        elif self.grids[c.row][c.col] == CellType.END:
            self.colourCell(c, GridColour.END, 0.8)
        elif self.grids[c.row][c.col] == CellType.GRASS:
            self.colourCell(c, GridColour.GRASS, 0.8)
        elif self.grids[c.row][c.col] == CellType.SAND:
            self.colourCell(c, GridColour.SAND, 0.8)
        elif self.grids[c.row][c.col] == CellType.WATER:
            self.colourCell(c, GridColour.WATER, 0.8)
        self.update()

    def drawGrids(self):
        ''' fill a grid with reduced size unless it's the white background '''
        colours = {CellType.BLOCK: GridColour.BLOCK, CellType.EMPTY: GridColour.EMPTY,
                   CellType.START: GridColour.START, CellType.END: GridColour.END,
                   CellType.SAND: GridColour.SAND, CellType.WATER: GridColour.WATER,
                   CellType.GRASS: GridColour.GRASS}
        ratios = {CellType.BLOCK: 0.8, CellType.EMPTY: 1.0,
                  CellType.START: 0.8, CellType.END: 0.8,
                  CellType.SAND: 0.8, CellType.WATER: 0.8,
                  CellType.GRASS: 0.8}
        if len(self.grids) > 0 and len(self.grids[0]) > 0:
            for row in range(len(self.grids)):
                for col in range(len(self.grids[0])):
                    cell = self.grids[row][col]
                    self.colourCell(Cell(row, col),
                                    colours[cell],
                                    ratios[cell])
                    if cell == CellType.START:
                        self.start = Cell(row, col)
                    elif cell == CellType.END:
                        self.end = Cell(row, col)

    def getValidNeighbour(self, c: Cell, direction: str):
        ''' get valid neighbour cells according to the direction'''
        if direction.lower() == 'north' and c.row > 0 and self.grids[c.row-1][c.col] != CellType.BLOCK:
            return Cell(c.row-1, c.col, c)
        if direction.lower() == 'north-east' and c.row > 0 and c.col < self.x_grid_num-1 and self.grids[c.row-1][c.col+1] != CellType.BLOCK:
            return Cell(c.row-1, c.col+1, c)
        if direction.lower() == 'east' and c.col < self.x_grid_num-1 and self.grids[c.row][c.col+1] != CellType.BLOCK:
            return Cell(c.row, c.col+1, c)
        if direction.lower() == 'south-east' and c.row < self.y_grid_num-1 and c.col < self.x_grid_num-1 and self.grids[c.row+1][c.col+1] != CellType.BLOCK:
            return Cell(c.row+1, c.col+1, c)
        if direction.lower() == 'south' and c.row < self.y_grid_num-1 and self.grids[c.row+1][c.col] != CellType.BLOCK:
            return Cell(c.row+1, c.col, c)
        if direction.lower() == 'south-west' and c.row < self.y_grid_num-1 and c.col > 0 and self.grids[c.row+1][c.col-1] != CellType.BLOCK:
            return Cell(c.row+1, c.col-1, c)
        if direction.lower() == 'west' and c.col > 0 and self.grids[c.row][c.col-1] != CellType.BLOCK:
            return Cell(c.row, c.col-1, c)
        if direction.lower() == 'north-west' and c.row > 0 and c.col > 0 and self.grids[c.row-1][c.col-1] != CellType.BLOCK:
            return Cell(c.row-1, c.col-1, c)
        return None

    def registerAll(self):
        ''' register callbacks '''
        # mark block
        self.registerLeftClick(self.processLeftClick)
        # mark start and end
        self.registerRightClick(self.processRightClick)
        # clear
        self.registerMiddleClick(self.processMiddleClick)
        # key maps: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
        self.registerKey(self.processDelKey, 'Delete')
        self.registerKey(self.processDelKey, 'Escape')
        # run
        self.registerKey(self.processSpaceKey, 'space')
        self.registerKey(self.processSpaceKey, 'Return')
        # save
        self.registerKey(self.processSaveKey, 's')
        self.registerKey(self.processSaveKey, 'S')
        self.registerKey(self.processSaveKey, 'w')
        self.registerKey(self.processSaveKey, 'W')
        # load
        self.registerKey(self.processLoadKey, 'l')
        self.registerKey(self.processLoadKey, 'o')
        self.registerKey(self.processLoadKey, 'L')
        self.registerKey(self.processLoadKey, 'O')
        # help
        self.registerKey(self.showHelp, 'h')
        self.registerKey(self.showHelp, 'H')
        # mark special grid
        self.screen.onkeypress(ctrlDown, 'Control_L')
        self.screen.onkeyrelease(ctrlUp, 'Control_L')
        self.screen.onkeypress(shiftDown, 'Shift_L')
        self.screen.onkeyrelease(shiftUp, 'Shift_L')
        self.screen.onkeypress(altDown, 'Alt_L')
        self.screen.onkeyrelease(altUp, 'Alt_L')

        self.screen.listen()

    def processSaveKey(self):
        ''' save the current map to disk '''
        if self.searching:
            return
        s = '\n'.join([','.join([str(col) for col in row])
                      for row in self.grids])
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        f.write(s)
        f.close()
        msgbox(f'File [{f.name}] has been saved')

    def processLoadKey(self):
        ''' load an existing map '''
        if self.searching:
            return
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
        self.grids = temp_grid
        self.drawGrids()
        self.drawGridLines()

    def processDelKey(self, x=0, y=0):
        ''' process del/esc keypress'''
        self.processMiddleClick(x, y)

    def processMiddleClick(self, x, y):
        ''' clear the map '''
        if self.searching:
            return
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Pathfinding Demo", "Clear and restart?")
        if ask is not None and ask.lower().startswith('y'):
            self.clear()

    def processLeftClick(self, x, y):
        ''' left click to mark blocks '''
        global ctrl_flag, shift_flag, alt_flag
        if self.searching:
            return
        pos = self.getGridIndices(x, y)
        if pos:
            # do not change start and end
            if self.start and pos == self.start or self.end and pos == self.end:
                return
            colour = GridColour.BLOCK
            c_type = CellType.BLOCK
            if ctrl_flag:
                colour = GridColour.GRASS
                c_type = CellType.GRASS
            elif shift_flag:
                colour = GridColour.SAND
                c_type = CellType.SAND
            elif alt_flag:
                colour = GridColour.WATER
                c_type = CellType.WATER
            # if self.grids[pos.row][pos.col] == CellType.BLOCK:
            #     return
            self.colourCell(pos, colour, 0.8)
            self.grids[pos.row][pos.col] = c_type

    def processRightClick(self, x, y):
        ''' record start/end of the searching or reset a cell  '''
        # log.log('in right click')
        if self.searching:
            return
        pos = self.getGridIndices(x, y)
        if pos:
            # log.log(f'pos get: ({pos.row},{pos.col})')
            if self.grids[pos.row][pos.col] == CellType.EMPTY:
                # log.log('empty')
                if self.start is None:
                    # log.log('mark start')
                    self.start = pos
                    self.colourCell(pos, GridColour.START, 0.8)
                    self.grids[pos.row][pos.col] = CellType.START
                elif self.end is None:
                    # log.log('mark end')
                    self.end = pos
                    self.colourCell(pos, GridColour.END, 0.8)
                    self.grids[pos.row][pos.col] = CellType.END
                else:
                    msgbox(
                        "Both START and END are ready\nRight-click to reset a cell\nPress SPACE or ENTER to search!\nPress DEL/ESC to clear!\nL to load a map or S to save the current map\nH for help information")
            else:
                # log.log('not empty')
                # log.log(f'cell value: {self.grids[pos.row][pos.col]}')
                if self.grids[pos.row][pos.col] == CellType.START:
                    self.start = None
                elif self.grids[pos.row][pos.col] == CellType.END:
                    self.end = None
                self.colourCell(pos, GridColour.EMPTY, 0.8)
                self.grids[pos.row][pos.col] = CellType.EMPTY

    def processSpaceKey(self):
        ''' space/enter keypress: has been setup properly to call .search() method '''
        if self.searching or self.start is None or self.end is None:
            return
        ask = turtle.TK.messagebox.askquestion(
            "COMP712 - Pathfinding Demo", "Start search?")
        if ask is not None and ask.lower().startswith('y'):
            # start the search
            self.searching = True
            self.drawGrids()
            self.drawGridLines()
            if self.search():
                for v in self.path:
                    c = self.grids[v.row][v.col]
                    colour = self.path_colour
                    if c == CellType.START:
                        colour = GridColour.START
                    elif c == CellType.END:
                        colour = GridColour.END
                    elif c == CellType.BLOCK:
                        colour = GridColour.BLOCK
                    elif c == CellType.GRASS:
                        colour = GridColour.GRASS
                    elif c == CellType.SAND:
                        colour = GridColour.SAND
                    elif c == CellType.WATER:
                        colour = GridColour.WATER
                    self.colourCell(v, colour)
            else:
                msgbox(
                    f"Cannot find path from {self.start} to {self.end}", "COMP712 - Pathfinding Demo")
            self.searching = False


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

    def writeText(self, p: Point, s: str, colour='black'):
        ''' display text on screen '''
        if not s.strip():
            return
        self.pen.up()
        self.pen.goto(p.x, p.y)
        self.pen.down()
        self.setColour(colour)
        self.pen.write(s, align="center", font=('Monaco', 22, "bold"))
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
