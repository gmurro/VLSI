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

    ax = df.plot.bar(rot=90, width=1)
    ax.set_yscale('log')
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.legend(loc="upper right")
    plt.show()


def main():
    column_names = ['A', 'B', 'C', 'D', 'E', 'F']
    directories = ["../CP/out/final_domWdeg_min_no_restart", "../CP/out/final_domWdeg_random_linear",
                   "../CP/out/final_domWdeg_random_luby", "../CP/out/final_domWdeg_random_no_restart",
                   "../CP/out/final_first_fail_random_linear", "../CP/out/final_input_order_indomain_min_no_restart"]
    data = get_dataframe(directories, column_names)
    show_histogram(data, 'Benchmark with different methods', 'Instances', 'Time in seconds')


if __name__ == "__main__":
    main()