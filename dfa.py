import pandas as pd
from util import stateViolation, alphabetViolation

class DFA:

    def __init__(self,alphabet, Q, init_state, transition_func, final_state):
        self.Q = Q
        self.sigma = alphabet

        if init_state not in Q:
            raise stateViolation("initial state not in Q")
        else:
            self.init_state = init_state

        if final_state not in Q:
            raise stateViolation("final state not in Q")
        else:
            self.final_state = final_state

        self.curr_state = init_state
    
    def validate_func(self, transition_func):
        #TODO handle dataframe instance of transition function
        if isinstance(transition_func, pd.DatFrame):
            self.transition_func = transition_func
        elif isinstance(transition_func, str):
            self.transition_func = pd.read_json(transition_func)

        elif isinstance(transition_func, dict):
            # search through keys of transition_func dictionary
            for key in transition_func:
                # each key is a tuple
                # if first val of tuple (init state)
                # not in Q raise error, repeat for dict[key]
                if key[0] not in self.Q:
                    raise stateViolation('state '+key[0]+' not in set Q')
                if key[1] not in self.sigma:
                    raise alphabetViolation('input '+key[1]+' not in sigma(alphabet)')
                if transition_func[key] not in self.Q:
                    raise stateViolation('state '+transition_func[key]+' not in set Q')
        else:
            raise ValueError('transition function not valid string, dataframe, or dict type')
    
    def step(self, sym):
        try:
            self.current_state = self.transition_func[(self.current_state, sym)]
        except KeyError:
            self.current_state = 'FAILSTATE'
    
    def consume_input(self, inp):
        for sym in inp:
            if sym in self.sigma:
                self.step(sym)
            else:
                raise alphabetViolation('input symbol: '+sym+' not in alphabet')
        if isinstance(final_state, list):
            if self.current_state in final_state:
                return True
        else:
            if self.curr_state == final_state:
                return True
        return False
        

        