# Maze Generator
## Copyright (c) 2023 TigerPointe Software, LLC

## Description
Gets a randomly generated maze using PowerShell.

Implements a recursive depth-search algorithm to generate a maze.

  - Accept a cell as a parameter (first one can be chosen at random)
  - Mark the accepted cell as visited
  - While the accepted cell has remaining unvisited neighbors
    - Choose one of the unvisited neighbors
    - Remove the wall between the accepted cell and the chosen neighbor
    - Invoke the procedure recursively for the chosen neighbor

Please consider giving to cancer research.

    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
             |        |           |  |           |  |
    +  +--+  +  +  +  +  +--+--+  +  +  +--+--+--+  +
    |     |  |  |  |  |  |  |     |  |     |        |
    +  +  +--+  +  +  +  +  +  +--+  +--+  +  +  +  +
    |  |        |  |  |  |  |     |     |  |  |  |  |
    +  +--+--+--+  +  +  +  +--+  +  +--+  +  +  +--+
    |        |     |     |           |     |  |     |
    +--+  +--+  +--+--+--+  +--+--+--+  +--+--+--+  +
    |  |  |     |              |  |     |           |
    +  +  +  +--+--+--+--+--+  +  +  +--+  +--+--+  +
    |     |        |        |  |  |     |  |        |
    +  +--+--+--+  +  +--+  +  +  +--+  +  +  +--+--+
    |  |     |  |     |     |     |     |  |  |     |
    +  +  +  +  +--+--+  +--+--+--+  +--+  +  +--+  +
    |     |           |                    |         
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

## Make a Difference
If you enjoy this software, please consider donating to one of the following:

[American Cancer Society](https://www.cancer.org)

[National Brain Tumor Society](https://braintumor.org)