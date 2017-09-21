from oracle import *
from draw import *
from test_data import *

oracle = Oracle("./models/imply_1layer.ckpt")

img, _x, _poss = get_img_class()
qry = mk_query(_x) 

trace = oracle.get_active_trace(qry, epi=0.0)

draw_orig(img, "drawings/orig.png")
for i in range(len(trace)):
  trace_prefix = trace[:i]
  all_preds = oracle.get_all_preds(trace_prefix)
  draw_allob(all_preds, "drawings/pred_ob{0}.png".format(i), trace_prefix)
