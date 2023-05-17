<#

.SYNOPSIS
Writes a randomly generated maze to the console in PowerShell.

.DESCRIPTION
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

.PARAMETER width
Specifies the number of horizontal cells to create.

.PARAMETER height
Specifies the number of vertical cells to create.

.INPUTS
None.

.OUTPUTS
A whole lot of fun.

.EXAMPLE
.\Write-Maze.ps1
Starts the program with the default options.

.EXAMPLE
.\Write-Maze.ps1 -width 25 -height 5
Starts the program with options for generating a 25x5 cell maze.

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
01.00 2023-May-17 Scott S. Initial release.

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/

#>
#Requires -Version 5.1

param
(
    [int]$width  = 16 # default number of horizontal cells to create
  , [int]$height = 8  # default number of vertical cells to create
)

# Sanity check
if ($width  -lt 1) { $width  = 1; }
if ($height -lt 1) { $height = 1; }
Clear-Host;
 
# Create a hash table to store the maze data
$maze = @{};

# Recursively walks the maze
function Walk-Maze {
  param(
      [int]$x # cell x-coordinate
    , [int]$y # cell y-coordinate
  )

  # Set the visited flag for the specified cell
  $maze[$y][$x].Visited = $true;

  # Get the neighboring cell references (if any exist)
  $neighbors = @();
  if ($x -gt 0)       { $neighbors += $maze[$y][$x - 1]; }
  if ($x -lt $width)  { $neighbors += $maze[$y][$x + 1]; }
  if ($y -gt 0)       { $neighbors += $maze[$y - 1][$x]; }
  if ($y -lt $height) { $neighbors += $maze[$y + 1][$x]; }

  # Shuffle the neighbors by sorting on a random value
  # (random sort orders produce the varied maze structures)
  $shuffled = ($neighbors | Sort-Object -Property { Get-Random });

  # Loop through each of the shuffled neighbors
  foreach ($neighbor in $shuffled)
  {

    # Skip processing if a neighbor has already been visited
    if ($neighbor.Visited) { continue; }

    # Check for a vertical neighbor (same x, different y)
    if ($neighbor.X -eq $x)
    {

      # Remove the shared wall (top of the greater y)
      if ($neighbor.Y -gt $y)
      {
        $neighbor.Top  = '+  ';
      }
      else
      {
        $maze[$y][$x].Top  = '+  ';
      }

    }

    # Check for a horizontal neighbor (same y, different x)
    if ($neighbor.Y -eq $y)
    {

      # Remove the shared wall (left of the greater x)
      if ($neighbor.X -gt $x)
      {
        $neighbor.Left = '   ';
      }
      else
      {
        $maze[$y][$x].Left = '   ';
      }

    }

    # Recursively walk the maze with the neighbor
    Walk-Maze -x $neighbor.X -y $neighbor.Y;

  } # end-foreach

}

# Initialize each data row
for ($y = 0; $y -lt $height; $y++)
{

  # Initialize each data column (cells y, x)
  $maze[$y] = @{};
  for ($x = 0; $x -lt $width; $x++)
  {
    $maze[$y][$x] = @{};
    $maze[$y][$x].Visited = $false;
    $maze[$y][$x].X       = $x;
    $maze[$y][$x].Y       = $y
    $maze[$y][$x].Left    = ':  ';
    $maze[$y][$x].Top     = '+--';
  }

  # Initialize the terminal column (not walked)
  $maze[$y][$width] = @{};
  $maze[$y][$width].Visited = $true;
  $maze[$y][$width].X       = $width;
  $maze[$y][$width].Y       = $y
  $maze[$y][$width].Left    = ':';
  $maze[$y][$width].Top     = '+';

}

# Initialize the terminal row (not walked)
$maze[$height] = @{};
for ($x = 0; $x -le $width; $x++)
{
  $maze[$height][$x] = @{}
  $maze[$height][$x].Visited = $true;
  $maze[$height][$x].X       = $x;
  $maze[$height][$x].Y       = $height;
  $maze[$height][$x].Left    = '';
  $maze[$height][$x].Top     = '+--';
}
$maze[$height][$width].Top     = '+';

# Choose a random cell and begin walking the maze
# (maze is a grid of cells with left and top walls)
Walk-Maze -x (Get-Random -Maximum $width) `
          -y (Get-Random -Maximum $height);

# Clear the maze entrance and exit walls
# (enter top-left, exit bottom-right)
$maze[0][0].Left = "   ";
$maze[$height - 1][$width].Left = " ";

# Write the completed maze to the console
$sb = [System.Text.StringBuilder]::new();
for ($y = 0; $y -le $height; $y++)
{
  for ($x = 0; $x -le $width; $x++)
  {
    [void]$sb.Append($maze[$y][$x].Top);
  }
  [void]$sb.AppendLine();
  for ($x = 0; $x -le $width; $x++)
  {
    [void]$sb.Append($maze[$y][$x].Left);
  }
  [void]$sb.AppendLine();
}
Write-Host -Object $sb.ToString();