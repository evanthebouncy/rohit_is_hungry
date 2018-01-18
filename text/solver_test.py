from text_solver import solve_st, solve_y
from gen import *
import random


def test_solve_st():
    print "Testing solving for s and t..."
    failed = []
    for i in xrange(100):
        L = random.randint(1, 25)
        x = get_message(L)
        num_params = random.randint(1, 5)
        xform = sample_transform(num_params)
        xform = map(lambda x: (x[0], (0, 0)), xform)
        # set the replacement to (0, 0) for now
        ideal_params = map(lambda x: x[0], xform)
        y = apply_transform(x, xform)
        print '\n{}) Solving for {}->{} with {}'.format(i+1, x, y, ideal_params)
        xform_synth = solve_st([(x,y)], num_params=len(ideal_params))
        if xform_synth is None:
            print "Failed to synth"
            failed.append(i+1)
            continue
        xform_synth = map(lambda x: (x, (0, 0)), xform_synth)
        synthesized_y = apply_transform(x, xform_synth)
        if y != synthesized_y:
            print "Wrong y value!", synthesized_y
            failed.append(i+1)
    if len(failed) == 0:
        print "Passed solving for s and t..."
        return True
    else:
        print "Failed:", failed
        return False


def test_solve_y():
    print "Testing solving for y..."
    failed = []
    for i in xrange(100):
        L = random.randint(1, 25)
        x = get_message(L)
        num_params = random.randint(1, 5)
        xform = sample_transform(num_params)
        # set the replacement to (0, 0) for now
        xform = map(lambda x: (x[0], (0, 0)), xform)
        params = map(lambda x: x[0], xform)
        y = apply_transform(x, xform)
        print '\n{}) Solving for {}->{} with {}'.format(i+1, x, y, params)
        solved_y = solve_y(x, params)
        if y != solved_y:
            print "Wrong y value!", solved_y
            failed.append(i+1)
    if len(failed) == 0:
        print "Passed solving for y..."
        return True
    else:
        print "Failed:", failed
        return False


if __name__ == '__main__':
    st = test_solve_st()
    y = test_solve_y()
    if st and y:
        print "Passed!"
