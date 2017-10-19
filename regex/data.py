from generator import *
import numpy as np

L = 120

def gen_data():
  par = generate_params()
  pos = [generate_positive_example(par) for i in range(random.randint(0, 20))]
  neg = [generate_negative_example(par) for i in range(random.randint(0, 20))]
  target = [(True, generate_positive_example(par)) if random.random() < 0.5\
      else (False, generate_negative_example(par)) for _ in range(20)]
  return par, pos, neg, zip(*target)

def pad(seq):
  ret = [2 for _ in range(L)]
  for i, ss in enumerate(seq):
    ret[i] = int(ss)
  return ret

def vec(seq_elem):
  if seq_elem == 0: return [1.0, 0.0, 0.0]
  if seq_elem == 1: return [0.0, 1.0, 0.0]
  if seq_elem == 2: return [0.0, 0.0, 1.0]
  print seq_elem, type(seq_elem)
  assert 0, "Impossibru!"


def vectorize_input_str(str_batch, label):
  str_batch = [L*'2'] + str_batch

  label = [1.0, 0.0] if label == True else [0.0, 1.0]
  ret = []
  for str1 in str_batch:
    seq = pad(list(str1)) 
    seq = [label+vec(x) for x in list(seq)]
    ret.append(seq)
  return np.array(ret)
  
def vectorize_target(target):
  labels, inp_strs = target
  print labels
  print inp_strs
  
  inp_seqs = [pad(inp_str) for inp_str in inp_strs]
  labels = [ [1.0, 0.0] if label == True else [0.0, 1.0] for label in labels]
  target = [[vec(int(x)) for x in inp_seq] for inp_seq in inp_seqs]

  return np.array(labels), np.array(target)

def gen_train_data():
  par, pos, neg, target = gen_data()

  pos_ex = vectorize_input_str(pos, True)
  neg_ex = vectorize_input_str(neg, False)
  together = np.concatenate([pos_ex, neg_ex], axis=0)
  target_lab, target_inp = vectorize_target(target)

  return together, target_inp, target_lab

if __name__ == "__main__":
  par, pos, neg, target = gen_data()
  print par
  print pos
  print neg
  print target
  print max( [(len(p),p) for p in pos] +[0])
  print max( [(len(p),p) for p in neg] +[0])

  print "=============================================="
  pos_ex = vectorize_input_str(pos, True)
  neg_ex = vectorize_input_str(neg, False)
  together = np.concatenate([pos_ex, neg_ex], axis=0)
  print together.shape

  target_lab, target_inp = vectorize_target(target)
  print target_lab
  print target_inp 

  print "====================== "

  known_str, new_str, new_lab =  gen_train_data()
  print known_str.shape, new_str.shape, new_lab.shape

  
