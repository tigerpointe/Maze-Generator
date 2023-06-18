#!/usr/bin/env python3
""" A Python replacement module for writing mazes with Unicode box characters.

IMPORTANT:  Be sure to view using a true Unicode compatible monospace font.

In the original writer, a "+" connector is used to delimit the grid cells.
Each segment of a connector can be thought of as having the compass directions
of North, South, West, and East.

         N
       W + E
         S

The walls of the neighbor cells determine whether a particular segment of the
connector is displayed.  Each compass direction segment can be assigned a
bitmask value.

N = (x, y - 1).left += 8
S = (x, y).left     += 4
W = (x - 1, y).top  += 2
E = (x, y).top      += 1

The bitmask combinations can now be mapped to Unicode box characters.

   N S W E Character
00 0 0 0 0  
01 0 0 0 1 ╶
02 0 0 1 0 ╴
03 0 0 1 1 ─
04 0 1 0 0 ╷
05 0 1 0 1 ┌
06 0 1 1 0 ┐
07 0 1 1 1 ┬
08 1 0 0 0 ╵
09 1 0 0 1 └
10 1 0 1 0 ┘
11 1 0 1 1 ┴
12 1 1 0 0 │
13 1 1 0 1 ├
14 1 1 1 0 ┤
15 1 1 1 1 ┼

A mapping string can be derived by translating the bitmask horizontally.

            0000000000111111 
            0123456789012345
Squared Box: ╶╴─╷┌┐┬╵└┘┴│├┤┼

Select a connector by using the bitmask as an index into the mapping string.

History:
01.00 2023-Jun-19 Scott S. Initial release.

MIT License

Copyright (c) 2023 TigerPointe Software, LLC

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

  ╶───────────┬───────────────────────┬───────────┬───────────────┐
    .   .   . │         .   .   .   . │           │               │
  ╷   ┌───┐   └───────┐   ┌───────┐   └───┐   ╷   ╵   ┌───────╴   │
  │   │   │ .   .   . │ . │       │ .   . │   │       │ .   .   . │
  │   │   └───────┐   ╵   │   ╶───┼───╴   ├───┴───────┘   ┌───┐   │
  │   │           │ .   . │ .   . │ .   . │ .   .   .   . │   │ . │
  │   │   ╶───┐   └───────┤   ╷   ╵   ┌───┘   ┌───┬───────┘   │   │
  │   │       │ .   .   . │ . │ .   . │     . │   │ .   .   . │ . │
  │   └───────┤   ╶───┐   │   ├───────┴───╴   │   ╵   ┌───┐   │   │
  │           │ .   . │ . │ . │         .   . │ .   . │   │ . │ . │
  ├───────╴   ├───╴   │   │   ├───────╴   ┌───┤   ┌───┘   │   ╵   │
  │           │ .   . │ . │ . │ .   .   . │   │ . │       │ .   . │
  ├───┬───────┤   ┌───┤   ╵   │   ╶───┬───┘   │   │   ╶───┴───┬───┤
  │   │       │ . │   │ .   . │ .   . │       │ . │     .   . │   │
  │   ╵   ╷   ╵   ╵   └───────┴───╴   │   ╶───┘   └───╴   ╷   ╵   ╵
  │       │     .   .   .   .   .   . │         .   .   . │ .   .
  └───────┴───────────────────────────┴───────────────────┴───────╴
  * YOU MUST USE A MONOSPACE UNICODE COMPATIBLE FONT TO VIEW THE ABOVE MAZE

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

import random_maze_solver_json as rmsj
import json


def write_maze_box(data=None):
    """ Writes the maze data as a printable string (Unicode box characters).
    Parameters
    data : the JSON maze data
    """

    # Load the JSON maze data
    grid = json.loads(data)
    width = len(grid[0]) - 1
    height = len(grid) - 1

    # Define the bitmask mapping string of box characters
    box = ' ╶╴─╷┌┐┬╵└┘┴│├┤┼'

    # Remove the entrance and exit walls
    grid[0][0]['left'] = False
    grid[height - 1][width]['left'] = False

    # Write the maze as a text string
    s = '\n  '
    c = ' '
    for y in range(height + 1):
        for x in range(width + 1):
            mask = 0
            if y > 0:
                if grid[y - 1][x]['left']:
                    mask += 8
            if grid[y][x]['left']:
                mask += 4
            if x > 0:
                if grid[y][x-1]['top']:
                    mask += 2
            if grid[y][x]['top']:
                mask += 1
            b = box[mask]
            if grid[y][x]['top']:
                s += b + '───'
            else:
                s += b + '   '
        s += '\n  '
        for x in range(width + 1):
            if grid[y][x]['path']:
                c = '.'
            else:
                c = ' '
            if grid[y][x]['left']:
                s += '│ ' + c + ' '
            else:
                s += '  ' + c + ' '
        s += '\n  '
    return s


def main(width=16, height=8, unsolved=True, solved=True):
    """ Defines the main entry point of the program.
    Parameters
    width    : the width of the maze in cells
    height   : the height of the maze in cells
    unsolved : a flag to show the unsolved maze
    solved   : a flag to show the solved maze
    """

    data = rmsj.get_maze(width, height)
    if unsolved:
        print(write_maze_box(data))
    if solved:
        data = rmsj.set_maze_path(data)
        print(write_maze_box(data))


# Start the program interactively
if __name__ == '__main__':
    main(unsolved=False)
    input('  Press ENTER to Continue: ')
