import turtle
import random
import time
from enum import Enum
import logging
logging.basicConfig(level=logging.DEBUG)

# --------------------------
# global parameters
# --------------------------

length = 100
speed = 10
turn_angle = 23
repeat_num = 4
running_time = 30
pen_size = 2
turtle_size = 3

# GUI Setup
turtle.shape("turtle")
turtle.turtlesize(turtle_size, turtle_size, turtle_size)
turtle.pensize(pen_size)


def log(s):
    ''' logging string to command window '''
    logging.debug(s)


# --------------------------
# Behaviour Tree Nodes
# --------------------------


class NodeStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class ActionNode:
    def __init__(self, name, action_func):
        self.name = name
        self.action_func = action_func

    def execute(self):
        status = self.action_func()
        logging.debug(f'action: {self.name} - {status}')
        return status


class SequenceNode:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

    def execute(self):
        logging.debug(f'execute: {self.name}')
        for node in self.nodes:
            status = node.execute()
            if status != NodeStatus.SUCCESS:
                logging.debug(f'\t{status}')
                return status
        logging.debug(f'\tSUCCESS')
        return NodeStatus.SUCCESS


class SelectorNode:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

    def execute(self):
        logging.debug(f'execute: {self.name}')
        for node in self.nodes:
            status = node.execute()
            if status != NodeStatus.FAILURE:
                logging.debug(f'\t{status}')
                return status
        logging.debug(f'\tFAILURE')
        return NodeStatus.FAILURE


class WaitNode:
    def __init__(self, name, wait_s, node) -> None:
        self.name = name
        self.wait_s = wait_s
        self.node = node
        self.time_s = 0

    def execute(self):
        logging.debug(f'execute: {self.name}')
        if self.time_s < 0:
            logging.debug("\tFAILURE - timer disabled")
            return NodeStatus.FAILURE
        elif self.time_s == 0:
            self.time_s = time.time()
            logging.debug("\tRUNNING - starts timer")
            self.node.execute()
            return NodeStatus.RUNNING
        elif time.time()-self.time_s < self.wait_s:
            logging.debug("\tRUNNING - timer is counting")
            self.node.execute()
            return NodeStatus.RUNNING
        else:
            self.time_s = -1
            logging.debug("\tSUCCESS - timer goes off")
            return NodeStatus.SUCCESS


class RepeaterNode:
    def __init__(self, name, number, node):
        self.name = name
        self.number = number
        self.node = node

    def execute(self):
        logging.debug('-'*20)
        logging.debug(f'execute: {self.name}')
        for _ in range(self.number):
            self.node.execute()
        logging.debug("\tSUCCESS")
        return NodeStatus.SUCCESS


# --------------------------
# Action functions
# --------------------------


def move_forward():
    turtle.forward(length)
    return random.choice([NodeStatus.SUCCESS, NodeStatus.FAILURE])
    return NodeStatus.SUCCESS


def turn_left():
    turtle.left(90)
    return NodeStatus.SUCCESS


def turn_right():
    turtle.right(90)
    return NodeStatus.SUCCESS


def obstacle_in_front():
    # Simulating an obstacle in front of the character
    return random.choice([NodeStatus.SUCCESS, NodeStatus.FAILURE])


# --------------------------
# Helper Functions
# --------------------------

def get_new_colour():
    R = random.random()
    B = random.random()
    G = random.random()
    turtle.color(R, G, B)
    return NodeStatus.SUCCESS


def get_new_dir():
    turtle.left(turn_angle)
    return NodeStatus.SUCCESS


def change_speed():
    global speed
    if random.random() < 0.5:
        return NodeStatus.FAILURE
    speed = random.choice(list(range(11)))
    return NodeStatus.SUCCESS


# --------------------------
# Behaviour Tree Construction
# --------------------------


def main_loop():
    ''' the main logic '''

    # draw one line with random
    draw_line = SelectorNode("Move, Turn, and Random Fail Sequence", [
        SequenceNode("Draw Line and Turn Sequence", [
            ActionNode("Draw Line Action", move_forward),
            ActionNode("Turn Left Action", turn_left)
        ]),
        SequenceNode("Alternate Move Sequence", [
            ActionNode("Turn Left Action", turn_left),
            SelectorNode("Turn Right or Move Forward Selector", [
                ActionNode("Turn Right Action", turn_right),
                ActionNode("Draw Line Action", move_forward)
            ]),
            ActionNode("Turn Left Action", turn_left)
        ]),
        ActionNode("Collide and Wait Action", obstacle_in_front)
    ])

    draw_square = RepeaterNode("Draw Square Repeater", repeat_num, draw_line)

    colour_act = ActionNode("Change Colour", get_new_colour)

    new_dir = ActionNode("Change Direction", get_new_dir)

    many_square = SequenceNode(
        "Draw More Square", [colour_act, new_dir, draw_square])

    wait_root = WaitNode("Wait One Minute", running_time, many_square)

    # draw_line.execute()
    # draw_square.execute()

    while wait_root.execute() != NodeStatus.FAILURE:
        pass

    # Run Behaviour Tree
    # for _ in range(math.floor(360/turn_angle)+1):
    # for _ in range(100):
    #     logging.debug('='*40)
    #     turtle.left(turn_angle)
    #     get_new_colour()
    #     draw_square.execute()

    turtle.done()


# --------------------------
# Behaviour Tree Simulation
# --------------------------
if __name__ == '__main__':
    main_loop()
