from model import *
from draw import *
import sys
from graphix_solver import *
import random
import time

def obs_to_constraints(trace, render):
  trace_coords = [x[0] for x in trace]

  sub_constraints = []
  for cc in trace_coords:
    # flip the coordinate to x,y space
    id1,id2 = cc
    x,y = rev(id1,id2)
    val = bool(render[id1][id2] == 1.0)
    sub_constraints.append(((x,y),val))
  return sub_constraints

class Inverter:

  def __init__(self):
    self.impnet = Implynet(tf.Session())
    self.impnet.load_model("./models/imply.ckpt")
    self.s = DrawingSolver()

  def clear_solver(self):
    self.s = DrawingSolver()

  def invert_cegis(self, constraints, render, method="cegis", sub_constraints=None):
    print method
    assert method in ["cegis", "r_cegis", "nn_cegis", "nn",]
    i = 0
    sub_constraints = constraints[:2] if sub_constraints == None else sub_constraints

    # ces is stored in idx space
    # pick a counter example, also return in idx space
    def ce_picker(ces):
      if method == "cegis":
        return ces[0]
      if method == "r_cegis":
        return random.choice(ces)
      if method == "nn_cegis":
        ces = set(ces)
        sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, render)
        for pr, id1_id2 in sorted_unlikely:
          if id1_id2 in ces:
            return id1_id2
      if method == "nn":
        sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, render, i)
        id1_id2 = sorted_unlikely[0][1]
        return id1_id2

    while True:
      i += 1
      paras = self.s.solve(8, sub_constraints, {})
      print paras
      # counter example in idx space
      ces = check(paras, render, i)
      if ces == None:
        return paras
      else:
        id1,id2 = ce_picker(ces)
        x,y = rev(id1,id2)
        val = bool(render[id1][id2] == 1)
        sub_constraints +=    [((int(x), int(y)), val)]

  def invert_full(self, constraints, full_img, method="full", fraction=0.1):
    assert method in ["full", "rand", "nn", "nn+cegis"]

    if method == "full":
      params = self.s.solve(8, constraints)
      return params

    if method == "rand":
      sub_constraints = random.sample(constraints, int(fraction * len(constraints)))
      params = self.s.solve(8, sub_constraints)
      return params

    if method == "nn":
      trace_obs = self.impnet.get_trace(full_img, 20, fraction)
      sub_constraints = obs_to_constraints(trace_obs, full_img)
      # the length won't perfectly lineup so we can clip a bit
      sub_constraints = sub_constraints[:int(fraction * len(constraints))]
      params = self.s.solve(8, sub_constraints)
      return params

    if method == "nn+cegis":
      trace_obs = self.impnet.get_trace(full_img, 20, fraction)
      sub_constraints = obs_to_constraints(trace_obs, full_img)
      return self.invert_cegis(constraints, full_img, "r_cegis", sub_constraints)


















