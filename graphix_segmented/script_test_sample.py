from model import *
from draw import *
import sys
import hand_examples

squares_orig,lines_orig = mk_scene(hand_examples.ex_box_line1)
# squares, lines = hand_example()
rendered = render(squares_orig + lines_orig)
draw_orig(rendered, "drawings/orig.png")

impnet = Implynet(tf.Session())
impnet.load_model("./models/imply.ckpt")

trace = impnet.get_trace(rendered)
print len(trace)
