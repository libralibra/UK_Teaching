import time
from fsm import FSM
import turtle


# ------------------------------------------------------------
# SET UP THE TURTLE
# ------------------------------------------------------------
light_radius = 100
pen = turtle.Turtle()
pen.hideturtle()
pen.speed('fastest')
screen = turtle.Screen()
screen.setup(800, 600)
screen.tracer(False)
turtle.title("COMP712 - Traffic Light FSM Demo")


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------


def draw_rect(pen: turtle.Turtle, c1, w, h, color='blue'):
    ''' draw a filled square with center c1 and size r1 '''
    ori_color = pen.color()[0]
    cx = c1[0]-w/2
    cy = c1[1]+h/2
    pen.up()
    pen.goto(cx, cy)
    pen.down()
    pen.color(color)
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(w)
        pen.right(90)
        pen.forward(h)
        pen.right(90)
    pen.end_fill()
    pen.color(ori_color)


def get_action(x, y):
    ''' get action button from (x,y) position '''
    acts = [act_error, act_power_off, act_power_on,
            act_restart, act_time_out, act_push_button]
    for a in acts:
        if a.x - a.width/2 <= x <= a.x+a.width/2 and a.y-a.height/2 <= y <= a.y+a.height/2:
            print(f'Signal input: {a.name.upper()}')
            return a.name.upper()
    return ''


def draw_square(pen, c1, r1, color='blue'):
    ''' draw a filled square with center c1 and size r1 '''
    draw_rect(pen, c1, r1, r1, color)


def process_info(x, y):
    ''' running fsm '''
    act = get_action(x, y).strip()
    if act:
        m.run([act])
        print(m)


# ------------------------------------------------------------
# STATE CLASS
# ------------------------------------------------------------


class State:
    def __init__(self, color, x, y, name, radius=light_radius) -> None:
        self.color = color
        self.x, self.y = x, y
        self.name = name.strip()
        self.radius = light_radius
        self.pen = turtle.Turtle()
        self.draw()
        self.on = True

    def draw(self, on=True):
        self.pen.hideturtle()
        self.pen.speed('fastest')
        self.pen.up()
        self.pen.goto(self.x, self.y)
        if not on:
            self.pen.dot(self.radius, 'gray')
            self.on = False
        else:
            self.pen.dot(self.radius, self.color)
            self.on = True
        if self.name:
            self.pen.goto(self.pen.xcor(), self.pen.ycor()-20)
            self.pen.write(self.name, align='center',
                           font=('Monaco', 24, "bold"))

    def turn_off(self):
        self.draw(False)

    def turn_on(self):
        self.draw(True)

    def set_color(self, color):
        self.color = color
        self.draw(True)

    def set_name(self, name):
        self.name = name
        self.draw(self.on)

    def switch(self):
        self.draw(not self.on)


# ------------------------------------------------------------
# ACTION CLASS
# ------------------------------------------------------------
class Action:
    def __init__(self, name, x, y, width, height, color) -> None:
        self.name = name
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.color = color
        self.pen = turtle.Turtle()
        self.draw()

    def draw(self):
        self.pen.hideturtle()
        self.pen.speed('fastest')
        draw_rect(self.pen, (self.x, self.y),
                  self.width, self.height, self.color)
        self.pen.goto(self.x, self.y)
        if self.name:
            self.pen.goto(self.pen.xcor(), self.pen.ycor()-20)
            self.pen.write(self.name, align='center',
                           font=('Monaco', 20, "bold"))


# ------------------------------------------------------------
# GLOBAL PARAMS
# ------------------------------------------------------------
line = Action('', -300, 200, 1200, 50, 'black')
beam = Action('', -380, 250, 20, 1200, 'brown')

m = FSM()
red = State('red', -150, 200, 'RED', light_radius)
amber = State('orange', 0, 200, 'AMBER', light_radius)
green = State('green', 150, 200, 'GREEN', light_radius)
wait = State('cyan', -150, 80,  'WAIT', light_radius)
start = State('pink', 0, 80, 'START', light_radius)
error = State('purple', 150, 80, 'ERROR', light_radius)

act_error = Action('SYSTEM ERROR', -250, -80, 200, 100, 'yellow')
act_power_on = Action('POWER ON', 0, -80, 200, 100, 'yellow')
act_power_off = Action('POWER OFF', 250, -80, 200, 100, 'yellow')
act_restart = Action('RESTART', -250, -200, 200, 100, 'yellow')
act_time_out = Action('TIME OUT', 0, -200, 200, 100, 'yellow')
act_push_button = Action('PUSH BUTTON', 250, -200, 200, 100, 'yellow')


# ------------------------------------------------------------
# STATE TRANSITION FUNCTIONS
# ------------------------------------------------------------
def start_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: START', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Powered ON, turning RED')
        red.turn_on()
        start.turn_off()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF!')
        start.turn_on()
    elif theSignal == 'TIME OUT':
        newState = 'START'
        print(f'Not started yet!')
        start.turn_on()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        start.turn_off()
        time.sleep(1)
        start.turn_on()
    elif theSignal == 'PUSH BUTTON':
        newState = 'START'
        print(f'Not started yet!')
        start.turn_on()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
        error.turn_on()
        start.turn_off()
    return (newState, signal[1:])


def red_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: RED', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'TIME OUT':
        newState = 'GREEN'
        print(f'Time out, turning GREEN')
        green.turn_on()
        red.turn_off()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
        error.turn_on()
        red.turn_off()
    elif theSignal == 'PUSH BUTTON':
        newState = 'RED'
        print(f'Already RED, no need to WAIT')
        red.turn_on()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
        start.turn_on()
        red.turn_off()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        red.turn_off()
        start.turn_on()
    elif theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Already ON, remains RED')
        red.turn_on()
    return (newState, signal[1:])


def green_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: GREEN', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'TIME OUT':
        newState = 'AMBER'
        print(f'Time out, turning AMBER')
        amber.turn_on()
        green.turn_off()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
        error.turn_on()
        green.turn_off()
    elif theSignal == 'PUSH BUTTON':
        newState = 'WAIT'
        print(f'Please WAIT')
        wait.turn_on()
        green.turn_off()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
        start.turn_on()
        green.turn_off()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        start.turn_on()
        green.turn_off()
    elif theSignal == 'POWER ON':
        newState = 'GREEN'
        print(f'Already ON, remains GREEN')
        green.turn_on()
    return (newState, signal[1:])


def amber_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: AMBER', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'TIME OUT':
        newState = 'RED'
        print(f'Time out, turning RED')
        red.turn_on()
        amber.turn_off()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
        error.turn_on()
        amber.turn_off()
    elif theSignal == 'PUSH BUTTON':
        newState = 'AMBER'
        print(f'Already waited, remains AMBER')
        amber.turn_on()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
        start.turn_on()
        amber.turn_off()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        start.turn_on()
        amber.turn_off()
    elif theSignal == 'POWER ON':
        newState = 'AMBER'
        print(f'Already ON, remains AMBER')
        amber.turn_on()
    return (newState, signal[1:])


def wait_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: WAIT', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'TIME OUT':
        newState = 'AMBER'
        print(f'Time out, turning AMBER')
        amber.turn_on()
        wait.turn_off()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
        error.turn_on()
        wait.turn_off()
    elif theSignal == 'PUSH BUTTON':
        newState = 'WAIT'
        print(f'Already on WAIT')
        wait.turn_on()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
        start.turn_on()
        wait.turn_off()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        start.turn_on()
        wait.turn_off()
    elif theSignal == 'POWER ON':
        newState = 'WAIT'
        print(f'Already ON, remains WAIT')
        wait.turn_on()
    return (newState, signal[1:])


def error_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: ERROR', end='\t')
    print(f'The signal: {theSignal}', end='\t')
    if theSignal == 'TIME OUT':
        newState = 'ERROR'
        print(f'Remains ERROR!')
        error.turn_on()
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Already on ERROR!')
        error.turn_on()
    elif theSignal == 'PUSH BUTTON':
        newState = 'ERROR'
        print(f'No response on ERROR!')
        error.turn_on()
    elif theSignal == 'RESTART':
        newState = 'START'
        print(f'Restarting!')
        error.turn_off()
        start.turn_on()
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
        error.turn_off()
        start.turn_on()
    elif theSignal == 'POWER ON':
        newState = 'ERROR'
        print(f'Already ON, remains ERROR')
        error.turn_on()
    return (newState, signal[1:])


# ------------------------------------------------------------
# GUI INITIALISATION
# ------------------------------------------------------------


def init():
    ''' initialise FSM and turning all but start OFF '''
    for s in states_dict.keys():
        if s == 'ERROR':
            m.add_state(s, states_dict[s], 1)
        else:
            m.add_state(s, states_dict[s], 0)
    m.set_start('START')
    print(m)
    [b.turn_off() for b in [start, red, amber, green, wait, error]]
    start.turn_on()


# ------------------------------------------------------------
# STATES
# ------------------------------------------------------------
states_dict = {'START': start_transition,
               'RED': red_transition,
               'AMBER': amber_transition,
               'GREEN': green_transition,
               'WAIT': wait_transition,
               'ERROR': error_transition}

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------
if __name__ == '__main__':
    init()
    turtle.onscreenclick(process_info)
    turtle.mainloop()
    turtle.done()
