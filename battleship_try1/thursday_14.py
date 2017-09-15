from data import *
from solver_bs import *
from naive_baseline import *
from draw import *
import time

test1()

ship_grids, occupied, pose = get_img_class(test=False)
draw_orig(ship_grids, "world.png")

query = mk_query(occupied)

def r_trace(qry):
  obs = []
  for _ in range(90):
    qry_pt = b_random_next_move(obs)
    answer = qry(qry_pt)
    obs.append((qry_pt, answer))
  return obs

trace = deductive_random_trace(boat_shapes, query)
trace = trace_to_obs(trace)
# trace = trace_to_obs(r_trace(query))
print " trace by deductive collection "
print trace, len(trace)
print "original world"
print ship_grids
print occupied
print pose
print "try to recover the ship posis from observations using rohit"
print findConfig(boat_shapes, trace)


