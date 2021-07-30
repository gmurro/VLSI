import sys
from z3 import *
from numpy import argmax
from itertools import combinations


def cumulative(start, duration, resources, total):

    decomposition = []
    for u in resources:
        decomposition.append(
            sum([If(And(start[i] <= u, u < start[i] + duration[i]), resources[i], 0)
                 for i in range(len(start))]) <= total
        )
    return decomposition


def solve_instance(w, n, x, y, l_max, mag_w):

    # index of the circuit with the highest value
    index = argmax(y)

    # definition of the variables

    # coordinates of the points
    p_x = [Int("p_x_%s" % str(i+1)) for i in range(n)]
    p_y = [Int("p_y_%s" % str(i+1)) for i in range(n)]

    # maximum height to minimize
    length = Int("length")

    # domain bounds
    domain_x = [And(p_x[i] >= 0,p_x[i] <= w-min(x)) for i in range(n)]
    domain_y = [And(p_y[i] >= 0,p_y[i] <= l_max-min(y)) for i in range(n)]

    # different coordinates
    all_different = [Distinct([mag_w * p_x[i] + p_y[i]]) for i in range(n)]

    # value of l
    objective = length == max([p_y[i] + y[i] for i in range(n)])

    # cumulative constraints
    cumulative_y = cumulative(p_y, y, x, w)
    cumulative_x = cumulative(p_x, x, y, l_max)

    # maximum width
    max_w = [max([p_x[i] + x[i] for i in range(n)]) <= w]

    # maximum height
    max_h = [max([p_y[i] + y[i] for i in range(n)]) <= l_max]

    # relationship avoiding overlapping
    overlapping = []
    for (i,j) in combinations(range(n),2):
        overlapping.append(Or(p_x[i] + x[i] <= p_x[j],
                              p_x[j] + x[j] <= p_x[i],
                              p_y[i] + y[i] <= p_y[j],
                              p_y[j] + y[j] <= p_y[i])
                           )

    # cumulative constraints

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(p_x[index] == 0, p_y[index] == 0)]

    # setting the optimizer
    opt = Optimize()
    opt.add(domain_x + domain_y + all_different + [objective] + cumulative_x +
            cumulative_y + max_w + max_h + symmetry)
    opt.minimize(length)

    # maximum time of execution
    time = 300000
    opt.set(timeout=time)

    # solving the problem
    if opt.check() == sat:
        model = opt.model()
        print(int(model.evaluate(length).as_string()))
    elif opt.reason_unknown() == "timeout":
        print("Solver timeout")
    else:
        print("Unsatisfiable")


def main():
    w = 11
    n = 7
    x = [3, 3, 3, 3, 5, 5, 8]
    y = [3, 4, 5, 6, 3, 4, 4]
    l_max = 29
    mag_w = 100

    solve_instance(w, n, x, y, l_max, mag_w)


main()



