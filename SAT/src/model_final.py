from sat_utils import *
import time
from tqdm import tqdm

def solve_instance(in_file, out_dir):
    instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
    instance_name = instance_name[:len(instance_name) - 4]
    out_file = os.path.join(out_dir, instance_name + '-out.txt')

    w, n, x, y, l_max = read_file(in_file)

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
    for i in tqdm(range(l_max), desc='Constraint 1: no overlapping between circuits', leave=False):
        for j in range(w):
            no_overlapping += amo_pairwise(p[i][j])

    # 2 - CONSTRAINT
    # Iterate over all the n circuits
    exactly_one_circuit_positioning = []
    for k in tqdm(range(n), desc='Constraint 2: exactly one circuit positioning', leave=False):
        x_k = x[k]
        y_k = y[k]

        # clause containing all possible positions of each circuit into the plate
        all_circuit_positions = []

        # Iterate over all the coordinates where the circuit can fit
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
    one_hot_length = exactly_one([l[i] for i in tqdm(range(l_max), desc='Constraint 3: one hot encoding length', leave=False)])

    # 4 - CONSTRAINT
    # compute the length consistent wrt the actual circuits positioning
    length_circuits_positioning = [l[i] == And([Or(flat(p[i]))] + [Not(Or(flat(p[j]))) for j in range(i + 1, l_max)])
                                   for i in
                                   tqdm(range(l_max), desc='Constraint 4: length consistent wrt circuits positioning', leave=False)]

    # 5 - CONSTRAINT
    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    max_y = np.argmax(y)
    highest_circuit_first = [
        And([p[i][j][k] if k == max_y else Not(p[i][j][k]) for k in range(n) for j in range(x[max_y]) for i in
             tqdm(range(y[max_y]), desc='Constraint 5: set highest circuit first', leave=False)])]

    ''' SETTING THE SOLVER '''
    solver = Solver()

    print('Adding constraints...')

    # add constraints
    solver.add(no_overlapping)
    solver.add(exactly_one_circuit_positioning)
    solver.add(one_hot_length)
    solver.add(length_circuits_positioning)
    solver.add(highest_circuit_first)


    # maximum time of execution
    timeout = 300000
    solver.set("timeout", timeout)

    ''' SOLVING THE PROBLEM '''
    print('Checking the model...')

    print(f'{out_file}:', end='\t', flush=True)
    start_time = time.time()

    # utility variable to check if a solution is been found
    solution_found = False

    # check the model until the minimal length is reached
    while True:
        if solver.check() == sat:

            model = solver.model()
            for k in range(l_max):
                if model.evaluate(l[k]):
                    length_sol = k

            # prevent next model from using the same assignment as a previous model
            solver.add(at_least_one([l[i] for i in range(length_sol)]))

            solution_found = True

        else:
            # break when it is impossible to improve anymore the length
            break

    if solution_found:
        length_sol += 1

        elapsed_time = time.time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')

        print(f"The minimal length is {length_sol}")
        p_x_sol, p_y_sol, rot_sol = model_to_coordinates(model, p, w, length_sol, n)

        # storing result
        write_file(w, n, x, y, p_x_sol, p_y_sol, rot_sol, length_sol, elapsed_time, out_file)

        if solver.reason_unknown() == "timeout":
            print("Timeout reached, no optimal solution provided")

    elif solver.reason_unknown() == "timeout":
        print("Timeout reached, no optimal solution provided")
    else:
        print("Unsatisfiable problem")


def main():
    in_file = "..\..\data\instances_txt\ins-11.txt"
    out_dir = "..\\out\\final"
    solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()
