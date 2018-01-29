from model import *
import sys
from dfa_solver import *
from gen import *
import random
import time
import hashlib
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

# check if something is solved, if not return counter examples
def check_solved(synth, all_pairs):
  wrong = []
  for x,y in all_pairs:
    if accept_state(execute_dfa(synth, x)) != y:
      wrong.append((x,y))
  return wrong

class Inverter:

  def __init__(self):
    # self.oracle = Oracle("oracle")
    # self.oracle.restore_model("./models/oracle.ckpt")
    self.clear_solver()

  def clear_solver(self):
    self.s = DFA_Solver(N_STATES, N_CHAR)

  def pick_arbitrary(self, ces):
    ces_ordered = [(int(hashlib.sha1(str(x)).hexdigest(),16),x) for x in ces]
    return min(ces_ordered)[1]

  def invert_cegis(self, all_data, data_subset, method):
    self.clear_solver()
    # build time, solve time, check time
    b_time = 0.0
    s_time = 0.0
    c_time = 0.0
    # print method
    assert method in ["cegis", "r_cegis", 'a_cegis',]
    data_subset = all_data[:1] if data_subset == None else data_subset

    # ces is stored in idx space
    # pick a counter example, also return in idx space
    def ce_picker(ces):
      if method == "cegis":
        return ces[0]
      if method == "r_cegis":
        return random.choice(ces)
      if method == "a_cegis":
        return self.pick_arbitrary(ces)

    # add initial data subset
    b_start = time.time()
    for i, x_y in enumerate(data_subset):
      print "adding ", i
      x,y = x_y
      self.s.add_example(i, x, y)
    b_time += time.time() - b_start

    i = len(data_subset)
    # do the cegis
    while True:
      i += 1
      solve_start = time.time()
      print "solving . . . ", i
      synth = self.s.get_matrix()
      s_time += time.time()-solve_start
      check_start = time.time()
      cex = check_solved(synth, all_data)
      c_time += time.time()-check_start
      if len(cex) == 0:
        return {"build_time" : b_time,
                "solve_time" : s_time,
                "n_examples" : len(data_subset),
                "correct"    : True,
                "check_time" : c_time,
               }
      else:
        ce = ce_picker(cex)
        data_subset.append(ce)
        self.s.add_example(i, ce[0], ce[1])


  def invert_full(self, all_data, method, confidence=0.9):
    fraction = 0.2
    assert method in ["full", "rand", "nn", "nn+cegis", "rand+cegis", "nn_experiment"]

    if method == "full":
      self.clear_solver()
      ret = dict()
      build_start = time.time()
      for i, x_y in enumerate(all_data):
        print "adding ", i
        x,y = x_y
        self.s.add_example(i, x, y)
      build_time = time.time()-build_start
      solve_start = time.time()
      print "solving . . . "
      synth = self.s.get_matrix()
      solve_time = time.time()-solve_start
      correct = len(check_solved(synth, all_data)) == 0
      assert correct
      ret['build_time'] = build_time
      ret['solve_time'] = solve_time
      ret['n_examples'] = len(all_data)
      ret['correct'] = correct
      return ret

    if method == "rand":
      assert 0, "NOT IMPLEMENTED UROD BLYAT"

    if method == "nn":
      assert 0, "NOT IMPLEMENTED UROD BLYAT"

    if method == "rand+cegis":
      sub_constraints = random.sample(constraints, int(fraction * len(constraints)))
      return self.invert_cegis(constraints, full_img, "r_cegis", sub_constraints)

    if method == "nn+cegis":
      s_time = time.time()
      trace_obs = self.oracle.get_trace(full_img, 20, confidence)
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
      trace_obs = self.oracle.get_trace(full_img, 20, confidence)
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

if __name__ == "__main__":
  invert = Inverter()

  test_mat = sample_matrix()
  all_data = generate_examples(test_mat, 1000)

  inv_full_ans = invert.invert_full(all_data, "full")
  print inv_full_ans

  inv_cegis_ans = invert.invert_cegis(all_data, [], 'cegis')
  print inv_cegis_ans

















