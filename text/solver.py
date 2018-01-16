from z3 import *


NONSENSE_CONSTANT = 100


def solve_st(pairs):
    '''
    Solves for s and t given x and y

    Args:
        pairs: list of (x, y) tuples
            x: list of ints
            y: list of ints gotten after transforming x
    Returns:
        (s0, s1) and (t0, t1)
    '''
    solver = Solver()
    constraints = []

    s = (Int('s_0'), Int('s_1'))
    t = (Int('t_0'), Int('t_1'))

    for (x,y) in pairs:
        solver.add(solve_one(x, y, s, t, num=0))

    if solver.check() == sat:
        model = solver.model()
        return (model[s[0]], model[s[1]]), (model[t[0]], model[t[1]])
    else:
        print "UNSAT"
        return None, None


def solve_y(x, s, t):
    '''
    Solves for y given x, s, and t

    Args:
        x: list of ints
        s: starting transformation tuple of two ints
        t: ending transformation tuple of two ints
    Returns:
        list of ints resulting from applying transformation
    '''
    solver = Solver()
    constraints = []

    y = [Int('y_{}'.format(i)) for i in xrange(len(x))]

    solver.add(solve_one(x, y, s, t, num=1))

    if solver.check() == sat:
        model = solver.model()
        y_ans = []
        for y_i in y:
            y_val = int(str(model[y_i]))
            if y_val != NONSENSE_CONSTANT:
                y_ans.append(y_val)
        return y_ans
    else:
        print "UNSAT"
        return None


def solve_one(x, y, s, t, num=1):
    '''Creates the constraints for one (x,y) pair to find either y or (s,t)

    Args:
        x: list of ints
        y: list of ints or Z3 Int variables
        s: tuple of two ints or two Z3 int variables
        t: tuple of two ints or two Z3 int variables
        num: unique number of this example

    Returns:
        list of constraints relating x, y, s, and t
    '''
    # pad y so it's the same length as x
    if len(y) == 0 or (len(y) < len(x) and type(y[0]) == int):
        y = y + [NONSENSE_CONSTANT for i in xrange(len(x)-len(y))]
        assert len(x) == len(y)
    constraints = []

    # 1) values in x that match s (sx) or match t (tx)
    sx_arr = [Bool('sx_{}|{}'.format(i, num)) for i in xrange(len(x))]
    tx_arr = [Bool('tx_{}|{}'.format(i, num)) for i in xrange(len(x))]

    for i in xrange(len(x)):
        constraints.append(sx_arr[i] == Or(s[0] == x[i], s[1] == x[i]))
        constraints.append(tx_arr[i] == Or(t[0] == x[i], t[1] == x[i]))


    # 2) s_bar constraints, lowest index matching a value in s
    s_bar = Int('s_bar|{}'.format(num))
    s_all_false = Bool('s_all_false|{}'.format(num))

    # len(x)+1 since need initial s_bar_0 and then another s_bar_i for each value in sx_arr
    s_bar_intermediates = [Int('s_bar_{}|{}'.format(i, num)) for i in xrange(len(x)+1)]

    constraints.append(s_all_false == Not(Or(sx_arr)))
    constraints.append(s_bar_intermediates[0] == NONSENSE_CONSTANT)
    for j in xrange(1, len(s_bar_intermediates)):
        i = len(sx_arr)-j  # i counts len(sx_arr)-1 ... 0
        constraints.append(s_bar_intermediates[j] == If(sx_arr[i], i, s_bar_intermediates[j-1]))

    # if all false then return bad, otherwise lowest found index
    constraints.append(s_bar == If(s_all_false, NONSENSE_CONSTANT, s_bar_intermediates[-1]))


    # 3) t_bar constraints, lowest index matching a value in t that is >= s_bar
    t_bar = Int('t_bar|{}'.format(num))
    t_bar_intermediates = [Int('t_bar_{}|{}'.format(i, num)) for i in xrange(len(x)+1)]

    constraints.append(t_bar_intermediates[0] == NONSENSE_CONSTANT)
    for j in xrange(1, len(t_bar_intermediates)):
        i = len(tx_arr)-j
        constraints.append(t_bar_intermediates[j] == If(And(tx_arr[i], i >= s_bar), i, t_bar_intermediates[j-1]))

    # if s_bar failed then t_bar failed, otherwise lowest found index
    constraints.append(t_bar == If(s_bar == NONSENSE_CONSTANT, NONSENSE_CONSTANT, t_bar_intermediates[-1]))

    # 4) use s and t to map x to y
    copy_idxs = [Int('copy_idxs_{}|{}'.format(i, num)) for i in xrange(len(x))]
    m = [[Int('M_{}_{}|{}'.format(i, j, num)) for j in xrange(len(x))] for i in xrange(len(x))]
    # y_min_helper = [[Int('y_min_helper_{}_{}|{}'.format(i, j, num)) for j in xrange(len(x)+1)] for i in xrange(len(x))]

    # copy_idxs find the index in y of each index in x
    start_copy_index = If(Or(s_bar == NONSENSE_CONSTANT, t_bar == NONSENSE_CONSTANT), NONSENSE_CONSTANT, s_bar)
    constraints.append(copy_idxs[0] == start_copy_index)
    for i in xrange(1, len(copy_idxs)):
        constraints.append(copy_idxs[i] == If(copy_idxs[i-1]+1 <= t_bar, copy_idxs[i-1]+1, NONSENSE_CONSTANT))

    # m is a matrix that maps values in copy_idxs to the values in x
    for i in xrange(len(x)):
        for j in xrange(len(y)):
            constraints.append(m[i][j] == If(j == copy_idxs[i], x[j], NONSENSE_CONSTANT))

    # now use m to map y to the min values of rows in the matrix

    for i in xrange(len(y)):
        # least_y_i_value keeps track of the least value that we've seen so far
        valid_y_value = If(m[i][0] != NONSENSE_CONSTANT, m[i][j], NONSENSE_CONSTANT)
        for j in xrange(len(y)):
            valid_y_value = If(m[i][j] != NONSENSE_CONSTANT, m[i][j], valid_y_value)

        constraints.append(y[i] == valid_y_value)

    return constraints


if __name__ == '__main__':
    # x = [1, 4, 3, 2, 4, 6]
    # y = [4, 3, 2, 4, 6]
    x = [9, 9, 2, 7, 0, 3]
    y = [9, 9, 2, 7, 0, 3]
    #((3, 9), (3, 8))

    print solve_st([(x, y)])