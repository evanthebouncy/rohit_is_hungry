from text_solver import solve_st, solve_y
from gen import *
import random


def test_solve_st():
    print "Testing solving for s and t..."
    failed = []
    for i in xrange(100):
        L = random.randint(1, 50)
        x = get_message(L)
        xform = sample_transform(1)
        # set the replacement to (0, 0) for now
        xform[0] = (xform[0][0], (0,0))
        y = apply_transform(x, xform)
        print '\n{}) Solving for {}->{} with {}'.format(i+1, x, y, xform[0][0])
        s, t = solve_st([(x,y)])
        if s is None or t is None:
            print x
            print xform
            print y
        xform_synth = [((s, t), (0, 0))]
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
        L = random.randint(1, 50)
        x = get_message(L)
        xform = sample_transform(1)
        # set the replacement to (0, 0) for now
        xform[0] = (xform[0][0], (0,0))
        y = apply_transform(x, xform)
        print '\n{}) Solving for {}->{} with {}'.format(i+1, x, y, xform[0][0])
        solved_y = solve_y(x, xform[0][0][0], xform[0][0][1])
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
