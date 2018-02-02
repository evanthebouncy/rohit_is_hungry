import pickle
import matplotlib.pyplot as plt
import numpy as np


def graph_stuff(TEST_LOC='results.p'):
    data = pickle.load( open( TEST_LOC, "rb" ) )
    
    names = []
    num_examples = {}
    is_rep = {}

    for i, trial in enumerate(data):
        for name, stats in trial.iteritems():
            if i == 0:
                names.append(name)
                num_examples[name] = [stats['num_examples']]
                is_rep[name] = [stats['is_rep']]
            else:
                num_examples[name].append(stats['num_examples'])
                is_rep[name].append(stats['is_rep'])

    ind = np.arange(len(names))
    num_examples = [num_examples[name] for name in names]
    is_rep = [1.0*sum(is_rep[name])/len(num_examples[0]) for name in names]

    avg_sizes = [np.mean(nums) for nums in num_examples]

    width = 0.35
    plt.bar(ind, avg_sizes, width)
    plt.xticks(ind, names)
    plt.title('Average Number of Examples Used')
    plt.show()

    plt.boxplot(num_examples, labels=names)
    plt.title('Distribution of Examples Used')
    plt.show()

    plt.bar(ind, is_rep, width)
    plt.xticks(ind, names)
    plt.title('Percent Is Representative Set')
    plt.show()


if __name__ == '__main__':
    graph_stuff()
