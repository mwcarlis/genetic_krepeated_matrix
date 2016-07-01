# genetic_krepeated_matrix
A genetic algorithm to generate a matrix out of a finite set of values that does not have any value repeated k times in a row or in a column.

To construct a matrix n*m using a finite set of values
(i.e: [0, 1, 2]) such that there are no values repeated k times in a row in horizontal/vertical.

n=3       m = 3     k=3
  GOOD:-   |   - BAD:
[0, 1, 2]--|--[1, 1, 1]
[2, 0, 1]--|--[2, 2, 2]
[0, 1, 2]--|--[0, 0, 0]

Representation of GOOD:  (I'm using a single list to represent the Matrix)
[0, 1, 2, 2, 0, 1, 0, 1, 2]
