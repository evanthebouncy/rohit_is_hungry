from draw import *
from util import *
import sys
import hand_examples
from invert import *
from graphix_lang import *
import time
import pickle

assert not USING_SHOWCASE, "still using showcase params plz change meta_param.py "
inverter = Inverter()

TEST_LOC = "./data/data_test.p"
def make_datas():
  to_write = []
  while len(to_write) < 400:
    print len(to_write)
    params = sample_params()
    squares_orig,lines_orig = mk_scene(params)
    rendered = render(squares_orig + lines_orig)
    # only test on sufficiently complex, non-trivial images
    if np.sum(rendered) < 100:
      continue
    else:
      to_write.append(params)
  pickle.dump(to_write, open(TEST_LOC, "wb"))

# # make some datas
# make_datas()
# assert 0

i = 0
test_data = pickle.load(open(TEST_LOC,"rb"))

RESULT_LOC = "icml_result.p"
to_dump = []

for params in test_data:
  squares_orig,lines_orig = mk_scene(params)
  rendered = render(squares_orig + lines_orig)
  constraints = img_2_constraints(rendered)

  i += 1

  draw_orig(rendered, "hand_drawings/target.png")
  print "i with pixels ", np.sum(rendered)

  to_add = [
      # inverter.invert_full(constraints, rendered, "full"),
      # inverter.invert_full(constraints, rendered, "rand"),
      # inverter.invert_full(constraints, rendered, "nn", 0.9),
      # inverter.invert_cegis(constraints, rendered, "cegis"),
      # inverter.invert_cegis(constraints, rendered, "r_cegis"),
      # inverter.invert_cegis(constraints, rendered, "a_cegis"),
      # inverter.invert_full(constraints, rendered, "rand+cegis"),
  inverter.invert_full(constraints, rendered, "h1+cegis"),
  inverter.invert_full(constraints, rendered, "nn+cegis", 0.9),
      ]

  if len(to_dump) == 0:
    to_dump = [[] for _ in range(len(to_add))]
  
  assert len(to_dump) == len(to_add)
  for jjj in range(len(to_dump)):
    to_dump[jjj].append(to_add[jjj])

  for blahblah in to_dump:
    print sorted(list(blahblah[-1].items()))

  if i % 2 == 0:
    print "dumping pickle result"
    pickle.dump(to_dump, open(RESULT_LOC, "wb"))

pickle.dump(to_dump, open(RESULT_LOC, "wb"))
