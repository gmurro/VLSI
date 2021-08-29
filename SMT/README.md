## SMT Execution Instruction:
# Execute all the instances:

``` console
cd SMT\src
pyhton solve_smt_instances.py [-h] [-i <instances folder>] [-o <folder to save output>] [-r execution of  model rotation]
```

# Execute one single instance:
Enter on SMT\src <br>
Open the model [<b>model_final</b> | <b>model rotation</b>] you want to run <br>
In <b>main()</b> [last method] modify: <br>
```python
in_file = <path instance file>
out_dir = <folder to save the output>
```
Run the model

``` console
cd SMT\src
python <model file name>
```
