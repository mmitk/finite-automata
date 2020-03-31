from util import StateViolation, AlphabetViolation, SetFormatError, powerset, log
from collections import Iterable
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
        new_states = []
        for state in self.current_states:
            try:
                [new_states.append(substate) for substate in self.e_closure(self.transition_func[(state, sym)])]
            except KeyError as e:
                #log(e, type = 0)
                #print(self.e_closure(self.transition_func(state, sym)))
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
        for sym in inp:
            log('current state: '+str(self.current_states) + 'symbol: '+ sym,type = 0)
            #if sym in self.sigma and not self.accepted:
            if sym in self.sigma:
                self.step(sym)
            #elif self.accepted:
                #log(self.current_states,type = 0)
                #log('ACCEPTED',type = 0)
                #self.accepted = False
                #return True
            else:
                raise AlphabetViolation('input symbol: '+ sym +' not in alphabet')
        
        if self.accepted:
            log(self.current_states,type = 0)
            log('ACCEPTED',type = 0)
            # reset then return True
            self.current_states = self.init_states
            self.accepted = False
            return True
        
         # reset then return False
        self.current_states = self.init_states
        self.accepted = False
        return False

    def to_dfa(self):
        """
         The set of states Q of a DFA from NFA is the powerset of all states of the NFA
         start with q0

        """
        log(message = '\nTO DFA BEGUN', type = 0,file='nfa_dfa.log')
        Qnew= list()
        Qnew.append(str(self.e_closure(self.init_states)))
        #Qnew.append(str([self.Q[0]]))
        new_init = [self.e_closure(self.init_states)]
        log(message = 'new q0: '+ str(new_init), type = 0,file='nfa_dfa.log')
        new_tf = dict()
        newfinal_states = list()
        breakc = 0
        isfinal = False
        # create new set of states for dfa Qd and new dfa transition_function iteratively
        for dstate in Qnew:
            if breakc == len(Qnew):
                break
            for nstate in dstate:
                for sym in self.sigma:
                    new_dstate = list()
                    if breakc == len(self.sigma):
                        break
                    if (str(dstate), sym) in new_tf.keys():
                        breakc += 1
                        break
                    #for substate in e_closure(self.transition_func(nstate, sym)):
                    try:
                        #TODO
                        #improve break efficiency
                        new_state = [substate for substate in self.e_closure(self.transition_func[(nstate, sym)])]
                        for f in self.final_states:
                            if f in new_state:
                                isfinal = True
                        new_dstate += new_state
                    except KeyError as k:
                        # Testing
                        print(k)
                    new_tf[(str(dstate), sym)] = str(new_dstate)
                    log(message = 'new dstate: '+ str(new_dstate), type = 0,file='nfa_dfa.log')
                    if isfinal:
                        newfinal_states.append(new_dstate)
                        log(message = 'final state: '+ str(new_dstate), type = 0,file='nfa_dfa.log')
                    Qnew.append(new_dstate)


        log(message = '\nCOMPLETED\n\n\n', type = 0,file='nfa_dfa.log')
        return DFA(self.sigma, Qnew, new_init, new_tf, newfinal_states)


    def to_string(self):
        return 'Finite Set of States Q: '+ str(self.Q) + '\n'+ 'Finite non-empty Set of symbols (alphabet): '+ str(self.sigma) + '\n'+ 'Initial State (member of Q): ' + str(self.init) + '\n'+ 'Final states (subset of Q)' + str(self.final_states) + '\n'+ 'Transition Function - delta (in dictionary Format) ' + str(self.transition_func) + '\n'
        
