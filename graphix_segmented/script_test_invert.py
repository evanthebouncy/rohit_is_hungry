from draw import *
from util import *
import sys
import hand_examples
from invert import *
import time

squares_orig,lines_orig = mk_scene(hand_examples.ex_box_line1)
rendered_squares = render(squares_orig)
rendered_lines = render(lines_orig)
rendered = render(squares_orig + lines_orig)
constraints = img_2_constraints(rendered_squares, rendered_lines)

draw_orig(rendered, "hand_drawings/target.png")

stime = time.time()
inverter = Inverter()
inverted_params = inverter.invert_full(constraints, rendered_squares, rendered_lines, "rand")
# inverter.invert_cegis(constraints, rendered_squares, rendered_lines, "cegis")
print time.time() - stime

squares,lines = mk_scene(inverted_params)
draw_orig(render(squares+lines), "hand_drawings/recovered.png")

