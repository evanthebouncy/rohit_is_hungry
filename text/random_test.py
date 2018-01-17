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
    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    examples = []
    while not check_same(xform, xform_synth):
        L = random.randint(1, 50)
        x = get_message(L)
        y = apply_transform(x, xform)
        examples.append((x, y))
        s, t = solve_st(examples)
        if s is None or t is None:
            raise Exception('UNSAT')
        xform_synth = [((s, t), (0, 0))]
    return len(examples)

def find_average():
    count = 0.
    total = 0.

    for i in xrange(1000):
        count += 1
        result = random_test()
        total += result
        with open('average1', 'a') as f:
            f.write(str(result) + '\n')
    return total/count

if __name__ == '__main__':
    print find_average()