from model import *
from draw import *
import sys
from graphix_solver import *
import random
import time

def obs_to_constraints(trace, r_square, r_line):
  trace_coords = [x[0] for x in trace]

  sub_constraints = []
  for cc in trace_coords:
    # flip the coordinate to x,y space
    id1,id2 = cc
    x,y = rev(id1,id2)
    s_val = bool(r_square[id1][id2] == 1.0)
    l_val = bool(r_line[id1][id2] == 1.0)
    sub_constraints.append(((x,y),'square',s_val))
    sub_constraints.append(((x,y),'line',l_val))
  return sub_constraints

class Inverter:

  def __init__(self):
    self.impnet = Implynet(tf.Session())
    self.impnet.load_model("./models/imply.ckpt")
    self.s = DrawingSolver()

  def clear_solver(self):
    self.s = DrawingSolver()

  def invert_cegis(self, constraints, r_squares, r_lines, method="cegis", sub_constraints=None):
    full_img = np.clip(r_squares + r_lines, 0, 1)
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
        sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, full_img)
        for pr, id1_id2 in sorted_unlikely:
          if id1_id2 in ces:
            return id1_id2
      if method == "nn":
        sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, full_img, i)
        id1_id2 = sorted_unlikely[0][1]
        return id1_id2

    while True:
      i += 1
      paras = self.s.solve(8, sub_constraints, {})
      print paras
      # counter example in idx space
      ces = check(paras, r_squares, r_lines, i)
      if ces == None:
        return paras
      else:
        id1,id2 = ce_picker(ces)
        x,y = rev(id1,id2)
        square_val = bool(r_squares[id1][id2] == 1)
        line_val =   bool(r_lines[id1][id2] == 1)
        sub_constraints +=    [((int(x), int(y)), 'square', square_val),
                               ((int(x), int(y)), 'line', line_val)]
        

  def invert_full(self, constraints, r_squares, r_lines, method="full", fraction=0.1):
    full_img = np.clip(r_squares + r_lines, 0, 1)
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
      sub_constraints = obs_to_constraints(trace_obs, r_squares, r_lines)
      # the length won't perfectly lineup so we can clip a bit
      sub_constraints = sub_constraints[:int(fraction * len(constraints))]
      params = self.s.solve(8, sub_constraints)
      return params

    if method == "nn":
      trace_obs = self.impnet.get_trace(full_img, 20, fraction)
      sub_constraints = obs_to_constraints(trace_obs, r_squares, r_lines)
      # the length won't perfectly lineup so we can clip a bit
      sub_constraints = sub_constraints[:int(fraction * len(constraints))]
      params = self.s.solve(8, sub_constraints)
      return params

    if method == "nn+cegis":
      trace_obs = self.impnet.get_trace(full_img, 20, fraction)
      sub_constraints = obs_to_constraints(trace_obs, r_squares, r_lines)
      return self.invert_cegis(constraints, r_squares, r_lines, "r_cegis", sub_constraints)


















