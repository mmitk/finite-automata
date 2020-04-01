from util import StateViolation, AlphabetViolation, SetFormatError, powerset, log
from collections import Iterable
from functools import reduce
from dfa import DFA


class NFA():
    def __init__(self, alphabet, Q, init_state, transition_func, final_states):
        # initialize set of states Q and set of symbols (alphabet) sigma
        self.Q = Q
        self.sigma = alphabet

        # set epsilon to string 'eps' , this will be used to represent epsilon, unless changed by the user
        self.eps = 'eps'

        # validate and initialize transition function
        if self.validate_func(transition_func):
            self.transition_func = transition_func

        # validate then initialize initial states to the epsilon closure of the given
        # set of initial states
        if init_state not in Q:
            raise StateViolation('(initial state states) state {} not in set Q'.format(init_state))
        # only single state should be given (i.e. no list, tuple, dictionary, set etc.)
        # strings are acceptable, e.g. 'q1'
        if isinstance(init_state, Iterable) and not isinstance(init_state,str):
            raise SetFormatError('Initial state must not be an iterable type that is not a string type')
        self.init = init_state
        # finding e-closure of initial states makes it smoother to consume input
        # but initial state is seperately saved (above)
        self.init_states = self.e_closure([init_state])
        self.current_states = self.init_states

        # validate then initialize final states
        for state in final_states:
            if state not in self.Q:
                raise StateViolation('(final states) state {} not in set Q'.format(state))
        self.final_states = final_states

        # since none of the current "paths" have been executed
        # NFA has not yet reached final state, and is not yet accepted
        self.accepted = False
    

    def set_eps(self, epsilon):
        """
        Gives user the option to change the symbol used to represent epsilon
        in case the traditional greek epsilon is in the alphabet
        """
        self.eps = epsilon

    def validate_func(self, transition_func):
        """
        validation of the transition function
        the transition function is a dictionary, whose key is a pair containing the current state and input symbol, 
        and whose value is the next or resulting state(s) i.e.
        tf[('current_state','symbol')] == ['target_state']
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
                    raise StateViolation('state '+key[0]+' not in set Q')
                    return False
                if key[1] not in self.sigma and key[1] != self.eps:
                    raise AlphabetViolation('input '+key[1]+' not in sigma(alphabet)')
                    return False
                if not isinstance(transition_func[key],list):
                    raise SetFormatError('Target value of transition function NFA must be a list')
                    return False
                for state in transition_func[key]:
                    if state not in self.Q:
                        raise StateViolation('state '+ state +' not in set Q')
                        return False

            return True

        else:
            raise ValueError('transition function must be valid dict type')

    def e_closure(self, R):
        """
        Find the epsilon closure of a given set of states R 
        MATH DEFINITION
        e-closure: Least set of states such that R is included in e-closure(R)
        an for all states q in R the transition function of (q,epsilon) is a subset
        of the epsilon-closure of R
        """
        eclose = R
        eps = self.eps
        tf = self.transition_func
        for state in R:
            try:
                 [eclose.append(substate)  for  substate in tf[(state, eps)] if substate not in eclose]
            except KeyError:
                continue
        return eclose


    def step(self, sym):
        """
        single step. consumes one symbol, by performing single step transition (which includes epsilon closure)
        for every single "choice"/"branch" 
        the transition function is a dictionary, whose key is a pair containing the current state and input symbol, 
        and whose value is the next or resulting state(s) i.e.
        tf[('current_state','symbol')] == ['target_state]
        """

        new_states = []
        # for each state that is in "current states" i.e. current choices or branches of the NFA,
        # calculate single step transiion using transition function
        for state in self.current_states:
            try:
                [new_states.append(substate) for substate in self.e_closure(self.transition_func[(state, sym)])]
            except KeyError as e:
                if sym in self.sigma:
                    self.curr_state = 'FAILSTATE'
                else:
                    raise AlphabetViolation('input symbol {} is not the alphabet'.format(sym))
        
        for state in new_states:
            if state in self.final_states:
                self.accepted = True
                break
            self.accepted = False

        self.current_states = new_states
        
    def consume_input(self , inp):
        """
        This consumes the input  given to the NFA
        for each symbol in the input, step is called. 
        After input is consumed, if the NFA is in an accepted state then
        it returns true (first reset for next input), otherwise return false
        """
        for sym in inp:
            log('current state: '+str(self.current_states) + 'symbol: '+ sym,type = 0)
            #if sym in self.sigma and not self.accepted:
            if sym in self.sigma:
                self.step(sym)
            else:
                raise AlphabetViolation('input symbol: '+ sym +' not in alphabet')
        
        if self.accepted:
            # reset current states and accepted status then return True
            self.current_states = self.init_states
            self.accepted = False
            return True
        
         # reset current states and accepted status then return false
        self.current_states = self.init_states
        self.accepted = False
        return False

    def to_dfa(self):
        """
        The algorithm used here to transform the NFA into a DFA is as follows:
        (1) Qd = {q0n} add initial state from NFA into set of states Q of new DFA
        (2) for each state in Qd find the resulting state for each symbol from the alphabet using the transition function
        (3) add the new resulting state into Qd then repeat the process
        (4) Once all the states have been checked, the algorithm is finished
        (5) Each new state that contains a final state is itself a final state of the resulting DFA
        """
        # since a list is not hashable (can not be used as key in a dictionary)
        # I am casting it to a frozenset, which is a hashable datatype
        q0 = frozenset(self.init_states)
        Qnew = set([q0]) # Qd is called Qnew
        unchecked = Qnew.copy() # make a copy of Qd
        delta_new = dict() # delta is a dictionary
        final_states = [] 
        sigma_new = self.sigma
        
        while len(unchecked) > 0:
            curr = unchecked.pop()
            for sym in sigma_new:
                try:
                    # obtain the next states using the transition function
                    # new state into hashable frozenset, and add to new transition function and Qnew
                    next_states = reduce(lambda x,y: x|y, [frozenset(self.transition_func[(q,sym)]) for q in curr if (q,sym) in self.transition_func.keys()])
            
                    next_states = frozenset(next_states)
                    delta_new[(curr,sym)] = next_states
                    if next_states not in Qnew:
                        Qnew.add(next_states)
                        unchecked.add(next_states)
                # catch any possible exceptions
                except Exception:
                    continue
        
        for curr in Qnew:
            # check which states in the new DFA contain any final states
            # from the NFA, and add the ones that do to the set of final_states
            if len(curr & frozenset(self.final_states)) > 0:
                final_states.append(curr)

        return DFA(self.sigma, Qnew, q0, delta_new, final_states)

       
        
                    

    def to_screen(self):
        print('Finite Set of States Q: ', str(self.Q))
        print('Finite non-empty Set of symbols (alphabet): ',str(self.sigma))
        print('Initial State (member of Q): ' , str(self.init))
        print('Final states (subset of Q)' ,str(self.final_states))
        print('Transition Function - delta (in dictionary Format, each step is a value in dictionary):')
        for step in self.transition_func:
            print('{} -> {}'.format(str(step),str(self.transition_func[step])))
    
        
