import argparse
import os
from glob import glob
from solve_instance import solve_instance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to the .mzn model", required=True, type=str)
    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the input .dzn instances",
                        required=True, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=True, type=str)
    parser.add_argument("-c", "--cores", help="Number of cores", required=False, type=int)
    args = parser.parse_args()

    model = args.model
    in_dir = args.in_dir
    out_dir = args.out_dir
    cores = args.cores if args.cores is not None else 1

    for in_file in glob(os.path.join(in_dir, '*.dzn')):
        solve_instance(cores, model, in_file, out_dir)


if __name__ == '__main__':
    main()