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
smallfont = pg.font.SysFont("Arial", 18)
pg.key.set_repeat(400, 40)

rows = 12
cols = 12
mine_percentage = 15
minesSet = False
status = None           # None, "win", or "lose"
mines = 0

singles = False
doubles = False
triples = False
singlenegs = False
doublenegs = False
triplenegs = False
megas = False
variationStrings = ["normal", "double", "triple", "negative", "doubleneg", "tripneg", "mega"]
VALUES = {"normal": 1, "double": 2, "triple": 3,
          "negative": -1, "doubleneg": -2, "tripneg": -3,
          "mega": 1}


def get_allowed():
    """Mine types currently enabled by the checkboxes (same order as variationStrings).
    Built fresh on every call so it always reflects the current checkbox state."""
    states = [singles, doubles, triples, singlenegs, doublenegs, triplenegs, megas]
    allowed = [name for on, name in zip(states, variationStrings) if on]
    return allowed or ["normal"]      # fallback if nothing is checked


# (row, col) of each special tile on the sheet
BLANK = (2, 0)
UNREVEALED = (2, 1)
FALSEFLAG = (2, 7)
CHECK = (5, 10)
X = (6, 10)
FORTY = (4, 3) # in 32x32 chunks

# convert_alpha must come after set_mode
image = pg.image.load('minesweepervariants.png').convert_alpha()

tile_size = 45          # updated whenever the grid is rebuilt
tile_cache = {}

# Addresses for assets in the image
numbers = [(5,3),(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),  # 0-8
                 (3,6),(3,7),(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),  # 9-16
                 (6,3),(7,3),(6,4),(7,4),(6,5),(7,5),(6,6),(7,7),  # 17-24
                 (6,7),(6,8),(7,8),(6,9),(7,9),(8,0),(8,1),(8,2),  # 25-32
                 (8,3),(8,4),(9,0),(9,1),(9,2),(9,3),(9,4)]        # 33-39 
negatives = [(2,7),(4,4),(4,5),(4,6),(4,7),(5,4),(5,5),(5,6),(5,7), # -1 - -8 (negatives[0] is FALSEFLAG)
                   (0,8),(0,9),(0,10),(1,8),(1,9),(1,10),(2,8),(2,9), # -9 - -16
                   (2,10),(3,8),(3,9),(3,10),(4,9),(4,10),(5,8),(5,9)] # -17 - -24
# sqrtnumbers = [(),(),(),(),(),(),(),()] WILL BE USED LATER

# [normal, double, triple, half, negative, negative double, negative triple, sqrt, massive, anti]
flags    = [(2,3),(5,2),(5,1),(4,3),(4,2),(4,1),(5,0)]
minesIDs = [(2,2),(3,5),(3,4),(3,3),(3,2),(3,1),(0,5)]

def getImage(pos):
    """Return the tile at (row, col), scaled to the current cell size (cached)."""
    row, col = pos
    key = (row, col, tile_size)
    if key not in tile_cache:
        tile = image.subsurface(col * 16, row * 16, 16, 16)
        tile_cache[key] = pg.transform.scale(tile, (tile_size, tile_size))
    return tile_cache[key]

def getSprite(pos, size=30):
    row, col = pos
    key = ("sprite", row, col, size)
    if key not in tile_cache:
        tile = image.subsurface(col * 16, row * 16, 16, 16)
        tile_cache[key] = pg.transform.scale(tile, (size, size))
    return tile_cache[key]

def getImage40():
    key = (4, 3, tile_size)
    if key not in tile_cache:
        tile = image.subsurface(4 * 16, 3 * 16, 16, 16)
        tile_cache[key] = pg.transform.scale(tile, (tile_size, tile_size))
    return tile_cache[key]


def countToImage(count):
    if count == 0:
        return getImage(BLANK)
    elif count == "zero":
        return getImage(numbers[0])
    elif count < 0:
        count = abs(count)
        return getImage(negatives[count])
    elif count == 40:
        return getImage40()
    try:
        return getImage(numbers[count])
    except IndexError:
        return getImage(FALSEFLAG)     # serves here as an error texture.


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

class Checkbox:
    def __init__(self,x,y,w,h,flip,action=None):

        self.rect = pg.Rect(x,y,w,h)
        self.action = action
        self.state = "unchecked"
        self.flip = flip
        self.set_image(X)

    def set_image(self, pos):
        row, col = pos
        tile = image.subsurface(col * 16, row * 16, 16, 16)
        self.image = pg.transform.scale(tile, self.rect.size)

    def draw(self, surface):
            surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action(self, self.flip)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, value, action=None):
        self.rect = pg.Rect(x, y, w, h)
        self.min = min_val
        self.max = max_val
        self.value = value
        self.action = action
        self.dragging = False

    def _value_from_x(self, mx):
        t = (mx - self.rect.x) / self.rect.w
        t = max(0, min(1, t))                      # clamp to the track
        return round(self.min + t * (self.max - self.min))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 \
                and self.rect.collidepoint(event.pos):
            self.dragging = True
            self.value = self._value_from_x(event.pos[0])
        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.value = self._value_from_x(event.pos[0])
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            if self.action:
                self.action(self.value)            # fire once, on release

    def draw(self, surface):
        y = self.rect.centery
        pg.draw.line(surface, "gray", (self.rect.left, y), (self.rect.right, y), 4)
        t = (self.value - self.min) / (self.max - self.min)
        handle_x = int(self.rect.left + t * self.rect.w)
        pg.draw.circle(surface, "white", (handle_x, y), self.rect.h // 2)

def drawText(text, x, y):
    img = textfont.render(text, True, "white")
    screen.blit(img, (x, y))

def drawSmallText(text,x,y):
    img = smallfont.render(text,True,"white")
    screen.blit(img,(x,y))

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

def meganeighbors(index):
    """Indexes of all cells within 2 tiles of `index`, with no wrap-around."""
    row, col = divmod(index, cols)
    result = []
    for dr in range(-2,3):
        for dc in range(-2,3):
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
        elif(buttons[n].mineVar == "double"):
            count+=2
        elif(buttons[n].mineVar == "triple"):
            count+=3
        elif(buttons[n].mineVar == "negative"):
            count-=1
        elif(buttons[n].mineVar == "doubleneg"):
            count-=2
        elif(buttons[n].mineVar == "tripneg"):
            count-=3
    for n in meganeighbors(index):
        if(buttons[n].mineVar == "mega"):
            count+=1
    return count

def count_flags(index):
    return sum((buttons[n].flagged != None) for n in neighbors(index))

def count_flags_inclusive(index):
    flagCount = 0
    for n in neighbors(index):
        if(buttons[n].flagged == "normal"):
            flagCount += 1
        elif(buttons[n].flagged == "double"):
            flagCount += 2
        elif(buttons[n].flagged == "triple"):
            flagCount += 3
        elif(buttons[n].flagged == "negative"):
            flagCount -= 1
        elif(buttons[n].flagged == "doubleneg"):
            flagCount -= 2
        elif(buttons[n].flagged == "tripneg"):
            flagCount -= 3
    for n in meganeighbors(index):
        if(buttons[n].flagged == "mega"):
            flagCount+=1
    return flagCount


def place_mines(safe_index):
    global mines
    safe = set(neighbors(safe_index)) | {safe_index}
    megasafe = set(meganeighbors(safe_index)) | {safe_index}

    allowed = get_allowed()
    nonmega = [a for a in allowed if a != "mega"]

    # megas only: keep every mine out of the 5x5 zone around the first click
    if nonmega:
        candidates = [i for i in range(rows * cols) if i not in safe]
    else:
        candidates = [i for i in range(rows * cols) if i not in megasafe]

    count = int(max(1, rows * cols * (mine_percentage / 100)))
    count = min(count, len(candidates))   # after candidates is final

    for i in random.sample(candidates, count):
        buttons[i].is_mine = True
        if i in megasafe and nonmega:
            buttons[i].mineVar = random.choice(nonmega)
        else:
            buttons[i].mineVar = random.choice(allowed)

    mines = sum(VALUES[b.mineVar] for b in buttons if b.is_mine) \
        - sum(VALUES[b.flagged] for b in buttons if b.flagged)


def reveal(start):
    # Reveal a cell; if it has 0 mines around it, keep spreading outward.

    stack = [start]
    while stack:
        i = stack.pop()
        b = buttons[i]
        if b.revealed or b.flagged != None:
            continue
        b.revealed = True
        count = count_mines_inclusive(i)
        realcount = count_mines(i)
        if count != 0:
            b.image = countToImage(count)
        elif realcount == 0:
            b.image = countToImage(0)
        else:
            b.image = countToImage("zero")
        if realcount == 0 and count == 0:
            stack.extend(neighbors(i))

def check_for_win(): # will need change when anti introduced
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
            elif b.mineVar == "triple":
                b.image = getImage(minesIDs[2])
            elif b.mineVar == "negative":
                b.image = getImage(minesIDs[3])
            elif b.mineVar == "doubleneg":
                b.image = getImage(minesIDs[4])
            elif b.mineVar == "tripneg":
                b.image = getImage(minesIDs[5])
            elif b.mineVar == "mega":
                b.image = getImage(minesIDs[6])
        elif not b.is_mine and b.flagged is not None:
            b.image = getImage(FALSEFLAG)

def chord(index): # will need changes with anti mine sigh
    """Clicking a revealed number: open all unflagged neighbors if flags match."""
    global status
    if count_mines(index) == 0:
        return
    if count_flags_inclusive(index) != count_mines_inclusive(index):
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

    cycle = [None] + get_allowed()
    old = button.flagged

    if old in cycle:
        new = cycle[(cycle.index(old) + 1) % len(cycle)]   # wraps back to None
    else:
        new = None      # that type was unchecked since flagging, so clear it

    mines += VALUES.get(old, 0) - VALUES.get(new, 0)
    button.flagged = new

    if new is None:
        button.image = getImage(UNREVEALED)
    else:
        button.image = getImage(flags[variationStrings.index(new)])


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


def checked(box, flip):
    global singles, doubles, triples, singlenegs, doublenegs, triplenegs, megas
    if(box.state == "checked"):
        box.state = "unchecked"
        box.set_image(X)
        if flip == 1:
            singles = False
        elif flip == 2:
            doubles = False
        elif flip == 3:
            triples = False
        elif flip == -1:
            singlenegs = False
        elif flip == -2:
            doublenegs = False
        elif flip == -3:
            triplenegs = False
        elif flip == 10:
            megas = False
    else:
        box.state = "checked"
        box.set_image(CHECK)
        if flip == 1:
            singles = True
        elif flip == 2:
            doubles = True
        elif flip == 3:
            triples = True
        elif flip == -1:
            singlenegs = True
        elif flip == -2:
            doublenegs = True
        elif flip == -3:
            triplenegs = True
        elif flip == 10:
            megas = True

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
box1 = Checkbox(855,250,30,30,1,checked)
box2 = Checkbox(920,300,30,30,2,checked)
box3 = Checkbox(920,350,30,30,3,checked)
negbox1 = Checkbox(1010,250,30,30,-1,checked)
negbox2 = Checkbox(1145,300,30,30,-2,checked)
negbox3 = Checkbox(1145,350,30,30,-3,checked)
megabox = Checkbox(1195, 250, 30, 30, 10, checked)
checkboxes = [box1,box2,box3,negbox1,negbox2,negbox3,megabox]
slidermines = Slider(800, 625, 100, 16, 5, 90, mine_percentage, mineEnter)
sliders = [slidermines]

buttons = createButtonList()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            gameReset()
        for b in buttons:
            b.handle_event(event)
        for c in checkboxes:
            c.handle_event(event)
        for d in sliders:
            d.handle_event(event)
        rowsInput.handle_event(event)
        colsInput.handle_event(event)

    screen.fill((30, 30, 30))
    for b in buttons:
        b.draw(screen)
    for c in checkboxes:
        c.draw(screen)
    rowsInput.draw(screen)
    colsInput.draw(screen)
    for d in sliders:
        d.draw(screen)
    # newGameButton.draw(screen)

    drawText("Rows:", 900, 475)
    drawText("Columns:", 900, 550)
    drawText("% Mines:", 920, 625)
    drawText(str(rows),1060,475)
    drawText(str(cols),1060,550)
    drawText(str(slidermines.value),1060,625)   # live value while dragging
    drawText(str(mines) + " Mines Left",800,400)
    drawText("Press SPACE to Reset", 800, 200)

    drawSmallText("Mines", 800, 250)
    screen.blit(getSprite(flags[0]),(890,250))
    drawSmallText("Double Mines", 800, 300)
    screen.blit(getSprite(flags[1]),(955,300))
    drawSmallText("Triple Mines", 800, 350)
    screen.blit(getSprite(flags[2]),(955,350))
    drawSmallText("Negatives", 925,250)
    screen.blit(getSprite(flags[3]),(1045,250))
    drawSmallText("Negative Doubles",1000,300)    
    screen.blit(getSprite(flags[4]),(1180,300))
    drawSmallText("Negative Triples",1000,350)
    screen.blit(getSprite(flags[5]),(1180,350))
    drawSmallText("Mega Mines",1084,250)
    screen.blit(getSprite(flags[6]),(1230,250))


    # gray while playing, green on win, red on loss
    status_color = {"win": "green", "lose": "red"}.get(status, "gray")
    pg.draw.rect(screen, status_color, (800, 50, 190, 90), border_radius=2)
    drawText("Clear all mines to win!", 800,150)



    pg.display.flip()
    clock.tick(60)

pg.quit()