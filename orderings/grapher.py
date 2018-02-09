import pickle
import matplotlib.pyplot as plt
import numpy as np


def graph_stuff(TEST_LOC='results.p'):
    data = pickle.load( open( TEST_LOC, "rb" ) )
    
    names = []
    num_examples = {}
    is_rep = {}
    p_rep = {}

    for i, trial in enumerate(data):
        for name, stats in trial.iteritems():
            if i == 0:
                names.append(name)
                num_examples[name] = [stats['num_examples']]
                is_rep[name] = [stats['is_rep']]
                p_rep[name] = [stats['p_rep']]
            else:
                num_examples[name].append(stats['num_examples'])
                is_rep[name].append(stats['is_rep'])
                p_rep[name].append(stats['p_rep'])

    names2 = names
    names = []
    for name in names2:
        if name == 'nn':
            pass
        else:
            names.append(name)
    names.append('nn')

    ind = np.arange(len(names))
    num_examples = [num_examples[name] for name in names]
    is_rep = [1.0*sum(is_rep[name])/len(num_examples[0]) for name in names]
    p_rep = [np.mean(p_rep[name]) for name in names]

    avg_sizes = [np.mean(nums) for nums in num_examples]

    names[-1] = 'ours'

    width = 0.35
    figsize = (4,3)
    plt.figure(figsize=figsize)
    plt.barh(ind, avg_sizes, width, color='#bfbfbf')
    plt.yticks(ind, names)
    plt.tight_layout()
    # plt.title('Average Percentage of Examples Used')
    plt.show()

    plt.figure(figsize=figsize)
    plt.xlim(xmax=1.0)
    plt.barh(ind, is_rep, width, color='#bfbfbf')
    plt.yticks(ind, names)
    plt.tight_layout()
    # plt.title('Percent Is Completely Representative')
    plt.show()


if __name__ == '__main__':
    graph_stuff()
