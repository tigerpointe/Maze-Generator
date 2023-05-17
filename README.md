# Maze Generator
## Copyright (c) 2023 TigerPointe Software, LLC

## Description
Writes a randomly generated maze to the console.

Implements a classic depth-first search algorithm.

A blank grid is produced by repeating the left and top cell content.

  +--
  :           (defines a 1x1 grid)

  +--+--+--
  :  :  :
  +--+--+--
  :  :  :     (defines a 3x3 grid)
  +--+--+--
  :  :  :

A terminal column is added on the right to close the rows.

A terminal row is added on the bottom to close the columns.

  +--+
  :  :        (defines a closed 1x1 grid)
  +--+

  +--+--+--+
  :  :  :  :
  +--+--+--+
  :  :  :  :  (defines a closed 3x3 grid)
  +--+--+--+
  :  :  :  :
  +--+--+--+

The depth-first search algorithm is defined as follows:

  - Accept a cell as a parameter (can be chosen randomly)
  - Mark the accepted cell as visited
  - While the accepted cell has remaining unvisited neighbors
    - Choose one of the unvisited neighbors
    - Remove the wall between the accepted cell and the chosen neighbor
    - Invoke the procedure recursively for the chosen neighbor

The algorithm guarantees at least one path through the completed maze.

## Make a Difference
If you enjoy this software, please consider donating to one of the following:

[American Cancer Society](https://www.cancer.org)

[National Brain Tumor Society](https://braintumor.org)