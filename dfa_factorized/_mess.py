import pickle
xxx = pickle.load( open( "_time_exp_result.p", "rb" ) )

print xxx

f_time = 0.0
r_c_time = 0.0
c_time = 0.0
nn_c_time = 0.0

nn_ces = 0.0
r_c_ces = 0.0

l = min([len(x) for x in xxx])
l = len(xxx[3])

for i in range(l):
  f_time += xxx[0][i]['build_time'] + xxx[0][i]['solve_time']
  c_time += xxx[2][i]['build_time'] + xxx[2][i]['solve_time'] + xxx[2][i]['check_time']
  r_c_time += xxx[1][i]['build_time'] + xxx[1][i]['solve_time']
  nn_c_time += xxx[3][i]['build_time'] + xxx[3][i]['solve_time'] + xxx[3][i]['check_time'] + xxx[3][i]['nn_time']

  r_c_ces += xxx[1][i]['n_examples_orig']
  nn_ces += xxx[3][i]['n_examples_orig']
  print xxx[3][i]['n_examples_orig'], " ", xxx[3][i]['solve_time'], " ", xxx[1][i]['solve_time']


print "average time "
print "full ", f_time / l
print "cegis ", c_time / l
print "rand+cegis ", r_c_time / l
print "nn+cegis ", nn_c_time / l


print "rand+cegis ces", r_c_ces / l
print "nn+cegis ces", nn_ces / l

