import numpy as np

# takes in parameters 
# returns a predicate function that draws the square
def mk_square(s_x,s_y,w):
  def square(x,y):
    return s_x-w<=x<=s_x+w and s_y-w<=y<=s_y+w
  return square

# takes in 3 integers a,b,c
# returns a linear transform on i, j
# output a single value
def mk_xform(a,b,c):
  def xform(i,j):
    return a * i + b * j + c
  return xform

# takes in a set of parameters
# returns a function that
# when takes in i, j as arguments
# produce a square constraint object
# @ arguments: oxa, oxb, oxc = xform args for the ox prameter
# -----------: oya, oyb, oyc = xform args for the oy prameter
# -----------: 0, 0, wwc     = xform args for the w  prameter
def mk_sq_xform(oxa,oxb,oxc,
                oya,oyb,oyc,
                wwc):
  ox_xform = mk_xform(oxa,oxb,oxc)
  oy_xform = mk_xform(oya,oyb,oyc)
  ow_xform = mk_xform(0, 0, wwc)
  def mk_xform_sq(i,j): 
    xformed_x = ox_xform(i,j)
    xformed_y = oy_xform(i,j)
    xformed_w = ow_xform(i,j)
    return mk_square(xformed_x, xformed_y, xformed_w)

  return mk_xform_sq

# --------------------------- generators -------------------------- #
def gen_w():
  return random.choice([3,5,8])

if __name__ == "__main__":

  from draw import *

  oxa,oxb,oxc,oya,oyb,oyc,wwc = 20, 5, 10, 5, 20, 20, 5
  sq1_xform = mk_sq_xform(oxa,oxb,oxc,oya,oyb,oyc,wwc)
  
  shapes = []

  for i in range(4):
    for j in range(3):
      sq = sq1_xform(i,j)
      shapes.append(sq)

  print shapes 
      
  canvas = np.zeros([100,100])

  for x in range(100):
    for y in range(100):
      for s in shapes:
        if s(x,y):
          canvas[y][x] = 1

  draw_orig(canvas, "./drawings/test_canvas.png")

  print "HOHO"
