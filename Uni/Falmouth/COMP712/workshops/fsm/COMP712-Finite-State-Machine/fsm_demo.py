'''
    Finite State Machine (FSM) Workshop Template
    COMP712 Classical Artificial Intelligence: FSM
    Falmouth University, 2023-2024
    Dr Daniel Zhang
    Oct 2023

    Tasks:

    1. complete each transition functions
    2. simulate the FSM state transition process
    3. can you add more states to the model?
    3. create a new script and implement the Vending Machine FSM
'''
from fsm import FSM
from random import choice

def start_transition(signal):
    # YOUR CODE HERE
    pass
    
def red_transition(signal):
    # YOUR CODE HERE
    pass

def green_transition(signal):
    # YOUR CODE HERE
    pass

def amber_transition(signal):
    # YOUR CODE HERE
    pass

def wait_transition(signal):
    # YOUR CODE HERE
    pass

def error_transition(signal):
    # YOUR CODE HERE
    pass

# state -> transition map
states_dict = {'START':start_transition,
                'RED':red_transition,
                'AMBER':amber_transition,
                'GREEN':green_transition,
                'WAIT':wait_transition,
                'ERROR':error_transition}

# action strings
power_action = ['POWER OFF','POWER ON']
error_action = 'SYSTEM ERROR'
action_list = ['POWER OFF','POWER ON','TIME OUT', 'RESTART','PUSH BUTTON','PUSH BUTTON','PUSH BUTTON']

# number of actions to simulate
action_num = 20

if __name__ == '__main__':
    m = FSM()

    # YOU CODE HERE

    # init the FSM

    # construct a feasible action list
    actions = []

    # simulate
    m.run(actions)
        