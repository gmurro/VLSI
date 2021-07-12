## PROJECT CDMO

We have to insert given circuits into a silicon plate.

Points:

- fixed width 
- fixed orientation of circuits
- number and dimensions of circuits are given 
- minimize length

**Instances example format**:

```
9 (w, width of silicon plate)
5 (n, number of necessary circuits to place)
3 3 (circuit 1, dimension x=3 - horizontal, y=3 - vertical)
2 4 
2 8 
3 9 
4 12
```

**Solution format**:

```
9 12 (w as before + l which is the minimal length of the plate)
5 (n, number of necessary circuits to place, as before)
3 3 4 0 (x, y as before + cx, cy which are coordinates of the left-bottom corner)
2 4 7 0
2 8 7 4
3 9 4 3
4 12 0 0
```



### Model

1. *Data*:

   - w
   - n
   - max_l (sum of all heights of circuits)

2. *Variables*: 

   - l (max of each column in the matrix that contains something)
   - p matrix of dimension w, max_l

3. Domains: 

   - p in [0, n] (0 means empty, 1,2,3..., n represent the correspondent block)

   

4. *Constraints*: 

   - sum on any horizontal line traversed circuits can be at most w (implied constraint)
   - global constraints
   - symmetry braking constraints 
     - (ideas) set initially bigger blocks

5. *Objective function*: minimize l



For CP investigate how work whether the rotation is allowed





### Runtime

Solutions must be provided by the model within 300 sec.

Solve as many instances as possible in this time range.