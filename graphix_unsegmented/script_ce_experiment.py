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

  i_rand_params = inverter.invert_full(constraints, rendered, "rand")
  inverter.clear_solver()
  i_nn_cegis_params = inverter.invert_full(constraints, rendered, "nn_experiment", 0.9)
  inverter.clear_solver()


  print "===================================== number {} with {} pixels ".format(i, np.sum(rendered)) 
  print "time_rand: ", i_rand_params['building_time'], i_rand_params['solving_time'], i_rand_params['ce_size'], 1.0 - float(i_rand_params['error']) / 1024
  print "time_nn_cegis: ", i_nn_cegis_params['building_time'], i_nn_cegis_params['solving_time'], i_nn_cegis_params['ce_size'], i_nn_cegis_params['nn_time'], 1.0 - i_nn_cegis_params['error'] / 1024, i_nn_cegis_params['orig_subset_size']
