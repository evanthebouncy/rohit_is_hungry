from data import *
from solver_bs import *
import random

def neighbors(crd):
  xx, yy = crd
  return [(xx+1,yy), (xx-1, yy), (xx, yy+1), (xx, yy-1)]

def has_nearby(obs):
  all_obs = set([o[0] for o in obs])
  all_yes = [o[0] for o in obs if o[1][0] > o[1][1]]
  for i in range(L):
    for j in range(L):
      neib = neighbors((i,j))
      for nb in neib:
        if nb in all_yes and (i,j) not in all_obs:
          return (i,j)
  return False

def random_move(obs): 
  all_crds = [(i,j) for i in range(L) for j in range(L)]
  for crd in [o[0] for o in obs]:
    all_crds.remove(crd)
  return random.choice(all_crds)

def next_move(obs):
  if has_nearby(obs):
    return has_nearby(obs)
  else:
    return random_move(obs)
  
def baseline_get_trace(qry):
  obs = []
  for _ in range(L*L):
    qry_pt = next_move(obs)
    answer = qry(qry_pt)
    obs.append((qry_pt, answer))
  return obs

def baseline_get_all_preds(trace_prefix):
  ret = np.zeros([L,L,2])
  for i in range(L):
    for j in range(L):
      ret[i][j] = [0.0, 1.0]
  for ob in trace_prefix:
    crd, ans = ob
    ret[crd[0]][crd[1]] = ans
  return ret 

def baseline_pred_acc(b_preds, qry):
  num_cor = 0
  for i in range(L):
    for j in range(L):
      if b_preds[i][j] == qry((i,j)):
        num_cor += 1
  return float(num_cor) / L*L


def b_random_next_move(obs):
  all_obs = [(i,j) for i in range(L) for j in range(L)]
  for oo in [o[0] for o in obs]:
    all_obs.remove(oo)
  return random.choice(all_obs)

def rrandom_trace(qry):
  obs = []
  for _ in range(L*L):
    qry_pt = b_random_next_move(obs)
    answer = qry(qry_pt)
    obs.append((qry_pt, answer))
  return obs


# use constraints to make more informed trace
def informed_next_move(ships, obs, implied):
  # all possible locations
  all_locs = [(x,y) for x in range(L) for y in range(L)]
  # all known locations, either observed or implied
  known_q_space = [ooo[0] for ooo in obs] + implied
  print known_q_space
  # filter
  all_locs = [xx for xx in all_locs if xx not in known_q_space]

  random.shuffle(all_locs)

  # a set of implied observations that can already been deduced 
  implied = [] 

  for loc in all_locs:
    if is_amb(loc, ships, trace_to_obs(obs)):
      return loc, implied
    else:
      implied.append(loc)
  return None, []

def deductive_random_trace(ships, qry):
  obs = []
  implied = []
  for _ in range(L*L):
    qry_pt, new_implied = informed_next_move(ships, obs, implied)
    implied += new_implied
    if not qry_pt:
      break
    answer = qry(qry_pt)
    obs.append((qry_pt, answer))
    print obs
  return obs

def trace_to_obs(trace):
  ret = []
  for tr in trace:
    cord, ans = tr
    aa = True if ans[0]>ans[1] else False
    ret.append((cord, aa))
  return ret

