from model import *
from draw import *
import sys

squares, lines = hand_example()
rendered = render(squares + lines)
constraints = img_2_bool(rendered)
draw_allob(constraints, "drawings/constraints.png", [])

query = mk_query(rendered)
print constraints

impnet = Implynet(tf.Session())
impnet.load_model("./models/imply.ckpt")

print impnet.get_trace(query, constraints)
