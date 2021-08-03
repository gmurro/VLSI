from z3 import *
import numpy as np
from itertools import combinations
import time
import matplotlib.pyplot as plt

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

        l_max = sum(y)

        # compute order of magnitude of w
        len_w = len(str(w))
        mag_w = 10 ** len_w

        return int(w), int(n), x, y, l_max, mag_w


def write_file(w, n, x, y, p_x_sol, p_y_sol, length, out_file):

    with open(out_file, 'w+') as f_out:

        f_out.write('{} {}\n'.format(w, length))
        f_out.write('{}\n'.format(n))

        for i in range(n):
            f_out.write('{} {} {} {}\n'.format(x[i], y[i], p_x_sol[i], p_y_sol[i]))


def z3_max(vector):
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)
    return maximum


def at_least_one(bool_vars):
    return Or(bool_vars)


def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]


def exactly_one(bool_vars):
    return at_most_one(bool_vars) + [at_least_one(bool_vars)]


def solve_instance(in_file, out_dir):

    instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    w, n, x, y, l_max, mag_w = read_file(in_file)

    # Define solver and base model
    solver = Solver()

    # definition of the variables

    # coordinates of the points
    plate = [[[Bool(f"b_{i}_{j}_{k}") for k in range(n)] for j in range(w)] for i in range(l_max)]

    # maximum height to minimize
    l = [Bool(f"l_{i}") for i in range(l_max)]

    print('Adding constraints...')

    # Each cell in the plate has only one value
    [solver.add(at_most_one(plate[i][j])) for i in range(l_max) for j in range(w)]

    # Iterate over all the n circuits
    for k in range(n):
        x_k = x[k]
        y_k = y[k]

        # clause containing all possible positions of each circuit into the plate
        all_circuit_positions = []

        # Iterate over all the coordinates where p can fit
        for i in range(l_max - y_k + 1):
            for j in range(w - x_k + 1):

                # all cells corresponding to the circuit position
                circuit_positioning = []

                # Iterate over the cells of circuit's patch
                for oy in range(l_max):
                    for ox in range(w):
                        if i <= oy < i + y_k and j <= ox < j + x_k:
                            circuit_positioning.append(plate[oy][ox][k])
                        else:
                            circuit_positioning.append(Not(plate[oy][ox][k]))

                """               
                for oy in range(i, i+y_k):
                    for ox in range(j, j+x_k):
                        circuit_positioning.append(plate[oy][ox][k])"""

                all_circuit_positions.append(And(*circuit_positioning))

        # Exactly one
        solver.add(at_least_one(all_circuit_positions))
        solver.add(at_most_one(all_circuit_positions))

    # compute the length
    solver.add([l[i] == And( [Or(list(np.concatenate(plate[i]).flat) )] + [Not(Or( list(np.concatenate(plate[j]).flat))) for j in range(i+1, l_max)]) for i in range(l_max)])

    # value of length
    #objective = [length == z3_max([k + y[i] if p_y[i][k] is True else None for k in range(l_max - min(y)) for i in range(n)])]


    # maximum time of execution
    #timeout = 300000
    #solver.set(timeout=timeout)

    solver.push()
    i = 0
    while solver.check() == sat and (i < 5):
        model = solver.model()
        for k in range(l_max):
            if model.evaluate(l[k]):
                print(k)
                length = k

        sol = np.zeros((l_max, w))

        for k in range(n):

            sol_2 = []
            for i in range(l_max):
                sol_2.append([])
                for j in range(w):
                    if model.evaluate(plate[i][j][k]):
                        sol_2[i].append(1)
                        sol[i][j] = k
                    else:
                        sol_2[i].append(0)

            plt.imshow(sol_2)
            plt.show()
        solver.add(at_least_one([l[i] for i in range(length)]))  # prevent next model from using the same assignment as a previous model
        i += 1
    solver.pop()

'''
    # solving the problem

    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    if solver.check() == sat:
        model = solver.model()
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        """
        sol = []
        for i in range(l_max):
            for j in range(w):
                for k in range(n):
                    if model.evaluate(plate[i][j][k]):
                        sol[i].append(k + 1)"""

        sol = np.zeros((l_max, w))

        for k in range(n):
            sol_2 = []
            for i in range(l_max):
                sol_2.append([])
                for j in range(w):
                    if model.evaluate(plate[i][j][k]):
                        sol_2[i].append(1)
                        sol[i][j] = k
                    else:
                        sol_2[i].append(0)

            plt.imshow(sol_2)
            plt.show()


        for k in range(l_max):
            if model.evaluate(l[k]):
                print(k)




        # getting values of variables
        #length_sol = model.evaluate(length).as_string()

        # storing result
        #write_file(w, n, x, y, p_x_sol, p_y_sol, length_sol, out_file)

    elif solver.reason_unknown() == "timeout":
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Timeout")
    else:
        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')
        print("Unsatisfiable")
'''

def main():

    in_file = "..\..\data\instances_txt\ins-1.txt"
    out_dir = "out"
    solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()
