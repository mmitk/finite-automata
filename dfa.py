#import pandas as pd
from util import StateViolation, AlphabetViolation, SetFormatError

class DFA:

    def __init__(self,alphabet, Q, init_state, transition_func, final_states):
        """
        DFA class is a progrematic representation of the Deterministic Finite Automota
        It hold true to the mathematical defintion: 
        a tuple of five values 
        (sigma, Q, q0, delta, F)
        sigma being the finite nonempty set of symbols called the alphabet
        Q being the finite nonempty set of states
        qo being the initial state and  member of Q
        delta being the transtion function
        F being the set of final states which is a subset of Q
        """
        # initialize set of states Q and set of symbols (alphabet) sigma
        self.Q = Q
        self.sigma = alphabet
        # initialize final states to an empty list 
        self.final_states = []

        # validate that initial state is a member of Q
        if init_state not in Q:
            raise StateViolation("initial state not in Q")
        else:
            self.init_state = init_state

        # Formatiing Validation
        if not isinstance(final_states,list):
            raise SetFormatError('Final States should be a list')

        # validate that the set final sets F is a subset
        # of Q 
        for state in final_states:
            if state not in Q:
                raise StateViolation("final state not in Q")
            else:
                self.final_states.append(state)
        
        # validate the transition function
        # determinism is validated by virtue of the dictionary data structure
        # only unique keys are able to be initialized in a dictionary
        if self.validate_func(transition_func):
            self.transition_func = transition_func

        self.curr_state = init_state
    
    def validate_func(self, transition_func):
        """
        validation of the transition function
        the transition function is a dictionary, whose key is a pair containing the current state and input symbol, 
        and whose value is the next or resulting state (single state) i.e.
        tf[('current_state','symbol')] == 'target_state'
        this function validates that all states and symbols included in the transition functions are members of Q and sigma respectively
        otherwise errors are raised
        errors are defined in util.py
        """

        if isinstance(transition_func, dict):
            # search through keys of transition_func dictionary
            for key in transition_func:
                # each key is a tuple
                # if first val of tuple (init state)
                # not in Q raise error, repeat for dict[key]
                if key[0] not in self.Q:
                    raise StateViolation('state {} not in set Q'.format(key[0]))
                    return False
                if key[1] not in self.sigma:
                    raise AlphabetViolation('input {} not in sigma(alphabet)'.format(key[1]))
                    return False
                if transition_func[key] not in self.Q:
                    raise StateViolation('state {} not in set Q'.format(transition_func[key]))
                    return False
                if isinstance(transition_func[key],list):
                    raise SetFormatError('Target value of transition function DFA has to be a single item, not list')
                    return False
            return True

        else:
            raise ValueError('transition function not valid string, dataframe, or dict type')
    
    def step(self, sym):
        """
        single step. consumes one symbol, by performing single step transition 
        the transition function is a dictionary, whose key is a pair containing the current state and input symbol, 
        and whose value is the next or resulting state (single state) i.e.
        tf[('current_state','symbol')] == 'target_state
        """
        try:
            self.curr_state = self.transition_func[(self.curr_state, sym)]
        except KeyError:
            if sym  in self.sigma:
                self.curr_state = 'FAILSTATE'
            else:
                raise AlphabetViolation('input symbol {} is not the alphabet'.format(sym))
   
    
    def consume_input(self, inp):
        """
        consumes input given by user
        for each symbol in a given input, performs a single step and consumes symbol
        """
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
        
    
    def to_screen(self):
        print('Finite Set of States Q: ', str(self.Q))
        print('Finite non-empty Set of symbols (alphabet): ',str(self.sigma))
        print('Initial State (member of Q): ' , str(self.init_state))
        print('Final states (subset of Q)' ,str(self.final_states))
        print('Transition Function - delta (in dictionary Format, each step is a value in dictionary):')
        for step in self.transition_func:
             print('{} -> {}'.format(str(step),str(self.transition_func[step])))


    def to_string(self):
       return 'Finite Set of States Q: '+ str(self.Q) + '\n'+ 'Finite non-empty Set of symbols (alphabet): '+ str(self.sigma) + '\n'+ 'Initial State (member of Q): ' + str(self.init_state) + '\n'+ 'Final states (subset of Q)' + str(self.final_states) + '\n'+ 'Transition Function - delta (in dictionary Format) ' + str(self.transition_func) + '\n'