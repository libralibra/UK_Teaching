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
running_time = 120
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
        self.parent = None

    def set_parent(self, name):
        self.parent = name

    def execute(self):
        status = self.action_func()
        log(f'\t action:\t {self.name} - {status}')
        return status


class SequenceNode:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
        self.parent = None
        [x.set_parent(name) for x in self.nodes]

    def set_parent(self, name):
        self.parent = name

    def execute(self):
        if not self.parent:
            log(f'\n======================================== New Tick  ====================================')
        log(f'\t execute:\t {self.name}')
        for node in self.nodes:
            status = node.execute()
            if status != NodeStatus.SUCCESS:
                log(f'\t\t {status}')
                return status
        log('\t\t SUCCESS')
        return NodeStatus.SUCCESS


class SelectorNode:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
        self.parent = None
        [x.set_parent(name) for x in self.nodes]

    def set_parent(self, name):
        self.parent = name

    def execute(self):
        if not self.parent:
            log(f'\n======================================== New Tick  ====================================')
        log(f'\t execute:\t {self.name}')
        for node in self.nodes:
            status = node.execute()
            if status != NodeStatus.FAILURE:
                log(f'\t\t {status}')
                return status
        log('\t\t FAILURE')
        return NodeStatus.FAILURE


class WaitNode:
    def __init__(self, name, wait_s, node) -> None:
        self.name = name
        self.parent = None
        self.wait_s = wait_s
        self.node = node
        self.time_s = 0
        node.set_parent(name)

    def set_parent(self, name):
        self.parent = name

    def execute(self):
        if not self.parent:
            log(f'\n======================================== New Tick  ====================================')
        log(f'\t execute:\t {self.name}')
        if self.time_s < 0:
            log("\t\t FAILURE - timer disabled")
            return NodeStatus.FAILURE
        elif self.time_s == 0:
            self.time_s = time.time()
            log("\t\t RUNNING - starts timer")
            self.node.execute()
            return NodeStatus.RUNNING
        elif time.time()-self.time_s < self.wait_s:
            log("\t\t RUNNING - timer is counting")
            self.node.execute()
            return NodeStatus.RUNNING
        else:
            self.time_s = -1
            log("\t\t SUCCESS - timer goes off")
            return NodeStatus.SUCCESS


class RepeaterNode:
    def __init__(self, name, number, node):
        self.name = name
        self.parent = None
        self.number = number
        self.node = node
        node.set_parent(name)

    def set_parent(self, name):
        self.parent = name

    def execute(self):
        if not self.parent:
            log('\n========================================== New Tick  ======================================')
        log('-'*76)
        log(f'\t execute:\t {self.name}')
        for i in range(self.number):
            log(f'\t repeat:\t number {i+1}')
            self.node.execute()
        log("\t\t SUCCESS")
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
    draw_line = SelectorNode("Move, Turn, and Random Fail Sequence", [
        SequenceNode("Draw Line and Turn Left Sequence", [
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
        "Draw More Squares", [colour_act, new_dir, draw_square])

    wait_root = WaitNode(
        f"Wait {running_time} Seconds", running_time, many_square)

    while wait_root.execute() != NodeStatus.FAILURE:
        pass

    # draw_line.execute()
    # draw_square.execute()

    # no BT version
    # for _ in range(100):
    #     log('='*40)
    #     for _ in range(4):
    #         move_forward()
    #         turn_left()
    #     turtle.left(turn_angle)
    #     get_new_colour()

    turtle.done()


# --------------------------
# Behaviour Tree Simulation
# --------------------------
if __name__ == '__main__':
    main_loop()
