from text_solver import CEGIS_Solver
from gen import *
import random
import time
import tqdm


def run_experiment(num_params):
    '''runs 1000 trials and outputs to a file'''

    for i in xrange(1000):
        print "\nRunning experiment {}...".format(i+1)
        cegis(num_params=num_params, fname='all{}'.format(num_params), M=25000)

def length_experiment(num_params):
    fname = 'length{}'.format(num_params)
    for i in xrange(100):
        xform = sample_transform(num_params)
        for L in xrange(20):
            if L < 2:
                continue
            with open(fname, 'a') as f:
                f.write(str(L) + ' ')
            all_xs = [get_message(L) for i in xrange(1000)]
            cegis(num_params=num_params, fname=fname, xform=xform, all_xs=all_xs)


def check_solved(xform_synth, all_pairs):
    for x,y in all_pairs:
        if apply_transform(x, xform_synth) != y:
            return (x,y)
    return None, None

# takes in M input-output pairs (say 1000)
# measure how many (K) of those M(1000) we need to explain
# writes to file: 
def cegis(M=1000, num_params=1, fname='output', xform=None, all_xs=None):
    result_str = ''
    start = time.time()
    xform = xform or sample_transform(num_params)
    all_xs = all_xs or [get_message(20) for i in xrange(M)]
    all_pairs = [(x, apply_transform(x, xform)) for x in all_xs]
    
    # print "Trying to find", xform
    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    examples = []

    solver = CEGIS_Solver(num_params)
    build_time = 0
    solve_time = 0

    while True:        
        x,y = check_solved(xform_synth, all_pairs)
        if x is None:
            break
        examples.append((x, y))
        start_build = time.time()
        solver.add(x, y)
        build_time += time.time()-start_build

        start_solve = time.time()
        xform_synth = solver.solve()
        solve_time += time.time()-start_solve
        if xform_synth is None:
            raise Exception('UNSAT')
        # print "got", xform_synth, "with", len(examples), examples

    # write cegis results
    result_str += '{} {} {} '.format(len(examples), build_time, solve_time)

    # pretend oracle just gave all good examples
    print 'solving from oracle...', result_str
    solver = CEGIS_Solver(num_params)
    start_build = time.time()
    for (x, y) in examples:
        solver.add(x, y)
    build_time = time.time()-start_build

    start_solve = time.time()
    xform_synth = solver.solve()
    solve_time = time.time()-start_solve

    if xform_synth is None or check_solved(xform_synth, all_pairs)[0] is not None:
        print xform_synth
        if xform_synth:
            print check_solved(xform_synth, all_pairs)
        print 'Failed to solve from oracle', build_time, solve_time
        build_time = -1
        solve_time = -1

    result_str += '{} {} '.format(build_time, solve_time)

    # now give twice as many examples
    print 'solving from 2x oracle...', result_str
    solver = CEGIS_Solver(num_params)
    # get twice as many examples
    for _ in xrange(len(examples)):
        example = random.choice(all_pairs)
        while example in examples:
            example = random.choice(all_pairs)
        examples.append(example)
    print 'examples ready'
    start_build = time.time()
    for (x, y) in examples:
        solver.add(x, y)
    build_time = time.time()-start_build

    start_solve = time.time()
    xform_synth = solver.solve()
    solve_time = time.time()-start_solve

    if xform_synth is None or check_solved(xform_synth, all_pairs)[0] is not None:
        print xform_synth
        if xform_synth:
            print check_solved(xform_synth, all_pairs)
        print 'Failed to solve from 2x oracle', build_time, solve_time
        build_time = -1
        solve_time = -1
    result_str += '{} {}\n'.format(build_time, solve_time)
    print result_str
    # add all
    # print 'building adding all...', result_str
    # solver = CEGIS_Solver(num_params)
    # start_build = time.time()
    # for (x, y) in tqdm.tqdm(all_pairs):
    #     solver.add(x, y)
    # build_time = time.time()-start_build
    # print 'solving adding all...'
    # start_solve = time.time()
    # xform_synth = solver.solve()
    # solve_time = time.time()-start_solve
    # if xform_synth is None or check_solved(xform_synth, all_pairs)[0] is not None:
    #     raise Exception('Failed to solve all pairs')
    # result_str += '{} {}\n'.format(build_time, solve_time)
    
    with open(fname, 'a') as f:
        f.write(result_str)

def min_cegis(M=1000, num_params=3):
    result_str = ''
    xform = sample_transform(num_params)
    print 'trying to find', xform
    print 'with min of', get_len(xform)
    all_xs = [get_message(10) for i in xrange(M)]
    all_pairs = [(x, apply_transform(x, xform)) for x in all_xs]

    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    examples = []

    solver = CEGIS_Solver(num_params)
    build_time = 0
    solve_time = 0

    while True:
        print 'trying solver with length:', len(examples)
        x,y = check_solved(xform_synth, all_pairs)
        if x is None:
            break
        examples.append((x, y))
        start_build = time.time()
        solver.add(x, y)
        build_time += time.time()-start_build

        start_solve = time.time()
        xform_synth = solver.find_minimal_program()
        solve_time += time.time()-start_solve
        if xform_synth is None:
            raise Exception('UNSAT')

    solver = CEGIS_Solver(num_params)
    xform_synth = [(((-1, -1), (-1, -1)), (-1, -1))]
    build_time2 = 0
    solve_time2 = 0

    # TODO get rid of hack
    examples = [random.choice(all_pairs) for i in xrange(20)]
    for (x, y) in examples:
        solver.add(x, y)

    while True:
        print 'trying solver with length:', len(examples)
        x,y = check_solved(xform_synth, all_pairs)
        if x is None:
            break
        examples.append((x, y))
        start_build = time.time()
        solver.add(x, y)
        build_time2 += time.time()-start_build

        start_solve = time.time()
        xform_synth = solver.find_minimal_program()
        print time.time()-start_solve
        solve_time2 += time.time()-start_solve
        if xform_synth is None:
            raise Exception('UNSAT')

    print 'first took', build_time, solve_time
    print 'second took', build_time2, solve_time2

def get_len(ar):
    ar = str(ar)
    total = 0
    for i in ar:
        try:
            total += int(i)
        except:
            pass
    print total


if __name__ == '__main__':
    min_cegis(num_params=3)
