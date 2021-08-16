import argparse
import os
from glob import glob
from solve_instance import solve_instance

default_in_dir = "..\instances_dzn" if os.name == 'nt' else "../instances_txt"
default_out_dir = "..\out" if os.name == 'nt' else "../out"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str)
    parser.add_argument("-o", "--out_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str)
    parser.add_argument("-s", "--symmetries", help="Flag to decide whether run model_symmetries, default is model_final",
                        required=False, action='store_true')
    parser.add_argument("-c", "--channel", help="Flag to decide whether run model_channel, default is model_final",
                        required=False, action='store_true')
    parser.add_argument("-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits",
                        required=False, action='store_true')
    args = parser.parse_args()

    # model to execute
    if args.symmetries:
        model = "symmetries"
    elif args.channel:
        model = "channel"
    elif args.rotation:
        model = "rotation"
    else:
        model = "final"

    print(f'Using model_{model} to solve instances.')

    in_dir = args.in_dir if args.in_dir is not None else default_in_dir
    out_dir = args.out_dir if args.out_dir is not None else os.path.join(default_out_dir, model)

    for i in range(len(glob(os.path.join(in_dir, '*.dzn')))):
        in_file = os.path.join(in_dir, f'ins-{i + 1}.dzn')

        print(f"\nSOLVING INSTANCE {i + 1}:")

        cores = 1

        if args.symmetries:
            solve_instance(cores, "model_symmetries.mzn", in_file, out_dir)
        elif args.channel:
            solve_instance(cores, "model_channel.mzn", in_file, out_dir)
        elif args.rotation:
            solve_instance(cores, "model_rotation.mzn", in_file, out_dir)
        else:
            solve_instance(cores, "model_final.mzn", in_file, out_dir)


if __name__ == '__main__':
    main()