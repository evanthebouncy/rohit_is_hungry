from draw import *
from graphix_solver import *
from data import *
import sys
import hand_examples
from model import *

squares_orig,lines_orig = mk_scene(hand_examples.ex1)
rendered_orig = render(squares_orig+lines_orig)
grid_constraints_orig = img_2_bool(rendered_orig)
# draw_allob(grid_constraints_orig, "hand_drawings/orig.png", [])
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

# invert random subset
random_sub_constraints = []
for xx in constraints:
  if random.random() < 0.05:
    random_sub_constraints.append(xx)

invert(random_sub_constraints, "random_sub_constraints")

# # invert neural network
# query = mk_query(rendered_orig)
# impnet = Implynet(tf.Session())
# impnet.load_model("./models/imply.ckpt")
# 
# # print impnet.get_sorted_unlikely([], grid_constraints_orig)
# trace = impnet.get_trace(query, grid_constraints_orig, 80)
# 
# print trace

trace = [((59, 41), [1.0, 0.0]), ((0, 59), [1.0, 0.0]), ((51, 14), [1.0, 0.0]), ((42, 55), [1.0, 0.0]), ((58, 14), [1.0, 0.0]), ((41, 16), [1.0, 0.0]), ((29, 42), [1.0, 0.0]), ((51, 44), [1.0, 0.0]), ((35, 34), [1.0, 0.0]), ((27, 34), [1.0, 0.0]), ((28, 38), [1.0, 0.0]), ((25, 41), [1.0, 0.0]), ((35, 12), [1.0, 0.0]), ((14, 15), [1.0, 0.0]), ((5, 61), [1.0, 0.0]), ((10, 10), [1.0, 0.0]), ((28, 59), [1.0, 0.0]), ((7, 33), [1.0, 0.0]), ((52, 39), [1.0, 0.0]), ((41, 42), [1.0, 0.0]), ((1, 39), [1.0, 0.0]), ((35, 59), [1.0, 0.0]), ((19, 28), [1.0, 0.0]), ((5, 7), [1.0, 0.0]), ((52, 63), [1.0, 0.0]), ((0, 15), [1.0, 0.0]), ((16, 43), [1.0, 0.0]), ((50, 23), [1.0, 0.0]), ((9, 55), [1.0, 0.0]), ((15, 54), [1.0, 0.0]), ((56, 20), [1.0, 0.0]), ((41, 22), [1.0, 0.0]), ((20, 16), [1.0, 0.0]), ((57, 47), [1.0, 0.0]), ((26, 14), [1.0, 0.0]), ((41, 31), [1.0, 0.0]), ((18, 37), [1.0, 0.0]), ((7, 38), [1.0, 0.0]), ((1, 31), [1.0, 0.0]), ((0, 35), [1.0, 0.0]), ((43, 5), [1.0, 0.0]), ((0, 7), [1.0, 0.0]), ((15, 3), [1.0, 0.0]), ((34, 41), [1.0, 0.0]), ((31, 17), [1.0, 0.0]), ((5, 13), [1.0, 0.0]), ((1, 11), [1.0, 0.0]), ((57, 63), [1.0, 0.0]), ((19, 63), [1.0, 0.0]), ((25, 19), [1.0, 0.0]), ((45, 47), [1.0, 0.0]), ((10, 62), [1.0, 0.0]), ((30, 9), [1.0, 0.0]), ((40, 47), [1.0, 0.0]), ((25, 9), [1.0, 0.0]), ((10, 5), [1.0, 0.0]), ((33, 37), [1.0, 0.0]), ((55, 42), [1.0, 0.0]), ((56, 38), [1.0, 0.0]), ((4, 36), [1.0, 0.0]), ((15, 39), [1.0, 0.0]), ((4, 56), [1.0, 0.0]), ((19, 51), [1.0, 0.0]), ((19, 0), [1.0, 0.0]), ((25, 62), [1.0, 0.0]), ((40, 8), [1.0, 0.0]), ((34, 63), [1.0, 0.0]), ((50, 48), [1.0, 0.0]), ((54, 46), [1.0, 0.0]), ((50, 18), [1.0, 0.0]), ((54, 16), [1.0, 0.0]), ((15, 25), [1.0, 0.0]), ((1, 63), [1.0, 0.0]), ((10, 30), [1.0, 0.0]), ((31, 35), [1.0, 0.0]), ((19, 12), [1.0, 0.0]), ((9, 14), [1.0, 0.0]), ((15, 62), [1.0, 0.0]), ((16, 29), [1.0, 0.0]), ((60, 23), [1.0, 0.0])]


nn_sub_constraints = []
for xx in trace:
  x_y, vale = xx
  vale = True if vale[0] else False
  y, x = x_y
  nn_sub_constraints.append(((x,y),vale))

nn_sub_constraints = nn_sub_constraints + random_sub_constraints
invert(nn_sub_constraints, "nn_sub_constraints")
