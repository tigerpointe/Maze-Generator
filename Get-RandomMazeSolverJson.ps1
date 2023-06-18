<#

.SYNOPSIS
A PowerShell module for generating and solving random mazes using JSON.

.DESCRIPTION
Implements a recursive depth-first search algorithm.

.PARAMETER width
Specifies the maze width in cells.

.PARAMETER height
Specifies the maze height in cells.

.PARAMETER unsolved
When present, shows the unsolved maze.

.PARAMETER solved
When present, shows the solved maze.

.INPUTS
None.

.OUTPUTS
The maze as a string.

.EXAMPLE
.\Get-RandomMazeSolverJson -width 20 -height 5 -unsolved
Gets a random unsolved maze of 20 cells wide and 5 cells high.

.EXAMPLE
.\Get-RandomMazeSolverJson -unsolved -solved
Gets a random maze which includes both unsolved and solved instances.

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

History:
01.00 2023-Jun-19 Scott S. Initial release.

.LINK
https://en.wikipedia.org/wiki/Maze_generation_algorithm

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/

#>
#Requires -Version 5.1

param
(
    [int]$width  = 16 # defines the default maze width
  , [int]$height = 8  # defines the default maze height
  , [switch]$unsolved # defines the show unsolved maze switch
  , [switch]$solved   # defines the show solved maze switch
)

function Get-Maze
# Gets a random maze as a JSON data string.
{
  param
  (
      [int]$width  = 16 # the width of the maze in cells
    , [int]$height = 8  # the height of the maze in cells
  )

  # Initialize a grid by stacking rows and columns of dictionary cells
  # (includes an extra right closure column and a bottom closure row)
  $grid = [object[]]::new($height + 1);
  for ($y = 0; $y -lt $height; $y++)
  {
    $grid[$y] = [object[]]::new($width + 1);
    for ($x = 0; $x -lt $width; $x++)
    {
      $grid[$y][$x] = @{
        Top     = $true
        Left    = $true
        Path    = $false
        Visited = $false
      }
    }
    $grid[$y][$width] = @{
      Top     = $false
      Left    = $true
      Path    = $false
      Visited = $true
    }
  }
  $grid[$height] = [object[]]::new($width + 1);
  for ($x = 0; $x -lt $width; $x++)
  {
    $grid[$height][$x] = @{
      Top     = $true
      Left    = $false
      Path    = $false
      Visited = $true
    }
  }
  $grid[$height][$width] = @{
    Top     = $false
    Left    = $false
    Path    = $false
    Visited = $true
  }

  function Enter-Cell
  # Enters a cell using a recursive depth-first search algorithm:
  # Accept a cell as a parameter
  # Mark the accepted cell as visited
  # While the accepted cell has unvisited neighbors
  # - Choose one of the remaining unvisited neighbors
  # - Remove the wall between the accepted cell and the chosen neighbor
  # - Recursively call the routine for the chosen neighbor
  {
    param
    (
        [int]$x # the x-coordinate
      , [int]$y # the y-coordinate
    )
    $grid[$y][$x].Visited = $true;
    $neighbors = @();
    if ($x -gt 0)       { $neighbors += ,@(($x - 1), $y); }
    if ($x -lt $width)  { $neighbors += ,@(($x + 1), $y); }
    if ($y -gt 0)       { $neighbors += ,@($x, ($y - 1)); }
    if ($y -lt $height) { $neighbors += ,@($x, ($y + 1)); }
    $neighbors = ($neighbors | Sort-Object -Property { Get-Random });
    foreach ($n in $neighbors)
    {
      $nx = $n[0];
      $ny = $n[1];
      if ($grid[$ny][$nx].Visited) { continue; }
      if ($nx -eq $x)
      {
        $my = [int](@($y, $ny) | Measure-Object -Maximum).Maximum;
        $grid[$my][$x].Top = $false;
      }
      if ($ny -eq $y)
      {
        $mx = [int](@($x, $nx) | Measure-Object -Maximum).Maximum;
        $grid[$y][$mx].Left = $false;
      }
      Enter-Cell -x $nx -y $ny;
    }
  }

  # Choose a random cell and begin walking the grid
  Enter-Cell -x (Get-Random -Maximum $width) `
             -y (Get-Random -Maximum $height);
  return (ConvertTo-Json -InputObject $grid);

}

function Set-MazePath
# Sets a solution path for the maze data.
{
  param
  (
      [string]$data # the JSON maze data
  )
  
  # Load the JSON maze data
  $grid   = [object[]](ConvertFrom-Json -InputObject $data);
  $width  = ($grid[0].Length - 1);
  $height = ($grid.Length - 1);

  function Test-Path
  # Tests all of the maze paths using a recursive depth-first search
  # algorithm until a solution has been found:
  # Accept a cell as a parameter
  # Mark the accepted cell as visited
  # If the accepted cell is equal to the exit cell, return as solved
  # Otherwise, while the accepted cell has unvisited, unwalled neighbors
  # - Choose one of the remaining unvisited, unwalled neighbors
  # - Recursively call the routine for the chosen neighbor until solved
  # If no neighbors return as solved, the accepted cell is discarded
  {
    param
    (
        [int]$x # the x-coordinate
      , [int]$y # the y-coordinate
    )
    $grid[$y][$x].Visited = $true;
    if (($x -eq ($width - 1)) -and ($y -eq ($height - 1)))
    {
      $grid[$y][$x].Path = $true;
      return $true;
    }
    $neighbors = @();
    if ($x -gt 0)       { $neighbors += ,@(($x - 1), $y); }
    if ($x -lt $width)  { $neighbors += ,@(($x + 1), $y); }
    if ($y -gt 0)       { $neighbors += ,@($x, ($y - 1)); }
    if ($y -lt $height) { $neighbors += ,@($x, ($y + 1)); }
    foreach ($n in $neighbors)
    {
      $nx = $n[0];
      $ny = $n[1];
      if ($grid[$ny][$nx].Visited) { continue; }
      if ($nx -eq $x)
      {
        $my = [int](@($y, $ny) | Measure-Object -Maximum).Maximum;
        if ($grid[$my][$x].Top) { continue; }
      }
      if ($ny -eq $y)
      {
        $mx = [int](@($x, $nx) | Measure-Object -Maximum).Maximum;
        if ($grid[$y][$mx].Left) { continue; }
      }
      if (-not (Test-Path -x $nx -y $ny)) { continue; }
      $grid[$y][$x].Path = $true;
      return $true;
    }
    return $false;
  }

  # Reset the visited flags, and then begin testing all of the generated
  # paths, starting from the entrance, continuing until an exit is found
  for ($y = 0; $y -lt $height; $y++)
  {
    for ($x = 0; $x -lt $width; $x++)
    {
      $grid[$y][$x].Visited = $false;
    }
  }
  $null = (Test-Path -x 0 -y 0);
  return (ConvertTo-Json -InputObject $grid);

}

function Write-Maze
# Writes the maze data as a printable string.
{
  param
  (
      [string]$data # the JSON maze data
  )

  # Load the JSON maze data
  $grid   = [object[]](ConvertFrom-Json -InputObject $data);
  $width  = ($grid[0].Length - 1);
  $height = ($grid.Length - 1);

  # Remove the entrance and exit walls
  $grid[0][0].Left = $false;
  $grid[$height - 1][$width].Left = $false;

  # Write the maze as a text string
  $s = "`n  ";
  $c = " ";
  for ($y = 0; $y -le $height; $y++)
  {
    for ($x = 0; $x -le $width; $x++)
    {
      if ($grid[$y][$x].Top) { $s += "+---"; } else { $s += "+   "; }
    }
    $s += "`n  ";
    for ($x = 0; $x -le $width; $x++)
    {
      if ($grid[$y][$x].Path) { $c  = ".";     } else { $c  = " ";     }
      if ($grid[$y][$x].Left) { $s += "| $c "; } else { $s += "  $c "; }
    }
    $s += "`n  ";
  }
  return $s;

}

function Start-Main
# Defines the main entry point of the program.
{
  param
  (
      [int]$width  = 16 # the width of the maze in cells
    , [int]$height = 8  # the height of the maze in cells
    , [switch]$unsolved # a flag to show the unsolved maze
    , [switch]$solved   # a flag to show the solved maze
  )

  $maze = "";
  $data = (Get-Maze -width $width -height $height);
  if ($unsolved.IsPresent)
  {
    $maze += (Write-Maze -data $data);
  }
  if ($solved.IsPresent)
  {
    $data =  (Set-MazePath -data $data);
    $maze += (Write-Maze -data $data);
  }
  Write-Output -InputObject $maze;

}

# Start the program interactively
try
{
  if (($unsolved.IsPresent) -or ($solved.IsPresent))
  {
    Start-Main -width $width -height $height `
               -unsolved:$unsolved -solved:$solved;
  }
  else
  {
    Start-Main -width $width -height $height -solved;
  }
  Read-Host -Prompt "  Press ENTER to Continue";
}
catch
{
  Write-Error -Message $_.Exception.Message;
}