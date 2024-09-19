#!/usr/bin/env python3
""" A minimalist Python module for generating random mazes.
History:
01.00 2024-Sep-15 Scott S. Initial release.

MIT License

Copyright (c) 2024 TigerPointe Software, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

If you enjoy this software, please do something kind for free.

  +   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
  |               |                   |               |           |
  +   +---+   +   +   +---+---+---+   +---+   +---+   +   +---+   +
  |   |       |       |           |           |   |   |       |   |
  +---+   +---+---+---+   +   +   +---+---+---+   +   +---+   +   +
  |       |               |   |   |               |       |   |   |
  +   +---+   +---+---+---+   +---+   +---+---+   +---+   +   +---+
  |       |       |       |           |               |   |       |
  +---+   +---+   +---+   +---+---+---+   +---+---+   +   +---+   +
  |       |       |           |       |           |   |           |
  +   +---+---+   +   +---+   +---+   +---+---+   +---+---+---+   +
  |           |       |   |               |   |   |               |
  +---+---+   +---+---+   +   +---+---+   +   +   +   +---+---+---+
  |           |       |       |       |       |       |           |
  +   +---+---+   +   +---+---+   +   +---+   +---+---+---+---+   +
  |               |               |       |                       |
  +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+   +

A 3x3 Walk-through Example of this Module

An initial 3x3 "tops" grid of repeating "+---" cells:

  +---+---+---+           add an extra "+" right closure cell to each row
  +---+---+---+
  +---+---+---+
  +---+---+---+           add an extra bottom closure row (same as others)

An initial 3x3 "lefts" grid of repeating "|   " cells:

  |   |   |   |           add an extra "|" right closure cell to each row
  |   |   |   |
  |   |   |   |
                          add an extra bottom closure row of empty strings

An initial 3x3 "visited" grid of repeating "False" cells:

  False False False True  add an extra "True" right closure cell to each row
  False False False True
  False False False True
  True  True  True  True  add an extra bottom closure row of "True" values

Alternated initial 3x3 "tops" and "lefts" when "joined" together:

  +---+---+---+           alternating "+" and "|" right closure column
  |   |   |   |
  +---+---+---+
  |   |   |   |           grid body with alternating "tops" and "lefts" rows
  +---+---+---+
  |   |   |   |
  +---+---+---+           trailing "tops" closure row
                          trailing "lefts" closure row (empty strings)

This module implements a recursive depth-first search algorithm:
https://en.wikipedia.org/wiki/Maze_generation_algorithm

  Accept a cell as a parameter
  Mark the accepted cell as visited
  While the accepted cell has unvisited neighbors
  - Choose one of the remaining unvisited neighbors
  - Remove the wall between the accepted cell and the chosen neighbor
  - Recursively call the routine for the chosen neighbor

Every cell is randomly visited one time, allowing for one solution path.
Neighbors are randomly walked until there are no more unvisited neighbors.
The shared "tops" of vertically aligned neighbors (same x) are removed.
The shared "lefts" of horizontally aligned neighbors (same y) are removed.
"max()" returns the bottom-most/right-most shared wall between two cells.
After all neighbors have been visited for a chosen cell, backtracking occurs.
Bounds checks on the -1/+1 neighbor cell coordinates are not necessary.
An index of -1 for any x or y coordinate references the trailing closure.
An overflow of +1 for any x or y coordinate references the trailing closure.
All trailing closures are initialized as "visited" and therefore not walked.
The first and last cell "tops" are removed to create the entrance and exit.
The finished maze is returned as a multiline string, indented with spaces.

Sample finished 3x3 random maze returned (and "printed") by this module:

  +   +---+---+
  |           |
  +   +---+   +
  |       |   |
  +---+---+   +
  |           |
  +---+---+   +

  Press ENTER to Continue:

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from random import randrange, shuffle


def get_maze(w=16, h=8):
    tops = [(['+---'] * w) + ['+'] for _ in range(h + 1)]
    lefts = [(['|   '] * w) + ['|'] for _ in range(h)] + [[''] * (w + 1)]
    visited = [([False] * w) + [True] for _ in range(h)] + [[True] * (w + 1)]

    def walk_cell(x, y):
        visited[y][x] = True
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        shuffle(neighbors)
        for (nx, ny) in neighbors:
            if visited[ny][nx]:
                continue
            if nx == x:
                tops[max(ny, y)][x] = '+   '
            elif ny == y:
                lefts[y][max(nx, x)] = '    '
            walk_cell(nx, ny)

    walk_cell(randrange(w), randrange(h))
    tops[0][0] = tops[h][w - 1] = '+   '

    s = ''
    for (zt, zl) in zip(tops, lefts):
        s += ''.join(['\n  '] + zt + ['\n  '] + zl)
    return s


if __name__ == '__main__':
    print(get_maze())
    input('  Press ENTER to Continue: ')
