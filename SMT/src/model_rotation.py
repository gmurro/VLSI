from z3 import *
import numpy as np
from itertools import combinations
import time
import model as md


def solve_instance(w, n, x, y, l_max, mag_w):

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y))

    # area of each circuit
    area = [x[i] * y[i] for i in range(n)]

    # definition of the variables

    # coordinates of the points
    p_x = [Int("p_x_%s" % str(i+1)) for i in range(n)]
    p_y = [Int("p_y_%s" % str(i+1)) for i in range(n)]

    # rotation array
    rotation = [Bool("rot_%s" % str(i+1)) for i in range(n)]

    # real dimensions of points considering rotation
    x_r = [Int("x_r_%s" % str(i+1)) for i in range(n)]
    y_r = [Int("y_r_%s" % str(i+1)) for i in range(n)]

    # maximum height to minimize
    length = Int("length")

    # domain bounds
    domain_x = [And(p_x[i] >= 0, p_x[i] <= w-min(x)) for i in range(n)]
    domain_y = [And(p_y[i] >= 0, p_y[i] <= l_max-min(y)) for i in range(n)]

    # lengths bound
    width_bound = [And(x_r[i] >= 1, x_r[i] <= w) for i in range(n)]
    heigth_bound = [And(y_r[i] >= 1, y_r[i] <= l_max) for i in range(n)]

    # relationship between rotation and dimensions
    rotation_rel = [If(rotation[i], And(x_r[i] == y[i], y_r[i] == x[i]), And(x_r[i] == x[i], y_r[i] == y[i]))
                    for i in range(n)]

    # different coordinates
    all_different = [Distinct([mag_w * p_x[i] + p_y[i]]) for i in range(n)]

    # value of l
    objective = [length == md.z3_max([p_y[i] + y[i] for i in range(n)])]

    # cumulative constraints
    cumulative_y = md.z3_cumulative(p_y, y, x, w)
    cumulative_x = md.z3_cumulative(p_x, x, y, l_max)

    # maximum width
    max_w = [md.z3_max([p_x[i] + x[i] for i in range(n)]) <= w]

    # maximum height
    max_h = [md.z3_max([p_y[i] + y[i] for i in range(n)]) <= l_max]

    # relationship avoiding overlapping
    '''overlapping = [Or(p_x[i] + x[i] <= p_x[j],
                              p_x[j] + x[j] <= p_x[i],
                              p_y[i] + y[i] <= p_y[j],
                              p_y[j] + y[j] <= p_y[i]) for j in range(n) for i in range(j)]'''
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

    # circuits must be pushed on the left
    left = [sum([If(p_x[i] <= w // 2, area[i], 0) for i in range(n)])
            > sum([If(p_x[i] > w // 2, area[i], 0) for i in range(n)])]

    # setting the optimizer
    opt = Optimize()
    opt.add(domain_x + domain_y + overlapping + all_different + objective + cumulative_x +
            cumulative_y + max_w + max_h + symmetry + left + width_bound + heigth_bound + rotation_rel)
    opt.minimize(length)

    # maximum time of execution
    time = 300000
    opt.set(timeout=time)

    p_x_sol = []
    p_y_sol = []
    rot_sol = []
    length_sol = ""
    # solving the problem
    if opt.check() == sat:
        msg = "Solved"
        model = opt.model()
        for i in range(n):
            p_x_sol.append(model.evaluate(p_x[i]).as_string())
            p_y_sol.append(model.evaluate(p_y[i]).as_string())
            rot_sol.append(str(model.evaluate(rotation[i])))
        length_sol = model.evaluate(length).as_string()
    elif opt.reason_unknown() == "timeout":
        msg = "Solver timeout"
    else:
        msg = "Unsatisfiable"
    return msg, p_x_sol, p_y_sol, length_sol


def main():
    w = 8
    n = 4
    x = [3, 3, 5, 5]
    y = [3, 5, 3, 5]
    l_max = 16
    mag_w = 10
    start_time = time.time()
    msg, p_x_sol, p_y_sol, length_sol = solve_instance(w, n, x, y, l_max, mag_w)
    end_time = time.time() - start_time
    print(end_time)


if __name__ == '__main__':
    main()