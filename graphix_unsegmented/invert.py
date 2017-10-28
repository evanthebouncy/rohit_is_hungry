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

  def pick_arbitrary(self, ces):
    ces_ordered = [(hash(x),x) for x in ces]
    return min(ces_ordered)[1]

  def invert_cegis(self, constraints, render, method="cegis", sub_constraints=None):
    b_time = 0
    s_time = 0
    # print method
    assert method in ["cegis", "r_cegis", 'a_cegis',]
    i = 0
    sub_constraints = constraints[:1] if sub_constraints == None else sub_constraints

    # ces is stored in idx space
    # pick a counter example, also return in idx space
    def ce_picker(ces):
      if method == "cegis":
        return ces[0]
      if method == "r_cegis":
        return random.choice(ces)
      if method == "a_cegis":
        return self.pick_arbitrary(ces)
#       if method == "nn_cegis":
#         ces = set(ces)
#         sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, render)
#         for pr, id1_id2 in sorted_unlikely:
#           if id1_id2 in ces:
#             return id1_id2
#       if method == "nn":
#         sorted_unlikely = self.impnet.get_sorted_unlikely(sub_constraints, render, i)
#         id1_id2 = sorted_unlikely[0][1]
#         return id1_id2

    while True:
      i += 1
      paras = self.s.solve(8, sub_constraints, {})
      # print paras
      b_time += paras['building_time']
      s_time += paras['solving_time']
      # counter example in idx space
      ces = check(paras, render, i)
      if ces == None:
        paras['building_time'] = b_time
        paras['solving_time'] = s_time
        paras['ce_size'] = len(sub_constraints)
        return paras
      else:
        id1,id2 = ce_picker(ces)
        x,y = rev(id1,id2)
        val = bool(render[id1][id2] == 1)
        sub_constraints +=    [((int(x), int(y)), val)]

  def invert_full(self, constraints, full_img, method="full", confidence=0.9):
    fraction = 0.2
    assert method in ["full", "rand", "nn", "nn+cegis", "rand+cegis", "nn_experiment"]

    if method == "full":
      params = self.s.solve(8, constraints)
      params['ce_size'] = len(constraints)
      return params

    if method == "rand":
      sub_constraints = random.sample(constraints, int(fraction * len(constraints)))
      params = self.s.solve(8, sub_constraints)
      params['ce_size'] = len(sub_constraints)
      square,line = mk_scene(params)
      recovered = render(square+line)
      diff = full_img - recovered
      diff_idx1, diff_idx2 = np.where(diff != 0)
      params['error'] = float(len(diff_idx1))
      return params

    if method == "nn":
      s_time = time.time()
      trace_obs = self.impnet.get_trace(full_img, 20, confidence)
      nn_time = time.time() - s_time
      sub_constraints = obs_to_constraints(trace_obs, full_img)
      params = self.s.solve(8, sub_constraints)
      params['ce_size'] = len(sub_constraints)
      params['nn_time'] = nn_time
      return params

    if method == "rand+cegis":
      sub_constraints = random.sample(constraints, int(fraction * len(constraints)))
      return self.invert_cegis(constraints, full_img, "r_cegis", sub_constraints)

    if method == "nn+cegis":
      s_time = time.time()
      trace_obs = self.impnet.get_trace(full_img, 20, confidence)
      nn_time = time.time() - s_time
      sub_constraints = obs_to_constraints(trace_obs, full_img)

      params = self.s.solve(8, sub_constraints)
      square,line = mk_scene(params)
      recovered = render(square+line)
      diff = full_img - recovered
      diff_idx1, diff_idx2 = np.where(diff != 0)
      self.clear_solver()

      orig_size = len(sub_constraints)
      params = self.invert_cegis(constraints, full_img, "r_cegis", sub_constraints)
      params['nn_time'] = nn_time
      params['error'] = float(len(diff_idx1))
      params['orig_subset_size'] = orig_size
      return params

    if method == "nn_experiment":
      s_time = time.time()
      trace_obs = self.impnet.get_trace(full_img, 20, confidence)
      nn_time = time.time() - s_time
      sub_constraints = obs_to_constraints(trace_obs, full_img)

      params = self.s.solve(8, sub_constraints)
      square,line = mk_scene(params)
      recovered = render(square+line)
      diff = full_img - recovered
      diff_idx1, diff_idx2 = np.where(diff != 0)
      self.clear_solver()
      orig_size = len(sub_constraints)

      params = self.invert_cegis(constraints, full_img, "r_cegis", sub_constraints)
      params['nn_time'] = nn_time
      params['error'] = float(len(diff_idx1))
      params['orig_subset_size'] = orig_size
      return params



















