import random
import re


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
	regex = '(^(({}{}{})*({}{}{})*)*$)'.format(*params)
	matcher = re.match(regex, example)
	if matcher is None:
		return False
	else:
		# first matched group is the biggest
		return matcher.groups()[0] == example


def generate_params():
	'''Gives you the parameters of a regex

	Returns:
		list of 6 parameters
	'''
	return [get_param() for _ in xrange(6)]


def generate_positive_example(params):
	'''Creates an example that follows the regex

	Args:
		params: list of 6 string parameters
	Returns:
		string example that follows the regex
	'''
	first_star = random.randint(0, 3)
	second_star = random.randint(0, 3)
	outer_star = random.randint(1, 3)

	s1 = ''.join(params[:3])*first_star
	s2 = ''.join(params[3:])*second_star
	return str((s1+s2)*outer_star)


def generate_negative_example(params, p1=1, p2=0.1, p3=0.1):
	'''Creates an example that does not follow the regex

	Args:
		params: list of 6 string parameters
		p1: probability of using the deletion method
		p2: probability of flipping each character in deletion
		p3: probability of switching a character in the params
	Return:
		string example that does not follow the params
	'''
	if random.random() < p1:
		example = list(generate_positive_example(params))
		for i in xrange(len(example)):
			if random.random() < p2:
				example[i] = '1' if example[i] == '0' else '0'
		example = str(example)
	else:
		new_params = [] + params
		for i in xrange(len(new_params)):
			if random.random() < p3:
				new_params[i] = get_param()
		example = generate_positive_example(new_params)
	if check_example(params, example):
		return generate_negative_example(params, p1=p1, p2=p2, p3=p3)
	else:
		return example


if __name__ == '__main__':
	# TEST!
	params = generate_params()
	print params
	print '((({}{}{})*({}{}{})*)*)'.format(*params)
	pos = [generate_positive_example(params) for i in xrange(50)]
	neg = [generate_negative_example(params) for i in xrange(50)]

	print 'Testing positive...'
	correct_pos = True
	for p in pos:
		correct_pos &= check_example(params, p)
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
