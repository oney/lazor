# Lazor Project
Lazor group project for EN.540.635(Software Carpentry)


This program can automatically find solutions to the "Lasers" game on Android and IPhone. 

## Team members
* Fangchi Shao <fshao1@jhmi.edu>
*  Wan-Huang Yang <wyang47@jhu.edu>

## Directions to use
1. Prepare a Lazor board via a text file with a specific format (.bff). Some of the boards were pregenerated in the release that can be used. The way to create a board is described in the next section.

2. Save all .py files of the program along with the .bff files in the same folder or directory.

3. Load main.py in your python IDE.

4. Change the name of the .bff file in line #8 of the main.py to match with the board you want to sovle. For instance, "bff = BFF("numbered_6.bff")" means "numbered_6.bff" will be solved.

5. With some time, the program will output a txt file that contains the solution to the maze in both text tile and png image.

## BFF files
Board information will be saved into a .bff file, which will include the following information:

1. The starting grid along with different types of blocks representations:

 - x = no block allowed
 - o = blocks allowed
 - A = fixed reflect block
 - B = fixed opaque block
 - C = fixed refract block
 Note: Grid will start at top left being (0, 0) and step size is by half blocks. Thus, this leads to even numbers indicating the rows/columns between blocks, and odd numbers intersecting blocks.
 "GRID START" and "GRID STOP" will be used to locate the starting grid in the .bff file.
 
2. Specify the type and number of the blocks. 
- Use the "A", "B", and "C" to indicate the block type, followed with a space and integer number to indicate the number of the specific block type.
- For instance, "A 2" indicate 2 fixed reflect blocks.

3. Specify the laser.
- We specify the laser with "x, y, vx, vy" format.
- The line starts with "L" followed with the starting position and the direction.
- Starting position is in half increments, if the grid is 2 by 2, the half increment style will be 4 by 4.
- The direction of the laser can be -1, -1 or -1, 1, or 1, 1 or 1, -1.
- An example can be "L 2 7 1 -1"

4. Specify the points that we need the lazers to intersect.
- We specify the points that the lser will hit wiht the same half increment axis style.
- The line started with "P" followed by the x and y position.
- An example will be "P 3 0"

## Output the solution to the board.
The output will be in both txt file and png image, which will be saved as "solution.txt" and "solution.png" respectively.

To help understand the output png image, we used different colors to indicate different blocks:
- Pink = fixed reflect block
- Blue = fixed opaque block
- Yellow = fixed refract block
- Grey = no block

As an example, for solution.txt with the following grid:

A B A

o o o 

A C o


The png image will looks like:

![](/Solution_examples/solution.png)



 
      

