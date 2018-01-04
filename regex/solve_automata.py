from z3 import *


def sorty(s):
    if '_' in s:
        return int(s.split('=')[0][-2])
    elif 'start' in s:
        return -1
    elif 'end' in s:
        return 1000000

def format_output(s):
    s = map(lambda x: x.strip(), str(s)[1:-1].replace('\n', '').split(','))
    return sorted(s, None, sorty)

def solve(s):
    '''start with just matching (01)*'''
    arr = map(int, s)
    s = Solver()
    
    start = Bool('start')
    end = Bool('end')
    states = [[Bool('0_{}'.format(j)), Bool('1_{}'.format(j))] for j in xrange(len(arr))]

    s.add(start == True)
    s.add(end == True)

    # add transitions
    s.add(Implies(start, states[0][0]))
    for j in xrange(len(arr)-1):
        old_states = states[j]
        next_states = states[j+1]

        s.add(Implies(old_states[0], next_states[1]))
        s.add(Implies(old_states[1], next_states[0]))

    s.add(And(states[-1][1], end))

    # add matching constraints
    for j in xrange(len(arr)):
        if arr[j] == 0:
            s.add(states[j][0] == True)
            s.add(states[j][1] == False)
        else:
            s.add(states[j][0] == False)
            s.add(states[j][1] == True)

    # if s.check() == sat:
    #     print format_output(s.model())
    return s.check()

if __name__ == '__main__':
    assert solve('0101') == sat
    assert solve('010101') == sat
    assert solve('0000') == unsat
    assert solve('01010') == unsat

