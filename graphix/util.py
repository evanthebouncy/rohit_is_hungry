import sys

def same_line_print(message):
  sys.stdout.write("\r" + message)
  sys.stdout.flush()

