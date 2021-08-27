# VLSI
Very Large Scale Integration

## Utils Execution Instruction:
### Show an image of a solution:

In order to visualize solutions, you can use the script `plot_solution.py`.
It is required to pass as parameter the output file, eg:
```
python plot_solution.py -f <solution file path>
```

### Plot barchart of execution time of instances

In order to create a barchart of the times of execution of different instances, you can use the script `show_results.py`.
Enter on utils
Open file <b>show_results.py</b>
In <b>main()</b> [line 106] modify:
```
column_names = <list of models names> (e.g. ['rotation','final','symmetries'])
directories = <list of output folder for the models> (e.g. ["../SAT/out/rotation","../SAT/out/final","../SAT/out/symmetries"])
num = <maximum of instances that can be plotted>
title = <title of image>
```
Then run the file 
```
python show_results.py
```
