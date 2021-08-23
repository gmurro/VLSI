import argparse
from glob import glob
import model_final
import model_rotation
from z3 import *

default_in_dir = "..\..\data\instances_txt" if os.name == 'nt' else "../../data/instances_txt"
default_out_dir = "..\out" if os.name == 'nt' else "../out"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str)
    parser.add_argument("-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits",
                        required=False, action='store_true')
    args = parser.parse_args()

    # model to execute
    if args.rotation:
        model = "rotation"
    else:
        model = "final"

    in_dir = args.in_dir if args.in_dir is not None else default_in_dir
    out_dir = args.out_dir if args.out_dir is not None else os.path.join(default_out_dir, model)

    for i in range(len(glob(os.path.join(in_dir, '*.txt')))):
        in_file = os.path.join(in_dir, f'ins-{i + 1}.txt')

        print(f"\n\nSOLVING INSTANCE {i + 1}:")

        if args.rotation:
            model_rotation.solve_instance(in_file, out_dir)
        else:
            model_final.solve_instance(in_file, out_dir)


if __name__ == '__main__':
    main()




