# Minesweeper Assets - FrostC - https://opengameart.org/content/minesweeper-esk-assets
# 12 Assets are by FrostC. (1-8, mine, flag, blank square, filled square)
# The rest were created by me and logged using lapse

import pygame as pg
import random

pg.display.set_caption("Tan's Minesweeper")

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
textfont = pg.font.SysFont("Arial", 32)
pg.key.set_repeat(400, 40)

rows = 10
cols = 10
mine_percentage = 10
minesSet = False
status = None           # None, "win", or "lose"
mines = 0

# (row, col) of each special tile on the sheet
BLANK = (2, 0)
UNREVEALED = (2, 1)
FALSEFLAG = (2, 7)

# convert_alpha must come after set_mode
image = pg.image.load('minesweepervariants.png').convert_alpha()

tile_size = 45          # updated whenever the grid is rebuilt
tile_cache = {}

# Addresses for assets in the image
numbers = [(5,3),(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),  # 0-8
                 (3,6),(3,7),(6,0),(6,1),(6,2),(7,0),(7,1),(7,2)]  # 9-16
# sqrtnumbers = [(),(),(),(),(),(),(),()] WILL BE USED LATER
# negativenumbers = [(),(),(),(),(),(),(),()] WILL BE USED LATER

# [normal, double, triple, half, negative, negative double, negative triple, sqrt, massive, anti]
flags = [(2,3),(5,2)]
minesIDs = [(2,2),(3,5)]

def getImage(pos):
    """Return the tile at (row, col), scaled to the current cell size (cached)."""
    row, col = pos
    key = (row, col, tile_size)
    if key not in tile_cache:
        tile = image.subsurface(col * 16, row * 16, 16, 16)
        tile_cache[key] = pg.transform.scale(tile, (tile_size, tile_size))
    return tile_cache[key]


def countToImage(count):
    if count == 0:
        return getImage(BLANK)
    elif count == "zero":
        return getImage(numbers[0])
    try:
        return getImage(numbers[count])
    except:
        return getImage(2,7)     # the falseflag image. serves here as an error texture.


class Button:
    def __init__(self, x, y, width, height, action=None, action2=None):
        self.rect = pg.Rect(x, y, width, height)
        self.is_mine = False
        self.mineVar = None
        self.revealed = False
        self.flagged = None
        self.action = action
        self.action2 = action2
        self.image = getImage(UNREVEALED)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 1 and self.action:
                self.action(self)
            elif event.button == 3 and self.action2:
                self.action2(self)


class Input:
    def __init__(self, x, y, w, h, action, max):
        self.rect = pg.Rect(x, y, w, h)
        self.action = action
        self.active = False
        self.text = ""
        self.max = max

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                if self.action:
                    self.action(self.text)
                self.text = ""
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() and len(self.text) < 2:
                self.text += event.unicode
                if int(self.text) > self.max:
                    self.text = str(self.max)
            

    def draw(self, surface):
        border = "white" if self.active else "gray"
        pg.draw.rect(surface, (20, 20, 20), self.rect)
        pg.draw.rect(surface, border, self.rect, width=2)

        label = textfont.render(self.text, True, "white")
        surface.blit(label, (self.rect.x + 10,
                             self.rect.centery - label.get_height() // 2))


def drawText(text, x, y):
    img = textfont.render(text, True, "white")
    screen.blit(img, (x, y))


def neighbors(index):
    """Indexes of all cells touching `index`, with no wrap-around."""
    row, col = divmod(index, cols)
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                result.append(r * cols + c)
    return result


def count_mines(index):
    return sum(buttons[n].is_mine for n in neighbors(index))

def count_mines_inclusive(index):
    count = 0
    for n in neighbors(index):
        if(buttons[n].mineVar == "normal"):
            count+=1
        if(buttons[n].mineVar == "double"):
            count+=2
    return count

def count_flags(index):
    return sum((buttons[n].flagged != None) for n in neighbors(index))

def count_flags_inclusive(index):
    return sum(buttons[n].flagged == "normal" for n in neighbors(index))+(2*sum(buttons[n].flagged == "double" for n in neighbors(index)))

def place_mines(safe_index):
    global mines
    mines = 0
    safe = set(neighbors(safe_index)) | {safe_index}
    candidates = [i for i in range(rows * cols) if i not in safe]
    count = int(max(1, rows * cols * (mine_percentage / 100)))
    count = min(count, len(candidates))
    for i in random.sample(candidates, count):
        buttons[i].is_mine = True
        if random.randint(0,1) == 0:
            buttons[i].mineVar = "normal"
        else:
            buttons[i].mineVar = "double"
        mines+=1

def reveal(start):
    """Reveal a cell; if it has 0 mines around it, keep spreading outward."""

    stack = [start]
    while stack:
        i = stack.pop()
        b = buttons[i]
        if b.revealed or b.flagged != None:
            continue
        b.revealed = True
        count = count_mines_inclusive(i)
        b.image = countToImage(count)
        if count == 0:
            stack.extend(neighbors(i))


def check_for_win():
    # Win = every safe cell has been revealed
    return all(b.revealed for b in buttons if not b.is_mine)


def lose():
    global status
    status = "lose"
    for b in buttons:
        if b.is_mine and b.flagged == None:
            if b.mineVar == "normal":
                b.image = getImage(minesIDs[0])
            elif b.mineVar == "double":
                b.image = getImage(minesIDs[1])


def chord(index):
    """Clicking a revealed number: open all unflagged neighbors if flags match."""
    global status
    mines = count_mines_inclusive(index)
    if mines == 0 or count_flags_inclusive(index) != mines:
        return

    hit_mine = False
    for n in neighbors(index):
        b = buttons[n]
        if b.flagged != None or b.revealed:
            continue
        if b.is_mine:
            b.revealed = True
            hit_mine = True
        else:
            reveal(n)

    if hit_mine:
        lose()
    elif check_for_win():
        status = "win"


def on_click(button):
    global minesSet, status
    if status is not None or button.flagged != None:
        return

    index = buttons.index(button)

    if button.revealed:
        chord(index)
        return

    if not minesSet:
        place_mines(index)
        minesSet = True

    if button.is_mine:
        button.revealed = True
        lose()
        return

    reveal(index)
    if check_for_win():
        status = "win"


def on_rClick(button):
    global mines
    if status is not None or button.revealed:
        return
    
    if button.flagged == None:
        mines -= 1
        button.flagged = "normal"
    elif button.flagged == "normal":
        button.flagged = "double"
        mines -= 1
    else:
        mines += 2
        button.flagged = None

    if button.flagged == "normal":
        button.image = getImage(flags[0])
    elif button.flagged == "double":
        button.image = getImage(flags[1])
    else:
        button.image = getImage(UNREVEALED)



def createButtonList():
    global tile_size
    cellSize = max(1, int(min(650 / cols, 650 / rows)))
    size = max(1, cellSize)
    tile_size = size                 # set BEFORE creating buttons so tiles match
    result = []
    for row in range(rows):
        for col in range(cols):
            result.append(Button(100 + col * cellSize, 25 + row * cellSize,
                                 size, size, on_click, on_rClick))
    return result


def gameReset():
    global buttons, minesSet, status, mines
    buttons = createButtonList()
    minesSet = False
    status = None
    mines = 0


def rowEnter(text):
    global rows
    if text and 1 <= int(text) <= 50:
        rows = int(text)
        gameReset()


def colsEnter(text):
    global cols
    if text and 1 <= int(text) <= 50:
        cols = int(text)
        gameReset()


def mineEnter(text):
    global mine_percentage
    if text and 1 <= int(text) <= 90:
        mine_percentage = int(text)
        gameReset()


rowsInput = Input(800, 475, 80, 40, rowEnter,50)
colsInput = Input(800, 550, 80, 40, colsEnter,50)
minepercentage = Input(800, 625, 80, 40, mineEnter,90)

buttons = createButtonList()
# newGameButton = Button(800, 300, 190, 90, gameReset())

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            gameReset()
        for b in buttons:
            b.handle_event(event)
        rowsInput.handle_event(event)
        colsInput.handle_event(event)
        minepercentage.handle_event(event)

    screen.fill((30, 30, 30))
    for b in buttons:
        b.draw(screen)
    rowsInput.draw(screen)
    colsInput.draw(screen)
    minepercentage.draw(screen)
    # newGameButton.draw(screen)

    drawText("Rows:", 900, 475)
    drawText("Columns:", 900, 550)
    drawText("% Mines:", 900, 625)
    drawText(str(rows),1060,475)
    drawText(str(cols),1060,550)
    drawText(str(mine_percentage),1060,625)
    drawText(str(mines) + " Mines Left",800,400)
    drawText("Press SPACE to Reset", 800, 300)

    # gray while playing, green on win, red on loss
    status_color = {"win": "green", "lose": "red"}.get(status, "gray")
    pg.draw.rect(screen, status_color, (800, 100, 190, 90), border_radius=2)
    drawText("Clear all mines to win!", 800,200)

    pg.display.flip()
    clock.tick(60)

pg.quit()