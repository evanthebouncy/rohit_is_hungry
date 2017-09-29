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
# produce a coordinate offset transform
# @ arguments: oxa, oxb, oxc = xform args for the ox prameter
# -----------: oya, oyb, oyc = xform args for the oy prameter
def mk_coord_xform(oxa,oxb,oxc, oya,oyb,oyc):
  ox_xform = mk_xform(oxa,oxb,oxc)
  oy_xform = mk_xform(oya,oyb,oyc)
  def mk_xform_coord(i,j): 
    xformed_x = ox_xform(i,j)
    xformed_y = oy_xform(i,j)
    return xformed_x, xformed_y

  return mk_xform_coord

# given an coord x and y 
# produce a square with offset and width
def mk_sq_from_coord(coord_x, coord_y, offset_x, offset_y, w):
  return mk_square(coord_x + offset_x,
                   coord_y + offset_y,w)


# given coord x and y
# produce a line with start offset, end offset
def mk_line_from_coord(coord_x, coord_y, i, j,
                       start_x, start_y,
                       end_x, end_y,
                       supress_i, supress_j):
  if supress_i and i == 0:
    return mk_null()
  if supress_j and j == 0:
    return mk_null()
  return mk_line(coord_x + start_x, coord_y + start_y,
                 coord_x + end_x, coord_y + end_y)

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

def sample_coord_xform_params():
  # base_choice = [0, 5, 10, 20, 40]
  base_choice = range(30)
  x_a = random.choice(base_choice)
  x_b = random.choice(base_choice)
  x_c = random.choice(base_choice)
  y_a = random.choice(base_choice)
  y_b = random.choice(base_choice)
  y_c = random.choice(base_choice)
  return [x_a, x_b, x_c, y_a, y_b, y_c]

def sample_square_params():
  base_choice = range(40)
  offset_x = random.choice(base_choice) - 20
  offset_y = random.choice(base_choice) - 20
  w = random.choice([2,3,5])
  return [offset_x, offset_y, w]

def sample_line_params():
  def sample_supress_iter():
    return [ random.choice([True, False]) ]

  base_choice = range(80)
  s_x = random.choice(base_choice) - 40
  s_y = random.choice(base_choice) - 40
  t_x = random.choice(base_choice) - 40
  t_y = random.choice(base_choice) - 40
  return [s_x, s_y, t_x, t_y]\
          + sample_supress_iter()\
          + sample_supress_iter()


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
  num_lines = 4
  num_i_iter = sample_iter()
  num_j_iter = sample_iter()

  coord_params = sample_coord_xform_params()
  square_params = [sample_square_params()\
                   for _ in range(num_squares)]
  line_params = [sample_line_params()\
                 for _ in range(num_lines)]

  coord_xform = mk_coord_xform(*coord_params)

  squares = []
  lines = []
  for i in range(num_i_iter):
    for j in range(num_j_iter):
      coord_x, coord_y = coord_xform(i,j)
      for s_params in square_params:
        square = mk_sq_from_coord(coord_x, coord_y, *s_params)
        squares.append(square)
      for l_params in line_params:
        line = mk_line_from_coord(coord_x, coord_y, i, j, *l_params)
        lines.append(line)

  return squares, lines

def sample_scene():
  squares, lines = _sample_scene()
  while not square_no_overlap(squares):
    squares, lines = _sample_scene()

  return render(squares + lines)
  

if __name__ == "__main__":

  from draw import *
  import time
  def hand_example():
    num_i_iter = 4
    num_j_iter = 4
    coord_params = [25, 4, 10, 0, 25, 10]
    square_params = []
    square_params = [[0,0,5], [5,12,3], [-8,12,2]]
    line_params = [[0,0,5,12,False,False],
                   [0,0,-8,12,False,False],
                   [0,0,-20,0,True,False],
                   [-8,12,-23,-15,True,True]
                  ]

    coord_xform = mk_coord_xform(*coord_params)

    squares = []
    lines = []
    for i in range(num_i_iter):
      for j in range(num_j_iter):
        coord_x, coord_y = coord_xform(i,j)
        for s_params in square_params:
          square = mk_sq_from_coord(coord_x, coord_y, *s_params)
          squares.append(square)
        for l_params in line_params:
          line = mk_line_from_coord(coord_x, coord_y, i, j, *l_params)
          lines.append(line)

    return squares, lines

  squares, lines = hand_example()
  rendered = render(squares + lines)
  draw_orig(rendered, "./drawings/test_canvas_hand.png")

  for i in range(1000):
    scene = sample_scene()
    draw_orig(scene, "./drawings/test_canvas.png")
    time.sleep(2)
    print "HOHO"

