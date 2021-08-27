## CP Execution Instruction:
# Execute all the instances:

``` console
cd CP\src
python solve_cp_instances.py -m <model path> -i <instances folder> -o <folder to save output>
```

# Execute one single instance:
Enter on CP\src <br>
Open <b>solve_instance.py</b> <br>
In <b>main()</b> [line 25] modify: <br>
```python
model = <model path>
in_file = <path of instance file>
out_dir = <folder to save the output>
```
Run <b>solve_instance.py</b>

``` console
cd CP\src
python solve_instance.py
```
