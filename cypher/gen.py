import random
from random import randint

N_CHAR = 10

def get_letter():
  return randint(0, N_CHAR-1)

def get_message(L):
  return [get_letter() for _ in range(L)]

def apply_rot(xs, rot):
  ret = []
  for i, x in enumerate(xs):
    ret.append( (rot[i % len(rot)] + x) % N_CHAR)
  return ret

def apply_shift(xs, k):
  assert k < N_CHAR, "yo bro"
  front = xs[:k]
  back = xs[k:]
  return back + front

def sample_encryptor(n_steps):
  ret = []
  for i in range(n_steps):
    if random.random() < 0.5:
      ret.append( ("shift", randint(0, N_CHAR-1)) )
    else:
      ret.append( ("rot", [randint(0, N_CHAR-1) for _ in range(3)]) )
  return ret 

def apply_encryptor(x, encryptor):
  for enc_kind, enc_key in encryptor:
    if enc_kind == "shift":
      x = apply_shift(x, enc_key)
    if enc_kind == "rot":
      x = apply_rot(x, enc_key)
  return x

if __name__ == "__main__":
  msg = get_message(10)
  encryptor = sample_encryptor(4)
  print msg
  print encryptor
  print apply_encryptor(msg, encryptor)
