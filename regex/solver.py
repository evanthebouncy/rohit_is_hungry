from generator import POSSIBLE_PARAMS, check_example
from util import *
import re

def transform_label(label):
    if type(label) == bool:
        return label
    elif label == -1:
        return False
    elif label == 1:
        return True
    else:
        raise Exception('Bad Label' + str(label))

solve_count = []

# check a set of params against an example set
def check(examples, params):
    auto = Automata(params)
    result = None
    for example, label in examples:
        label = transform_label(label)
        if auto.test_string(example) != label:
            return example, label
            # result = example, label
    # return result
    return None

class RSolver:

  def __init__(self):
    self.params_s = []
    for p1 in unit_gen(0):
      for p2 in unit_gen(1):
        for p3 in unit_gen(2):
          for p4 in unit_gen(3):
            for p5 in unit_gen(4):
              for p6 in unit_gen(5):
                param = [p1,p2,p3,p4,p5,p6]
                self.params_s.append(param)
    self.cur_idx = 0
    self.max_n = len(self.params_s)

  def solve(self, examples):
    while self.cur_idx < self.max_n:
      cur_params = self.params_s[self.cur_idx]
      ce = check(examples, cur_params)
      if ce == None:
        return cur_params
      else:
        self.cur_idx += 1
    raise Exception('UNSAT!')

# def solve(examples):
#     global solve_count
#     break_ind = {}
#     count = 0
#     params = [None for i in xrange(6)]
#     for p1 in unit_gen(0):
#         params[0] = p1
#         for p2 in unit_gen(1):
#             params[1] = p2
#             for p3 in unit_gen(2):
#                 params[2] = p3
#                 for p4 in unit_gen(3):
#                     params[3] = p4
#                     for p5 in unit_gen(4):
#                         params[4] = p5
#                         for p6 in unit_gen(5):
#                             params[5] = p6
#                             count += 1
#                             for i, (example, label) in enumerate(examples):
#                                 label = transform_label(label)
#                                 if check_example(params, example) != label:
#                                     if i not in break_ind:
#                                         break_ind[i] = 1
#                                     else:
#                                         break_ind[i] += 1
#                                     break
#                             else:
#                                 solve_count.append(count)
#                                 return params, break_ind
#     raise Exception('UNSAT!')

def CEGIS(examples):
    solver = RSolver()
    counter_examples = []
    while True:
        candidate_params = solver.solve(counter_examples)
        ce = check(examples, candidate_params) # get all counter examples of candidate_params
        if ce == None:
            print "found solution with ", len(counter_examples)
            # print counter_examples
            return candidate_params, counter_examples
        else:
            counter_examples.append(ce)

if __name__ == '__main__':
    import random
    import time
    from generator import *
    times = []
    for i in xrange(1):
        
        params = generate_params()

        # auto = Automata(params)
        # r_strs = [rand_str() for _ in range(1000)]
        # examples = [(rstr, auto.test_string(rstr)) for rstr in r_strs]
        # print examples[:10]
      
        god_ex = god_example(params), True

        pos_examples = [(generate_positive_example(params), True) for i in xrange(1000)]
        neg_examples = [(generate_negative_example(params), False) for i in xrange(1000)]

        examples = pos_examples + neg_examples 
        random.shuffle(examples)
        
        examples += [god_ex]

        examples_subset = [x for x in examples if random.random() < 0.05]
        
        print "target params ", params
        print god_ex
        # running correct program
        start = time.time()
        ans = RSolver().solve(examples)
        print "inverted params ", ans
        times.append(time.time()-start)

        start = time.time()
        ans = RSolver().solve(examples_subset)
        print "subeset params ", ans
        times.append(time.time()-start)

        start = time.time()
        ans2, oracle_examples = CEGIS(examples)
        print "cegis params ", ans2
        times.append(time.time()-start)

        start = time.time()
        ans3 = RSolver().solve(oracle_examples)
        print "oracular params ", ans3
        times.append(time.time()-start)

        print 'solve counts ', solve_count

        bad = False
        counter_examples = []
        for example, label in examples:
            if check_example(ans, example) != label:
                counter_examples.append((example, label))
                bad = True
        print len(counter_examples), counter_examples[:5]
#         print "short counter examples "
#         for ee, labb in counter_examples:
#             if len(ee) < 20:
#                 print ee, labb

        if bad:
            print 'SUBSET FAILED ', len(examples_subset)
        else:
            print 'SUBSET SUCCESS ', len(examples_subset)
        
        print 'TIMES ', times
        print "cegis counter exmaples "
        print oracle_examples, max([len(x[0]) for x in oracle_examples])
        print "cegis ce index ", [examples.index(x) for x in oracle_examples]

