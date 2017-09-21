from solver_bs import *
from data import *
from draw import *

def to_vec(x):
  if x == True: return [1.0, 0.0]
  if x == False: return [0.0, 1.0]
  assert 0, "should not happen "
# somehow this import breaks the solver ?
# from tensorflow.examples.tutorials.mnist import input_data

test1()

obs1 = [((7, 6), False), ((3, 4), False), ((7, 8), False), ((2, 6), False), ((8, 8), False), ((1, 4), False), ((5, 7), False), ((2, 9), False), ((0, 0), False), ((6, 4), True), ((2, 7), False), ((8, 7), False), ((6, 5), True), ((1, 9), False), ((1, 0), False), ((6, 9), False), ((3, 1), False), ((2, 5), False), ((0, 6), False), ((3, 9), False), ((5, 9), True)]

obs2 = [((1, 0), False), ((0, 8), True), ((9, 4), False), ((4, 0), False), ((6, 3), False), ((9, 8), False), ((0, 3), False), ((7, 8), False), ((8, 4), True), ((9, 0), False), ((4, 7), False), ((4, 1), False), ((8, 8), True), ((8,7), False)]



obs = obs2

obs_haha = [(xx[0], to_vec(xx[1])) for xx in obs]
draw_obs(obs_haha, "failure.png")

assert len(obs) == len(set(obs))

print findConfig(boat_shapes, obs)
