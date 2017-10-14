import sys
import numpy as np
from graphix_lang import L

def same_line_print(message):
  sys.stdout.write("\r" + message)
  sys.stdout.flush()

def mk_query(img):
  def qry(x_y):
    x,y = x_y
    if img[x][y] == 1.0:
      return [1.0, 0.0]
    else:
      return [0.0, 1.0]
  return qry

def img_2_constraints(img_squares, img_lines):
  M,N = img_squares.shape
  ret = []
  for y in range(M):
    for x in range(N):
      square_val = bool(img_squares[y][x] == 1)
      line_val = bool(img_lines[y][x] == 1)
      ret.append(((x,y),'square',square_val))
      ret.append(((x,y),'line',line_val))
      
  return ret

def img_2_labels(img):
  full_obs = np.zeros([L,L,2])
  qry = mk_query(img)
  for i in range(L):
    for j in range(L):
      full_obs[i][j] = qry((i,j))
  return full_obs

