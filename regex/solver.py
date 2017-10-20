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

def solve(examples, params2):
    global solve_count
    break_ind = {}
    count = 0
    '''Iteratively goes through all possible examples to find a solution'''
    params = [None for i in xrange(6)] # placeholder
    for p1 in POSSIBLE_PARAMS:
        params[0] = p1
        for p2 in POSSIBLE_PARAMS:
            params[1] = p2
            for p3 in POSSIBLE_PARAMS:
                params[2] = p3
                for p4 in POSSIBLE_PARAMS:
                    params[3] = p4
                    for p5 in POSSIBLE_PARAMS:
                        params[4] = p5
                        for p6 in POSSIBLE_PARAMS:
                            count += 1
                            params[5] = p6
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

        examples_subset = [x for x in examples if random.random() < 0.05]
        
        print params
        # running correct program
        start = time.time()
        ans, break_ind1 = solve(examples, params)
        times.append(time.time()-start)


        # running fraction
        # examples_subset = examples[:100]
        # random.shuffle(examples)

        start = time.time()
        ans, break_ind2 = solve(examples_subset, params)
        times.append(time.time()-start)

        print solve_count
        print break_ind1
        print break_ind2
        ['10', '1', '0', '11', '00', '1']
        # print examples_subset

        bad = False
        counter_examples = []
        for example, label in examples:
            if check_example(ans, example) != label:
                counter_examples.append((example, label))
                bad = True
        print len(examples_subset)
        print len(counter_examples), counter_examples[:5]

        if not bad:
            print 'SUCCESS', ans
        
        print times
