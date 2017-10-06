from draw import *
from graphix_solver import *
from data import *
import sys
import hand_examples

squares,lines = mk_scene(hand_examples.ex1)
rendered = render(squares+lines)
grid_constraints = img_2_bool(rendered)
draw_allob(grid_constraints, "hand_drawings/orig.png", [])

solver = DrawingSolver()
inverted_params = solver.solve_grid(10, rendered)
print "inverted parameters: "
print inverted_params

squares,lines = mk_scene(inverted_params)
rendered = render(squares+lines)
grid_constraints = img_2_bool(rendered)
draw_allob(grid_constraints, "hand_drawings/recovered.png", [])
