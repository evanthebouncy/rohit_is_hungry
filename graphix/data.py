from graphix_lang import *

N_BATCH = 20
def mk_query(img):
  def qry(x_y):
    x,y = x_y
    if img[x][y] == 1.0:
      return [1.0, 0.0]
    else:
      return [0.0, 1.0]
  return qry

def img_2_bool(img):
  full_obs = np.zeros([L,L,2])
  qry = mk_query(img)
  for i in range(L):
    for j in range(L):
      full_obs[i][j] = qry((i,j))
  return full_obs


def rand_data(epi):

  partial_obss = []
  full_obss = []

  for bb in range(N_BATCH):
    # generate a hidden variable X
    # get a single thing out
    img = sample_scene()
    qry = mk_query(img)
    partial_obs = np.zeros([L,L,2])
    full_obs = np.zeros([L,L,2])
    for i in range(L):
      for j in range(L):
        full_obs[i][j] = qry((i,j))
        if np.random.random() < epi:
          partial_obs[i][j] = qry((i,j))
    partial_obss.append(partial_obs)
    full_obss.append(full_obs)

  return  np.array(partial_obss),\
          np.array(full_obss)

# while True:
#   rand_data(0.1, 2)
#   print "HAHA!"
