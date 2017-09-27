import numpy as np
import random

# takes in parameters: center x, center y, width
# returns a predicate function that draws the square
def mk_square(s_x,s_y,w):
  def square(x,y):
    return s_x-w<=x<=s_x+w and s_y-w<=y<=s_y+w
  return square

# takes in parameters: start x, start y, terminal x, terminal y
# returns a predicate function that draws the line
def mk_line(s_x,s_y,t_x,t_y):
  x_min, x_max = min(s_x,t_x), max(s_x,t_x)
  y_min, y_max = min(s_y,t_y), max(s_y,t_y)
  line_diffx = t_x - s_x
  line_diffy = t_y - s_y

  def line(x,y):
    # if out of bound then no way
    if x < x_min or x > x_max or y < y_min or y > y_max:
      return False

    diffx, diffy = x - s_x, y - s_y
    err = abs(diffx * line_diffy - diffy * line_diffx) 

    def left_right_logic():
      up_diffy   = diffy - 1
      down_diffy = diffy + 1

      up_err = abs(diffx * line_diffy - up_diffy * line_diffx) 
      down_err = abs(diffx * line_diffy - down_diffy * line_diffx) 

      return err <= up_err and err <= down_err

    def up_down_logic():
      left_diffx = diffx - 1
      right_diffx = diffx + 1
      left_err = abs(left_diffx * line_diffy - diffy * line_diffx)
      right_err = abs(right_diffx * line_diffy - diffy * line_diffx)

      return err <= left_err and err <= right_err

    return left_right_logic() or up_down_logic()

  return line
    

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
  return random.choice([2,5,8])

if __name__ == "__main__":

  from draw import *

  oxa,oxb,oxc,oya,oyb,oyc,wwc = 20, 5, 10, 5, 20, 20, 2
  sq1_xform = mk_sq_xform(oxa,oxb,oxc,oya,oyb,oyc,wwc)
  
  shapes = []

#   for i in range(4):
#     for j in range(3):
#       sq = sq1_xform(i,j)
#       shapes.append(sq)

  print shapes 

  for i in range(10):
    aa = random.choice(range(100))
    bb = random.choice(range(100))
    cc = random.choice(range(100))
    dd = random.choice(range(100))
    shapes.append(mk_line(aa,bb, cc, dd))
      
  canvas = np.zeros([100,100])

  for x in range(100):
    for y in range(100):
      for s in shapes:
        if s(x,y):
          canvas[y][x] = 1

  draw_orig(canvas, "./drawings/test_canvas.png")

  print "HOHO"
