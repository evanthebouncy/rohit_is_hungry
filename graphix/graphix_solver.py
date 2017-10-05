from z3 import *
import numpy as np

class Square(object):

    def __init__(self, center_x, center_y, width):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width

    def inside(self, x,y):
        return And(
            self.center_x-self.width<=x, x<=self.center_x+self.width,
            self.center_y-self.width<=y, y<=self.center_y+self.width
        )

def transform(i,j,a,b,c):
    return i*a + j*b + c

def create_solver(num_squares, grid):
    (M,N) = grid.shape
    s = Solver()

    (c_x, c_y, w, ds, sq_constraints) = ([], [], [], [], [])

    
    transforms = [Int('xform'+c) for c in ['a', 'b', 'c', 'd', 'e', 'f']]
    x_transforms = transforms[:3]
    y_transforms = transforms[3:]

    iter_i = Int('i')
    iter_j = Int('j')

    for i in xrange(2):
        for j in xrange(2):
            transform_x = Int('tx_{}_{}'.format(i,j))
            transform_y = Int('ty_{}_{}'.format(i,j))
            s.add(transform_x == transform(i,j,*x_transforms))
            s.add(transform_y == transform(i,j,*y_transforms))
            for sq_num in xrange(num_squares):
                c_x.append(Int('cx_%d' % sq_num))
                c_y.append(Int('cy_%d' % sq_num))
                w.append(Int('w_%d' % sq_num))
                ds.append(Bool('d_%d' % sq_num))
                # adds the square function
                sq_constraints.append(Square(c_x[sq_num]+transform_x, c_y[sq_num]+transform_y, w[sq_num]).inside)

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
        for i in xrange(num_squares):
            output.append((model[c_x[i]].as_long(),model[c_y[i]].as_long(),model[w[i]].as_long()))
        return output
    else:
        #print "UNSAT!"
        return "UNSAT"





num_squares = 1
grid = np.array([
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
# grid = np.array([
#     [1, 0, 0],
#     [0, 0, 1],
#     [0, 0, 0]
#     ])

t = (0, 3)
c = (2, 0)
w = 1

print create_solver(num_squares, grid)
