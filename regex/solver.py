from generator import POSSIBLE_PARAMS, check_example


def transform_label(label):
    if type(label) == bool:
        return label
    elif label == -1:
        return False
    elif label == 1:
        return True
    else:
        raise Exception('Bad Label' + str(label))


def solve(examples, params2):
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
                            params[5] = p6
                            for example, label in examples:
                                label = transform_label(label)
                                if check_example(params, example) != label:
                                    break
                            else:
                                return params

    raise Exception('UNSAT!')


if __name__ == '__main__':
    import random
    import time
    from generator import *
    for i in xrange(100):
        times = []
        
        params = generate_params()

        pos_examples = [(generate_positive_example(params), True) for i in xrange(random.randint(100, 500))]
        neg_examples = [(generate_negative_example(params), False) for i in xrange(random.randint(100, 500))]

        examples = pos_examples + neg_examples
        random.shuffle(examples)

        for example, label in examples:
            if check_example(params, example) != label:
                print params, example, label

        print params
        start = time.time()
        ans = solve(examples, params)
        if not check_same_params(params, ans):
            print "Not correct solution", ans
        else:
            print ans
        times.append(time.time()-start)
        print times[-1]
    print sum(times)/len(times)
