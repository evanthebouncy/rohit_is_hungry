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

    params = [(s,t)]

    for i, (x,y) in enumerate(pairs):
        solver.add(solve_one(x, y, params, num=i))

    if solver.check() == sat:
        model = solver.model()
        for (s,t) in params:
            solved_s = (int(str(model[s[0]])), int(str(model[s[1]])))
            solved_t = (int(str(model[t[0]])), int(str(model[t[1]])))
            return solved_s, solved_t
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

    params = [(s,t)]

    y = [Int('y_{}'.format(i)) for i in xrange(len(x))]

    solver.add(solve_one(x, y, params, num=1))

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


def solve_one(x, y, params, num=1):
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
    num_params = len(params)
    # pad y so it's the same length as x
    if len(y) == 0 or (len(y) < len(x) and type(y[0]) == int):
        y = y + [NONSENSE_CONSTANT for i in xrange(len(x)-len(y))]
        assert len(x) == len(y)
    constraints = []

    # 1) values in x that match s (sx) or match t (tx)
    sx_arr = [[Bool('sx_{}|{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(num_params)]
    tx_arr = [[Bool('tx_{}|{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(num_params)]

    for i in xrange(num_params):
        s, t = params[i]
        for j in xrange(len(x)):
            constraints.append(sx_arr[i][j] == Or(s[0] == x[j], s[1] == x[j]))
            constraints.append(tx_arr[i][j] == Or(t[0] == x[j], t[1] == x[j]))


    # 2) s_bar constraints, lowest index matching a value in s
    grabs = [(Int('s_bar|{}|{}'.format(k, num)), Int('t_bar|{}|{}'.format(k, num))) for k in xrange(num_params)]
    # s_bar = Int('s_bar|{}'.format(num))
    for i in xrange(num_params):
        s_bar = grabs[i][0]
        s_all_false = Bool('s_all_false|{}|{}'.format(i, num))

        # len(x)+1 since need initial s_bar_0 and then another s_bar_i for each value in sx_arr
        s_bar_intermediates = [Int('s_bar_{}|{}|{}'.format(k, i, num)) for k in xrange(len(x)+1)]
        constraints.append(s_all_false == Not(Or(sx_arr[i])))
        constraints.append(s_bar_intermediates[0] == NONSENSE_CONSTANT)

        for j in xrange(1, len(s_bar_intermediates)):
            k = len(sx_arr[i])-j  # i counts len(sx_arr)-1 ... 0
            constraints.append(s_bar_intermediates[j] == If(sx_arr[i][k], k, s_bar_intermediates[j-1]))

        # if all false then return bad, otherwise lowest found index
        constraints.append(s_bar == If(s_all_false, NONSENSE_CONSTANT, s_bar_intermediates[-1]))

        # 3) t_bar constraints, lowest index matching a value in t that is >= s_bar
        # t_bar = Int('t_bar|{}'.format(num))
        t_bar = grabs[i][1]
        t_bar_intermediates = [Int('t_bar_{}|{}|{}'.format(k, i, num)) for k in xrange(len(x)+1)]

        constraints.append(t_bar_intermediates[0] == NONSENSE_CONSTANT)
        for j in xrange(1, len(t_bar_intermediates)):
            k = len(tx_arr[i])-j
            constraints.append(t_bar_intermediates[j] == If(And(tx_arr[i][k], k >= s_bar), k, t_bar_intermediates[j-1]))

        # if s_bar failed then t_bar failed, otherwise lowest found index
        constraints.append(t_bar == If(s_bar == NONSENSE_CONSTANT, NONSENSE_CONSTANT, t_bar_intermediates[-1]))

    # 4) use s and t to map x to y
    copy_idxs = [Int('copy_idxs_{}|{}'.format(k, num)) for k in xrange(len(x))]
    m = [[Int('M_{}_{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(len(x))]

    # copy_idxs is a list of indices that say where in x each value of y comes from
    prev_c = -1
    for c_i in copy_idxs:
        constraints.append(c_i == _get_next(prev_c, grabs))
        prev_c = c_i


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


def _get_next(c_i, grabs):
    '''creates a constraint for the next copyidx'''
    else_condition = If(True, NONSENSE_CONSTANT, NONSENSE_CONSTANT)
    for (s,t) in grabs[::-1]:
        else_condition = If(And(s!= NONSENSE_CONSTANT, t!= NONSENSE_CONSTANT, c_i+1<=s), s, else_condition)
    return If(Or([And(s <= c_i+1, c_i+1 <=t, s!= NONSENSE_CONSTANT, t!= NONSENSE_CONSTANT) for (s,t) in grabs]), c_i+1, else_condition)


if __name__ == '__main__':
    x = [1, 4, 3, 2, 4, 6]
    y = [4, 3, 2, 4, 6]
    x2 = [3, 1, 6]
    y2 = [3, 1]
    # should print something equivalent to ((4, 3), (6, 1))
    print solve_st([(x, y), (x2, y2)])

    x = [2, 5, 1, 7]
    y = [2, 5, 1, 7]
    # ((9, 2), (7, 9))
    print solve_st([(x, y)])
    
    


