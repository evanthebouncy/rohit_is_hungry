from model import *
import sys
from dfa_solver import *
from gen import *
import random
import time
import hashlib
import time
from invert import *
import pickle
TEST_LOC = "./data/data_test.p"

def make_test_data(n=400):
  to_write = []
  for i in range(n):
    test_mat = sample_matrix()
    all_data = generate_examples(test_mat, 2000)
    all_data = dedup(all_data)
    print i, " ", len(all_data)
    to_write.append(all_data)
  pickle.dump( to_write, open( TEST_LOC, "wb" ) )

def data_ratio(data):
  pos, neg = 0, 0
  for x in data:
    if x[1] is True:
      pos += 1
    else:
      neg += 1
  return pos, neg


if __name__ == "__main__":
  make_test_data()
  assert 0

  invert = Inverter()
  test_data = pickle.load( open( TEST_LOC, "rb" ) )

  full_result, rand_cegis_result, cegis_result, nn_cegis_result = [],[],[],[]
  
  for idx, all_data in enumerate(test_data):
    all_data = dedup(all_data)

    print "testing iteration ", idx, " balance ", data_ratio(all_data)
    inv_full_ans = invert.invert_full(all_data, "full")
    inv_rand_cegis_ans = invert.invert_full(all_data, "rand+cegis")
    inv_cegis_ans = invert.invert_cegis(all_data, [], 'cegis')
    inv_nn_cegis_ans = invert.invert_full(all_data, "nn+cegis", confidence=0.8)

    full_result.append(inv_full_ans)
    rand_cegis_result.append(inv_rand_cegis_ans)
    cegis_result.append(inv_cegis_ans)
    nn_cegis_result.append(inv_nn_cegis_ans)

    if idx % 10 == 0:
      print "dumping pickle "
      pickle.dump( (full_result, rand_cegis_result, cegis_result, nn_cegis_result), 
                   open( "_time_exp_result.p", "wb" ) )


