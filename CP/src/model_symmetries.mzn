include "cumulative.mzn";
include "alldifferent.mzn";
include "global_cardinality_low_up.mzn";
include "lex_lesseq.mzn";
include "diffn.mzn";

% input of the problem

% width of the plate
int: w;
set of int: FEASIBLE_WIDTH = 1..w;

% maximum heigth of the plate
int: l_max;
set of int: FEASIBLE_HEIGTH = 1..l_max;

% number of circuits
int: n;
set of int: CIRCUITS = 1..n;

% horizontal dimension of circuits
array[CIRCUITS] of FEASIBLE_WIDTH: x;

% vertical dimension of the circuits
array[CIRCUITS] of FEASIBLE_HEIGTH: y;

% order of magnitude of w
% N.B. not used in this model but necessary to run it because it is in the input file
int: mag_w;


% definition of the variables

% x coordinate of circuits
array[CIRCUITS] of var 0..w-min(x): p_x;

% y coordinate of circuits
array[CIRCUITS] of var 0..l_max-min(y): p_y;

% length of the plate to minimize
var FEASIBLE_HEIGTH: l;
l = max([p_y[i] + y[i] | i in CIRCUITS]);

% duel modeling
% channeling with a matrix containing the distribution of the circuits
set of int: VALUES = 1..n+1;
array[0..l_max-1,0..w-1] of var VALUES: plate;


% constraints of the problem

% IMPLIED CONSTRAINTS

% maximum width
constraint max([p_x[i] + x[i] | i in CIRCUITS]) <= w;

% maximum heigth
constraint max([p_y[i] + y[i] | i in CIRCUITS]) <= l_max;

% relationships among circuits
constraint diffn(p_x, p_y, x, y);


% considering each circuit as an activity whose duration is the verical length and amount of resources is equals to its horizontal length
constraint cumulative(p_y, y, x, w);
constraint cumulative(p_x, x, y, l_max);

% channelling constraint
% constraint on the board
constraint forall(i in 0..l_max-1,j in 0..w-1, k in CIRCUITS)(plate[i,j] == k <-> (p_x[k] <= i /\ i < p_x[k] + x[k] /\ p_y[k] <= j /\ j < p_y[k] + y[k]));

% cardinality constraint
constraint forall(i in 0..l_max-1)(
  global_cardinality_low_up([plate[i,j] | j in 0..w-1], 0..n, [0 | k in 0..n], [w | k in 0..n])
);

constraint forall(j in 0..w-1)(
  global_cardinality_low_up([plate[i,j] | i in 0..l_max-1], 0..n, [0 | k in 0..n], [l_max | k in 0..n])
);

% symmetry breaking (horizontal flip, vertical flip and 180° rotation)
constraint symmetry_breaking_constraint(
           lex_lesseq(array1d(plate), [ plate[i,j] | i in 0..l_max-1, j in reverse(0..w-1)])
        /\ lex_lesseq(array1d(plate),[ plate[i,j] | i in reverse(0..l_max-1), j in 0..w-1])
        /\ lex_lesseq(array1d(plate), [ plate[i,j] | i in reverse(0..l_max-1), j in reverse(0..w-1)]));

% Parameters to control the search heuristic and restart strategy
int: heuristic = 6;
int: restart = 4;

ann: search_ann_x = 
if heuristic == 1 then
  int_search(p_x, input_order, indomain_min)
elseif heuristic == 2 then
  int_search(p_x, first_fail, indomain_min)
elseif heuristic == 3 then
  int_search(p_x, dom_w_deg, indomain_min)
elseif heuristic == 4 then
  int_search(p_x, input_order, indomain_random)
elseif heuristic == 5 then
  int_search(p_x, first_fail, indomain_random)
else
  int_search(p_x, dom_w_deg, indomain_random)
endif;

ann: search_ann_y = 
if heuristic == 1 then
  int_search(p_y, input_order, indomain_min)
elseif heuristic == 2 then
  int_search(p_y, first_fail, indomain_min)
elseif heuristic == 3 then
  int_search(p_y, dom_w_deg, indomain_min)
elseif heuristic == 4 then
  int_search(p_y, input_order, indomain_random)
elseif heuristic == 5 then
  int_search(p_y, first_fail, indomain_random)
else
  int_search(p_y, dom_w_deg, indomain_random)
endif;

ann: search_ann_plate = 
if heuristic == 1 then
  int_search(array1d(plate), input_order, indomain_min)
elseif heuristic == 2 then
  int_search(array1d(plate), first_fail, indomain_min)
elseif heuristic == 3 then
  int_search(array1d(plate), dom_w_deg, indomain_min)
elseif heuristic == 4 then
  int_search(array1d(plate), input_order, indomain_random)
elseif heuristic == 5 then
  int_search(array1d(plate), first_fail, indomain_random)
else
  int_search(array1d(plate), dom_w_deg, indomain_random)
endif;

ann: restart_ann =
if restart == 1 then
  restart_constant(100)
elseif restart == 2 then
  restart_linear(100)
elseif restart == 3 then
  restart_geometric(1.5,100)
elseif restart == 4 then
  restart_luby(100)
else
  restart_none
endif;

solve :: search_ann_x
      :: search_ann_y
      :: search_ann_plate
      :: restart_ann
         minimize l;

output["\(w) \(l)\n\(n)\n"] ++ ["\(x[i]) \(y[i]) \(p_x[i]) \(p_y[i])\n" | i in CIRCUITS];
