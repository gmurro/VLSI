from z3 import *
import numpy as np
from itertools import combinations
from tqdm import tqdm

def read_file(input_filename):
    with open(input_filename, 'r') as f_in:
        lines = f_in.read().splitlines()

        w = int(lines[0])
        n = int(lines[1])

        x = []
        y = []

        for i in range(int(n)):
            split = lines[i + 2].split(' ')
            x.append(int(split[0]))
            y.append(int(split[1]))

        # compute a feasible approximation of l_max
        l_max = sum(y)
        max_x = max(x)
        max_y = max(y)
        w_blocks = w // max_x
        l_max = -(l_max // -w_blocks)
        l_max = max_y if l_max < max_y else l_max

        return w, n, x, y, l_max


def write_file(w, n, x, y, p_x_sol, p_y_sol, rot_sol, length, elapsed_time,  out_file):
    with open(out_file, 'w+') as f_out:
        f_out.write('{} {}\n'.format(w, length))
        f_out.write('{}\n'.format(n))

        for i in range(n):
            is_rotated = "R" if rot_sol[i] else ""
            f_out.write('{} {} {} {} {}\n'.format(x[i], y[i], p_x_sol[i], p_y_sol[i], is_rotated))
        f_out.write(f'{elapsed_time :.2f}')


def z3_lex_less_eq(x, y, n, desc):
    return And([z3_less_eq(x[0], y[0])] +
               [
                   Implies(
                       And([And([x[j][k] == y[j][k] for k in range(n)]) for j in range(i)]),
                       z3_less_eq(x[i], y[i])
                   )
                   for i in tqdm(range(1, len(x)), desc=desc, leave=False)
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


# at least one constraint
def at_least_one(bool_vars):
    return Or(bool_vars)


# at most one constraint pairwise encoding
def amo_pairwise(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]


# at most one constraint binary encoding
def amo_binary(x, aux_vars):
    n = len(x)

    k = int(np.ceil(np.log2(n)))

    clause = []
    for i in range(n):
        # i represented as a binary string (reversed)
        i_binary = np.binary_repr(i, k)[::-1]

        for j in range(k):
            clause += [Or(Not(x[i]), aux_vars[j]) if i_binary[j] == "1" else Or(Not(x[i]), Not(aux_vars[j]))]
    return clause


# at most one constraint bimander encoding
def amo_bimander(bool_vars, aux_vars, m):
    k = len(aux_vars)

    # split variables in m subsets
    g = np.array_split(bool_vars, m)

    first_clause = []
    for i in range(m):
        first_clause += amo_pairwise(g[i])

    second_clause = []
    for i in range(m):
        # i represented as a binary string (reversed)
        i_binary = np.binary_repr(i, k)[::-1]
        for h in range(len(g[i])):
            for j in range(k):
                second_clause += [Or(Not(g[i][h]), aux_vars[j]) if i_binary[j] == "1" else Or(Not(g[i][h]), Not(aux_vars[j]))]

    return first_clause + second_clause


def exactly_one(bool_vars):
    return amo_pairwise(bool_vars) + [at_least_one(bool_vars)]


def flat(list_of_lists):
    return list(np.concatenate(list_of_lists).flat)


def model_to_coordinates(model, p, w, l, n, r=None):
    # Create solution array
    solution = np.array([[[is_true(model[p[i][j][k]]) for k in range(n)] for j in range(w)] for i in range(l)])

    p_x_sol = []
    p_y_sol = []
    rot_sol = [False for i in range(n)]

    for k in range(n):
        y_ids, x_ids = solution[:, :, k].nonzero()
        x = np.min(x_ids)
        y = np.min(y_ids)
        p_x_sol.append(x)
        p_y_sol.append(y)
        if r is not None:
            rot_sol[k] = is_true(model[r[k]])
    return p_x_sol, p_y_sol, rot_sol
