from z3 import *
import numpy as np
from util import *
import time

N_SQUARES = 3
ITER_I_BND = 3
ITER_J_BND = 3
S_WIDTHS = [2,3,5]
TR_LOW_BND, TR_HIGH_BND = 0, 30
SQ_LOW_BND, SQ_HIGH_BND = -20, 20


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
        # set range limit on these transforms
        for tr_par in self.transforms:
          self.s.add(tr_par < TR_HIGH_BND)
          self.s.add(tr_par >= TR_LOW_BND)

        # parameters for the square
        self.c_x, self.c_y, self.w = [],[],[] 
        # the list of square constraints being created
        self.sq_constraints = []


        # make some square parameters
        for sq_num in xrange(N_SQUARES):
            sq_offset_x = Int('sq_offset_x_%d' % sq_num)
            sq_offset_y = Int('sq_offset_y_%d' % sq_num)
            s_width = Int('sq_w_%d' % sq_num)

            self.c_x.append(sq_offset_x)
            self.c_y.append(sq_offset_y)
            self.w.append(s_width)

            # constrain offset 
            self.s.add(And([sq_offset_x >= SQ_LOW_BND, sq_offset_x < SQ_HIGH_BND]))
            self.s.add(And([sq_offset_y >= SQ_LOW_BND, sq_offset_y < SQ_HIGH_BND]))
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

    def solve(self, program_size_bnd, constraints):

        start_time = time.time()
        print "adding constraints . . . "
        self.s.add(self.program_size <= program_size_bnd)
        for x_y, val in constraints:
          value = val
          all_shapes_occupy = Or([sq_const(*x_y) for sq_const in self.sq_constraints])
          self.s.add(value == all_shapes_occupy)

        model_building_time = time.time() - start_time
        print "finished adding constraints, solving . . ."

        if self.s.check() == sat:
            model = self.s.model()
            
            solving_time = time.time() - start_time - model_building_time
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

            ret['building_time'] = model_building_time
            ret['solvng_time'] = solving_time
            return ret
        else:
            return "UNSAT"

    def solve_grid(self, program_size_bnd, grid):
        print "solving grid "
        (M,N) = grid.shape

        constraints = []
        # the outer loop is actually y and the inner is x
        for y in xrange(M):
            for x in xrange(N):
                value = True if grid[y][x] else False
                constraints.append(((x,y),value))
        return self.solve(program_size_bnd, constraints)

def check(params, orig_render, i):
  from data import *
  from draw import *
  
  from graphix_lang import * 
  squares,lines = mk_scene(params)
  rendered = render(squares+lines)

  grid_constraints = img_2_bool(rendered)
  draw_allob(grid_constraints, "hand_drawings/recovered_cegis{}.png".format(i), [])

  diff = rendered - orig_render
  diff_idx1, diff_idx2 = np.where(diff != 0)

  if len(diff_idx1) == 0:
    return None

  else:
    iddd = random.choice(range(len(diff_idx1)))
    id1,id2 = diff_idx1[iddd], diff_idx2[iddd]
    return (int(id2), int(id1)), True if orig_render[id1][id2] else False


def CEGIS(constraints, rendered_orig, start_constraints = []):

  sub_constraints = constraints[:1] + start_constraints

  i = 0
  
  while True:
    i += 1
    solver = DrawingSolver()
    print sub_constraints
    paras = solver.solve(10, sub_constraints)
    print "paras"
    print paras
    ce = check(paras, rendered_orig, i)
    print "ce"
    print ce
    if ce == None:
      return paras
    else:
      sub_constraints.append(ce)
  
   

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
