#import pandas as pd
from util import StateViolation, AlphabetViolation, SetFormatError

class DFA:

    def __init__(self,alphabet, Q, init_state, transition_func, final_states):
        self.Q = Q
        self.sigma = alphabet
        self.final_states = []

        if init_state not in Q:
            raise StateViolation("initial state not in Q")
        else:
            self.init_state = init_state

        if not isinstance(final_states,list):
            raise SetFormatError('Final States should be a list')

        for state in final_states:
            if state not in Q:
                raise StateViolation("final state not in Q")
            else:
                self.final_states.append(state)
        
        if self.validate_func(transition_func):
            self.transition_func = transition_func

        self.curr_state = init_state
    
    def validate_func(self, transition_func):

        if isinstance(transition_func, dict):
            # search through keys of transition_func dictionary
            for key in transition_func:
                # each key is a tuple
                # if first val of tuple (init state)
                # not in Q raise error, repeat for dict[key]
                if key[0] not in self.Q:
                    raise StateViolation('state '+key[0]+' not in set Q')
                    return False
                if key[1] not in self.sigma:
                    raise AlphabetViolation('input '+key[1]+' not in sigma(alphabet)')
                    return False
                if transition_func[key] not in self.Q:
                    raise StateViolation('state '+transition_func[key]+' not in set Q')
                    return False
                if isinstance(transition_func[key],list):
                    raise SetFormatError('Target value of transition function DFA has to be a single item, not list')
                    return False
            return True

        else:
            raise ValueError('transition function not valid string, dataframe, or dict type')
    
    def step(self, sym):
        try:
            #print('start state: ', self.curr_state)
            #print('input: ',sym)
            self.curr_state = self.transition_func[(self.curr_state, sym)]
        except KeyError:
            if sym  in self.sigma:
                self.curr_state = 'FAILSTATE'
            else:
                raise AlphabetViolation('input symbol {} is not the alphabet'.format(sym))
        #print('New State: ', self.curr_state)
    
    def consume_input(self, inp):
        for sym in inp:
            if sym in self.sigma:
                self.step(sym)
            else:
                raise AlphabetViolation('input symbol: '+ sym +' not in alphabet')

        if self.curr_state in self.final_states:
            # first reset current state
            self.curr_state = self.init_state
            # then return true, final state achieved
            return True

       # first reset current state
        self.curr_state = self.init_state

        # then return false, final state not achieved
        return False
        

    def to_string(self):
       return 'Finite Set of States Q: '+ str(self.Q) + '\n'
       + 'Finite non-empty Set of symbols (alphabet): '+ str(self.sigma) + '\n'
       + 'Initial State (member of Q): ' + str(self.init_state) + '\n'
       + 'Final states (subset of Q)' + str(self.final_states) + '\n'
       + 'Transition Function - delta (in dictionary Format) ' + str(self.transition_func) + '\n'