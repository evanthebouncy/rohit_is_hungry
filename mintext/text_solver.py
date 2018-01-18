from z3 import *


NONSENSE_CONSTANT = 100


class CEGIS_Solver(object):
    """docstring for cegis_solver"""
    def __init__(self, num_params=1):
        super(CEGIS_Solver, self).__init__()
        self.solver = Solver()
        self.solver.set("timeout", 100*1000)
        self.params = [
            (((Int('s_0|{}'.format(i)), Int('s_1|{}'.format(i))),
            (Int('t_0|{}'.format(i)), Int('t_1|{}'.format(i)))),
            (Int('r_0|{}'.format(i)), Int('r_1|{}'.format(i))))
            for i in xrange(num_params)
        ]
        self.size = Int('size')

        all_nums = []
        # size constraint
        for param in self.params:
            grab, r = param
            s, t = grab
            all_nums += [s[0], s[1], t[0], t[1], r[0], r[1]]

        self.solver.add(self.size == Sum(all_nums))        
        self.current_size = 0
        self.counter = 0

    def add(self, x, y):
        self.solver.add(solve_one(x, y, self.params, num=self.counter))
        self.counter += 1

    def solve(self):
        if self.solver.check() == sat:
            model = self.solver.model()
            solved = []

            for (grab, r) in self.params:
                s, t = grab
                solved_s = (int(str(model[s[0]])), int(str(model[s[1]])))
                solved_t = (int(str(model[t[0]])), int(str(model[t[1]])))
                solved_r = (int(str(model[r[0]])), int(str(model[r[1]])))
                solved.append(((solved_s, solved_t), solved_r))
            return solved
        else:
            print "UNSAT"
            return None

    def exist_program_less_than(self, num=30):
        self.solver.push()
        self.solver.add(self.size <= num)
        ans = None
        solved = [(((-1, -1), (-1, -1)), (-1, -1))]
        if self.solver.check() == sat:
            model = self.solver.model()
            ans = model[self.size]
            solved = []

            for (grab, r) in self.params:
                s, t = grab
                solved_s = (int(str(model[s[0]])), int(str(model[s[1]])))
                solved_t = (int(str(model[t[0]])), int(str(model[t[1]])))
                solved_r = (int(str(model[r[0]])), int(str(model[r[1]])))
                solved.append(((solved_s, solved_t), solved_r))
        self.solver.pop()
        return ans, solved

    def find_minimal_program(self):
        for i in range(self.current_size, 1000):
            print 'trying ', i
            ans, solved = self.exist_program_less_than(i)
            if ans is not None:
                self.current_size = i
                return solved


def solve_st(pairs, num_params=1):
    '''
    Solves for s and t given x and y.
    WARNING: the solver gets finicky when len(x) get too large (like > 40)

    Args:
        pairs: list of (x, y) tuples
            x: list of ints
            y: list of ints gotten after transforming x
        num_params: number of (s,t) pairs
    Returns:
        list of ((s,t), r) tuples
    '''
    solver = Solver()
    solver.set("timeout", 15*60*1000)
    constraints = []

    params = [
        (((Int('s_0|{}'.format(i)), Int('s_1|{}'.format(i))),
        (Int('t_0|{}'.format(i)), Int('t_1|{}'.format(i)))),
        (Int('r_0|{}'.format(i)), Int('r_1|{}'.format(i))))
        for i in xrange(num_params)
    ]

    for i, (x,y) in enumerate(pairs):
        solver.add(solve_one(x, y, params, num=i))

    if solver.check() == sat:
        model = solver.model()
        solved = []

        num = 0

        for (grab, r) in params:
            s, t = grab
            solved_s = (int(str(model[s[0]])), int(str(model[s[1]])))
            solved_t = (int(str(model[t[0]])), int(str(model[t[1]])))
            solved_r = (int(str(model[r[0]])), int(str(model[r[1]])))
            solved.append(((solved_s, solved_t), solved_r))
        return solved
    else:
        print "UNSAT"
        return None


def solve_y(x, params):
    '''
    Solves for y given x, s, and t

    Args:
        x: list of ints
        params: list of (s,t) pairs
    Returns:
        list of ints resulting from applying transformation
    '''
    solver = Solver()
    constraints = []

    y = [Int('y_{}'.format(i)) for i in xrange(len(x))]
    solver.add(solve_one(x, y, params, num=0))

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
    # FIRST: WORRY ABOUT GRABBING STRINGS OUT
    num_params = len(params)
    # pad y so it's the same length as x
    if len(y) == 0 or (len(y) < len(x) and type(y[0]) == int):
        y = y + [NONSENSE_CONSTANT for i in xrange(len(x)-len(y))]
        assert len(x) == len(y)
    constraints = []

    for param in params:
        grab, r = param
        s, t = grab
        constraints.append(And(s[0] != NONSENSE_CONSTANT, s[1] != NONSENSE_CONSTANT, 0 <= s[0], 0 <= s[1], s[0] <= 9, s[1] <= 9))
        constraints.append(And(t[0] != NONSENSE_CONSTANT, t[1] != NONSENSE_CONSTANT, 0 <= t[0], 0 <= t[1], t[0] <= 9, t[1] <= 9))
        constraints.append(And(r[0] != NONSENSE_CONSTANT, r[1] != NONSENSE_CONSTANT, 0 <= r[0], 0 <= r[1], r[0] <= 9, r[1] <= 9))

    # 1) values in x that match s (sx) or match t (tx)
    sx_arr = [[Bool('sx_{}|{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(num_params)]
    tx_arr = [[Bool('tx_{}|{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(num_params)]

    for i in xrange(num_params):
        grab, r = params[i]
        s, t = grab
        for j in xrange(len(x)):
            constraints.append(sx_arr[i][j] == Or(s[0] == x[j], s[1] == x[j]))
            constraints.append(tx_arr[i][j] == Or(t[0] == x[j], t[1] == x[j]))


    # 2) s_bar constraints, lowest index matching a value in s
    grabs = [(Int('s_bar|{}|{}'.format(k, num)), Int('t_bar|{}|{}'.format(k, num))) for k in xrange(num_params)]
    prev_t_bars = [Int('prev_t_bar|{}|{}'.format(k, num)) for k in xrange(num_params+1)]
    prev_t_bar = prev_t_bars[0]
    constraints.append(prev_t_bar == -1)
    for i in xrange(num_params):
        s_bar = grabs[i][0]
        s_all_false = Bool('s_all_false|{}|{}'.format(i, num))

        # len(x)+1 since need initial s_bar_0 and then another s_bar_i for each value in sx_arr
        s_bar_intermediates = [Int('s_bar_{}|{}|{}'.format(k, i, num)) for k in xrange(len(x)+1)]
        constraints.append(s_all_false == Not(Or(sx_arr[i])))
        constraints.append(s_bar_intermediates[0] == NONSENSE_CONSTANT)

        for j in xrange(1, len(s_bar_intermediates)):
            k = len(sx_arr[i])-j  # i counts len(sx_arr)-1 ... 0
            constraints.append(s_bar_intermediates[j] == If(And(sx_arr[i][k], k > prev_t_bar), k, s_bar_intermediates[j-1]))

        # if all false then return bad, otherwise lowest found index
        constraints.append(s_bar == If(s_all_false, NONSENSE_CONSTANT, s_bar_intermediates[-1]))

        # 3) t_bar constraints, lowest index matching a value in t that is >= s_bar
        t_bar = grabs[i][1]
        t_bar_intermediates = [Int('t_bar_{}|{}|{}'.format(k, i, num)) for k in xrange(len(x)+1)]

        constraints.append(t_bar_intermediates[0] == NONSENSE_CONSTANT)
        for j in xrange(1, len(t_bar_intermediates)):
            k = len(tx_arr[i])-j
            constraints.append(t_bar_intermediates[j] == If(And(tx_arr[i][k], k >= s_bar), k, t_bar_intermediates[j-1]))

        # if s_bar failed then t_bar failed, otherwise lowest found index
        constraints.append(t_bar == If(s_bar == NONSENSE_CONSTANT, NONSENSE_CONSTANT, t_bar_intermediates[-1]))
        
        # prepare previous t_bar for next iteration
        prev_t_bar = prev_t_bars[i+1]
        constraints.append(prev_t_bar == If(t_bar != NONSENSE_CONSTANT, t_bar, prev_t_bars[i]))

    # 4) use s and t to map x to pre_y (y before transformation)
    copy_idxs = [Int('copy_idxs_{}|{}'.format(k, num)) for k in xrange(len(x))]
    m = [[Int('M_{}_{}|{}'.format(k, k2, num)) for k in xrange(len(x))] for k2 in xrange(len(x))]
    pre_y = [Int('pre_y_{}|{}'.format(k, num)) for k in xrange(len(x))]

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

    for i in xrange(len(pre_y)):
        # least_y_i_value keeps track of the least value that we've seen so far
        valid_y_value = If(m[i][0] != NONSENSE_CONSTANT, m[i][j], NONSENSE_CONSTANT)
        for j in xrange(len(pre_y)):
            valid_y_value = If(m[i][j] != NONSENSE_CONSTANT, m[i][j], valid_y_value)

        constraints.append(pre_y[i] == valid_y_value)

    # NOW WORRY ABOUT REPLACEMENT
    param_mask = [Int('param_mask_{}|{}'.format(k, num)) for k in xrange(len(x))]
    
    # find which param is responsible for each index
    for i in xrange(len(param_mask)):
        param_mask_val = If(True, NONSENSE_CONSTANT, NONSENSE_CONSTANT)
        for j, (s_bar, t_bar) in enumerate(grabs[::-1]):
            k = len(grabs) - j - 1
            param_mask_val = If(And(copy_idxs[i] >= s_bar, copy_idxs[i] <= t_bar, s_bar != NONSENSE_CONSTANT, t_bar != NONSENSE_CONSTANT), k, param_mask_val)
        constraints.append(param_mask[i] == param_mask_val)

    # now map it to y
    for i, y_i in enumerate(y):
        valid_y_value = If(True, pre_y[i], pre_y[i])
        for j in xrange(num_params):
            _, r = params[j]
            valid_y_value = If(And(param_mask[i] == j, r[0] == pre_y[i]), r[1], valid_y_value)
        constraints.append(y_i == valid_y_value)

    return constraints


def _get_next(c_i, grabs):
    '''creates a constraint for the next copyidx'''
    else_condition = If(True, NONSENSE_CONSTANT, NONSENSE_CONSTANT)
    for (s,t) in grabs[::-1]:
        else_condition = If(And(s != NONSENSE_CONSTANT, t != NONSENSE_CONSTANT, c_i+1 <= s), s, else_condition)
    return If(Or([And(s <= c_i+1, c_i+1 <= t, s != NONSENSE_CONSTANT, t != NONSENSE_CONSTANT) for (s,t) in grabs]), c_i+1, else_condition)


if __name__ == '__main__':
    from gen import *
    # x = [1, 4, 3, 2, 4, 6]
    # y = [4, 3, 2, 4, 6]
    # x2 = [3, 1, 6]
    # y2 = [3, 1]
    # # should print something equivalent to ((4, 3), (6, 1))
    # print solve_st([(x, y), (x2, y2)])

    # x = [2, 5, 1, 7, 8, 9]
    # y = [2, 1, 7, 9]
    # y_transformed = [5, 1, 3, 3]
    # # ((9, 2), (7, 9))
    # result = solve_st([(x, y_transformed)], num_params=3)
    # print result
    # print apply_transform(x, result)

    x = [2, 9, 4]
    y = []
    params = [(((5, 7), (4, 2)), (1, 0)), (((1, 7), (5, 3)), (9, 9)), (((8, 5), (4, 1)), (4, 8)), (((5, 9), (8, 0)), (6, 5))]

    print solve_y(x, params)
    result = solve_st([(x, y)], num_params=len(params))
    print result
    print apply_transform(x, result)

    # x = [6, 4, 0, 9, 0, 1, 2, 3, 8, 2, 1, 2, 2, 2, 4]
    # y = [9, 0]
    # params = [(((5, 7), (7, 3)), (0, 0)), (((9, 8), (4, 0)), (0, 0))]
    # synth_y = solve_y(x, params)
    # print y, synth_y
    
    # x = [7, 1, 9, 8, 6, 5, 7, 4, 6]
    # y = [9, 8, 6, 5, 7]

    # ideal = [(((0, 0), (0, 8)), (0, 0)), (((9, 2), (5, 6)), (0, 0)), (((5, 1), (1, 7)), (0, 0))]


    # pairs = [(x,y)]
    # print solve_st(pairs, num_params=len(ideal))
