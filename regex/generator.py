import random
import re
from automata import Automata


POSSIBLE_PARAMS = ['', '1', '0', '01', '10', '11', '00']


def get_param():
  '''Returns a random character from characters'''
  return random.choice(POSSIBLE_PARAMS)


def check_example(params, example):
  '''Checks if an example is parameterized by these params
  Args:
    params: list of 6 parameters
    example: string to check
  Return:
    True if a match is found and it completely captures the example
  '''
  # for i in xrange(1, 4):
  #   if len(example) % i == 0:
  #     # chunk = example[0:len(example)/i]
  #     for j in xrange(0, i):
  #       chunk = example[j*len(example)/i:(j+1)*len(example)/i]
  #       if not check_subregex(params, chunk):
  #         break
  #     else:
  #       # goes here if the loop finishes completely without breaks
  #       return True
  # return False
  a = Automata(params)
  return a.test_string(example)


def generate_params():
  '''Gives you the parameters of a regex

  Returns:
    list of 6 parameters
  '''
  return [get_param() for _ in xrange(6)]

def check_same_params(p1, p2):
  pieces1 = (''.join(p1[:3]), ''.join(p1[3:]))
  pieces2 = (''.join(p2[:3]), ''.join(p2[3:]))
  return pieces1 == pieces2 or pieces1 == (pieces2[1], pieces2[0])



def generate_positive_example(params):
  '''Creates an example that follows the regex

  Args:
    params: list of 6 string parameters
  Returns:
    string example that follows the regex
  '''
  outer_star = random.randint(1, 3)

  s = ''
  for i in xrange(outer_star):
    first_star = random.randint(0, 3)
    second_star = random.randint(0, 3)
    s1 = ''.join(params[:3])*first_star
    s2 = ''.join(params[3:])*second_star
    s += s1+s2

  return s


def generate_negative_example(params, p1=0.5, p2=0.5, p3=0.5, rec_depth=0):
  if rec_depth > 100:
    return None
  '''Creates an example that does not follow the regex

  Args:
    params: list of 6 string parameters
    p1: probability of using the deletion method
    p2: probability of flipping each character in deletion
    p3: probability of switching a character in the params
  Return:
    string example that does not follow the params
  '''
  def flip(char):
    return random.choice([x for x in POSSIBLE_PARAMS if x != char])
    
  if random.random() < p1:
    example = list(generate_positive_example(params))
    for i in xrange(len(example)):
      if random.random() < p2:
        example[i] = flip(example[i])
    example = reduce(lambda x,y:x+y, example, '')
  else:
    new_params = [] + params
    for i in xrange(len(new_params)):
      if random.random() < p3:
        new_params[i] = get_param()
    example = generate_positive_example(new_params)

  if check_example(params, example):
    return generate_negative_example(params, p1=p1, p2=p2, p3=p3, rec_depth=rec_depth+1)
  else:
    return example


if __name__ == '__main__':
  # TEST!
  for i in xrange(1000):
      params = generate_params()
      print params
      print '((?:(?:{}{}{})+?(?:{}{}{})*)*)'.format(*params)
      pos = [generate_positive_example(params) for i in xrange(50)]
      neg = [generate_negative_example(params) for i in xrange(50)]

      # print "pos ", pos
      # print "neg ", neg

      print 'Testing positive...'
      correct_pos = True
      for p in pos:
        correct_pos &= check_example(params, p)
        if not check_example(params, p):
            print params, p
      if not correct_pos:
        print 'something is wrong with positive examples'

      print 'Testing negative...'
      correct_neg = True
      for n in neg:
        correct_neg &= not check_example(params, n)
      if not correct_neg:
        print 'something is wrong with negative examples'

      if correct_pos and correct_neg:
        print 'Passed!'
      else:
        raise Exception("Something is still wrong! :(")
  import time
  start = time.time()
  # can get stuck sometimes, for instance re.match('(^((00)*(10011)*)*$)', '000000000000000000000000000000000000000000000000000000000000000')
  for i in range(100000):
    params = generate_params()
    e = generate_negative_example(params)
    now = time.time()
    if now-start > 0.001 and e is not None:
        print i, now-start, params, e
    start = now
