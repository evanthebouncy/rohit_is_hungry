from generator import POSSIBLE_PARAMS, check_example
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

def solve(examples):
    global solve_count
    break_ind = {}
    count = 0
    params = [None for i in xrange(6)]
    for p1 in unit_gen(0):
        params[0] = p1
        for p2 in unit_gen(1):
            params[1] = p2
            for p3 in unit_gen(2):
                params[2] = p3
                for p4 in unit_gen(3):
                    params[3] = p4
                    for p5 in unit_gen(4):
                        params[4] = p5
                        for p6 in unit_gen(5):
                            params[5] = p6
                            count += 1
                            for i, (example, label) in enumerate(examples):
                                label = transform_label(label)
                                if check_example(params, example) != label:
                                    if i not in break_ind:
                                        break_ind[i] = 1
                                    else:
                                        break_ind[i] += 1
                                    break
                            else:
                                solve_count.append(count)
                                return params, break_ind
    raise Exception('UNSAT!')

def CEGIS(examples):
    counter_examples = []
    while True:
        candidate_params, _ = solve(counter_examples)
        ces = check(examples, candidate_params) # get all counter examples of candidate_params
        if ces == []:
            print "found solution with ", len(counter_examples)
            # print counter_examples
            return candidate_params, counter_examples
        else:
            counter_examples.append(ces[0])


# def get_first_counter(examples, params):
#     counter_examples = []
#     for example, label in examples:
#         if check_example(params, example) != label:
#             counter_examples.append((example, label))
#             return counter_examples
#     return counter_examples


def check(examples, params):
    counter_examples = []
    for example, label in examples:
        if check_example(params, example) != label:
            counter_examples.append((example, label))
    return counter_examples



if __name__ == '__main__':
    import random
    import time
    from generator import *
    times = []
    for i in xrange(1):
        
        params = generate_params()

        pos_examples = [(generate_positive_example(params), True) for i in xrange(500)]
        neg_examples = [(generate_negative_example(params), False) for i in xrange(500)]

        examples = pos_examples + neg_examples
        random.shuffle(examples)

        examples_subset = [x for x in examples if random.random() < 0.01]
        
        print "target params ", params
        # running correct program
        start = time.time()
        ans, break_ind1 = solve(examples)
        print "inverted params ", ans
        times.append(time.time()-start)


        start = time.time()
        ans, break_ind2 = solve(examples_subset)
        print "subeset params ", ans
        times.append(time.time()-start)

        start = time.time()
        ans2, oracle_examples = CEGIS(examples)
        print "cegis params ", ans2
        times.append(time.time()-start)

        start = time.time()
        ans3, _ = solve(oracle_examples)
        print "oracular params ", ans3
        times.append(time.time()-start)

        print 'solve counts ', solve_count
        print 'failure counts ', break_ind1, max(break_ind1.keys())
        print 'failure counts ', break_ind2, max(break_ind2.keys())

        bad = False
        counter_examples = []
        for example, label in examples:
            if check_example(ans, example) != label:
                counter_examples.append((example, label))
                bad = True
        print len(counter_examples), counter_examples[:5]

        if bad:
            print 'SUBSET FAILED'
        else:
            print 'SUBSET SUCCESS'
        
        print times
        print "cegis counter exmaples "
        print oracle_examples

