from draw import *
from util import *
import sys
import hand_examples
from invert import *
from graphix_lang import *
import time

squares_orig,lines_orig = sample_scene()
# squares_orig,lines_orig = mk_scene(hand_examples.ex4)
rendered_squares = render(squares_orig)
rendered_lines = render(lines_orig)
rendered = render(squares_orig + lines_orig)
constraints = img_2_constraints(rendered_squares, rendered_lines)

draw_orig(rendered, "hand_drawings/target.png")

inverter = Inverter()

def run_comparison():

  stime = time.time()
  inverted_params = inverter.invert_full(constraints, rendered_squares, rendered_lines, "nn+cegis")
  nn_cegis_time = time.time() - stime
  squares,lines = mk_scene(inverted_params)
  draw_orig(render(squares+lines), "hand_drawings/result_nn+cegis.png")

  inverter.clear_solver()

  stime = time.time()
  inverted_params = inverter.invert_full(constraints, rendered_squares, rendered_lines, "nn", 0.1)
  nn_time = time.time() - stime
  squares,lines = mk_scene(inverted_params)
  draw_orig(render(squares+lines), "hand_drawings/result_full_nn.png")

  inverter.clear_solver()

  stime = time.time()
  inverted_params = inverter.invert_full(constraints, rendered_squares, rendered_lines, "rand", 0.1)
  rand_time = time.time() - stime
  squares,lines = mk_scene(inverted_params)
  draw_orig(render(squares+lines), "hand_drawings/result_full_rand.png")

  inverter.clear_solver()

  stime = time.time()
  inverted_params = inverter.invert_cegis(constraints, rendered_squares, rendered_lines, "r_cegis")
  r_cegis_time = time.time() - stime
  squares,lines = mk_scene(inverted_params)
  draw_orig(render(squares+lines), "hand_drawings/result_r_cegis.png")

  inverter.clear_solver()

  stime = time.time()
  inverted_params = inverter.invert_cegis(constraints, rendered_squares, rendered_lines, "cegis")
  cegis_time = time.time() - stime
  squares,lines = mk_scene(inverted_params)
  draw_orig(render(squares+lines), "hand_drawings/result_cegis.png")

  inverter.clear_solver()

  print "all done times "
  print "nn ", nn_time
  print "rand ", rand_time

  print "rcegis ", r_cegis_time
  print "cegis ",  cegis_time
  print "nn then cegis ", nn_cegis_time

run_comparison()
