include "cumulative.mzn";
include "alldifferent.mzn";
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

% array to specify whether a circuit is rotated or not
array[CIRCUITS] of var bool: rotation;

% dimensions considering rotation of the circuits

% horizontal dimension of circuits
array[CIRCUITS] of var FEASIBLE_WIDTH: x_r = [if rotation[i] then y[i] else x[i] endif | i in CIRCUITS];

% vertical dimension of the circuits
array[CIRCUITS] of var FEASIBLE_HEIGTH: y_r = [if rotation[i] then x[i] else y[i] endif | i in CIRCUITS];

% area of circuits
array[CIRCUITS] of int: area = [ x[i] * y[i] | i in CIRCUITS];

% int: index = arg_max(y);

% order of magnitude of w
% N.B. not used in this model but necessary to run it because it is in the input file
int: mag_w;

% circuit with the maximum height
int: index = arg_max(y);


% definition of the variables

% x coordinate of circuits
array[CIRCUITS] of var 0..w-min(x): p_x;

% y coordinate of circuits
array[CIRCUITS] of var 0..l_max-min(y): p_y;

% length of the plate to minimize
var FEASIBLE_HEIGTH: l;
l = max([p_y[i] + y[i] | i in CIRCUITS]);


% constraints of the problem

% IMPLIED CONSTRAINTS

% maximum width
constraint max([p_x[i] + x_r[i] | i in CIRCUITS]) <= w;

% maximum heigth (it could be eliminated for construction of l_max if we do not take into account rotation)
constraint max([p_y[i] + y_r[i] | i in CIRCUITS]) <= l_max;

% relationships among circuits
constraint diffn(p_x, p_y, x_r, y_r);

% a circuit cannot be rotated whether its height is greater than w
constraint forall(i in CIRCUITS)(y[i] > w -> rotation[i]==false);

% considering each circuit as an activity whose duration is the verical length and amount of resources is equals to its horizontal length
constraint cumulative(p_y, y_r, x_r, w);
constraint cumulative(p_x, x_r, y_r, l_max);

% symmetry breaking constraint
constraint symmetry_breaking_constraint(
  p_x[index] == 0 /\ p_y[index] == 0
);

% higher density on the left wrt the right
constraint symmetry_breaking_constraint(
  sum(i in CIRCUITS where p_x[i] <= w div 2)(area[i]) > sum(i in CIRCUITS where p_x[i] > w div 2)(area[i])
);

% Parameters to control the search heuristic and restart strategy
int: heuristic = 7;
int: restart = 3;

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

ann: search_ann_x_r = 
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

ann: search_ann_y_r = 
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

solve :: search_ann_x
      :: search_ann_y
      :: search_ann_x_r
      :: search_ann_y_r
      :: restart_ann
         minimize l;


output ["\(w) \(l)\n\(n)\n"]
    ++ ["\(x[i]) \(y[i]) \(p_x[i]) \(p_y[i])" 
        ++ if fix(rotation[i]) then " R" else "" endif
        ++ "\n" 
       | i in index_set(rotation)];