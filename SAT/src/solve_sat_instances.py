import argparse
from glob import glob
import model_final as md
from z3 import *


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the initial instances",
                        required=True, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=True, type=str)
    parser.add_argument("-r","--rotation", help="Flag to decide whether it is possible use rotated circuits",
                        required=False, action='store_true')
    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out_dir
    rotation = args.rotation if args.rotation is not None else False

    if not rotation:

        # running standard model
        for in_file in glob(os.path.join(in_dir, '*.txt')):
            md.solve_instance(in_file, out_dir)

    '''else:

        # running rotation model
        for in_file in glob(os.path.join(in_dir, '*.txt')):
            mdr.solve_instance(in_file, out_dir)'''


if __name__ == '__main__':
    main()




