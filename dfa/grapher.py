import re
import numpy as np
import matplotlib.pyplot as plt

fname = 'exp1'

def extract_data(fname):
    matcher = re.compile('(.*) got .* in \((.*) build, (.*) solve\): (.*) total time. Was Solved: (.*). Used (.*) examples.')

    results = {}

    with open('exps/' + fname) as f:
        for line in f:
            result = matcher.match(line)
            if not result:
                continue
            name = result.group(1)
            if name not in results:
                results[name] = {'build': [], 'solve': [], 'total': [], 'is_correct': [], 'num_examples': []}
            d = results[name]
            d['build'].append(float(result.group(2)))
            d['solve'].append(float(result.group(3)))
            d['total'].append(float(result.group(4)))
            d['is_correct'].append(True if result.group(5) == 'True' else False)
            d['num_examples'].append(int(result.group(6)))

    # TODO filter step maybe?

    return results

def plot_boxes(data):
    names = data.keys()
    names2 = filter(lambda x: x not in ['AddAll', 'Add200'], data.keys())

    build_time = [data[name]['build'] for name in names2]
    plt.boxplot(build_time, labels=names2)
    plt.title('Total Build Time Taken')
    plt.show()

    solve_time = [data[name]['solve'] for name in names]
    plt.boxplot(solve_time, labels=names)
    plt.title('Total Solve Time Taken')
    plt.show()

    total_time = [data[name]['total'] for name in names]
    plt.boxplot(total_time, labels=names)
    plt.title('Total Time Taken')
    plt.show()

    num_examples = [data[name]['num_examples'] for name in names2]
    plt.boxplot(num_examples, labels=names2)
    plt.title('Number of Examples Used')
    plt.show()


def stacked_time(data):
    names = data.keys()
    ind = np.arange(len(names))
    width = 0.35

    build_time = np.array([np.mean(data[name]['build']) for name in names])
    solve_time = np.array([np.mean(data[name]['solve']) for name in names])

    p1 = plt.bar(ind, build_time, width, color='#d62728')
    p2 = plt.bar(ind, solve_time, width, bottom=build_time)
    plt.xticks(ind, names)
    plt.title('Average Total Time Taken')
    plt.legend((p1[0], p2[0]), ('Build', 'Solve'))
    plt.show()


def bar_examples(data):
    names = filter(lambda x: x != 'AddAll', data.keys())
    ind = np.arange(len(names))
    width = 0.35

    num_examples = np.array([np.mean(data[name]['num_examples']) for name in names])

    p1 = plt.bar(ind, num_examples, width)
    plt.xticks(ind, names)
    plt.title('Average Number of Examples')
    plt.show()

def percent_correct(data):
    names = data.keys()
    ind = np.arange(len(names))
    width = 0.35

    num_examples = np.array([1.*np.sum(data[name]['is_correct']) for name in names])
    num_examples /= len(data['AddAll']['num_examples'])

    p1 = plt.bar(ind, num_examples, width)
    plt.xticks(ind, names)
    plt.title('Percentage of Correct Examples')
    plt.show()
            
if __name__ == '__main__':
    data = extract_data('exp9')
    plot_boxes(data)
    stacked_time(data)
    bar_examples(data)
    percent_correct(data)


