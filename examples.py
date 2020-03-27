import util
import dfa

#try:
#    raise util.stateViolation('ERROR')
#except util.stateViolation as s:
#    print(s)

#such that 'aa' is a substring
def aa_substring(input = None):
    print('Testing DFA, Detect if \'aa\' is a substring of w')
    alpha = ['a','b']
    Q = ['q1','q2','q3']
    init_state = 'q1'
    tf = dict()
    tf[('q1','a')] = 'q2'
    tf[('q1','b')] = 'q1'
    tf[('q2','a')] = 'q3'
    tf[('q2','b')] = 'q1'
    tf[('q3','a')] = 'q3'
    tf[('q3','b')] = 'q3'
    final = ['q3']

    if input is None:
        inp1 = 'aabbbb'
        inp2 = 'bbbbbbb'

        try:
            my_auto = dfa.DFA(alpha,Q,init_state,tf,final)
            accept1 = my_auto.consume_input(inp1)
            accept2 = my_auto.consume_input(inp2)
        except util.stateViolation as e:
            print(e)

        a = '{} was accepted by the DFA'
        n = '{} was not accepted by the DFA'
        if accept1:
            print(a.format(inp1))
        else:
            print(n.format(inp1))
        if accept2:
            print(a.format(inp2))
        else:
            print(n.format(inp2))
        



if __name__ == '__main__':
    aa_substring()