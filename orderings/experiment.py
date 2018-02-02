from gen import *
from solver import *
from prune import *
import pickle
import random
import tqdm

TEST_LOC = "./data/data_test.p"

def trial(sample_examples):
    stats = {}

    # do random first
    random.shuffle(sample_examples)
    random_examples = sample_examples[:int(len(sample_examples)*.2)]
    is_rep = check_representative(random_examples, sample_examples)
    stats['random'] = {'num_examples': len(random_examples), 'is_rep': is_rep}

    # hasse set
    o = OrderingGraph()
    hasse_examples = o.find_smallest_set(sample_examples)
    is_rep = check_representative(hasse_examples, sample_examples)
    stats['hasse'] = {'num_examples': len(hasse_examples), 'is_rep': is_rep}

    # cegis set
    c = OrderCEGIS()
    cegis_examples = c.solve(examples)
    is_rep = check_representative(cegis_examples, sample_examples)
    stats['cegis'] = {'num_examples': len(cegis_examples), 'is_rep': is_rep}

    return stats



def generate_data(n=500):
    to_write = []
    for i in xrange(n):
        ordering = gen_ordering()
        sample_examples = get_data(ordering)
        to_write.append(sample_examples)

    pickle.dump( to_write, open( TEST_LOC, "wb" ) )

def load_data():
    return pickle.load( open( TEST_LOC, "rb" ) )


if __name__ == '__main__':
    # generate_data()
    data = load_data()
    stats = []

    for examples in tqdm.tqdm(data):
        stats.append(trial(examples))

    pickle.dump( (stats), 
                   open( "results.p", "wb" ) )
