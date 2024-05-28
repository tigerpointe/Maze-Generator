#!/usr/bin/env python3
""" A Python module for generating and solving random mazes using JSON.
Implements a recursive depth-first search algorithm.
https://en.wikipedia.org/wiki/Maze_generation_algorithm
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

  +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    .   .   .   . | .   .   .   .   . |     .   .   . |           |
  +   +---+   +   +   +---+---+---+   +---+   +---+   +   +---+   +
  |   |       | .   . | .   .     | .   .   . |   | . |       |   |
  +---+   +---+---+---+   +   +   +---+---+---+   +   +---+   +   +
  |       | .   .   .   . | . |   | .   .   .   . | .   . |   |   |
  +   +---+   +---+---+---+   +---+   +---+---+   +---+   +   +---+
  |       | .   . |       | .   .   . | .   .   .     | . |       |
  +---+   +---+   +---+   +---+---+---+   +---+---+   +   +---+   +
  |       |     . | .   .   . |       | .   .   . |   | .   .   . |
  +   +---+---+   +   +---+   +---+   +---+---+   +---+---+---+   +
  |           | .   . |   | .   .   .   . |   | . | .   .   .   . |
  +---+---+   +---+---+   +   +---+---+   +   +   +   +---+---+---+
  |           |       |       |       | .   . | .   . |           |
  +   +---+---+   +   +---+---+   +   +---+   +---+---+---+---+   +
  |               |               |       | .   .   .   .   .   .
  +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from random import randrange, shuffle
import json


def get_maze(width=16, height=8):
    """ Gets a random maze as a JSON data string.
    Parameters
    width  : the width of the maze in cells
    height : the height of the maze in cells
    """

    # Initialize a grid by stacking rows and columns of dictionary cells
    # (includes an extra right closure column and a bottom closure row)
    grid = [[None] * (width + 1) for i in range(height + 1)]
    for y in range(height):
        for x in range(width):
            grid[y][x] = {
                'top': True,
                'left': True,
                'path': False,
                'visited': False
            }
        grid[y][width] = {
            'top': False,
            'left': True,
            'path': False,
            'visited': True
        }
    for x in range(width):
        grid[height][x] = {
            'top': True,
            'left': False,
            'path': False,
            'visited': True
        }
    grid[height][width] = {
        'top': False,
        'left': False,
        'path': False,
        'visited': True
    }

    # Remove the entrance and exit walls
    grid[0][0]['left'] = False
    grid[height - 1][width]['left'] = False

    def enter_cell(x, y):
        """ Enters a cell using a recursive depth-first search algorithm:
        Accept a cell as a parameter
        Mark the accepted cell as visited
        While the accepted cell has unvisited neighbors
        - Choose one of the remaining unvisited neighbors
        - Remove the wall between the accepted cell and the chosen neighbor
        - Recursively call the routine for the chosen neighbor
        Parameters
        x : the x-coordinate
        y : the y-coordinate
        """

        grid[y][x]['visited'] = True
        neighbors = []
        if x > 0:
            neighbors += [(x - 1, y)]
        if x < width:
            neighbors += [(x + 1, y)]
        if y > 0:
            neighbors += [(x, y - 1)]
        if y < height:
            neighbors += [(x, y + 1)]
        shuffle(neighbors)
        for (nx, ny) in neighbors:
            if grid[ny][nx]['visited']:
                continue
            if nx == x:
                grid[max(y, ny)][x]['top'] = False
            if ny == y:
                grid[y][max(x, nx)]['left'] = False
            enter_cell(nx, ny)

    # Choose a random cell and begin walking the grid
    enter_cell(randrange(width), randrange(height))
    return json.dumps(grid)


def set_maze_path(data=None):
    """ Sets a solution path for the maze data.
    Parameters
    data : the JSON maze data
    """

    # Load the JSON maze data
    grid = json.loads(data)
    width = len(grid[0]) - 1
    height = len(grid) - 1

    def test_path(x, y):
        """ Tests all of the maze paths using a recursive depth-first search
        algorithm until a solution has been found:
        Accept a cell as a parameter
        Mark the accepted cell as visited
        If the accepted cell is equal to the exit cell, return as solved
        Otherwise, while the accepted cell has unvisited, unwalled neighbors
        - Choose one of the remaining unvisited, unwalled neighbors
        - Recursively call the routine for the chosen neighbor until solved
        If no neighbors return as solved, the accepted cell is discarded
        Parameters
        x : the x-coordinate
        y : the y-coordinate
        """

        grid[y][x]['visited'] = True
        if (x == (width - 1)) and (y == (height - 1)):
            grid[y][x]['path'] = True
            return True
        neighbors = []
        if x > 0:
            neighbors += [(x - 1, y)]
        if x < width:
            neighbors += [(x + 1, y)]
        if y > 0:
            neighbors += [(x, y - 1)]
        if y < height:
            neighbors += [(x, y + 1)]
        for (nx, ny) in neighbors:
            if grid[ny][nx]['visited']:
                continue
            if (nx == x) and (grid[max(y, ny)][x]['top']):
                continue
            if (ny == y) and (grid[y][max(x, nx)]['left']):
                continue
            if not test_path(nx, ny):
                continue
            grid[y][x]['path'] = True
            return True
        return False

    # Reset the visited flags, and then begin testing all of the generated
    # paths, starting from the entrance, continuing until an exit is found
    for y in range(height):
        for x in range(width):
            grid[y][x]['visited'] = False
    _ = test_path(0, 0)
    return json.dumps(grid)


def write_maze(data=None):
    """ Writes the maze data as a printable string.
    Parameters
    data : the JSON maze data
    """

    # Load the JSON maze data
    grid = json.loads(data)
    width = len(grid[0]) - 1
    height = len(grid) - 1

    # Write the maze as a text string
    s = '\n  '
    c = ' '
    for y in range(height + 1):
        for x in range(width + 1):
            if grid[y][x]['top']:
                s += '+---'
            else:
                s += '+   '
        s += '\n  '
        for x in range(width + 1):
            if grid[y][x]['path']:
                c = '.'
            else:
                c = ' '
            if grid[y][x]['left']:
                s += '| ' + c + ' '
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

    data = get_maze(width, height)
    if unsolved:
        print(write_maze(data))
    if solved:
        data = set_maze_path(data)
        print(write_maze(data))


# Start the program interactively
if __name__ == '__main__':
    main(unsolved=False)
    input('  Press ENTER to Continue: ')
