include "cumulative.mzn";

% input of the problem

% width of the plate
int: w;
set of int: MAX_WIDTH_CIR = 1..w;

% number of circuits
int: n;
set of int: CIRCUITS = 1..n;

% horizontal dimension of circuits
array[CIRCUITS] of MAX_WIDTH_CIR: x;

% vertical dimension of the circuits
array[CIRCUITS] of int: y;

% maximum heigth of the plate
int: l_max;
set of int: MAX_HEIGTH = 1..l_max;

% definition of the variables

% matrix containing left-bottom corner coordinates of each circuit
array[CIRCUITS,1..2] of var 0..l_max-1: p;

% length of the plate to minimize
var MAX_HEIGTH: l;
l = max([p[i,2] + y[i] | i in CIRCUITS]);

% constraints of the problem

% all coordinates must be different
constraint forall(i,j in CIRCUITS where i<j)(p[i,1] != p[j,1] \/ p[i,2] != p[j,2]);

% maximum width
constraint max([p[i,1] + x[i] | i in CIRCUITS]) <= w;

% maximum heigth
constraint max([p[i,2] + y[i] | i in CIRCUITS]) <= l_max;

% relationship on y axes
% if the y of a block is between the y of another block and its y plus its heigth, it means that
% the other block is on the right or left of this block
constraint forall(i,j in CIRCUITS where i<j)((p[j,2] <= p[i,2] /\ p[i,2] < p[j,2] + y[j]) -> (p[j,1] + x[j] <= p[i,1]) \/ (p[i,1] + x[i] <= p[j,1]));

% considering each circuit as an activity whose duration is the verical length and amount of resources is equals to its horizontal length
constraint cumulative([p[i,2] | i in CIRCUITS], y, x, w);

% constraint about x
constraint forall(i,j in CIRCUITS where i < j)(p[i,2] == p[j,2] -> (p[i,1] + x[i] <= p[j,1]) \/ (p[j,1] + x[j] <= p[i,1]));


% minimizing the length of the plate
solve minimize l;

output["\(w) \(l)\n\(n)\n"] ++ ["\(x[i]) \(y[i]) \(p[i,1]) \(p[i,2])\n" | i in CIRCUITS];