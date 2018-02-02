import random
import numpy as np

L = 10

def gen_ordering():
  to_ret = [_ for _ in range(L)]
  random.shuffle(to_ret)
  return to_ret

def get_all_data(ordering):
  to_ret = []
  for i in range(L):
    for j in range(L):
      i_pos = ordering.index(i)
      j_pos = ordering.index(j)
      to_ret.append( ( (i,j), i_pos < j_pos) )
  return to_ret

def get_data(ordering):
  all_data = get_all_data(ordering)
  rand_len = int(len(all_data) * np.random.uniform(low=0.3, high=1.0))
  random.shuffle(all_data)
  return all_data[:rand_len]

if __name__ == "__main__":
  ord1 = gen_ordering()
  print ord1
  print get_data(ord1)

