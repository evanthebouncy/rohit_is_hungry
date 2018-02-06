import random
import time

from dfa_solver import *
from gen import *

# N_STATES are in N_CHAR


# exp1: 5 states, 3 char, 2500 samples, L=10
# exp2: 5 states, 10 char, 100 samples, L=10
# exp3: 2 states, 15 char, 100 samples, L=2
# exp4: 3 states, 15 char, 2500 samples, L=3
# exp5: 2 states, 15 char, 2500 samples, L=20
# exp6: 3 states, 15 char, 2500 samples, L=20 -> too hard for cegis


'''
results: 
    - states influences solve time most directly
    - char influences number of examples needed (+increases solve time)
    - L influences how long it takes to add an example (+ solve time if long)
'''

def check_solved(synth, all_pairs):
    wrong = []
    for x,y in all_pairs:
        if accept_state(execute_dfa(synth, x)) != y:
            wrong.append((x,y))
    return wrong



class DFA_CEGIS(object):

    def __init__(self, n_states=N_STATES, n_chars=N_CHAR):
        self.solver = DFA_Solver(n_states=n_states, n_chars=n_chars)
        self.n_chars = n_chars
        self.n_states = n_states

    def _reset(self):
        self.solver = DFA_Solver(n_states=self.n_states, n_chars=self.n_chars)

    def solve(self, examples):
        print "Trying to solve with CEGIS..."
        used_examples = []
        k = 0
        (x, y) = random.choice(examples)
        used_examples.append((x,y))
        build_time = 0
        solve_time = 0

        while True:
            print "Adding example {}: ({}, {})".format(k+1, x, y)
            build_start = time.time()
            self.solver.add_example(k, x, y)
            build_time += time.time()-build_start

            solve_start = time.time()
            synth = self.solver.get_matrix()
            solve_time += time.time()-solve_start

            wrong = check_solved(synth, examples)
            if len(wrong) == 0:
                self._reset()
                print "Solved with {} examples in {}s!".format(len(used_examples), build_time+solve_time)
                return synth, used_examples, build_time, solve_time, True

            (x, y) = random.choice(wrong)
            used_examples.append((x,y))
            k += 1


class AddN(object):

    def __init__(self, n_states=N_STATES, n_chars=N_CHAR):
        self.solver = DFA_Solver(n_states=n_states, n_chars=n_chars)
        self.n_chars = n_chars
        self.n_states = n_states

    def solve(self, examples, n):
        print "Trying to solve using {} examples...".format(min(len(examples), n))
        used_examples = []
        solve_time = 0
        # add them randomly
        random.shuffle(examples)

        print "Adding examples..."
        build_start = time.time()
        for k in xrange(n):
            if k >= len(examples):
                break
            (x, y) = examples[k]
            self.solver.add_example(k, x, y)
            used_examples.append((x, y))
        build_time = time.time()-build_start
        print "Added in {}".format(build_time)

        print "Solving..."
        solve_start = time.time()
        synth = self.solver.get_matrix()
        solve_time = time.time()-solve_start
        print "Solved in {}".format(solve_time)

        correct = len(check_solved(synth, examples)) == 0
        correct_str = "correct!" if correct else "not correct..."
        print "Solver was", correct_str

        return synth, used_examples, build_time, solve_time, correct


class Oracle(object):

    def __init__(self, n_states=N_STATES, n_chars=N_CHAR):
        self.solver = DFA_Solver(n_states=n_states, n_chars=n_chars)
        self.n_chars = n_chars
        self.n_states = n_states

    def solve(self, good_examples, examples):
        print "Trying to solve using {} examples...".format(len(good_examples))
        solve_time = 0

        print "Adding examples..."
        build_start = time.time()
        for k, (x, y) in enumerate(good_examples):
            self.solver.add_example(k, x, y)
        build_time = time.time()-build_start
        print "Added in {}".format(build_time)

        print "Solving..."
        solve_start = time.time()
        synth = self.solver.get_matrix()
        solve_time = time.time()-solve_start
        print "Solved in {}".format(solve_time)

        correct = len(check_solved(synth, examples)) == 0
        correct_str = "correct!" if correct else "not correct..."
        print "Solver was", correct_str

        return synth, good_examples, build_time, solve_time, correct


def log_goal(i, goal, num_samples, fname='output'):
    prefix = '\n' if i > 0 else ''
    with open(fname, 'a') as f:
        f.write('{}Trial {}: {} with {} samples\n'.format(prefix, i+1, goal, num_samples))

def log_trial(solver_name, synth, used_examples, build_time, solve_time, correct, fname='output'):
    with open(fname, 'a') as f:
        f.write('{} got {} in ({} build, {} solve): {} total time. Was Solved: {}. Used {} examples.\n'.format(
            solver_name, synth, build_time, solve_time, build_time+solve_time, correct, len(used_examples)
        ))

def run_experiments(num=1, num_samples=2500, fname='output'):

    for i in xrange(num):
        T_sample = sample_matrix()
        examples = generate_examples(T_sample, num_samples)
        log_goal(i, T_sample, num_samples, fname=fname)

#         solver_name = 'Add10'
#         results = AddN().solve(examples, 10)
#         log_trial(solver_name, *results, fname=fname)

        solver_name = 'AddAll'
        results = AddN().solve(examples, len(examples))
        log_trial(solver_name, *results, fname=fname)

        solver_name = 'CEGIS'
        results = DFA_CEGIS().solve(examples)
        log_trial(solver_name, *results, fname=fname)

#         cegis_examples = results[1]
# 
#         solver_name = 'Oracle'
#         results = Oracle().solve(cegis_examples, examples)
#         log_trial(solver_name, *results, fname=fname)





if __name__ == '__main__':
    num = 100
    num_samples = 1000
    fname = '_hi'
    run_experiments(num=num, num_samples=num_samples, fname=fname)


