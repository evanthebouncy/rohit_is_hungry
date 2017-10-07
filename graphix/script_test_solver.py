from draw import *
from graphix_solver import *
from data import *
import sys
import hand_examples
from model import *

squares_orig,lines_orig = mk_scene(hand_examples.ex1)
rendered_orig = render(squares_orig+lines_orig)
grid_constraints_orig = img_2_bool(rendered_orig)
draw_allob(grid_constraints_orig, "hand_drawings/orig.png", [])
constraints = img_2_constraints(rendered_orig)

def invert(constraints, name):
  solver = DrawingSolver()
  inverted_params = solver.solve(10, constraints)
  print "inverted parameters: "
  print inverted_params

  squares,lines = mk_scene(inverted_params)
  rendered = render(squares+lines)
  grid_constraints = img_2_bool(rendered)
  draw_allob(grid_constraints, "hand_drawings/recovered_{}.png".format(name), [])

# invert the full constraint
# invert(constraints, "full_constraints")
# assert 0

# invert random subset

random_sub_constraints = []
for xx in constraints:
  if random.random() < 0.02:
    random_sub_constraints.append(xx)

invert(random_sub_constraints, "random_sub_constraints")

# sub_constraints = constraints[:1]
# print CEGIS(constraints, rendered_orig)

# # invert neural network
# query = mk_query(rendered_orig)
# impnet = Implynet(tf.Session())
# impnet.load_model("./models/imply.ckpt")

# print impnet.get_sorted_unlikely([], grid_constraints_orig)
# trace = impnet.get_trace(query, grid_constraints_orig, 80)
trace = [((16, 2), [1.0, 0.0]), ((0, 59), [1.0, 0.0]), ((5, 8), [1.0, 0.0]), ((33, 41), [1.0, 0.0]), ((59, 40), [1.0, 0.0]), ((27, 19), [1.0, 0.0]), ((15, 15), [1.0, 0.0]), ((59, 20), [1.0, 0.0]), ((10, 31), [1.0, 0.0]), ((41, 56), [1.0, 0.0]), ((20, 43), [1.0, 0.0]), ((5, 13), [1.0, 0.0]), ((32, 15), [1.0, 0.0]), ((50, 20), [1.0, 0.0]), ((19, 29), [1.0, 0.0]), ((29, 36), [1.0, 0.0]), ((27, 43), [1.0, 0.0]), ((26, 39), [1.0, 0.0]), ((25, 35), [1.0, 0.0]), ((44, 19), [1.0, 0.0]), ((34, 10), [1.0, 0.0]), ((3, 34), [1.0, 0.0]), ((43, 4), [1.0, 0.0]), ((44, 41), [1.0, 0.0]), ((27, 10), [1.0, 0.0]), ((40, 47), [1.0, 0.0]), ((7, 55), [1.0, 0.0]), ((14, 41), [1.0, 0.0]), ((18, 52), [1.0, 0.0]), ((34, 61), [1.0, 0.0]), ((15, 62), [1.0, 0.0]), ((51, 42), [1.0, 0.0]), ((41, 33), [1.0, 0.0]), ((51, 47), [1.0, 0.0]), ((1, 39), [1.0, 0.0]), ((60, 45), [1.0, 0.0]), ((39, 22), [1.0, 0.0]), ((58, 13), [1.0, 0.0]), ((28, 60), [1.0, 0.0]), ((35, 35), [1.0, 0.0]), ((10, 60), [1.0, 0.0]), ((6, 59), [1.0, 0.0]), ((7, 63), [1.0, 0.0]), ((53, 13), [1.0, 0.0]), ((20, 38), [1.0, 0.0]), ((50, 63), [1.0, 0.0]), ((6, 39), [1.0, 0.0]), ((39, 42), [1.0, 0.0]), ((10, 6), [1.0, 0.0]), ((0, 9), [1.0, 0.0]), ((20, 62), [1.0, 0.0]), ((45, 46), [1.0, 0.0]), ((0, 15), [1.0, 0.0]), ((20, 16), [1.0, 0.0]), ((10, 14), [1.0, 0.0]), ((56, 63), [1.0, 0.0]), ((39, 16), [1.0, 0.0]), ((30, 40), [1.0, 0.0]), ((28, 14), [1.0, 0.0]), ((3, 62), [1.0, 0.0]), ((31, 44), [1.0, 0.0]), ((35, 43), [1.0, 0.0]), ((30, 11), [1.0, 0.0]), ((10, 36), [1.0, 0.0]), ((15, 25), [1.0, 0.0]), ((8, 10), [1.0, 0.0]), ((56, 43), [1.0, 0.0]), ((55, 39), [1.0, 0.0]), ((57, 47), [1.0, 0.0]), ((3, 56), [1.0, 0.0]), ((51, 16), [1.0, 0.0]), ((56, 23), [1.0, 0.0]), ((54, 19), [1.0, 0.0]), ((55, 15), [1.0, 0.0]), ((40, 7), [1.0, 0.0]), ((25, 63), [1.0, 0.0]), ((44, 29), [1.0, 0.0]), ((32, 37), [1.0, 0.0]), ((50, 38), [1.0, 0.0]), ((2, 30), [1.0, 0.0])]

trace = trace[:40]
random_sub_constraints = random_sub_constraints[:40]

print trace

nn_sub_constraints = []
for xx in trace:
  x_y, vale = xx
  vale = True if vale[0] else False
  y, x = x_y
  nn_sub_constraints.append(((x,y),vale))

# invert(nn_sub_constraints, "nn_sub_constraints")
CEGIS(constraints, rendered_orig, nn_sub_constraints)
