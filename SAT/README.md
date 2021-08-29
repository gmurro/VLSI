## SAT Execution Instruction:
# Execute all the instances:

``` console
cd SAT\src
pyhton solve_sat_instances.py [-h] [-i <instances folder>] [-o <folder to save output>] [-s execution of model_symmetries ] [-b execution of model_bimander] [-r execution of  model rotation]
```

# Execute one single instance:
Enter on SAT\src <br>
Open the model [<b>model_final</b> | <b>model_bimander</b> | <b>model_symmetries</b> | <b>model rotation</b>] you want to run <br>
In <b>main()</b> [last method] modify: <br>
```python
in_file = <path instance file>
out_dir = <folder to save the output>
```
Run the model

``` console
cd SAT\src
python <model file name>
```
