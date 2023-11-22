''' Finite State Machine

    This is a simple FSM implementation
    handlers is a dict of signal->transition map
    startState indicate where to start
    endStates is a group of states that terminate the FSM

    Daniel Zhang @ Falmouth University
    2023-2024
'''


class FSM(object):
    def __init__(self) -> None:
        ''' constructor '''
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.lastState = None
        self.currentState = None

    def add_state(self, name, handler, end_state=0) -> None:
        ''' add a new state to the FSM '''
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name) -> None:
        ''' set up the starting state for the FSM '''
        self.startState = name.upper()
        # self.currentState = self.startState

    def run(self, params) -> None:
        ''' continuously simulate the FSM until it reaches one of the endStates '''
        if self.startState is None:
            raise Exception('.set_start() has to be called before .run()')
        if self.startState not in self.handlers:
            raise Exception('startState handler was not set')
        if len(self.endStates) == 0:
            raise Exception('have to assign at least one end state')

        # start the simulation
        print('\nStarting the simulation...')
        if self.currentState is None:
            handler = self.handlers[self.startState]
        else:
            handler = self.handlers[self.currentState]
        while True:
            # print(f'Last state: {self.lastState}, current state: {self.currentState}')
            self.lastState = self.currentState
            self.currentState, params = handler(params)
            if self.currentState in self.endStates:
                print(f'Final state reached: {self.currentState}')
                break
            elif len(params) == 0:
                print('No more signals to process')
                break
            else:
                handler = self.handlers[self.currentState]

    def __str__(self) -> str:
        ''' response the print() and str() calls '''
        s = f'\nFinite State Machine with {len(self.handlers)} states\n'
        s += f'Transitions are: {self.handlers.keys()}\n'
        s += f'Start state is: {self.startState}\n'
        s += f'End states are: {self.endStates}\n'
        s += f'Last state is: {self.lastState}\n'
        s += f'Current state is: {self.currentState}\n'
        return s
