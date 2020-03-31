import util
import dfa
import nfa

#try:
#    raise util.stateViolation('ERROR')
#except util.stateViolation as s:
#    print(s)

#such that 'aa' is a substring
def aa_substring(string = None):
    print('Testing DFA, Detect if \'aa\' is a substring of w')
    sigma = ['a','b']
    Q = ['q1','q2','q3']
    init_state = 'q1'
    delta = dict()
    delta[('q1','a')] = 'q2'
    delta[('q1','b')] = 'q1'
    delta[('q2','a')] = 'q3'
    delta[('q2','b')] = 'q1'
    delta[('q3','a')] = 'q3'
    delta[('q3','b')] = 'q3'
    final = ['q3']

    if input is None:
        inp1 = 'aabbbb'
        inp2 = 'bbbbbbb'
        inp3 = 'bababaabbba'
        inp4 = 'abababababa'

        try:
            my_auto = dfa.DFA(sigma,Q,init_state,delta,final)
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
        

def multof2(string = None):
    print('Testing DFA, Detect if number of 0\'s is even (multiple of 2)')
    sigma = ['1','0']
    Q = ['q1','q2']
    init_state = 'q1'
    delta = dict()
    delta[('q1','1')] = 'q1'
    delta[('q1','0')] = 'q2'
    delta[('q2','0')] = 'q1'
    delta[('q2','1')] = 'q2'
    final = ['q1']

    a = '{} was accepted by the DFA'
    n = '{} was not accepted by the DFA'

    my_dfa = dfa.DFA(sigma,Q,init_state,delta,final)

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

def nfa_01_is_substring():
    print('Testing NFA that accepts input with 01 as a substring')
    eps = 'eps'
    Q = ['q0','q1','q2']
    final = ['q2']
    init = 'q0'
    sig = ['0','1']
    delta = dict()
    delta[('q0','1')] = ['q0']
    delta[('q0','0')] = ['q0','q1']
    delta[('q1','1')] = ['q2']

    mynfa = nfa.NFA(sig, Q, init, delta, final)

    inputs = ['01010111101', '1111','10111010','001','11011']
    for inp in inputs:
        if mynfa.consume_input(inp):
            print('{} was accepted'.format(inp))
        else:
            print('{} was not accepted'.format(inp))
    print('\n\n')

def nfa_1_at_third_or_second(string = None):
    util.log('TEST BEGUN\n1 at 2nd or 3rd\n', 0)
    print('Testing the NFA that accepts input with a 1 at either the third or second from positions from the end')
    eps = 'eps'
    Q = ['q1','q2','q3','q4']
    final = ['q4']
    sigma = ['1','0']
    init = 'q1'
    delta = dict()
    delta[('q1','0')] = ['q1']
    delta[('q1','1')] = ['q1','q2']
    delta[('q2','0')] = ['q3']
    delta[('q2','1')] = ['q3']
    delta[('q2',eps)] = ['q3']
    delta[('q3','0')] = ['q4']
    delta[('q3','1')] = ['q4']
    
    mynfa = nfa.NFA(sigma, Q, init, delta, final)

    if string is None:
        inputs = ['01010111101', '1111','10111010','001','11011','000','100001','11110100001']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    util.log('TEST COMPLETE\n\n\n', 0)



def nfa_to_dfa_simple_test(string = None):
    util.log('TEST BEGUN\n\t\t\t\tTrivial NFA to DFA\n', 0)
    print('Trivial NFA to DFA conversion test, NFA accepts input such that \'aa\' is a substring')
    print('Resulting to_dfa() operation should be essentially equivalent in structure to NFA')

    sigma = ['a','b']
    Q = ['q1','q2','q3']
    init = 'q1'
    delta = dict()
    delta[('q1','a')] = ['q2']
    delta[('q1','b')] = ['q1']
    delta[('q2','a')] = ['q3']
    delta[('q2','b')] = ['q1']
    delta[('q3','a')] = ['q3']
    delta[('q3','b')] = ['q3']
    
    final_states = ['q3']

    mynfa = nfa.NFA(sigma, Q, init, delta, final_states)
    print('The structure of the initial NFA:')
    print(mynfa.to_string())
    print('testing input of NFA:')
    if string is None:
        inputs = ['aabbaa','abababab','baab','bbbbaa']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))


    mydfa = mynfa.to_dfa()
    print('The structure of the resulting DFA:')
    print(mydfa.to_string)
    print('testing same input on the resulting DFA:')
    if string is None:
        inputs = ['aabbaa','abababab','baab','bbbbaa']
        for inp in inputs:
            if mydfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))



if __name__ == '__main__':
    #aa_substring()
   # multof2()
   #nfa_01_is_substring()
   #nfa_1_at_third_or_second()
   nfa_to_dfa_simple_test()