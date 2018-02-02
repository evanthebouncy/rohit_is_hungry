from z3 import *

L = 10

class OrderSolver(object):

    def __init__(self):
        self.reset_solver()

    def reset_solver(self):
        self.solver = Solver()

        self.ordering = [Int('ans_{}'.format(i)) for i in xrange(L)]
        
        for o in self.ordering:
            self.solver.add(And(0 <= o, o <= 9))

        self.solver.add(Distinct(self.ordering))

    def add_example(self, example):
        nums, truth = example
        num1, num2 = nums
        if truth:
            self.solver.add(self.ordering[num1] < self.ordering[num2])
        else:
            self.solver.add(Not(self.ordering[num1] < self.ordering[num2]))

    def solve(self):
        if self.solver.check() == sat:
            model = self.solver.model()
            order = []
            for i, o in enumerate(self.ordering):
                order.append((i, model[o].as_long()))
            order = sorted(order, key=lambda x: x[1])
            return map(lambda x: x[0], order)
        else:
            print unsat
            return None

    def add_temp(self, example):
        '''temporarily adds an example and checks if sat'''
        self.solver.push()
        nums, truth = example
        num1, num2 = nums
        if truth:
            self.solver.add(self.ordering[num1] < self.ordering[num2])
        else:
            self.solver.add(Not(self.ordering[num1] < self.ordering[num2]))
        is_sat = self.solver.check() == sat
        self.solver.pop()
        return is_sat


if __name__ == '__main__':
    # check if solver works
    from gen import *

    s = OrderSolver()

    for _ in xrange(100):
        truth = gen_ordering()
        examples = get_data(truth)
        for e in examples:
            s.add_example(e)
        synth = s.solve()
        print 'truth:', truth
        print 'synth:', synth
        assert synth
        s.reset_solver()

    # reset solver and check an "ambiguous" example
    print 'Trying 2 ambiguous examples...'
    print s.add_temp(((5, 1), True))
    print s.add_temp(((5, 1), False))
