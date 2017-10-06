from z3 import *
import numpy as np

N_SQUARES = 3
ITER_I_BND = 3
ITER_J_BND = 3

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

def create_solver(program_size_bnd, grid):
    (M,N) = grid.shape
    s = Solver()

    (c_x, c_y, w, ds, sq_constraints) = ([], [], [], [], [])

    transforms = [Int('xform'+c) for c in ['a', 'b', 'c', 'd', 'e', 'f']]
    x_transforms = transforms[:3]
    y_transforms = transforms[3:]

    iter_i = Int('iter_bnd_i')
    iter_j = Int('iter_bnd_j')
    n_squares = Int('n_squares')

    s.add(1 <= n_squares)
    s.add(n_squares <= N_SQUARES)
    s.add(iter_i <= ITER_I_BND)
    s.add(iter_j <= ITER_J_BND)

    program_size = Int('program_size')
    s.add(program_size == iter_i + iter_j + n_squares)

    s.add(program_size <= program_size_bnd)

    for i in xrange(ITER_I_BND):
        for j in xrange(ITER_J_BND):
            transform_x = Int('tx_{}_{}'.format(i,j))
            transform_y = Int('ty_{}_{}'.format(i,j))
            s.add(transform_x == transform(i,j,*x_transforms))
            s.add(transform_y == transform(i,j,*y_transforms))

            # check if a particular i, j iteration is being executed
            run_at_ij = Bool('run_at_{}_{}'.format(i,j))
            s.add(run_at_ij == And([i < iter_i, j < iter_j]))
            
            for sq_num in xrange(N_SQUARES):
                c_x.append(Int('cx_%d' % sq_num))
                c_y.append(Int('cy_%d' % sq_num))
                w.append(Int('w_%d' % sq_num))
                # check if this square should exist
                square_exist = Bool('square_exist_{}'.format(sq_num))
                s.add(square_exist == (sq_num < n_squares))
                sq_constraints.append(Square(c_x[sq_num]+transform_x, c_y[sq_num]+transform_y, w[sq_num], 
                                             run_at_ij, square_exist).inside)

    for i in xrange(M):
        for j in xrange(N):
            value = True if grid[i][j] else False
            all_shapes_occupy = Or([sq_const(i,j) for sq_const in sq_constraints])
            s.add(value == all_shapes_occupy)


    # for weight in w:
    #     s.add(weight >= 0)

    if s.check() == sat:
        model = s.model()
        print model
        output = []
        # output.append((model[transform_x],model[transform_y]))
        for i in xrange(N_SQUARES):
            output.append((model[c_x[i]].as_long(),model[c_y[i]].as_long(),model[w[i]].as_long()))
        return output
    else:
        #print "UNSAT!"
        return "UNSAT"





grid = np.array([
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
# grid = np.array([
#     [1, 0, 0],
#     [0, 0, 1],
#     [0, 0, 0]
#     ])

t = (0, 3)
c = (2, 0)
w = 1

print create_solver(6, grid)
