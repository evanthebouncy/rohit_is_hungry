import random
from random import randint
import numpy as np

# N_CHAR = 2
# L = 10
# N_STATES = 6

N_CHAR = 2
L = 10
N_STATES = 6

def get_letter():
  return randint(0, N_CHAR-1)

def get_input_string(L):
  return [get_letter() for _ in range(L)]

# a matrix is valid only if it can accept some and reject some other
def check_valid(matrix):
  pos, neg = [], []
  for i in range(100):
    input_str = get_input_string(L)
    output_TF = accept_state( execute_dfa(matrix, input_str) )

    if output_TF is True:
      pos.append((input_str, output_TF))
    if output_TF is False:
      neg.append((input_str, output_TF))
  return len(pos) > 0 and len(neg) > 0

# the transition matrix is a matrix of shape [N_STATES, N_CHAR] and each entry N_STATE
def sample_matrix():
  ret = [[randint(0, N_STATES-1) for i in range(N_CHAR)] for _ in range(N_STATES)]
  if check_valid(ret):
    return ret
  else:
    return sample_matrix()

# to use the transition matrix, notice it is of shape
# [N_STATES, N_CHAR] and each entry N_STATE
# so if cur_state is 3, and you read character 2, you go to
# transition_matrix[3][2] and read off the value there, say it's 1
# now cur_state is 1
def execute_dfa(matrix, input_string):
  cur_state = 0
  # print matrix
  try:
    for x in input_string:
      cur_state = matrix[cur_state][x]
    # print x, cur_state
    return cur_state
  except:
    # might get IndexError: string index out of range if doesn't exist, so clearly wrong
    return -1

# we deem a dfa "accepts" an input string if the final state is the last one
def accept_state(state):
  return state == (N_STATES - 1)

def dedup(data):
  ahem = set()
  for d in data:
    ahem.add(repr(d))
  ret = []
  for d in ahem:
    ret.append(eval(d))
  return ret


# generate n input output examples
def generate_examples(matrix, n):
  return generate_balanced_examples(matrix, n)
  ret = []

  while len(ret) < n:
    input_str = get_input_string(L)
    output_TF = accept_state( execute_dfa(matrix, input_str) )
    ret.append( (input_str, output_TF) )

  random.shuffle(ret)
  return ret

# generate n input output examples
def generate_balanced_examples(matrix, n):
  pos = []
  neg = []

  while min( len(pos), len(neg) ) < n / 2:
    input_str = get_input_string(L)
    output_TF = accept_state( execute_dfa(matrix, input_str) )

    if output_TF is True:
      pos.append((input_str, output_TF))
    if output_TF is False:
      neg.append((input_str, output_TF))

  ret = pos[:n/2] + neg[:n/2]
  random.shuffle(ret)
  return ret


# turn examples into numpy arrays
def examples_to_numpy(examples):
  def to_1hot(char):
    to_ret = [0.0 for _ in range(N_CHAR)]
    to_ret[char] = 1.0
    return to_ret

  ret_in, ret_out = [], []
  for e in examples:
    xx, outt = e
    xx_np = [to_1hot(x) for x in xx]
    outt_np = [1.0, 0.0] if outt else [0.0, 1.0]
    ret_in.append(xx_np)
    ret_out.append(outt_np)

  return np.array(ret_in), np.array(ret_out)

def gen_train_data(n=100, together=False):
  m = sample_matrix()
  examples = generate_balanced_examples(m, n)
  np_in, np_out = examples_to_numpy(examples)

  all_idxs = [i for i in range(n)]
  random.shuffle(all_idxs)
  to_observe = random.randint(1, n-1)

  observed_idxs   = all_idxs[:to_observe]
  unobserved_idxs = all_idxs[to_observe:]

  seen_in, seen_out = [np_in[i] for i in observed_idxs], [np_out[i] for i in observed_idxs]
  unseen_in, unseen_out = [np_in[i] for i in unobserved_idxs], [np_out[i] for i in unobserved_idxs]

  if not together:
    return np.array(seen_in),\
           np.array(seen_out),\
           np.array(unseen_in),\
           np.array(unseen_out)
  else:
    return np_in, np_out


def gen_exam():
  m = sample_matrix()
  examples = generate_examples(m, 100)
  train = examples[:80]
  test = examples[80:]
  return train, test



if __name__ == "__main__":
  m = sample_matrix()
  examples = generate_examples(m, 10)
#   np_in, np_out = examples_to_numpy(examples)
#   for x in zip(examples, np_in, np_out):
#     print x[0]
#     print x[1], x[2]
  examples = generate_examples(m, 20)
  for i, x in enumerate(examples):
    if i < 12:
      print x
    else: print x[0]
  print 100*'\n'
  print examples

  x,y,z,w = gen_train_data()
  print len(x), len(y), len(z), len(w)

