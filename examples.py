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

    my_auto = dfa.DFA(sigma,Q,init_state,delta,final)
    if string is None:
        inputs = ['aabbbb','bbbbbbb','bababaabbba','abababababa']
        for inp in inputs:
            if my_auto.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if my_auto.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))



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

    if string is None:
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
    else:
        if my_dfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    print('\n')    


def multof2or3(string = None):
    print('Testing DFA, Detect if number of 0\'s is multiple of 2 or 3')
    sigma = ['1','0']
    Q = ['q0','q1','q2','q3','q4','q5']
    init_state = 'q1'
    delta = dict()
    delta[('q0','0')] = 'q1'
    delta[('q0','1')] = 'q0'
    delta[('q1','0')] = 'q2'
    delta[('q1','1')] = 'q1'
    delta[('q2','0')] = 'q3'
    delta[('q2','1')] = 'q2'
    delta[('q3','0')] = 'q4'
    delta[('q3','1')] = 'q3'
    delta[('q4','0')] = 'q5'
    delta[('q4','1')] = 'q4'
    delta[('q5','0')] = 'q0'
    delta[('q5','1')] = 'q5'

    final = ['q0','q2','q3','q4']

    a = '{} was accepted by the DFA'
    n = '{} was not accepted by the DFA'

    my_dfa = dfa.DFA(sigma,Q,init_state,delta,final)

    if string is None:
        inputs = ['100100', '1111','10111010','0000','000']
        for inp in inputs:
            if my_dfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if my_dfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    print('\n') 

def multof3(string = None):
    print('Testing DFA, Detect if number of 0\'s is a multiple of 3')
    sigma = ['1','0']
    Q = ['r1','r2','r3']
    init_state = 'r1'
    delta = dict()
    delta[('r1','0')] = 'r2'
    delta[('r1','1')] = 'r1'
    delta[('r2','0')] = 'r3'
    delta[('r2','1')] = 'r2'
    delta[('r3','0')] = 'r1'
    delta[('r3','1')] = 'r3'


    final = ['r1']

    a = '{} was accepted by the DFA'
    n = '{} was not accepted by the DFA'

    my_dfa = dfa.DFA(sigma,Q,init_state,delta,final)

    if string is None:
        inputs = ['100100', '1111','10111010','0000','000']
        for inp in inputs:
            if my_dfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    
    else:
        if my_dfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    print('\n')       


def nfa_01_is_substring(string = None):
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
    
    if string is None:
        inputs = ['01010111101', '1111','10111010','001','11011']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mynfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    
    print('\n\n')
    mydfa = mynfa.to_dfa()
    print('The structure of the resulting DFA:')
    print(str(mydfa.to_screen()))
    print('testing same input on the resulting DFA:')
    if string is None:
        inputs = ['aabbaa','abababab','baab','bbbbaa']
        for inp in inputs:
            if mydfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mydfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))

    print('\n\n')

def nfa_1_at_third_or_second(string = None):
    print('Testing the NFA, then converting to DFA that accepts input with a 1 at either the third or second from positions from the end')
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
    print('The structure of the initial NFA:')
    print(mynfa.to_screen())
    print('testing input of NFA:')
    if string is None:
        inputs = ['01010111101', '1111','10111010','001','11011','000','100001','11110100001']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mynfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    
    print('\nThe structure of this NFA:')
    mynfa.to_screen()

    print('\nNow the NFA converted into DFA, and resulting DFA structure:')
    mydfa = mynfa.to_dfa()
    mydfa.to_screen()
    print('\nTesting same inputs on resulting DFA:')
    if string is None:
        inputs = ['01010111101', '1111','10111010','001','11011','000','100001','11110100001']
        for inp in inputs:
            if mydfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mydfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))
    


    

def nfa_to_dfa_simple_test(string = None):
    print('Example of NFA to DFA conversion, NFA accepts input such that \'aa\' is a substring')


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
    print(mynfa.to_screen())
    print('testing input of NFA:')
    if string is None:
        inputs = ['aabbaa','abababab','baab','bbbbaa']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mynfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))

    print('\n\n')
    mydfa = mynfa.to_dfa()
    print('The structure of the resulting DFA:')
    print(str(mydfa.to_screen()))
    print('testing same input on the resulting DFA:')
    if string is None:
        inputs = ['aabbaa','abababab','baab','bbbbaa']
        for inp in inputs:
            if mydfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mydfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))


def nfa_an_n_is_even_div_3(string = None):
    print('More complicated NFA to DFA conversion Example, NFA accepts input a^n such that n is even or divisible by three')
    print('As well as NFA example')

    eps = 'eps'
    Q = ['P','Q','R','Q1','R1','R2']
    final = ['Q','R']
    init = 'P'
    sigma = ['a']
    delta = dict()
    delta[('P',eps)] = ['Q','R']
    delta[('Q','a')] = ['Q1']
    delta[('Q1','a')] = ['Q']
    delta[('R','a')] = ['R1']
    delta[('R1','a')] = ['R2']
    delta[('R2','a')] = ['R']


    mynfa = nfa.NFA(sigma, Q, init, delta, final)
    print('The structure of the initial NFA:')
    print(mynfa.to_screen())
    print('testing input of NFA:')
    if string is None:
        inputs = ['aaaa','aaaaa','aaa','a','aaaaaa']
        for inp in inputs:
            if mynfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mynfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))

    print('\n\n')
    mydfa = mynfa.to_dfa()
    print('The structure of the resulting DFA:')
    print(str(mydfa.to_screen()))
    print('testing same input on the resulting DFA:')
    if string is None:
        inputs = ['aaaa','aaaaa','aaa','a','aaaaaa']
        for inp in inputs:
            if mydfa.consume_input(inp):
                print('{} was accepted'.format(inp))
            else:
                print('{} was not accepted'.format(inp))
    else:
        if mydfa.consume_input(string):
            print('{} was accepted'.format(string))
        else:
            print('{} was not accepted'.format(string))



