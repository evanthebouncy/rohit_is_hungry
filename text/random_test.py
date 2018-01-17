from text_solver import solve_st
from gen import *
import random


def check_same(xform1, xform2):
    '''returns True if two transformations have the same values'''
    return (
        set(xform1[0][0][0]) == set(xform2[0][0][0]) and
        set(xform1[0][0][1]) == set(xform2[0][0][1]) and
        set(xform1[0][1]) == set(xform2[0][1])
    )

def random_test():
    '''Runs an experiment to test how many examples it takes to discover s and t

    Returns:
        int: number of examples to discover s and t
    '''
    xform = sample_transform(1)
    xform[0] = (xform[0][0], (0,0))
    print "Trying to find", xform
    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    examples = []
    while not check_same(xform, xform_synth):
        L = random.randint(1, 10)
        x = get_message(L)
        y = apply_transform(x, xform)
        examples.append((x, y))
        s, t = solve_st(examples)
        if s is None or t is None:
            raise Exception('UNSAT')
        xform_synth = [((s, t), (0, 0))]
        print "got", xform_synth, "with", len(examples), examples
    return len(examples)

def find_average():
    '''finds the average of running 1000 trials'''
    count = 0.
    total = 0.

    for i in xrange(1000):
        print "\nRunning experiment {}...".format(i+1)
        count += 1
        result = random_test()
        total += result
        with open('average1', 'a') as f:
            f.write(str(result) + '\n')

    return total/count
def check_solved(xform_synth, all_pairs):
    for x,y in all_pairs:
        if apply_transform(x, xform_synth) != y:
            return (x,y)
    return None, None

# takes in M input-output pairs (say 1000)
# measure how many (K) of those M(1000) we need to explain
def sort_of_cegis(M=1000):
    xform = sample_transform(1)
    xform[0] = (xform[0][0], (0,0))
    all_xs = [get_message(random.randint(1, 10)) for i in xrange(M)]
    all_pairs = [(x, apply_transform(x, xform)) for x in all_xs]
    
    print "Trying to find", xform
    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    examples = []

    while True:        
        x,y = check_solved(xform_synth, all_pairs)
        if x is None:
            break
        examples.append((x, y))
        s, t = solve_st(examples)
        if s is None or t is None:
            raise Exception('UNSAT')
        xform_synth = [((s, t), (0, 0))]
        print "got", xform_synth, "with", len(examples), examples
    return len(examples)

if __name__ == '__main__':
    print sort_of_cegis()