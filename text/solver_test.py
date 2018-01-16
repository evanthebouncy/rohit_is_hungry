from solver import solve
from gen import *


def gen_random():
    x = get_message(L)
    xform = sample_transform(1)
    # print xform
    # print
    xform[0] = (xform[0][0], (0,0))
    y = apply_transform(x, xform)
    print x
    print xform
    print y
    s, t = solve(x, y)
    xform_synth = [((s, t), (0, 0))]
    print xform_synth
    synthesized = apply_transform(x, xform_synth)



if __name__ == '__main__':
    gen_random()

