from model import *
from draw import *
import sys
import hand_examples

squares_orig,lines_orig = mk_scene(hand_examples.ex_box_line1)
# squares, lines = hand_example()
rendered = render(squares_orig + lines_orig)
constraints = img_2_labels(rendered)
draw_allob(constraints, "drawings/constraints.png", [])

query = mk_query(rendered)
print constraints

impnet = Implynet(tf.Session())
impnet.load_model("./models/imply.ckpt")

print impnet.get_trace(query, constraints)
