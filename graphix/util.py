import sys

def same_line_print(message):
  sys.stdout.write("\r" + message)
  sys.stdout.flush()

def img_2_constraints(img):
  M,N = img.shape
  ret = []
  for y in range(M):
    for x in range(N):
      val = True if img[y][x] else False
      ret.append(((x,y),val))
  return ret
