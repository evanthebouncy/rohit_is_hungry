import pickle

rand_pickle = pickle.load(open('_time_exp_rand_only.p', "rb"))
other_pickle = pickle.load(open('_time_exp_result.p', "rb"))

print len(rand_pickle)
print len(other_pickle)

ret_pick = [[] for _ in range(8)]

ret_pick[0] = other_pickle[0]
ret_pick[1] = other_pickle[1]
ret_pick[2] = other_pickle[2]
for xx in ret_pick[2]:
  xx["method"] = "rand_0.1"
ret_pick[3] = rand_pickle[0]
for xx in ret_pick[3]:
  xx["method"] = "rand_0.3"
ret_pick[4] = rand_pickle[1]
for xx in ret_pick[4]:
  xx["method"] = "rand_0.5"
ret_pick[5] = rand_pickle[2]
for xx in ret_pick[5]:
  xx["method"] = "rand_0.7"
ret_pick[6] = other_pickle[3]
for xx in ret_pick[6]:
  xx["method"] = "h1"
ret_pick[7] = other_pickle[4]
for xx in ret_pick[7]:
  xx["method"] = "ours"

print "dumping pickle "
pickle.dump( ret_pick, open( "_time_exp_final_result.p", "wb" ) )


