from z3 import *
import numpy as np
from itertools import combinations
import time
from tqdm import tqdm


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


def z3_lex_less_eq(x, y, n, desc):
    return And([z3_less_eq(x[0], y[0])] +
               [
                   Implies(
                       And([And([x[j][k] == y[j][k] for k in range(n)]) for j in range(i)]),
                       z3_less_eq(x[i], y[i])
                   )
                   for i in tqdm(range(1, len(x)), desc=desc)
               ])


def bool_greater_eq(x, y):
    return Or(x, Not(y))


# less_eq between arrays of bool "one-hot" encoded
# implementation like lexicographical ordering encoding
def z3_less_eq(x, y):
    return And(
            [bool_greater_eq(x[0], y[0])] +
            [
                Implies(
                    And([x[j] == y[j] for j in range(i)]),
                    bool_greater_eq(x[i], y[i])
                )
                for i in range(1, len(x))
            ]
    )


def at_least_one(bool_vars):
    return Or(bool_vars)


def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]


def exactly_one(bool_vars):
    return at_most_one(bool_vars) + [at_least_one(bool_vars)]


def flat(list_of_lists):
    return list(np.concatenate(list_of_lists).flat)


def model_to_coordinates(model, p, w, l, n):
    # Create solution array
    solution = np.array([[[is_true(model[p[i][j][k]]) for k in range(n)] for j in range(w)] for i in range(l)])

    p_x_sol = []
    p_y_sol = []
    for c in range(n):
        y_ids, x_ids = solution[:, :, c].nonzero()
        x = np.min(x_ids)
        y = np.min(y_ids)
        p_x_sol.append(x)
        p_y_sol.append(y)
    return p_x_sol, p_y_sol


def solve_instance(in_file, out_dir):
    instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    w, n, x, y, l_max, mag_w = read_file(in_file)


    max_x = max(x)
    max_y = max(y)
    w_blocks = w // max_x
    l_max = -(l_max // -w_blocks)
    l_max = max_y if l_max < max_y else l_max

    ''' DEFINITION OF THE VARIABLES '''

    # plate of boolean variables
    p = [[[Bool(f"p_{i}_{j}_{k}") for k in range(n)] for j in range(w)] for i in range(l_max)]

    # length of the plate to minimize (one-hot representation)
    l = [Bool(f"l_{i}") for i in range(l_max)]

    ''' DEFINITION OF THE CONSTRAINTS '''

    print('Defining constraints...')

    # 1 - CONSTRAINT
    # Each cell in the plate has at most one value
    no_overlapping = []
    for i in tqdm(range(l_max), desc='Constraint 1: no overlapping between circuits'):
        for j in range(w):
            no_overlapping += at_most_one(p[i][j])

    # 2 - CONSTRAINT
    # Iterate over all the n circuits
    exactly_one_circuit_positioning = []
    for k in tqdm(range(n), desc='Constraint 2: exactly one circuit positioning'):
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
                            circuit_positioning.append(p[oy][ox][k])
                        else:
                            circuit_positioning.append(Not(p[oy][ox][k]))

                all_circuit_positions.append(And(circuit_positioning))

        # Exactly one
        exactly_one_circuit_positioning += exactly_one(all_circuit_positions)

    # 3 - CONSTRAINT
    # one-hot encoding of the length
    one_hot_length = exactly_one([l[i] for i in tqdm(range(l_max), desc='Constraint 3: one hot encoding length')])

    # 4 - CONSTRAINT
    # compute the length consistent wrt the actual circuits positioning
    length_circuits_positioning = [l[i] == And([Or(flat(p[i]))] + [Not(Or(flat(p[j]))) for j in range(i + 1, l_max)])
                                   for i in
                                   tqdm(range(l_max), desc='Constraint 4: length consistent wrt circuits positioning')]

    # 5 - CONSTRAINT
    # symmetry breaking constraint: remove horizontal flip, vertical flip and 180° rotation
    symmetry_breaking = [z3_lex_less_eq([p[i][j] for j in range(w) for i in range(l_max)],
                              [p[i][j] for j in range(w) for i in reversed(range(l_max))], n, "Constraint 5: symmetry breaking vertial flip")]

    symmetry_breaking += [z3_lex_less_eq([p[i][j] for j in range(w) for i in range(l_max)],
                               [p[i][j] for j in reversed(range(w)) for i in range(l_max)], n, "Constraint 5: symmetry breaking horizontal flip")]

    symmetry_breaking += [z3_lex_less_eq([p[i][j] for j in range(w) for i in range(l_max)],
                               [p[i][j] for j in reversed(range(w)) for i in reversed(range(l_max))], n, "Constraint 5: symmetry breaking 180° rotation")]

    ''' SETTING THE SOLVER '''
    solver = Solver()

    print('Adding constraints...')

    # add constraints
    solver.add(no_overlapping)
    solver.add(exactly_one_circuit_positioning)
    solver.add(one_hot_length)
    solver.add(length_circuits_positioning)
    solver.add(symmetry_breaking)

    # maximum time of execution
    timeout = 300000
    solver.set(timeout=timeout)

    ''' SOLVING THE PROBLEM '''
    print('Checking the model...')

    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    # utility variable to check if at least a solution is computed before reaching the timeout
    at_least_one_solution = False

    # check the model until the minimal length is reached
    while True:
        if solver.check() == sat:

            model = solver.model()
            for k in range(l_max):
                if model.evaluate(l[k]):
                    length_sol = k

            # prevent next model from using the same assignment as a previous model
            solver.add(at_least_one([l[i] for i in range(length_sol)]))

            at_least_one_solution = True

        elif solver.reason_unknown() == "timeout":
            print("Timeout reached, no optimal solution provided")
            break
        else:
            # break when it is impossible to improve anymore the length
            break

    if at_least_one_solution:
        length_sol += 1

        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')

        print(f"The minimal length is {length_sol}")
        p_x_sol, p_y_sol = model_to_coordinates(model, p, w, length_sol, n)

        # storing result
        write_file(w, n, x, y, p_x_sol, p_y_sol, length_sol, out_file)
    else:
        print("Unsatisfiable problem")


def main():
    in_file = "..\..\data\instances_txt\ins-10.txt"
    out_dir = "out"
    solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()
