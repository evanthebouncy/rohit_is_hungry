import random
import re
from automata import Automata


POSSIBLE_PARAMS = ['', '1', '0', '01', '10', '11', '00', '1111','0110', '011', '111', '010','000']

# POSSIBLE_PARAMS = ['', '11011','0110', '0101', '111', '0010','000', '01101']

param_space = [
  ['01', '11', '000'],
  ['110', '101', '1111'],
  ['0100', '10', '1000'],
  ['011', '1110', '1010'],
  ['10101', '', '1001'],
  ['1', '11011', '0001'],
]


def unit_gen(i):
  for x in param_space[i]:
    yield x
    # for i in POSSIBLE_PARAMS:
    #     for i2 in POSSIBLE_PARAMS:
    #         for i3 in POSSIBLE_PARAMS:
    #             yield i+i2+i3



def get_param(i):
  '''Returns a random character from characters'''
  return random.choice(param_space[i])


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
  params = []
  for i in xrange(6):
    s = [get_param(i) for _ in xrange(1)]
    params.append(s)
  return params


def generate_positive_example(params):
  '''Creates an example that follows the regex

  Args:
    params: list of 6 string parameters
  Returns:
    string example that follows the regex
  '''
  s = ''

  intro = params[0]
  # s += ''.join(intro) * random.randint(0, 3)

  verse = params[1]
  chorus = params[2]
  outro = params[3]
  outro2 = params[4]
  outro3 = params[5]

  for i in xrange(random.randint(0, 3)):
    s = ''
    for p in params:
      s += ''.join(p)*random.randint(1,3) if random.random() < 0.50 else ''
    # first_star = random.randint(0, 3)
    # second_star = random.randint(0, 3)
    # s1 = ''.join(verse)*first_star
    # s2 = ''.join(chorus)*second_star
    # s+= s1+s2

  # outro = params[3]
  # s += ''.join(outro) * random.randint(0, 3)
  return s


def generate_negative_example(params, p1=0.5, p2=0.5, p3=0.5, rec_depth=0):
  if rec_depth > 10:
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
        new_params[i] = get_param(i)
    example = generate_positive_example(new_params)

  if check_example(params, example):
    return generate_negative_example(params, p1=p1, p2=p2, p3=p3, rec_depth=rec_depth+1)
  else:
    return example


if __name__ == '__main__':
  # TEST!
  for i in xrange(10):
      params = generate_params()
      print params
      # print '((?:(?:{}{}{})+?(?:{}{}{})*)*)'.format(*params)
      pos = [generate_positive_example(params) for i in xrange(50)]
      print 'got pos'
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
  for i in range(1000):
    params = generate_params()
    e = generate_negative_example(params)
    now = time.time()
    if now-start > 0.001 and e is not None:
        print i, now-start, params, e
    start = now
