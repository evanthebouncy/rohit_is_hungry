from draw import *
from graphix_solver import *
from data import *
import sys
import hand_examples
from model import *

squares_orig,lines_orig = mk_scene(hand_examples.ex_box_line1)
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
#invert(constraints, "full_constraints")
#assert 0

# invert random subset

# random_sub_constraints = []
# for xx in constraints:
#   if random.random() < 0.05:
#     random_sub_constraints.append(xx)
# 
# invert(random_sub_constraints, "random_sub_constraints")

# sub_constraints = constraints[:1]
# print CEGIS(constraints, rendered_orig)

# # invert neural network
# query = mk_query(rendered_orig)
# impnet = Implynet(tf.Session())
# impnet.load_model("./models/imply.ckpt")

# print impnet.get_sorted_unlikely([], grid_constraints_orig)
# trace = impnet.get_trace(query, grid_constraints_orig, 80)
# trace = [((16, 2), [1.0, 0.0]), ((0, 59), [1.0, 0.0]), ((5, 8), [1.0, 0.0]), ((33, 41), [1.0, 0.0]), ((59, 40), [1.0, 0.0]), ((27, 19), [1.0, 0.0]), ((15, 15), [1.0, 0.0]), ((59, 20), [1.0, 0.0]), ((10, 31), [1.0, 0.0]), ((41, 56), [1.0, 0.0]), ((20, 43), [1.0, 0.0]), ((5, 13), [1.0, 0.0]), ((32, 15), [1.0, 0.0]), ((50, 20), [1.0, 0.0]), ((19, 29), [1.0, 0.0]), ((29, 36), [1.0, 0.0]), ((27, 43), [1.0, 0.0]), ((26, 39), [1.0, 0.0]), ((25, 35), [1.0, 0.0]), ((44, 19), [1.0, 0.0]), ((34, 10), [1.0, 0.0]), ((3, 34), [1.0, 0.0]), ((43, 4), [1.0, 0.0]), ((44, 41), [1.0, 0.0]), ((27, 10), [1.0, 0.0]), ((40, 47), [1.0, 0.0]), ((7, 55), [1.0, 0.0]), ((14, 41), [1.0, 0.0]), ((18, 52), [1.0, 0.0]), ((34, 61), [1.0, 0.0]), ((15, 62), [1.0, 0.0]), ((51, 42), [1.0, 0.0]), ((41, 33), [1.0, 0.0]), ((51, 47), [1.0, 0.0]), ((1, 39), [1.0, 0.0]), ((60, 45), [1.0, 0.0]), ((39, 22), [1.0, 0.0]), ((58, 13), [1.0, 0.0]), ((28, 60), [1.0, 0.0]), ((35, 35), [1.0, 0.0]), ((10, 60), [1.0, 0.0]), ((6, 59), [1.0, 0.0]), ((7, 63), [1.0, 0.0]), ((53, 13), [1.0, 0.0]), ((20, 38), [1.0, 0.0]), ((50, 63), [1.0, 0.0]), ((6, 39), [1.0, 0.0]), ((39, 42), [1.0, 0.0]), ((10, 6), [1.0, 0.0]), ((0, 9), [1.0, 0.0]), ((20, 62), [1.0, 0.0]), ((45, 46), [1.0, 0.0]), ((0, 15), [1.0, 0.0]), ((20, 16), [1.0, 0.0]), ((10, 14), [1.0, 0.0]), ((56, 63), [1.0, 0.0]), ((39, 16), [1.0, 0.0]), ((30, 40), [1.0, 0.0]), ((28, 14), [1.0, 0.0]), ((3, 62), [1.0, 0.0]), ((31, 44), [1.0, 0.0]), ((35, 43), [1.0, 0.0]), ((30, 11), [1.0, 0.0]), ((10, 36), [1.0, 0.0]), ((15, 25), [1.0, 0.0]), ((8, 10), [1.0, 0.0]), ((56, 43), [1.0, 0.0]), ((55, 39), [1.0, 0.0]), ((57, 47), [1.0, 0.0]), ((3, 56), [1.0, 0.0]), ((51, 16), [1.0, 0.0]), ((56, 23), [1.0, 0.0]), ((54, 19), [1.0, 0.0]), ((55, 15), [1.0, 0.0]), ((40, 7), [1.0, 0.0]), ((25, 63), [1.0, 0.0]), ((44, 29), [1.0, 0.0]), ((32, 37), [1.0, 0.0]), ((50, 38), [1.0, 0.0]), ((2, 30), [1.0, 0.0])]

# trace = trace[:40]
# random_sub_constraints = random_sub_constraints[:40]
# 
# print trace
# 
# nn_sub_constraints = []
# for xx in trace:
#   x_y, vale = xx
#   vale = True if vale[0] else False
#   y, x = x_y
#   nn_sub_constraints.append(((x,y),vale))
# 
# # invert(nn_sub_constraints, "nn_sub_constraints")
nn_sub_constraints = [((0, 0), False), ((5, 0), True), ((1, 0), False), ((2, 0), False), ((3, 0), False), ((12, 0), True), ((4, 0), False), ((6, 0), True), ((9, 0), True), ((30, 0), True), ((16, 0), False), ((7, 0), True), ((28, 0), False), ((14, 0), True), ((15, 0), True), ((29, 0), False), ((10, 0), True), ((21, 0), False), ((35, 0), True), ((17, 0), False), ((39, 0), True), ((25, 0), False), ((55, 0), True), ((37, 0), True), ((40, 0), True), ((41, 0), False), ((46, 0), False), ((44, 0), False), ((31, 0), True), ((56, 0), True), ((13, 0), True), ((45, 0), False), ((20, 0), False), ((22, 0), False), ((26, 0), False), ((54, 0), False), ((57, 0), True), ((62, 0), True), ((2, 1), False), ((5, 1), True), ((16, 5), True), ((4, 1), False), ((16, 1), False), ((6, 1), True), ((32, 0), True), ((63, 0), True), ((12, 1), True), ((0, 2), False), ((22, 1), False), ((16, 2), False), ((27, 0), False), ((47, 0), False), ((1, 1), False), ((41, 1), False), ((38, 1), True), ((5, 3), True), ((42, 1), False), ((20, 2), False), ((37, 2), True), ((21, 2), False), ((56, 1), True), ((28, 1), False), ((23, 0), False), ((52, 1), False), ((41, 2), False), ((53, 0), False), ((51, 0), False), ((59, 0), True), ((47, 1), False), ((24, 2), False), ((53, 1), False), ((19, 0), False), ((24, 0), False), ((28, 2), False), ((48, 4), False), ((43, 1), False), ((25, 2), False), ((5, 4), True), ((30, 1), True), ((13, 1), True), ((39, 1), True), ((49, 0), False), ((10, 3), True), ((22, 2), False), ((18, 5), True), ((16, 3), False), ((51, 1), False), ((16, 4), False), ((19, 5), True), ((32, 1), True), ((6, 4), True), ((15, 1), True), ((61, 0), True), ((29, 1), False), ((5, 5), True), ((5, 2), True), ((20, 5), True), ((16, 6), False), ((12, 2), True), ((18, 2), False), ((54, 2), False), ((55, 1), True), ((3, 2), False), ((57, 1), True), ((17, 3), False), ((14, 1), True), ((18, 3), False), ((22, 5), True), ((52, 2), False), ((19, 1), False), ((48, 1), False), ((7, 1), True), ((14, 3), True), ((54, 1), False), ((19, 3), False), ((41, 5), True), ((5, 6), True), ((42, 4), False), ((24, 5), True), ((60, 0), True), ((0, 3), False), ((41, 4), False), ((20, 3), False), ((55, 2), True), ((23, 6), False), ((18, 0), False), ((16, 7), False), ((0, 5), False), ((61, 1), True), ((51, 3), False), ((30, 2), True), ((13, 2), True), ((44, 5), True), ((3, 5), False), ((63, 3), True), ((49, 1), False), ((44, 1), False), ((29, 5), True), ((55, 4), True), ((31, 2), True), ((45, 5), True), ((4, 3), False), ((41, 6), False), ((50, 0), False), ((4, 5), False), ((12, 4), True), ((5, 11), False), ((14, 2), True), ((44, 4), False), ((25, 3), False), ((4, 6), False), ((5, 7), True), ((6, 6), True), ((29, 2), False), ((27, 4), False), ((42, 5), True), ((55, 6), True), ((10, 11), True), ((39, 2), True), ((43, 2), False), ((26, 2), False), ((0, 6), False), ((24, 6), False), ((25, 6), False), ((29, 3), False), ((48, 5), True), ((49, 5), True), ((10, 6), True), ((41, 3), False), ((17, 6), False), ((18, 4), False), ((15, 3), True), ((17, 7), False), ((14, 6), True), ((45, 4), False), ((5, 8), True), ((13, 3), True), ((53, 5), True), ((56, 2), True), ((54, 5), True), ((15, 11), True), ((53, 2), False), ((7, 11), False), ((42, 6), False), ((8, 11), False), ((8, 1), True), ((20, 6), False), ((18, 6), False), ((49, 2), False), ((7, 2), True), ((46, 3), False), ((48, 0), False), ((6, 7), True), ((55, 10), True), ((7, 3), True), ((29, 6), False), ((22, 4), False), ((52, 4), False), ((41, 7), False), ((23, 2), False), ((54, 4), False), ((45, 6), False), ((25, 5), True), ((16, 8), False), ((7, 7), True), ((46, 9), False), ((9, 11), False), ((43, 4), False), ((55, 5), True), ((30, 3), True), ((31, 3), True), ((11, 9), True), ((5, 9), True), ((24, 8), False), ((11, 11), False), ((47, 2), False), ((28, 4), False), ((0, 7), False), ((40, 2), True), ((54, 6), False), ((29, 4), False), ((5, 10), True), ((26, 5), True), ((60, 11), True), ((13, 4), True), ((23, 3), False), ((22, 9), False), ((2, 6), False), ((3, 10), False), ((16, 10), False), ((21, 4), False), ((14, 11), False), ((0, 11), False), ((6, 11), False), ((0, 9), False), ((41, 8), False), ((29, 7), False), ((12, 11), False), ((52, 0), False), ((17, 10), False), ((34, 11), False), ((43, 6), False), ((16, 9), False), ((45, 8), False), ((21, 6), False), ((10, 13), True), ((43, 7), False), ((1, 4), False), ((2, 3), False), ((50, 1), False), ((50, 7), False), ((2, 8), False), ((16, 11), False), ((41, 9), False), ((22, 10), False), ((12, 5), True), ((49, 8), False), ((47, 4), False), ((12, 9), True), ((24, 3), False), ((11, 7), True), ((14, 12), False), ((26, 6), False), ((25, 8), False), ((27, 6), False), ((1, 9), False), ((26, 8), False), ((51, 6), False), ((0, 15), True), ((62, 1), True), ((4, 10), False), ((0, 13), False), ((47, 6), False), ((11, 10), True), ((45, 1), False), ((15, 12), True), ((0, 14), False), ((30, 4), True), ((62, 10), True), ((10, 14), True), ((18, 11), False), ((0, 12), False), ((7, 12), False), ((48, 6), False), ((13, 10), True), ((38, 11), False), ((24, 4), False), ((19, 11), False), ((41, 10), False), ((23, 9), False), ((39, 11), False), ((27, 5), True), ((33, 11), False), ((10, 12), True), ((24, 9), False), ((52, 6), False), ((44, 6), False), ((10, 8), True), ((42, 10), False), ((37, 11), False), ((6, 10), True), ((24, 10), False), ((28, 6), False), ((34, 13), False), ((42, 0), False), ((12, 16), True), ((25, 9), False), ((32, 11), False), ((13, 12), False), ((31, 11), False), ((4, 8), False), ((16, 12), False), ((1, 15), True), ((20, 11), False), ((15, 13), True), ((15, 15), True), ((27, 9), False), ((20, 12), False), ((1, 13), False), ((12, 14), False), ((2, 14), False), ((63, 11), False), ((26, 4), False), ((6, 8), True), ((25, 10), False), ((41, 11), False), ((52, 8), False), ((13, 13), False), ((5, 15), False), ((36, 12), False), ((15, 14), True), ((21, 7), False), ((14, 10), True), ((27, 12), False), ((19, 15), False), ((17, 2), False), ((17, 11), False), ((33, 14), False), ((14, 13), False), ((9, 12), False), ((4, 15), True), ((28, 8), False), ((45, 9), False), ((7, 10), True), ((57, 14), False), ((10, 15), True), ((11, 13), False), ((23, 15), False), ((34, 14), False), ((3, 9), False), ((13, 14), False), ((14, 14), False), ((11, 16), False), ((19, 16), False), ((4, 9), False), ((26, 9), False), ((24, 11), False), ((9, 15), False), ((62, 16), True), ((12, 15), False), ((17, 16), True), ((48, 7), False), ((25, 11), False), ((18, 15), False), ((4, 12), False), ((28, 11), False), ((30, 15), False), ((62, 11), False), ((37, 12), False), ((16, 14), False), ((11, 17), False), ((10, 16), True), ((5, 17), True), ((17, 12), False), ((24, 14), False), ((0, 16), True), ((4, 13), False), ((13, 15), False), ((6, 17), True), ((19, 22), True), ((60, 15), True), ((6, 16), False), ((52, 9), False), ((17, 13), False), ((37, 13), False), ((4, 14), False), ((18, 16), True), ((19, 17), False), ((13, 16), True), ((61, 12), False), ((13, 17), True), ((4, 20), False), ((1, 16), True), ((23, 17), False), ((10, 18), False), ((7, 17), True), ((10, 19), False), ((0, 22), False), ((35, 18), False), ((5, 16), False), ((21, 22), True), ((17, 14), False), ((8, 17), True), ((6, 20), False), ((8, 16), False), ((9, 16), False), ((9, 17), True), ((18, 17), True), ((24, 17), False), ((55, 17), True), ((9, 18), False), ((19, 18), False), ((5, 21), False), ((10, 17), True), ((2, 16), True), ((7, 22), False), ((22, 22), True), ((30, 22), False), ((63, 17), True), ((26, 10), False), ((0, 20), False), ((23, 22), True), ((53, 6), False), ((5, 18), False), ((17, 15), False), ((3, 12), False), ((17, 17), True), ((25, 20), False), ((10, 22), False), ((24, 22), True), ((21, 16), False), ((19, 21), False), ((3, 20), False), ((25, 21), False), ((11, 14), False), ((25, 22), True), ((15, 23), False), ((33, 21), False), ((26, 22), True), ((26, 23), False), ((27, 22), True), ((14, 15), False), ((27, 20), False), ((19, 23), False), ((1, 20), False), ((28, 22), True), ((29, 22), True), ((37, 14), False), ((33, 22), False), ((29, 21), False), ((29, 23), True), ((20, 13), False), ((29, 24), True), ((9, 25), True), ((4, 22), False), ((4, 23), False), ((0, 25), False), ((12, 23), False), ((5, 25), False), ((9, 23), False), ((11, 22), False), ((8, 25), False), ((5, 19), False), ((22, 17), False), ((28, 20), False), ((20, 25), False), ((16, 25), True), ((19, 24), False), ((18, 25), True), ((29, 37), True), ((10, 26), True), ((5, 26), False)]

CEGIS(constraints, rendered_orig, nn_sub_constraints)
# CEGIS(constraints, rendered_orig, nn_sub_constraints)
