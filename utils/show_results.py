import numpy as np
from matplotlib import pyplot as plt
import os


def get_results(dir_list, num_instances):

    """
    dir_list: path of directories containing instances
    num_instances: maximum number of instances that could be solved
    """

    # array containing different execution time
    results = np.zeros((len(dir_list), num_instances))

    # index of the first directory
    dir_index = 0

    for directory in dir_list:
        for instance_name in os.listdir(directory):
            file_ins = os.path.join(directory, instance_name)

            with open(file_ins, 'r') as f_in:
                lines = f_in.read().splitlines()
                elapsed_time = float(lines[-1])

                # number of the instance
                ins_index = int(instance_name[4:-8])

                # storing result in the matrix
                results[dir_index][ins_index - 1] = elapsed_time

        dir_index = dir_index + 1

    return results


def filter_solved_instances(results):

    num_solved = 0
    # list of solved instances
    solved_instances = []
    # index of solved instances
    instances = []
    for j in range(results.shape[1]):
        for i in range(results.shape[0]):
            # exists a search method that provided a solution
            if results[i][j] > 0:
                num_solved = num_solved + 1
                instances.append(j)
                solved_instances.append(str(j+1))
                break

    # creation of actually solved instances
    real_results = np.zeros((results.shape[0], num_solved))

    # index to move among columns
    j = 0
    for ins in instances:
        real_results[:,j] = results[:,ins]
        j = j + 1

    return real_results, solved_instances


def compute_position(positions, index, length, num_dir):

    return (positions - length / 2) + index * length / num_dir


def show_bar_chart(results, ins_labels, column_labels, y_label, title):

    # label locations
    x = np.arange(results.shape[1])

    # width of the bars
    width = 0.35

    fig, ax = plt.subplots()

    rects = []

    # bar chart for each directory
    for dir_index in range(results.shape[0]):
        rects.append(ax.bar(compute_position(x, dir_index + 1, width, results.shape[0]), results[dir_index][:], width,
                            label=column_labels[dir_index]))

    ax.set_ylabel(y_label)
    ax.set_yscale('log')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(ins_labels)
    ax.legend()

    plt.show()


def main():

    column_names = ['A', 'B', 'C', 'D']
    directories = ["../CP/out/final_domWdeg_min_no_restart", "../CP/out/final_domWdeg_random_linear",
                   "../CP/out/final_domWdeg_random_luby", "../CP/out/final_domWdeg_random_no_restart"]
    num = 40

    results = get_results(directories, num)
    real_results, instances_names = filter_solved_instances(results)
    y_label = "Time in seconds"
    title = "Benchmark on different search strategies with CP final model"

    show_bar_chart(real_results, instances_names,column_names, y_label, title)


main()