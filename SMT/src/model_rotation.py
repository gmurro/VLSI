from z3 import *
import numpy as np
from itertools import combinations
import time
import model_final as md


def write_file(w, n, x, y, p_x_sol, p_y_sol, rot_sol, length, out_file, elapsed_time):

    with open(out_file, 'w+') as f_out:

        f_out.write('{} {}\n'.format(w, length))
        f_out.write('{}\n'.format(n))

        for i in range(n):
            is_rotated = "R" if rot_sol[i] else ""
            f_out.write('{} {} {} {} {}\n'.format(x[i], y[i], p_x_sol[i], p_y_sol[i], is_rotated))

        f_out.write('{}'.format(elapsed_time))


def solve_instance(in_file, out_dir):

    instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    w, n, x, y, l_max, mag_w = md.read_file(in_file)

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

    # real dimensions of circuits considering rotation
    x_r = [If(And(x[i] != y[i], rotation[i]), y[i], x[i]) for i in range(n)]
    y_r = [If(And(x[i] != y[i], rotation[i]), x[i], y[i]) for i in range(n)]

    # maximum height to minimize
    length = md.z3_max([p_y[i] + y[i] for i in range(n)])

    # domain bounds
    domain_x = [p_x[i] >= 0 for i in range(n)]
    domain_y = [p_y[i] >= 0 for i in range(n)]

    # lengths bound
    width_bound = [And(x_r[i] >= 1, x_r[i] <= w) for i in range(n)]
    height_bound = [And(y_r[i] >= 1, y_r[i] <= l_max) for i in range(n)]

    # different coordinates
    all_different = [Distinct([mag_w * p_x[i] + p_y[i]]) for i in range(n)]

    # cumulative constraints
    cumulative_y = md.z3_cumulative(p_y, y_r, x_r, w)
    cumulative_x = md.z3_cumulative(p_x, x_r, y_r, l_max)

    # maximum width
    max_w = [md.z3_max([p_x[i] + x_r[i] for i in range(n)]) <= w]

    # maximum height
    max_h = [md.z3_max([p_y[i] + y_r[i] for i in range(n)]) <= l_max]

    # relationship avoiding overlapping
    '''overlapping = [Or(p_x[i] + x[i] <= p_x[j],
                              p_x[j] + x[j] <= p_x[i],
                              p_y[i] + y[i] <= p_y[j],
                              p_y[j] + y[j] <= p_y[i]) for j in range(n) for i in range(j)]'''
    overlapping = []
    for (i,j) in combinations(range(n),2):
        overlapping.append(Or(p_x[i] + x_r[i] <= p_x[j],
                              p_x[j] + x_r[j] <= p_x[i],
                              p_y[i] + y_r[i] <= p_y[j],
                              p_y[j] + y_r[j] <= p_y[i])
                           )

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(p_x[index] == 0, p_y[index] == 0)]

    # circuits must be pushed on the left
    left = [sum([If(p_x[i] <= w // 2, area[i], 0) for i in range(n)])
            >= sum([If(p_x[i] > w // 2, area[i], 0) for i in range(n)])]

    # setting the optimizer
    opt = Optimize()
    opt.add(domain_x + domain_y + overlapping + all_different + cumulative_x +
            cumulative_y + max_w + max_h + symmetry + width_bound + height_bound + left)
    opt.minimize(length)

    # maximum time of execution
    timeout = 300000
    opt.set("timeout", timeout)

    p_x_sol = []
    p_y_sol = []
    rot_sol = []

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
            rot_value = model[rotation[i]]
            if rot_value is None:
                rot_sol.append(False)
            else:
                rot_sol.append(rot_value)
        length_sol = model.evaluate(length).as_string()

        # storing result
        write_file(w, n, x, y, p_x_sol, p_y_sol, rot_sol, length_sol, out_file, elapsed_time)
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
    out_dir = "../out/out_rotation"
    solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()