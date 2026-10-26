Note: This is the README for WEEK 1, not for Prep Week 3.
-
MINESWEEPER VARIANTS
-
Original Game made by Curt Johnson and Robert Donner in 1990

How To Play: You can click a tile in the grid to reveal it, either revealing nothing, a number, or a mine.
If it reveals a number, the number represents how many 'mines' are around it, orthogonally or diagonally.
Clicking a mine will instantly end your run. You can also place a flag as a marker. Your goal is to reveal
every cell that is not a mine, and in most cases you can deduce which tiles are not mines logically. Revealing
a blank tile represents zero mines surrounding it. Clicking an already revealed tile with an equal number of 
mines as flags will reveal all surrounding tiles, which does have a chance of instantly ending your game.

This program is a twist on Minesweeper where there are a ton of different mine types that affect the safe number
cells nearby in different ways. There are regular mines, double mines, triple mines, negative versions of each of
those, and mega mines which increases every tile in a 5x5 radius by 1 instead of the regular 3x3 radius.

You can change the grid size to up to 50 rows/columns, and up to 90% of the tiles can be mines.

Controls: 
Left Click - Reveal Tile, Reveal Surrounding Tiles
Right Click - Place Flag, Change Flag Type
Space - Reset Board

You can change the number of rows, columns, and the percentage of mines on the board using the UI on the right.
There is also a box that is usually gray that turns green upon a win and red upon a lose. Losing will also reveal
every mine and false flag.


Creation Process:

At the start of the week, I created lots of assets on lapse, because with all of the unique variants there are tons
of different combinations that can make the clue number very high.
I did lots of work making assets on Lapse, which can be found here: https://lapse.hackclub.com/user/@tan1

Afterwards, once I made enough assets, I coded the double mine. The numbers go up to 16, and at this point they were
unable to be turned off.

I made more assets for numbers up to 24 and down to -24, and then began coding triple mines, and negative mines.
After making the first mine variation, it became less difficult to add additional ones, so I was able to code 5 of the
six variants by this time.

Next, I added toggles so you can control which variants you want on and which ones you want off. This took me longer
than expected, I had to create an entire new class for buttons (along with custom button sprites!)

Finally, today and yesterday I added mega mines, and made assets since numbers could now go up to 40 (although
I wasnt able to get one that high), and added touch ups and sliders and optimized the code until the project was complete!


I used AI to help with debugging and deciphering functions and methods from the pygame class that were not made clear in
the documentation, as well as to optimize broken or slow code.
