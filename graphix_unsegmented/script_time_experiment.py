from draw import *
from util import *
import sys
import hand_examples
from invert import *
from graphix_lang import *
import time

assert not USING_SHOWCASE, "still using showcase params plz change meta_param.py "
inverter = Inverter()

i = 0
while True:
  params = sample_params()
  squares_orig,lines_orig = mk_scene(params)
  rendered = render(squares_orig + lines_orig)
  # only test on sufficiently complex, non-trivial images
  if np.sum(rendered) < 100:
    continue
  constraints = img_2_constraints(rendered)

  i += 1

  draw_orig(rendered, "hand_drawings/target.png")

  i_full_params = inverter.invert_full(constraints, rendered, "full")
  inverter.clear_solver()
  i_rand_params = inverter.invert_full(constraints, rendered, "rand")
  inverter.clear_solver()
  i_nn_params = inverter.invert_full(constraints, rendered, "nn", 0.9)
  inverter.clear_solver()
  i_cegis_params = inverter.invert_cegis(constraints, rendered, "cegis")
  inverter.clear_solver()
  i_rcegis_params = inverter.invert_cegis(constraints, rendered, "r_cegis")
  inverter.clear_solver()
  i_acegis_params = inverter.invert_cegis(constraints, rendered, "a_cegis")
  inverter.clear_solver()
  i_rand_cegis_params = inverter.invert_full(constraints, rendered, "rand+cegis")
  inverter.clear_solver()
  i_nn_cegis_params = inverter.invert_full(constraints, rendered, "nn+cegis", 0.9)
  inverter.clear_solver()


  print "===================================== number {} with {} pixels ".format(i, np.sum(rendered)) 
  print "time_full: ", i_full_params['building_time'], i_full_params['solving_time'], i_full_params['ce_size']
  print "time_rand: ", i_rand_params['building_time'], i_rand_params['solving_time'], i_rand_params['ce_size'], i_rand_params['error'] / 1024
  print "time_nn: ", i_nn_params['building_time'], i_nn_params['solving_time'], i_nn_params['ce_size'], i_nn_params['nn_time']
  print "time_cegis: ", i_cegis_params['building_time'], i_cegis_params['solving_time'], i_cegis_params['ce_size']
  print "time_rcegis: ", i_rcegis_params['building_time'], i_rcegis_params['solving_time'], i_rcegis_params['ce_size']
  print "time_acegis: ", i_acegis_params['building_time'], i_acegis_params['solving_time'], i_acegis_params['ce_size']
  print "time_rand_cegis: ", i_rand_cegis_params['building_time'], i_rand_cegis_params['solving_time'], i_rand_cegis_params['ce_size']
  print "time_nn_cegis: ", i_nn_cegis_params['building_time'], i_nn_cegis_params['solving_time'], i_nn_cegis_params['ce_size'], i_nn_cegis_params['nn_time'], i_nn_cegis_params['error'] / 1024, i_nn_cegis_params['orig_subset_size']
