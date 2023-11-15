
import turtle
import random
import time
from enum import Enum
import logging
logging.basicConfig(level=logging.DEBUG)

# --------------------------
# global parameters and setup
# --------------------------

# GUI Setup
turtle.shape("turtle")
turtle.turtlesize(3, 3, 1)
turtle.pensize(2)

# movement speed
turtle.speed(10)


def log(s):
    ''' logging string to command window '''
    logging.debug(s)

# --------------------------
# Behaviour Tree Nodes
# --------------------------


class NodeStatus(Enum):
    ''' Node Status Enum '''
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class ActionNode:
    def __init__(self, name, action_func):
        ''' leaf action node: name and function '''
        pass

    def execute(self):
        ''' perform an action tick '''
        # ----------------------------------------------------------------
        # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
        # ----------------------------------------------------------------
        pass


class SequenceNode:
    def __init__(self, name, nodes):
        ''' sequence composite node: name and node list '''
        self.name = name
        self.nodes = nodes

    def execute(self):
        ''' perform sequence tick '''
        # ----------------------------------------------------------------
        # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
        # ----------------------------------------------------------------
        pass


class SelectorNode:
    def __init__(self, name, nodes):
        ''' selector composite node: name and node list '''
        self.name = name
        self.nodes = nodes

    def execute(self):
        ''' perform selector tick '''
        # ----------------------------------------------------------------
        # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
        # ----------------------------------------------------------------
        pass


class WaitNode:
    def __init__(self, name, wait_s, node) -> None:
        ''' act as a timer: tick the given node for a period of time '''
        self.name = name
        self.wait_s = wait_s
        self.node = node
        self.time_s = 0

    def execute(self):
        ''' perform a timer tick: fail after given time '''
        # ----------------------------------------------------------------
        # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
        # ----------------------------------------------------------------
        pass


class RepeaterNode:
    def __init__(self, name, number, node):
        ''' repeater decorator node: repeat given node tick for specific number of times'''
        self.name = name
        self.number = number
        self.node = node

    def execute(self):
        ''' perform the tick repeatedly '''
        # ----------------------------------------------------------------
        # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
        # ----------------------------------------------------------------
        pass


# --------------------------
# Action functions
# --------------------------


def move_forward():
    ''' command the turtle moving forward '''
    turtle.forward(100)
    return NodeStatus.SUCCESS


def turn_left():
    ''' command the turtle turn left 90 degrees '''
    turtle.left(90)
    return NodeStatus.SUCCESS


def turn_right():
    ''' command the turtle turn right 90 degrees '''
    turtle.right(90)
    return NodeStatus.SUCCESS


def obstacle_in_front():
    # simulating an obstacle in front of the turtle
    # randomly choose between success and failure
    return random.choice([NodeStatus.SUCCESS, NodeStatus.FAILURE])


# --------------------------
# Helper Functions
# --------------------------

def get_new_colour():
    ''' get a random colour '''
    R = random.random()
    B = random.random()
    G = random.random()
    turtle.color(R, G, B)
    return NodeStatus.SUCCESS


def get_new_dir():
    ''' offset the direction '''
    turtle.left(23)
    return NodeStatus.SUCCESS


def change_speed():
    ''' change the speed randomly: [0,10]'''
    global speed
    if random.random() < 0.5:
        return NodeStatus.FAILURE
    speed = random.choice(list(range(11)))
    return NodeStatus.SUCCESS


# --------------------------
# Behaviour Tree Construction
# --------------------------


def main_loop():
    ''' the main logic: construct and simulate the BT '''

    # ----------------------------------------------------------------
    # >>>>>>>> YOUR CODE HERE <<<<<<<<<<
    # ----------------------------------------------------------------

    # don't change
    turtle.done()


# --------------------------
# Behaviour Tree Simulation
# --------------------------
if __name__ == '__main__':
    main_loop()
