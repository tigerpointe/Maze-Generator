# Maze Generator
## Copyright (c) 2023 TigerPointe Software, LLC

## Description
Gets a randomly generated maze using PowerShell.

Implements a recursive depth-first search algorithm to generate a maze.

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

## Update (2023-Jun-19)
A total of two new PowerShell and Python scripts were added to generate, solve, and output written mazes.  If you know one language, and would like to learn the other, the Python script is a line-by-line port of the PowerShell code, respecting the best practices and conventions of each environment.

These scripts are by far some of the smallest and most easy to understand maze generators available.  The updated scripts separate the generator, solver, and writer features into different methods.  A simple JSON string is used as an intermediate data format for communicating between these methods.  Each script can be used as an independent module and does not require an installer.

The included writer methods output ASCII text for portability.  If you are a developer, you can save the JSON markup and pass it to your own custom writer method (for example, one that outputs graphics or Unicode box characters).  These scripts were only intended as simple tools to illustrate complicated concepts.

BONUS SCRIPT:  A sample Unicode box writer module is now included for Python.

In general, the Python script runs faster, but PowerShell allows for much greater levels of recursion.

The original PowerShell script (which only generates strings) is still included in the project for historical purposes.

## Make a Difference
If you enjoy this software, please consider donating to one of the following:

[American Cancer Society](https://www.cancer.org)

[National Brain Tumor Society](https://braintumor.org)