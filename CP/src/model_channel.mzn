include "globals.mzn";

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

% x coordinate of circuits
array[CIRCUITS] of var 0..w-min(x): p_x;

% y coordinate of circuits
array[CIRCUITS] of var 0..l_max-min(y): p_y;

% length of the plate to minimize
var MAX_HEIGTH: l;
l = max([p_y[i] + y[i] | i in CIRCUITS]);

% channeling with a matrix containing the distribution of the circuits
array[0..w-1,0..l_max-1] of var 0..n: board;

% area of each circuit
array[CIRCUITS] of int: area = [ x[i] * y[i] | i in CIRCUITS];



% constraints of the problem

% all coordinates must be different
constraint forall(i,j in CIRCUITS where i<j)(p_x[i] != p_x[j] \/ p_y[i] != p_y[j]);


% maximum width
constraint max([p_x[i] + x[i] | i in CIRCUITS]) <= w;

% maximum heigth
constraint max([p_y[i] + y[i] | i in CIRCUITS]) <= l_max;

% relationship on x axes
% if the x of a block is between the x of another block and its x plus its width, it means that
% the other block is on or under this block
constraint forall(i,j in CIRCUITS where i != j)((p_x[j] <= p_x[i] /\ p_x[i] < p_x[j] + x[j]) -> (p_y[j] + y[j] <= p_y[i]) \/ (p_y[i] + y[i] <= p_y[j]));

% relationship on y axes
% if the y of a block is between the y of another block and its y plus its heigth, it means that
% the other block is on the right or left of this block
constraint forall(i,j in CIRCUITS where i != j)((p_y[j] <= p_y[i] /\ p_y[i] < p_y[j] + y[j]) -> (p_x[j] + x[j] <= p_x[i]) \/ (p_x[i] + x[i] <= p_x[j]));

% considering each circuit as an activity whose duration is the verical length and amount of resources is equals to its horizontal length
constraint cumulative(p_y, y, x, w);
constraint cumulative(p_x, x, y, l_max);

% constraint on the board
constraint forall(i in 0..w-1,j in 0..l_max-1, k in CIRCUITS)(board[i,j] == k <-> p_x[k] <= i /\ i < p_x[k] + x[k] /\ p_y[k] <= j /\ j < p_y[k] + y[k]);

% constraint on the number of space each circuit must cover
constraint global_cardinality(array1d(board), [i | i in CIRCUITS], area);

 
% minimizing the length of the plate
ann: search_ann_x = int_search(p_x,dom_w_deg,indomain_random);
ann: search_ann_y = int_search(p_y,dom_w_deg,indomain_random);
ann: restart = restart_luby(100);

% maybe also a LNS could be useful for this COP

solve :: search_ann_x
      :: search_ann_y
      :: restart
      minimize l;

output["\(w) \(l)\n\(n)\n"] ++ ["\(x[i]) \(y[i]) \(p_x[i]) \(p_y[i])\n" | i in CIRCUITS];