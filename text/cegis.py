from text_solver import solve_st
from gen import *
import random


def find_average(num_params):
    '''finds the average of running 1000 trials'''
    count = 0.
    total = 0.

    for i in xrange(1000):
        print "\nRunning experiment {}...".format(i+1)
        count += 1
        result = cegis(num_params=num_params)
        total += result
        with open('average{}'.format(num_params), 'a') as f:
            f.write(str(result) + '\n')

    return total/count


def check_solved(xform_synth, all_pairs):
    for x,y in all_pairs:
        if apply_transform(x, xform_synth) != y:
            return (x,y)
    return None, None

# takes in M input-output pairs (say 1000)
# measure how many (K) of those M(1000) we need to explain
def cegis(M=1000, num_params=1):
    xform = sample_transform(num_params)
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
        xform_synth = solve_st(examples, num_params=num_params)
        if xform_synth is None:
            raise Exception('UNSAT')
        print "got", xform_synth, "with", len(examples), examples
    return len(examples)

if __name__ == '__main__':
    print find_average(5)