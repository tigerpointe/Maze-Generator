<#

.SYNOPSIS
Gets a randomly generated maze using PowerShell.

.DESCRIPTION
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

.PARAMETER width
Specifies the maze width in cells.

.PARAMETER height
Specifies the maze height in cells.

.PARAMETER margin
Specifies the left margin in characters.

.INPUTS
None.

.OUTPUTS
The maze as a string.

.EXAMPLE
.\Get-RandomMaze.ps1 -width 20 -height 5
Gets a random maze of 20 cells wide and 5 cells high.

.EXAMPLE
.\Get-RandomMaze.ps1 -margin 4 | Out-File -FilePath .\out.txt -Encoding utf8
Gets a random maze with a left margin of 4 characters.
The output can be redirected or piped to an output file for printing.

.NOTES
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

History:
01.00 2023-May-20 Scott S. Initial release.

.LINK
https://en.wikipedia.org/wiki/Maze_generation_algorithm

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/

#>

# Accept width, height and margin from console or use defaults
param ([int]$width = 16, [int]$height = 8, [int]$margin = 0)

# Makes the maze, returns a string
# (commas force values as repeating list elements)
function Make-Maze
{
  param ([int]$w, [int]$h)

  # Grid of visited flags, ex. 3x3 cells
  #   0001
  #   0001  (includes extra right, bottom closures)
  #   0001
  #   1111
  $vis = @();
  for ($i = 0; $i -lt $h; $i++)
  {
    $tmp =  ,0 * $w;
    $tmp += ,1;
    $vis += ,$tmp;
  }
  $tmp =  ,1 * ($w + 1);
  $vis += ,$tmp;

  # Grid of vertical walls, ex. 3x3 cells
  #    |  |  |  |
  #    |  |  |  |  (includes extra right closures)
  #    |  |  |  |
  #                (bottom has no vertical walls)
  $ver = @();
  for ($i = 0; $i -lt $h; $i++)
  {
    $tmp =  ,'|  ' * $w;
    $tmp += ,'|';
    $ver += ,$tmp;
  }
  $tmp =  ,'' * ($w + 1);
  $ver += ,$tmp;

  # Grid of horizontal walls, ex. 3x3 cells
  #    +--+--+--+
  #    +--+--+--+  (includes extra right, bottom closures)
  #    +--+--+--+
  #    +--+--+--+
  $hor = @();
  for ($i = 0; $i -le $h; $i++)
  {
    $tmp =  ,'+--' * $w;
    $tmp += ,'+';
    $hor += ,$tmp;
  }

  # Recursively walks grid for cell at x and y
  function Walk-Grid
  {
    param ([int]$x, [int]$y)

    # Mark cell as visited
    $vis[$y][$x] = 1;

    # Get direct neighbors (left, right, top, bottom), if exist
    $d = @();
    if ($x -gt 0)  { $d += ,@(($x - 1), $y); }
    if ($x -lt $w) { $d += ,@(($x + 1), $y); }
    if ($y -gt 0)  { $d += ,@($x, ($y - 1)); }
    if ($y -lt $h) { $d += ,@($x, ($y + 1)); }

    # Randomly sort and loop through neighbors
    $d = ($d | Sort-Object -Property { Get-Random });
    foreach ($dd in $d)
    {

      # Get current neighbor x and y
      $xx = $dd[0];
      $yy = $dd[1];

      # Skip, if already visited
      if ($vis[$yy][$xx] -ne 0) { continue; }

      # Same x, different y, remove connecting horizontal wall
      if ($xx -eq $x)
      {
        $my = (@($y, $yy) | Measure-Object -Maximum).Maximum;
        $hor[$my][$x] = '+  ';
      }

      # Same y, different x, remove connecting vertical wall
      if ($yy -eq $y)
      {
        $mx = (@($x, $xx) | Measure-Object -Maximum).Maximum;
        $ver[$y][$mx] = '   ';
      }

      #  Recursively walk grid for neighbor
      Walk-Grid -x $xx -y $yy;

    } # end-foreach
  } # end-function

  # Recursively walk grid for random cell
  Walk-Grid -x (Get-Random -Maximum $w) `
            -y (Get-Random -Maximum $h);

  # Remove entrance and exit walls
  $ver[0][0] = '   ';
  $ver[$h - 1][$w] = ' ';

  # Combine all horizonal and vertical walls
  $s = '';
  for ($i = 0; $i -le $h; $i++)
  {
    $s += ' ' * $margin;
    $s += ($hor[$i] -join '') + "`n";
    $s += ' ' * $margin;
    $s += ($ver[$i] -join '') + "`n";
  }
  return $s;

} # end-function

# Sanity check
if ($width  -lt 1) { $width  = 1; }
if ($height -lt 1) { $height = 1; }
if ($margin -lt 0) { $margin = 0; }

# Make maze for specified width and height
Make-Maze -w $width -h $height;