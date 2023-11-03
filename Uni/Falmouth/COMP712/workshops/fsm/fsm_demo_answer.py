
from fsm import FSM
from random import choice

def start_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: START',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Powered ON, turning RED')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting, turning RED')
    elif theSignal == 'PUSH BUTTON':
        newState = 'START'
        print(f'Not started yet!')
    return (newState,signal[1:])
    
def red_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: RED',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'TIME OUT':
        newState = 'GREEN'
        print(f'Time out, turning GREEN')
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'PUSH BUTTON':
        newState = 'RED'
        print(f'Already RED, no need to WAIT')
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting, remains RED')
    elif theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Already ON, remains RED')
    return (newState,signal[1:])

def green_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: GREEN',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'TIME OUT':
        newState = 'AMBER'
        print(f'Time out, turning AMBER')
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'PUSH BUTTON':
        newState = 'WAIT'
        print(f'Please WAIT')
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting, turning RED')
    elif theSignal == 'POWER ON':
        newState = 'GREEN'
        print(f'Already ON, remains GREEN')
    return (newState,signal[1:])

def amber_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: AMBER',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'TIME OUT':
        newState = 'RED'
        print(f'Time out, turning RED')
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'PUSH BUTTON':
        newState = 'WAIT'
        print(f'Pease WAIT')
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting, turning RED')
    elif theSignal == 'POWER ON':
        newState = 'AMBER'
        print(f'Already ON, remains AMBER')
    return (newState,signal[1:])

def wait_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: WAIT',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'TIME OUT':
        newState = 'AMBER'
        print(f'Time out, turning AMBER')
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'PUSH BUTTON':
        newState = 'WAIT'
        print(f'Already WAIT')
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting, turning RED')
    elif theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Already ON, turning RED')
    return (newState,signal[1:])

def error_transition(signal):
    theSignal = signal[0].upper()
    newState = 'ERROR'
    print(f'Current state: ERROR',end='\t')
    print(f'The signal: {theSignal}',end='\t')
    if theSignal == 'TIME OUT':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'SYSTEM ERROR':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'PUSH BUTTON':
        newState = 'ERROR'
        print(f'Error!')
    elif theSignal == 'RESTART':
        newState = 'RED'
        print(f'Restarting!')
    elif theSignal == 'POWER OFF':
        newState = 'START'
        print(f'Powered OFF, back to START')
    elif theSignal == 'POWER ON':
        newState = 'RED'
        print(f'Already ON, turning RED')
    return (newState,signal[1:])

# states
states_dict = {'START':start_transition,
                'RED':red_transition,
                'AMBER':amber_transition,
                'GREEN':green_transition,
                'WAIT':wait_transition,
                'ERROR':error_transition}

power_action = ['POWER OFF','POWER ON']
error_action = 'SYSTEM ERROR'
action_list = ['POWER OFF','POWER ON','TIME OUT', 'RESTART','PUSH BUTTON','PUSH BUTTON','PUSH BUTTON']
action_num = 20

if __name__ == '__main__':
    m = FSM()
    for s in states_dict.keys():
        if s == 'ERROR':
            m.add_state(s,states_dict[s],1)
        else:
            m.add_state(s,states_dict[s],0)
    m.set_start('START')
    print(m)

    # random actions
    actions = [choice(action_list[:-1]) for _ in range(action_num)]
    # off/on 3 times
    for _ in range(3):
        idx = choice(range(len(actions)))
        actions.insert(idx,'POWER OFF')
        actions.insert(idx+1,'POWER ON')
    # add start and end operation
    actions.insert(0,'POWER ON')
    actions.append('SYSTEM ERROR')
    print(f'The actions are:\n{actions}')

    m.run(actions)
        