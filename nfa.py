from util import stateViolation, alphabetViolation, SetFormatError
from dfa import DFA


class NFA(DFA):
    def __init__(self, alphabet, Q, init_state, transiiton_func, final_states):
        super.__init()

    def validate_func(self, transition_func):
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
                if not isinstance(transition_func[key],list):
                    raise SetFormatError('Target value of transition function NFA must be a list')
                    return False
                for state in transition_func[key]:
                    if state not in self.Q:
                        raise stateViolation('state '+ state +' not in set Q')
                        return False

            return True

        else:
            raise ValueError('transition function must be valid dict type')