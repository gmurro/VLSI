## Visualize solutions

In order to visualize solutions, you can use the script `plot_solution.py`.
It is required to pass as parameter the output file, eg:
```
python plot_solution.py -f ../data/outputs/test.txt
```

## Solve all CP instances
Run the following command:
```
python solve_cp_instances.py -m ..\CP\model_dual.mzn -i ..\data\instances_dzn -o ..\data\outputs
```