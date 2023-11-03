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
    
    def add_state(self,name,handler,end_state=0) -> None:
        ''' add a new state to the FSM '''
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
    
    def set_start(self, name) -> None:
        ''' set up the starting state for the FSM '''
        self.startState = name.upper()
        self.currentState = self.startState

    def run(self, params) -> None:
        ''' continuously simulate the FSM until it reaches one of the endStates '''

        # try to access the startState's handler
        # it will raise error if not set in advance
        try:
            handler = self.handlers[self.startState]
        except:
            raise Exception('.set_start() has to be called before .run()')
        if not self.endStates:
            raise Exception('have to assign at least one end state')
        
        # start the simulation
        print(f'\nStarting the simulation...')
        while True:
            # print(f'Last state: {self.lastState}, current state: {self.currentState}')
            self.lastState = self.currentState
            self.currentState, params = handler(params)
            if self.currentState in self.endStates:
                print(f'Final state reached: {self.currentState}')
                break
            else:
                handler = self.handlers[self.currentState]
    
    def __str__(self) -> str:
        ''' response the print() and str() calls '''
        s = f'\nFinite State Machine with {len(self.handlers)} states\n'
        s += f'Transitions are: {self.handlers.keys()}\n'
        s += f'Start state is: {self.startState}\n'
        s+= f'End states are: {self.endStates}\n'
        return s