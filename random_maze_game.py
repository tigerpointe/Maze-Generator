﻿#!/usr/bin/env python3
""" A Python module for interactively playing randomly generated mazes.

Copy this module into the same folder as random_maze_solver_json.py

History:
01.00 2024-May-25 Scott S. Initial release.

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

  Press the arrow keys to move, escape to quit.
  
  +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    .             |                   |               |           |
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
  |               |               |       |                      
  +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

# Requires:  pip install pynput
# (using a keypress library improves the game playability over text inputs)
from pynput.keyboard import Key, Listener
import json
import os
import random_maze_solver_json as rmsj


def clear():
    """Clears the screen, works across all platforms."""
    if (os.name == 'nt'):
        os.system('cls')   # Microsoft Windows
    else:
        os.system('clear')  # All others (posix)
    print('\n  Press the arrow keys to move, escape to quit.')


def play(width=16, height=8):
    """ Starts the gameplay.
    Parameters
    width  : the width of the maze in cells
    height : the height of the maze in cells
    """

    # Create a new randomly generated maze
    grid = json.loads(rmsj.get_maze(width, height))

    # Initialize the player's coordinates
    px = 0
    py = 0

    # Show the player's initial position in the maze
    grid[py][px]['path'] = True
    clear()
    print(rmsj.write_maze(json.dumps(grid)), end='')

    def save_game():
        """ Saves the game to a file."""

        # Save the JSON grid data to a file
        file = os.path.basename(__file__) + '.txt'
        f = open(file, 'w')
        f.write(json.dumps(grid))
        f.close()
        print('Game saved:', file, '\n  ', end='')
        return True

    def reload_game():
        """ Reloads the game from a file."""

        # Allow the grid variables to be updated in the parent scope
        nonlocal grid, width, height
        nonlocal px, py

        # Reload the JSON grid data from a file
        file = os.path.basename(__file__) + '.txt'
        if (os.path.isfile(file)):

            # Read the file contents
            f = open(file, 'r')
            grid = json.loads(f.read())
            f.close()

            # Set the grid variables (a found path breaks the nested loops)
            width = len(grid[0]) - 1
            height = len(grid) - 1
            for y in range(height):
                for x in range(width):
                    if (grid[y][x]['path']):
                        px = x  # found player's x-coordinate
                        py = y  # found player's y-coordinate
                        break
                else:
                    continue
                break

            # Show the player's reloaded position in the maze
            clear()
            print(rmsj.write_maze(json.dumps(grid)), end='')
            print('Game reloaded:', file, '\n  ', end='')

        else:
            print('File not found:', file, '\n  ', end='')
        return True

    def on_press(key):
        """Handles the keypress event.
        PARAMETERS:
        key : the pressed key
        """

        # Allow the player's coordinates to be updated in the parent scope
        nonlocal px, py

        # Save or reload the game
        if (hasattr(key, 'char')):
            if (key.char == 's'):
                return save_game()  # return the save status
            elif (key.char == 'r'):
                return reload_game()  # return the reload status

        # Clear the player's current position in the maze
        grid[py][px]['path'] = False

        # Update the player coordinates based on the pressed key
        if (key == Key.esc):
            print('Game stopped.')
            return False  # stop playing
        elif (key == Key.left):
            if (px > 0) and (not grid[py][px]['left']):
                px = px - 1  # move left
        elif (key == Key.right):
            if (px < (width - 1) and (not grid[py][px + 1]['left'])):
                px = px + 1  # move right
        elif (key == Key.up):
            if (py > 0) and (not grid[py][px]['top']):
                py = py - 1  # move up
        elif (key == Key.down):
            if (py < (height - 1)) and (not grid[py + 1][px]['top']):
                py = py + 1  # move down

        # Show the player's updated position in the maze
        grid[py][px]['path'] = True
        clear()
        print(rmsj.write_maze(json.dumps(grid)), end='')

        # Determine whether the player has found the exit
        if (px == (width - 1)) and (py == (height - 1)):
            print('CONGRATULATIONS!  You successfully solved the maze.')
            return False  # exit found, stop playing
        return True  # continue playing

    # Listen for keypresses until false is returned
    with Listener(on_press=on_press, suppress=True) as lstn:
        lstn.join()


# Start the program interactively
if __name__ == '__main__':
    play()
    input('  Press ENTER to Continue: ')