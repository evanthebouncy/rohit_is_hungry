from z3 import *
import numpy as np
from util import *

N_SQUARES = 3
ITER_I_BND = 3
ITER_J_BND = 3
S_WIDTHS = [2,3,5]

class Square(object):

    def __init__(self, center_x, center_y, width, run_at_ij, square_exist):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.run_at_ij = run_at_ij
        self.square_exist = square_exist

    def inside(self, x,y):
        return And(
            self.center_x-self.width<=x, x<=self.center_x+self.width,
            self.center_y-self.width<=y, y<=self.center_y+self.width,
            self.run_at_ij, self.square_exist,
        )

def transform(i,j,a,b,c):
    return i*a + j*b + c

# the solver for taking in constraints and make them into squares
class DrawingSolver:

    def __init__(self):
        self.mk_solver()

    def mk_solver(self):
        self.s = Solver()

        # overall bound on the size of the program
        self.iter_i = Int('iter_bnd_i')
        self.iter_j = Int('iter_bnd_j')
        self.n_squares = Int('n_squares')
        self.program_size = Int('program_size')
        # constraints on iterations and n squares and program size
        self.s.add(self.program_size == self.iter_i + self.iter_j + self.n_squares)
        self.s.add(self.iter_i <= ITER_I_BND)
        self.s.add(self.iter_j <= ITER_J_BND)
        self.s.add(1 <= self.n_squares)
        self.s.add(self.n_squares <= N_SQUARES)

        # coordinate transformations
        self.transforms = [Int('xform'+c) for c in ['a', 'b', 'c', 'd', 'e', 'f']]
        self.x_transforms = self.transforms[:3]
        self.y_transforms = self.transforms[3:]

        # parameters for the square
        self.c_x, self.c_y, self.w = [],[],[] 
        # the list of square constraints being created
        self.sq_constraints = []


        # make some square parameters
        for sq_num in xrange(N_SQUARES):
            self.c_x.append(Int('cx_%d' % sq_num))
            self.c_y.append(Int('cy_%d' % sq_num))
            s_width = Int('w_%d' % sq_num)
            self.w.append(s_width)
            # constrain width
            self.s.add(Or([s_width == w for w in S_WIDTHS]))

        for i in xrange(ITER_I_BND):
            for j in xrange(ITER_J_BND):
                transform_x = Int('tx_{}_{}'.format(i,j))
                transform_y = Int('ty_{}_{}'.format(i,j))
                self.s.add(transform_x == transform(i,j,*self.x_transforms))
                self.s.add(transform_y == transform(i,j,*self.y_transforms))

                # check if a particular i, j iteration is being executed
                run_at_ij = Bool('run_at_{}_{}'.format(i,j))
                self.s.add(run_at_ij == And([i < self.iter_i, j < self.iter_j]))
                
                for sq_num in xrange(N_SQUARES):
                    # check if this square should exist
                    square_exist = Bool('square_exist_{}'.format(sq_num))
                    self.s.add(square_exist == (sq_num < self.n_squares))
                    self.sq_constraints.append(Square(self.c_x[sq_num]+transform_x, self.c_y[sq_num]+transform_y, self.w[sq_num], 
                                               run_at_ij, square_exist).inside)


    def solve_grid(self, program_size_bnd, grid):
        print "solving grid "
        (M,N) = grid.shape

        self.s.add(self.program_size <= program_size_bnd)

        # the outer loop is actually y and the inner is x
        for y in xrange(M):
            for x in xrange(N):
                same_line_print("constraining {} {}".format(x,y))
                value = True if grid[y][x] else False
                all_shapes_occupy = Or([sq_const(x,y) for sq_const in self.sq_constraints])
                self.s.add(value == all_shapes_occupy)

        print "finished adding constraints, solving . . ."

        if self.s.check() == sat:
            model = self.s.model()
            print model
            ret = {}
            # get the loop iteration information and bounds
            ret['iter_i'] = model[self.iter_i].as_long()
            ret['iter_j'] = model[self.iter_j].as_long()
            ret['n_squares'] = model[self.n_squares].as_long()
            ret['program_size'] = model[self.program_size].as_long()
            # get the transform information
            ret['transforms'] = [model[xform_param].as_long() for xform_param in self.transforms]
            squares = [[] for _ in range(ret['n_squares'])]
            for square_id in range(ret['n_squares']):
              squares[square_id].append(model[self.c_x[square_id]].as_long())
              squares[square_id].append(model[self.c_y[square_id]].as_long())
              squares[square_id].append(model[self.w[square_id]].as_long())
            ret['squares'] = squares

            ret['lines'] = []
            return ret
        else:
            return "UNSAT"

if __name__ == '__main__':
  # for this simple picture overwrite the width constrain
  S_WIDTHS = [0,1]
  grid = np.array([
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          ])

  solver = DrawingSolver()
  print solver.solve_grid(7, grid)
