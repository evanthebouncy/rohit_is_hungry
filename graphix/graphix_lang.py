import numpy as np
import random

# null shape
def mk_null():
  def null(x,y):
    return False
  return null

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

# takes in a set of parameters
# returns a function that
# when takes in i, j as arguments
# produce a line constraint object
# @ arguments: sxa, sxb, sxc = xform args for the sx prameter
# -----------: sya, syb, syc = xform args for the sy prameter
# ^ with these 2 xforms it will produce a start point
# @ arguments: movex, movey
# ^ with these 2 xforms it will creat the end-point based off of the start
def mk_line_xform(sxa,sxb,sxc,
                  sya,syb,syc,
                  movex, movey, supress_i, supress_j):
  sx_xform = mk_xform(sxa,sxb,sxc)
  sy_xform = mk_xform(sya,syb,syc)
  def mk_xform_line(i,j): 
    xformed_sx = sx_xform(i,j)
    xformed_sy = sy_xform(i,j)
    t_x = xformed_sx + movex
    t_y = xformed_sy + movey
    if supress_i and i == 0:
      return mk_null()
    if supress_j and j == 0:
      return mk_null()
    return mk_line(xformed_sx, xformed_sy, t_x, t_y)

  return mk_xform_line

# render shapes onto a 100 by 100 canvas
def render(shapes):
  canvas = np.zeros([100,100])

  for x in range(100):
    for y in range(100):
      for s in shapes:
        if s(x,y):
          canvas[y][x] = 1

  return canvas

# --------------------------- generators -------------------------- #
def sample_w():
  return [ random.choice([2,5,8]) ]

def sample_pos():
  base_choice = [0, 5, 10, 20, 40]
  x_a = random.choice(base_choice)
  x_b = random.choice(base_choice)
  x_c = random.choice(base_choice)
  y_a = random.choice(base_choice)
  y_b = random.choice(base_choice)
  y_c = random.choice(base_choice)
  return [x_a, x_b, x_c, y_a, y_b, y_c]

def sample_line_wh():
  w = random.choice(range(40))
  h = random.choice(range(40))
  return [w-20, h-20]

def sample_supress_iter():
  return [ random.choice([True, False]) ]

def sample_iter():
  return random.choice(range(1,4))

def square_no_overlap(squares):
  for i in range(100):
    for j in range(100):
      preds = [1 if s(i,j) else 0 for s in squares]
      if sum(preds) > 1:
        return False
  return True 
  
def _sample_scene():
  num_squares = 3
  num_lines = 3
  num_i_iter = sample_iter()
  num_j_iter = sample_iter()

  square_params = [sample_pos() + sample_w()\
                   for _ in range(num_squares)]
  line_params = [sample_pos() + sample_line_wh()\
                 + sample_supress_iter() + sample_supress_iter()\
                 for _ in range(num_lines)]

  square_xforms = [mk_sq_xform(*s_par) for s_par in square_params]
  line_xforms = [mk_line_xform(*l_par) for l_par in line_params]

  squares = []
  lines = []
  for i in range(num_i_iter):
    for j in range(num_j_iter):
      for sq_xform in square_xforms:
        squares.append(sq_xform(i,j))
      for line_xform in line_xforms:
        lines.append(line_xform(i,j))

  return squares, lines

def sample_scene():
  squares, lines = _sample_scene()
#  while not square_no_overlap(squares):
#    squares, lines = _sample_scene()

  return render(squares + lines)
  

if __name__ == "__main__":

  from draw import *

  def hand_example():
    oxa,oxb,oxc,oya,oyb,oyc,wwc = 20, 5, 10, 5, 20, 20, 5
    sq1_xform = mk_sq_xform(oxa,oxb,oxc,oya,oyb,oyc,wwc)
    
    sxa,sxb,sxc,sya,syb,syc = 20, 5, 10, 5, 20, 20
    line1_xform = mk_line_xform(sxa, sxb, sxc, sya, syb, syc, 20, 20, True, True)

    shapes = []

    for i in range(4):
      for j in range(3):
        sq = sq1_xform(i,j)
        line = line1_xform(i,j)
        shapes.append(sq)
        shapes.append(line)

    print shapes 

  scene = sample_scene()

  draw_orig(scene, "./drawings/test_canvas.png")

  print "HOHO"
