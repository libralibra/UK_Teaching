""" Pacman, classic arcade game.

Exercises:

1. Change where pacman starts.
2. Change the number of ghosts and their positions. 
3. Make the ghosts with different colours.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter - apply different rules.
6. Modify the game board.
"""

from random import choice
from turtle import *
from freegames import floor, vector

# define the global parameters
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
pellet_size = 4

# pacman parameters
aim = vector(5, 0)
pacman = vector(-40, -80)

# ghost parameters
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# use 1D list to represent the 2D space
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def draw_grid(x: int, y: int) -> None:
    """ Draw a grid (one tile) using path at (x, y). """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for _ in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()


def get_coords(index: int) -> vector:
    ''' convert from 1d index to 2d coordinates '''
    x = (index % 20) * 20 - 200
    y = 180 - (index // 20) * 20
    return vector(x, y)


def get_index(p: vector) -> int:
    """ Return offset of point in tiles: the index of the point """
    # column
    x = (floor(p.x, 20) + 200) / 20
    # row
    y = (180 - floor(p.y, 20)) / 20
    return int(x + y * 20)


def is_valid(p: vector) -> bool:
    """ Return True if point is is_valid in tiles. """
    index = get_index(p)
    if tiles[index] == 0:
        return False
    index = get_index(p + 19)
    if tiles[index] == 0:
        return False
    return p.x % 20 == 0 or p.y % 20 == 0


def draw_dot(p: vector, c: str, s=20, pen=None) -> None:
    ''' draw either the pacman or the ghost at vector P(x,y) with size s and colour c, if no pen was defined, use the global pen '''
    if pen:
        pen.up()
        pen.goto(p.x + 10, p.y + 10)
        pen.dot(s, c)
    else:
        up()
        goto(p.x + 10, p.y + 10)
        dot(s, c)


def draw_board():
    """ Draw board using path. """
    bgcolor('black')
    path.color('green')
    # each tile
    for index, tile in enumerate(tiles):
        if tile > 0:
            p = get_coords(index)
            draw_grid(p.x, p.y)
            if tile == 1:
                draw_dot(p, 'white', pellet_size, path)


def random_direction():
    ''' return a vector represent the random movement '''
    options = [
        vector(5, 0),
        vector(-5, 0),
        vector(0, 5),
        vector(0, -5)]
    return choice(options)


def change(x, y):
    """ Change pacman aim if is_valid ."""
    if is_valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


def play():
    """ Move pacman and all ghosts. """
    writer.undo()
    writer.write(state['score'], font=('Monaco', 20, "bold"))
    clear()

    # move pacman
    if is_valid(pacman + aim):
        pacman.move(aim)

    index = get_index(pacman)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        p = get_coords(index)
        draw_grid(p.x, p.y)

    draw_dot(pacman, 'yellow')

    for point, direction in ghosts:
        if is_valid(point + direction):
            point.move(direction)
        else:
            new_dir = random_direction()
            direction.x = new_dir.x
            direction.y = new_dir.y
        draw_dot(point, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(play, 100)


def init():
    ''' initialise the board '''
    setup(420, 420)
    hideturtle()
    tracer(False)
    title('COMP712/Rule-based AI - PACMAN: Falmouth University, 2023-2024')
    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'], font=('Monaco', 20, "bold"))


def keyboard():
    ''' listen to keyboard events '''
    listen()
    onkey(lambda: change(5, 0), 'Right')
    onkey(lambda: change(-5, 0), 'Left')
    onkey(lambda: change(0, 5), 'Up')
    onkey(lambda: change(0, -5), 'Down')


if __name__ == '__main__':
    init()
    keyboard()
    draw_board()
    play()
    done()
