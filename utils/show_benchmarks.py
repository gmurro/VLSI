import os
import pandas as pd
from matplotlib import pyplot as plt


def get_dataframe(list_of_dir, column_names):

    i = 0
    dataframe_dict = {}
    # for each instance in the folder create a dictionary which associates to each instance the elapsed time
    for directory in list_of_dir:
        dir_dict = {}
        for instance_name in os.listdir(directory):
            file_ins = os.path.join(directory, instance_name)
            with open(file_ins, 'r') as f_in:
                lines = f_in.read().splitlines()
                elapsed_time = float(lines[-1])
                dir_dict["{}".format(instance_name[:-8])] = elapsed_time
        dataframe_dict['{}'.format(column_names[i])] = dir_dict
        i = i + 1

    # creation of the datafame to use for visulizaion purpose
    df = pd.DataFrame(dataframe_dict)

    # setting NaN to 0 (instance too hard to execute)
    df = df.fillna(0)

    # ordering for instance name
    df = df.sort_index()

    return df


def show_histogram(df, title, x_label, y_label):

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    df.plot.bar()
    plt.legend(loc="upper right")
    plt.show()


def main():
    column_names = ['CP', 'SAT', 'SMT']
    directories = ["../CP/out", "../SAT/out/final", "../SMT/out"]
    data = get_dataframe(directories, column_names)
    show_histogram(data, "Benchmark with different methods", "Instances", "Time in seconds")


if __name__ == "__main__":
    main()