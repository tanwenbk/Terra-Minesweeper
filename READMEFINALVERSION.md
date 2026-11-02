Note: This is the README for WEEK 2, not for Prep Week 3 nor Week 1.
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
cells nearby in different ways. There are regular mines, double mines, triple mines, half mines, negative versions
of each of those (besides the half mines), mega mines which increases every tile in a 5x5 radius by 1 instead of
the regular 3x3 radius, and square root mines that can result in imaginary numbers.

You can change the grid size to up to 50 rows/columns, and up to 90% of the tiles can be mines.
Sliders underneath each main variant determines the chance of a specific variant spawning.

Controls: 
Left Click - Reveal Tile, Reveal Surrounding Tiles
Right Click - Place Flag, Change Flag Type
Space - Reset Board

You can change the number of rows, columns, mine variant weight, and the percentage of mines on the board using the
UI on the right. There is also a box that is usually gray that turns green upon a win and red upon a lose. Losing will
also reveal every mine and false flag.


Creation Process:

As more mine variants are created, the amount of assets needed for the combinations of possible mines being made grows
exponentially. You can see in the spritesheet I originally planned to add an 'anti-mine', which was drawn as a mine with
a happy face (near the top left). This mine would have to be revealed in order to win, and doesn't increase the normal
mine count, but instead a side mine count that would have been represented by a symbol or a letter. However, this created
way too many possibilities and I was already pushing the limit on logging time with lapse...

I spent around 3.5 hours this week making assets using Lapse, although it was spread out throughout the week.

I started by making square root mines, which can trick you in ways like seeing a 2 which is actually 4 mines, with one of
them being a square root mine. 

Next, I made an inclusive total mine count, and an exclusive mine count for each mine which shows how many of each mine are
remaining on the board.

Around this time, I also created a timer for players that tracks how long they have been playing that run.

Afterwards, I made half mines, created a How To Play screen, touched up the UI, added weighting to individual mines,
and the game was complete!


I used AI to help with debugging and deciphering functions and methods from the pygame class that were not made clear in
the documentation, as well as to optimize broken or slow code.
