from model import *
from solver_bs import *
from data import boat_shapes

def to_vec(x):
  if x == True: return [1.0, 0.0]
  if x == False: return [0.0, 1.0]
  assert 0, "should not happen "

class Oracle(Implynet):

  def __init__(self, model_loc): 
    print "making a embed_1_layer model "
    impnet = Implynet(embed_1_layer, "1layer", tf.Session())
    impnet.load_model(model_loc)
    self.impnet = impnet
    self.sess = self.impnet.sess
    

  def get_all_preds(self, obs):
    # extend the observations with unambiguous points
    ambiguous_obs, implied_obs = sat_infer(boat_shapes, obs)
    implied_obs = [(imp_ob[0], to_vec(imp_ob[1])) for imp_ob in implied_obs]
    all_preds = self.impnet.get_all_preds(implied_obs)
    for loc, ans in implied_obs:
      all_preds[loc[0]][loc[1]] = ans
    return all_preds

