from z3 import *
import numpy as np
from itertools import combinations
import time
from utils.utility import compute_l_max


def read_file(input_filename):

    with open(input_filename, 'r') as f_in:

        lines = f_in.read().splitlines()

        w = lines[0]
        n = lines[1]

        x = []
        y = []

        for i in range(int(n)):
            split = lines[i + 2].split(' ')
            x.append(int(split[0]))
            y.append(int(split[1]))

        l_max = compute_l_max(x, y, int(w))

        # compute order of magnitude of w
        len_w = len(str(w))
        mag_w = 10 ** len_w

        return int(w), int(n), x, y, l_max, mag_w


def write_file(w, n, x, y, p_x_sol, p_y_sol, length, out_file, elapsed_time):

    with open(out_file, 'w+') as f_out:

        f_out.write('{} {}\n'.format(w, length))
        f_out.write('{}\n'.format(n))

        for i in range(n):
            f_out.write('{} {} {} {}\n'.format(x[i], y[i], p_x_sol[i], p_y_sol[i]))

        f_out.write('{}\n'.format(elapsed_time))


def z3_max(vector):
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)
    return maximum


def z3_cumulative(start, duration, resources, total):

    decomposition = []
    for u in resources:
        decomposition.append(
            sum([If(And(start[i] <= u, u < start[i] + duration[i]), resources[i], 0)
                 for i in range(len(start))]) <= total
        )
    return decomposition


def solve_instance(in_file, out_dir):

    instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out_final.txt')

    w, n, x, y, l_max, mag_w = read_file(in_file)

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y))

    # area of each circuit
    area = [x[i] * y[i] for i in range(n)]

    # definition of the variables

    # coordinates of the points
    p_x = [Int("p_x_%s" % str(i+1)) for i in range(n)]
    p_y = [Int("p_y_%s" % str(i+1)) for i in range(n)]

    # maximum height to minimize
    length = z3_max([p_y[i] + y[i] for i in range(n)])

    # domain bounds
    domain_x = [And(p_x[i] >= 0,p_x[i] <= w-min(x)) for i in range(n)]
    domain_y = [And(p_y[i] >= 0,p_y[i] <= l_max-min(y)) for i in range(n)]

    # different coordinates
    all_different = [Distinct([mag_w * p_x[i] + p_y[i]]) for i in range(n)]

    # cumulative constraints
    cumulative_y = z3_cumulative(p_y, y, x, w)
    cumulative_x = z3_cumulative(p_x, x, y, l_max)

    # maximum width
    max_w = [z3_max([p_x[i] + x[i] for i in range(n)]) <= w]

    # maximum height
    max_h = [z3_max([p_y[i] + y[i] for i in range(n)]) <= l_max]

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

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(p_x[index] == 0, p_y[index] == 0)]

    # circuits must be pushed on the left
    left = [sum([If(p_x[i] <= w // 2, area[i], 0) for i in range(n)])
            >= sum([If(p_x[i] > w // 2, area[i], 0) for i in range(n)])]


    # setting the optimizer
    opt = Optimize()
    opt.add(domain_x + domain_y + overlapping + all_different + cumulative_x +
            cumulative_y + max_w + max_h + symmetry + left)
    opt.minimize(length)

    # maximum time of execution
    timeout = 300000
    opt.set(timeout=timeout)

    p_x_sol = []
    p_y_sol = []

    # solving the problem

    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    if opt.check() == sat:
        model = opt.model()
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        # getting values of variables
        for i in range(n):
            p_x_sol.append(model.evaluate(p_x[i]).as_string())
            p_y_sol.append(model.evaluate(p_y[i]).as_string())
        length_sol = model.evaluate(length).as_string()

        # storing result
        write_file(w, n, x, y, p_x_sol, p_y_sol, length_sol, out_file, elapsed_time)

    elif opt.reason_unknown() == "timeout":
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Timeout")
    else:
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Unsatisfiable")


def main():

    in_file = "..\..\data\instances_txt\ins-1.txt"
    out_dir = "../out/out_final"
    solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()



