import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def get_dataframe(list_of_dir, column_names):

    dataframe_list = []
    # for each instance in the folder create a dictionary which associates to each instance the elapsed time
    for directory in list_of_dir:
        dir_dict = {}
        for instance_name in os.listdir(directory):
            file_ins = os.path.join(directory, instance_name)
            with open(file_ins, 'r') as f_in:
                lines = f_in.read().splitlines()
                elapsed_time = float(lines[-1])
                dir_dict["{}".format(instance_name[:-4])] = elapsed_time
        dataframe_list.append(dir_dict)
    print(dataframe_list)

    # creation of the datafame to use for visulizaion purpose
    df = pd.DataFrame(data=dataframe_list, columns=column_names)

    print(df)
    # setting NaN to 0 (instance too hard to execute)
    df = df.fillna(0)

    return df


def show_histogram(df):

    df.plot.bar()
    #plt.show()


def main():
    column_names = ['CP', 'SAT', 'SMT']
    directories = ["../CP/out", "../SAT/src/out", "../SMT/out"]
    data = get_dataframe(directories, column_names)
    show_histogram(data)


if __name__ == "__main__":
    main()