import examples as ex



  

if input('would you like to test the examples with your own input? y/n\n') == 'y':
    inp = True
else:
    inp = False
    
    
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for DFA which takes a\'s and b\'s and accepts input with \'aa\' as a substring\n')
    else:
        string = None
    ex.aa_substring(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for DFA which takes 0\'s and 1\'s and accepts input where number of 0\' is a multiple of 2\n')
    else:
        string = None
    ex.multof2(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for DFA which takes 0\'s and 1\'s and accepts input where number of 0\' is a multiple of 3\n')
    else:
        string = None
    ex.multof3(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for NFA which takes 0\'s and 1\'s and accepts input which ends in \'01\' g\n')
    else:
        string = None
    ex.nfa_01_is_substring(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for NFA which takes 0\'s and 1\'s and accepts input Where there is a 1 in the second or third position from the end\n')
    else:
        string = None
    ex.nfa_1_at_third_or_second(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for NFA (and DFA after conversion) which takes a\'s and b\'s and accepts input such that \'aa\' is a substring\n')
    else:
        string = None
    ex.nfa_to_dfa_simple_test(string)
    print('***********************************************************************')
if input('would you like to see the next example? y/n\n') == 'y' :
    if inp:
        string = input('enter your input for NFA and DFA after conversion which takes a\'s and accepts input Where the number of a\'s is even or divisible by three\n')
    else:
        string = None
    ex.nfa_an_n_is_even_div_3(string)
    print('***********************************************************************')

    print('goodbye')