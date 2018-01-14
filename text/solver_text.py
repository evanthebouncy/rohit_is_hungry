from z3 import *


BIG_CONSTANT = 200000000

def min2(x, y):
    return If(x < y, x, y)

def sbarcalc(sx_list, x, y):
    sbar = If(sx_list[0], 0, BIG_CONSTANT)
    for i in xrange(1, len(sx_list)):
        sbar = If(And(i < sbar, sx_list[i], x[i] == y[0]), i, sbar)
    return sbar

def tbarcalc(tx_list, sbar):
    tbar = If(And(tx_list[0], 0 >= sbar), 0, BIG_CONSTANT)
    for i in xrange(1, len(tx_list)):
        tbar = If(And(i < tbar, tx_list[i], i >= sbar), i, tbar)
    return tbar

def solve():
    solver = Solver()
    x = [1, 4, 3, 2, 4, 6]
    y = [4, 3, 2, 4, 6, -1]
    assert len(x) == len(y)

    constraints = []

    constraints += solve_one(x, y)

    solver.add(constraints)

    if solver.check() == sat:
        model = solver.model()
        print model
    else:
        print "UNSAT"

def solve_one(x, y, num=1):
    constraints = []    

    s = (Int('s_0_{}'.format(num)), Int('s_1_{}'.format(num)))
    # constraints.append(s[0] == 4)
    # constraints.append(s[1] == 3)
    t = (Int('t_0_{}'.format(num)), Int('t_1_{}'.format(num)))
    # constraints.append(t[0] == 6)
    # constraints.append(t[1] == 1)
    last_y_ind = Int('last_y_ind_{}'.format(num))

    # 0) find last_y
    last_y_constraint = If(True, 0, 0)
    for i in xrange(1, len(y)):
        last_y_constraint = If(y[i] != -1, i, last_y_constraint)
    constraints.append(last_y_ind == last_y_constraint)

    # 1) truth value constraints
    sxs = [Bool('sx_{}_{}'.format(i, num)) for i in xrange(len(x))]
    txs = [Bool('tx_{}_{}'.format(i, num)) for i in xrange(len(x))]

    for i in xrange(len(x)):
        constraints.append(sxs[i] == Or(s[0] == x[i], s[1] == x[i]))
        constraints.append(txs[i] == Or(t[0] == x[i], t[1] == x[i]))

    # 2) Index constraints
    indexes = [Int('i_{}_{}'.format(i, num)) for i in xrange(len(x))]

    # initial i constraint
    for i in xrange(len(indexes)):
        i_constraint = And(indexes[i] == 0, x[0] == y[i])
        for j in xrange(1, len(x)):
            i_constraint = Xor(i_constraint, And(indexes[i] == j, x[j] == y[i]))
        i_constraint = Or(i_constraint, And(indexes[i] == -1, y[i] == -1))
        constraints.append(i_constraint)

    # i ordering constraint
    for i in xrange(len(indexes)-1):
        constraints.append(Or(indexes[i] < indexes[i+1], indexes[i+1] == -1))

    # finding s_bar and t_bar constraints
    s_bar = Int('s_bar_{}'.format(num))
    t_bar = Int('t_bar_{}'.format(num))
    constraints.append(And(s_bar == sbarcalc(sxs, x, y), s_bar != BIG_CONSTANT))
    constraints.append(And(t_bar == tbarcalc(txs, s_bar), t_bar != BIG_CONSTANT))
    constraints.append(t_bar-s_bar == last_y_ind)
    return constraints

    


if __name__ == '__main__':
    solve()