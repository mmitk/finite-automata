import pandas as pd
from util import stateViolation

class DFA:

    def __init__(self,alphabet, Q, init_state, transition_func, final_state):
        self.Q = Q
        self.sigma = alphabet
        if init_state not in Q:
            raise stateViolation("initial state not in Q")
        else:
            self.init_state = init_state
        
        ##TODO VALIDATE TRANSITION FUNCTION
        if isinstance(transition_func, pd.DatFrame):
            self.transition_func = transition_func
        elif isinstance(transition_func, str):
            self.transition_func = pd.read_json(transition_func)
        else:
            raise ValueError('transition function not valid filename or dataframe')
        
        if final_state not in Q:
            raise stateViolation("final state not in Q")
        else:
            self.final_state = final_state
        

        