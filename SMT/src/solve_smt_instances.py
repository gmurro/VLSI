from time import time
import argparse
from glob import glob
import os
import model as md
from z3 import *


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

        return w, n, x, y, l_max, mag_w


def write_file(w, n, x, y, p_x_sol, p_y_sol, length, out_file):

    with open(out_file, 'w+') as f_out:

        f_out.write('{} {}\n'.format(w, length))
        f_out.write('{}\n'.format(n))

        for i in range(n):
            f_out.write('{} {} {} {}\n'.format(x[i], y[i], p_x_sol[i], p_y_sol[i]))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the initial instances",
                        required=True, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=True, type=str)
    parser.add_argument("-r","--rotation", help="Flag to decide whether it is possible use rotated circuits",
                        required=False, type=bool)
    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out_dir
    rotation = args.rotation if args.rotation is not None else 0

    for in_file in glob(os.path.join(in_dir, '*.txt')):

        instance_name = in_file.split('\\')[-1] if os.name == 'nt' else in_file.split('/')[-1]
        instance_name = instance_name[:len(instance_name) - 4]
        out_file = os.path.join(out_dir, instance_name + '-out.txt')

        # reading data from the file
        w, n, x, y, l_max, mag_w = read_file(in_file)

        # solving the current instance
        print(f'{out_file}:', end='\t', flush=True)
        start_time = time()
        msg, p_x_sol, p_y_sol, length = md.solve_instance(w, n, x, y, l_max, mag_w)
        elapsed_time = time() - start_time
        print(f'{elapsed_time * 1000:.1f} ms')

        # storing the output with the standard format
        write_file(w, n, x, y, p_x_sol, p_y_sol, length, out_file)


if __name__ == '__main__':
    main()




