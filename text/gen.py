############ A STRING TRANSFORMATION TASK ##############
# a text based task of string transformation
# a string is simply a list of numbers, for example, [3,4,1,2,4,5,6]
# transformation happens in 2 stages: sub-string grabbing, and character substitution 
#
# stage1: grabbing sub-strings. 
#         a grabber consists of (start, end) , both start and end are set of characters
#         for instance, let start = (1,4) and end = (5,9)
#         the grabbing executes as: start grabbing until end.
#             i.e. start grabbing when either 1 or 4 are encountered
#                  stop grabbing when either 5 or 9 are encountered
#         all in all we would've grabbed [4,1,2,4,5] from our original [3,4,1,2,4,5,6]
#
# stage2: transformation of substring by substition of 1 character with another
#         for example, 2 => 1
#         then grabbed substring [4,1,2,4,5] will become [4,1,1,4,5] by changing 2 to 1
#
# a transformation is defined as a fixed number of (grab, substitute) executed together
# to execute the transformation, all the grabs are first executed in sequence
# then, all the grabbed substrings have their characters substituted
# finally, all the substituted substrings are concatenated back together
#
# ---- an example execution ---- 
#
# executing the transformation:
#   [(((4, 1), (6, 6)), (7, 2)),  # start grabbing at 4 or 1 until 6 or 6, sub 7 with 2 
#    (((8, 4), (2, 6)), (2, 5)),  # start grabbing at 8 or 4 until 2 or 6, sub 2 with 5 
#    (((1, 5), (4, 7)), (0, 0)) ] # start grabbing at 1 or 5 until 4 or 7, sub 0 with 0
#
# on this input sequence:
# [8, 1, 5, 7, 5, 3, 6, 8, 8, 8, 7, 2, 8, 1, 1, 4, 0, 6, 4, 6]
#
# step1, grabbed substrings:
# [1, 5, 7, 5, 3, 6], [8, 8, 8, 7, 2], [1, 1, 4]
#
# step2, applying transformations 7 => 2, 2 => 5, 0 => 0 gives:
# [1, 5, 2, 5, 3, 6], [8, 8, 8, 7, 5], [1, 1, ]
# 
# step3, putting everything together gives
# [1, 5, 2, 5, 3, 6, 8, 8, 8, 7, 5, 1, 1, 4]


import random
from random import randint

N_CHAR = 10
N_SUB = 3
L = 20

def get_letter():
  return randint(0, N_CHAR-1)

def get_message(L):
  return [get_letter() for _ in range(L)]

def grab_substring(ss, start_end):
  start, end = start_end
  def find_occurance(marker):
    return [i for i in range(len(ss)) if ss[i] in marker]
  pairs = [(s,t) for s in find_occurance(start) for t in find_occurance(end) if s <= t]
  best_pair = min(pairs + [(999,999)])
  if best_pair == (999,999): return [], ss
  return ss[best_pair[0]:best_pair[1]+1], ss[best_pair[1]+1:]

def grab_substrings(ss, start_ends):
  togo, ret = ss, []
  for start_end in start_ends:
    new_substr, togo = grab_substring(togo, start_end)
    ret.append(new_substr)
  return ret 

def apply_substitution(substring, rep_with):
  r,w = rep_with
  return [s if s != r else w for s in substring]

def sample_transform(n_steps):
  ret = []
  for i in range(n_steps):
    ret.append( ( ( (randint(0, N_CHAR-1),randint(0, N_CHAR-1)), 
                    (randint(0, N_CHAR-1),randint(0, N_CHAR-1)) 
                  ),
                  (randint(0, N_CHAR-1),randint(0, N_CHAR-1))) )
  return ret 

def apply_transform(x, transform):
  start_ends = [tr[0] for tr in transform]
  replacements = [tr[1] for tr in transform]
  substrs = grab_substrings(x, start_ends)
  sub_reps = zip(substrs, replacements)
  replaced_subs = [apply_substitution(x[0],x[1]) for x in sub_reps]
  return reduce(lambda x,y:x+y, replaced_subs)

if __name__ == "__main__":
  # msg = get_message(L)
  # start_end1 = [[1,2],[3,4]]
  # start_end2 = [[5,6],[7,8]]
  # print msg, start_end1, start_end2
  # print grab_substring(msg, start_end1)

  # print grab_substrings(msg, [start_end1, start_end1, start_end2])
  #   
  # replace_with = [1,9]
  # print apply_substitution(msg, replace_with)

  xform = sample_transform(3)
  print "a transformation ", xform
  print "a message ", msg
  print "transformed message ", apply_transform(msg, xform)

