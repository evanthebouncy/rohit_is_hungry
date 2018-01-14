from z3 import *


def check_arr(s):
    arr = map(int, s)
    s = Solver()

    I = IntSort()
    derp = Array('derp', I, I)
    base = Array('base', I, I)
    other = Array('other', I, I)

    for i, num in enumerate([0, 1]):
        base = Store(base, i, num)

    for i, num in enumerate([0, 0]):
        other = Store(other, i, num)

    j = 0
    for i in xrange(len(arr)):
        s.add(arr[i] == derp[j])
        j = (j+1) % 2

    s.add(j == 0)
    s.add(Xor(derp == base, derp == other))

    is_basic = Int('is_basic')
    s.add(If(derp==base, is_basic == 7, is_basic == 10))

    if s.check() == sat:
        model = s.model()
        print model[is_basic]
        # base_ind = str(model[base])[-2]
        # other_ind = str(model[other])[-2]
        # derp_ind = str(s.model()[derp])[-2]

        # if derp_ind == base_ind:
        #     print 'base'
        # elif derp_ind == other_ind:
        #     print 'other'

    return s.check()

if __name__ == '__main__':
    assert check_arr('0101') == sat
    assert check_arr('010101') == sat
    assert check_arr('0000') == sat
    assert check_arr('01010') == unsat
