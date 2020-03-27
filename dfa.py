#import pandas as pd
from util import stateViolation, alphabetViolation, SetFormatError

class DFA:

    def __init__(self,alphabet, Q, init_state, transition_func, final_states):
        self.Q = Q
        self.sigma = alphabet
        self.final_states = []

        if init_state not in Q:
            raise stateViolation("initial state not in Q")
        else:
            self.init_state = init_state

        if not isinstance(final_states,list):
            raise SetFormatError('Final States should be a list')

        for state in final_states:
            if state not in Q:
                raise stateViolation("final state not in Q")
            else:
                self.final_states.append(state)
        
        if self.validate_func(transition_func):
            self.transition_func = transition_func

        self.curr_state = init_state
    
    def validate_func(self, transition_func):
        #TODO handle dataframe instance of transition function
        '''
        if isinstance(transition_func, pd.DatFrame):
            self.transition_func = transition_func
        elif isinstance(transition_func, str):
            self.transition_func = pd.read_json(transition_func)
        '''

        if isinstance(transition_func, dict):
            # search through keys of transition_func dictionary
            for key in transition_func:
                # each key is a tuple
                # if first val of tuple (init state)
                # not in Q raise error, repeat for dict[key]
                if key[0] not in self.Q:
                    raise stateViolation('state '+key[0]+' not in set Q')
                    return False
                if key[1] not in self.sigma:
                    raise alphabetViolation('input '+key[1]+' not in sigma(alphabet)')
                    return False
                if transition_func[key] not in self.Q:
                    raise stateViolation('state '+transition_func[key]+' not in set Q')
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
            self.curr_state = 'FAILSTATE'
        #print('New State: ', self.curr_state)
    
    def consume_input(self, inp):
        for sym in inp:
            if sym in self.sigma:
                self.step(sym)
            else:
                raise alphabetViolation('input symbol: '+ sym +' not in alphabet')

        if self.curr_state in self.final_states:
            # first reset current state
            self.curr_state = self.init_state
            # then return true, final state achieved
            return True

       # first reset current state
        self.curr_state = self.init_state

        # then return false, final state not achieved
        return False
        

        