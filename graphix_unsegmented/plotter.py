import numpy as np
import matplotlib.pyplot as plt

# time_full:  20.3801050186 8.56738305092 1024
# time_rand:  4.11032700539 8.76360487938 204 0.01171875
# time_nn:  2.42858314514 4.01715779305 120 1.72694206238
# time_cegis:  2.3168554306 19.5129356384 110
# time_rcegis:  1.16638946533 136.078774691 56
# time_acegis:  1.79295325279 47.3505141735 85
# time_rand_cegis:  4.25371098518 42.6225004196 211
# time_nn_cegis:


categories = ['time_full', 'time_rand', 'time_nn', 'time_cegis', 'time_rcegis', 'time_acegis', 'time_rand_cegis', 'time_nn_cegis']
cat_trimmed = ['time_full', 'time_cegis', 'time_rcegis', 'time_acegis', 'time_rand_cegis', 'time_nn_cegis']
labels = [cat[5:] for cat in categories]
labels_trimmed = [cat[5:] for cat in cat_trimmed]
# labels[3] = 'rand+cegis'
labels[-1] = 'ours'
labels_trimmed[-2] = 'rand+cegis'
labels_trimmed[-1] = 'ours'


def load_results(fname):
    '''Gives data in the format {'cat': [(time, num_constraints)...]}
    '''
    fname = fname or '_results'
    with open(fname) as f:
        relevant = False
        trials = []
        run = []
        for line in f:
            if not relevant and line[0] != '=':
                continue
            elif line[0] == '=':
                relevant = True

            if line[0] == '=':
                trials.append(run)
                run = {}
            else:
                try:
                    line = line.strip().split()
                    run[line[0][:-1]] = map(float, line[1:])
                except:
                    relevant = False

        trials = trials[1:]
        return compile_cats(trials)

def compile_cats(trials):
    data = {cat: [] for cat in categories}

    for trial in trials:
        for cat in categories:
            nums = trial[cat]
            time_taken = nums[0:2]
            num_constraints = [nums[2]]
            if cat in ['time_nn', 'time_rand']:
                time_taken += [nums[3]]
            elif cat  == 'time_nn_cegis':
                time_taken += nums[3:5]
                num_constraints += [nums[5]]
            data[cat].append((time_taken, num_constraints))
    return data

def make_time_boxplots(results):
    data = []
    for cat in cat_trimmed:
        points = [sum(x[0]) for x in results[cat]]
        print cat[5:] + " avg:", 1.*sum(points)/len(points)
        data.append(points)

    fig, ax = plt.subplots()
    box = plt.boxplot(data[::-1], 0, '', vert=False)
    xtop = 40
    ax.set_xlim(0, xtop)

    medians = [item.get_xdata() for i, item in enumerate(box['medians'])]

    whiskers = [item.get_xdata()[0] for i, item in enumerate(box['whiskers']) if i % 2 == 1]
    caps = [item.get_xdata()[0] for i, item in enumerate(box['caps']) if i % 2 == 1]
    # print len(whiskers, caps)
    vals = zip(whiskers, caps)

    # write overflow labels
    for i,(whisker, cap) in zip(range(len(labels_trimmed)),vals):
        if whisker > xtop:
            ax.annotate('{}, {}'.format(int(whisker), int(cap)), xy=(xtop, i+0.9))
        elif cap > xtop:
            ax.annotate(str(int(cap)), xy=(xtop, i+1.1))

    ax.set_yticklabels(labels_trimmed[::-1])
    plt.title('Distribution of Time to Complete Synthesis')
    plt.xlabel('time (s)')
    plt.show()


def stacked_avg_times(results):
    build_times = []
    solve_times = []
    nn_times = []
    # nn_times2 = []
    for cat in cat_trimmed:
        bt = [x[0][0] for x in results[cat]]
        build_times.append(1.*sum(bt)/len(bt))
        st = [x[0][1] for x in results[cat]]
        solve_times.append(1.*sum(st)/len(st))
        if 'nn' in cat:
            nnt = [x[0][2] for x in results[cat]]
            nn_times.append(1.*sum(nnt)/len(nnt))
        else:
            nn_times.append(0)
        # if 'nn_cegis' in cat:
        #     nnt = [x[0][3] for x in results[cat]]
        #     nn_times2.append(1.*sum(nnt)/len(nnt))
        # else:
        #     nn_times2.append(0)

    build_times = np.array(build_times)
    solve_times = np.array(solve_times)
    nn_times = np.array(nn_times)
    total = build_times+solve_times+nn_times
    # nn_times2 = np.array(nn_times2)
    ind = np.arange(len(labels_trimmed))
    fig, ax = plt.subplots()

    # p0 = plt.bar(ind, nn_times2, color='red')
    p1 = plt.bar(ind, nn_times, color='#000000')
    p2 = plt.bar(ind, build_times, color='#bfbfbf', bottom=nn_times, hatch='//')
    p3 = plt.bar(ind, solve_times, color='#a6a6a6', bottom=build_times+nn_times)#, hatch='//')
    plt.legend((p1[0], p2[0], p3[0]), ('NN Phase', 'Build Phase', 'Solve Phase'))
    ytop = 40
    ax.set_ylim(0, ytop)

    for i,j in zip(range(len(labels_trimmed)),total):
        if j > ytop:
            ax.annotate(str(round(j, 1)),xy=(i-.3, ytop-2))
            # offset += 1.5


    plt.title('Average Time to Complete Synthesis')
    plt.ylabel('time (s)')
    plt.xticks(ind, labels_trimmed)
    plt.show()



def sizes_plots(results):
    sizes = []
    sizes2 = []
    for cat in categories:
        bt = [x[1] for x in results[cat]]
        bt1 = [x[0] for x in bt]

        if len(bt[0]) > 1:
            bt2 = bt1
            avg = 1.*sum(bt2)/len(bt2)
            bt1 = [avg-x[1] for x in bt]
        else:
            bt2 = [0 for x in bt]
        sizes.append(1.*sum(bt1)/len(bt1))
        sizes2.append(1.*sum(bt2)/len(bt2))

    l2 = ['cegis', 'rcegis', 'acegis', 'rand+cegis', 'ours']
    ind = np.arange(len(l2))
    fig, ax = plt.subplots()

    # sizes[2] = 141.7910447761194
    # sizes[5] = 143.24875621890547

    s1 = np.array([0, 0, 0, sizes[1], sizes2[-1]])
    s2 = np.array([sizes[3], sizes[4], sizes[5], sizes[6]-sizes[1], sizes[-1]])


    p1 = plt.bar(ind, s1, color='#e2e2e2')
    p2 = plt.bar(ind, s2, color='#999999', bottom=s1, hatch='//')
    # p1 = plt.bar(ind, sizes, color='#d62728')
    # p2 = plt.bar(ind, build_times, color='#1a93ef', bottom=nn_times)
    # p3 = plt.bar(ind, solve_times, color='#11e075', bottom=build_times+nn_times)
    plt.legend((p1[0], p2[0]), ('Initial Examples', 'CEGIS Examples'))
    plt.title('Average Number of Examples Used')
    plt.ylabel('number of examples')
    plt.xticks(ind, l2)
    # print build_times
    # print solve_times
    # print nn_times
    # print labels
    plt.show()



if __name__ == '__main__':
    results = load_results('REAL_RESULTS')
    make_time_boxplots(results)
    stacked_avg_times(results)
    sizes_plots(results)
