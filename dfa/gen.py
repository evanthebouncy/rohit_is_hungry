import random
from random import randint

N_CHAR = 2
L = 10
N_STATES = 6

def get_letter():
  return randint(0, N_CHAR-1)

def get_input_string(L):
  return [get_letter() for _ in range(L)]

# the transition matrix is a matrix of shape [N_STATES, N_CHAR] and each entry N_STATE
def sample_matrix():
  return [[randint(0, N_STATES-1) for i in range(N_CHAR)] for _ in range(N_STATES)]

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

# generate n input output examples
def generate_examples(matrix, n):
  ret = []
  for i in range(n):
    input_str = get_input_string(L)
    ret.append( (input_str, accept_state( execute_dfa(matrix, input_str) ) ) )
  return ret

# we deem a dfa "accepts" an input string if the final state is the last one
def accept_state(state):
  return state == (N_STATES - 1)

if __name__ == "__main__":
  m = sample_matrix()
  examples = generate_examples(m, 1)
  for e in examples:
    print e
