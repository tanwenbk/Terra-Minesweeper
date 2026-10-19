-----------
MINESWEEPER
-----------
Original Game made by Curt Johnson and Robert Donner in 1990

How To Play:
You can click a tile in the grid to reveal it, either revealing nothing, a number, or a mine. If it reveals a number, the number
represents how many 'mines' are around it, orthogonally or diagonally. Clicking a mine will instantly end your run. You can also
place a flag as a marker. Your goal is to reveal every cell that is not a mine, and in most cases you can deduce which tiles are
not mines logically. Revealing a blank tile represents zero mines surrounding it. Clicking an already revealed tile with an equal
number of mines as flags will reveal all surrounding tiles, which does have a chance of instantly ending your game.

You can change the grid size to up to 50 rows/columns, and up to 90% of the tiles can be mines.

Controls:
Left Click - Reveal Tile
Right Click - Place Flag
Space - Reset Board

You can change the number of rows, columns, and the percentage of mines on the board using the UI on the right.
There is also a box that is usually gray that turns green upon a win and red upon a lose.
Losing will also reveal every mine and false flag.

Creation Process:
I started by importing pygame and creating a 10x10 grid of buttons. I made the buttons activate a function when clicked that turned them red, and a different function for right clicking that turned them green. The surrounding cells were turned yellow.

Then, I made a const called MINES, set it to 10, and created a system to automatically place MINES amount of 'mines' around the grid, represented by purple colored tiles. I ensured that these 10 mines are not on the first clicked button nor do they surround the first click button, making sure the first pressed button is always a zero.

After that, I made a mine detection system and a lose/win condition that stops the player from playing if they reveal all non-mine spaces or if they reveal a mine. I also coded a system that automatically reveals all squares around a zero if a zero is revealed. I also made it so that if you click an already revealed square with an equal number of surrounding flags as its number, all the squares around the clicked square will reveal themselves (which may kill you if you place false flags!)

Next, I made a new class for input boxes and made the size of the grid and the percentage of tiles that are mines customizable, within limits. I mapped the individual squares to assets, depending on the state or the number.
I found the assets here: https://opengameart.org/content/minesweeper-esk-assets by FrostC.

I added touch-ups and formatting and the game was complete!

I used AI to help with debugging and deciphering functions and methods from the pygame function that were not made clear in the documentation, as well as to optimize broken or slow code.
