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
        inp3 = 'bababaabbba'
        inp4 = 'abababababa'

        try:
            my_auto = dfa.DFA(alpha,Q,init_state,tf,final)
            accept1 = my_auto.consume_input(inp1)
            accept2 = my_auto.consume_input(inp2)
            accept3 = my_auto.consume_input(inp3)
            accept4 = my_auto.consume_input(inp4)
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
        if accept3:
            print(a.format(inp3))
        else:
            print(n.format(inp3))
        if accept4:
            print(a.format(inp4))
        else:
            print(n.format(inp4))
        print('\n')   
        

def multof2(input = None):
    print('Testing DFA, Detect if number of 0\'s is even (multiple of 2)')
    alpha = ['1','0']
    Q = ['q1','q2']
    init_state = 'q1'
    tf = dict()
    tf[('q1','1')] = 'q1'
    tf[('q1','0')] = 'q2'
    tf[('q2','0')] = 'q1'
    tf[('q2','1')] = 'q2'
    final = ['q1']

    a = '{} was accepted by the DFA'
    n = '{} was not accepted by the DFA'

    my_dfa = dfa.DFA(alpha,Q,init_state,tf,final)

    if input is None:
        inputs = ['100100', '1111','10111010','0000','000']
        results = {}
        for inp in inputs:
            try:
                results[inp] = my_dfa.consume_input(inp)
                if results[inp]:
                    print(a.format(inp))
                else:
                    print(n.format(inp))
            except util.stateViolation as e:
                print(e)
    print('\n')        

if __name__ == '__main__':
    aa_substring()
    multof2()