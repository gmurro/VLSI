import argparse
import os
from glob import glob
import model_final
import model_bimander
import model_simmetry
import model_rotation

default_in_dir = "..\..\data\instances_txt" if os.name == 'nt' else "../../data/instances_txt"
default_out_dir = "..\out" if os.name == 'nt' else "../out_final"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str)
    parser.add_argument("-s", "--simmetry", help="Flag to decide whether run model_simmetry, default is model_final",
                        required=False, action='store_true')
    parser.add_argument("-b", "--bimander", help="Flag to decide whether run model_bimander, default is model_final",
                        required=False, action='store_true')
    parser.add_argument("-r","--rotation", help="Flag to decide whether it is possible use rotated circuits",
                        required=False, action='store_true')
    args = parser.parse_args()

    # model to execute
    model = "final"
    if args.simmetry:
        model = "simmetry"
    elif args.bimander:
        model = "bimander"
    elif args.rotation:
        model = "rotation"


    in_dir = args.in_dir if args.in_dir is not None else default_in_dir
    out_dir = args.out_dir if args.out_dir is not None else default_out_dir
    rotation = args.rotation if args.rotation is not None else False

    """in_dir = args.in_dir
    out_dir = args.out_dir
    rotation = args.rotation if args.rotation is not None else False

    if not rotation:

        # running standard model
        for in_file in glob(os.path.join(in_dir, '*.txt')):
            md.solve_instance(in_file, out_dir)"""

    '''else:

        # running rotation model
        for in_file in glob(os.path.join(in_dir, '*.txt')):
            mdr.solve_instance(in_file, out_dir)'''


if __name__ == '__main__':
    main()




