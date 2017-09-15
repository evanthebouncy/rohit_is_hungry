# ROHIT IS GOD!!!

from z3 import Solver, Int, Bool, Or, And, If, Not, sat, is_true, is_false


def rect(x,y,w,h,i,j):
    return And(And(x <= i, i < (x + w)),And(y <= j, j < (y + h)))
    
def getAreaCount(ships):
    ac = 0
    for (w,h) in ships:
        ac += w*h
    return ac

def findConfig(ships, observations, dimensions=(10,10)):
    (M,N) = dimensions
    NS = len(ships)
    s = Solver()
    W = map(lambda (w,h): w, ships)
    H = map(lambda (w,h): h, ships)
    (xs,ys,ds) = ([],[],[])
    for k in range(NS):
        xs.append(Int('x_%d' % k))
        ys.append(Int('y_%d' % k))
        ds.append(Bool('d_%d' % k))
        #assert that x,y are in the dimensions' range
        s.add(xs[k] < M, xs[k] >= 0, ys[k] < N, ys[k] >=0)
        
    occupied = dict()
    observe = dict()
        
    for i in range(M):
        occupied[i] = dict()
        observe[i] = dict()
        for j in range(N):
            occupied[i][j] = dict()
            observe[i][j] = False
            for k in range(NS):
                rect1 = rect(xs[k],ys[k],W[k],H[k],i,j)
                rect2 = rect(xs[k],ys[k],H[k],W[k],i,j)
                occupied[i][j][k] = Or(And(ds[k], rect1),And(Not(ds[k]), rect2))
                observe[i][j] = Or(occupied[i][j][k],observe[i][j])
    sumvar = 0
    for ((i,j),hit) in observations:
        if hit:
            s.add(observe[i][j])
        else:
            s.add(Not(observe[i][j]))
            
    for i in range(M):
        for j in range(N):   
            sumvar = If(observe[i][j],1,0) + sumvar 
    
    s.add(sumvar == getAreaCount(ships))
    if s.check() == sat:
        model = s.model()
        output = []
        for k in range(NS):
            output.append((model[xs[k]].as_long(),model[ys[k]].as_long(),is_true(model[ds[k]])))
        return output
    else:
        #print "UNSAT!"
        return "UNSAT"


def create_solver(ships, observations, dimensions=(10,10)):
    (M,N) = dimensions
    NS = len(ships)
    s = Solver()
    W = map(lambda (w,h): w, ships)
    H = map(lambda (w,h): h, ships)
    (xs,ys,ds) = ([],[],[])
    for k in range(NS):
        xs.append(Int('x_%d' % k))
        ys.append(Int('y_%d' % k))
        ds.append(Bool('d_%d' % k))
        #assert that x,y are in the dimensions' range
        s.add(xs[k] < M, xs[k] >= 0, ys[k] < N, ys[k] >=0)
        
    occupied = dict()
    observe = dict()
        
    for i in range(M):
        occupied[i] = dict()
        observe[i] = dict()
        for j in range(N):
            occupied[i][j] = dict()
            observe[i][j] = False
            for k in range(NS):
                rect1 = rect(xs[k],ys[k],W[k],H[k],i,j)
                rect2 = rect(xs[k],ys[k],H[k],W[k],i,j)
                occupied[i][j][k] = Or(And(ds[k], rect1),And(Not(ds[k]), rect2))
                observe[i][j] = Or(occupied[i][j][k],observe[i][j])
    sumvar = 0
    for ((i,j),hit) in observations:
        if hit:
            s.add(observe[i][j])
        else:
            s.add(Not(observe[i][j]))
            
    for i in range(M):
        for j in range(N):   
            sumvar = If(observe[i][j],1,0) + sumvar 
    
    s.add(sumvar == getAreaCount(ships))
    return s, occupied, observe

def is_amb(query_location, ships, observations, dimensions=(10,10)):
  print "ROHIT PLEASE EAT THESE OBSERVATIONS "
  print observations
  x,y = query_location
  pretend_true = observations + [((x,y),True)]
  pretend_false = observations + [((x,y),False)]
  config_true = findConfig(ships, pretend_true, dimensions)
  config_false = findConfig(ships, pretend_false, dimensions)
  print "is amb under ", query_location
  print config_true
  print config_false
  assert not (config_true == "UNSAT" and config_false == "UNSAT")
  ret = not(config_true == "UNSAT" or config_false == "UNSAT")
  print "ambivalence ", ret
  return ret
  

def get_good_observations(ships, observations, dimensions=(10,10)):
    """
    Returns a list of observations that will yield new info
    """
    (M,N) = dimensions
    solver, occupied, observe = create_solver(ships, observations, dimensions)
    possible_obs = set([(i,j) for i in xrange(M) for j in xrange(N)])
    observations = [a for (a, b) in observations]
    possible_obs = list(possible_obs.difference(observations))
    good_obs = []
    implicit = []

    print observations

    assert len(possible_obs) + len(observations) == M*N

    # now need to check each observation
    for (i,j) in possible_obs:
        solver.push()
        solver.add(observe[i][j])
        hit_possible = solver.check()
        solver.pop()
        solver.push()
        solver.add(Not(observe[i][j]))
        miss_possible = solver.check()
        solver.pop()

        if hit_possible == sat and miss_possible == sat:
            good_obs.append((i,j))
        # TODO maybe say what the implicit observation is?
        elif hit_possible != sat and miss_possible != sat:
            print hit_possible, miss_possible
            print "something is wrong", i, j

        elif hit_possible == sat:
            print i,j, "is a hit"

    return good_obs
















def test1(): #sat
    ships = [(2,4), (1,5), (1,3), (1,3), (1,3)]
    observations = [((3, 2), False), ((8, 6), False), ((2, 8), False), ((0, 7), False), ((2, 2), True), ((5, 6), True), ((1, 7), True), ((9, 1), False), ((5, 2), False), ((2, 0), True), ((2, 4), True), ((6, 4), False), ((4, 3), False), ((0, 8), False), ((6, 0), False), ((3, 8), False), ((8, 4), False), ((3, 3), False), ((5, 0), False), ((5, 5), False), ((8, 2), False), ((8, 7), False), ((9, 7), True), ((9, 3), False), ((5, 4), False), ((4, 5), False), ((3, 1), False), ((4, 7), True), ((8, 8), False), ((4, 9), False), ((3, 5), False), ((9, 8), True), ((6, 6), True), ((7, 9), False), ((6, 5), False), ((6, 9), False), ((2, 3), True), ((0, 6), False), ((4, 8), False), ((9, 0), False), ((2, 9), False), ((8, 5), False), ((7, 3), False), ((7, 2), False), ((2, 6), True), ((8, 1), False), ((9, 4), False), ((6, 7), True), ((0, 2), False), ((2, 7), False), ((7, 4), False), ((0, 0), False), ((7, 8), False), ((7, 7), False), ((1, 0), False), ((1, 6), True), ((3, 7), True), ((6, 8), False), ((1, 3), False), ((4, 0), True), ((4, 1), False), ((6, 2), False), ((0, 1), False), ((9, 2), False), ((7, 6), False), ((0, 3), False), ((6, 1), False), ((4, 4), False), ((5, 7), True), ((7, 5), False), ((3, 6), True), ((5, 1), False), ((4, 2), False), ((1, 5), True), ((6, 3), False), ((1, 9), False), ((3, 4), False), ((1, 2), False), ((0, 4), False), ((9, 9), True), ((3, 9), False), ((4, 6), True), ((1, 1), False), ((5, 3), False), ((1, 4), False), ((1, 8), False), ((9, 5), False), ((0, 9), False), ((8, 9), False), ((0, 5), False), ((8, 3), False), ((5, 8), False), ((3, 0), True), ((7, 0), False), ((8, 0), False), ((5, 9), False), ((9, 6), False), ((2, 5), True), ((7, 1), False), ((2, 1), False)]
    print "ship sizes:",ships
    config = findConfig(ships,observations)
    print "ship placements:",config

def test2(): #unsat
    ships = [(2,4), (1,5), (1,3), (1,3), (1,3)]
    observations = [((3, 2), False), ((8, 6), False), ((2, 8), False), ((0, 7), False), ((2, 2), True), ((5, 6), True), ((1, 7), True), ((9, 1), False), ((5, 2), False), ((2, 0), True), ((2, 4), True), ((6, 4), False), ((4, 3), False), ((0, 8), False), ((6, 0), False), ((3, 8), False), ((8, 4), False), ((3, 3), False), ((5, 0), False), ((5, 5), False), ((8, 2), False), ((8, 7), False), ((9, 7), True), ((9, 3), False), ((5, 4), False), ((4, 5), False), ((3, 1), False), ((4, 7), True), ((8, 8), False), ((4, 9), False), ((3, 5), False), ((9, 8), True), ((6, 6), True), ((7, 9), False), ((6, 5), False), ((6, 9), False), ((2, 3), True), ((0, 6), False), ((4, 8), False), ((9, 0), False), ((2, 9), False), ((8, 5), False), ((7, 3), False), ((7, 2), False), ((2, 6), True), ((8, 1), False), ((9, 4), False), ((6, 7), True), ((0, 2), False), ((2, 7), False), ((7, 4), False), ((0, 0), False), ((7, 8), False), ((7, 7), False), ((1, 0), False), ((1, 6), True), ((3, 7), True), ((6, 8), False), ((1, 3), False), ((4, 0), True), ((4, 1), False), ((6, 2), False), ((0, 1), False), ((9, 2), False), ((7, 6), False), ((0, 3), False), ((6, 1), False), ((4, 4), False), ((5, 7), True), ((7, 5), False), ((3, 6), True), ((5, 1), False), ((4, 2), False), ((1, 5), True), ((6, 3), False), ((1, 9), False), ((3, 4), False), ((1, 2), False), ((0, 4), False), ((9, 9), True), ((3, 9), False), ((4, 6), True), ((1, 1), False), ((5, 3), False), ((1, 4), False), ((1, 8), False), ((9, 5), False), ((0, 9), False), ((8, 9), False), ((0, 5), False), ((8, 3), False), ((5, 8), False), ((3, 0), False), ((7, 0), False), ((8, 0), False), ((5, 9), False), ((9, 6), False), ((2, 5), True), ((7, 1), False), ((2, 1), False)]
    print "ship sizes:",ships
    config = findConfig(ships,observations)
    print "ship placements:",config
    
def test3(): #sat
    ships = [(2,4), (1,5), (1,3), (1,3), (1,3)]
    observations = [((3, 2), False), ((8, 6), False), ((2, 8), False), ((0, 7), False), ((2, 2), True), ((5, 6), True), ((1, 7), True), ((9, 1), False), ((5, 2), False), ((2, 0), True), ((2, 4), True), ((6, 4), False), ((4, 3), False), ((0, 8), False), ((6, 0), False), ((3, 8), False), ((8, 4), False), ((3, 3), False), ((5, 0), False), ((5, 5), False), ((8, 2), False), ((8, 7), False), ((9, 7), True), ((9, 3), False), ((5, 4), False), ((4, 5), False), ((3, 1), False), ((4, 7), True), ((8, 8), False), ((4, 9), False), ((3, 5), False), ((9, 8), True), ((6, 6), True), ((7, 9), False), ((6, 5), False), ((6, 9), False), ((2, 3), True), ((0, 6), False), ((4, 8), False), ((9, 0), False), ((2, 9), False), ((8, 5), False), ((7, 3), False), ((7, 2), False), ((2, 6), True), ((8, 1), False), ((9, 4), False), ((6, 7), True), ((0, 2), False), ((2, 7), False), ((7, 4), False), ((0, 0), False), ((7, 8), False), ((7, 7), False)]
    print "ship sizes:",ships
    config = findConfig(ships,observations)
    print "ship placements:",config
    
def test4(): #sat
    ships = [(2,4), (1,5), (1,3), (1,3), (1,3)]
    observations = [ ((6, 9), False), ((2, 3), True), ((0, 6), False), ((4, 8), False), ((9, 0), False), ((2, 9), False), ((8, 5), False), ((7, 3), False), ((7, 2), False), ((2, 6), True), ((8, 1), False), ((9, 4), False), ((6, 7), True), ((0, 2), False), ((2, 7), False), ((7, 4), False), ((0, 0), False), ((7, 8), False), ((7, 7), False)]
    print "ship sizes:",ships
    config = findConfig(ships,observations)
    print "ship placements:",config
    
    
if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
