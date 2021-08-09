import os
import pandas as pd


def get_dataframe(list_of_dir):

    dataframe_list = []
    # for each instance in the folder create a dictionary which associates to each instance the elapsed time
    for directory in list_of_dir:
        dir_dict = {}
        for instance_name in os.listdir(directory):
            file_ins = os.path.join(directory, instance_name)
            with open(file_ins, 'r') as f_in:
                lines = f_in.read().splitlines()
                elapsed_time = lines[-1]
                dir_dict[instance_name] = elapsed_time
        dataframe_list.append(dir_dict)

    # creation of the datafame to use for visulizaion
    df = pd.DataFrame(dataframe_list)
    return df


def main():
    directories = ["../CP/out", "../SAT/src/out", "../SMT/out"]
    data = get_dataframe(directories)
    print(data)


if __name__ == "__main__":
    main()