import argparse
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import sys
from os import path


# Define function to plot the solution
def plot_solution(w_plate, h_plate, n, circuits, solution, colors=None):
    """
    Show the given solution as a 2D plot.
    The solution should be a list of bottom left corners,
    contained in the given w_plate and h_plate margins
    """
    assert(isinstance(w_plate, int))
    assert(isinstance(h_plate, int))
    assert(isinstance(circuits, list))
    assert(isinstance(n, int) and n == len(circuits))
    assert(isinstance(solution, dict))
    assert('corners' in solution)
    assert(len(circuits) == len(solution['corners']))

    corners = solution['corners']

    # get n random colors if they are not passed as parameter
    if colors is None:
        colors = np.random.rand(n, 3)

    fig, ax = plt.subplots(facecolor='w', edgecolor='k')

    for i in range(n):
        ax.add_patch(Rectangle(
            corners[i],
            circuits[i][0],
            circuits[i][1],
            facecolor=colors[i]
        ))
    ax.set_xlim(0, w_plate)
    ax.set_ylim(0, h_plate)
    plt.xlabel("width")
    plt.ylabel("height")
    plt.grid(color='black', linestyle='--')

    # TODO insert legend

    #plt.savefig(f"plots/{model}/{w_paper}x{h_paper}-sol.png", dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":

    # Construct the argument parser
    parser = argparse.ArgumentParser()

    # Add the arguments to the parser
    parser.add_argument("-f", "--filename", help="Filename of the output of the problem", required=True, type=str)
    args = parser.parse_args()

    if not path.isfile(args.filename):
        print("\nSpecified file does not exist, please insert an existing solution file.\n")
    else:
        with open(args.filename, "r") as file:  # Use file to refer to the file object

            # Read the first line which contains the width and the minimal height of the silicon plate
            first_line = file.readline().strip().split(" ")

            width = int(first_line[0])
            height = int(first_line[1])

            # Read the second line which contains the number of necessary circuits
            n_circuits = int(file.readline().strip())

            # Read all the remaining lines which contains the horizontal and vertical dimension of the i-th circuit
            # and its bottom left corner coordinate
            remaining_lines = file.readlines()

            # To remove empty lines
            remaining_lines = [line.strip() for line in remaining_lines if line.strip()]

            circuits = []
            solution = {'corners': []}

            for i, line in enumerate(remaining_lines):
                line = line.split()
                circuits.append((int(line[0]), int(line[1])))
                solution['corners'].append((int(line[2]), int(line[3])))

        plot_solution(width, height, n_circuits, circuits, solution)